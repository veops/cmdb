import { getCompanyInfo } from '@/api/company'

const logo = {
    state: {
        file_name: '',
        small_file_name: ''
    },
    mutations: {
        SET_FILENAME: (state, name) => {
            state.file_name = name
        },
        SET_SMALL_FILENAME: (state, name) => {
            state.small_file_name = name
        }
    },
    actions: {
        getCompanyInfo({ commit }) {
            return new Promise((resolve, reject) => {
                getCompanyInfo().then(res => {
                    commit('SET_FILENAME', res.info.logoName)
                    commit('SET_SMALL_FILENAME', res.info.smallLogoName)
                    resolve(res.info)
                }).catch(err => {
                    console.log('获取失败', err)
                    reject(err)
                })
            })
        }
    }
}
export default logo
