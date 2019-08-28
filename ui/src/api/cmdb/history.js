import { axios } from '@/utils/request'

export function getCIHistory (ciId) {
  return axios({
    url: `/v0.1/history/ci/${ciId}`,
    method: 'GET'
  })
}
