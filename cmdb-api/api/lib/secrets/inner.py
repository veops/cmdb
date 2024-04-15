import json
import os
import secrets
import sys
import threading

from base64 import b64decode, b64encode
from Cryptodome.Protocol.SecretSharing import Shamir
from colorama import Back, Fore, Style, init as colorama_init
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import current_app

global_iv_length = 16
global_key_shares = 5  # Number of generated key shares
global_key_threshold = 3  # Minimum number of shares required to rebuild the key

backend_root_key_name = "root_key"
backend_encrypt_key_name = "encrypt_key"
backend_root_key_salt_name = "root_key_salt"
backend_encrypt_key_salt_name = "encrypt_key_salt"
backend_seal_key = "seal_status"

success = "success"
seal_status = True

secrets_encrypt_key = ""
secrets_root_key = ""

def string_to_bytes(value):
    if not value:
        return ""
    if isinstance(value, bytes):
        return value
    if sys.version_info.major == 2:
        byte_string = value
    else:
        byte_string = value.encode("utf-8")
    return byte_string


class Backend:
    def __init__(self, backend=None):
        self.backend = backend
        # cache is a redis object
        self.cache = backend.cache

    def get(self, key):
        return self.backend.get(key)

    def add(self, key, value):
        return self.backend.add(key, value)

    def update(self, key, value):
        return self.backend.update(key, value)

    def get_shares(self, key):
        return self.backend.get_shares(key)

    def set_shares(self, key, value):
        return self.backend.set_shares(key, value)


class KeyManage:

    def __init__(self, trigger=None, backend=None):
        self.trigger = trigger
        self.backend = backend
        self.share_key = "cmdb::secret::secrets_share"
        if backend:
            self.backend = Backend(backend)

    def init_app(self, app, backend=None):
        if (sys.argv[0].endswith("gunicorn") or
                (len(sys.argv) > 1 and sys.argv[1] in ("run", "cmdb-password-data-migrate"))):

            self.backend = backend
            threading.Thread(target=self.watch_root_key, args=(app,)).start()

            self.trigger = app.config.get("INNER_TRIGGER_TOKEN")
            if not self.trigger:
                return

            resp = self.auto_unseal()
            self.print_response(resp)

    def hash_root_key(self, value):
        algorithm = hashes.SHA256()
        salt = self.backend.get(backend_root_key_salt_name)
        if not salt:
            salt = secrets.token_hex(16)
            msg, ok = self.backend.add(backend_root_key_salt_name, salt)
            if not ok:
                return msg, ok

        kdf = PBKDF2HMAC(
            algorithm=algorithm,
            length=32,
            salt=string_to_bytes(salt),
            iterations=100000,
        )
        key = kdf.derive(string_to_bytes(value))

        return b64encode(key).decode('utf-8'), True

    def generate_encrypt_key(self, key):
        algorithm = hashes.SHA256()
        salt = self.backend.get(backend_encrypt_key_salt_name)
        if not salt:
            salt = secrets.token_hex(32)

        kdf = PBKDF2HMAC(
            algorithm=algorithm,
            length=32,
            salt=string_to_bytes(salt),
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(string_to_bytes(key))
        msg, ok = self.backend.add(backend_encrypt_key_salt_name, salt)
        if ok:
            return b64encode(key).decode('utf-8'), ok
        else:
            return msg, ok

    @classmethod
    def generate_keys(cls, secret):
        shares = Shamir.split(global_key_threshold, global_key_shares, secret, False)
        new_shares = []
        for share in shares:
            t = [i for i in share[1]] + [ord(i) for i in "{:0>2}".format(share[0])]
            new_shares.append(b64encode(bytes(t)))

        return new_shares

    def is_valid_root_key(self, root_key):
        if not root_key:
            return False
        root_key_hash, ok = self.hash_root_key(root_key)
        if not ok:
            return root_key_hash, ok
        backend_root_key_hash = self.backend.get(backend_root_key_name)
        if not backend_root_key_hash:
            return "should init firstly", False
        elif backend_root_key_hash != root_key_hash:
            return "invalid root key", False
        else:
            return "", True

    def auth_root_secret(self, root_key, app):
        with app.app_context():
            msg, ok = self.is_valid_root_key(root_key)
            if not ok:
                return {
                    "message": msg,
                    "status": "failed"
                }

            encrypt_key_aes = self.backend.get(backend_encrypt_key_name)
            if not encrypt_key_aes:
                return {
                    "message": "encrypt key is empty",
                    "status": "failed"
                }

            secret_encrypt_key, ok = InnerCrypt.aes_decrypt(string_to_bytes(root_key), encrypt_key_aes)
            if ok:
                msg, ok = self.backend.update(backend_seal_key, "open")
                if ok:
                    global secrets_encrypt_key, secrets_root_key
                    secrets_encrypt_key = secret_encrypt_key
                    secrets_root_key = root_key
                    self.backend.cache.set(self.share_key, json.dumps([]))
                    return {"message": success, "status": success}
                return {"message": msg, "status": "failed"}
            else:
                return {
                    "message": secret_encrypt_key,
                    "status": "failed"
                }

    def parse_shares(self, shares, app):
        if len(shares) >= global_key_threshold:
            recovered_secret = Shamir.combine(shares[:global_key_threshold], False)
            return self.auth_root_secret(b64encode(recovered_secret), app)

    def unseal(self, key):
        if not self.is_seal():
            return {
                "message": "current status is unseal, skip",
                "status": "skip"
            }

        try:
            t = [i for i in b64decode(key)]
            v = (int("".join([chr(i) for i in t[-2:]])), bytes(t[:-2]))
            shares = self.backend.get_shares(self.share_key)
            if v not in shares:
                shares.append(v)
                self.set_shares(shares)
            if len(shares) >= global_key_threshold:
                return self.parse_shares(shares, current_app)
            else:
                return {
                    "message": "waiting for inputting other unseal key {0}/{1}".format(len(shares),
                                                                                       global_key_threshold),
                    "status": "waiting"
                }
        except Exception as e:
            return {
                "message": "invalid token: " + str(e),
                "status": "failed"
            }

    def generate_unseal_keys(self):
        info = self.backend.get(backend_root_key_name)
        if info:
            return "already exist", [], False

        secret = AESGCM.generate_key(128)
        shares = self.generate_keys(secret)

        return b64encode(secret), shares, True

    def init(self):
        """
        init the master key, unseal key and store in backend
        :return:
        """
        root_key = self.backend.get(backend_root_key_name)
        if root_key:
            return {"message": "already init, skip", "status": "skip"}, False
        else:
            root_key, shares, status = self.generate_unseal_keys()
            if not status:
                return {"message": root_key, "status": "failed"}, False

            # hash root key and store in backend
            root_key_hash, ok = self.hash_root_key(root_key)
            if not ok:
                return {"message": root_key_hash, "status": "failed"}, False

            msg, ok = self.backend.add(backend_root_key_name, root_key_hash)
            if not ok:
                return {"message": msg, "status": "failed"}, False

            # generate encrypt key from root_key and store in backend
            encrypt_key, ok = self.generate_encrypt_key(root_key)
            if not ok:
                return {"message": encrypt_key, "status": "failed"}

            encrypt_key_aes, status = InnerCrypt.aes_encrypt(root_key, encrypt_key)
            if not status:
                return {"message": encrypt_key_aes, "status": "failed"}

            msg, ok = self.backend.add(backend_encrypt_key_name, encrypt_key_aes)
            if not ok:
                return {"message": msg, "status": "failed"}, False
            msg, ok = self.backend.add(backend_seal_key, "open")
            if not ok:
                return {"message": msg, "status": "failed"}, False

            global secrets_encrypt_key, secrets_root_key
            secrets_encrypt_key = encrypt_key
            secrets_root_key = root_key

            self.print_token(shares, root_token=root_key)

            return {"message": "OK",
                    "details": {
                        "root_token": root_key,
                        "seal_tokens": shares,
                    }}, True

    def auto_unseal(self):
        if not self.trigger:
            return {
                "message": "trigger config is empty, skip",
                "status": "skip"
            }

        if self.trigger.startswith("http"):
            return {
                "message": "todo in next step, skip",
                "status": "skip"
            }
            #  TODO
        elif len(self.trigger.strip()) == 24:
            res = self.auth_root_secret(self.trigger.encode(), current_app)
            if res.get("status") == success:
                return {
                    "message": success,
                    "status": success
                }
            else:
                return {
                    "message": res.get("message"),
                    "status": "failed"
                }
        else:
            return {
                "message": "trigger config is invalid, skip",
                "status": "skip"
            }

    def seal(self, root_key):
        root_key = root_key.encode()
        msg, ok = self.is_valid_root_key(root_key)
        if not ok:
            return {
                "message": msg,
                "status": "failed"
            }
        else:
            msg, ok = self.backend.update(backend_seal_key, "block")
            if not ok:
                return {
                    "message": msg,
                    "status": "failed",
                }
            self.clear()
            self.backend.cache.publish(self.share_key, "clear")

            return {
                "message": success,
                "status": success
            }

    @staticmethod
    def clear():
        global secrets_encrypt_key, secrets_root_key
        secrets_encrypt_key = ''
        secrets_root_key = ''

    def is_seal(self):
        """
        If there is no initialization or the root key is inconsistent, it is considered to be in a sealed state..
        :return:
        """
        # secrets_root_key = current_app.config.get("secrets_root_key")
        if not secrets_root_key:
            return True
        msg, ok = self.is_valid_root_key(secrets_root_key)
        if not ok:
            return True
        status = self.backend.get(backend_seal_key)
        return status == "block"

    @classmethod
    def print_token(cls, shares, root_token):
        """
        data: {"message": "OK",
               "details": {
                    "root_token": root_key,
                    "seal_tokens": shares,
              }}
        """
        colorama_init()
        print(Style.BRIGHT, "Please be sure to store the Unseal Key in a secure location and avoid losing it."
                            " The Unseal Key is required to unseal the system every time when it restarts."
                            " Successful unsealing is necessary to enable the password feature." + Style.RESET_ALL)

        for i, v in enumerate(shares):
            print(
                "unseal token " + str(i + 1) + ": " + Fore.RED + Back.BLACK + v.decode("utf-8") + Style.RESET_ALL)
            print()

        print(Fore.GREEN + "root token:  " + root_token.decode("utf-8") + Style.RESET_ALL)

    @classmethod
    def print_response(cls, data):
        status = data.get("status", "")
        message = data.get("message", "")
        status_colors = {
            "skip": Style.BRIGHT,
            "failed": Fore.RED,
            "waiting": Fore.YELLOW,
        }
        print(status_colors.get(status, Fore.GREEN), message, Style.RESET_ALL)

    def set_shares(self, values):
        new_value = list()
        for v in values:
            new_value.append((v[0], b64encode(v[1]).decode("utf-8")))
        self.backend.cache.publish(self.share_key, json.dumps(new_value))
        self.backend.cache.set(self.share_key, json.dumps(new_value))

    def watch_root_key(self, app):
        pubsub = self.backend.cache.pubsub()
        pubsub.subscribe(self.share_key)

        new_value = set()
        for message in pubsub.listen():
            if message["type"] == "message":
                if message["data"] == b"clear":
                    self.clear()
                    continue
                try:
                    value = json.loads(message["data"].decode("utf-8"))
                    for v in value:
                        new_value.add((v[0], b64decode(v[1])))
                except Exception as e:
                    return []
                if len(new_value) >= global_key_threshold:
                    self.parse_shares(list(new_value), app)
                    new_value = set()


class InnerCrypt:
    def __init__(self):
        self.encrypt_key = b64decode(secrets_encrypt_key)
        #self.encrypt_key = b64decode(secrets_encrypt_key, "".encode("utf-8"))

    def encrypt(self, plaintext):
        """
        encrypt method contain aes currently
        """
        if not self.encrypt_key:
            return ValueError("secret is disabled, please seal firstly"), False
        return self.aes_encrypt(self.encrypt_key, plaintext)

    def decrypt(self, ciphertext):
        """
        decrypt method contain aes currently
        """
        if not self.encrypt_key:
            return ValueError("secret is disabled, please seal firstly"), False
        return self.aes_decrypt(self.encrypt_key, ciphertext)

    @classmethod
    def aes_encrypt(cls, key, plaintext):
        if isinstance(plaintext, str):
            plaintext = string_to_bytes(plaintext)
        iv = os.urandom(global_iv_length)
        try:
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            v_padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_plaintext = v_padder.update(plaintext) + v_padder.finalize()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

            return b64encode(iv + ciphertext).decode("utf-8"), True
        except Exception as e:

            return str(e), False

    @classmethod
    def aes_decrypt(cls, key, ciphertext):
        try:
            s = b64decode(ciphertext.encode("utf-8"))
            iv = s[:global_iv_length]
            ciphertext = s[global_iv_length:]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decrypter = cipher.decryptor()
            decrypted_padded_plaintext = decrypter.update(ciphertext) + decrypter.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(decrypted_padded_plaintext) + unpadder.finalize()

            return plaintext.decode('utf-8'), True
        except Exception as e:
            return str(e), False


if __name__ == "__main__":

    km = KeyManage()
    # info, shares, status = km.generate_unseal_keys()
    # print(info, shares, status)
    # print("..................")
    # for i in shares:
    #     print(b64encode(i[1]).decode())

    res1, ok1 = km.init()
    if not ok1:
        print(res1)
    # for j in res["details"]["seal_tokens"]:
    #     r = km.unseal(j)
    #     if r["status"] != "waiting":
    #         if r["status"] != "success":
    #             print("r........", r)
    #         else:
    #             print(r)
    #         break

    t_plaintext = b"Hello, World!"  # The plaintext to encrypt
    c = InnerCrypt()
    t_ciphertext, status1 = c.encrypt(t_plaintext)
    print("Ciphertext:", t_ciphertext)
    decrypted_plaintext, status2 = c.decrypt(t_ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext)