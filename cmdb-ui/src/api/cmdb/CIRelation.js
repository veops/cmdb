import { axios } from '@/utils/request'

export function getFirstCIs (ciId) {
  return axios({
    url: '/v0.1/ci_relations/' + ciId + '/first_cis',
    method: 'GET'
  })
}

export function getSecondCIs (ciId) {
  return axios({
    url: '/v0.1/ci_relations/' + ciId + '/second_cis',
    method: 'GET'
  })
}

export function searchCIRelation (params) {
  return axios({
    url: `/v0.1/ci_relations/s?${params}`,
    method: 'GET'
  })
}

export function statisticsCIRelation (params) {
  return axios({
    url: '/v0.1/ci_relations/statistics',
    method: 'GET',
    params: params
  })
}

export function batchUpdateCIRelation (ciIds, parents) {
  return axios({
    url: '/v0.1/ci_relations/batch',
    method: 'POST',
    data: { ci_ids: ciIds, parents: parents }
  })
}
