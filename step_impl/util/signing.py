import cbor2
from cose.keys.curves import P256
from cose.keys.ec2 import EC2Key
from cose.keys.rsa import RSAKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from base45 import b45encode
from cose.headers import KID, Algorithm
from cose.messages.sign1message import Sign1Message
from zlib import compress

edgcPrefix = 'HC1:'

def get_rsa_key_from_private_key(key: RSAPrivateKey) -> RSAKey:
    private_numbers = key.private_numbers()
    p = private_numbers.p.to_bytes(
        (private_numbers.p.bit_length() + 7) // 8, byteorder='big')
    q = private_numbers.q.to_bytes(
        (private_numbers.q.bit_length() + 7) // 8, byteorder='big')
    d = private_numbers.d.to_bytes(
        (private_numbers.d.bit_length() + 7) // 8, byteorder='big')
    dp = private_numbers.dmp1.to_bytes(
        (private_numbers.dmp1.bit_length() + 7) // 8, byteorder='big')
    dq = private_numbers.dmq1.to_bytes(
        (private_numbers.dmq1.bit_length() + 7) // 8, byteorder='big')
    qinv = private_numbers.iqmp.to_bytes(
        (private_numbers.iqmp.bit_length() + 7) // 8, byteorder='big')

    public_numbers = private_numbers.public_numbers

    n = public_numbers.n.to_bytes(
        (public_numbers.n.bit_length() + 7) // 8, byteorder='big')
    e = public_numbers.e.to_bytes(
        (public_numbers.e.bit_length() + 7) // 8, byteorder='big')

    return RSAKey(n=n, e=e, d=d, p=p, q=q, dp=dp, dq=dq, qinv=qinv)



def get_ec_key_from_private_key(key: EllipticCurvePrivateKey):
    d_value = key.private_numbers().private_value
    x_coor = key.public_key().public_numbers().x
    y_coor = key.public_key().public_numbers().y
    crv = P256()
    return EC2Key(crv=crv,
                  d=d_value.to_bytes(crv.size, "big"),
                  x=x_coor.to_bytes(crv.size, "big"),
                  y=y_coor.to_bytes(crv.size, "big"))


def cose_sign(cborData: bytes, signKey, algorithm, kid: bytes):
    msg = Sign1Message(
        phdr={Algorithm: algorithm, KID: kid},
        payload=cborData,
        key=signKey
    )
    return msg.encode()


def sign_and_encode_dcc(certData, signKey, algorithm, kid: bytes):
    cbor_data = cbor2.dumps(certData)
    coseData = cose_sign(cbor_data, signKey, algorithm, kid)
    compressedCoseData = compress(coseData)
    base45data = b45encode(compressedCoseData)
    return f"{edgcPrefix}{base45data.decode('utf-8')}"
