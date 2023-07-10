import { axios } from '@/utils/request'

export const getNoticeApps = () => {
    return axios({
        url: `/common-setting/v1/message/apps`,
        method: 'get',
    })
}

export const getNoticeCategoriesByApp = (app_name) => {
    return axios({
        url: `/common-setting/v1/message/${app_name}/categories`,
        method: 'get',
    })
}

export const getMessage = (params) => {
    return axios({
        url: `/common-setting/v1/message`,
        method: 'get',
        params
    })
}

export const postMessage = (data) => {
    return axios({
        url: `/common-setting/v1/message`,
        method: 'post',
        data
    })
}

export const updateMessage = (id, data) => {
    return axios({
        url: `/common-setting/v1/message/${id}`,
        method: 'put',
        data
    })
}

export const getUnreadMessageCount = (params) => {
    return axios({
        url: `/common-setting/v1/message/unread`,
        method: 'get',
        params
    })
}

export const batchUpdateMessage = (data) => {
    return axios({
        url: `/common-setting/v1/message/batch`,
        method: 'post',
        data
    })
}
