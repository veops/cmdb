import { axios } from '@/utils/request'

// 保存布局
export function saveSystemConfig(data) {
    return axios({
        url: '/v0.1/system_config',
        method: 'POST',
        data
    })
}

// 获取布局
export function getSystemConfig(params) {
    return axios({
        url: '/v0.1/system_config',
        method: 'GET',
        params
    })
}
