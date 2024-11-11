import { axios } from '@/utils/request'

export function getIPAMSubnet() {
  return axios({
    url: '/v0.1/ipam/subnet',
    method: 'GET'
  })
}

export function postIPAMSubnet(data) {
  return axios({
    url: '/v0.1/ipam/subnet',
    method: 'POST',
    data
  })
}

export function getIPAMSubnetById(id) {
  return axios({
    url: `/v0.1/ipam/subnet/${id}`,
    method: 'GET'
  })
}

export function putIPAMSubnet(id, data) {
  return axios({
    url: `/v0.1/ipam/subnet/${id}`,
    method: 'PUT',
    data
  })
}

export function deleteIPAMSubnet(id) {
  return axios({
    url: `/v0.1/ipam/subnet/${id}`,
    method: 'DELETE'
  })
}

export function postIPAMScope(data) {
  return axios({
    url: '/v0.1/ipam/scope',
    method: 'POST',
    data
  })
}

export function putIPAMScope(id, data) {
  return axios({
    url: `/v0.1/ipam/scope/${id}`,
    method: 'PUT',
    data
  })
}

export function deleteIPAMScope(id) {
  return axios({
    url: `/v0.1/ipam/scope/${id}`,
    method: 'DELETE'
  })
}

export function getIPAMAddress(params) {
  return axios({
    url: '/v0.1/ipam/address',
    method: 'GET',
    params
  })
}

export function getIPAMHosts(params) {
  return axios({
    url: '/v0.1/ipam/subnet/hosts',
    method: 'GET',
    params
  })
}

export function postIPAMAddress(data) {
  return axios({
    url: '/v0.1/ipam/address',
    method: 'POST',
    data
  })
}

export function getIPAMHistoryOperate(params) {
  return axios({
    url: '/v0.1/ipam/history/operate',
    method: 'GET',
    params
  })
}

export function getIPAMHistoryScan(params) {
  return axios({
    url: '/v0.1/ipam/history/scan',
    method: 'GET',
    params
  })
}

export function getIPAMStats(params) {
  return axios({
    url: '/v0.1/ipam/stats',
    method: 'GET',
    params
  })
}
