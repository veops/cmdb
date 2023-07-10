<template>
  <div>
    <div id="business-counter" :style="{ height: `${domHeight}px` }"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'BusinessCounter',
  inject: ['statistics'],
  data() {
    return {
      chart: null,
      dimension: 0,
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    domHeight() {
      return this.windowHeight - 570 > 300 ? this.windowHeight - 570 : 300
    },
    business_counter() {
      return this.statistics().business_counter
    },
  },
  watch: {
    business_counter: {
      immediate: true,
      deep: true,
      handler(newValue) {
        if (newValue && JSON.stringify(newValue) !== '{}') {
          this.setChart()
        }
      },
    },
  },
  methods: {
    setChart() {
      const that = this
      if (!this.chart) {
        this.chart = echarts.init(document.getElementById('business-counter'))
        this.chart.on('updateAxisPointer', function(event) {
          const xAxisInfo = event.axesInfo[0]
          if (xAxisInfo) {
            const dimension = xAxisInfo.value + 1
            that.dimension = xAxisInfo.value
            that.chart.setOption({
              title: {
                subtext: `${business[that.dimension]}`,
              },
              series: {
                id: 'pie',
                label: {
                  formatter: '{b}: {@[' + dimension + ']} ({d}%)',
                },
                encode: {
                  value: dimension,
                  tooltip: dimension,
                },
              },
            })
          }
        })
      }
      const business = Object.keys(this.business_counter.detail)
      let _resourceName = []
      business.forEach((bu) => {
        _resourceName = [..._resourceName, ...Object.keys(this.business_counter.detail[bu])]
      })
      const resourceName = [...new Set(_resourceName)]
      const source = [['resource', ...business]]
      resourceName.forEach((r) => {
        const list = [r]
        business.forEach((bu) => {
          list.push(this.business_counter.detail[bu][r] || 0)
        })
        source.push(list)
      })
      this.chart.setOption({
        title: {
          subtext: `${business[that.dimension]}`,
          left: '8%',
        },
        legend: {
          type: 'scroll',
          left: 'center',
          bottom: 0,
        },
        tooltip: {
          trigger: 'axis',
          showContent: false,
        },
        dataset: {
          source: source,
        },
        xAxis: { type: 'category' },
        yAxis: { gridIndex: 0 },
        grid: { top: '10%', left: '30%', right: 0, bottom: '15%' },
        series: [
          ...resourceName.map((item) => {
            return {
              type: 'line',
              smooth: true,
              seriesLayoutBy: 'row',
              emphasis: { focus: 'series' },
            }
          }),
          {
            type: 'pie',
            id: 'pie',
            radius: '50%',
            center: ['10%', '50%'],
            emphasis: {
              focus: 'self',
            },
            label: {
              formatter: `{b}: {@${business[that.dimension]}} ({d}%)`,
            },
            encode: {
              itemName: 'resource',
              value: business[that.dimension],
              tooltip: business[that.dimension],
            },
          },
        ],
      })
    },
  },
}
</script>

<style></style>
