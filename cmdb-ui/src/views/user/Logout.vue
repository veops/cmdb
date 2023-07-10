<template>
  <h1>{{ msg }}</h1>
</template>

<script>
import config from '@/config/setting'
import appConfig from '@/config/app'

export default {
  name: 'Logout',
  data() {
    return {
      msg: '正在退出，请稍后',
    }
  },
  mounted() {
    if (config.useSSO) {
        window.location.href = appConfig.ssoLogoutURL
    } else {
    }
  },
}
</script>
