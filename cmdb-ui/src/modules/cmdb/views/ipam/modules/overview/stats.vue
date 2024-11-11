<template>
  <div class="stats">
    <div
      class="stats-card"
      v-for="(item, index) in statsListData"
      :key="index"
    >
      <div class="stats-card-left">
        <div class="stats-card-title">{{ $t(item.title) }}</div>

        <div class="stats-card-row">
          <div
            v-for="(dataItem, dataIndex) in item.data"
            :key="dataIndex"
            class="stats-card-data"
          >
            <span class="stats-card-data-label">{{ $t(dataItem.label) }}</span>
            <span class="stats-card-data-value">{{ dataItem.value }}</span>
          </div>
        </div>
      </div>

      <div
        v-if="item.logo"
        class="stats-card-logo"
      >
        <ops-icon
          :type="item.logo"
          class="stats-card-logo-icon"
        />
      </div>

      <StatsChart
        v-else
        :statsData="item"
      />
    </div>
  </div>
</template>

<script>
import StatsChart from './statsChart.vue'

export default {
  name: 'Statistics',
  components: {
    StatsChart
  },
  props: {
    statsData: {
      type: Object,
      default: () => {}
    }
  },
  computed: {
    statsListData() {
      const {
        subnet_num = 0,
        address_num = 0,
        address_free_num = 0,
        address_assign_num = 0,
        address_unassign_num = 0,
        address_used_num = 0,
        address_used_free_num = 0
      } = this.statsData || {}

      return [
        {
          title: 'cmdb.ipam.subnetStats',
          logo: 'caise-IPAM',
          data: [
            {
              label: 'cmdb.ipam.total',
              value: subnet_num
            }
          ]
        },
        {
          title: 'cmdb.ipam.addressStats',
          data: [
            {
              label: 'cmdb.ipam.total',
              value: address_num,
              chartValue: address_num - address_free_num,
            },
            {
              label: 'cmdb.ipam.free',
              value: address_free_num
            }
          ],
          ratio: address_num && address_free_num ? Math.round((address_free_num / address_num) * 100) : 0,
          chartColor: ['#6EE3EB', '#6592FD']
        },
        {
          title: 'cmdb.ipam.assignStats',
          data: [
            {
              label: 'cmdb.ipam.assigned',
              value: address_assign_num
            },
            {
              label: 'cmdb.ipam.unassigned',
              value: address_unassign_num
            }
          ],
          ratio: address_num && address_assign_num ? Math.round((address_assign_num / address_num) * 100) : 0,
          chartColor: ['#8C85ED', '#387BFD']
        },
        {
          title: 'cmdb.ipam.onlineStats',
          data: [
            {
              label: 'cmdb.ipam.online',
              value: address_used_num
            },
            {
              label: 'cmdb.ipam.offline',
              value: address_used_free_num
            }
          ],
          ratio: address_num && address_used_num ? Math.round((address_used_num / address_num) * 100) : 0,
          chartColor: ['#009FA9', '#17D4B0']
        },
      ]
    }
  },
  watch: {
    statsData: {
      deep: true,
      immediate: true,
      handler(data) {
        this.initData(data)
      }
    }
  },
  methods: {
    initData() {

    }
  }
}
</script>

<style lang="less" scoped>
.stats {
  width: 100%;
  display: flex;
  column-gap: 24px;
  row-gap: 12px;

  &-card {
    padding: 14px 17px;
    background-color: #F7F8FA;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;

    &-left {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
    }

    &-title {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
    }

    &-row {
      display: flex;
      align-items: baseline;
      margin-top: 12px;
      flex-wrap: wrap;
      column-gap: 25px;
    }

    &-data {
      display: flex;

      &-label {
        font-size: 14px;
        font-weight: 400;
        color: #1D2129;
      }

      &-value {
        font-size: 14px;
        font-weight: 700;
        color: #1D2129;
        margin-left: 6px;
      }
    }

    &-logo {
      width: 52px;
      height: 52px;
      border-radius: 52px;
      background-color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;

      &-icon {
        font-size: 25px;
      }
    }
  }
}
</style>
