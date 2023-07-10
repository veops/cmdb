import { axios } from '@/utils/request'

export function getCIHistory (ciId) {
  return axios({
    url: `/v0.1/history/ci/${ciId}`,
    method: 'GET'
  })
}

export function getCIHistoryTable (params) {
  return axios({
    url: `/v0.1/history/records/attribute`,
    method: 'GET',
    params: params
  })
}

export function getRelationTable (params) {
  return axios({
    url: `/v0.1/history/records/relation`,
    method: 'GET',
    params: params
  })
}

export function getCITypesTable (params) {
  return axios({
    url: `/v0.1/history/ci_types`,
    method: 'GET',
    params: params
  })
}

export function getUsers (params) {
  return axios({
    url: `/v1/acl/users/employee`,
    method: 'GET',
    params: params
  })
}
