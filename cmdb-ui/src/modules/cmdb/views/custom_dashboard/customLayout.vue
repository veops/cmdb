<template>
  <div
    :style="{
      height: `${windowHeight - 40}px`,
      overflowY: 'auto',
      overflowX: 'hidden',
      position: 'relative',
      margin: '-24px',
    }"
  >
    <template v-if="layout && layout.length">
      <div v-if="editable">
        <a-button
          :style="{ marginLeft: '22px', marginTop: '20px', backgroundColor: '#D6E9FF', boxShadow: 'none' }"
          @click="openChartForm('add', { options: { w: 3 } })"
          type="primary"
          icon="plus-circle"
          class="ops-button-primary"
        >{{ $t('cmdb.custom_dashboard.newChart') }}</a-button
        >
      </div>
      <GridLayout
        :layout.sync="layout"
        :col-num="12"
        :row-height="30"
        :is-draggable="editable"
        :is-resizable="editable"
        :is-mirrored="false"
        :margin="[22, 22]"
        @layout-updated="layoutUpdatedEvent"
      >
        <GridItem
          class="cmdb-dashboard-grid-item"
          v-for="item in layout"
          :x="item.x"
          :y="item.y"
          :w="item.w"
          :h="item.h"
          :i="item.i"
          :key="item.i"
          :style="{
            background:
              item.options.chartType === 'count'
                ? Array.isArray(item.options.bgColor)
                  ? `linear-gradient(to bottom, ${item.options.bgColor[0]} 0%, ${item.options.bgColor[1]} 100%)`
                  : item.options.bgColor
                : '#fafafa',
          }"
        >
          <div class="cmdb-dashboard-grid-item-title">
            <template v-if="item.options.chartType !== 'count' && item.options.showIcon && getCiType(item)">
              <template v-if="getCiType(item).icon">
                <img
                  v-if="getCiType(item).icon.split('$$')[2]"
                  :src="`/api/common-setting/v1/file/${getCiType(item).icon.split('$$')[3]}`"
                />
                <ops-icon
                  v-else
                  :style="{
                    color: getCiType(item).icon.split('$$')[1],
                  }"
                  :type="getCiType(item).icon.split('$$')[0]"
                />
              </template>
              <span :style="{ color: '#2f54eb' }" v-else>{{ getCiType(item).name[0].toUpperCase() }}</span>
            </template>
            <span :style="{ color: item.options.chartType === 'count' ? item.options.fontColor : '#000' }">{{
              item.options.name
            }}</span>
          </div>
          <a-dropdown v-if="editable">
            <a
              class="cmdb-dashboard-grid-item-operation"
              :style="{
                color: item.options.chartType === 'count' ? item.options.fontColor : '',
              }"
            ><a-icon type="menu"></a-icon
            ></a>
            <a-menu slot="overlay">
              <a-menu-item>
                <a @click="() => openChartForm('edit', item)"><a-icon style="margin-right:5px" type="edit" />{{ $t('edit') }}</a>
              </a-menu-item>
              <a-menu-item>
                <a @click="deleteChart(item)"><a-icon style="margin-right:5px" type="delete" />{{ $t('delete') }}</a>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
          <!-- <a
            v-if="editable && item.category === 1"
            class="cmdb-dashboard-grid-item-chart-type"
            @click="changeChartType(item)"
          ><a-icon
            :type="item.options.chartType === 'bar' ? 'bar-chart' : 'pie-chart'"
          /></a> -->
          <Chart
            :ref="`chart_${item.id}`"
            :chartId="item.id"
            :data="totalData[item.id]"
            :category="item.category"
            :options="item.options"
            :editable="editable"
            :ci_types="ci_types"
            :type_id="item.type_id"
          />
        </GridItem>
      </GridLayout>
    </template>
    <div v-else class="dashboard-empty">
      <a-empty :image="emptyImage" description=""></a-empty>
      <a-button
        @click="openChartForm('add', { options: { w: 3 } })"
        v-if="editable"
        size="small"
        type="primary"
        icon="plus"
      >
        定制仪表盘
      </a-button>
      <span v-else>{{ $t('cmdb.custom_dashboard.noCustomDashboard') }}</span>
    </div>
    <ChartForm ref="chartForm" @refresh="refresh" :ci_types="ci_types" :totalData="totalData" />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import VueGridLayout from 'vue-grid-layout'
import ChartForm from './chartForm.vue'
import Chart from './chart.vue'
import {
  getCustomDashboard,
  deleteCustomDashboard,
  putCustomDashboard,
  batchUpdateCustomDashboard,
} from '../../api/customDashboard.js'
import { getCITypes } from '../../api/CIType'
import emptyImage from '@/assets/data_empty.png'
import { getStatistics } from '../../api/statistics'

export default {
  name: 'CustomLayout',
  components: { ChartForm, Chart, GridLayout: VueGridLayout.GridLayout, GridItem: VueGridLayout.GridItem },
  props: {
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      emptyImage,
      layout: [],
      ci_types: [],
      totalData: {},
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  provide() {
    return {
      layout: () => {
        return this.layout
      },
    }
  },
  created() {
    getCITypes().then((res) => {
      this.ci_types = res.ci_types
    })
  },
  mounted() {
    this.getLayout()
  },
  methods: {
    async getLayout() {
      const res = await getCustomDashboard()
      this.layout = res.map((item) => {
        return {
          ...item,
          i: item.id,
          x: (item.options || {}).x || 0,
          y: (item.options || {}).y || 0,
          w: (item.options || {}).w || 4,
          h: (item.options || {}).h || 5,
        }
      })
      if (this.layout && this.layout.length) {
        getStatistics().then((res1) => {
          this.totalData = res1
        })
      }
    },
    openChartForm(type = 'add', item = {}) {
      console.log(type, item)
      this.$refs.chartForm.open(type, item)
    },
    refresh(id) {
      if (id) {
        setTimeout(() => {
          this.$refs[`chart_${id}`][0].resizeChart()
        }, 100)
      } else {
        this.getLayout()
      }
    },
    deleteChart(item) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认删除？',
        onOk() {
          deleteCustomDashboard(item.id).then(() => {
            that.getLayout()
          })
        },
      })
    },
    changeChartType(item) {
      putCustomDashboard(item.id, {
        options: { ...item.options, chartType: item.options.chartType === 'bar' ? 'pie' : 'bar' },
      }).then(async () => {
        await this.getLayout()
      })
    },
    layoutUpdatedEvent(newLayout) {
      const id2options = {}
      newLayout.forEach((item) => {
        const oldOptions = _.cloneDeep(item.options)
        const newOptions = { ..._.cloneDeep(item.options), x: item.x, y: item.y, w: item.w, h: item.h }
        if (!_.isEqual(oldOptions, newOptions)) {
          id2options[item.id] = newOptions
        }
      })
      if (JSON.stringify(id2options) !== '{}') {
        batchUpdateCustomDashboard({ id2options }).then(async () => {
          await this.getLayout()
          Object.keys(id2options).forEach((key) => {
            this.$refs[`chart_${key}`][0].resizeChart()
          })
        })
      }
    },
    getCiType(item) {
      if (item.type_id || item.options?.type_ids) {
        const _find = this.ci_types.find((type) => type.id === item.type_id || type.id === item.options?.type_ids[0])
        return _find || null
      }
      return null
    },
  },
}
</script>

<style lang="less" scoped>
.dashboard-empty {
  margin-top: 200px;
  text-align: center;
}
.cmdb-dashboard-grid-item {
  border-radius: 8px;
  padding: 6px 12px;
  .cmdb-dashboard-grid-item-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 700;
    color: #000000;
  }
  .cmdb-dashboard-grid-item-operation {
    position: absolute;
    right: 12px;
    top: 6px;
  }
  .cmdb-dashboard-grid-item-chart-type {
    position: absolute;
    top: 6px;
    right: 24px;
  }
}
</style>

<style lang="less">
.cmdb-dashboard-grid-item-title {
  display: flex;
  align-items: center;
  > i {
    font-size: 16px;
    margin-right: 5px;
  }
  > img {
    width: 16px;
    margin-right: 5px;
  }
  > span:not(:last-child) {
    display: inline-block;
    width: 16px;
    height: 16px;
    font-size: 16px;
    text-align: center;
    margin-right: 5px;
  }
}
.ops-button-primary:hover {
  background-color: #2f54eb !important;
}
</style>
