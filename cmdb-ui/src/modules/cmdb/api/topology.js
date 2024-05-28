import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function getTopoGroups() {
  return axios({
    url: `${urlPrefix}/topology_views`,
    method: 'GET',
  })
}

export function getTopoView(_id) {
  return axios({
    url: `${urlPrefix}/topology_views/${_id}`,
    method: 'GET',
  })
}

export function postTopoGroup(data) {
  return axios({
      url: `${urlPrefix}/topology_views/groups`,
      method: 'POST',
      data: data
  })
}

export function putTopoGroupByGId(gid, data) {
  return axios({
      url: `${urlPrefix}/topology_views/groups/${gid}`,
      method: 'PUT',
      data: data
  })
}

export function putTopoGroupsOrder(data) {
  return axios({
      url: `${urlPrefix}/topology_views/groups/order`,
      method: 'PUT',
      data: data
  })
}

export function deleteTopoGroup(gid, data) {
  return axios({
      url: `${urlPrefix}/topology_views/groups/${gid}`,
      method: 'DELETE',
      data: data
  })
}

export function addTopoView(data) {
  return axios({
      url: `${urlPrefix}/topology_views`,
      method: 'POST',
      data: data
  })
}

export function updateTopoView(_id, data) {
  return axios({
      url: `${urlPrefix}/topology_views/${_id}`,
      method: 'PUT',
      data: data
  })
}

export function deleteTopoView(_id) {
  return axios({
      url: `${urlPrefix}/topology_views/${_id}`,
      method: 'DELETE',
  })
}

export function getRelationsByTypeId(_id) {
  return axios({
    url: `${urlPrefix}/topology_views/relations/ci_types/${_id}`,
    method: 'GET',
  })
}

export function previewTopoView(params) {
  return axios({
    url: `${urlPrefix}/topology_views/preview`,
    method: 'POST',
    data: params,
  })
}

export function showTopoView(_id) {
  return axios({
    url: `${urlPrefix}/topology_views/${_id}/view`,
    method: 'GET',
  })
}

export function grantTopologyView(viewId, rid, data) {
  return axios({
    url: `/v0.1/topology_views/${viewId}/roles/${rid}/grant`,
    method: 'POST',
    data: data
  })
}

export function revokeTopologyView(viewId, rid, data) {
  return axios({
    url: `/v0.1/topology_views/${viewId}/roles/${rid}/revoke`,
    method: 'POST',
    data: data
  })
}
