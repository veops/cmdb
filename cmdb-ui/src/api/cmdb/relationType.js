import { axios } from '@/utils/request'

export function getRelationTypes () {
  return axios({
    url: '/v0.1/relation_types',
    method: 'GET'
  })
}

export function addRelationType (payload) {
  return axios({
    url: `/v0.1/relation_types`,
    method: 'POST',
    data: payload
  })
}

export function updateRelationType (rtId, payload) {
  return axios({
    url: `/v0.1/relation_types/${rtId}`,
    method: 'PUT',
    data: payload
  })
}

export function deleteRelationType (rtId) {
  return axios({
    url: `/v0.1/relation_types/${rtId}`,
    method: 'DELETE'
  })
}
