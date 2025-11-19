import { axios } from '@/utils/request'

export function getFirstCIsByCiId(ciId) {
  return axios({
    url: '/v0.1/ci_relations/' + ciId + '/first_cis',
    method: 'GET'
  })
}

export function getSecondCIsByCiId(ciId) {
  return axios({
    url: '/v0.1/ci_relations/' + ciId + '/second_cis',
    method: 'GET'
  })
}

export function searchCIRelation(params) {
  return axios({
    url: `/v0.1/ci_relations/s?${params}`,
    method: 'GET'
  })
}

export function statisticsCIRelation(params) {
  return axios({
    url: '/v0.1/ci_relations/statistics',
    method: 'GET',
    params: params
  })
}

// Batch add child nodes
export function batchUpdateCIRelationChildren(ciIds, parents, ancestor_ids = undefined) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, parents, ancestor_ids }
  })
}

// Batch add parent nodes
export function batchUpdateCIRelationParents(ciIds, children) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, children: children }
  })
}

// Batch delete
export function batchDeleteCIRelation(ciIds, parents, ancestor_ids = undefined) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'DELETE',
    data: { ci_ids: ciIds, parents, ancestor_ids }
  })
}

// Single add
export function addCIRelationView(firstCiId, secondCiId, data) {
  return axios({
    url: `/v0.1/ci_relations/${firstCiId}/${secondCiId}`,
    method: 'POST',
    data
  })
}

// Single delete
export function deleteCIRelationView(firstCiId, secondCiId, data) {
  return axios({
    url: `/v0.1/ci_relations/${firstCiId}/${secondCiId}`,
    method: 'DELETE',
    data
  })
}

export function searchCIRelationFull(params) {
  return axios({
    url: `/v0.1/ci_relations/search/full`,
    method: 'GET',
    params,
  })
}

export function searchCIRelationPath(data) {
  return axios({
    url: `/v0.1/ci_relations/path/s`,
    method: 'POST',
    data,
  })
}
