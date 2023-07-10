import { axios } from '@/utils/request'

export function getWX() {
    return axios({
        url: '/v1/acl/users',
        method: 'GET'
    })
}
