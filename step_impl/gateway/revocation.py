# ---license-start
# eu-digital-green-certificates / dgc-api-tests
# ---
# Copyright (C) 2021 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end

import json
from base64 import b64encode
from datetime import datetime, timedelta, timezone
from random import randbytes

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import data_store, step

from step_impl.util import baseurl
from step_impl.util.certificates import create_cms

REVOCATION_LIST_PATH = '/revocation-list'


@step("create a revocation list of type <hashtype> with <num_entries> entries in short format")
def create_a_revocation_list_short(hashtype, num_entries):
    return create_a_revocation_list_of_type_with_entries(hashtype, num_entries, short_format=True)


@step("create a revocation list of type <hashtype> with <num_entries> entries for country <country>")
def create_a_revocation_list_short(hashtype, num_entries, country):
    return create_a_revocation_list_of_type_with_entries(hashtype, num_entries, country=country)


@step("create revocation list: type=<hashtype>, entries=<num_entries>, expiry=<days>")
def create_a_revocation_list_of_type_with_entries(hashtype, num_entries, days=2, short_format=False, country='DX'):
    if short_format:
        entries = [b64encode(randbytes(16)).decode('utf-8') for _ in range(int(num_entries))]
    else:
        entries = [{'hash': b64encode(randbytes(16)).decode('utf-8')} for _ in range(int(num_entries))]
    revocation_list = {
        'country': country,
        'expires': (datetime.now() + timedelta(days=int(days))).isoformat(timespec='hours') + ':00:00Z',
        'kid': '0NSBDWlaTng=',
        'hashType': hashtype,
        'entries': entries
    }

    # print(f"Revocation list: {revocation_list}")
    data_store.scenario["revocation.list"] = json.dumps(revocation_list)


@step("sign revocation list")
def sign_revocation_list_as_first_country():
    """Creates a CMS message from the revocation list using the upload cert"""
    upload_cert = x509.load_pem_x509_certificate(
        open(data_store.scenario['certs.upload.crt'], "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(data_store.scenario['certs.upload.key'], "rb").read(), None)

    revocation_list = data_store.scenario["revocation.list"]

    data_store.scenario["revocation.list.signed"] = create_cms(
        bytes(revocation_list, 'utf-8'), upload_cert, upload_key)

    return data_store.scenario["revocation.list.signed"]


@step("download revocation list from <days> days ago")
def download_revocation_list_from_days_ago(days):
    pivot_date = datetime.now() - timedelta(days=int(days))
    date_str = pivot_date.isoformat(timespec='hours') + ':00:00Z'
    return get_revocation_list(if_modified_since=date_str)


def get_revocation_list(if_modified_since='2021-06-01T00:00:00Z'):
    response = requests.get(f"{baseurl}{REVOCATION_LIST_PATH}",
                            headers={'If-Modified-Since': if_modified_since},
                            cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
    data_store.scenario["response"] = response
    # print("Response: ", response.status_code, response.text)
    return response


@step("check that only results from <days> days ago are in the response")
def check_that_only_results_from_days_ago_are_in_the_response(days):
    pivot_date = datetime.now(timezone.utc) - timedelta(days=int(days))
    for batch in data_store.scenario["response"].json()["batches"]:
        batch_date = datetime.fromisoformat(batch["date"])
        assert batch_date >= pivot_date


@step("download batch with id <batchId>")
def get_revocation_list_batch(batch_id):
    response = requests.get(f"{baseurl}{REVOCATION_LIST_PATH}/{batch_id}",
                            cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
    data_store.scenario["response"] = response
    return response


@step("upload revocation list")
def upload_revocation_list():
    assert "revocation.list.signed" in data_store.scenario

    cert = (data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'])
    if "rev.lists.created" not in data_store.spec:
        data_store.spec["rev.lists.created"] = []

    headers = {"Content-Type": "application/cms", "Content-Transfer-Encoding": "base64"}
    response = requests.post(f"{baseurl}{REVOCATION_LIST_PATH}", data=data_store.scenario["revocation.list.signed"],
                             headers=headers, cert=cert)
    data_store.scenario["response"] = response
    # print(f"Post-Batch: status={response.status_code}, header={response.headers}, text={response.text}")
    # for cleanup later
    if response.ok:
        data_store.scenario["revocation.list.batch_id"] = response.headers['ETag']
        data_store.spec["rev.lists.created"].append({
            'certs.upload.crt': data_store.scenario['certs.upload.crt'],
            'certs.upload.key': data_store.scenario['certs.upload.key'],
            'certs.auth.crt': data_store.scenario['certs.auth.crt'],
            'certs.auth.key': data_store.scenario['certs.auth.key'],
            'batch_id': response.headers['ETag']
        })


@step("delete all uploaded revocation lists using alternate endpoint")
def delete_all_uploaded_revocation_lists_using_alternate_endpoint():
    delete_all_uploaded_revocation_lists(alternate_endpoint=True)


@step("delete all uploaded revocation lists using current certificates")
def delete_all_uploaded_revocation_lists_using_current_certificates():
    delete_all_uploaded_revocation_lists(use_upload_certs=False)


@step("delete all uploaded revocation lists")
def delete_all_uploaded_revocation_lists(alternate_endpoint=False, use_upload_certs=True):
    if "rev.lists.deleted" not in data_store.spec:
        data_store.scenario["rev.lists.deleted"] = []
    if "rev.lists.deleted_ids" not in data_store.spec:
        data_store.scenario["rev.lists.deleted_ids"] = []
    if "rev.lists.created" in data_store.spec:
        for uploaded_batch in data_store.spec["rev.lists.created"]:
            cert_and_key_container = uploaded_batch if use_upload_certs else data_store.scenario
            upload_cert = x509.load_pem_x509_certificate(
                open(cert_and_key_container['certs.upload.crt'], "rb").read())
            upload_key = serialization.load_pem_private_key(
                open(cert_and_key_container['certs.upload.key'], "rb").read(), None)
            cert = (cert_and_key_container['certs.auth.crt'], cert_and_key_container['certs.auth.key'])

            payload_json = json.dumps({'batchId': uploaded_batch['batch_id']})
            payload_cms = create_cms(bytes(payload_json, 'utf-8'), upload_cert, upload_key)

            headers = {"Content-Type": "application/cms", "Content-Transfer-Encoding": "base64"}

            if alternate_endpoint:
                response = requests.post(f"{baseurl}{REVOCATION_LIST_PATH}/delete",
                                         data=payload_cms, headers=headers, cert=cert)
            else:
                response = requests.delete(f"{baseurl}{REVOCATION_LIST_PATH}",
                                           data=payload_cms, headers=headers, cert=cert)

            # print(f"DELETED batchId={uploaded_batch['batch_id']}  response={response.status_code}, {response.text}")
            data_store.scenario["rev.lists.deleted"].append(response)
            data_store.scenario["rev.lists.deleted_ids"].append(uploaded_batch['batch_id'])

        data_store.spec["rev.lists.created"] = []


@step("check that deleted batches are <empty_if_positive> deleted")
def check_that_deleted_batches_are_deleted(empty_if_positive=''):
    batches = data_store.scenario["response"].json()["batches"]
    for batch_id in get_and_clear_list("rev.lists.deleted_ids"):
        batch = find_batch(batch_id=lambda: batch_id, batches=lambda: batches)
        assert not empty_if_positive == batch['deleted'], f"Batch {batch_id} has not been deleted"


@step("check that deletion responses are <empty_if_positive> ok")
def check_deletion_responses(empty_if_positive=''):
    for resp in get_and_clear_list("rev.lists.deleted"):
        assert not empty_if_positive == resp.ok, f'{resp.text} ok={resp.ok} expected ok={bool(empty_if_positive)}'


@step("batch can be found")
def find_batch(batch_id=lambda: data_store.scenario["revocation.list.batch_id"],
               batches=lambda: data_store.scenario["response"].json()["batches"]):
    for batch in batches():
        if batch_id() == batch['batchId']:
            return batch
    assert False, f"Couldn't find batch {batch_id()} in {batches()}"


def get_and_clear_list(name):
    assert name in data_store.scenario, f"{name} was not in data_store.scenario"
    result = data_store.scenario[name]
    data_store.scenario[name] = []
    return result
