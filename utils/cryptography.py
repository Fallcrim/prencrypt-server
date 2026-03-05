from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def verify_signature(signature: bytes, data: bytes, pubkey: bytes) -> bool:
    """
    Validates an RSA signature
    :param signature:
    :param data:
    :param pubkey:
    :return:
    """
    data_hash = SHA256.new(data)
    verifier = pss.new(RSA.import_key(pubkey))
    try:
        verifier.verify(data_hash, signature)
        return True
    except ValueError:
        return False


def generate_signature(data: bytes, pubkey: bytes) -> bytes:
    """
    Generates an RSA signature
    :param data:
    :param pubkey:
    :return:
    """
    data_hash = SHA256.new(data)
    verifier = pss.new(RSA.import_key(pubkey))
    signature = verifier.sign(data_hash)
    return signature
