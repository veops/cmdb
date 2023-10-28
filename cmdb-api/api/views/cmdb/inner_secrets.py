from api.resource import APIView
from api.lib.secrets.inner import KeyManage
from api.lib.secrets.secrets import InnerKVManger

from flask import request, abort


class InnerSecretUnSealView(APIView):
    url_prefix = "/secrets/unseal"

    def post(self):
        unseal_key = request.headers.get("Unseal-Token")
        res = KeyManage(backend=InnerKVManger()).unseal(unseal_key)
        # if res.get("status") == "failed":
        #     return abort(400, res.get("message"))
        return self.jsonify(**res)


class InnerSecretSealView(APIView):
    url_prefix = "/secrets/seal"

    def post(self):
        unseal_key = request.headers.get("Inner-Token")
        res = KeyManage(backend=InnerKVManger()).seal(unseal_key)
        # if res.get("status") == "failed":
        #     return abort(400, res.get("message"))
        return self.jsonify(**res)


class InnerSecretAutoSealView(APIView):
    url_prefix = "/secrets/auto_seal"

    def post(self):
        unseal_key = request.headers.get("Inner-Token")
        res = KeyManage(backend=InnerKVManger()).seal(unseal_key)
        # if res.get("status") == "failed":
        #     return abort(400, res.get("message"))
        return self.jsonify(**res)
