import { axios } from '@/utils/request'

export function sendTestEmail(receive_address, data) {
  return axios({
    url: `/common-setting/v1/notice_config/send_test_email?receive_address=${receive_address}`,
    method: 'post',
    data
  })
}

export const getNoticeConfigByPlatform = (platform) => {
  return axios({
    url: '/common-setting/v1/notice_config',
    method: 'get',
    params: { ...platform },
  })
}

export const postNoticeConfigByPlatform = (data) => {
  return axios({
    url: '/common-setting/v1/notice_config',
    method: 'post',
    data
  })
}

export const putNoticeConfigByPlatform = (id, info) => {
  return axios({
    url: `/common-setting/v1/notice_config/${id}`,
    method: 'put',
    data: info
  })
}

export const getNoticeConfigAppBot = () => {
  return axios({
    url: `/common-setting/v1/notice_config/app_bot`,
    method: 'get',
  })
}
