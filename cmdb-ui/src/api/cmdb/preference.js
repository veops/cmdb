import { axios } from '@/utils/request'

export function getPreference (instance = true, tree = null) {
  return axios({
    url: '/v0.1/preference/ci_types',
    method: 'GET',
    params: { instance: instance, tree: tree }
  })
}

export function getSubscribeAttributes (ciTypeId) {
  return axios({
    url: `/v0.1/preference/ci_types/${ciTypeId}/attributes`,
    method: 'GET'
  })
}

export function getSubscribeTreeView () {
  return axios({
    url: '/v0.1/preference/tree/view',
    method: 'GET'
  })
}

export function subscribeCIType (ciTypeId, attrs) {
  return axios({
    url: `/v0.1/preference/ci_types/${ciTypeId}/attributes`,
    method: 'POST',
    data: {
      attr: attrs
    }
  })
}

export function subscribeTreeView (ciTypeId, levels) {
  return axios({
    url: `/v0.1/preference/tree/view`,
    method: 'POST',
    data: { type_id: ciTypeId, levels: levels }
  })
}

export function getRelationView () {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'GET'
  })
}

export function deleteRelationView (viewName) {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'DELETE',
    data: { name: viewName }
  })
}

export function subscribeRelationView (payload) {
  return axios({
    url: `/v0.1/preference/relation/view`,
    method: 'POST',
    data: payload
  })
}
