import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function getTriggers(params) {
  return axios({
    url: urlPrefix + '/triggers',
    method: 'GET',
    params: params
  })
}

export function addTrigger(data) {
  return axios({
    url: urlPrefix + '/triggers',
    method: 'POST',
    data: data
  })
}

export function updateTrigger(tid, data) {
  return axios({
    url: urlPrefix + `/triggers/${tid}`,
    method: 'PUT',
    data: data
  })
}

export function deleteTrigger(tid) {
  return axios({
    url: urlPrefix + `/triggers/${tid}`,
    method: 'DELETE'
  })
}

export function applyTrigger(tid) {
  return axios({
    url: urlPrefix + `/triggers/${tid}/apply`,
    method: 'POST'
  })
}

export function cancelTrigger(tid) {
  return axios({
    url: urlPrefix + `/triggers/${tid}/cancel`,
    method: 'POST'
  })
}

export function patternResults(params) {
  return axios({
    url: `${urlPrefix}/triggers/resources`,
    method: 'POST',
    data: params
  })
}
