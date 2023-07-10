<template>
  <a-row>
    <a-col :span="14">
      <div id="summary-counter-left" :style="{ height: '300px' }"></div>
    </a-col>
    <a-col :span="10">
      <div id="summary-counter-right" :style="{ height: '300px' }"></div>
    </a-col>
  </a-row>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'SummaryCounter',
  inject: ['statistics'],
  data() {
    return {
      chart1: null,
      chart2: null,
    }
  },
  computed: {
    summary_counter() {
      return this.statistics().summary_counter
    },
  },
  watch: {
    summary_counter: {
      immediate: true,
      deep: true,
      handler(newValue) {
        if (newValue && newValue.length) {
          this.setChart()
        }
      },
    },
  },
  mounted() {},
  methods: {
    setChart() {
      if (!this.chart1) {
        this.chart1 = echarts.init(document.getElementById('summary-counter-left'))
      }
      if (!this.chart2) {
        this.chart2 = echarts.init(document.getElementById('summary-counter-right'))
      }
      this.chart1.setOption({
        color: '#3ba1ff',
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
        xAxis: {
          type: 'category',
          data: this.summary_counter.map((item) => item[0]),
          axisLabel: {
            fontSize: 10,
          },
        },
        yAxis: {
          type: 'value',
          axisLine: {
            show: false,
          },
        },
        series: [
          {
            data: this.summary_counter.map((item) => item[1]),
            type: 'bar',
          },
        ],
      })
      this.chart2.setOption({
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
            type: 'funnel',
            width: '80%',
            height: '90%',
            left: '20%',
            top: '10%',
            sort: 'ascending',
            label: {
              position: 'left',
            },
            data: this.summary_counter
              .filter((item) => item[1])
              .map((item) => {
                return { value: item[1], name: item[0] }
              }),
          },
        ],
      })
    },
  },
}
</script>

<style></style>
