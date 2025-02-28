import sha3
import ethereum
from eth_utils import is_hex_address
from django import forms
from ethereum.utils import ecrecover_to_pub
from eth_utils import to_checksum_address

def sig_to_vrs(sig):
    #    sig_bytes = bytes.fromhex(sig[2:])
    r = int(sig[2:66], 16)
    s = int(sig[66:130], 16)
    v = int(sig[130:], 16)
    return v, r, s


def hash_personal_message(msg):
    padded = "\x19Ethereum Signed Message:\n" + str(len(msg)) + msg
    return sha3.keccak_256(bytes(padded, 'utf8')).digest()


def recover_to_addr(msg, sig):
    msghash = hash_personal_message(msg)
    vrs = sig_to_vrs(sig)
    return to_checksum_address('0x' + sha3.keccak_256(ecrecover_to_pub(msghash, *vrs)).hexdigest()[24:])


def validate_eth_address(value):
    if not is_hex_address(value):
        raise forms.ValidationError(
            '%s is not a valid Ethereum address' % value,
            params={'value': value},
        )
