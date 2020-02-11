# -*- coding: utf-8 -*-
from api.models.cmdb import Attribute

from tests.sample import init_attributes


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

    # check there is a attribute in database
    attr_id = resp.json["attr_id"]
    attr_ins = Attribute.get_by_id(attr_id)
    assert attr_ins.id == attr_id
    assert attr_ins.name == "region"
    assert attr_ins.alias == "区域"


def test_update_attribute(session, client):
    attr_ins = init_attributes(1)[0]

    url = "/api/v0.1/attributes/" + str(attr_ins.id)
    payload = {
        "name": "update",
    }

    resp = client.put(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert resp.json["attr_id"] == attr_ins.id

    # check attribute updated in database
    attr_ins = Attribute.get_by_id(attr_ins.id)
    assert attr_ins.name == "update"


def test_delete_attribute(session, client):
    attr_ins = init_attributes(1)[0]
    url = "/api/v0.1/attributes/" + str(attr_ins.id)

    resp = client.delete(url)

    assert resp.status_code == 200
    # attr should be soft delete
    attr_ins = Attribute.get_by_id(attr_ins.id)
    assert attr_ins.deleted is True
    assert attr_ins.deleted_at

