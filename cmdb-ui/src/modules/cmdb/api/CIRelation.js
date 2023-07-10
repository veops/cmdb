import { axios } from '@/utils/request'

export function getFirstCIs(ciId) {
  return axios({
    url: '/v0.1/ci_relations/' + ciId + '/first_cis',
    method: 'GET'
  })
}

export function getSecondCIs(ciId) {
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
export function batchUpdateCIRelationChildren(ciIds, parents) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, parents: parents }
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
export function batchDeleteCIRelation(ciIds, parents) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'DELETE',
    data: { ci_ids: ciIds, parents: parents }
  })
}

// 单个添加
export function addCIRelationView(firstCiId, secondCiId) {
  return axios({
    url: `/v0.1/ci_relations/${firstCiId}/${secondCiId}`,
    method: 'POST',
  })
}

// 单个删除
export function deleteCIRelationView(firstCiId, secondCiId) {
  return axios({
    url: `/v0.1/ci_relations/${firstCiId}/${secondCiId}`,
    method: 'DELETE',
  })
}
