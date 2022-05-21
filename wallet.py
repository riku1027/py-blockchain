import base58
import codecs
import hashlib

from ecdsa import NIST256p
from ecdsa import SigningKey

import utils


class Wallet(object):

    def __init__(self):
        # 1. creating a publick key with ECDSA.
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    ## NOTE: Generate block chain address according to Bitcoin specification \
    #  to keep the address length as short as possible.
    #  FYI: https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
    ##
    def generate_blockchain_address(self):
        # NOTE: bpk equal "byte private key"

        # 2: SHA-256 for the public key
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        # 3: Ripemd 160 for the SHA-256
        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

        # 4: Add Network byte
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemed160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex'
        )

        # 5: Doublce SHA-256
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        # 6: Get checksum
        checksum = sha256_hex[:8]

        # 7: Concatenate public key and checsum
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')

        # 8: Encoding the key with Base 58
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')

        return blockchain_address

if __name__ == '__main__':
    wallet = Wallet()
    print('private key', wallet.private_key)
    print('public key', wallet.public_key)
