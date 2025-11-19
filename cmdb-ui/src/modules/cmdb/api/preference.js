import { axios } from '@/utils/request'
import { CI_DEFAULT_ATTR } from '@/modules/cmdb/utils/const.js'
import i18n from '@/lang'

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

export function getSubscribeAttributes(ciTypeId, formatDefaultAttr = true) {
  return new Promise(async (resolve) => {
    const res = await axios({
      url: `/v0.1/preference/ci_types/${ciTypeId}/attributes`,
      method: 'GET'
    })

    if (
      formatDefaultAttr &&
      res?.attributes?.length
    ) {
      res.attributes.forEach((item) => {
        switch (item.name) {
          case CI_DEFAULT_ATTR.UPDATE_USER:
            item.id = item.name
            item.alias = i18n.t('cmdb.components.updater')
            break
          case CI_DEFAULT_ATTR.UPDATE_TIME:
            item.id = item.name
            item.alias = i18n.t('cmdb.components.updateTime')
            break
          default:
            break
        }
      })
    }

    resolve(res)
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

// User save condition filter options
export function getPreferenceSearch(payload) {
  // Parameters include prv_id: relation view id, ptv_id: hierarchy view id, type_id: model id
  return axios({
    url: `/v0.1/preference/search/option`,
    method: 'GET',
    params: payload
  })
}

export function savePreferenceSearch(payload) {
  // Parameters include GET parameters, required parameter name, option is a JSON
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

// Service tree authorization
export function grantRelationView(rid, data) {
  return axios({
    url: `/v0.1/preference/relation/view/roles/${rid}/grant`,
    method: 'POST',
    data: data
  })
}

// Service tree permission revocation
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

export function getAutoSubscription() {
  return axios({
    url: '/v0.1/preference/auto_subscription',
    method: 'get',
  })
}

export function putAutoSubscription(data) {
  return axios({
    url: '/v0.1/preference/auto_subscription',
    method: 'put',
    data
  })
}
