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

export function postUploadFile(parameter) {
    return axios({
        url: '/common-setting/v1/upload-file',
        method: 'post',
        data: parameter,
    })
}

export function getUploadFile(file_id) {
    return axios({
        url: `/common-setting/v1/upload-file/${file_id}`,
        method: 'get',
    })
}

export function postReviewFile(parameter) {
    return axios({
        url: '/common-setting/v1/review-file',
        method: 'post',
        data: parameter,
    })
}

export function getReviewFile(file_id) {
    return axios({
        url: `/common-setting/v1/review-file/${file_id}`,
        method: 'get',
    })
}
