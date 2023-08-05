# -*- coding: utf-8 -*-
"""Encryption module for providing users an option to not store their DynECT DNS
passwords in plain-text, but rather to provide a means of automatic password
encryption. Note: password encryption requires nothing more than the the
installation of the `PyCrypto <http://www.dlitz.net/software/pycrypto/>`_.
module. Users are free to not install PyCrypto, however, your passwords will not
be encrypted when stored in your session instance
"""
import base64
import random
import hashlib

__author__ = 'jnappi'
__all__ = ['generate_key', 'AESCipher']


def generate_key(force=False):
    """Generate a new, uniquely random, secret key. If we have already created
    one, then return the already created key. You may override this behaviour
    and force a new key to be generated by specifying *force* as *True*

    :param force: A Boolean flag specifying whether or not to force the
        generation of a new key
    """
    if generate_key.secret_key is not None and not force:
        return generate_key.secret_key

    choices = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join([random.SystemRandom().choice(choices) for i in range(50)])
    generate_key.secret_key = key
    return generate_key.secret_key
generate_key.secret_key = None


try:
    from Crypto import Random
    from Crypto.Cipher import AES

    class AESCipher(object):
        """An AES-256 password hasher"""
        def __init__(self, key=None):
            """Create a new AES-256 Cipher instance

            :param key: The secret key used to generate the password hashes
            """
            self.bs = 32
            if key is None:
                key = generate_key()
            self.key = hashlib.sha256(key.encode()).digest()

        def encrypt(self, raw):
            """Encrypt the provided password and return the encoded password
            hash

            :param raw: The raw password string to encode
            """
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        def decrypt(self, enc):
            """Decrypt an encoded password hash using the secret key provided,
            and return the decrypted string

            :param enc: The encoded AES-256 password hash
            """
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s) - 1:])]

except ImportError:
    # If we don't have PyCrypto installed, we won't encrypt passwords
    class AESCipher(object):
        """An AES-256 password hasher"""
        def __init__(self, key=None):
            """Create a new AES-256 Cipher instance

            :param key: The secret key used to generate the password hashes
            """
            self.key = key

        def encrypt(self, raw):
            """Encrypt the provided password and return the encoded password
            hash

            :param raw: The raw password string to encode
            """
            return raw

        def decrypt(self, enc):
            """Decrypt an encoded password hash using the secret key provided,
            and return the decrypted string

            :param enc: The encoded AES-256 password hash
            """
            return enc
