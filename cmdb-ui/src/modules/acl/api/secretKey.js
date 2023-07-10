import { axios } from '@/utils/request'

export function getSecret() {
    return axios({
        url: '/v1/acl/users/secret',
        method: 'GET'
    })
}

export function updateSecret(data) {
    return axios({
        url: '/v1/acl/users/reset_key_secret',
        method: 'POST',
        data,
    })
}
