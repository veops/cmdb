<template>
  <a-tabs
    id="preValueArea"
    v-model="activeKey"
    @change="changeActiveKey"
    size="small"
    :tabBarStyle="{ borderBottom: 'none' }"
  >
    <a-tab-pane key="define" :disabled="disabled">
      <span style="font-size:14px;" slot="tab">{{ $t('cmdb.ciType.enum') }}</span>
      <PreValueDefine
        v-model="valueList"
        :disabled="disabled"
        :enumValueType="enumValueType"
      />
    </a-tab-pane>
    <a-tab-pane key="builtin" :disabled="disabled">
      <div class="tab-builtin" slot="tab">
        <span class="tab-builtin-title">{{ $t('cmdb.ciType.builtin') }}</span>
        <span v-if="isOpenSource" class="tab-builtin-tag">Pro</span>
      </div>
      <PreValueBuiltIn ref="builtInRef" />
    </a-tab-pane>
    <a-tab-pane key="webhook" :disabled="disabled">
      <span style="font-size:14px;" slot="tab">Webhook</span>
      <Webhook ref="webhook" style="margin-top:10px" />
      <a-form-model :model="form">
        <a-col :span="24">
          <a-form-model-item prop="ret_key" :labelCol="{ span: 3 }" :wrapperCol="{ span: 18 }">
            <template slot="label">
              <span
                style="position:relative;white-space:pre;"
              >{{ $t('cmdb.ciType.filter') }}
                <a-tooltip
                  :title="$t('cmdb.ciType.choiceWebhookTips')"
                >
                  <a-icon
                    class="tab-webhook-filter-icon"
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
      <span style="font-size:14px;" slot="tab">{{ $t('cmdb.ciType.choiceOther') }}</span>
      <a-row :gutter="[24, 24]">
        <a-col :span="24">
          <a-form-item
            :style="{ lineHeight: '24px', marginBottom: '5px' }"
            :label="$t('cmdb.ciType.ciType')"
            :label-col="{ span: 3 }"
            :wrapper-col="{ span: 12 }"
          >
            <treeselect
              :disable-branch-nodes="true"
              :class="{
                'custom-treeselect': true,
                'custom-treeselect-white': true,
              }"
              :style="{
                '--custom-height': '32px',
                lineHeight: '32px',
                '--custom-multiple-lineHeight': '14px',
              }"
              v-model="choice_other.type_ids"
              :multiple="true"
              :clearable="true"
              searchable
              :options="ciTypeGroup"
              value-consists-of="LEAF_PRIORITY"
              :placeholder="$t('cmdb.ciType.selectCIType')"
              :normalizer="
                (node) => {
                  return {
                    id: node.id || -1,
                    label: node.alias || node.name || $t('other'),
                    title: node.alias || node.name || $t('other'),
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
        <a-col :span="24" v-if="choice_other.type_ids && choice_other.type_ids.length">
          <a-form-item
            :style="{ marginBottom: '5px' }"
            :label="$t('cmdb.ciType.attributes')"
            :label-col="{ span: 3 }"
            :wrapper-col="{ span: 12 }"
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
              :placeholder="$t('cmdb.ciType.selectCITypeAttributes')"
              :normalizer="
                (node) => {
                  return {
                    id: node.id || -1,
                    label: node.alias || node.name || $t('other'),
                    title: node.alias || node.name || $t('other'),
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
            :label="$t('cmdb.ciType.filter')"
            :label-col="{ span: 3 }"
            :wrapper-col="{ span: 19 }"
          >
            <AttrFilter
              ref="attrFilter"
              :isDropdown="false"
              :canSearchPreferenceAttrList="typeAttrs"
              :CITypeId="CITypeId"
              :expression="filterExp ? `q=${filterExp}` : ''"
              :curModelAttrList="curModelAttrList"
              @setExpFromFilter="setExpFromFilter"
            />
          </a-form-item>
        </a-col>
      </a-row>
    </a-tab-pane>
    <a-tab-pane key="script" :disabled="disabled || !canDefineScript">
      <span style="font-size:14px;" slot="tab">{{ $t('cmdb.ciType.code') }}</span>
      <a-form-item
        :style="{ marginBottom: '5px' }"
        :label="$t('cmdb.ciType.cascadeAttr')"
        :label-col="{ span: $i18n.locale === 'en' ? 3 : 2 }"
        :wrapper-col="{ span: 19 }"
        labelAlign="left"
      >
        <a-select
          mode="multiple"
          style="width: 100%"
          :placeholder="$t('placeholder2')"
          optionFilterProp="title"
          v-model="cascade_attributes"
        >
          <a-select-option
            v-for="attr in curModelAttrList"
            :key="attr.id"
            :title="attr.name"

          >
            {{ attr.name }}
          </a-select-option>
        </a-select>
        <div class="ant-form-explain">{{ scriptCodeExtraText }}</div>
      </a-form-item>

      <div class="script-tip">
        <div>1. {{ $t('cmdb.ciType.computedAttrTip1') }}</div>
        <div>2. {{ $t('cmdb.ciType.computedAttrTip2') }}</div>
        <div>3. {{ $t('cmdb.ciType.computedAttrTip3') }}</div>
      </div>

      <div class="all-attr-btn">
        <a-button size="small" @click="showAllPropDrawer">
          {{ $t('cmdb.ciType.viewAllAttr') }}
        </a-button>
      </div>
      <AllAttrDrawer ref="allAttrDrawer" />

      <CustomCodeMirror
        codeMirrorId="cmdb-pre-value"
        ref="codemirror"
        @changeCodeContent="changeCodeContent"
      ></CustomCodeMirror>
      <!-- <codemirror style="z-index: 9999" :options="cmOptions" v-model="script"></codemirror> -->
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
import { getCITypeCommonAttributesByTypeIds, getCITypeAttributesById } from '../../api/CITypeAttr'
import AttrFilter from './preValueAttr/attrFilter/index.vue'
import AllAttrDrawer from './allAttrDrawer.vue'
import PreValueDefine from './preValueAttr/define/index.vue'
import PreValueBuiltIn from './preValueAttr/builtin/index.vue'
import { ENUM_VALUE_TYPE } from './preValueAttr/constants.js'

import CustomCodeMirror from '@/components/CustomCodeMirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'
require('codemirror/mode/python/python.js')

export default {
  name: 'PreValueArea',
  components: { draggable, PreValueTag, ColorPicker, Webhook, AttrFilter, CustomCodeMirror, AllAttrDrawer, PreValueDefine, PreValueBuiltIn },
  props: {
    disabled: {
      type: Boolean,
      default: true,
    },
    canDefineScript: {
      type: Boolean,
      default: false,
    },
    CITypeId: {
      type: Number,
      default: null,
    },
    // eslint-disable-next-line vue/require-default-prop
    enumValueType: {
      type: String,
      defualt: ENUM_VALUE_TYPE.INPUT
    }
  },
  data() {
    return {
      defautValueColor,
      activeKey: 'define', // define webhook
      valueList: [
        [
          '',
          {
            style: {},
            icon: {},
            label: ''
          }
        ]
      ],
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
      script:
        this.$t('cmdb.ciType.choiceScriptDemo'),
      cmOptions: {
        lineNumbers: true,
        mode: 'python',
        height: '200px',
        theme: 'monokai',
        tabSize: 4,
        lineWrapping: true,
        readOnly: this.disabled || !this.canDefineScript,
      },
      curModelAttrList: [], // 当前模型属性
      cascade_attributes: [] // 级联属性id列表
    }
  },
  computed: {
    scriptCodeExtraText() {
      return this.$t('cmdb.ciType.cascadeAttrTip') + (this.isOpenSource ? ` (${this.$t('cmdb.enterpriseVersionTip')})` : '')
    }
  },
  watch: {
    disabled: {
      immediate: false,
      handler(newValue) {
        const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
        if (newValue) {
          // If it is disabled, the ink-bar of the tab will also be grayed out.
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
    this.getCITypeAttributesById()
  },
  methods: {
    async getCITypeAttributesById() {
      if (!this.CITypeId) {
        this.curModelAttrList = []
        return
      }
      const res = await getCITypeAttributesById(this.CITypeId)
      let curModelAttrList = []
      if (res?.attributes?.length) {
        curModelAttrList = res.attributes.filter(attr => !attr.is_password)
      }
      this.curModelAttrList = curModelAttrList
    },

    getData() {
      if (this.activeKey === 'builtin') {
        return {
          choice_value: [],
          choice_web_hook: null,
          choice_other: null,
        }
      } else if (this.activeKey === 'define') {
        if (this.validateDefine()) {
          return {
            isError: true
          }
        }

        return {
          choice_value: this.valueList.filter((item) => !['', null, undefined].includes(item?.[0])),
          choice_web_hook: null,
          choice_other: null
        }
      } else if (this.activeKey === 'webhook') {
        const choice_web_hook = this.$refs.webhook.getParams()
        choice_web_hook.ret_key = this.form.ret_key
        return { choice_value: [], choice_web_hook, choice_other: null }
      } else if (this.activeKey === 'script') {
        return {
          choice_value: [],
          choice_web_hook: null,
          choice_other: {
            script: this.script,
            cascade_attributes: this.cascade_attributes,
          },
        }
      } else {
        let choice_other = {}
        if (this.choice_other.type_ids && this.choice_other.type_ids.length) {
          this.$refs.attrFilter.handleSubmit()
          choice_other = { ...this.choice_other, filter: this.filterExp }
        }
        return {
          choice_value: [],
          choice_web_hook: null,
          choice_other
        }
      }
    },

    validateDefine() {
      const valueList = this.valueList.filter((item) => {
        return !['', null, undefined].includes(item?.[0])
      })
      const isRepeat = _.uniq(valueList.map(item => item?.[0])).length !== valueList.length
      if (isRepeat) {
        this.$message.warning(this.$t('cmdb.ciType.enumValueTip2'))
        return true
      }

      return false
    },

    setData({ choice_value, choice_web_hook, choice_other }) {
      if (choice_web_hook) {
        this.activeKey = 'webhook'
        this.$nextTick(() => {
          this.$refs.webhook.setParams(choice_web_hook)
          this.form.ret_key = choice_web_hook.ret_key ?? ''
        })
      } else if (choice_other) {
        if (choice_other.script) {
          this.activeKey = 'script'
          this.script = choice_other.script
          this.$nextTick(() => {
            this.$refs.codemirror.initCodeMirror(choice_other.script)
          })
        } else {
          this.activeKey = 'choice_other'
          const { type_ids, attr_id, filter } = choice_other
          this.choice_other = { type_ids, attr_id }
          this.filterExp = filter
          this.cascade_attributes = choice_other?.cascade_attributes || []
          if (type_ids && type_ids.length) {
            this.$nextTick(() => {
              this.$refs.attrFilter.init(true, false)
            })
          }
        }
      } else {
        let valueList = [[
          '',
          {
            style: {},
            icon: {},
            label: ''
          }
        ]]
        if (choice_value?.length) {
          valueList = choice_value.map((item) => {
            return [
              item[0],
              {
                icon: item?.[1]?.['icon'] || {},
                style: item?.[1]?.['style'] || {},
                label: item?.[1]?.['label'] || item?.[0] || ''
              }
            ]
          })
        }
        this.valueList = valueList
        this.activeKey = 'define'
      }
      const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
      if (this.disabled) {
        // If it is disabled, the ink-bar of the tab will also be grayed out.
        dom.style.backgroundColor = '#00000040'
      } else {
        dom.style.backgroundColor = '#2f54eb'
      }
    },

    resetData() {
      this.activeKey = 'define'
      this.$set(this, 'valueList', [
        [
          '',
          {
            style: {},
            icon: {},
            label: ''
          }
        ]
      ])

      this.$nextTick(() => {
        if (this.$refs.builtInRef) {
          this.$refs.builtInRef.setData({})
        }

        if (this.$refs.webhook) {
          this.$refs.webhook.setParams({})
        }
        this.form.ret_key = ''

        this.script = ''
        this.cascade_attributes = []
        if (this.$refs.codemirror) {
          this.$refs.codemirror.initCodeMirror('')
        }

        this.choice_other = {
          type_ids: undefined,
          attr_id: undefined
        }
        if (this.$refs.attrFilter) {
          this.$refs.attrFilter.init(true, false)
        }
      })
    },

    initEnumValue() {
      if (this.valueList) {
        const valueList = _.cloneDeep(this.valueList)
        valueList.forEach((item) => {
          item[0] = ''
        })
        this.$set(this, 'valueList', valueList)
      }
    },

    setExpFromFilter(filterExp) {
      if (filterExp) {
        this.filterExp = `${filterExp}`
      } else {
        this.filterExp = ''
      }
    },
    changeCodeContent(value) {
      this.script = value && value.replace('\t', '    ')
    },
    changeActiveKey(value) {
      if (value === 'script') {
        this.$nextTick(() => {
          this.$refs.codemirror.initCodeMirror(this.script)
        })
      }
    },

    showAllPropDrawer() {
      this.$refs.allAttrDrawer.open()
    },
  },
}
</script>

<style lang="less" scoped>
.tab-builtin {
  display: flex;
  align-items: center;

  &-title {
    font-size: 14px;
  }

  &-tag {
    background-color: #E1EFFF;
    color: @primary-color;
    font-size: 10px;
    font-weight: 400;
    padding: 0 3px;
    margin-left: 3px;
  }
}

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

.tab-webhook-filter-icon {
  position: absolute;
  top: 3px;
  left: -17px;
  color: @primary-color;
}

.script-tip {
  font-size: 12px;
  line-height: 22px;
  color: #a5a9bc;
}

.all-attr-btn {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
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
