# -*- coding: utf-8 -*-
from .sample import init_ci_with_type, init_ci_type_relation, init_ci_relation
from api.lib.cmdb.ci import CIRelationManager
from api.models.cmdb import CIRelation, CIType, CI


def test_create_ci_relation(session, client):
    init_ci_type_relation(1)
    ci_types = CIType.query.all()
    cis = init_ci_with_type(ci_types)

    url = "/api/v0.1/ci_relations/{}/{}".format(cis[0]['ci_id'], cis[1]['ci_id'])

    resp = client.post(url)
    assert resp.status_code == 200
    cr_id = resp.json['cr_id']
    cr = CIRelation.get_by_id(cr_id)
    assert cr is not None


def test_delte_ci_relation_by_ci_id(session, client):
    cr_id = init_ci_relation()
    cis = CI.query.all()

    url = "/api/v0.1/ci_relations/{}/{}".format(cis[0].id, cis[1].id)
    resp = client.delete(url)
    assert resp.status_code == 200
    cr = CIRelation.get_by_id(cr_id)
    assert cr is None


def test_delete_ci_relation_by_id(session, client):
    cr_id = init_ci_relation()
    url = "/api/v0.1/ci_relations/{cr_id}".format(cr_id=cr_id)
    resp = client.delete(url)
    assert resp.status_code == 200
    cr = CIRelation.get_by_id(cr_id)
    assert cr is None

