import { axios } from '@/utils/request'

export function getAuthData(data_type) {
    return axios({
        url: `/common-setting/v1/auth_config/${data_type}`,
        method: 'get',
    })
}

export function postAuthData(data_type, data) {
    return axios({
        url: `/common-setting/v1/auth_config/${data_type}`,
        method: 'post',
        data,
    })
}

export function putAuthData(data_type, id, data) {
    return axios({
        url: `/common-setting/v1/auth_config/${data_type}/${id}`,
        method: 'put',
        data,
    })
}

export function getAuthDataEnable() {
    return axios({
        url: `/common-setting/v1/auth_config/enable_list`,
        method: 'get',
    })
}


export function testLDAP(test_type, data) {
    return axios({
        url: `/common-setting/v1/auth_config/LDAP/test?test_type=${test_type}`,
        method: 'post',
        data,
    })
}
