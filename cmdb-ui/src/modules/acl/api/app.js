import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function searchRole(params) {
  return axios({
    url: urlPrefix + `/roles`,
    method: 'GET',
    params: params
  })
}

export function addRole(params) {
  return axios({
    url: urlPrefix + '/roles',
    method: 'POST',
    data: params
  })
}

export function updateRoleById(id, params) {
  return axios({
    url: urlPrefix + `/roles/${id}`,
    method: 'PUT',
    data: params
  })
}

export function deleteRoleById(id) {
  return axios({
    url: urlPrefix + `/roles/${id}`,
    method: 'DELETE'
  })
}

export function searchApp(params = {}) {
  return axios({
    url: urlPrefix + '/apps',
    method: 'GET',
    params: { ...params, page_size: 9999 }
  })
}

export function addApp(data) {
  return axios({
    url: urlPrefix + '/apps',
    method: 'POST',
    data: data
  })
}

export function updateApp(aid, data) {
  return axios({
    url: urlPrefix + `/apps/${aid}`,
    method: 'PUT',
    data: data
  })
}

export function getApp(aid) {
  return axios({
    url: urlPrefix + `/apps/${aid}`,
    method: 'GET',
  })
}

export function deleteApp(aid) {
  return axios({
    url: urlPrefix + `/apps/${aid}`,
    method: 'DELETE'
  })
}
