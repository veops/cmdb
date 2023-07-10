<template>
  <a-modal :title="`${type === 'add' ? '新增' : '编辑'}图表`" :visible="visible" @cancel="handleclose" @ok="handleok">
    <a-form-model ref="chartForm" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <a-form-model-item label="类型" prop="category">
        <a-select v-model="form.category" @change="changeDashboardCategory">
          <a-select-option v-for="cate in Object.keys(dashboardCategory)" :key="cate" :value="Number(cate)">{{
            dashboardCategory[cate].label
          }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item v-if="form.category !== 0" label="名称" prop="name">
        <a-input v-model="form.name" placeholder="请输入图表名称"></a-input>
      </a-form-model-item>
      <a-form-model-item label="模型" prop="type_id">
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
      <a-form-model-item v-if="form.category === 1" label="模型属性" prop="attr_id">
        <a-select show-search optionFilterProp="children" v-model="form.attr_id" placeholder="请选择模型属性">
          <a-select-option v-for="attr in attributes" :key="attr.id" :value="attr.id">{{
            attr.alias || attr.name
          }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item v-if="form.category === 1" label="图表类型" prop="chartType">
        <a-radio-group v-model="chartType">
          <a-radio value="bar">
            柱状图
          </a-radio>
          <a-radio value="pie">
            饼图
          </a-radio>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item v-if="form.category === 2" label="关系层级" prop="level">
        <a-input v-model="form.level" placeholder="请输入关系层级"></a-input>
      </a-form-model-item>
      <a-form-model-item v-if="form.category === 0" label="字体">
        <FontConfig ref="fontConfig" />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { dashboardCategory } from './constant'
import { postCustomDashboard, putCustomDashboard } from '../../api/customDashboard'
import { getCITypeAttributesById } from '../../api/CITypeAttr'
import { getLastLayout } from '../../utils/helper'
import FontConfig from './fontConfig.vue'
export default {
  name: 'ChartForm',
  components: { FontConfig },
  props: {
    ci_types: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      dashboardCategory,
      visible: false,
      attributes: [],
      type: 'add',
      form: {
        category: 0,
        name: undefined,
        type_id: undefined,
        attr_id: undefined,
        level: undefined,
      },
      rules: {
        category: [{ required: true, trigger: 'change' }],
        name: [{ required: true, message: '请输入图表名称' }],
        type_id: [{ required: true, message: '请选择模型', trigger: 'change' }],
        attr_id: [{ required: true, message: '请选择模型属性', trigger: 'change' }],
        level: [{ required: true, message: '请输入关系层级' }],
      },
      item: {},
      chartType: 'bar',
    }
  },
  inject: ['layout'],
  methods: {
    open(type, item = {}) {
      this.visible = true
      this.type = type
      this.item = item
      const { category = 0, name, type_id, attr_id, level } = item
      const chartType = (item.options || {}).chartType || 'bar'
      this.chartType = chartType
      if (type_id && attr_id) {
        getCITypeAttributesById(type_id).then((res) => {
          this.attributes = res.attributes
        })
      }
      const default_form = {
        category: 0,
        name: undefined,
        type_id: undefined,
        attr_id: undefined,
        level: undefined,
      }
      this.form = {
        ...default_form,
        category,
        name,
        type_id,
        attr_id,
        level,
      }
      if (category === 0) {
        this.$nextTick(() => {
          this.$refs.fontConfig.setConfig((item.options || {}).fontConfig)
        })
      }
    },
    handleclose() {
      this.attributes = []
      this.$refs.chartForm.clearValidate()
      this.visible = false
    },
    changeCIType(value) {
      getCITypeAttributesById(value).then((res) => {
        this.attributes = res.attributes
        this.form = {
          ...this.form,
          attr_id: undefined,
        }
      })
    },
    handleok() {
      this.$refs.chartForm.validate(async (valid) => {
        if (valid) {
          const fontConfig = this.form.category === 0 ? this.$refs.fontConfig.getConfig() : undefined
          const _find = this.ci_types.find((attr) => attr.id === this.form.type_id)
          const name = this.form.name || (_find || {}).alias || (_find || {}).name
          if (this.item.id) {
            await putCustomDashboard(this.item.id, {
              ...this.form,
              options: {
                ...this.item.options,
                name,
                fontConfig,
                chartType: this.chartType,
              },
            })
          } else {
            const { xLast, yLast, wLast } = getLastLayout(this.layout())
            const w = 3
            const x = xLast + wLast + w > 12 ? 0 : xLast + wLast
            const y = xLast + wLast + w > 12 ? yLast + 1 : yLast
            await postCustomDashboard({
              ...this.form,
              options: {
                x,
                y,
                w,
                h: this.form.category === 0 ? 3 : 5,
                name,
                chartType: this.chartType,
                fontConfig,
              },
            })
          }
          this.handleclose()
          this.$emit('refresh')
        }
      })
    },
    changeDashboardCategory(value) {
      this.$refs.chartForm.clearValidate()
      if (value === 1 && this.form.type_id) {
        this.changeCIType(this.form.type_id)
      }
    },
  },
}
</script>

<style></style>
