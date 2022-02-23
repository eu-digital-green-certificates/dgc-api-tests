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

import base64
import requests
import ecdsa
import json
import jwt
from ecdsa.curves import NIST256p
from os import path
from uuid import uuid4
from datetime import datetime, timedelta
from getgauge.python import data_store, step
from datetime import datetime
from step_impl.util import validationServiceUrl, callbackServer
from step_impl.util.signing import sign_and_encode_dcc

from hashlib import sha256
from cose.algorithms import Es256, Ps256
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from ecdsa.util import sigencode_der
from random import randbytes, choice
from string import digits, ascii_uppercase

from step_impl.util.signing import sign_and_encode_dcc
from step_impl.util.signing import get_ec_key_from_private_key
from step_impl.util.signing import get_rsa_key_from_private_key

_DECORATOR_KEY_FILE = 'key_decorator.pem'
_DECORATOR_KEY_KID_FILE = 'key_decorator.kid'
_CERTIFICATES_FOLDER = 'certificates'

# Defaults 

_DEFAULT_GIVENNAME = 'Vorname'
_DEFAULT_FAMILYNAME = 'Nachname'
_DEFAULT_DOB = '1990-01-01'
_DEFAULT_VACCINE = 'EU/1/20/1528'
_DEFAULT_VAC_MANUFACTURER = 'ORG-100030215'
_DEFAULT_COUNTRY = 'DE'



@step("The validation service must be available")
def the_validation_service_must_be_available():
    services = requests.get( validationServiceUrl ).json()
    assert "verificationMethod" in services

    # Get the validation service encryption key and save it in the session
    # It will be used to encrypt the symmetric key which encrypts the DCC before transmission to the service
    for method in services["verificationMethod"]:
        if method["id"].endswith("ValidationServiceEncKey-1"):
            data_store.scenario["validatorkey"] = method["publicKeyJwk"]["x5c"]
            data_store.scenario["validatorkey:obj"] = RSA.import_key(f'-----BEGIN CERTIFICATE-----\n{method["publicKeyJwk"]["x5c"]}\n-----END CERTIFICATE-----')
            data_store.scenario["validatorkey:kid"] = method["publicKeyJwk"]["kid"]
            break
    
    assert "validatorkey" in data_store.scenario

def _random_uvci():
    random_part = ''.join( choice(ascii_uppercase + digits) for x in range(26) )
    return f'URN:UVCI:V1:{_DEFAULT_COUNTRY}:{random_part}'

@step("Create a recovery payload")
def create_a_recovery_payload():
    payload = {-260: {1: {'dob': _DEFAULT_DOB,
            'nam': {'fn': _DEFAULT_FAMILYNAME,
                    'fnt': _DEFAULT_FAMILYNAME.upper(),
                    'gn': _DEFAULT_GIVENNAME,
                    'gnt': _DEFAULT_GIVENNAME.upper()},
            'r': [{'ci': _random_uvci(),
                   'co': _DEFAULT_COUNTRY,
                   'df': '2021-10-01',
                   'du': '2022-11-01',
                   'fr': '2021-11-01',
                   'is': 'Testarzt T-Systems',
                   'tg': '840539006'}],
            'ver': '1.3.0'}},
        1: 'DE',
        6: 1600000000,
        4: 1700000000}
    data_store.scenario["dcc_payload"] = payload


@step("Create a vaccination payload")
def create_vaccination_payload():
    payload = {-260: {1: {'dob': _DEFAULT_DOB,
            'nam': {'fn': _DEFAULT_FAMILYNAME,
                    'fnt': _DEFAULT_FAMILYNAME.upper(),
                    'gn': _DEFAULT_GIVENNAME,
                    'gnt': _DEFAULT_GIVENNAME.upper()},
            'v': [{'ci': _random_uvci(),
                   'co': _DEFAULT_COUNTRY,
                   'dn': 2,
                   'dt': '2021-08-01',
                   'is': 'Impfzentrum T-Systems',
                   'ma': _DEFAULT_VAC_MANUFACTURER,
                   'mp': _DEFAULT_VACCINE,
                   'sd': 2,
                   'tg': '840539006',
                   'vp': '1119305005'}],
            'ver': '1.3.0'}},
        1: 'DE',
        6: 1600000000,
        4: 1700000000}
    data_store.scenario["dcc_payload"] = payload


@step("Set rDCC field <fieldname> to <value>")
def set_vdcc_field( fieldname, value ):
    data_store.scenario["dcc_payload"][-260][1]['r'][0][fieldname] = value


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
    #print(data_store.scenario["dcc_signed"])

@step("Start a new checkin procedure with callback")
def new_checkin_procedure_with_cb():
    return new_checkin_procedure(callback=True)

@step("Start a new checkin procedure")
def new_checkin_procedure(callback=False):
    sc = data_store.scenario
    sc["subject"] = str(uuid4())
    sc["userkey"] = ecdsa.SigningKey.generate(curve=NIST256p,hashfunc=sha256)

    sc["decoratorkey"] = open(path.join(_CERTIFICATES_FOLDER,_DECORATOR_KEY_FILE)).read()
    sc["decoratorkey:kid"] = open(path.join(_CERTIFICATES_FOLDER,_DECORATOR_KEY_KID_FILE)).read().strip()
    #print(sc['decoratorkey:kid'])

    for keyType in ['initialize','status']:
        sc[f"{keyType}key"] =  jwt.encode({
                                  "sub": sc['subject'],
                                  "exp": int(datetime(2030,12,31).timestamp()),
                                  "iat":0,
                                  "aud": f"{validationServiceUrl}/{keyType}/{sc['subject']}"
                                  },
                                  sc["decoratorkey"], algorithm="ES256", headers={"kid":sc["decoratorkey:kid"]})

    # Initialize the checkin
    body = {    "keyType":"ES256",
                "pubKey": sc["userkey"].get_verifying_key().to_pem().decode(), 
                "nonce": base64.b64encode(bytes(16)).decode() } 
    if callback:
        body['callback'] = f"{callbackServer}/{sc['subject']}"
    headers = {"content-type": "application/json","Authorization":"Bearer "+sc['initializekey'], "X-Version":"1.0"}    
    #print(body, headers)            
    response = requests.put( f"{validationServiceUrl}/initialize/{sc['subject']}", data=json.dumps(body), headers=headers )
    #print(response.status_code, response.text, response.headers)
    assert response.ok

    # Filling the validation context with defaults, so only test case specific data needs to be overwritten
    sc['validationContext'] = {
                "lang":"en",
                "fnt":_DEFAULT_FAMILYNAME.upper(),
                "gnt":_DEFAULT_GIVENNAME.upper(),
                "dob":_DEFAULT_DOB,
                "validationClock": datetime.now().isoformat(),
                "validFrom": datetime.now().isoformat(),
                "validTo": (datetime.now() + timedelta(days=2)).isoformat(),
                "type":["v","r"], # 2G-Regel
                "category" : ["Standard"]
                }

@step("Set departure country <COD>")
def set_departure_country(COD):
    data_store.scenario['validationContext']['cod'] = COD
    data_store.scenario['validationContext']['rod'] = COD

@step("Set arrival country <COA>")
def set_arrival_country(COA):
    data_store.scenario['validationContext']['coa'] = COA
    data_store.scenario['validationContext']['roa'] = COA

@step("Set departure date <dateISO>")
def set_departure_date(dateISO):
    data_store.scenario['validationContext']['validFrom'] = datetime.fromisoformat(dateISO).isoformat()+"+01:00"
    data_store.scenario['validationContext']['validationClock'] = (datetime.fromisoformat(dateISO)+timedelta(hours=8)).isoformat()+"+01:00"

@step("Set arrival date <dateISO>")
def set_arrival_date(dateISO):
    recoded_date = datetime.fromisoformat(dateISO).isoformat()+"+01:00"
    data_store.scenario['validationContext']['validTo'] = recoded_date

@step("Validate DCC")
def validate_dcc():
    sc = data_store.scenario

    password = randbytes(32)
            
    cipher = PKCS1_OAEP.new(sc['validatorkey:obj'],hashAlgo=SHA256)
    cryptKey = cipher.encrypt(password)
    aesCipher = AES.new(password, AES.MODE_CBC,iv=bytes(16))
    ciphertext= aesCipher.encrypt(pad(bytes(sc["dcc_signed"],'utf-8'),AES.block_size))
    signature = sc["userkey"].sign(ciphertext,hashfunc=SHA256.new,sigencode=sigencode_der)

    validateToken = jwt.encode({
                                  "jti":str(uuid4()),
                                  "sub":sc['subject'],
                                  "exp":int(datetime(2030,12,31).timestamp()),
                                  "aud": f"{validationServiceUrl}/validate/{sc['subject']}",
                                  "t": 2,
                                  "v":"1.0",
                                  "vc":sc['validationContext']
                                  },
                                  sc["decoratorkey"], algorithm="ES256",headers={"kid":sc["decoratorkey:kid"]})

    headers = {'content-type': 'application/json', "Authorization":"Bearer " + validateToken,"X-Version":"1.0"}


    body = {"kid":sc['validatorkey:kid'],
                "dcc":base64.b64encode(ciphertext).decode(),
                "sig":base64.b64encode(signature).decode(),
                "sigAlg":"EC",
                "encKey":base64.b64encode(cryptKey).decode(),
                "encScheme":"RSAOAEPWithSHA256AESCBC",
                "sigAlg":"SHA256withECDSA"}

    response = requests.post( f"{validationServiceUrl}/validate/{sc['subject']}", data=json.dumps(body), headers=headers )
    if not response.ok:
        print(response.status_code, response.text)
    assert response.ok
    #print(f'Validate result: {response.status_code}')

    headers = {"Authorization":"Bearer "+sc['statuskey'],"X-Version":"1.0"}
    response = requests.get(f"{validationServiceUrl}/status/{sc['subject']}", headers=headers )
    assert response.ok
    sc['validation:status'] = jwt.decode(response.content, options={"verify_signature":False})
    print("\n",sc['validation:status']['result'],sc['validation:status']['results'])


@step("Check that the result is valid")
def check_that_the_result_is_valid():
    assert data_store.scenario['validation:status']['result'] == 'OK'

@step("Check that the result is invalid")
def check_that_the_result_is_invalid():
    assert data_store.scenario['validation:status']['result'] in ('NOK','CHK')

@step("Check that callback result is identical to polling result")
def check_that_callback_result_is_identical_to_polling_result():
    sc = data_store.scenario
    response = requests.get(url=f"{callbackServer}/{sc['subject']}")
    assert response.ok
    callback_status = jwt.decode(response.content, options={"verify_signature":False})
    assert callback_status == sc['validation:status']
