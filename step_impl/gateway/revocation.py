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

from hashlib import sha256
from random import randbytes

from asn1crypto import cms
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests import Response
from step_impl.util import baseurl, certificateFolder

@step("create a revocation list of type <hashtype> with <num_entries> entries")
def create_a_revocation_list_of_type_with_entries(hashtype, num_entries):
    revocation_list = [b64encode(sha256(randbytes(64)).digest()).decode('utf-8') for n in range(int(num_entries))]
    data_store.scenario["revocation.list"] = json.dumps(revocation_list) 


@step("add revocation list recipient <country>")
def add_revocation_list_recipient(country):
    if not "revocation.recipient_certs" in data_store.scenario:
        data_store.scenario["revocation.recipient_list"] = []

    for upload_cert in data_store.scenario['trustlist.UPLOAD']:
        if upload_cert['country'].upper() == country.upper():
            decorated_pem = '-----BEGIN CERTIFICATE-----\n'+upload_cert['rawData']+'\n-----END CERTIFICATE-----\n'
            x509.load_pem_x509_certificate(bytes(decorated_pem,'utf-8'))
            print(upload_cert['kid'])

@step("encrypt and sign CMS as <country>")
def encrypt_and_sign_cms_as(country):
    assert False, "Add implementation code"

@step("upload CMS as <DX>")
def upload_cms_as(DX):
    assert False, "Add implementation code"

@step("download CSM as <DE>")
def download_csm_as(DE):
    assert False, "Add implementation code"