import { axios } from '@/utils/request'

/**
 * 获取 ci_type 的属性
 * @param CITypeName
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypeAttributesByName(CITypeName, parameter) {
  return axios({

    url: `/v0.1/ci_types/${CITypeName}/attributes`,
    method: 'get',
    params: parameter
  })
}

/**
 * 获取 ci_type 的属性
 * @param CITypeId
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypeAttributesById(CITypeId, parameter) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'get',
    params: parameter
  })
}

/**
 * 更新属性
 * @param attrId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateAttributeById(attrId, data) {
  return axios({
    url: `/v0.1/attributes/${attrId}`,
    method: 'put',
    data: data
  })
}

/**
 * 添加属性
 * @param data
 * @returns {AxiosPromise}
 */
export function createAttribute(data) {
  return axios({
    url: `/v0.1/attributes`,
    method: 'post',
    data: data
  })
}

/**
 * 搜索属性/ 获取所有的属性
 * @param data
 * @returns {AxiosPromise}
 */
export function searchAttributes(params) {
  return axios({
    url: `/v0.1/attributes/s`,
    method: 'get',
    params: params
  })
}

export function getCITypeAttributesByTypeIds(params) {
  return axios({
    url: `/v0.1/ci_types/attributes`,
    method: 'get',
    params: params
  })
}

/**
 * 删除属性
 * @param attrId
 * @returns {AxiosPromise}
 */
export function deleteAttributesById(attrId) {
  return axios({
    url: `/v0.1/attributes/${attrId}`,
    method: 'delete'
  })
}

/**
 * 绑定ci_type 属性
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function createCITypeAttributes(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'post',
    data: data
  })
}

/**
 * 更新ci_type 属性
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCITypeAttributesById(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'put',
    data: data
  })
}

/**
 * 删除ci_type 属性
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function deleteCITypeAttributesById(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'delete',
    data: data
  })
}

export function transferCITypeAttrIndex(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes/transfer`,
    method: 'POST',
    data: data
  })
}

export function transferCITypeGroupIndex(CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups/transfer`,
    method: 'POST',
    data: data
  })
}

export function canDefineComputed() {
  return axios({
    url: `/v0.1/ci_types/can_define_computed`,
    method: 'HEAD',
  })
}
