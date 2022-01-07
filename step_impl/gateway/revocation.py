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

from base64 import b64encode

import requests
import json
import uuid

from hashlib import sha256
from random import randbytes

from os import path
from datetime import datetime, timedelta
from asn1crypto import cms
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests import Response
from step_impl.util import baseurl, certificateFolder, secondCountryFolder 
from step_impl.util.certificates import create_cms


REVOCATION_LIST_PATH = '/revocation-list'

@step("create a revocation list of type <hashtype> with <num_entries> entries")
def create_a_revocation_list_of_type_with_entries(hashtype, num_entries):
    #batch_id = str(uuid.uuid4())
    #entries = [b64encode(randbytes(16)).decode('utf-8') for n in range(int(num_entries))]
    entries = [ {'hash':b64encode(randbytes(16)).decode('utf-8')} for n in range(int(num_entries))]
    revocation_list = {
        'country' : 'DX', 
        'expires' : (datetime.now()+timedelta(days=2)).isoformat(timespec='hours') + ':00:00Z',
        'kid' : '0NSBDWlaTng=', 
        'hashType' : hashtype, 
        'entries' : entries
    }
    data_store.scenario["revocation.list"] = json.dumps(revocation_list)  
    #data_store.scenario["revocation.list.batch_id"] = batch_id


@step("sign revocation list")
def sign_revocation_list_as_first_country():
    'Creates a CMS message from the revocation list using the upload cert'
    upload_cert = x509.load_pem_x509_certificate(
        open(data_store.scenario['certs.upload.crt'] , "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(data_store.scenario['certs.upload.key'] , "rb").read(), None)

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
    print("Response: ", response.status_code,  response.text)
    #data_store.scenario["revocation-list.batches"] = response.json()['batches']

@step("download batch with id <batchId>")
def get_revocation_list_batch(batchId):
    response = requests.get(f"{baseurl}{REVOCATION_LIST_PATH}/{batchId}", 
        cert=(data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key']))
    data_store.scenario["response"] = response
    print("Response: ", response.status_code,  response.text)


@step("upload revocation list")
def upload_revocation_list():
    assert "revocation.list.signed" in data_store.scenario

    cert = ( data_store.scenario['certs.auth.crt'], data_store.scenario['certs.auth.key'] )
    if not "rev.lists.created" in data_store.spec:
        data_store.spec["rev.lists.created"] = []

    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64",
               #"ETag" : data_store.scenario["revocation.list.batch_id"],
               }
    response = requests.post(f"{baseurl}{REVOCATION_LIST_PATH}", data=data_store.scenario["revocation.list.signed"], headers=headers, cert=cert)
    print(response.headers)
    data_store.scenario["response"] = response
    print("Response: ", response.status_code,  response.text)
    # for cleanup later
    if response.ok:
        data_store.spec["rev.lists.created"].append( {
            'certs.upload.crt' : data_store.scenario['certs.upload.crt'],
            'certs.upload.key' : data_store.scenario['certs.upload.key'],
            'certs.auth.crt' : data_store.scenario['certs.auth.crt'],
            'certs.auth.key' : data_store.scenario['certs.auth.key'],
            'batch_id' : "6b865013-9c2a-4ff8-ae5c-f2faee7ef905" # response.headers['ETag'],
        } )

@step("delete all uploaded revocation lists")
def delete_all_uploaded_revocation_lists():
    if "rev.lists.created" in data_store.spec:
        for uploaded_batch in data_store.spec["rev.lists.created"]:

            upload_cert = x509.load_pem_x509_certificate(open(uploaded_batch['certs.upload.crt'] , "rb").read())
            upload_key = serialization.load_pem_private_key(open(uploaded_batch['certs.upload.key'] , "rb").read(), None)
            cert = (uploaded_batch['certs.auth.crt'], uploaded_batch['certs.auth.key'])

            payload_json = json.dumps({'batchId':uploaded_batch['batch_id']})
            payload_cms = create_cms(bytes(payload_json, 'utf-8'), upload_cert, upload_key)

            headers = {"Content-Type": "application/cms",
                       "Content-Transfer-Encoding": "base64"}

            response = requests.delete(f"{baseurl}{REVOCATION_LIST_PATH}", data=payload_cms, headers=headers, cert=cert)
            print(f"DELETING batchId={uploaded_batch['batch_id']}  response={response.status_code}, {response.text}")
        
        data_store.spec["rev.lists.created"] = []


