<template>
  <div class="top-menu" v-if="routes.length > 2">
    <a-menu v-model="current" mode="horizontal">
      <a-menu-item :key="route.name" v-for="route in routes.slice(0, routes.length - 1)">
        <router-link :to="{name: route.name}">{{ route.meta.title }}</router-link>
      </a-menu-item>
    </a-menu>
  </div>
</template>

<script>
import store from '@/store'

export default {
  data () {
    return {
      routes: store.getters.addRouters,
      current: [store.getters.addRouters[0].name]
    }
  }
}
</script>

<style lang="less">
.top-menu {
  display: inline-block;
}
.ant-menu-horizontal {
  border-bottom: 0 !important;
}
.ant-menu-horizontal > .ant-menu-item {
  border-bottom: 0;
}
</style>
