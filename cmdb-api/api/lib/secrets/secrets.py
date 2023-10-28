from api.models.cmdb import InnerKV


class InnerKVManger(object):
    def __init__(self):
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
        res = InnerKV.get_by(first=True, to_dict=False, **{"key": key})
        if not res:
            return None

        return res.value
