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

import requests
import ecdsa
import jwt
from ecdsa.curves import NIST256p
from os import path
from uuid import uuid4
from datetime import datetime, timedelta
from getgauge.python import data_store, step
from datetime import datetime
from step_impl.util import validationServiceUrl
from step_impl.util.signing import sign_and_encode_dcc

from hashlib import sha256
from cose.algorithms import Es256, Ps256
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from step_impl.util.signing import sign_and_encode_dcc
from  step_impl.util.signing import get_ec_key_from_private_key
from  step_impl.util.signing import get_rsa_key_from_private_key

_DECORATOR_KEY_FILE = 'key_decorator.pem'
_CERTIFICATES_FOLDER = 'certificates'

@step("The validation service must be available")
def the_validation_service_must_be_available():
    services = requests.get( validationServiceUrl ).json()
    assert "verificationMethod" in services


@step("Create a vaccination payload")
def create_vaccination_payload():
    payload = {-260: {1: {'dob': '1990-01-01',
            'nam': {'fn': 'Nachname',
                    'fnt': 'NACHNAME',
                    'gn': 'Vorname',
                    'gnt': 'VORNAME'},
            'v': [{'ci': 'URN:UVCI:V1:DE:8IUW3BRPRGIKP1C3C8EHGGEBNY',
                   'co': 'DE',
                   'dn': 1,
                   'dt': '2021-08-01',
                   'is': 'Impfzentrum T-Systems',
                   'ma': 'ORG-100001699',
                   'mp': 'EU/1/21/1529',
                   'sd': 2,
                   'tg': '840539006',
                   'vp': '1119305005'}],
            'ver': '1.3.0'}},
        1: 'DX',
        6: 1609455600,
        4: 1672441200}

    data_store.scenario["dcc_payload"] = payload

@step("Set vDCC field <fieldname> to <value>")
def set_vdcc_field( fieldname, value ):
    data_store.scenario["dcc_payload"][-260][1]['v'][0][fieldname] = value

@step("Set vDCC dose <dn> of <sd>")
def set_vdcc_dose_no( dn, sd ):
    data_store.scenario["dcc_payload"][-260][1]['v'][0]["dn"] = int(dn)
    data_store.scenario["dcc_payload"][-260][1]['v'][0]["sd"] = int(sd)

@step("Add claim keys valid from <issued_at> until <valid_until>")
def add_claim_keys( issued_at, valid_until ):
    data_store.scenario["dcc_payload"][4] = int(datetime.fromisoformat(valid_until).timestamp())
    data_store.scenario["dcc_payload"][6] = int(datetime.fromisoformat(issued_at).timestamp())

@step("Sign with DSC of <country_code>")
def sign_with_dsc(country_code):
    with open(path.join(".", _CERTIFICATES_FOLDER, f"dsc-{country_code}", "dsc.crt"), "rb") as f:
        dscCert = x509.load_pem_x509_certificate(f.read())
    with open(path.join(".", _CERTIFICATES_FOLDER, f"dsc-{country_code}", "dsc.key"), "rb") as f:
        dscKey = serialization.load_pem_private_key(f.read(), None)
    fingerprint = dscCert.fingerprint(hashes.SHA256())
    kid = fingerprint[:8]
    if isinstance(dscKey, RSAPrivateKey):
        key = get_rsa_key_from_private_key(dscKey)
        algorithm = Ps256
    else:
        key = get_ec_key_from_private_key(dscKey)
        algorithm = Es256
    data_store.scenario["dcc_signed"] = sign_and_encode_dcc(data_store.scenario["dcc_payload"], key, algorithm, kid )
    print(data_store.scenario["dcc_signed"])

@step("Start a new checkin procedure")
def new_checkin_procedure():
    sc = data_store.scenario
    sc["subject"] = str(uuid4())
    sc["userkey"] = ecdsa.SigningKey.generate(curve=NIST256p,hashfunc=sha256)
    sc["decoratorkey"] = open(path.join(_CERTIFICATES_FOLDER,_DECORATOR_KEY_FILE)).read()
    for keyType in ['initialize','status']:
        sc[f"{keyType}key"] =  jwt.encode({
                                  "sub": sc['subject'],
                                  "exp": int(datetime(2030,12,31).timestamp()),
                                  "iat":0,
                                  "aud": f"{validationServiceUrl}/{keyType}/{sc['subject']}"
                                  },
                                  sc["decoratorkey"], algorithm="ES256")

    # Initialize the checkin
    body = {    "keyType":"ES256",
                "pubKey": sc["userkey"].get_verifying_key().to_pem().decode(), 
                "nonce": str(uuid4())}
    headers = {"Authorization":"Bearer "+sc['initializekey'], "X-Version":"1.0"}                
    response = requests.put( f"{validationServiceUrl}/initialize/{sc['subject']}", json=body, headers=headers )
    print(response.status_code, response.text)
    assert response.ok


@step("Set departure country <DX>")
def set_departure_country(DX):
    pass

@step("Set arrival country <DE>")
def set_arrival_country(DE):
    pass

@step("Set departure date <2021-12-01>")
def set_departure_date(arg1):
    pass

@step("Set arrival date <2021-12-01>")
def set_arrival_date(arg1):
    pass

@step("Validate DCC")
def validate_dcc():
    pass

@step("Check that the result is valid")
def check_that_the_result_is_valid():
    pass

@step("Check that the result is invalid")
def check_that_the_result_is_invalid():
    pass


