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
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item :label="$t('alias')">
          <a-input name="alias" v-decorator="['alias', { rules: [] }]" />
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
            <a-select-option :value="key" :key="key" v-for="(value, key) in valueTypeMap">
              {{ value }}
              <span class="value-type-des" v-if="key === '3'">yyyy-mm-dd HH:MM:SS</span>
              <span class="value-type-des" v-if="key === '4'">yyyy-mm-dd</span>
              <span class="value-type-des" v-if="key === '5'">HH:MM:SS</span>
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-col>
      <a-col :span="currentValueType === '6' ? 24 : 12">
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
              v-else-if="
                currentValueType === '2' ||
                  currentValueType === '5' ||
                  currentValueType === '7' ||
                  currentValueType === '8'
              "
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
    </a-row>

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
    <a-col :span="6" v-if="currentValueType !== '6' && currentValueType !== '7'">
      <a-form-item
        :label-col="{ span: 8 }"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        :label="$t('cmdb.ciType.unique')"
      >
        <a-switch
          :disabled="isShowComputedArea"
          @change="onChange"
          name="is_unique"
          v-decorator="['is_unique', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6" v-if="currentValueType === '2'">
      <a-form-item :label-col="horizontalFormItemLayout.labelCol" :wrapper-col="horizontalFormItemLayout.wrapperCol">
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ $t('cmdb.ciType.index') }}
            <a-tooltip :title="$t('cmdb.ciType.indexTips')">
              <a-icon
                style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                type="question-circle"
                theme="filled"
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
    </a-col>
    <a-col :span="6">
      <a-form-item
        :label-col="currentValueType === '2' ? { span: 8 } : horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ $t('cmdb.ciType.defaultShow') }}
            <a-tooltip :title="$t('cmdb.ciType.defaultShowTips')">
              <a-icon
                style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                type="question-circle"
                theme="filled"
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
        :label-col="currentValueType === '2' ? horizontalFormItemLayout.labelCol : { span: 8 }"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        :label="$t('cmdb.ciType.isSortable')"
      >
        <a-switch
          :disabled="isShowComputedArea"
          @change="(checked) => onChange(checked, 'is_sortable')"
          name="is_sortable"
          v-decorator="['is_sortable', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>

    <a-col :span="6" v-if="currentValueType !== '6' && currentValueType !== '7'">
      <a-form-item
        :label-col="currentValueType === '2' ? { span: 8 } : horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
      >
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ $t('cmdb.ciType.list') }}
            <a-tooltip :title="$t('cmdb.ciType.listTips')">
              <a-icon
                style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                type="question-circle"
                theme="filled"
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
          @change="(checked) => onChange(checked, 'is_list')"
          name="is_list"
          v-decorator="['is_list', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-divider style="font-size:14px;margin-top:6px;">{{ $t('cmdb.ciType.advancedSettings') }}</a-divider>
    <a-row>
      <a-col :span="24" v-if="!['6'].includes(currentValueType)">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 12 }" :label="$t('cmdb.ciType.reg')">
          <RegSelect :isShowErrorMsg="false" v-model="re_check" :limitedFormat="getLimitedFormat()" />
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" :label="$t('cmdb.ciType.font')">
          <FontArea ref="fontArea" />
        </a-form-item>
      </a-col>
      <a-col :span="24" v-if="!['6', '7'].includes(currentValueType)">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" :label="$t('cmdb.ciType.choiceValue')">
          <PreValueArea ref="preValueArea" :canDefineScript="canDefineScript" :disabled="isShowComputedArea" />
        </a-form-item>
      </a-col>
      <a-col :span="24" v-if="!['6', '7'].includes(currentValueType)">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
          <template slot="label">
            <span
              style="position:relative;white-space:pre;"
            >{{ $t('cmdb.ciType.computedAttribute') }}
              <a-tooltip :title="$t('cmdb.ciType.computedAttributeTips')">
                <a-icon
                  style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                  type="question-circle"
                  theme="filled"
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
            :disabled="!canDefineComputed"
            @change="(checked) => onChange(checked, 'is_computed')"
            name="is_computed"
            v-decorator="['is_computed', { rules: [], valuePropName: 'checked' }]"
          />
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

export default {
  name: 'CreateNewAttribute',
  components: {
    ComputedArea,
    PreValueArea,
    vueJsonEditor,
    FontArea,
    RegSelect,
  },
  props: {
    hasFooter: {
      type: Boolean,
      default: true,
    },
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
    }
  },
  computed: {
    valueTypeMap() {
      return valueTypeMap()
    },
    canDefineScript() {
      return this.canDefineComputed
    },
  },
  methods: {
    handleSubmit(isCloseModal = true) {
      this.form.validateFields(async (err, values) => {
        if (!err) {
          if (values.choice_value) {
            values.choice_value = values.choice_value.split('\n')
          }

          console.log(values)
          const { is_required, default_show, default_value } = values
          const data = { is_required, default_show }
          delete values.is_required
          delete values.default_show
          if (values.value_type === '0' && default_value) {
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
          delete values.default_value
          if (values.is_computed) {
            const computedAreaData = this.$refs.computedArea.getData()
            values = { ...values, ...computedAreaData }
          } else {
            // If it is a non-computed attribute, check to see if there is a predefined value
            if (!['6', '7'].includes(values.value_type)) {
              const preValueAreaData = this.$refs.preValueArea.getData()
              values = { ...values, ...preValueAreaData }
            }
          }
          const fontOptions = this.$refs.fontArea.getData()

          // is_index: except for text, the index is hidden, text index default is true
          // 5 types in the box,  is_index=true
          // json, password, link  is_index=false
          if (['6', '7', '8'].includes(values.value_type)) {
            values.is_index = false
          } else if (values.value_type !== '2') {
            values.is_index = true
          }
          if (values.value_type === '7') {
            values.value_type = '2'
            values.is_password = true
          }
          if (values.value_type === '8') {
            values.value_type = '2'
            values.is_link = true
          }
          if (values.value_type !== '6') {
            values.re_check = this.re_check?.value ?? null
          }
          const { attr_id } = await createAttribute({ ...values, option: { fontOptions } })

          this.form.resetFields()
          this.currentValueType = '2'
          if (!['6'].includes(values.value_type) && !values.is_password) {
            this.$refs.preValueArea.valueList = []
          }
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
      this.currentValueType = value
      this.$nextTick(() => {
        this.form.setFieldsValue({
          default_value: this.form.getFieldValue('is_list') || value === '0' ? [] : null,
        })
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
        this.form.setFieldsValue({
          default_value: checked ? [] : '',
        })
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
      if (value === '$custom_time') {
        this.form.setFieldsValue({
          default_value: undefined,
        })
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
  },
}
</script>
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
