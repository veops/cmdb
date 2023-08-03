import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function searchCI(params) {
  return axios({
    url: urlPrefix + `/ci/s`,
    method: 'GET',
    params: params
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

//  获取单个ci实例
export function getCIById(ciId) {
  return axios({
    // url: urlPrefix + `/ci/${ciId}`,
    url: urlPrefix + `/ci/s?q=_id:${ciId}`,
    method: 'GET'
  })
}

//  获取自动发现占比
export function getCIAdcStatistics() {
  return axios({
    url: urlPrefix + `/ci/adc/statistics`,
    method: 'GET'
  })
}
