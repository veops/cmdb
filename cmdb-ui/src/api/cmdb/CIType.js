import { axios } from '@/utils/request'

/**
 * get all CI Type
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCITypes (parameter) {
  return axios({
    url: '/v0.1/ci_types',
    method: 'GET',
    params: parameter
  })
}

/**
 * get a CI Type
 * @param CITypeName
 * @param parameter
 * @returns {AxiosPromise}
 */
export function getCIType (CITypeName, parameter) {
  return axios({
    url: `/v0.1/ci_types/${CITypeName}`,
    method: 'GET',
    params: parameter
  })
}

/**
 * Create CI Type
 * @param data
 * @returns {AxiosPromise}
 */
export function createCIType (data) {
  return axios({
    url: '/v0.1/ci_types',
    method: 'POST',
    data: data
  })
}

/**
 * Update CI Type
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCIType (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}`,
    method: 'PUT',
    data: data
  })
}

/**
 * Delete CI Type
 * @param CITypeId
 * @returns {AxiosPromise}
 */
export function deleteCIType (CITypeId) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}`,
    method: 'DELETE'
  })
}

/**
 * Gets a grouping of a CI Type
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function getCITypeGroupById (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups`,
    method: 'GET',
    params: data
  })
}

/**
 * Save a group of CI Type
 * @param CITypeId
 * @param data
 * @returns {AxiosPromise}
 */
export function createCITypeGroupById (CITypeId, data) {
  return axios({
    url: `/v0.1/ci_types/${CITypeId}/attribute_groups`,
    method: 'POST',
    data: data
  })
}

/**
 * Changes the grouping of a CI Type
 * @param groupId
 * @param data
 * @returns {AxiosPromise}
 */
export function updateCITypeGroupById (groupId, data) {
  return axios({
    url: `/v0.1/ci_types/attribute_groups/${groupId}`,
    method: 'PUT',
    data: data
  })
}

/**
 * Removes a group for a CI Type
 * @param groupId
 * @param data
 * @returns {AxiosPromise}
 */
export function deleteCITypeGroupById (groupId, data) {
  return axios({
    url: `/v0.1/ci_types/attribute_groups/${groupId}`,
    method: 'delete',
    data: data
  })
}
