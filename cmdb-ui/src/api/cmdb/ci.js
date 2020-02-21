import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function searchCI (params) {
  return axios({
    url: urlPrefix + `/ci/s?${params}`,
    method: 'GET'
  })
}

export function addCI (params) {
  return axios({
    url: urlPrefix + '/ci',
    method: 'POST',
    data: params
  })
}

export function updateCI (id, params) {
  return axios({
    url: urlPrefix + `/ci/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteCI (ciId) {
  return axios({
    url: urlPrefix + `/ci/${ciId}`,
    method: 'DELETE'
  })
}

//  Get a single CI instance
export function getCIById (ciId) {
  return axios({
    url: urlPrefix + `/ci/${ciId}`,
    method: 'GET'
  })
}
