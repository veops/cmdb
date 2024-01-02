import VueI18n from 'vue-i18n'
import zh from './zh'
import en from './en'
import Vue from 'vue'
import zhCN from 'vxe-table/lib/locale/lang/zh-CN'
import enUS from 'vxe-table/lib/locale/lang/en-US'

Vue.use(VueI18n)
const i18n = new VueI18n({
    locale: 'zh', // 初始化中文
    messages: {
        'zh': { ...zh, ...zhCN },
        'en': { ...en, ...enUS },
    },
    silentTranslationWarn: true
})

export default i18n
