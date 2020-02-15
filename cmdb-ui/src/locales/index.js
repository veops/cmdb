
import Vue from 'vue'
import VueI18n from 'vue-i18n'
// default language
import enUS from './lang/en-US'
import zhCN from './lang/zh-CN'
// change default accept-language
import { axios } from '@/utils/request'

Vue.use(VueI18n)

export const defaultLang = 'zh-CN'
export const showLocale = true

const messages = {
  'en-US': {
    ...enUS
  },
  'zh-CN': {
    ...zhCN
  }
}

const i18n = new VueI18n({
  locale: defaultLang,
  fallbackLocale: defaultLang,
  messages
})

export default i18n

const loadedLanguages = [defaultLang]

function setI18nLanguage (lang) {
  i18n.locale = lang
  axios.defaults.headers.common['Accept-Language'] = lang
  document.querySelector('html').setAttribute('lang', lang)
  return lang
}

export function i18nRender (key) {
  return i18n.t(key)
}

export function loadLanguageAsync (lang = defaultLang) {
  return new Promise(resolve => {
    Vue.ls.set('lang', lang)
    if (i18n.locale !== lang) {
      if (!loadedLanguages.includes(lang)) {
        return import(/* webpackChunkName: "lang-[request]" */ `./lang/${lang}`).then(msg => {
          i18n.setLocaleMessage(lang, msg.default)
          loadedLanguages.push(lang)
          return setI18nLanguage(lang)
        })
      }
      return resolve(setI18nLanguage(lang))
    }
    return resolve(lang)
  })
}

// if (Vue.ls.get('lang') !== null && defaultLang !== Vue.ls.get('lang')) {
//   loadLanguageAsync(localStorage.lang)
// }
