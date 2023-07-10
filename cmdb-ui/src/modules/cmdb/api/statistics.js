import { axios } from '@/utils/request'

export function getStatistics() {
    return axios({
        url: '/v0.1/statistics',
        method: 'GET'
    })
}
