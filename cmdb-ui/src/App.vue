<template>
  <a-config-provider :locale="locale">
    <div id="app" :class="{ 'ops-fullscreen': isOpsFullScreen, 'ops-only-topmenu': isOpsOnlyTopMenu }">
      <router-view v-if="alive" />
    </div>
  </a-config-provider>
</template>

<script>
import { mapActions } from 'vuex'
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'
import { AppDeviceEnquire } from '@/utils/mixin'
import { debounce } from './utils/util'

export default {
  mixins: [AppDeviceEnquire],
  provide() {
    return {
      reload: this.reload,
    }
  },
  data() {
    return {
      locale: zhCN,
      alive: true,
      timer: null,
    }
  },
  computed: {
    isOpsFullScreen() {
      return this.$route.name === 'cmdb_screen'
    },
    isOpsOnlyTopMenu() {
      return ['fullscreen_index', 'setting_person'].includes(this.$route.name)
    },
  },
  created() {
    this.timer = setInterval(() => {
      this.setTime(new Date().getTime())
    }, 1000)
  },
  mounted() {
    this.$store.dispatch('setWindowSize')
    window.addEventListener(
      'resize',
      debounce(() => {
        this.$store.dispatch('setWindowSize')
      })
    )
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    ...mapActions(['setTime']),
    reload() {
      this.alive = false
      this.$nextTick(() => {
        this.alive = true
      })
    },
  },
}
</script>
<style lang="less">
@import './style/index.less';

#app {
  height: 100%;
}
</style>
