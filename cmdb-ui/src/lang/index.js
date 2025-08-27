import Vue from 'vue'
import VueI18n from 'vue-i18n'
import enUS from 'vxe-table/lib/locale/lang/en-US'
import zhCN from 'vxe-table/lib/locale/lang/zh-CN'
import en from './en'
import vi from './vi'
import zh from './zh'

Vue.use(VueI18n)
const i18n = new VueI18n({
    locale: 'zh', // 初始化中文
    messages: {
        'zh': { ...zh, ...zhCN },
        'en': { ...en, ...enUS },
        'vi': { ...vi, ...enUS }, // Sử dụng enUS cho vxe-table vì chưa có locale tiếng Việt
    },
    silentTranslationWarn: true
})

export default i18n
