<template>
  <page-view :title="false" :avatar="avatar">
    <a-card :bordered="false" style="margin: -24px -24px 0px;">
      <result type="error" :title="title" :description="description">
        <template slot="action">
          <a-button type="primary" @click="$router.push('/')" >欢迎访问</a-button>
        </template>
      </result>
    </a-card>
  </page-view>
</template>

<script>
import { Result } from '@/components'
import PageView from '@/layouts/PageView'

export default {
  name: 'Error',
  components: {
    PageView,
    Result
  },
  data () {
    return {
      title: '欢迎访问',
      description: '欢迎使用本系统......^-^'
    }
  }
}
</script>

<style scoped>

</style>
