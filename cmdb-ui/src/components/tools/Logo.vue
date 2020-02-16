<template>
  <div class="logo">
    <router-link :to="{name:'cmdb'}">
      <div style="text-align: center; margin-right: 24px">
        <div style="display: inline-block;">
          <img src="@/assets/cmdb.png" width="50px" height="50px" style="margin:0; padding:0" />
        </div>
        <h1 v-if="showTitle">{{ title }}</h1>
      </div>
    </router-link>
  </div>
</template>

<script>
import LogoSvg from '@/assets/logo.svg?inline'

export default {
  name: 'Logo',
  components: {
    LogoSvg
  },
  props: {
    title: {
      type: String,
      default: 'CMDB',
      required: false
    },
    showTitle: {
      type: Boolean,
      default: true,
      required: false
    }
  }
}
</script>
