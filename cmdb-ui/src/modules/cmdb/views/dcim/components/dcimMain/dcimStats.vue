<template>
  <div class="dcim-stats">
    <div
      v-for="(item, index) in statsList"
      :key="index"
      class="dcim-stats-card"
    >
      <div class="dcim-stats-card-left">
        <div class="dcim-stat-card-title">{{ $t(item.title) }}</div>

        <div class="dcim-stats-card-row">
          <div
            v-for="(data, dataIndex) in item.countList"
            :key="dataIndex"
            class="dcim-stats-card-count"
          >
            <span class="dcim-stats-card-count-label">{{ $t(data.label) }}:</span>
            <span class="dcim-stats-card-count-value">{{ data.value }}</span>
          </div>
        </div>
      </div>

      <div
        v-if="item.icon"
        class="dcim-stats-card-icon"
      >
        <ops-icon
          :type="item.icon"
        />
      </div>

      <DCIMStatsChart
        v-else-if="item.chartData"
        :chartData="item.chartData"
        :chartRatio="item.chartRatio"
      />
    </div>
  </div>
</template>

<script>
import DCIMStatsChart from './dcimStatsChart.vue'

export default {
  name: 'DCIMStats',
  props: {
    statsData: {
      type: Object,
      default: () => {}
    }
  },
  components: {
    DCIMStatsChart
  },
  computed: {
    statsList() {
      const {
        device_count = 0,
        rack_count = 0,
        u_count = 0,
        u_used_count = 0,
      } = this.statsData || {}

      return [
        {
          title: 'cmdb.dcim.rackCount',
          icon: 'veops-cabinet',
          countList: [
            {
              label: 'cmdb.dcim.total',
              value: rack_count
            }
          ]
        },
        {
          title: 'cmdb.dcim.deviceCount',
          icon: 'veops-device',
          countList: [
            {
              label: 'cmdb.dcim.total',
              value: device_count
            }
          ]
        },
        {
          title: 'cmdb.dcim.utilizationRation',
          countList: [
            {
              label: 'cmdb.dcim.used',
              value: `${u_used_count}u`
            },
            {
              label: 'cmdb.dcim.unused',
              value: `${u_count - u_used_count}u`
            }
          ],
          chartRatio: u_used_count > 0 && u_count > 0 ? Math.round((u_used_count / u_count) * 100) : 0,
          chartData: [
            {
              label: 'cmdb.dcim.used',
              value: u_used_count,
              color: '#009FA9'
            },
            {
              label: 'cmdb.dcim.unused',
              value: u_count - u_used_count,
              color: '#17D4B0'
            }
          ]
        },
      ]
    }
  }
}
</script>

<style lang="less" scoped>
.dcim-stats {
  width: 100%;
  display: flex;
  align-items: stretch;
  column-gap: 16px;
  flex-shrink: 0;

  &-card {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 24px;
    background-color: #F7F8FA;
    filter: drop-shadow(0px 0px 12px rgba(231, 236, 239, 0.10));

    &-left {
      width: 100%;
      margin-right: 12px;
    }

    &-title {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
    }

    &-row {
      display: flex;
      flex-wrap: wrap;
      margin-top: 12px;
      column-gap: 12px;
    }

    &-count {
      flex-shrink: 0;
      display: flex;
      align-items: baseline;

      &-label {
        font-size: 14px;
        font-weight: 400;
        color: #1D2129;
      }

      &-value {
        font-size: 16px;
        font-weight: 700;
        color: #1D2129;
        margin-left: 6px;
      }
    }

    &-icon {
      width: 52px;
      height: 52px;
      border-radius: 52px;
      background-color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      flex-shrink: 0;
    }
  }
}
</style>
