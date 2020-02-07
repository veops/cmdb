<template>
  <a-locale-provider :locale="locale">
    <div id="app">
      <router-view v-if="alive" />
    </div>
  </a-locale-provider>
</template>

<script>
import i18n from '@/locales'
import { AppDeviceEnquire } from '@/utils/mixin'
import { mixin } from '@/store/i18n-mixin'

export default {
  mixins: [AppDeviceEnquire, mixin],
  provide () {
    return {
      reload: this.reload
    }
  },
  data () {
    return {
      locale: {},
      alive: true
    }
  },
  created () {
    this.$watch('currentLang', () => {
      this.locale = i18n.getLocaleMessage(this.currentLang).antLocale
    })
  },

  methods: {
    reload () {
      this.alive = false
      this.$nextTick(() => {
        this.alive = true
      })
    }
  }
}
</script>
<style>
#app {
  height: 100%;
}
</style>
