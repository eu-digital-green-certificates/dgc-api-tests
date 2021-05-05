from base64 import b64encode
from datetime import datetime, timedelta
from os import path

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import Certificate
from getgauge.python import data_store, step

from . import baseurl, certificateFolder
from .certificates import create_cms, create_dsc


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

    data_store.scenario["signed_dsc"] = create_cms(
        dsc_cert, upload_cert, upload_key)


@step("sign DSC with UPLOAD certificate of another country")
def sign_dsc_with_upload_certificate_of_another_country():
    dsc_cert = data_store.scenario["dsc"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "secondCountry", "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "secondCountry", "key_upload.pem"), "rb").read(), None)

    data_store.scenario["signed_dsc"] = create_cms(
        dsc_cert, upload_cert, upload_key)


@step("upload DSC")
def upload_public_key():
    signedDsc = data_store.scenario["signed_dsc"]
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/signerCertificate", data=signedDsc, headers=headers, cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("upload DSC as text")
def upload_dsc_as_text():
    signedDsc = data_store.scenario["signed_dsc"]
    headers = {"Content-Type": "text/plain"}
    response = requests.post(url=baseurl + "/signerCertificate", data=signedDsc, headers=headers, cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("upload unsigned DSC")
def upload_unsigned_dsc():
    dsc: Certificate = data_store.scenario["dsc"]
    data = b64encode(dsc.public_bytes(serialization.Encoding.DER))
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/signerCertificate", data=data, headers=headers, cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    data_store.scenario["response"] = response


@step("check that DSC is in trustlist")
def check_dsc_is_in_trustlist():
    response = requests.get(url=baseurl + "/trustList", cert=(
        path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem")))
    assert response.status_code == 200, "Coudn't get trustlist"
    data = response.json()
    certs_in_trustlist = [x["rawData"] for x in data]
    dscRaw = b64encode(data_store.scenario["dsc"].public_bytes(
        serialization.Encoding.DER)).decode('UTF-8')

    assert dscRaw in certs_in_trustlist, "DSC not in trustlist"


@step("upload DSC without client certificate")
def upload_dsc_without_client_certificate():
    dsc_cert = data_store.scenario["dsc"]
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    body = create_cms(dsc_cert, upload_cert, upload_key)
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(
        url=baseurl + "/signerCertificate", data=body, headers=headers)
    data_store.scenario["response"] = response
