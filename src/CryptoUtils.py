
import base64

from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def generateKeyPair() -> 'str, str, RsaKey':
    """Generates a pair of public keys

    Returns:
        str, str, RsaKey: returns the public key, the private key and the pair
    """
    pair = RSA.generate(1024)

    public_key = strip_pem_public_data(pair.publickey().export_key())
    private_key = strip_pem_private_data(pair.export_key())

    return public_key, private_key, pair


def firm_data(data, private_key) -> str:
    """Firms data with a private key

    Args:
        data (_type_): the data to firm
        private_key (_type_): the private key to firm the data with

    Returns:
        str: the firm on base64 encoded string
    """
    message_hash = SHA1.new(data)
    signer = PKCS1_v1_5.new(private_key)

    return base64.b64encode(signer.sign(message_hash))


def strip_pem_public_data(key) -> str:
    """Convenient method to remove pem strings from public key

    Args:
        key (_type_): the pem public key

    Returns:
        str: the public key
    """
    return ''.join(key.decode("utf-8").split()[3:-3])


def strip_pem_private_data(key) -> str:
    """Convenient method to remove pem strings from private key

    Args:
        key (_type_): the pem private key

    Returns:
        str: the private key
    """
    return ''.join(key.decode("utf-8").split()[4:-4])