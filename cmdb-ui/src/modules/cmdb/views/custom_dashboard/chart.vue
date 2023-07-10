<template>
  <div :style="{ width: '100%', height: 'calc(100% - 2.2vw)' }">
    <div v-if="category === 0" class="cmdb-dashboard-grid-item-chart">
      <span :style="{ ...options.fontConfig }">{{ toThousands(data) }}</span>
    </div>
    <div
      :id="`cmdb-dashboard-${chartId}-${editable}`"
      v-if="category === 1 || category === 2"
      class="cmdb-dashboard-grid-item-chart"
    ></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mixin } from '@/utils/mixin'
import { toThousands } from '../../utils/helper'
import { category_1_bar_options, category_1_pie_options, category_2_bar_options } from './chartOptions'
export default {
  name: 'Chart',
  mixins: [mixin],
  props: {
    chartId: {
      type: Number,
      default: 0,
    },
    data: {
      type: [Number, Object],
      default: 0,
    },
    category: {
      type: Number,
      default: 0,
    },
    options: {
      type: Object,
      default: () => {},
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chart: null,
    }
  },
  watch: {
    data: {
      immediate: true,
      deep: true,
      handler(newValue, oldValue) {
        if (this.category === 1 || this.category === 2) {
          if (Object.prototype.toString.call(newValue) === '[object Object]') {
            this.setChart()
          }
        }
      },
    },
    sidebarOpened(val) {
      setTimeout(() => {
        this.resizeChart()
      }, 200)
    },
  },
  mounted() {
    window.addEventListener('resize', this.resizeChart)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  },
  methods: {
    toThousands,
    setChart() {
      if (!this.chart) {
        this.chart = echarts.init(document.getElementById(`cmdb-dashboard-${this.chartId}-${this.editable}`))
      }
      if (this.category === 1 && this.options.chartType === 'bar') {
        this.chart.setOption(category_1_bar_options(this.data), true)
      }
      if (this.category === 1 && this.options.chartType === 'pie') {
        this.chart.setOption(category_1_pie_options(this.data), true)
      }
      if (this.category === 2) {
        this.chart.setOption(category_2_bar_options(this.data), true)
      }
    },
    resizeChart() {
      this.$nextTick(() => {
        if (this.chart) {
          this.chart.resize()
        }
      })
    },
  },
}
</script>

<style lang="less" scoped>
.cmdb-dashboard-grid-item-chart {
  width: 100%;
  height: 100%;
  position: relative;
  padding: 10px;
  > span {
    font-size: 50px;
    font-weight: 700;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}
</style>
