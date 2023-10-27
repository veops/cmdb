from api.resource import APIView
from api.models.cmdb import InnerKV
from api.lib.secrets.inner import KeyMange

from flask import request, abort


class InnerSecretUnSealView(APIView):
    url_prefix = "/secrets/unseal"

    def post(self):
        unseal_key = request.headers.get("Inner-Token")
        res = KeyMange(InnerKV()).unseal(unseal_key)
        if res.get("status") == "failed":
            return abort(400, res.get("message"))
        return self.jsonify(**res)


class InnerSecretSealView(APIView):
    url_prefix = "/secrets/seal"

    def post(self):
        unseal_key = request.headers.get("Inner-Token")
        res = KeyMange(InnerKV()).seal(unseal_key)
        if res.get("status") == "failed":
            return abort(400, res.get("message"))
        return self.jsonify(**res)
