import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function getResourcePerms (resourceID) {
  return axios({
    url: urlPrefix + `/resources/${resourceID}/permissions`,
    method: 'GET'
  })
}

export function getResourceTypePerms (typeID) {
  return axios({
    url: urlPrefix + `/resource_types/${typeID}/perms`,
    method: 'GET'
  })
}

export function getResourceGroupPerms (resourceGroupID) {
  return axios({
    url: urlPrefix + `/resource_groups/${resourceGroupID}/permissions`,
    method: 'GET'
  })
}

export function setRoleResourcePerm (rid, resourceID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/${resourceID}/grant`,
    method: 'POST',
    data: params
  })
}

export function setRoleResourceGroupPerm (rid, resourceGroupID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/${resourceGroupID}/grant`,
    method: 'POST',
    data: params
  })
}

export function deleteRoleResourcePerm (rid, resourceID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/${resourceID}/revoke`,
    method: 'POST',
    data: params
  })
}

export function deleteRoleResourceGroupPerm (rid, resourceGroupID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/${resourceGroupID}/revoke`,
    method: 'POST',
    data: params
  })
}
