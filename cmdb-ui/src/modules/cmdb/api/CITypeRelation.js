import { axios } from '@/utils/request'

export function getCITypeChildren(CITypeID, parameter) {
  return axios({
    url: '/v0.1/ci_type_relations/' + CITypeID + '/children',
    method: 'get',
    params: parameter
  })
}

export function getCITypeParent(CITypeID) {
  return axios({
    url: '/v0.1/ci_type_relations/' + CITypeID + '/parents',
    method: 'get'
  })
}

export function getCITypeRelations() {
  return axios({
    url: '/v0.1/ci_type_relations',
    method: 'GET'
  })
}

export function getRelationTypes(CITypeID, parameter) {
  return axios({
    url: '/v0.1/relation_types',
    method: 'get',
    params: parameter
  })
}

export function createRelation(parentId, childrenId, data) {
  return axios({
    url: `/v0.1/ci_type_relations/${parentId}/${childrenId}`,
    method: 'post',
    data
  })
}

export function deleteRelation(parentId, childrenId) {
  return axios({
    url: `/v0.1/ci_type_relations/${parentId}/${childrenId}`,
    method: 'delete'
  })
}

export function grantTypeRelation(first_type_id, second_type_id, rid, data) {
  return axios({
    url: `/v0.1/ci_type_relations/${first_type_id}/${second_type_id}/roles/${rid}/grant`,
    method: 'post',
    data
  })
}

export function revokeTypeRelation(first_type_id, second_type_id, rid, data) {
  return axios({
    url: `/v0.1/ci_type_relations/${first_type_id}/${second_type_id}/roles/${rid}/revoke`,
    method: 'post',
    data
  })
}

export function getRecursive_level2children(type_id) {
  return axios({
    url: `/v0.1/ci_type_relations/${type_id}/recursive_level2children`,
    method: 'GET'
  })
}

export function getCanEditByParentIdChildId(parent_id, child_id) {
  return axios({
    url: `/v0.1/ci_type_relations/${parent_id}/${child_id}/can_edit`,
    method: 'GET'
  })
}
