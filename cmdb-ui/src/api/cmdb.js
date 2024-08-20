import { axios } from '@/utils/request'

export function searchCI(params, isShowMessage = true) {
  return axios({
    url: `/v0.1/ci/s`,
    method: 'GET',
    params: params,
    isShowMessage
  })
}

export function getCIType(CITypeName, parameter) {
  return axios({
    url: `/v0.1/ci_types/${CITypeName}`,
    method: 'GET',
    params: parameter
  })
}
