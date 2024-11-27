<template>
  <div class="stats-chart">
    <div
      class="stats-chart-pie"
      ref="statsChartRef"
    ></div>
    <div class="stats-chart-ratio">
      {{ chartRatio }}%
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'DCIMStatsChart',
  props: {
    chartRatio: {
      type: Number,
      default: 0
    },
    chartData: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    chartData: {
      deep: true,
      immediate: true,
      handler(data) {
        this.updateChart(data)
      }
    }
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  },
  methods: {
    updateChart(data) {
      const option = {
        color: data?.map?.((item) => item.color) || [],
        tooltip: {
          show: false
        },
        legend: {
          show: false,
        },
        series: [
          {
            type: 'pie',
            radius: ['60%', '85%'],
            data: data?.map((item) => {
              return {
                name: this.$t(item?.label),
                value: item?.value || 0
              }
            }) || [],
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 1
            },
            label: {
              show: false,
            },
          }
        ]
      }

      this.$nextTick(() => {
        if (!this.chart) {
          const el = this.$refs.statsChartRef
          this.chart = echarts.init(el)
        }
        this.chart.setOption(option)
      })
    }
  }
}
</script>

<style lang="less" scoped>
.stats-chart {
  width: 60px;
  height: 60px;
  position: relative;
  flex-shrink: 0;

  &-pie {
    width: 100%;
    height: 100%;
  }

  &-ratio {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2;

    font-size: 14px;
    font-weight: 700;
    color: #1D2129;
  }
}
</style>
