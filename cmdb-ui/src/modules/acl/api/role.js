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

export function deleteRoleById(id, data) {
  return axios({
    url: urlPrefix + `/roles/${id}`,
    method: 'DELETE',
    data: data
  })
}

export function addParentRole(id, otherID, data) {
  return axios({
    url: urlPrefix + `/roles/${id}/parents`,
    method: 'POST',
    data: { ...data, parent_id: otherID }
  })
}

// export function addChildRole (id, otherID, data) {
//   return axios({
//     url: urlPrefix + `/roles/${otherID}/parents`,
//     method: 'POST',
//     data: {...data, parent_id: id }
//   })
// }

export function delParentRole(cid, pid, data) {
  return axios({
    url: urlPrefix + `/roles/${cid}/parents`,
    method: 'DELETE',
    data: { ...data, parent_id: pid }
  })
}

// export function delChildRole (pid, cid, data) {
//   return axios({
//     url: urlPrefix + `/roles/${cid}/parents`,
//     method: 'DELETE',
//     data: { data, parent_id: pid }
//   })
// }

export function getUsersUnderRole(rid, data) {
  return axios({
    url: urlPrefix + `/roles/${rid}/users`,
    method: 'GET',
    params: data
  })
}

export function addBatchParentRole(parent_id, data) {
  return axios({
    url: urlPrefix + `/roles/${parent_id}/children`,
    method: 'POST',
    data
  })
}
