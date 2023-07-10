<template>
  <a-form :form="form" class="create-new-attribute">
    <a-divider style="font-size:14px;margin-top:6px;">基础设置</a-divider>
    <a-col :span="12">
      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="属性名(英文)">
        <a-input
          name="name"
          placeholder="英文"
          v-decorator="[
            'name',
            {
              rules: [
                { required: true, message: '请输入属性名' },
                { message: '不能以数字开头，可以是英文 数字以及下划线 (_)', pattern: RegExp('^(?!\\d)[a-zA-Z_0-9]+$') },
                { message: '内置字段', pattern: RegExp('^(?!(id|_id|ci_id|type|_type|ci_type)$).*$') },
              ],
            },
          ]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="12">
      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="别名">
        <a-input name="alias" v-decorator="['alias', { rules: [] }]" />
      </a-form-item>
    </a-col>
    <a-col :span="12">
      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="数据类型">
        <a-select
          name="value_type"
          style="width: 100%"
          v-decorator="['value_type', { rules: [{ required: true }], initialValue: '2' }]"
          @change="handleChangeValueType"
        >
          <a-select-option :value="key" :key="key" v-for="(value, key) in valueTypeMap">{{ value }}</a-select-option>
        </a-select>
      </a-form-item>
    </a-col>
    <a-col :span="currentValueType === '6' ? 24 : 12">
      <a-form-item
        :label-col="{ span: currentValueType === '6' ? 4 : 8 }"
        :wrapper-col="{ span: currentValueType === '6' ? 18 : 12 }"
        label="默认值"
      >
        <template>
          <a-select
            v-if="form.getFieldValue('is_list')"
            mode="tags"
            :style="{ width: '100%' }"
            v-decorator="['default_value', { rules: [{ required: false }] }]"
          >
          </a-select>
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
              自增ID
            </a-select-option>
          </a-select>
          <a-input
            style="width: 100%"
            v-else-if="currentValueType === '2' || currentValueType === '5'"
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
              创建时间
            </a-select-option>
            <a-select-option key="$updated_at">
              更新时间
            </a-select-option>
            <a-select-option key="$custom_time">
              自定义时间
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
                  <a>创建时间</a>
                </a-menu-item>
                <a-menu-item key="$updated_at">
                  <a>更新时间</a>
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
        label="必须"
      >
        <a-switch
          @change="onChange"
          name="is_required"
          v-decorator="['is_required', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6" v-if="currentValueType !== '6'">
      <a-form-item :label-col="{ span: 8 }" :wrapper-col="horizontalFormItemLayout.wrapperCol" label="唯一">
        <a-switch
          :disabled="isShowComputedArea"
          @change="onChange"
          name="is_unique"
          v-decorator="['is_unique', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6" v-if="currentValueType !== '6'">
      <a-form-item :label-col="horizontalFormItemLayout.labelCol" :wrapper-col="horizontalFormItemLayout.wrapperCol">
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ `索引` }}
            <a-tooltip title="字段可被用于检索，加速查询">
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
      <a-form-item :label-col="{ span: 8 }" :wrapper-col="horizontalFormItemLayout.wrapperCol">
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ `显示` }}
            <a-tooltip title="CI实例表格默认展示该字段">
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
    <a-col :span="6" v-if="currentValueType !== '6'">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="排序"
      >
        <a-switch
          :disabled="isShowComputedArea"
          @change="onChange"
          name="is_sortable"
          v-decorator="['is_sortable', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>

    <a-col :span="6" v-if="currentValueType !== '6'">
      <a-form-item :label-col="{ span: 8 }" :wrapper-col="horizontalFormItemLayout.wrapperCol">
        <template slot="label">
          <span
            style="position:relative;white-space:pre;"
          >{{ `多值` }}
            <a-tooltip title="字段的值是1个或者多个，接口返回的值的类型是list">
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
    <a-col :span="6" v-if="currentValueType === '2'">
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="密码"
      >
        <a-switch
          :disabled="isShowComputedArea"
          @change="(checked) => onChange(checked, 'is_password')"
          name="is_password"
          v-decorator="['is_password', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-col :span="6" v-if="currentValueType === '2'">
      <a-form-item :label-col="{ span: 8 }" :wrapper-col="horizontalFormItemLayout.wrapperCol" label="链接">
        <a-switch
          :disabled="isShowComputedArea"
          @change="(checked) => onChange(checked, 'is_link')"
          name="is_link"
          v-decorator="['is_link', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
    </a-col>
    <a-divider style="font-size:14px;margin-top:6px;">高级设置</a-divider>
    <a-row>
      <a-col :span="24">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" label="字体">
          <FontArea ref="fontArea" />
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }" label="预定义值">
          <PreValueArea ref="preValueArea" :disabled="isShowComputedArea" />
        </a-form-item>
      </a-col>
      <a-col :span="24">
        <a-form-item :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
          <template slot="label">
            <span
              style="position:relative;white-space:pre;"
            >{{ `计算属性` }}
              <a-tooltip
                :title="
                  `该属性的值是通过模型的其它属性构建的表达式或者执行一段代码的方式计算而来，属性的引用方法为: {{ 属性名 }}`
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
            name="is_password"
            v-decorator="['is_computed', { rules: [], valuePropName: 'checked' }]"
          />
          <ComputedArea ref="computedArea" v-if="isShowComputedArea" :canDefineComputed="canDefineComputed" />
        </a-form-item>
      </a-col>
    </a-row>
    <a-form-item v-if="hasFooter" :wrapper-col="{ offset: 18 }">
      <a-button type="primary" @click="handleSubmit">新增</a-button>
      <a-divider type="vertical" />
      <a-button @click="handleClose">取消</a-button>
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

export default {
  name: 'CreateNewAttribute',
  components: {
    ComputedArea,
    PreValueArea,
    vueJsonEditor,
    FontArea,
  },
  props: {
    hasFooter: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      valueTypeMap,
      formItemLayout: {
        labelCol: { span: 8 },
        wrapperCol: { span: 12 },
      },
      horizontalFormItemLayout: {
        labelCol: { span: 16 },
        wrapperCol: { span: 4 },
      },
      form: this.$form.createForm(this),
      currentValueType: '2',
      default_value_json: {},
      default_value_json_right: true, // 当前json是否正确

      canDefineComputed: false,
      isShowComputedArea: false,

      defaultForDatetime: '',
    }
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
          if (values.value_type === '0' && default_value && default_value.length) {
            values.default = { default: default_value[0] }
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
            // 如果是非计算属性，就看看有没有预定义值
            const preValueAreaData = this.$refs.preValueArea.getData()
            values = { ...values, ...preValueAreaData }
          }
          const fontOptions = this.$refs.fontArea.getData()

          const { attr_id } = await createAttribute({ ...values, option: { fontOptions } })

          this.form.resetFields()
          this.currentValueType = '0'
          this.$refs.preValueArea.valueList = []
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
          if (this.currentValueType === '2') {
            this.form.setFieldsValue({
              is_password: false,
              is_link: false,
            })
          }
        }
      }
      if (checked && property === 'is_password') {
        this.form.setFieldsValue({
          is_link: false,
        })
      }
      if (checked && property === 'is_link') {
        this.form.setFieldsValue({
          is_password: false,
        })
      }
      if (property === 'is_list') {
        this.form.setFieldsValue({
          default_value: checked ? [] : '',
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
</style>
