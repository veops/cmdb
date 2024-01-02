<template>
  <CustomDrawer
    :closable="true"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="800"
    :bodyStyle="{ paddingTop: 0 }"
    :headerStyle="{ borderBottom: 'none' }"
    wrapClassName="attribute-edit-form"
  >
    <a-form :form="form" :layout="formLayout">
      <a-divider style="font-size:14px;margin-top:6px;">{{ $t('cmdb.ciType.basicConfig') }}</a-divider>
      <a-col :span="12">
        <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" :label="$t('cmdb.ciType.AttributeName')">
          <a-input
            :disabled="true"
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
                ],
              },
            ]"
          />
        </a-form-item>
      </a-col>
      <a-col
        :span="12"
      ><a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" :label="$t('alias')">
        <a-input name="alias" v-decorator="['alias', { rules: [] }]" /> </a-form-item
      ></a-col>
      <a-col
        :span="12"
      ><a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" :label="$t('cmdb.ciType.DataType')">
        <a-select
          :disabled="true"
          name="value_type"
          style="width: 100%"
          v-decorator="['value_type', { rules: [{ required: true }] }]"
          @change="handleChangeValueType"
        >
          <a-select-option :value="key" :key="key" v-for="(value, key) in valueTypeMap">{{ value }}</a-select-option>
        </a-select>
      </a-form-item></a-col
      >
      <a-col :span="currentValueType === '6' ? 24 : 12">
        <a-form-item
          :label-col="{ span: currentValueType === '6' ? 4 : 8 }"
          :wrapper-col="{ span: currentValueType === '6' ? 18 : 12 }"
          :label="$t('cmdb.ciType.defaultValue')"
        >
          <template>
            <a-select
              v-if="form.getFieldValue('is_list')"
              mode="tags"
              :style="{ width: '100%' }"
              v-decorator="['default_value', { rules: [{ required: false }] }]"
            >
            </a-select>
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
            <a-input-number
              style="width: 100%"
              v-else-if="currentValueType === '1'"
              v-decorator="['default_value', { rules: [{ required: false }] }]"
            >
            </a-input-number>
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
        <a-form-item :label-col="{ span: 8 }" :wrapper-col="horizontalFormItemLayout.wrapperCol" :label="$t('cmdb.ciType.unique')">
          <a-switch
            :disabled="isShowComputedArea"
            @change="onChange"
            name="is_unique"
            v-decorator="['is_unique', { rules: [], valuePropName: 'checked' }]"
          />
        </a-form-item>
      </a-col>
      <a-col :span="currentValueType === '2' ? 6 : 0" v-if="currentValueType !== '6'">
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
            v-decorator="['is_index', { rules: [], valuePropName: 'checked' }]"
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
            :disabled="true || isShowComputedArea"
            @change="(checked) => onChange(checked, 'is_list')"
            name="is_list"
            v-decorator="['is_list', { rules: [], valuePropName: 'checked' }]"
          />
        </a-form-item>
      </a-col>
      <a-divider style="font-size:14px;margin-top:6px;">{{ $t('cmdb.ciType.advancedSettings') }}</a-divider>
      <a-row>
        <a-col :span="24">
          <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" :label="$t('cmdb.ciType.font')">
            <FontArea ref="fontArea" />
          </a-form-item>
        </a-col>
        <a-col :span="24" v-if="!['6', '7'].includes(currentValueType)">
          <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" :label="$t('cmdb.ciType.choiceValue')">
            <PreValueArea
              v-if="drawerVisible"
              :canDefineScript="canDefineScript"
              ref="preValueArea"
              :disabled="isShowComputedArea"
            />
          </a-form-item>
        </a-col>
        <a-col :span="24" v-if="!['6', '7'].includes(currentValueType)">
          <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <template slot="label">
              <span
                style="position:relative;white-space:pre;"
              >{{ $t('cmdb.ciType.computedAttribute') }}
                <a-tooltip
                  :title="
                    $t('cmdb.ciType.computedAttributeTips')
                  "
                >
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
            <ComputedArea
              showCalcComputed
              ref="computedArea"
              v-show="isShowComputedArea"
              @handleCalcComputed="handleCalcComputed"
              :canDefineComputed="canDefineComputed"
            />
          </a-form-item>
        </a-col>
      </a-row>

      <a-form-item>
        <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
      </a-form-item>
      <div class="custom-drawer-bottom-action">
        <a-button @click="onClose">{{ $t('cancel') }}</a-button>
        <a-button @click="handleSubmit(false)" type="primary">{{ $t('confirm') }}</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>

<script>
import _ from 'lodash'
import moment from 'moment'
import vueJsonEditor from 'vue-json-editor'
import {
  updateAttributeById,
  updateCITypeAttributesById,
  canDefineComputed,
  calcComputedAttribute,
} from '@/modules/cmdb/api/CITypeAttr'
import { valueTypeMap } from '../../utils/const'
import ComputedArea from './computedArea.vue'
import PreValueArea from './preValueArea.vue'
import FontArea from './fontArea.vue'

export default {
  name: 'AttributeEditForm',
  components: { ComputedArea, PreValueArea, vueJsonEditor, FontArea },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
    CITypeName: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      drawerTitle: this.$t('cmdb.ciType.addAttribute'),
      drawerVisible: false,

      formLayout: 'horizontal',

      record: {},

      currentValueType: '0',
      default_value_json: {},
      default_value_json_right: true, // Is the current json correct?

      canDefineComputed: false,
      isShowComputedArea: false,

      defaultForDatetime: '',
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  computed: {
    valueTypeMap() {
      return valueTypeMap()
    },
    formItemLayout() {
      const { formLayout } = this
      return formLayout === 'horizontal'
        ? {
            labelCol: { span: 8 },
            wrapperCol: { span: 12 },
          }
        : {}
    },

    horizontalFormItemLayout() {
      return {
        labelCol: { span: 16 },
        wrapperCol: { span: 4 },
      }
    },
    canDefineScript() {
      return this.canDefineComputed
    },
  },
  mounted() {},
  methods: {
    async handleCreate() {
      try {
        await canDefineComputed()
        this.canDefineComputed = true
      } catch {
        this.canDefineComputed = false
      }

      this.drawerTitle = this.$t('cmdb.ciType.addAttribute')
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
    },
    onChange(checked, property) {
      if (property === 'is_computed') {
        this.isShowComputedArea = checked
        if (checked) {
          this.form.setFieldsValue({
            is_list: false,
            is_unique: false,
            is_sortable: false,
          })
          if (this.currentValueType === '2') {
            this.form.setFieldsValue({
              is_index: true,
            })
          }
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

    async handleEdit(record, attributes) {
      try {
        await canDefineComputed()
        this.canDefineComputed = true
      } catch {
        this.canDefineComputed = false
      }
      const _record = _.cloneDeep(record)
      if (_record.is_password) {
        _record.value_type = '7'
      }
      if (_record.is_link) {
        _record.value_type = '8'
      }
      this.drawerTitle = this.$t('cmdb.ciType.editAttribute')
      this.drawerVisible = true
      this.record = _record
      this.currentValueType = _record.value_type
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: _record.id,
          alias: _record.alias,
          name: _record.name,
          value_type: _record.value_type,
          is_required: _record.is_required,
          default_show: _record.default_show,
        })
        if (!['6', '7'].includes(_record.value_type)) {
          this.form.setFieldsValue({
            is_list: _record.is_list,
            is_unique: _record.is_unique,
            is_index: _record.is_index,
            is_sortable: _record.is_sortable,
            is_computed: _record.is_computed,
          })
        }
        console.log(_record)
        if (_record.default) {
          this.$nextTick(() => {
            if (_record.value_type === '0') {
              this.form.setFieldsValue({
                default_value: _record.default.default ? [_record.default.default] : [],
              })
            } else if (_record.value_type === '6') {
              this.default_value_json = _record?.default?.default || null
            } else if (_record.value_type === '3' || _record.value_type === '4') {
              if (_record?.default?.default === '$created_at' || _record?.default?.default === '$updated_at') {
                this.defaultForDatetime = _record.default.default
                this.form.setFieldsValue({
                  default_value: _record?.default?.default,
                })
              } else {
                this.defaultForDatetime = '$custom_time'
                this.form.setFieldsValue({
                  default_value: _record.default && _record.default.default ? moment(_record.default.default) : null,
                })
              }
            } else {
              this.$nextTick(() => {
                this.form.setFieldsValue({
                  default_value: _record.default && _record.default.default ? _record.default.default : null,
                })
              })
            }
          })
        } else {
          this.default_value_json = {}
          if (_record.value_type === '0') {
            this.form.setFieldsValue({
              default_value: [],
            })
          } else if (_record.value_type !== '6') {
            this.form.setFieldsValue({
              default_value: null,
            })
          }
        }
        this.isShowComputedArea = _record.is_computed
        if (_record.is_computed) {
          this.$nextTick(() => {
            this.$refs.computedArea.setData({
              compute_expr: _record.compute_expr,
              compute_script: _record.compute_script,
            })
          })
        }
        const _find = attributes.find((item) => item.id === _record.id)
        if (!['6', '7'].includes(_record.value_type)) {
          this.$refs.preValueArea.setData({
            choice_value: (_find || {}).choice_value || [],
            choice_web_hook: _record.choice_web_hook,
            choice_other: _record.choice_other || undefined,
          })
        }
        this.$refs.fontArea.setData({
          fontOptions: _find?.option?.fontOptions || {},
        })
      })
    },

    async handleSubmit(isCalcComputed = false) {
      await this.form.validateFields(async (err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)

          if (this.record.is_required !== values.is_required || this.record.default_show !== values.default_show) {
            console.log('changed is_required')
            await updateCITypeAttributesById(this.CITypeId, {
              attributes: [
                { attr_id: this.record.id, is_required: values.is_required, default_show: values.default_show },
              ],
            })
          }

          delete values['default_show']
          delete values['is_required']
          const { default_value } = values
          if (values.value_type === '0' && default_value) {
            values.default = { default: default_value[0] || null }
          } else if (values.value_type === '6') {
            if (this.default_value_json_right) {
              values.default = { default: this.default_value_json }
            } else {
              values.default = { default: null }
            }
          } else if (default_value || default_value === 0) {
            if (values.value_type === '3') {
              if (default_value === '$created_at' || default_value === '$updated_at') {
                values.default = { default: default_value }
              } else {
                values.default = { default: moment(default_value).format('YYYY-MM-DD HH:mm:ss') }
              }
            } else if (values.value_type === '4') {
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
          if (values.value_type === '7') {
            values.value_type = '2'
            values.is_password = true
          }
          if (values.value_type === '8') {
            values.value_type = '2'
            values.is_link = true
          }
          if (values.id) {
            await this.updateAttribute(values.id, { ...values, option: { fontOptions } }, isCalcComputed)
          } else {
            // this.createAttribute(values)
          }
        }
      })
    },
    async updateAttribute(attrId, data, isCalcComputed = false) {
      await updateAttributeById(attrId, data)
      if (isCalcComputed) {
        await calcComputedAttribute(attrId)
      }
      this.$message.success(this.$t('updateSuccess'))
      this.handleOk()
      this.onClose()
    },
    handleOk() {
      this.$emit('ok')
    },
    handleChangeValueType(value) {
      this.currentValueType = value
      this.$nextTick(() => {
        this.form.setFieldsValue({
          default_value: this.form.getFieldValue('is_list') ? [] : null,
        })
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
    async handleCalcComputed() {
      await this.handleSubmit(true)
    },
  },
  watch: {},
}
</script>

<style lang="less" scoped></style>
<style lang="less">
.attribute-edit-form {
  .jsoneditor-outer {
    height: var(--custom-height) !important;
    border: 1px solid #2f54eb;
  }
  div.jsoneditor-menu {
    background-color: #2f54eb;
  }
}
</style>
