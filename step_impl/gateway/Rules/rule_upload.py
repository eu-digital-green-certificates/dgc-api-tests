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
from base64 import b64decode
from datetime import datetime, timedelta
from os import getcwd, path
from typing import List

import requests
from asn1crypto import cms
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests.exceptions import SSLError
from step_impl.util import baseurl, certificateFolder, FailedResponse
from step_impl.util.certificates import create_cms
from step_impl.util.json import DateTimeEncoder
from step_impl.util.rules import (delete_rule_by_id_with_base_data,
                                  download_rule_of_country, get_rule_id_list)


def add_rule_to_store(rule):
    try:
        rules = data_store.spec["created_rules"]
    except KeyError:
        rules = []
        data_store.spec["created_rules"] = rules
    rules.append(rule)


def get_signed_rule(append_extra_data=False):
    rule = data_store.scenario["rule"]
    
    ruleJson = json.dumps(rule, cls=DateTimeEncoder)
    if append_extra_data:
        ruleJson = ruleJson + ruleJson

    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    return create_cms(ruleJson.encode("utf-8"), upload_cert, upload_key)

@step("upload Rule with extra data")
def upload_rule_with_extra_data():
    return upload_rule(append_extra_data=True)

@step("upload Rule")
def upload_rule(append_extra_data=False):
    data = get_signed_rule(append_extra_data)
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/rules",
                             data=data, headers=headers, cert=(cert_location, key_location))
    data_store.scenario["response"] = response
    # for cleanup later
    if response.ok:
        add_rule_to_store(data_store.scenario["rule"])


@step("upload Rule with cms header")
def upload_rule_with_cms_header():
    data = get_signed_rule()
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/rules",
                             data=data, headers=headers, cert=(cert_location, key_location))
    data_store.scenario["response"] = response
    # for cleanup later
    if response.ok:
        add_rule_to_store(data_store.scenario["rule"])


@step("upload Rule with custom authentication certificate")
def upload_rule_with_custom_authentication_certificate():
    data = get_signed_rule()
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    try:
        response = requests.post(url=baseurl + "/rules",
                             data=data, headers=headers, cert=(cert_location, key_location))
    except SSLError:
        response = FailedResponse()

    data_store.scenario["response"] = response


@step("upload Rule with certificate from another country")
def upload_rule_with_certificate_from_another_country():
    data = get_signed_rule()
    cert_location = path.join(certificateFolder, "secondCountry", "auth.pem")
    key_location = path.join(
        certificateFolder, "secondCountry", "key_auth.pem")
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/rules",
                             data=data, headers=headers, cert=(cert_location, key_location))
    data_store.scenario["response"] = response


@step("check that Rule is in Rulelist")
def check_that_rule_is_in_rulelist():
    csca = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    countryName = csca.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[
        0].value
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    ruleListResponse = download_rule_of_country(
        countryName, cert_location, key_location)
    assert ruleListResponse.ok, f"didn't get a rulelist. Status Code {ruleListResponse.status_code}"
    ruleList = ruleListResponse.json()
    ruleIdList = get_rule_id_list(ruleList)
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    assert ruleId in ruleIdList, f"ruleId '{ruleId}' not in Rulelist '{', '.join(ruleIdList)}'"


@step("check that Rule is not in Rulelist")
def check_that_rule_is_not_in_rulelist():
    csca = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    countryName = csca.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[
        0].value
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    ruleListResponse = download_rule_of_country(
        countryName, cert_location, key_location)
    ruleIdList = get_rule_id_list(ruleListResponse.json())
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    assert not ruleId in ruleIdList, f"ruleId '{ruleId}' should not be in Rulelist '{', '.join(ruleIdList)}'"


@step("delete all created rules")
def delete_all_created_rules():
    try:
        rules: List[Certificate] = data_store.spec["created_rules"]
        for rule in rules:
            ruleId = rule["Identifier"]
            delete_rule_by_id_with_base_data(ruleId)
    except KeyError:
        return
