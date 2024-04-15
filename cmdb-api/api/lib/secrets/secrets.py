import base64
import json

from api.models.cmdb import InnerKV
from api.extensions import rd


class InnerKVManger(object):
    def __init__(self):
        self.cache = rd.r
        pass

    @classmethod
    def add(cls, key, value):
        data = {"key": key, "value": value}
        res = InnerKV.create(**data)
        if res.key == key:
            return "success", True

        return "add failed", False

    @classmethod
    def get(cls, key):
        res = InnerKV.get_by(first=True, to_dict=False, key=key)
        if not res:
            return None

        return res.value

    @classmethod
    def update(cls, key, value):
        res = InnerKV.get_by(first=True, to_dict=False, key=key)
        if not res:
            return cls.add(key, value)

        t = res.update(value=value)
        if t.key == key:
            return "success", True

        return "update failed", True

    @classmethod
    def get_shares(cls, key):
        new_value = list()
        v = rd.get_str(key)
        if not v:
            return new_value
        try:
            value = json.loads(v.decode("utf-8"))
            for v in value:
                new_value.append((v[0], base64.b64decode(v[1])))
        except Exception as e:
            return []
        return new_value

    @classmethod
    def set_shares(cls, key, value):
        new_value = list()
        for v in value:
            new_value.append((v[0], base64.b64encode(v[1]).decode("utf-8")))
        rd.set_str(key, json.dumps(new_value))


