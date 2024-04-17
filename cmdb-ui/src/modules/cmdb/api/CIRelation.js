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

// 批量添加子节点
export function batchUpdateCIRelationChildren(ciIds, parents, ancestor_ids = undefined) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, parents, ancestor_ids }
  })
}

// 批量添加父节点
export function batchUpdateCIRelationParents(ciIds, children) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, children: children }
  })
}

// 批量删除
export function batchDeleteCIRelation(ciIds, parents, ancestor_ids = undefined) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'DELETE',
    data: { ci_ids: ciIds, parents, ancestor_ids }
  })
}

// 单个添加
export function addCIRelationView(firstCiId, secondCiId, data) {
  return axios({
    url: `/v0.1/ci_relations/${firstCiId}/${secondCiId}`,
    method: 'POST',
    data
  })
}

// 单个删除
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
