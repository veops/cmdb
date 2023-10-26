import hvac
from base64 import b64encode, b64decode


class VaultSDK:
    def __init__(self, base_url, token, mount_path):
        self.client = hvac.Client(url=base_url, token=token)
        self.mount_path = mount_path

    def create_approle(self, role_name, policies):
        resp = self.client.create_approle(role_name, policies=policies)
        return resp == 200

    def delete_approle(self, role_name):
        resp = self.client.delete_approle(role_name)
        return resp == 204

    def update_approle_policies(self, role_name, policies):
        resp = self.client.update_approle_role(role_name, policies=policies)
        return resp == 204

    def get_approle(self, role_name):
        resp = self.client.get_approle(role_name)
        resp.json()
        if resp.status_code == 200:
            return resp.json
        else:
            return {}

    def enable_secrets_engine(self):
        resp = self.client.sys.enable_secrets_engine('kv', path=self.mount_path)
        resp_01 = self.client.sys.enable_secrets_engine('transit')

        if resp.status_code == 200 and resp_01.status_code == 200:
            return resp.json
        else:
            return {}

    def encrypt_data(self, plaintext):
        response = self.client.secrets.transit.encrypt_data(name='transit-key', plaintext=plaintext)
        ciphertext = response['data']['ciphertext']
        return ciphertext

    # decrypt data
    def decrypt_data(self, ciphertext):
        response = self.client.secrets.transit.decrypt_data(name='transit-key', ciphertext=ciphertext)
        plaintext = response['data']['plaintext']
        return plaintext

    def write_data(self, path, data, encrypt=None):
        if encrypt:
            for k, v in data.items():
                data[k] = self.encrypt_data(self.encode_base64(v))
        response = self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data,
            mount_point=self.mount_path
        )

        return response

    # read data
    def read_data(self, path, decrypt=None):
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path, raise_on_deleted_version=False, mount_point=self.mount_path
            )
        except Exception as e:
            return str(e), False
        data = response['data']['data']
        if decrypt:
            try:
                for k, v in data.items():
                    data[k] = self.decode_base64(self.decrypt_data(v))
            except Exception:
                return data, True
        return data, True

    # update data
    def update_data(self, path, data, overwrite=None, encrypt=None):
        if encrypt:
            for k, v in data.items():
                data[k] = self.encrypt_data(self.encode_base64(v))
        if overwrite:
            response = self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=self.mount_path
            )
        else:
            response = self.client.secrets.kv.v2.patch(path=path, secret=data, mount_point=self.mount_path)
        return response

    # delete data
    def delete_data(self, path):
        response = self.client.secrets.kv.v2.delete_metadata_and_all_versions(
            path=path,
            mount_point=self.mount_path
        )
        return response

    # Base64 encode
    @classmethod
    def encode_base64(cls, data):
        encoded_bytes = b64encode(data.encode())
        encoded_string = encoded_bytes.decode()
        return encoded_string

    # Base64 decode
    @classmethod
    def decode_base64(cls, encoded_string):
        decoded_bytes = b64decode(encoded_string)
        decoded_string = decoded_bytes.decode()
        return decoded_string


class VaultAppRoleSDK(VaultSDK):
    def __int__(self, base_url, role_id, secret_id):
        self.base_url = base_url
        self.role_id = role_id
        self.secret_id = secret_id
        self.token = self.get_token()
        super(VaultAppRoleSDK, self).__int__(base_url, self.token)


if __name__ == "__main__":
    base_url = "http://localhost:8200"
    token = "hvs.OALuhK2wToxsn2Z1WFnDaKRw"
    mount_path = "cmdb"

    path = "test001"
    # Example
    sdk = VaultSDK(base_url, token, mount_path)
    # sdk.enable_secrets_engine()
    data = {"key1": "value1", "key2": "value2", "key3": "value3"}
    data = sdk.update_data(path, data, overwrite=True, encrypt=True)
    print(data.status_code)
    data = sdk.read_data(path, decrypt=True)
    print(data)
