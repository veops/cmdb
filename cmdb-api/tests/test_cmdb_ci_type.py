# -*- coding: utf-8 -*-
from api.models.cmdb import (
    CIType, CITypeAttribute,
    Attribute, CITypeAttributeGroup,
    CITypeAttributeGroupItem)

from tests.sample import (
    init_attributes, init_ci_types,
    init_attribute_groups)


def test_create_ci_type(session, client):
    attr = init_attributes(1)[0]

    url = "/api/v0.1/ci_types"
    payload = {
        "name": "test",
        "alias": "测试",
        "unique_key": attr.id
    }

    resp = client.post(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert resp.json["type_id"]

    # check there is a attribute in database
    type_id = resp.json["type_id"]
    ci_type_ins = CIType.get_by_id(type_id)
    assert ci_type_ins.id == type_id
    assert ci_type_ins.name == "test"
    assert ci_type_ins.alias == "测试"
    assert ci_type_ins.unique_id == attr.id


def test_update_ci_type(session, client):
    ci_type_ins = init_ci_types(1)[0]

    url = "/api/v0.1/ci_types/" + str(ci_type_ins.id)
    payload = {
        "name": "update",
    }

    resp = client.put(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert resp.json["type_id"] == ci_type_ins.id

    # check ci_type updated in database
    ci_type_ins = CIType.get_by_id(ci_type_ins.id)
    assert ci_type_ins.name == "update"


def test_delete_ci_type(session, client):
    ci_type_ins = init_ci_types(1)[0]
    url = "/api/v0.1/ci_types/" + str(ci_type_ins.id)

    resp = client.delete(url)

    assert resp.status_code == 200
    # attr should be soft delete
    ci_type_ins = CIType.get_by_id(ci_type_ins.id)
    assert ci_type_ins.deleted is True
    assert ci_type_ins.deleted_at


def test_bind_attributes_ci_type(session, client):
    attrs = init_attributes(3)
    ci_type = init_ci_types(1)[0]

    url = "/api/v0.1/ci_types/{}/attributes".format(ci_type.id)
    payload = {
        "attr_id": [str(x.id) for x in attrs]
    }

    resp = client.post(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert len(resp.json["attributes"]) == len(attrs)

    # check ci_type has 4 attributes
    ci_type_attribute_ids = [x.attr_id for x in CITypeAttribute.query.filter_by(type_id=ci_type.id).all()]
    for attr in attrs:
        assert attr.id in ci_type_attribute_ids


def test_get_attributes_ci_type(session, client):
    ci_type = init_ci_types(1)[0]
    url = "/api/v0.1/ci_types/{}/attributes".format(ci_type.name)

    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.json["attributes"]) == 1


def test_update_attributes_ci_type(session, client):
    ci_type = init_ci_types(1)[0]
    attr = Attribute.query.first()
    url = "/api/v0.1/ci_types/{}/attributes".format(ci_type.id)

    payload = {
        "attributes": [
            {"attr_id": attr.id, "default_show": False, "is_required": True}
        ]
    }
    resp = client.put(url, json=payload)
    assert resp.status_code == 200

    ci_type_attr_ins = CITypeAttribute.query.filter_by(type_id=ci_type.id).first()
    assert ci_type_attr_ins
    assert ci_type_attr_ins.is_required is True
    assert ci_type_attr_ins.default_show is False


def test_create_attribute_group_ci_type(session, client):
    ci_type = init_ci_types(1)[0]

    url = "/api/v0.1/ci_types/{}/attribute_groups".format(ci_type.id)
    payload = {
        "name": "A",
        "order": 100,
    }

    resp = client.post(url, json=payload)

    # check resp status code and content
    assert resp.status_code == 200
    assert resp.json["group_id"]

    ins = CITypeAttributeGroup.query.filter_by(type_id=ci_type.id).first()
    assert ins
    assert ins.id == resp.json["group_id"]
    assert ins.name == "A"
    assert ins.order == 100


def test_update_attribute_group_ci_type(session, client):
    attribute_groups = init_attribute_groups(1)[0]

    url = "/api/v0.1/ci_types/attribute_groups/{}".format(attribute_groups.id)
    payload = {
        "attributes": [x.id for x in Attribute.query.all()]
    }

    resp = client.put(url, json=payload)
    assert resp.status_code == 200
    assert resp.json["group_id"]

    ag_items = CITypeAttributeGroupItem.query.filter_by(group_id=attribute_groups.id).all()
    for a in Attribute.query.all():
        assert a.id in [x.attr_id for x in ag_items]


def test_delete_attribute_group_ci_type(session, client):
    attribute_groups = init_attribute_groups(1)[0]

    url = "/api/v0.1/ci_types/attribute_groups/{}".format(attribute_groups.id)
    resp = client.delete(url)

    assert resp.status_code == 200
    attribute_group_ins = CITypeAttributeGroup.query.filter_by(id=attribute_groups.id).first()
    assert attribute_group_ins.deleted is True
    assert attribute_group_ins.deleted_at
