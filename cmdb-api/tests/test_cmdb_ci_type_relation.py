# -*- coding: utf-8 -*-
from api.models.cmdb import (
   CITypeRelation
)

from .sample import init_relation_type, init_ci_types, init_ci_type_relation


def test_create_ci_type_relation(session, client):
    ci_types = init_ci_types(2)
    relation_type = init_relation_type(1)[0]

    url = "/api/v0.1/ci_type_relations/{}/{}".format(*[x.id for x in ci_types])
    payload = {
        "relation_type_id": relation_type.id,
    }

    resp = client.post(url, json=payload)

    assert resp.status_code == 200
    assert resp.json["ctr_id"]

    ci_type_relations_id = resp.json["ctr_id"]
    ci_type_relation = CITypeRelation.get_by_id(ci_type_relations_id)
    assert ci_type_relation.parent_id == ci_types[0].id
    assert ci_type_relation.child_id == ci_types[1].id
    assert ci_type_relation.relation_type_id == relation_type.id


def test_delete_ci_type_relation_by_ci_type_id(session, client):
    ci_type_relation_ins = init_ci_type_relation(1)[0]
    url = "/api/v0.1/ci_type_relations/{}/{}".format(
        ci_type_relation_ins.parent_id, ci_type_relation_ins.child_id)
    resp = client.delete(url)

    assert resp.status_code == 200
    # fake deleted
    ci_type_relation_ins = CITypeRelation.query.filter_by(id=ci_type_relation_ins.id).first()
    assert ci_type_relation_ins is not None


def test_delete_ci_type_relation_by_id(session, client):
    ci_type_relation_ins = init_ci_type_relation(1)[0]
    url = "/api/v0.1/ci_type_relations/" + str(ci_type_relation_ins.id)
    resp = client.delete(url)

    assert resp.status_code == 200
    # fake deleted
    ci_type_relation_ins = CITypeRelation.query.filter_by(id=ci_type_relation_ins.id).first()
    assert ci_type_relation_ins is not None


def test_get_ci_type_relations(session, client):
    ci_type_relations = init_ci_type_relation(2)
    url = "/api/v0.1/ci_type_relations"
    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.json) == 2
    assert resp.json[0]["id"] == ci_type_relations[0].id
    assert resp.json[1]["id"] == ci_type_relations[1].id


def test_get_children(session, client):
    ci_type_relation_ins = init_ci_type_relation(1)[0]
    url = "/api/v0.1/ci_type_relations/{parent_id}/children".format(
        parent_id=ci_type_relation_ins.parent_id)
    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.json["children"]) == 1
    assert resp.json["children"][0]["id"] == ci_type_relation_ins.child_id


def test_get_parents(session, client):
    ci_type_relation_ins = init_ci_type_relation(1)[0]
    url = "/api/v0.1/ci_type_relations/{child_id}/parents".format(
        child_id=ci_type_relation_ins.child_id)
    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.json["parents"]) == 1
    assert resp.json["parents"][0]["id"] == ci_type_relation_ins.parent_id



