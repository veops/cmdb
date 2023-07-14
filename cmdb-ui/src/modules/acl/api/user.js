/* eslint-disable */
import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function currentUser() {
  return axios({
    url: urlPrefix + `/users/info`,
    method: 'GET'
  })
}

export function getOnDutyUser() {
  return axios({
    url: urlPrefix + '/users/employee',
    method: 'GET',
    // data: { 'originUrl': 'http://hr.dfc.sh/api/all_users?work_status=在职' }
  })
}

export function searchUser(params) {
  return axios({
    url: urlPrefix + `/users`,
    method: 'GET',
    params: params
  })
}

export function addUser(params) {
  return axios({
    url: urlPrefix + '/users',
    method: 'POST',
    data: params
  })
}

export function updateUserById(id, params) {
  return axios({
    url: urlPrefix + `/users/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteUserById(id) {
  return axios({
    url: urlPrefix + `/users/${id}`,
    method: 'DELETE'
  })
}
