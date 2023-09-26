import { axios } from '@/utils/request'

/**
 * 获取 所有的 ci_types
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypes(parameter) {
  return axios({
    url: '/v0.1/ci_types',
    method: 'GET',
    params: parameter
  })
}

/**
 * 获取 某个 ci_types
 * @param CITypeName
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCIType(CITypeName, parameter) {
  return axios({
    url: `/v0.1/ci_types/${CITypeName}`,
    method: 'GET',
    params: parameter
  })
}

/**
 * 创建 ci_type
 * @param data
 * @returns {AxiosPromise}
 */
export function createCIType(data) {
  return axios({
    url: '/v0.1/ci_types',
    method: 'POST',
    data: data
  })
}

/**
 * 更新 ci_type
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCIType(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}`,
    method: 'PUT',
    data: data
  })
}

/**
 * 删除 ci_type
 * @param CITypeId
 * @returns {AxiosPromise}
 */
export function deleteCIType(CITypeId) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}`,
    method: 'DELETE'
  })
}

/**
 * 获取 某个 ci_type 的分组
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function getCITypeGroupById(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups`,
    method: 'GET',
    params: data
  })
}

/**
 * 保存 某个 ci_type 的分组
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function createCITypeGroupById(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups`,
    method: 'POST',
    data: data
  })
}

/**
 * 修改 某个 ci_type 的分组
 * @param groupId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCITypeGroupById(groupId, data) {
  return axios({
    url: `/v0.1/ci_types/attribute_groups/${groupId}`,
    method: 'PUT',
    data: data
  })
}

/**
 * 删除 某个 ci_type 的分组
 * @param groupId
 * @param data
 * @returns {AxiosPromise}
 */
export function deleteCITypeGroupById(groupId, data) {
  return axios({
    url: `/v0.1/ci_types/attribute_groups/${groupId}`,
    method: 'delete',
    data: data
  })
}

export function getUniqueConstraintList(type_id) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/unique_constraint`,
    method: 'get',
  })
}

export function addUniqueConstraint(type_id, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/unique_constraint`,
    method: 'post',
    data: data
  })
}

export function updateUniqueConstraint(type_id, id, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/unique_constraint/${id}`,
    method: 'put',
    data: data
  })
}

export function deleteUniqueConstraint(type_id, id) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/unique_constraint/${id}`,
    method: 'delete',
  })
}

export function getTriggerList(type_id) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/triggers`,
    method: 'get',
  })
}

export function addTrigger(type_id, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/triggers`,
    method: 'post',
    data: data
  })
}

export function updateTrigger(type_id, id, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/triggers/${id}`,
    method: 'put',
    data: data
  })
}

export function deleteTrigger(type_id, id) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/triggers/${id}`,
    method: 'delete',
  })
}

// CMDB的模型和实例的授权接口
export function grantCiType(type_id, rid, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/roles/${rid}/grant`,
    method: 'post',
    data
  })
}
// CMDB的模型和实例的删除授权接口
export function revokeCiType(type_id, rid, data) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/roles/${rid}/revoke`,
    method: 'post',
    data
  })
}
// CMDB的模型和实例的过滤的权限
export function ciTypeFilterPermissions(type_id) {
  return axios({
    url: `/v0.1/ci_types/${type_id}/filters/permissions`,
    method: 'get',
  })
}

export function getAllDagsName(params) {
  return axios({
      url: '/v1/dag/all_names',
      method: 'GET',
      params: params
  })
}
