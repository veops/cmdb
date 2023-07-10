<template>
  <div>
    <a-row :gutter="[12, 12]">
      <a-col v-for="item in dashboardList" :key="item.title" :span="item.span">
        <DashboardCard :title="item.title" :componentName="item.component" />
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { dashboardList } from './constants.js'
import { getStatistics } from '../../api/statistics'
import DashboardCard from './components/dashboardCard.vue'
export default {
  name: 'CmdbDashboard',
  components: { DashboardCard },
  data() {
    return {
      dashboardList,
      statistics: {},
      interval: null,
    }
  },
  provide() {
    return {
      statistics: () => {
        return this.statistics
      },
    }
  },
  mounted() {
    this.getData()
    this.interval = setInterval(() => {
      this.getData()
    }, 30000)
  },
  methods: {
    getData() {
      getStatistics().then((res) => {
        this.statistics = res
      })
    },
  },
}
</script>

<style></style>
