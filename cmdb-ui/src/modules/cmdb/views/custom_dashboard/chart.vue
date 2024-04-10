<template>
  <div
    :id="`cmdb-dashboard-${chartId}-${editable}-${isPreview}`"
    :style="{ width: '100%', height: 'calc(100% - 2.2vw)' }"
  >
    <div
      v-if="options.chartType === 'count'"
      :style="{ color: options.fontColor || '#fff' }"
      class="cmdb-dashboard-grid-item-chart"
    >
      <div class="cmdb-dashboard-grid-item-chart-icon" v-if="options.showIcon && ciType">
        <template v-if="ciType.icon">
          <img v-if="ciType.icon.split('$$')[2]" :src="`/api/common-setting/v1/file/${ciType.icon.split('$$')[3]}`" />
          <ops-icon
            v-else
            :style="{
              color: ciType.icon.split('$$')[1],
            }"
            :type="ciType.icon.split('$$')[0]"
          />
        </template>
        <span :style="{ color: '#2f54eb' }" v-else>{{ ciType.name[0].toUpperCase() }}</span>
      </div>
      <span :style="{ ...options.fontConfig }">{{ toThousands(data) }}</span>
    </div>
    <vxe-table
      :max-height="tableHeight"
      :data="tableData"
      :stripe="!!options.ret"
      size="mini"
      class="ops-stripe-table"
      v-if="options.chartType === 'table'"
      :span-method="mergeRowMethod"
      :border="!options.ret"
      show-overflow
      show-header-overflow
    >
      <template v-if="options.ret">
        <vxe-column v-for="col in columns" :key="col" :title="col" :field="col">
          <template #default="{ row }">
            <span>{{ row[col] }}</span>
          </template>
        </vxe-column>
      </template>
      <template v-else>
        <vxe-column
          v-for="(key, index) in Array(keyLength)"
          :key="`key${index}`"
          :title="columnName[index]"
          :field="`key${index}`"
        >
          <template #default="{ row }">
            <span>{{ row[`key${index}`] }}</span>
          </template>
        </vxe-column>
        <vxe-column field="value" :title="$t('cmdb.custom_dashboard.quantity')"></vxe-column>
      </template>
    </vxe-table>
    <div
      :id="`cmdb-dashboard-${chartId}-${editable}`"
      v-else-if="category === 1 || category === 2"
      class="cmdb-dashboard-grid-item-chart"
    ></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mixin } from '@/utils/mixin'
import { toThousands } from '../../utils/helper'
import {
  category_1_bar_options,
  category_1_line_options,
  category_1_pie_options,
  category_2_bar_options,
  category_2_pie_options,
} from './chartOptions'
import { getCITypeAttributesByTypeIds } from '../../api/CITypeAttr'

export default {
  name: 'Chart',
  mixins: [mixin],
  props: {
    ci_types: {
      type: Array,
      default: () => [],
    },
    chartId: {
      type: Number,
      default: 0,
    },
    data: {
      type: [Number, Object, Array],
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
    type_id: {
      type: [Number, Array],
      default: null,
    },
    isPreview: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      chart: null,
      columns: [],
      tableHeight: '',
      tableData: [],
      keyLength: 0,
      attributes: [],
      columnName: [],
    }
  },
  computed: {
    ciType() {
      if (this.type_id || this.options?.type_ids) {
        const _find = this.ci_types.find((item) => item.id === this.type_id || item.id === this.options?.type_ids[0])
        return _find || null
      }
      return null
    },
  },
  watch: {
    data: {
      immediate: true,
      deep: true,
      handler(newValue, oldValue) {
        if (this.category === 1 || this.category === 2) {
          if (this.options.chartType !== 'table' && Object.prototype.toString.call(newValue) === '[object Object]') {
            if (this.isPreview) {
              this.$nextTick(() => {
                this.setChart()
              })
            } else {
              this.setChart()
            }
          }
        }
        if (this.options.chartType === 'table') {
          this.$nextTick(() => {
            const dom = document.getElementById(`cmdb-dashboard-${this.chartId}-${this.editable}-${this.isPreview}`)
            this.tableHeight = dom.offsetHeight
          })
          if (this.options.ret) {
            const excludeKeys = ['_X_ROW_KEY', 'ci_type', 'ci_type_alias', 'unique', 'unique_alias', '_id', '_type']
            if (newValue && newValue.length) {
              this.columns = Object.keys(newValue[0]).filter((keys) => !excludeKeys.includes(keys))
              this.tableData = newValue
            }
          } else {
            getCITypeAttributesByTypeIds({ type_ids: this.options?.type_ids.join(',') }).then((res) => {
              this.attributes = res.attributes
              const _data = []
              this.keyLength = this.options?.attr_ids?.length ?? 0
              const _columnName = []
              this.options.attr_ids.forEach((attr) => {
                const _find = this.attributes.find((item) => item.id === attr)
                _columnName.push(_find?.alias || _find?.name)
              })
              this.columnName = _columnName
              this.formatTableData(_data, this.data, {})
              this.tableData = _data
            })
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
        this.chart.setOption(category_1_bar_options(this.data, this.options), true)
      }
      if (this.category === 1 && this.options.chartType === 'line') {
        this.chart.setOption(category_1_line_options(this.data, this.options), true)
      }
      if (this.category === 1 && this.options.chartType === 'pie') {
        this.chart.setOption(category_1_pie_options(this.data, this.options), true)
      }
      if (this.category === 2 && ['bar', 'line'].includes(this.options.chartType)) {
        this.chart.setOption(category_2_bar_options(this.data, this.options, this.options.chartType), true)
      }
      if (this.category === 2 && this.options.chartType === 'pie') {
        this.chart.setOption(category_2_pie_options(this.data, this.options), true)
      }
    },
    resizeChart() {
      this.$nextTick(() => {
        if (this.chart) {
          this.chart.resize()
        }
      })
    },
    formatTableData(_data, data, obj) {
      Object.keys(data).forEach((k) => {
        if (typeof data[k] === 'number') {
          _data.push({ ...obj, [`key${Object.keys(obj).length}`]: k, value: data[k] })
        } else {
          this.formatTableData(_data, data[k], { ...obj, [`key${Object.keys(obj).length}`]: k })
        }
      })
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['key0', 'key1', 'key2']
      const cellValue = row[column.field]
      if (cellValue && fields.includes(column.field)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow[column.field] === cellValue) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow[column.field] === cellValue) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },
  },
}
</script>

<style lang="less" scoped>
.cmdb-dashboard-grid-item-chart {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  > span {
    font-size: 50px;
    font-weight: 700;
  }
  .cmdb-dashboard-grid-item-chart-icon {
    > i {
      font-size: 40px;
    }
    > img {
      width: 40px;
    }
    > span {
      display: inline-block;
      width: 40px;
      height: 40px;
      font-size: 50px;
      text-align: center;
      line-height: 50px;
    }
  }
}
</style>
