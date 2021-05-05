from base64 import b64encode
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.x509 import Certificate
from cryptography.x509.oid import NameOID


def create_dsc(csca_cert: Certificate, csca_key: RSAPrivateKey):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    issuer = csca_cert.issuer

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"DE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,
                           u"Nothrhine Westphalia"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Essen"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                           u"T-Systems International"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"api-test"),
    ])
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(
        x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(seconds=10)).sign(csca_key, hashes.SHA256())
    return cert


def create_cms(dsc_cert: Certificate, upload_cert: Certificate, upload_key: RSAPrivateKey):

    options = [pkcs7.PKCS7Options.Binary]

    builder = pkcs7.PKCS7SignatureBuilder().set_data(
        dsc_cert.public_bytes(serialization.Encoding.DER))
    signed = builder.add_signer(upload_cert, upload_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    return b64encode(signed)
