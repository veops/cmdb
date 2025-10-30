<template>
  <a-form
    :form="form"
    class="create-new-attribute"
    :label-col="formItemLayout.labelCol"
    :wrapper-col="formItemLayout.wrapperCol"
  >
    <a-divider style="font-size:14px;margin-top:6px;">{{ $t('cmdb.ciType.basicConfig') }}</a-divider>
    <a-row>
      <a-col :span="12">
        <a-form-item :label="$t('cmdb.ciType.AttributeName')">
          <a-input
            name="name"
            :placeholder="$t('cmdb.ciType.English')"
            v-decorator="[
              'name',
              {
                rules: [
                  { required: true, message: $t('cmdb.ciType.inputAttributeName') },
                  {
                    message: $t('cmdb.ciType.attributeNameTips'),
                    pattern: RegExp('^(?!\\d)[a-zA-Z_0-9]+$'),
                  },
                  {
                    message: $t('cmdb.ciType.buildinAttribute'),
                    pattern: RegExp('^(?!(id|_id|ci_id|type|_type|ci_type)$).*$'),
                  },
                ],
              },
            ]"
          />
          <div class="ant-form-explain">{{ $t('cmdb.ciType.fieldCannotModify') }}</div>
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item :label="$t('alias')">
          <a-input
            name="alias"
            :placeholder="$t('cmdb.ciType.aliasPlaceholder')"
            v-decorator="['alias', { rules: [] }]"
          />
        </a-form-item>
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="12">
        <a-form-item :label="$t('cmdb.ciType.DataType')">
          <a-select
            name="value_type"
            style="width: 100%"
            v-decorator="['value_type', { rules: [{ required: true }], initialValue: '2' }]"
            @change="handleChangeValueType"
          >
            <a-select-option :value="item.key" :key="item.key" v-for="(item) in valueTypeMap">
              <ops-icon :type="getPropertyIcon({ value_type: item.key })" />
              <span class="value-type-text">{{ item.value }}</span>
              <span class="value-type-des" v-if="item.key === '2'">{{ $t('cmdb.ciType.shortTextTip') }}</span>
              <span class="value-type-des" v-if="item.key === '3'">yyyy-mm-dd HH:MM:SS</span>
              <span class="value-type-des" v-if="item.key === '4'">yyyy-mm-dd</span>
              <span class="value-type-des" v-if="item.key === '5'">HH:MM:SS</span>
            </a-select-option>
          </a-select>
          <div class="ant-form-explain">{{ $t('cmdb.ciType.fieldCannotModify') }}</div>
        </a-form-item>
      </a-col>
      <a-col
        v-if="currentValueType !== '11'"
        :span="currentValueType === '6' ? 24 : 12"
      >
        <a-form-item
          :label-col="{ span: currentValueType === '6' ? 4 : 8 }"
          :wrapper-col="{ span: currentValueType === '6' ? 18 : 15 }"
          :label="$t('cmdb.ciType.defaultValue')"
        >
          <template>
            <a-input
              v-if="form.getFieldValue('is_list')"
              :style="{ width: '100%' }"
              v-decorator="['default_value', { rules: [{ required: false }] }]"
            >
            </a-input>
            <a-switch
              v-else-if="currentValueType === '10'"
              v-decorator="['default_value', { rules: [{ required: false }], valuePropName: 'checked' }]"
            />
            <a-input-number
              style="width: 100%"
              v-else-if="currentValueType === '1'"
              v-decorator="['default_value', { rules: [{ required: false }] }]"
            >
            </a-input-number>
            <a-select
              v-decorator="['default_value', { rules: [{ required: false }] }]"
              mode="tags"
              v-else-if="currentValueType === '0'"
              @select="selectIntDefaultValue"
            >
              <a-select-option key="$auto_inc_id">
                {{ $t('cmdb.ciType.autoIncID') }}
              </a-select-option>
            </a-select>
            <a-input
              style="width: 100%"
              v-else-if="['2', '5', '7', '8', '9'].includes(currentValueType)"
              v-decorator="['default_value', { rules: [{ required: false }] }]"
            >
            </a-input>
            <a-select
              allowClear
              v-decorator="['default_value', { rules: [{ required: false }] }]"
              v-else-if="currentValueType === '3' && defaultForDatetime !== '$custom_time'"
              @select="changeDefaultForDatetime"
            >
              <a-select-option key="$created_at">
                {{ $t('createdAt') }}
              </a-select-option>
              <a-select-option key="$updated_at">
                {{ $t('updatedAt') }}
              </a-select-option>
              <a-select-option key="$custom_time">
                {{ $t('cmdb.ciType.customTime') }}
              </a-select-option>
            </a-select>
            <template v-else-if="currentValueType === '4' || currentValueType === '3'">
              <a-date-picker
                style="width: 100%"
                v-decorator="['default_value', { rules: [{ required: false }] }]"
                :format="currentValueType === '4' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
                :showTime="currentValueType === '4' ? false : { format: 'HH:mm:ss' }"
              />
              <a-dropdown
                :style="{ position: 'absolute', right: '-15px', top: '-10px' }"
                :trigger="['click']"
                v-if="currentValueType === '3'"
              >
                <a><a-icon type="down" /> </a>
                <a-menu slot="overlay" @click="onClick">
                  <a-menu-item key="$created_at">
                    <a>{{ $t('createdAt') }}</a>
                  </a-menu-item>
                  <a-menu-item key="$updated_at">
                    <a>{{ $t('updatedAt') }}</a>
                  </a-menu-item>
                </a-menu>
              </a-dropdown>
            </template>

            <vue-json-editor
              v-else-if="currentValueType === '6'"
              :style="{ '--custom-height': `${200}px` }"
              v-model="default_value_json"
              :showBtns="false"
              :mode="'code'"
              lang="zh"
              @json-change="onJsonChange"
              @has-error="onJsonError"
            />
          </template>
        </a-form-item>
      </a-col>

      <a-col
        v-if="currentValueType === '11'"
        :span="12"
      >
        <ReferenceModelSelect
          :form="form"
          :formItemLayout="formItemLayout"
        />
      </a-col>
    </a-row>

    <!-- <a-col :span="currentValueType === '2' ? 6 : 0" v-if="currentValueType !== '6'">
      <a-form-item
        :hidden="currentValueType === '2' ? false : true"
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ $t('cmdb.ciType.index') }}
            <a-tooltip :title="$t('cmdb.ciType.indexTips')">
              <a-icon
                style="position:absolute;top:2px;left:-17px;color:#2f54eb;"
                type="question-circle"
                @click="
                  (e) => {
                    e.stopPropagation()
                    e.preventDefault()
                  }
                "
              />
            </a-tooltip>
          </span>
        </template>
        <a-switch
          :disabled="isShowComputedArea"
          @change="onChange"
          name="is_index"
          v-decorator="['is_index', { rules: [], valuePropName: 'checked', initialValue: true }]"
        />
      </a-form-item>
    </a-col> -->
    <a-col :span="6" v-if="currentValueType !== '6' && currentValueType !== '7'">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span style="position:relative;white-space:pre;">{{ $t('cmdb.ciType.unique') }}
            <a-tooltip :title="$t('cmdb.ciType.uniqueHint')">
              <a-icon
                style="position:absolute;top:2px;left:-17px;color:#A5A9BC;"
                type="info-circle"
                @click="(e) => { e.stopPropagation(); e.preventDefault() }"
              />
            </a-tooltip>
          </span>
        </template>
        <a-switch
          :disabled="isShowComputedArea"
          @change="onChange"
          name="is_unique"
          v-decorator="['is_unique', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        :label="$t('required')"
      >
        <a-switch
          @change="(checked) => onChange(checked, 'is_required')"
          name="is_required"
          v-decorator="['is_required', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ $t('cmdb.ciType.defaultShow') }}
            <a-tooltip :title="$t('cmdb.ciType.defaultShowTips')">
              <a-icon
                style="position:absolute;top:2px;left:-17px;color:#A5A9BC;"
                type="info-circle"
                @click="
                  (e) => {
                    e.stopPropagation()
                    e.preventDefault()
                  }
                "
              />
            </a-tooltip>
          </span>
        </template>
        <a-switch
          @change="onChange"
          name="default_show"
          v-decorator="['default_show', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6" v-if="currentValueType !== '6' && currentValueType !== '7'">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span style="position:relative;white-space:pre;">{{ $t('cmdb.ciType.isSortable') }}
            <a-tooltip :title="$t('cmdb.ciType.sortableHint')">
              <a-icon
                style="position:absolute;top:2px;left:-17px;color:#A5A9BC;"
                type="info-circle"
                @click="(e) => { e.stopPropagation(); e.preventDefault() }"
              />
            </a-tooltip>
          </span>
        </template>
        <a-switch
          :disabled="isShowComputedArea"
          @change="(checked) => onChange(checked, 'is_sortable')"
          name="is_sortable"
          v-decorator="['is_sortable', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>

    <a-col :span="6" v-if="!['6', '7', '10'].includes(currentValueType)">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >
            <a-tooltip :title="$t('cmdb.ciType.listTips')">
              <a-icon
                style="position:absolute;top:3px;left:-17px;color:#A5A9BC;"
                type="info-circle"
                @click="
                  (e) => {
                    e.stopPropagation()
                    e.preventDefault()
                  }
                "
              />
            </a-tooltip>
            {{ $t('cmdb.ciType.list') }}
          </span>
        </template>
        <a-switch
          :disabled="isShowComputedArea"
          @change="(checked) => onChange(checked, 'is_list')"
          name="is_list"
          v-decorator="['is_list', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col span="6">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >
            <a-tooltip :title="$t('cmdb.ciType.dynamicTips')">
              <a-icon
                style="position:absolute;top:3px;left:-17px;color:#A5A9BC;"
                type="info-circle"
                @click="
                  (e) => {
                    e.stopPropagation()
                    e.preventDefault()
                  }
                "
              />
            </a-tooltip>
            {{ $t('cmdb.ciType.isDynamic') }}
          </span>
        </template>
        <a-switch
          @change="(checked) => onChange(checked, 'is_dynamic')"
          name="is_dynamic"
          v-decorator="['is_dynamic', { rules: [], valuePropName: 'checked', initialValue: currentValueType === '6' ? true: false }]"
        />
      </a-form-item>
    </a-col>
    <a-divider style="font-size:14px;margin-top:6px;">{{ $t('cmdb.ciType.advancedSettings') }}</a-divider>
    <a-row>
      <a-col :span="24">
        <a-form-item
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 12 }"
          :label="$t('cmdb.ciType.reg')"
        >
          <RegSelect
            v-model="re_check"
            :isShowErrorMsg="false"
            :limitedFormat="getLimitedFormat()"
            :disabled="['6', '10', '11'].includes(currentValueType)"
          />
          <div class="ant-form-explain">{{ $t('cmdb.ciType.regCheckHint') }}</div>
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <a-form-item
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 20 }"
          :label="$t('cmdb.ciType.font')"
        >
          <FontArea ref="fontArea" :fontColorDisabled="['8', '11'].includes(currentValueType)" />
          <div class="ant-form-explain">{{ $t('cmdb.ciType.fontHint') }}</div>
        </a-form-item>
      </a-col>
      <a-col :span="24" v-if="!['6', '7', '10', '11'].includes(currentValueType)">
        <a-form-item
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 20 }"
        >
          <template slot="label">
            <span style="position:relative;white-space:pre;">{{ $t('cmdb.ciType.choiceValue') }}
              <a-tooltip :title="$t('cmdb.ciType.choiceValueHint')">
                <a-icon
                  style="position:absolute;top:2px;left:-17px;color:#A5A9BC;"
                  type="info-circle"
                  @click="(e) => { e.stopPropagation(); e.preventDefault() }"
                />
              </a-tooltip>
            </span>
          </template>
          <PreValueArea
            ref="preValueArea"
            :canDefineScript="canDefineScript"
            :disabled="isShowComputedArea"
            :CITypeId="CITypeId"
            :enumValueType="enumValueType"
          />

          <a-button type="primary" size="small" ghost @click="resetPreValue" style="margin-top: 8px;">{{ $t('reset') }}</a-button>
        </a-form-item>
      </a-col>
      <a-col :span="24" v-if="!['6', '7', '10', '11'].includes(currentValueType)">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
          <template slot="label">
            <span
              style="position:relative;white-space:pre;"
            >
              <a-tooltip :title="$t('cmdb.ciType.computedAttributeTips')">
                <a-icon
                  style="position:absolute;top:3px;left:-17px;color:#A5A9BC;"
                  type="info-circle"
                  @click="
                    (e) => {
                      e.stopPropagation()
                      e.preventDefault()
                    }
                  "
                />
              </a-tooltip>
              {{ $t('cmdb.ciType.computedAttribute') }}
            </span>
          </template>
          <a-switch
            :disabled="!canDefineComputed"
            @change="(checked) => onChange(checked, 'is_computed')"
            name="is_computed"
            v-decorator="['is_computed', { rules: [], valuePropName: 'checked' }]"
          />
          <div v-show="isShowComputedArea" class="computed-attr-tip">
            <div>1. {{ $t('cmdb.ciType.computedAttrTip1') }}</div>
            <div>2. {{ $t('cmdb.ciType.computedAttrTip2') }}</div>
            <div>3. {{ $t('cmdb.ciType.computedAttrTip3') }}</div>
          </div>
          <ComputedArea ref="computedArea" v-if="isShowComputedArea" :canDefineComputed="canDefineComputed" />
        </a-form-item>
      </a-col>
    </a-row>
    <a-form-item v-if="hasFooter" :wrapper-col="{ offset: 18 }">
      <a-button type="primary" @click="handleSubmit">{{ $t('new') }}</a-button>
      <a-divider type="vertical" />
      <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
import moment from 'moment'
import vueJsonEditor from 'vue-json-editor'
import { createAttribute, canDefineComputed } from '@/modules/cmdb/api/CITypeAttr'
import { valueTypeMap } from '../../utils/const'
import ComputedArea from './computedArea.vue'
import PreValueArea from './preValueArea.vue'
import FontArea from './fontArea.vue'
import RegSelect from '@/components/RegexSelect'
import { getPropertyIcon } from '../../utils/helper'
import ReferenceModelSelect from './attributeEdit/referenceModelSelect.vue'
import { ENUM_VALUE_TYPE } from './preValueAttr/constants.js'

export default {
  name: 'CreateNewAttribute',
  components: {
    ComputedArea,
    PreValueArea,
    vueJsonEditor,
    FontArea,
    RegSelect,
    ReferenceModelSelect,
  },
  props: {
    hasFooter: {
      type: Boolean,
      default: true,
    },
    CITypeId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      formItemLayout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 15 },
      },
      horizontalFormItemLayout: {
        labelCol: { span: 16 },
        wrapperCol: { span: 4 },
      },
      form: this.$form.createForm(this),
      currentValueType: '2',
      default_value_json: {},
      default_value_json_right: true, // Is the current json correct?

      canDefineComputed: false,
      isShowComputedArea: false,

      defaultForDatetime: '',

      re_check: {},
      enumValueType: ENUM_VALUE_TYPE.INPUT
    }
  },
  computed: {
    valueTypeMap() {
      const map = valueTypeMap()
      const keys = ['0', '1', '2', '9', '3', '4', '5', '6', '7', '8', '10', '11']
      return keys.map((key) => ({
        key,
        value: map[key]
      }))
    },
    canDefineScript() {
      return this.canDefineComputed
    },
  },
  methods: {
    getPropertyIcon,
    handleSubmit(isCloseModal = true) {
      this.form.validateFields(async (err, values) => {
        if (!err) {
          if (values.choice_value) {
            values.choice_value = values.choice_value.split('\n')
          }

          console.log(values)
          const { is_required, default_show, default_value, is_dynamic } = values
          const data = { is_required, default_show, is_dynamic }

          if (values.value_type === '10') {
            values.default = { default: values.is_list ? (default_value || null) : Boolean(default_value) }
          } else if (values.value_type === '0' && default_value) {
            if (values.is_list) {
              values.default = { default: default_value || null }
            } else {
              values.default = { default: default_value[0] || null }
            }
          } else if (values.value_type === '6') {
            if (this.default_value_json_right) {
              values.default = { default: this.default_value_json }
            } else {
              values.default = { default: null }
            }
          } else if (default_value || default_value === 0) {
            if (values.value_type === '3' && !values.is_list) {
              if (default_value === '$created_at' || default_value === '$updated_at') {
                values.default = { default: default_value }
              } else {
                values.default = { default: moment(default_value).format('YYYY-MM-DD HH:mm:ss') }
              }
            } else if (values.value_type === '4' && !values.is_list) {
              values.default = { default: moment(default_value).format('YYYY-MM-DD') }
            } else {
              values.default = { default: default_value }
            }
          } else {
            values.default = { default: null }
          }

          if (values.is_computed) {
            const computedAreaData = this.$refs.computedArea.getData()
            values = { ...values, ...computedAreaData }
          } else {
            // If it is a non-computed attribute, check to see if there is a predefined value
            if (!['6', '7', '10', '11'].includes(values.value_type)) {
              const preValueAreaData = this.$refs.preValueArea.getData()
              // 预定义值校验错误
              if (preValueAreaData?.isError) {
                return
              }
              values = { ...values, ...preValueAreaData }
            }
          }

          delete values.is_required
          delete values.default_show
          delete values.default_value

          const fontOptions = this.$refs.fontArea.getData()

          // 索引
          values.is_index = !['6', '7', '8', '9', '11'].includes(values.value_type)

          // 重置数据类型
          switch (values.value_type) {
            case '7':
              values.value_type = '2'
              values.is_password = true
              break
            case '8':
              values.value_type = '2'
              values.is_link = true
              break
            case '9':
              values.value_type = '2'
              break
            case '10':
              values.value_type = '7'
              values.is_bool = true
              break
            case '11':
              values.value_type = '0'
              values.is_reference = true
              break
            default:
              break
          }

          const { attr_id } = await createAttribute({ ...values, option: { fontOptions } })

          this.form.resetFields()
          if (this?.$refs?.preValueArea) {
            this.$refs.preValueArea.valueList = []
          }
          this.currentValueType = '2'
          this.$emit('done', attr_id, data, isCloseModal)
        } else {
          throw new Error()
        }
      })
    },
    handleClose() {
      this.$emit('cancel')
    },
    async checkCanDefineComputed() {
      try {
        await canDefineComputed()
        this.canDefineComputed = true
      } catch {
        this.canDefineComputed = false
      }
    },
    handleChangeValueType(value) {
      this.$nextTick(() => {
        this.currentValueType = value
        if (['6', '10', '11'].includes(value)) {
          this.re_check = {}
        }

        switch (value) {
          case '0':
          case '1':
            this.enumValueType = ENUM_VALUE_TYPE.NUMBER
            break
          case '3':
            this.enumValueType = ENUM_VALUE_TYPE.DATE_TIME
            break
          case '4':
            this.enumValueType = ENUM_VALUE_TYPE.DATE
            break
          default:
            this.enumValueType = ENUM_VALUE_TYPE.INPUT
            break
        }
        if (['0', '1', '3', '4'].includes(value)) {
          if (this.$refs.preValueArea) {
            this.$refs.preValueArea.initEnumValue()
          }
        }

        this.handleSwitchType({ valueType: value })
      })
    },
    onChange(checked, property) {
      if (property === 'is_computed') {
        this.isShowComputedArea = checked
        if (checked) {
          this.form.setFieldsValue({
            is_list: false,
            is_unique: false,
            is_index: false,
            is_sortable: false,
          })
        }
      }
      if (property === 'is_list') {
        this.handleSwitchType({ checked })
      }
      if (checked && property === 'is_sortable') {
        this.$message.warning(this.$t('cmdb.ciType.addAttributeTips1'))
        this.form.setFieldsValue({
          is_required: true,
        })
      }
      if (!checked && property === 'is_required' && this.form.getFieldValue('is_sortable')) {
        this.$message.warning(this.$t('cmdb.ciType.addAttributeTips1'))
        this.$nextTick(() => {
          this.form.setFieldsValue({
            is_required: true,
          })
        })
      }
    },

    handleSwitchType({
      checked,
      valueType
    }) {
      checked = checked ?? this.form.getFieldValue('is_list')
      valueType = valueType ?? this.currentValueType

      let defaultValue = checked || valueType === '0' ? [] : ''

      switch (valueType) {
        case '2':
        case '9':
          defaultValue = ''
          break
        case '10':
          defaultValue = checked ? '' : false
          break
        default:
          break
      }

      this.form.setFieldsValue({
        default_value: defaultValue,
      })
    },

    onJsonChange(value) {
      this.default_value_json_right = true
    },
    onJsonError() {
      this.default_value_json_right = false
    },
    selectIntDefaultValue(value) {
      this.form.setFieldsValue({
        default_value: [value],
      })
    },
    changeDefaultForDatetime(value) {
      this.defaultForDatetime = value
      switch (value) {
        case '$custom_time':
          this.form.setFieldsValue({
            default_value: undefined,
          })
          break
        case '$updated_at':
          this.form.setFieldsValue({
            is_dynamic: true,
          })
          break
        default:
          break
      }
    },
    onClick({ key }) {
      console.log(key)
      this.defaultForDatetime = key
      this.form.setFieldsValue({
        default_value: key,
      })
    },
    getLimitedFormat() {
      if (['0'].includes(this.currentValueType)) {
        return ['number', 'phone', 'landline', 'zipCode', 'IDCard', 'monetaryAmount', 'custom']
      }
      if (['1'].includes(this.currentValueType)) {
        return ['number', 'monetaryAmount', 'custom']
      }
      if (['3', '4', '5'].includes(this.currentValueType)) {
        return ['custom']
      }
      if (this.currentValueType === '8') {
        return ['link', 'custom']
      }
      return []
    },

    resetPreValue() {
      if (this.$refs.preValueArea) {
        this.$refs.preValueArea.resetData()
      }
    }
  },
}
</script>
<style lang="less" scoped>
.computed-attr-tip {
  font-size: 12px;
  line-height: 22px;
  color: #a5a9bc;
}
.value-type-text {
  margin: 0 4px;
}
</style>
<style lang="less">
.create-new-attribute {
  .jsoneditor-outer {
    height: var(--custom-height) !important;
    border: 1px solid #2f54eb;
  }
  div.jsoneditor-menu {
    background-color: #2f54eb;
  }
}
.value-type-des {
  font-size: 10px;
  color: #a9a9a9;
}
</style>
