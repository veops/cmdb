import { axios } from '@/utils/request'

export function getSystemLanguage() {
  return axios({
    url: '/common-setting/v1/system/language',
    method: 'get',
  })
}
