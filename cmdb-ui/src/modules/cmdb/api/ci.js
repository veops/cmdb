import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function searchCI(params, isShowMessage = true) {
  return axios({
    url: urlPrefix + `/ci/s`,
    method: 'GET',
    params: params,
    isShowMessage
  })
}

export function searchCI2(params) {
  return axios({
    url: urlPrefix + `/ci/s?${params}`,
    method: 'GET'
  })
}

export function addCI(params) {
  return axios({
    url: urlPrefix + '/ci',
    method: 'POST',
    data: params
  })
}

export function updateCI(id, params, isShowMessage = true) {
  return axios({
    url: urlPrefix + `/ci/${id}`,
    method: 'PUT',
    data: params,
    isShowMessage
  })
}

export function deleteCI(ciId, isShowMessage = true) {
  return axios({
    url: urlPrefix + `/ci/${ciId}`,
    method: 'DELETE',
    isShowMessage
  })
}

// Get single CI instance
export function getCIById(ciId) {
  return axios({
    // url: urlPrefix + `/ci/${ciId}`,
    url: urlPrefix + `/ci/s?q=_id:${ciId}`,
    method: 'GET'
  })
}

// Get auto-discovery statistics
export function getCIAdcStatistics() {
  return axios({
    url: urlPrefix + `/ci/adc/statistics`,
    method: 'GET'
  })
}
