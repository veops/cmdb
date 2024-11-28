import { axios } from '@/utils/request'

export function getDCIMTreeView(params) {
  return axios({
    url: '/v0.1/dcim/tree_view ',
    method: 'GET',
    params
  })
}

export function getDCIMById(type, id) {
  return axios({
    url: `/v0.1/dcim/${type}/${id}`,
    method: 'GET'
  })
}

export function postDCIM(type, data) {
  return axios({
    url: `/v0.1/dcim/${type}`,
    method: 'POST',
    data
  })
}

export function putDCIM(type, id, data) {
  return axios({
    url: `/v0.1/dcim/${type}/${id}`,
    method: 'PUT',
    data
  })
}

export function deleteDCIM(type, id) {
  return axios({
    url: `/v0.1/dcim/${type}/${id}`,
    method: 'DELETE',
  })
}

export function getDCIMRacks(id, params) {
  return axios({
    url: `/v0.1/dcim/server_room/${id}/racks`,
    method: 'GET',
    params
  })
}

export function postDevice(rackId, deviceId, data) {
  return axios({
    url: `/v0.1/dcim/rack/${rackId}/device/${deviceId}`,
    method: 'POST',
    data
  })
}

export function deleteDevice(rackId, deviceId) {
  return axios({
    url: `/v0.1/dcim/rack/${rackId}/device/${deviceId}`,
    method: 'DELETE'
  })
}

export function putDevice(rackId, deviceId, data) {
  return axios({
    url: `/v0.1/dcim/rack/${rackId}/device/${deviceId}`,
    method: 'PUT',
    data
  })
}

export function migrateDevice(rackId, deviceId, data) {
  return axios({
    url: `/v0.1/dcim/rack/${rackId}/device/${deviceId}/migrate`,
    method: 'PUT',
    data
  })
}

export function getDCIMHistoryOperate(params) {
  return axios({
    url: `/v0.1/dcim/history/operate`,
    method: 'GET',
    params
  })
}

export function calcUnitFreeCount() {
  return axios({
    url: `/v0.1/dcim/rack/calc_u_free_count`,
    method: 'POST'
  })
}
