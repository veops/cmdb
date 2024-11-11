<template>
  <div class="overview">
    <Stats :statsData="statsData" />
    <SubnetTable :tableData="tableData" />
  </div>
</template>

<script>
import { getIPAMStats } from '@/modules/cmdb/api/ipam.js'

import Stats from './stats.vue'
import SubnetTable from './subnetTable.vue'

export default {
  name: 'Overview',
  components: {
    Stats,
    SubnetTable
  },
  props: {
    nodeId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      statsData: {},
      tableData: []
    }
  },
  watch: {
    nodeId: {
      deep: true,
      immediate: true,
      handler(newValue, oldValue) {
        if (newValue !== oldValue) {
          this.initData(newValue)
        }
      }
    }
  },
  methods: {
    async initData() {
      const res = await getIPAMStats({
        parent_id: this.nodeId === 'all' ? 0 : this.nodeId
      })
      const tableData = res?.subnets || []
      tableData.forEach((item) => {
        item.hosts_count = item?.hosts_count || 0
        item.used_ratio = item?.used_count && item?.hosts_count ? Math.round((item.used_count / item.hosts_count) * 100) : 0
      })

      this.statsData = res
      this.tableData = tableData
    }
  }
}
</script>

<style lang="less" scoped>
.overview {
  width: 100%;
}
</style>
