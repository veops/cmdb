# -*- coding: utf-8 -*-
from .sample import init_ci_types, fake_attr_value
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci import CIManager


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


