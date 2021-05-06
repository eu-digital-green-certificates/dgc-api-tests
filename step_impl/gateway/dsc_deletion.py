from os import path
from random import choice

import requests
from getgauge.python import data_store, step
from requests import Response

from . import authCerts, baseurl, certificateFolder
from cryptography.hazmat.primitives import serialization


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
    response = delete_dsc(dscToDelete, (cert_location, key_location))
    data_store.scenario["response"] = response
