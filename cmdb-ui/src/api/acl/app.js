import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function searchRole (params) {
  return axios({
    url: urlPrefix + `/roles`,
    method: 'GET',
    params: params
  })
}

export function addRole (params) {
  return axios({
    url: urlPrefix + '/roles',
    method: 'POST',
    data: params
  })
}

export function updateRoleById (id, params) {
  return axios({
    url: urlPrefix + `/roles/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteRoleById (id) {
  return axios({
    url: urlPrefix + `/roles/${id}`,
    method: 'DELETE'
  })
}
