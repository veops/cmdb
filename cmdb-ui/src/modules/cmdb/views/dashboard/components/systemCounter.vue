<template>
  <div id="system-counter" :style="{ height: '300px' }"></div>
</template>

<script>
import _ from 'lodash'
import * as echarts from 'echarts'
export default {
  name: 'SystemCounter',
  inject: ['statistics'],
  data() {
    return {
      chart: null,
    }
  },
  computed: {
    system_counter() {
      return this.statistics().system_counter
    },
  },
  watch: {
    system_counter: {
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
      if (!this.chart) {
        this.chart = echarts.init(document.getElementById('system-counter'))
      }
      const sum = _.sum(Object.values(this.system_counter))
      this.chart.setOption({
        grid: {
          left: 0,
          right: 0,
          top: 50,
          bottom: 0,
          containLabel: true,
        },
        tooltip: {
          trigger: 'item',
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: '80%',
            data: Object.keys(this.system_counter).map((item) => {
              return {
                value: this.system_counter[item],
                name: item,
                label: {
                  position: this.system_counter[item] / sum < 0.2 ? 'outside' : 'inside',
                  formatter: '{b}: {c}'
                },
              }
            }),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      })
    },
  },
}
</script>

<style></style>
