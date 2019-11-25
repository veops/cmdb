import { axios } from '@/utils/request'

export function getCITypeChildren (CITypeID, parameter) {
  return axios({
    url: '/v0.1/ci_type_relations/' + CITypeID + '/children',
    method: 'get',
    params: parameter
  })
}

export function getCITypeParent (CITypeID) {
  return axios({
    url: '/v0.1/ci_type_relations/' + CITypeID + '/parents',
    method: 'get'
  })
}

export function createRelation (parentId, childrenId, relationTypeId) {
  return axios({
    url: `/v0.1/ci_type_relations/${parentId}/${childrenId}`,
    method: 'post',
    data: { relation_type_id: relationTypeId }
  })
}

export function deleteRelation (parentId, childrenId) {
  return axios({
    url: `/v0.1/ci_type_relations/${parentId}/${childrenId}`,
    method: 'delete'

  })
}
