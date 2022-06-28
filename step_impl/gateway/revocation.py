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
from requests.exceptions import SSLError
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import data_store, step

from step_impl.util import baseurl, FailedResponse
from step_impl.util.certificates import create_cms

REVOCATION_LIST_PATH = '/revocation-list'


@step("create a revocation batch of type <hashtype> with <num_entries> entries in short format")
def create_a_revocation_list_short(hashtype, num_entries):
    return create_a_revocation_list_of_type_with_entries(hashtype, num_entries, short_format=True)


@step("create a revocation batch of type <hashtype> with <num_entries> entries for country <country>")
def create_a_revocation_list_short(hashtype, num_entries, country):
    return create_a_revocation_list_of_type_with_entries(hashtype, num_entries, country=country)


@step("create revocation batch: type=<hashtype>, entries=<num_entries>, expiry=<days>")
def create_a_revocation_list_of_type_with_entries(hashtype, num_entries, days=2, short_format=False, country='DX'):
    if short_format:
        entries = [b64encode(randbytes(16)).decode('utf-8') for _ in range(int(num_entries))]
    else:
        entries = [{'hash': b64encode(randbytes(16)).decode('utf-8')} for _ in range(int(num_entries))]
    revocation_list = {
        'country': country,
        'expires': (datetime.now() + timedelta(days=int(days))).isoformat(timespec='hours') + ':00:00Z',
        'kid': b64encode(randbytes(8)).decode('utf-8'),
        'hashType': hashtype,
        'entries': entries
    }

    # print(f"Revocation list: {revocation_list}")
    data_store.scenario["revocation.list"] = json.dumps(revocation_list)


@step("sign revocation batch")
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
    pivot_date = datetime.utcnow() - timedelta(days=int(days))
    date_str = pivot_date.isoformat(timespec='hours') + ':00:00Z'
    return get_revocation_list(if_modified_since=date_str)


@step("download revocation list from <minutes> minutes ago")
def download_revocation_list_from_days_ago(minutes):
    pivot_date = datetime.utcnow() - timedelta(minutes=int(minutes))
    date_str = pivot_date.isoformat(timespec='hours') + ':00:00Z'
    return get_revocation_list(if_modified_since=date_str)


def get_revocation_list(if_modified_since='2021-06-01T00:00:00Z'):
    try: 
        response = requests.get(f"{baseurl}{REVOCATION_LIST_PATH}",
                            headers={'If-Modified-Since': if_modified_since},
                            cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
    except SSLError:
        response = FailedResponse()    
    data_store.scenario["response"] = response
    return response


@step("check that only results from <days> days ago are in the response")
def check_that_only_results_from_days_ago_are_in_the_response(days):
    pivot_date = datetime.now(timezone.utc) - timedelta(days=int(days))
    for batch in data_store.scenario["response"].json()["batches"]:
        batch_date = datetime.fromisoformat(batch["date"])
        assert batch_date >= pivot_date


@step("download uploaded batch")
def get_revocation_list_batch():
    try:
        response = requests.get(f"{baseurl}{REVOCATION_LIST_PATH}/{data_store.scenario['revocation.list.batch_id']}",
                            cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
        data_store.scenario["response"] = response
    except SSLError:
        data_store.scenario["response"] = FailedResponse()

    return  data_store.scenario["response"]


@step("upload revocation batch")
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


@step("delete uploaded revocation batches using alternate endpoint")
def delete_all_uploaded_revocation_lists_using_alternate_endpoint():
    delete_all_uploaded_revocation_lists(alternate_endpoint=True)


@step("delete uploaded revocation batches using current certificates")
def delete_all_uploaded_revocation_lists_using_current_certificates():
    delete_all_uploaded_revocation_lists(use_upload_certs=False)


@step("delete uploaded revocation batches")
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


@step("check that deleted batches are not deleted")
def check_that_deleted_batches_are_not_deleted():
    check_that_deleted_batches_are_deleted(should_be_deleted=False)


@step("check that deleted batches are deleted")
def check_that_deleted_batches_are_deleted(should_be_deleted=True):
    batches = data_store.scenario["response"].json()["batches"]
    for batch_id in get_and_clear_list("rev.lists.deleted_ids"):
        batch = find_batch(batch_id=lambda: batch_id, batches=lambda: batches)
        assert should_be_deleted == batch['deleted'], f"Batch {batch_id} deletion status should be {should_be_deleted} but is {batch['deleted']}"


@step("check that deletion responses are not ok")
def check_deletion_responses_are_not_ok():
    check_deletion_responses(should_be_okay=False)


@step("check that deletion responses are ok")
def check_deletion_responses(should_be_okay=True):
    for resp in get_and_clear_list("rev.lists.deleted"):
        assert should_be_okay == resp.ok, f'{resp.text} ok={resp.ok} expected ok={should_be_okay}'


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


@step("check that there are more batches")
def check_that_there_are_more_batches():
    assert data_store.scenario["response"].json()["more"], "There should be more batches on the gw for this Test-Case."


@step("check that revocation list is full")
def check_that_revocation_list_is_full():
    assert len(data_store.scenario["response"].json()["batches"]) == 1000, "List should contain 1000 batches"


@step("check that batches are sorted by ascending date")
def check_that_batches_are_sorted_by_ascending_date():
    last_date = None
    for batch in data_store.scenario["response"].json()["batches"]:
        batch_date = datetime.fromisoformat(batch["date"])
        assert last_date is None or batch_date >= last_date
        last_date = batch_date


@step("download revocation list with If-Modified-Since after last list")
def download_revocation_list_with_modified_since_after_last_list():
    last_batch = data_store.scenario["response"].json()["batches"][-1]
    data_store.scenario["last_batch"] = last_batch
    batch_date = datetime.fromisoformat(last_batch['date'])
    date_str = batch_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return get_revocation_list(if_modified_since=date_str)


@step("check that revocation list is not empty")
def check_that_revocation_list_is_not_empty():
    assert data_store.scenario["response"].json()["batches"], "List should not be empty"


@step("check that the last batch from the last revocation list is not in the new list")
def check_that_last_batch_from_last_revocation_list_is_not_in_the_new_list():
    for batch in data_store.scenario['response'].json()['batches']:
        assert batch['batchId'] != data_store.scenario['last_batch']['batchId']


@step("upload <batches> batches for country <country>")
def upload_batches_for_country(batches, country='DX'):
    for i in range(int(batches)):
        create_a_revocation_list_of_type_with_entries("SIGNATURE", 1, days=2, country=country)
        sign_revocation_list_as_first_country()
        upload_revocation_list()
        assert data_store.scenario["response"].ok, "Response should be ok"
        print(f"Uploaded batch {i}: {data_store.scenario['revocation.list.batch_id']}")
