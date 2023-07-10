import { axios } from '@/utils/request'

const urlPrefix = '/v0.1'

export function getCITypeGroups(params) {
    return axios({
        url: `${urlPrefix}/ci_types/groups`,
        method: 'GET',
        params: params
    })
}

export function postCITypeGroup(data) {
    return axios({
        url: `${urlPrefix}/ci_types/groups`,
        method: 'POST',
        data: data
    })
}

export function putCITypeGroupByGId(gid, data) {
    return axios({
        url: `${urlPrefix}/ci_types/groups/${gid}`,
        method: 'PUT',
        data: data
    })
}

export function deleteCITypeGroup(gid, data) {
    return axios({
        url: `${urlPrefix}/ci_types/groups/${gid}`,
        method: 'DELETE',
        data: data
    })
}

export function getCITypeGroupsConfig(params) {
    return axios({
        url: `${urlPrefix}/ci_types/groups/config`,
        method: 'GET',
        params: params
    })
}

// 更新模型配置分组的排序
export const putCITypeGroups = (data) => {
    return axios({
        url: `${urlPrefix}/ci_types/groups/order`,
        method: 'PUT',
        data: data
    })
}
