import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function searchResource (params) {
  return axios({
    url: urlPrefix + `/resources`,
    method: 'GET',
    params: params
  })
}

export function addResource (params) {
  return axios({
    url: urlPrefix + '/resources',
    method: 'POST',
    data: params
  })
}

export function updateResourceById (id, params) {
  return axios({
    url: urlPrefix + `/resources/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteResourceById (id) {
  return axios({
    url: urlPrefix + `/resources/${id}`,
    method: 'DELETE'
  })
}
