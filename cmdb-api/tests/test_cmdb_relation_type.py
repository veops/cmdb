# -*- coding: utf-8 -*-
from api.models.cmdb import (
   RelationType 
)

from .sample import init_relation_type


def test_get_relation_type(session, client):
    relation_type_instances = init_relation_type(2)
    url = "/api/v0.1/relation_types"
    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.json) == 2
    assert resp.json[0]["id"] == relation_type_instances[0].id
    assert resp.json[1]["id"] == relation_type_instances[1].id


def test_create_relation_type(session, client):

    url = "/api/v0.1/relation_types"
    payload = {
        "name": "test",
    }

    resp = client.post(url, json=payload)

    assert resp.status_code == 200
    assert resp.json["id"]

    relation_types_id = resp.json["id"]
    relation_type = RelationType.get_by_id(relation_types_id)
    assert relation_type.id == relation_types_id
    assert relation_type.name == "test"


def test_create_relation_type_name_strip(session, client):
    url = "/api/v0.1/relation_types"
    payload = {
        "name": "test\t   ",
    }

    resp = client.post(url, json=payload)

    assert resp.status_code == 200
    assert resp.json["id"]

    relation_types_id = resp.json["id"]
    relation_type = RelationType.get_by_id(relation_types_id)
    assert relation_type.name == "test"


def test_update_relation_type(session, client):
    relation_type_ins = init_relation_type(1)[0]

    url = "/api/v0.1/relation_types/" + str(relation_type_ins.id)
    payload = {
        "name": "update",
    }

    resp = client.put(url, json=payload)

    assert resp.status_code == 200
    assert resp.json["id"] == relation_type_ins.id

    relation_type_ins = RelationType.get_by_id(relation_type_ins.id)
    assert relation_type_ins.name == "update"


def test_delete_relation_type(session, client):
    relation_type_ins = init_relation_type(1)[0]
    url = "/api/v0.1/relation_types/" + str(relation_type_ins.id)
    resp = client.delete(url)

    assert resp.status_code == 200
    relation_type_ins = RelationType.query.filter_by(id=relation_type_ins.id).first()
    assert relation_type_ins.deleted is True
    assert relation_type_ins.deleted_at

