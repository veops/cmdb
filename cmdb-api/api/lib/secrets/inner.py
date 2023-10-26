from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import padding
import os
import sys

# global_root_key just for test here
global_root_key = "4OIzj9ztvfu/qUbzUkjvH54jVC0xGyVaWlemotx6PC0="
global_iv_length = 16


def string_to_bytes(value):
    if sys.version_info.major == 2:
        byte_string = value
    else:
        byte_string = value.encode("utf-8")
    return byte_string


class KeyMange:

    def __init__(self):
        pass

    @staticmethod
    def generate_unseal_keys():
        root_key = AESGCM.generate_key(256)
        return root_key

    @staticmethod
    def generate_key():
        return AESGCM.generate_key(256)

    def _acquire(self):
        """
        get encryption key from backend storage
        :return:
        """
        return

    def init(self):
        """
        init the master key, unseal key.
        :return:
        """
    @staticmethod
    def is_seal():
        return global_root_key == b''


class InnerCrypt:
    def __init__(self):
        self.encrypt_key = b64decode(global_root_key.encode("utf-8"))

    def encrypt(self, plaintext):
        status = True
        encrypt_value = self.aes_encrypt(plaintext)
        return encrypt_value, status

    def decrypt(self, ciphertext):
        status = True
        decrypt_value = self.aes_decrypt(ciphertext)
        return decrypt_value, status

    def aes_encrypt(self, plaintext):
        if isinstance(plaintext, str):
            plaintext = string_to_bytes(plaintext)
        iv = os.urandom(global_iv_length)
        cipher = Cipher(algorithms.AES(self.encrypt_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv+ciphertext).decode('utf-8')

    def aes_decrypt(self, ciphertext):
        s = b64decode(ciphertext.encode("utf-8"))
        iv = s[:global_iv_length]
        ciphertext = s[global_iv_length:]
        cipher = Cipher(algorithms.AES(self.encrypt_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(decrypted_padded_plaintext) + unpadder.finalize()
        return plaintext.decode('utf-8')


if __name__ == "__main__":
    t_plaintext = "Hello, World!"  # The plaintext to encrypt
    c = InnerCrypt()
    t_ciphertext = c.aes_encrypt(t_plaintext)
    print("Ciphertext:", t_ciphertext)
    decrypted_plaintext = c.aes_decrypt(t_ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext)
