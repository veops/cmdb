import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function getResourcePerms(resourceID, params) {
  return axios({
    url: urlPrefix + `/resources/${resourceID}/permissions`,
    method: 'GET',
    params
  })
}

export function getResourceTypePerms(typeID) {
  return axios({
    url: urlPrefix + `/resource_types/${typeID}/perms`,
    method: 'GET'
  })
}

export function getResourceGroupPerms(resourceGroupID) {
  return axios({
    url: urlPrefix + `/resource_groups/${resourceGroupID}/permissions`,
    method: 'GET'
  })
}

export function setRoleResourcePerm(rid, resourceID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/${resourceID}/grant2`,
    method: 'POST',
    data: params
  })
}

export function setRoleResourceGroupPerm(rid, resourceGroupID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/${resourceGroupID}/grant`,
    method: 'POST',
    data: params
  })
}

export function deleteRoleResourcePerm(rid, resourceID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/${resourceID}/revoke2`,
    method: 'POST',
    data: params
  })
}

export function deleteRoleResourceGroupPerm(rid, resourceGroupID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/${resourceGroupID}/revoke`,
    method: 'POST',
    data: params
  })
}

// 资源组  清空按钮使用
export function deleteRoleResourceGroupPerm2(rid, resourceGroupID, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/${resourceGroupID}/revoke2`,
    method: 'POST',
    data: params
  })
}

export function searchPermResourceByRoleId(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources`,
    method: 'GET',
    params: params
  })
}

export function roleHasPermissionToGrant(params) {
  return axios({
    url: urlPrefix + '/roles/has_perm',
    method: 'GET',
    params: params
  })
}

// 资源批量授权
export function setBatchRoleResourcePerm(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/batch/grant`,
    method: 'POST',
    data: params
  })
}

// 资源组批量授权
export function setBatchRoleResourceGroupPerm(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/batch/grant`,
    method: 'POST',
    data: params
  })
}

// 资源批量权限回收
export function setBatchRoleResourceRevoke(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/batch/revoke`,
    method: 'POST',
    data: params
  })
}

// 资源组批量授权
export function setBatchRoleResourceGroupRevoke(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resource_groups/batch/revoke`,
    method: 'POST',
    data: params
  })
}

// 按资源名批量授权
export function setBatchRoleResourceByResourceName(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/batch/grant2`,
    method: 'POST',
    data: params
  })
}

// 资源名批量回收
export function setBatchRoleResourceRevokeByResourceName(rid, params) {
  return axios({
    url: urlPrefix + `/roles/${rid}/resources/batch/revoke2`,
    method: 'POST',
    data: params
  })
}
