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
from datetime import datetime, timedelta
from os import path

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import Certificate
from getgauge.python import data_store, step
from step_impl.gateway.dsc_deletion import delete_dsc
from step_impl.util import authCerts, baseurl, certificateFolder, FailedResponse
from requests.exceptions import SSLError
from step_impl.util.certificates import (create_certificate,
                                         create_cms_with_certificate,
                                         create_dsc)


def add_dsc_to_store(dsc: str):
    try:
        dscs = data_store.spec["created_dscs"]
    except KeyError:
        dscs = []
        data_store.spec["created_dscs"] = dscs
    dscs.append(dsc)

@step("create a valid DSC")
def create_valid_dsc():
    csca_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "csca.pem"), "rb").read())
    csca_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_csca.pem"), "rb").read(), None)

    cert = create_dsc(csca_cert, csca_key)
    data_store.scenario["dsc"] = cert


@step("create a DSC for another country")
def create_a_dsc_for_another_country():
    csca_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "secondCountry", "csca.pem"), "rb").read())
    csca_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "secondCountry", "key_csca.pem"), "rb").read(), None)

    cert = create_dsc(csca_cert, csca_key)
    data_store.scenario["dsc"] = cert


@step("sign DSC with UPLOAD certificate")
def sign_dsc_with_upload_certificate():
    dsc_cert = data_store.scenario["dsc"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)

    data_store.scenario["signed_dsc"] = create_cms_with_certificate(
        dsc_cert, upload_cert, upload_key)


@step("sign DSC with UPLOAD certificate of another country")
def sign_dsc_with_upload_certificate_of_another_country():
    dsc_cert = data_store.scenario["dsc"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "secondCountry", "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "secondCountry", "key_upload.pem"), "rb").read(), None)

    data_store.scenario["signed_dsc"] = create_cms_with_certificate(
        dsc_cert, upload_cert, upload_key)


@step("upload DSC")
def upload_public_key():
    signedDsc = data_store.scenario["signed_dsc"]
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/signerCertificate", data=signedDsc, headers=headers, cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response
    # for cleanup later
    if response.ok:
        add_dsc_to_store(signedDsc)


@step("create custom authentication certificate")
def create_custom_authentication_certificate():
    (cert, key) = create_certificate()
    data_store.scenario["auth_cert"] = cert
    data_store.scenario["auth_key"] = key
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


@step("upload unsigned DSC")
def upload_unsigned_dsc():
    dsc: Certificate = data_store.scenario["dsc"]
    data = b64encode(dsc.public_bytes(serialization.Encoding.DER))
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/signerCertificate", data=data, headers=headers, cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("upload DSC with custom client certificate")
def upload_dsc_with_custom_client_certificate():
    signedDsc = data_store.scenario["signed_dsc"]
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    try:
        response = requests.post(url=baseurl + "/signerCertificate",
                             data=signedDsc, headers=headers, cert=(cert_location, key_location))
    except SSLError:
        response = FailedResponse()

    data_store.scenario["response"] = response


@step("delete all created certificates")
def delete_all_created_certificates():
    try:
        signedDscs: List[Certificate] = data_store.spec["created_dscs"]
        for dsc in signedDscs:
            delete_dsc(dsc, authCerts)
    except KeyError:
        return
