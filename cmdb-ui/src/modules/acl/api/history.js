import { axios } from '@/utils/request'

const urlPrefix = '/v1/acl'

export function searchPermissonHistory(params) {
    return axios({
        url: urlPrefix + `/audit_log/permission`,
        method: 'GET',
        params: params
    })
}

export function searchRoleHistory(params) {
    return axios({
        url: urlPrefix + `/audit_log/role`,
        method: 'GET',
        params: params
    })
}

export function searchResourceHistory(params) {
    return axios({
        url: urlPrefix + `/audit_log/resource`,
        method: 'GET',
        params: params
    })
}

export function searchTriggerHistory(params) {
    return axios({
        url: urlPrefix + `/audit_log/trigger`,
        method: 'GET',
        params: params
    })
}
