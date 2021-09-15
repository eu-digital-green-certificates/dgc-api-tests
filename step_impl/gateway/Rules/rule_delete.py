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
from os import path

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from getgauge.python import data_store, step
from requests import Response
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from step_impl.util import baseurl, certificateFolder, FailedResponse
from step_impl.util.rules import delete_rule_by_id
from step_impl.util.certificates import create_cms, get_own_country_name
from requests.exceptions import SSLError




def delete_rule_by_id_for_teststeps(ruleId: str, upload_cert: Certificate, upload_key: RSAPrivateKey, tls_cert_location: str, tls_key_location: str) -> Response:
    response = delete_rule_by_id(ruleId, upload_cert, upload_key, tls_cert_location, tls_key_location)
    data_store.scenario["response"] = response


@step("delete Rule")
def delete_rule():
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    delete_rule_by_id_for_teststeps(
        ruleId, upload_cert, upload_key, cert_location, key_location)


@step("delete Rule using alias Endpoint")
def delete_rule_using_alias_endpoint():
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    data = create_cms(ruleId.encode("utf-8"), upload_cert, upload_key)
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/rules/delete",
                               data=data, headers=headers, cert=(cert_location, key_location))
    data_store.scenario["response"] = response


@step("delete Rule with certificate of another country")
def delete_rule_with_certificate_of_another_country():
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    cert_location = path.join(certificateFolder, "secondCountry", "auth.pem")
    key_location = path.join(
        certificateFolder, "secondCountry", "key_auth.pem")
    delete_rule_by_id_for_teststeps(
        ruleId, upload_cert, upload_key, cert_location, key_location)

@step("delete Rule created with custom client certificate")
def delete_rule_created_with_custom_client_certificate():
    rule = data_store.scenario["rule"]
    ruleId = rule["Identifier"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    try:
        delete_rule_by_id_for_teststeps(
            ruleId, upload_cert, upload_key, cert_location, key_location)
    except SSLError:
        data_store.scenario["response"] = FailedResponse()



@step("delete Rule not in rulelist")
def delete_rule_not_in_rulelist():
    countryName = get_own_country_name()
    ruleId = f"GR-{countryName}-9999"
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    cert_location = path.join(certificateFolder, "auth.pem")
    key_location = path.join(certificateFolder, "key_auth.pem")
    delete_rule_by_id_for_teststeps(
        ruleId, upload_cert, upload_key, cert_location, key_location)
