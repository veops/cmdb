<template>
  <a-card>
    <div class="dashboard-title">{{ title }}</div>
    <components :is="componentName" />
  </a-card>
</template>

<script>
import SummaryCounter from './summaryCounter.vue'
import SystemCounter from './systemCounter.vue'
import BusinessCounter from './businessCounter.vue'
export default {
  name: 'DashboardCard',
  components: { SummaryCounter, SystemCounter, BusinessCounter },
  props: {
    title: {
      type: String,
      default: '',
    },
    componentName: {
      type: String,
      default: '',
    },
  },
}
</script>

<style lang="less" scoped>
.dashboard-title {
  font-size: large;
  font-weight: 500;
  border-left: 4px solid #57738e;
  padding-left: 8px;
  margin-bottom: 5px;
}
</style>
