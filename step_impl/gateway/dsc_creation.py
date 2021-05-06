from base64 import b64encode
from datetime import datetime, timedelta
from os import path

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import Certificate
from getgauge.python import data_store, step

from . import baseurl, certificateFolder, authCerts
from .certificates import create_cms, create_dsc, create_certificate
from .dsc_deletion import delete_dsc


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
    # for cleanup later
    if response.ok:
        add_dsc_to_store(signedDsc)


@step("create custom authentication certificate")
def create_custom_authentication_certificate():
    (cert, key) = create_certificate()
    data_store.scenario["auth_cert"] = cert
    data_store.scenario["auth_key"] = key


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
    authCert = data_store.scenario["auth_cert"]
    authKey = data_store.scenario["auth_key"]
    cert_location = path.join(certificateFolder, "custom_auth.pem")
    key_location = path.join(certificateFolder, "custom_key_auth.pem")
    with open(cert_location, "wb") as f:
        f.write(authCert.public_bytes(serialization.Encoding.PEM))
    with open(key_location, "wb") as f:
        f.write(authKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}
    response = requests.post(url=baseurl + "/signerCertificate",
                             data=signedDsc, headers=headers, cert=(cert_location, key_location))
    data_store.scenario["response"] = response

@step("delete all created certificates")
def delete_all_created_certificates():
    try:
        signedDscs: List[Certificate] = data_store.spec["created_dscs"]
        for dsc in signedDscs:
            delete_dsc(dsc, authCerts)
    except KeyError:
        return