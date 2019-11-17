import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function currentUser () {
  return axios({
    url: urlPrefix + `/users/info`,
    method: 'GET'
  })
}

export function searchUser (params) {
  return axios({
    url: urlPrefix + `/users?${params}`,
    method: 'GET'
  })
}

export function addUser (params) {
  return axios({
    url: urlPrefix + '/users',
    method: 'POST',
    data: params
  })
}

export function updateUserById (id, params) {
  return axios({
    url: urlPrefix + `/users/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteUserById (id) {
  return axios({
    url: urlPrefix + `/users/${id}`,
    method: 'DELETE'
  })
}

