import { axios } from '@/utils/request'

export function getPreference(instance = true, tree = null) {
  return axios({
    url: '/v0.1/preference/ci_types',
    method: 'GET',
    params: { instance: instance, tree: tree }
  })
}

export function getPreference2(instance = true, tree = null) {
  return axios({
    url: '/v0.1/preference/ci_types2',
    method: 'GET',
    params: { instance: instance, tree: tree }
  })
}

export function getSubscribeAttributes(ciTypeId) {
  return axios({
    url: `/v0.1/preference/ci_types/${ciTypeId}/attributes`,
    method: 'GET'
  })
}

export function getSubscribeTreeView() {
  return axios({
    url: '/v0.1/preference/tree/view',
    method: 'GET'
  })
}

export function subscribeCIType(ciTypeId, attrs) {
  return axios({
    url: `/v0.1/preference/ci_types/${ciTypeId}/attributes`,
    method: 'POST',
    data: {
      attr: attrs
    }
  })
}

export function subscribeTreeView(ciTypeId, levels) {
  return axios({
    url: `/v0.1/preference/tree/view`,
    method: 'POST',
    data: { type_id: ciTypeId, levels: levels }
  })
}

export function getRelationView() {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'GET'
  })
}

export function deleteRelationView(viewName) {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'DELETE',
    data: { name: viewName }
  })
}

export function subscribeRelationView(payload) {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'POST',
    data: payload
  })
}

export function putRelationView(id, data) {
  return axios({
    url: `/v0.1/preference/relation/view/${id}`,
    method: 'put',
    data
  })
}

// 用户保存条件过滤选项
export function getPreferenceSearch(payload) {
  // 参数有prv_id: 关系视图的id， ptv_id: 层级视图的id, type_id: 模型id
  return axios({
    url: `/v0.1/preference/search/option`,
    method: 'GET',
    params: payload
  })
}

export function savePreferenceSearch(payload) {
  // 参数包括GET的参数 ，必须参数name，option option是个json
  return axios({
    url: `/v0.1/preference/search/option`,
    method: 'POST',
    data: payload
  })
}

export function deletePreferenceSearch(id) {
  return axios({
    url: `/v0.1/preference/search/option/${id}`,
    method: 'DELETE',
  })
}

// 服务树授权
export function grantRelationView(rid, data) {
  return axios({
    url: `/v0.1/preference/relation/view/roles/${rid}/grant`,
    method: 'POST',
    data: data
  })
}

// 服务树权限回收
export function revokeRelationView(rid, data) {
  return axios({
    url: `/v0.1/preference/relation/view/roles/${rid}/revoke`,
    method: 'POST',
    data: data
  })
}

// preference citype order
export function preferenceCitypeOrder(data) {
  return axios({
    url: `/v0.1/preference/ci_types/order`,
    method: 'POST',
    data: data
  })
}
