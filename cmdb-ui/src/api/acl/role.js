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

export function addParentRole (id, otherID) {
  return axios({
    url: urlPrefix + `/roles/${id}/parents`,
    method: 'POST',
    data: { parent_id: otherID }
  })
}

export function addChildRole (id, otherID) {
  return axios({
    url: urlPrefix + `/roles/${otherID}/parents`,
    method: 'POST',
    data: { parent_id: id }
  })
}

export function delParentRole (cid, pid) {
  return axios({
    url: urlPrefix + `/roles/${cid}/parents`,
    method: 'DELETE',
    data: { parent_id: pid }
  })
}

export function delChildRole (pid, cid) {
  return axios({
    url: urlPrefix + `/roles/${cid}/parents`,
    method: 'DELETE',
    data: { parent_id: pid }
  })
}
