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
from os import path
from random import choice

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests import Response
from step_impl.util import baseurl, certificateFolder


@step("check that DSC is in trustlist")
def check_dsc_is_in_trustlist():
    get_complete_trustlist();
    response = data_store.scenario["response"]
    assert response.ok, "Coudn't get trustlist"
    data = response.json()
    certs_in_trustlist = [x["rawData"] for x in data]
    dscRaw = b64encode(data_store.scenario["dsc"].public_bytes(
        serialization.Encoding.DER)).decode('UTF-8')

    assert dscRaw in certs_in_trustlist, "DSC not in trustlist"


@step("check that DSC is not in trustlist")
def check_that_dsc_is_not_in_trustlist():
    get_complete_trustlist()
    response = data_store.scenario["response"]
    assert response.ok, "Coudn't get trustlist"
    data = response.json()
    certs_in_trustlist = [x["rawData"] for x in data]
    dscRaw = b64encode(data_store.scenario["dsc"].public_bytes(
        serialization.Encoding.DER)).decode('UTF-8')

    assert dscRaw not in certs_in_trustlist, "DSC not in trustlist"

@step("get complete trustlist")
def get_complete_trustlist():
    response = requests.get(baseurl + "/trustList", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that created keys are in trustlist")
def check_that_created_keys_are_in_trustlist():
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert len(data) > 0, "No certificates in trustlist"


@step("get the trustList with the type <type>")
def get_the_trustlist_with_the_type(type):
    response = requests.get(baseurl + f"/trustList/{type}", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that only entries of the type <type> are present")
def check_that_only_entries_of_the_type_are_present(type):
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert all(x == type for x in [y["certificateType"]
               for y in data]), f"found not only type {type}"


@step("get the trustList with the type <type> and country <country>")
def get_the_trustlist_with_the_type_and_country(type, country):
    response = requests.get(baseurl + f"/trustList/{type}/{country}", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that only entries of the type <type> and <country> are present")
def check_that_only_entries_of_the_type_and_county_are_present(type, country):
    check_that_only_entries_of_the_type_are_present(type)
    response: Response = data_store.scenario["response"]
    data = response.json()
    assert all(x == country for x in [y["country"]
               for y in data]), f"found not only country {country}"

@step("get random DSC from trustlist from another country")
def get_random_dsc_from_trustlist_from_another_country():
    trustListResponse: Response = data_store.scenario["response"]
    assert trustListResponse.ok, "Couldn't get trustlist"
    trustList = trustListResponse.json()
    csca_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    country = csca_cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
    randomDsc = choice([x["rawData"] for x in trustList if x["country"] != country])
    data_store.scenario["signed_dsc"] = randomDsc
