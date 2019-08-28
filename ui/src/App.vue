<template>
  <a-locale-provider :locale="locale">
    <div id="app">
      <router-view v-if="alive" />
    </div>
  </a-locale-provider>
</template>

<script>
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'
import { AppDeviceEnquire } from '@/utils/mixin'

export default {
  mixins: [AppDeviceEnquire],
  provide () {
    return {
      reload: this.reload
    }
  },
  data () {
    return {
      locale: zhCN,
      alive: true
    }
  },
  mounted () {},
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
