<template>
  <a-tabs id="preValueArea" v-model="activeKey" size="small" :tabBarStyle="{ borderBottom: 'none' }">
    <a-tab-pane key="define" :disabled="disabled">
      <span style="font-size:12px;" slot="tab">定义</span>
      <PreValueTag type="add" :item="[]" @add="addNewValue" :disabled="disabled">
        <template #default>
          <a-button
            :style="{ marginBottom: '10px', fontSize: '12px', padding: '1px 7px' }"
            type="primary"
            ghost
            :disabled="disabled"
            size="small"
          >
            <a-icon type="plus" />添加</a-button
          >
        </template>
      </PreValueTag>
      <draggable :list="valueList" handle=".handle" :disabled="disabled">
        <PreValueTag
          :disabled="disabled"
          v-for="(item, index) in valueList"
          :key="`${item[0]}_${index}`"
          :item="item"
          @deleteValue="deleteValue"
          @editValue="editValue"
        />
      </draggable>
    </a-tab-pane>
    <a-tab-pane key="webhook" :disabled="disabled">
      <span style="font-size:12px;" slot="tab">Webhook</span>
      <Webhook ref="webhook" style="margin-top:10px" />
      <a-form-model :model="form">
        <a-col :span="24">
          <a-form-model-item prop="ret_key" :labelCol="{ span: 3 }" :wrapperCol="{ span: 18 }">
            <template slot="label">
              <span
                style="position:relative;white-space:pre;"
              >{{ `过滤` }}
                <a-tooltip
                  title="返回的结果按字段来过滤，层级嵌套用##分隔，比如k1##k2，web请求返回{k1: [{k2: 1}, {k2: 2}]}, 解析结果为[1, 2]"
                >
                  <a-icon
                    style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                    type="question-circle"
                    theme="filled"
                  />
                </a-tooltip>
              </span>
            </template>
            <a-input style="width:150px;" v-model="form.ret_key" placeholder="k1##k2" :disabled="disabled" />
          </a-form-model-item>
        </a-col>
      </a-form-model>
    </a-tab-pane>
    <a-tab-pane key="choice_other" :disabled="disabled">
      <span style="font-size:12px;" slot="tab">其他模型属性</span>
      <a-row :gutter="[24, 24]">
        <a-col :span="12">
          <a-form-item
            :style="{ lineHeight: '24px', marginBottom: '5px' }"
            label="模型"
            :label-col="{ span: 4 }"
            :wrapper-col="{ span: 20 }"
          >
            <treeselect
              :disable-branch-nodes="true"
              :class="{
                'custom-treeselect': true,
                'custom-treeselect-bgcAndBorder': true,
              }"
              :style="{
                '--custom-height': '32px',
                lineHeight: '32px',
                '--custom-bg-color': '#fff',
                '--custom-border': '1px solid #d9d9d9',
                '--custom-multiple-lineHeight': '14px',
              }"
              v-model="choice_other.type_ids"
              :multiple="true"
              :clearable="true"
              searchable
              :options="ciTypeGroup"
              value-consists-of="LEAF_PRIORITY"
              placeholder="请选择CMDB模型"
              :normalizer="
                (node) => {
                  return {
                    id: node.id || -1,
                    label: node.alias || node.name || '其他',
                    title: node.alias || node.name || '其他',
                    children: node.ci_types,
                  }
                }
              "
              appendToBody
              :zIndex="1050"
              @select="
                () => {
                  choice_other.attr_id = undefined
                }
              "
            >
              <div
                :title="node.label"
                slot="option-label"
                slot-scope="{ node }"
                :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
              >
                {{ node.label }}
              </div>
            </treeselect>
          </a-form-item>
        </a-col>
        <a-col :span="12" v-if="choice_other.type_ids && choice_other.type_ids.length">
          <a-form-item
            :style="{ marginBottom: '5px' }"
            label="属性"
            :label-col="{ span: 4 }"
            :wrapper-col="{ span: 20 }"
          >
            <treeselect
              :disable-branch-nodes="true"
              class="ops-setting-treeselect"
              v-model="choice_other.attr_id"
              :multiple="false"
              :clearable="true"
              searchable
              :options="typeAttrs"
              value-consists-of="LEAF_PRIORITY"
              placeholder="请选择模型属性"
              :normalizer="
                (node) => {
                  return {
                    id: node.id || -1,
                    label: node.alias || node.name || '其他',
                    title: node.alias || node.name || '其他',
                  }
                }
              "
              appendToBody
              :zIndex="1050"
            >
              <div
                :title="node.label"
                slot="option-label"
                slot-scope="{ node }"
                :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
              >
                {{ node.label }}
              </div>
            </treeselect>
          </a-form-item>
        </a-col>
        <a-col :span="24" v-if="choice_other.type_ids && choice_other.type_ids.length">
          <a-form-item
            :style="{ marginBottom: '5px' }"
            class="pre-value-filter"
            label="筛选"
            :label-col="{ span: 2 }"
            :wrapper-col="{ span: 22 }"
          >
            <FilterComp
              ref="filterComp"
              :isDropdown="false"
              :canSearchPreferenceAttrList="typeAttrs"
              @setExpFromFilter="setExpFromFilter"
              :expression="filterExp ? `q=${filterExp}` : ''"
            />
          </a-form-item>
        </a-col>
      </a-row>
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import PreValueTag from './preValueTag.vue'
import { defautValueColor } from '../../utils/const'
import ColorPicker from '../../components/colorPicker/index.vue'
import Webhook from '../../components/webhook'
import { getCITypeGroups } from '../../api/ciTypeGroup'
import { getCITypeCommonAttributesByTypeIds } from '../../api/CITypeAttr'
import FilterComp from '@/components/CMDBFilterComp'

export default {
  name: 'PreValueArea',
  components: { draggable, PreValueTag, ColorPicker, Webhook, FilterComp },
  props: {
    disabled: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      defautValueColor,
      activeKey: 'define', // define webhook
      valueList: [],
      form: {
        ret_key: '',
      },
      choice_other: {
        type_ids: undefined,
        attr_id: undefined,
      },
      ciTypeGroup: [],
      typeAttrs: [],
      filterExp: '',
    }
  },
  watch: {
    disabled: {
      immediate: false,
      handler(newValue) {
        const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
        if (newValue) {
          // 如果是disabled 把tab 的ink-bar也置灰
          dom.style.backgroundColor = '#00000040'
        } else {
          dom.style.backgroundColor = '#2f54eb'
        }
      },
    },
    'choice_other.type_ids': {
      handler(newValue) {
        if (newValue && newValue.length) {
          getCITypeCommonAttributesByTypeIds({ type_ids: newValue.join(',') }).then((res) => {
            this.typeAttrs = res.attributes
          })
        }
      },
    },
  },
  created() {
    getCITypeGroups({ need_other: true }).then((res) => {
      this.ciTypeGroup = res
        .filter((item) => item.ci_types && item.ci_types.length)
        .map((item) => {
          item.id = `parent_${item.id || -1}`
          return { ..._.cloneDeep(item) }
        })
    })
  },
  methods: {
    addNewValue(newValue, newStyle, newIcon) {
      if (newValue) {
        const idx = this.valueList.findIndex((v) => v[0] === newValue)
        if (idx > -1) {
          this.$message.warning('当前值已存在！')
        } else {
          this.valueList.push([newValue, { style: newStyle, icon: { ...newIcon } }])
        }
      }
    },
    deleteValue(item) {
      const _valueList = _.cloneDeep(this.valueList)
      const idx = _valueList.findIndex((v) => v[0] === item[0])
      if (idx > -1) {
        _valueList.splice(idx, 1)
        this.valueList = _valueList
      }
    },
    editValue(item, newValue, newStyle, newIcon) {
      const _valueList = _.cloneDeep(this.valueList)
      const idx = _valueList.findIndex((v) => v[0] === item[0])
      if (idx > -1) {
        _valueList[idx] = [newValue, { style: newStyle, icon: { ...newIcon } }]
        this.valueList = _valueList
      }
    },
    getData() {
      if (this.activeKey === 'define') {
        return {
          choice_value: this.valueList,
          choice_web_hook: null,
          choice_other: null,
        }
      } else if (this.activeKey === 'webhook') {
        const choice_web_hook = this.$refs.webhook.getParams()
        choice_web_hook.ret_key = this.form.ret_key
        return { choice_value: [], choice_web_hook, choice_other: null }
      } else {
        let choice_other = {}
        if (this.choice_other.type_ids && this.choice_other.type_ids.length) {
          this.$refs.filterComp.handleSubmit()
          choice_other = { ...this.choice_other, filter: this.filterExp }
        }
        return {
          choice_value: [],
          choice_web_hook: null,
          choice_other,
        }
      }
    },
    setData({ choice_value, choice_web_hook, choice_other }) {
      if (choice_web_hook) {
        this.activeKey = 'webhook'
        this.$nextTick(() => {
          this.$refs.webhook.setParams(choice_web_hook)
          this.form.ret_key = choice_web_hook.ret_key ?? ''
        })
      } else if (choice_other) {
        this.activeKey = 'choice_other'
        const { type_ids, attr_id, filter } = choice_other
        this.choice_other = { type_ids, attr_id }
        this.filterExp = filter
        if (type_ids && type_ids.length) {
          this.$nextTick(() => {
            this.$refs.filterComp.visibleChange(true, false)
          })
        }
      } else {
        this.valueList = choice_value
        this.activeKey = 'define'
      }
      const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
      if (this.disabled) {
        // 如果是disabled 把tab 的ink-bar也置灰
        dom.style.backgroundColor = '#00000040'
      } else {
        dom.style.backgroundColor = '#2f54eb'
      }
    },
    setExpFromFilter(filterExp) {
      if (filterExp) {
        this.filterExp = `${filterExp}`
      } else {
        this.filterExp = ''
      }
    },
  },
}
</script>

<style lang="less" scoped>
.pre-value-edit-color {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  .pre-value-edit-color-item {
    cursor: pointer;
    display: inline-block;
    width: 25px;
    height: 20px;
    margin: 5px;
  }
}
</style>

<style lang="less">
.pre-value-filter {
  .ant-form-item-control {
    line-height: 24px;
  }
  .table-filter-add {
    line-height: 40px;
  }
}
</style>
