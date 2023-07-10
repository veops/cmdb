import { axios } from '@/utils/request'

export function getCustomDashboard() {
    return axios({
        url: '/v0.1/custom_dashboard',
        method: 'get',
    })
}

export function postCustomDashboard(data) {
    return axios({
        url: '/v0.1/custom_dashboard',
        method: 'post',
        data
    })
}

export function putCustomDashboard(id, data) {
    return axios({
        url: `/v0.1/custom_dashboard/${id}`,
        method: 'put',
        data
    })
}

export function deleteCustomDashboard(id) {
    return axios({
        url: `/v0.1/custom_dashboard/${id}`,
        method: 'delete',
    })
}

export function batchUpdateCustomDashboard(data) {
    return axios({
        url: `/v0.1/custom_dashboard/batch`,
        method: 'put',
        data
    })
}
