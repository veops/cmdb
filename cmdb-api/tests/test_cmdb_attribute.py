# -*- coding: utf-8 -*-
from api.models.cmdb import Attribute


def test_create_attribute(session, client):
    url = "/api/v0.1/attributes"
    payload = {
        "name": "region",
        "alias": "区域",
        "value_type": "2"
    }

    resp = client.post(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert resp.json["attr_id"]

    # check there is a ci_types in database
    attr_id = resp.json["attr_id"]
    attr_ins = Attribute.get_by_id(attr_id)
    assert attr_ins.id == attr_id
    assert attr_ins.name == "region"
    assert attr_ins.alias == "区域"


