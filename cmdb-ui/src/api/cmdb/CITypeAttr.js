import { axios } from '@/utils/request'

/**
 * Get CI Type attributes
 * @param CITypeName
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypeAttributesByName (CITypeName, parameter) {
  return axios({

    url: `/v0.1/ci_types/${CITypeName}/attributes`,
    method: 'get',
    params: parameter
  })
}

/**
 * Get CI Type attributes
 * @param CITypeId
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypeAttributesById (CITypeId, parameter) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'get',
    params: parameter
  })
}

/**
 * Update attribute
 * @param attrId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateAttributeById (attrId, data) {
  return axios({
    url: `/v0.1/attributes/${attrId}`,
    method: 'put',
    data: data
  })
}

/**
 * Add attribute
 * @param data
 * @returns {AxiosPromise}
 */
export function createAttribute (data) {
  return axios({
    url: `/v0.1/attributes`,
    method: 'post',
    data: data
  })
}

/**
 * Search attributes or get all attributes
 * @param data
 * @returns {AxiosPromise}
 */
export function searchAttributes (params) {
  return axios({
    url: `/v0.1/attributes/s`,
    method: 'get',
    params: params
  })
}

/**
 * Delete attribute
 * @param attrId
 * @returns {AxiosPromise}
 */
export function deleteAttributesById (attrId) {
  return axios({
    url: `/v0.1/attributes/${attrId}`,
    method: 'delete'
  })
}

/**
 * Bind attribute
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function createCITypeAttributes (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'post',
    data: data
  })
}

/**
 * Update CI Type attribute
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCITypeAttributesById (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'put',
    data: data
  })
}

/**
 * Delete CI Type attribute
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function deleteCITypeAttributesById (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes`,
    method: 'delete',
    data: data
  })
}

export function transferCITypeAttrIndex (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attributes/transfer`,
    method: 'POST',
    data: data
  })
}

export function transferCITypeGroupIndex (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups/transfer`,
    method: 'POST',
    data: data
  })
}
