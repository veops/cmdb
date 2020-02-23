# -*- coding: utf-8 -*-
from .sample import init_ci_types, fake_attr_value, init_ci
from api.lib.cmdb.ci_type import CITypeAttributeManager, CITypeManager
from api.lib.cmdb.ci import CIManager
from api.models.cmdb import CI


def test_create_ci(session, client):
    ci_type = init_ci_types(1)[0]
    attrs = CITypeAttributeManager.get_attributes_by_type_id(ci_type.id)
    url = "/api/v0.1/ci"

    fake_value = fake_attr_value(attrs[0])

    payload = {
        "ci_type": ci_type.id,
        **fake_value
    }

    resp = client.post(url, json=payload)
    assert resp.status_code == 200
    assert resp.json["ci_id"]

    ci_id = resp.json["ci_id"]
    ci = CIManager().get_ci_by_id_from_db(ci_id)
    assert ci[attrs[0]["name"]] == fake_value[attrs[0]['name']]


def test_update_ci(session, client):
    ci = init_ci(1)[0]
    ci_id = ci.get("ci_id")
    ci_type = CITypeManager.get_ci_types(ci.get("ci_type"))[0]
    attrs = CITypeAttributeManager.get_attributes_by_type_id(ci_type["id"])
    url = "/api/v0.1/ci/{}".format(ci_id)

    fake_value = fake_attr_value(attrs[0])

    payload = {**fake_value}

    resp = client.put(url, json=payload)

    assert resp.status_code == 200
    assert resp.json["ci_id"] == ci_id
    ci = CIManager().get_ci_by_id_from_db(ci_id)
    assert ci[attrs[0]['name']] == fake_value[attrs[0]['name']]


def test_delete_ci(session, client):
    ci = init_ci(1)[0]
    ci_id = ci.get("ci_id")
    url = "/api/v0.1/ci/{}".format(ci_id)

    resp = client.delete(url)

    assert resp.status_code == 200

    ci_from_db = CI.query.filter_by(id=ci_id).first()
    assert ci_from_db is None


def test_get_ci_by_types(session, client):
    ci = init_ci(1)[0]
    ci_type = CITypeManager.get_ci_types(ci.get("ci_type"))[0]
    url = "/api/v0.1/ci/type/{}".format(ci_type["id"])

    resp = client.get(url)
    assert resp.status_code == 200

    assert resp.json['cis'][0]['ci_id'] == ci['ci_id']


def test_get_ci_by_id(session, client):
    ci = init_ci(1)[0]
    url = "/api/v0.1/ci/{}".format(ci["ci_id"])

    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json['ci_id'] == ci['ci_id']


def test_get_ci_detail_by_id(session, client):
    ci = init_ci(1)[0]
    url = "/api/v0.1/ci/{}/detail".format(ci["ci_id"])

    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json['id'] == ci['ci_id']


