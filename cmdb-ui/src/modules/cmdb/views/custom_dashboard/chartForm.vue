<template>
  <a-modal
    width="1100px"
    :title="`${type === 'add' ? '新增' : '编辑'}图表`"
    :visible="visible"
    @cancel="handleclose"
    @ok="handleok"
    :bodyStyle="{ paddingTop: 0 }"
  >
    <div class="chart-wrapper">
      <div class="chart-left">
        <a-form-model ref="chartForm" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 18 }">
          <a-form-model-item label="标题" prop="name">
            <a-input v-model="form.name" placeholder="请输入图表标题"></a-input>
          </a-form-model-item>
          <a-form-model-item label="类型" prop="category" v-if="chartType !== 'count' && chartType !== 'table'">
            <a-radio-group
              @change="
                () => {
                  resetForm()
                }
              "
              :default-value="1"
              v-model="form.category"
            >
              <a-radio-button :value="Number(key)" :key="key" v-for="key in Object.keys(dashboardCategory)">
                {{ dashboardCategory[key].label }}
              </a-radio-button>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item label="类型" prop="tableCategory" v-if="chartType === 'table'">
            <a-radio-group
              @change="
                () => {
                  resetForm()
                }
              "
              :default-value="1"
              v-model="form.tableCategory"
            >
              <a-radio-button :value="1">
                计算指标
              </a-radio-button>
              <a-radio-button :value="2">
                资源数据
              </a-radio-button>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item
            v-if="(chartType !== 'table' && form.category !== 2) || (chartType === 'table' && form.tableCategory === 1)"
            label="模型"
            prop="type_ids"
          >
            <a-select
              show-search
              optionFilterProp="children"
              @change="changeCIType"
              v-model="form.type_ids"
              placeholder="请选择模型"
              mode="multiple"
            >
              <a-select-option v-for="ci_type in ci_types" :key="ci_type.id" :value="ci_type.id">{{
                ci_type.alias || ci_type.name
              }}</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item v-else label="模型" prop="type_id">
            <a-select
              show-search
              optionFilterProp="children"
              @change="changeCIType"
              v-model="form.type_id"
              placeholder="请选择模型"
            >
              <a-select-option v-for="ci_type in ci_types" :key="ci_type.id" :value="ci_type.id">{{
                ci_type.alias || ci_type.name
              }}</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item
            label="维度"
            prop="attr_ids"
            v-if="(['bar', 'line', 'pie'].includes(chartType) && form.category === 1) || chartType === 'table'"
          >
            <a-select
              :filter-option="filterOption"
              @change="changeAttr"
              v-model="form.attr_ids"
              placeholder="请选择维度"
              mode="multiple"
              show-search
            >
              <a-select-option
                v-for="attr in commonAttributes.filter((attr) => !attr.is_password)"
                :key="attr.id"
                :value="attr.id"
              >{{ attr.alias || attr.name }}</a-select-option
              >
            </a-select>
          </a-form-model-item>
          <a-form-model-item
            prop="type_ids"
            label="关系模型"
            v-if="['bar', 'line', 'pie'].includes(chartType) && form.category === 2"
          >
            <a-select
              show-search
              optionFilterProp="children"
              mode="multiple"
              v-model="form.type_ids"
              placeholder="请选择模型"
            >
              <a-select-opt-group
                v-for="(key, index) in Object.keys(level2children)"
                :key="key"
                :label="`层级${index + 1}`"
              >
                <a-select-option
                  @click="(e) => clickLevel2children(e, citype, index + 1)"
                  v-for="citype in level2children[key]"
                  :key="citype.id"
                  :value="citype.id"
                >
                  {{ citype.alias || citype.name }}
                </a-select-option>
              </a-select-opt-group>
            </a-select>
          </a-form-model-item>
          <div :class="{ 'chart-left-preview': true, 'chart-left-preview-empty': !isShowPreview }">
            <span class="chart-left-preview-operation" @click="showPreview"><a-icon type="play-circle" /> 预览</span>
            <template v-if="isShowPreview">
              <div v-if="chartType !== 'count'" class="cmdb-dashboard-grid-item-title">
                <template v-if="form.showIcon && ciType">
                  <template v-if="ciType.icon">
                    <img
                      v-if="ciType.icon.split('$$')[2]"
                      :src="`/api/common-setting/v1/file/${ciType.icon.split('$$')[3]}`"
                    />
                    <ops-icon
                      v-else
                      :style="{
                        color: ciType.icon.split('$$')[1],
                      }"
                      :type="ciType.icon.split('$$')[0]"
                    />
                  </template>
                  <span :style="{ color: '#2f54eb' }" v-else>{{ ciType.name[0].toUpperCase() }}</span>
                </template>
                <span :style="{ color: '#000' }"> {{ form.name }}</span>
              </div>
              <div
                class="chart-left-preview-box"
                :style="{
                  height: chartType === 'count' ? '120px' : '',
                  marginTop: chartType === 'count' ? '80px' : '',
                  background:
                    chartType === 'count'
                      ? Array.isArray(bgColor)
                        ? `linear-gradient(to bottom, ${bgColor[0]} 0%, ${bgColor[1]} 100%)`
                        : bgColor
                      : '#fafafa',
                }"
              >
                <div :style="{ color: fontColor }">{{ form.name }}</div>
                <Chart
                  :ref="`chart_${item.id}`"
                  :chartId="item.id"
                  :data="previewData"
                  :category="form.category"
                  :options="{
                    ...item.options,
                    name: form.name,
                    fontColor: fontColor,
                    bgColor: bgColor,
                    chartType: chartType,
                    showIcon: form.showIcon,
                    barDirection: barDirection,
                    barStack: barStack,
                    chartColor: chartColor,
                    type_ids: form.type_ids,
                    attr_ids: form.attr_ids,
                    isShadow: isShadow,
                    ret: form.tableCategory === 2 ? 'cis' : '',
                  }"
                  :editable="false"
                  :ci_types="ci_types"
                  :type_id="form.type_id || form.type_ids"
                  isPreview
                />
              </div>
            </template>
          </div>
          <a-form-model-item label="是否显示icon" prop="showIcon" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
            <a-switch v-model="form.showIcon"></a-switch>
          </a-form-model-item>
        </a-form-model>
      </div>

      <div class="chart-right">
        <h4>图表类型</h4>
        <div class="chart-right-type">
          <div
            :class="{ 'chart-right-type-box': true, 'chart-right-type-box-selected': chartType === t.value }"
            v-for="t in chartTypeList"
            :key="t.value"
            @click="changeChartType(t)"
          >
            <ops-icon :type="`cmdb-${t.value}`" />
            <span>{{ t.label }}</span>
          </div>
        </div>
        <h4>数据筛选</h4>
        <FilterComp
          ref="filterComp"
          :isDropdown="false"
          :canSearchPreferenceAttrList="attributes"
          @setExpFromFilter="setExpFromFilter"
          :expression="filterExp ? `q=${filterExp}` : ''"
        />
        <h4>格式</h4>
        <a-form-model :colon="false" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
          <a-form-model-item label="字体颜色" v-if="chartType === 'count'">
            <ColorPicker
              v-model="fontColor"
              :colorList="[
                '#1D2129',
                '#4E5969',
                '#103C93',
                '#86909C',
                '#ffffff',
                '#C9F2FF',
                '#FFEAC0',
                '#D6FFE6',
                '#F2DEFF',
              ]"
            />
          </a-form-model-item>
          <a-form-model-item label="背景颜色" v-if="chartType === 'count'">
            <ColorPicker
              v-model="bgColor"
              :colorList="[
                ['#6ABFFE', '#5375EB'],
                ['#C69EFF', '#A377F9'],
                ['#85EBC9', '#4AB8D8'],
                ['#FEB58B', '#DF6463'],
                '#ffffff',
                '#FFFBF0',
                '#FFF1EC',
                '#E5FFFE',
                '#E5E7FF',
              ]"
            />
          </a-form-model-item>
          <a-form-model-item label="图表颜色" v-else-if="chartType !== 'table'">
            <ColorListPicker v-model="chartColor" />
          </a-form-model-item>
          <a-form-model-item label="图表长度(%)">
            <a-radio-group class="chart-width" style="width:100%;" v-model="width">
              <a-radio-button :value="3">
                25
              </a-radio-button>
              <a-radio-button :value="6">
                50
              </a-radio-button>
              <a-radio-button :value="9">
                75
              </a-radio-button>
              <a-radio-button :value="12">
                100
              </a-radio-button>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item label="柱状图类型" v-if="chartType === 'bar'">
            <a-radio-group v-model="barStack">
              <a-radio value="total">
                堆积柱状图
              </a-radio>
              <a-radio value="">
                多系列柱状图
              </a-radio>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item label="方向" v-if="chartType === 'bar'">
            <a-radio-group v-model="barDirection">
              <a-radio value="x">
                X轴
              </a-radio>
              <a-radio value="y">
                y轴
              </a-radio>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item label="下方阴影" v-if="chartType === 'line'">
            <a-switch v-model="isShadow" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </div>
  </a-modal>
</template>

<script>
import Chart from './chart.vue'
import { dashboardCategory } from './constant'
import { postCustomDashboard, putCustomDashboard, postCustomDashboardPreview } from '../../api/customDashboard'
import { getCITypeAttributesByTypeIds, getCITypeCommonAttributesByTypeIds } from '../../api/CITypeAttr'
import { getRecursive_level2children } from '../../api/CITypeRelation'
import { getLastLayout } from '../../utils/helper'
import FilterComp from '@/components/CMDBFilterComp'
import ColorPicker from './colorPicker.vue'
import ColorListPicker from './colorListPicker.vue'

export default {
  name: 'ChartForm',
  components: { Chart, FilterComp, ColorPicker, ColorListPicker },
  props: {
    ci_types: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    const chartTypeList = [
      {
        value: 'count',
        label: '指标',
      },
      {
        value: 'bar',
        label: '柱状图',
      },
      {
        value: 'line',
        label: '折线图',
      },
      {
        value: 'pie',
        label: '饼状图',
      },
      {
        value: 'table',
        label: '表格',
      },
    ]
    return {
      dashboardCategory,
      chartTypeList,
      visible: false,
      attributes: [],
      type: 'add',
      form: {
        category: 0,
        tableCategory: 1,
        name: undefined,
        type_id: undefined,
        type_ids: undefined,
        attr_ids: undefined,
        level: undefined,
        showIcon: false,
      },
      rules: {
        category: [{ required: true, trigger: 'change' }],
        name: [{ required: true, message: '请输入图表名称' }],
        type_id: [{ required: true, message: '请选择模型', trigger: 'change' }],
        type_ids: [{ required: true, message: '请选择模型', trigger: 'change' }],
        attr_ids: [{ required: true, message: '请选择模型属性', trigger: 'change' }],
        level: [{ required: true, message: '请输入关系层级' }],
        showIcon: [{ required: false }],
      },
      item: {},
      chartType: 'count', // table,bar,line,pie,count
      width: 3,
      fontColor: '#ffffff',
      bgColor: ['#6ABFFE', '#5375EB'],
      chartColor: '#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF', // 图表颜色
      isShowPreview: false,
      filterExp: undefined,
      previewData: null,
      barStack: 'total',
      barDirection: 'y',
      commonAttributes: [],
      level2children: {},
      isShadow: false,
    }
  },
  computed: {
    ciType() {
      if (this.form.type_id || this.form.type_ids) {
        const _find = this.ci_types.find((item) => item.id === this.form.type_id || item.id === this.form.type_ids[0])
        return _find || null
      }
      return null
    },
  },
  inject: ['layout'],
  methods: {
    async open(type, item = {}) {
      this.visible = true
      this.type = type
      this.item = item
      const { category = 0, name, type_id, attr_id, level } = item
      const chartType = (item.options || {}).chartType || 'count'
      const fontColor = (item.options || {}).fontColor || '#ffffff'
      const bgColor = (item.options || {}).bgColor || ['#6ABFFE', '#5375EB']
      const width = (item.options || {}).w
      const showIcon = (item.options || {}).showIcon
      const type_ids = item?.options?.type_ids || []
      const attr_ids = item?.options?.attr_ids || []
      const ret = item?.options?.ret || ''
      this.width = width
      this.chartType = chartType
      this.filterExp = item?.options?.filter ?? ''
      this.chartColor = item?.options?.chartColor ?? '#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF'
      this.isShadow = item?.options?.isShadow ?? false

      if (chartType === 'count') {
        this.fontColor = fontColor
        this.bgColor = bgColor
      }
      if (type_ids && type_ids.length) {
        await getCITypeAttributesByTypeIds({ type_ids: type_ids.join(',') }).then((res) => {
          this.attributes = res.attributes
        })
        if ((['bar', 'line', 'pie'].includes(chartType) && category === 1) || chartType === 'table') {
          this.barDirection = item?.options?.barDirection ?? 'y'
          this.barStack = item?.options?.barStack ?? 'total'
          await getCITypeCommonAttributesByTypeIds({
            type_ids: type_ids.join(','),
          }).then((res) => {
            this.commonAttributes = res.attributes
          })
        }
      }
      if (type_id) {
        getRecursive_level2children(type_id).then((res) => {
          this.level2children = res
        })
        await getCITypeCommonAttributesByTypeIds({
          type_ids: type_id,
        }).then((res) => {
          this.commonAttributes = res.attributes
        })
      }
      this.$nextTick(() => {
        this.$refs.filterComp.visibleChange(true, false)
      })
      const default_form = {
        category: 0,
        name: undefined,
        type_id: undefined,
        type_ids: undefined,
        attr_ids: undefined,
        level: undefined,
        showIcon: false,
        tableCategory: 1,
      }
      this.form = {
        ...default_form,
        category,
        name,
        type_id,
        type_ids,
        attr_ids,
        level,
        showIcon,
        tableCategory: ret === 'cis' ? 2 : 1,
      }
    },
    handleclose() {
      this.attributes = []
      this.$refs.chartForm.clearValidate()
      this.isShowPreview = false
      this.visible = false
    },
    changeCIType(value) {
      this.form.attr_ids = []
      this.commonAttributes = []
      if ((Array.isArray(value) && value.length) || (!Array.isArray(value) && value)) {
        getCITypeAttributesByTypeIds({ type_ids: Array.isArray(value) ? value.join(',') : value }).then((res) => {
          this.attributes = res.attributes
        })
      }
      if (!Array.isArray(value) && value) {
        getRecursive_level2children(value).then((res) => {
          this.level2children = res
        })
      }
      if ((['bar', 'line', 'pie'].includes(this.chartType) && this.form.category === 1) || this.chartType === 'table') {
        getCITypeCommonAttributesByTypeIds({ type_ids: Array.isArray(value) ? value.join(',') : value }).then((res) => {
          this.commonAttributes = res.attributes
        })
      }
    },
    handleok() {
      this.$refs.chartForm.validate(async (valid) => {
        if (valid) {
          const name = this.form.name
          const { chartType, fontColor, bgColor } = this
          this.$refs.filterComp.handleSubmit()
          if (this.item.id) {
            const params = {
              ...this.form,
              options: {
                ...this.item.options,
                name,
                w: this.width,
                chartType: this.chartType,
                showIcon: this.form.showIcon,
                type_ids: this.form.type_ids,
                filter: this.filterExp,
                isShadow: this.isShadow,
              },
            }
            if (chartType === 'count') {
              params.options.fontColor = fontColor
              params.options.bgColor = bgColor
            }
            if (['bar', 'line', 'pie'].includes(chartType)) {
              if (this.form.category === 1) {
                params.options.attr_ids = this.form.attr_ids
              }
              params.options.chartColor = this.chartColor
            }
            if (chartType === 'bar') {
              params.options.barDirection = this.barDirection
              params.options.barStack = this.barStack
            }
            if (chartType === 'table') {
              params.options.attr_ids = this.form.attr_ids
              if (this.form.tableCategory === 2) {
                params.options.ret = 'cis'
              }
            }
            delete params.showIcon
            delete params.type_ids
            delete params.attr_ids
            delete params.tableCategory
            await putCustomDashboard(this.item.id, params)
            this.$emit('refresh', this.item.id)
          } else {
            const { xLast, yLast, wLast } = getLastLayout(this.layout())
            const w = this.width
            const x = xLast + wLast + w > 12 ? 0 : xLast + wLast
            const y = xLast + wLast + w > 12 ? yLast + 1 : yLast
            const params = {
              ...this.form,
              options: {
                x,
                y,
                w,
                h: this.form.category === 0 ? 3 : 5,
                name,
                chartType: this.chartType,
                showIcon: this.form.showIcon,
                type_ids: this.form.type_ids,
                filter: this.filterExp,
                isShadow: this.isShadow,
              },
            }
            if (chartType === 'count') {
              params.options.fontColor = fontColor
              params.options.bgColor = bgColor
            }
            if (['bar', 'line', 'pie'].includes(chartType)) {
              if (this.form.category === 1) {
                params.options.attr_ids = this.form.attr_ids
              }
              params.options.chartColor = this.chartColor
            }
            if (chartType === 'bar') {
              params.options.barDirection = this.barDirection
              params.options.barStack = this.barStack
            }
            if (chartType === 'table') {
              params.options.attr_ids = this.form.attr_ids
              if (this.form.tableCategory === 2) {
                params.options.ret = 'cis'
              }
            }
            delete params.showIcon
            delete params.type_ids
            delete params.attr_ids
            delete params.tableCategory
            await postCustomDashboard(params)
          }
          this.handleclose()
          this.$emit('refresh')
        }
      })
    },
    // changeDashboardCategory(value) {
    //   this.$refs.chartForm.clearValidate()
    //   if (value === 1 && this.form.type_id) {
    //     this.changeCIType(this.form.type_id)
    //   }
    // },
    changeChartType(t) {
      if (!(['bar', 'line', 'pie'].includes(this.chartType) && ['bar', 'line', 'pie'].includes(t.value))) {
        this.resetForm()
      }
      this.chartType = t.value
      this.isShowPreview = false
      if (t.value === 'count') {
        this.form.category = 0
      } else {
        this.form.category = 1
      }
    },
    showPreview() {
      this.$refs.chartForm.validate(async (valid) => {
        if (valid) {
          this.isShowPreview = false
          const name = this.form.name
          const { chartType, fontColor, bgColor } = this
          this.$refs.filterComp.handleSubmit()
          const params = {
            ...this.form,
            options: {
              name,
              chartType,
              showIcon: this.form.showIcon,
              type_ids: this.form.type_ids,
              filter: this.filterExp,
              isShadow: this.isShadow,
            },
          }
          if (chartType === 'count') {
            params.options.fontColor = fontColor
            params.options.bgColor = bgColor
          }
          if (['bar', 'line', 'pie'].includes(chartType)) {
            if (this.form.category === 1) {
              params.options.attr_ids = this.form.attr_ids
            }
            params.options.chartColor = this.chartColor
          }
          if (chartType === 'bar') {
            params.options.barDirection = this.barDirection
            params.options.barStack = this.barStack
          }
          if (chartType === 'table') {
            params.options.attr_ids = this.form.attr_ids
            if (this.form.tableCategory === 2) {
              params.options.ret = 'cis'
            }
          }
          delete params.showIcon
          delete params.type_ids
          delete params.attr_ids
          delete params.tableCategory
          postCustomDashboardPreview(params).then((res) => {
            this.isShowPreview = true
            this.previewData = res.counter
          })
        }
      })
    },
    setExpFromFilter(filterExp) {
      if (filterExp) {
        this.filterExp = `${filterExp}`
      } else {
        this.filterExp = undefined
      }
    },
    resetForm() {
      this.form.type_id = undefined
      this.form.type_ids = []
      this.form.attr_ids = []
      this.$refs.chartForm.clearValidate()
    },
    changeAttr(value) {
      if (value && value.length) {
        if (['line', 'pie'].includes(this.chartType)) {
          this.form.attr_ids = [value[value.length - 1]]
        }
        if (['bar'].includes(this.chartType) && value.length > 2) {
          this.form.attr_ids = value.slice(value.length - 2, value.length)
        }
        if (['table'].includes(this.chartType) && value.length > 3) {
          this.form.attr_ids = value.slice(value.length - 3, value.length)
        }
      }
    },
    clickLevel2children(e, citype, level) {
      if (this.form.level !== level) {
        this.$nextTick(() => {
          this.form.type_ids = [citype.id]
        })
      }
      this.form.level = level
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
  },
}
</script>

<style lang="less" scoped>
.chart-wrapper {
  display: flex;
  .chart-left {
    width: 50%;
    .chart-left-preview {
      border: 1px solid #e4e7ed;
      border-radius: 2px;
      height: 280px;
      width: 92%;
      position: relative;
      padding: 12px;
      .chart-left-preview-operation {
        color: #86909c;
        position: absolute;
        top: 12px;
        right: 12px;
        cursor: pointer;
      }
      .chart-left-preview-box {
        padding: 6px 12px;
        height: 250px;
        border-radius: 8px;
      }
    }
    .chart-left-preview-empty {
      background: url('../../assets/dashboard_empty.png');
      background-size: contain;
      background-repeat: no-repeat;
      background-position-x: center;
      background-position-y: center;
    }
  }
  .chart-right {
    width: 50%;
    h4 {
      font-weight: 700;
      color: #000;
    }
    .chart-right-type {
      display: flex;
      justify-content: space-between;
      background-color: #f0f5ff;
      padding: 6px 12px;
      .chart-right-type-box {
        cursor: pointer;
        width: 70px;
        height: 60px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        > i {
          font-size: 32px;
        }
        > span {
          font-size: 12px;
        }
      }
      .chart-right-type-box-selected {
        background-color: #e5f1ff;
      }
    }
    .chart-width {
      width: 100%;
      > label {
        width: 25%;
        text-align: center;
      }
    }
  }
}
</style>
<style lang="less">
.chart-wrapper {
  .ant-form-item {
    margin-bottom: 0;
  }
}
</style>
