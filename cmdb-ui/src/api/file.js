import { axios } from '@/utils/request'

export function postImageFile(parameter) {
    return axios({
        url: '/common-setting/v1/file',
        method: 'post',
        data: parameter,
    })
}

export function getFileData(data_type) {
    return axios({
        url: `/common-setting/v1/data/${data_type}`,
        method: 'get',
    })
}

export function addFileData(data_type, data) {
    return axios({
        url: `/common-setting/v1/data/${data_type}`,
        method: 'post',
        data,
    })
}

export function deleteFileData(data_type, id) {
    return axios({
        url: `/common-setting/v1/data/${data_type}/${id}`,
        method: 'delete',
    })
}
