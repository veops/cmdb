from api.lib.perm.auth import auth_abandoned
from api.resource import APIView
from api.lib.secrets.inner import KeyManage
from api.lib.secrets.secrets import InnerKVManger

from flask import current_app
from flask import request


class InnerSecretUnSealView(APIView):
    url_prefix = "/secrets/unseal"

    @auth_abandoned
    def post(self):
        unseal_key = request.headers.get("Unseal-Token")
        res = KeyManage(backend=InnerKVManger()).unseal(unseal_key)
        return self.jsonify(**res)


class InnerSecretSealView(APIView):
    url_prefix = "/secrets/seal"

    @auth_abandoned
    def post(self):
        unseal_key = request.headers.get("Inner-Token")
        res = KeyManage(backend=InnerKVManger()).seal(unseal_key)
        return self.jsonify(**res)


class InnerSecretAutoSealView(APIView):
    url_prefix = "/secrets/auto_seal"

    @auth_abandoned
    def post(self):
        root_key = request.headers.get("Inner-Token")
        res = KeyManage(trigger=root_key,
                        backend=InnerKVManger()).auto_unseal()
        return self.jsonify(**res)
