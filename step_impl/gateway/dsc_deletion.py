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
from random import choice

import requests
from cryptography.hazmat.primitives import serialization
from getgauge.python import data_store, step
from requests import Response
from step_impl.util import authCerts, baseurl, certificateFolder, FailedResponse
from requests.exceptions import SSLError

def delete_dsc(signedDsc: str, authCerts: (str, str)):
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.delete(
        url=baseurl + "/signerCertificate", data=signedDsc, headers=headers, cert=authCerts)
    return response


@step("delete DSC created")
def delete_dsc_created():
    signedDsc = data_store.scenario["signed_dsc"]
    response = delete_dsc(signedDsc, authCerts)
    data_store.scenario["response"] = response


@step("delete DSC created using alias Endpoint")
def delete_dsc_created_using_alias_endpoint():
    signedDsc = data_store.scenario["signed_dsc"]
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(
        url=baseurl + "/signerCertificate/delete", data=signedDsc, headers=headers, cert=authCerts)
    data_store.scenario["response"] = response


@step("delete DSC from another country")
def delete_dsc_from_another_country():
    delete_dsc_created()


@step("delete random DSC with custom client certificate")
def revoke_random_dsc_of_trustlist_with_unauthorized_authentication_certificate():
    trustListResponse: Response = data_store.scenario["response"]
    assert trustListResponse.ok, "Couldn't get trustlist"
    trustList = trustListResponse.json()
    dscToDelete = choice(trustList)["rawData"]
    cert = data_store.scenario["auth_cert"]
    key = data_store.scenario["auth_key"]
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    with open(cert_location, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(key_location, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    try:
        response = delete_dsc(dscToDelete, (cert_location, key_location))
    except SSLError:
        response = FailedResponse()

    data_store.scenario["response"] = response
