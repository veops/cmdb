<template>
  <a-drawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >

    <a-form :form="form" :layout="formLayout" @submit="handleSubmit">

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="属性名(英文)"
      >
        <a-input
          name="name"
          placeholder="英文"
          v-decorator="['name', {rules: [{ required: true, message: '请输入属性名'},{message: '不能以数字开头，可以是英文 数字以及下划线 (_)', pattern: RegExp('^(?!\\d)[a-zA-Z_0-9]+$')}]} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="别名"
      >
        <a-input
          name="alias"
          v-decorator="['alias', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="数据类型"
      >

        <a-select
          name="value_type"
          style="width: 120px"
          v-decorator="['value_type', {rules: [{required: true}], } ]"
        >
          <a-select-option :value="key" :key="key" v-for="(value, key) in ValueTypeMap">{{ value }}</a-select-option>
        </a-select>

      </a-form-item>

      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否唯一"
      >
        <a-switch
          @change="onChange"
          name="is_unique"
          v-decorator="['is_unique', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否索引"
      >
        <a-switch
          @change="onChange"
          name="is_index"
          v-decorator="['is_index', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否可排序"
      >
        <a-switch
          @change="onChange"
          name="is_sortable"
          v-decorator="['is_sortable', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否是链接"
      >
        <a-switch
          @change="onChange"
          name="is_link"
          v-decorator="['is_link', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否是密码"
      >
        <a-switch
          @change="onChange"
          name="is_password"
          v-decorator="['is_password', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否列表"
      >
        <a-switch
          @change="onChange"
          name="is_list"
          v-decorator="['is_list', {rules: [], valuePropName: 'checked',} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="预定义值"
      >
        <a-textarea
          :rows="5"
          name="choice_value"
          placeholder="多个值使用换行分隔"
          v-decorator="['choice_value', {rules: []} ]"
        />
      </a-form-item>
      <a-form-item>
        <a-input
          name="id"
          type="hidden"
          v-decorator="['id', {rules: []} ]"
        />
      </a-form-item>

      <div
        :style="{
          position: 'absolute',
          left: 0,
          bottom: 0,
          width: '100%',
          borderTop: '1px solid #e9e9e9',
          padding: '0.8rem 1rem',
          background: '#fff',

        }"
      >
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">确定</a-button>
        <a-button @click="onClose">取消</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { createAttribute, createCITypeAttributes, updateAttributeById } from '@/api/cmdb/CITypeAttr'
import { valueTypeMap } from './const'

export default {
  name: 'AttributeForm',
  components: {
    STable
  },
  data () {
    return {

      drawerTitle: '新增属性',
      drawerVisible: false,
      CITypeName: this.$route.params.CITypeName,
      CITypeId: this.$route.params.CITypeId,

      formLayout: 'vertical',

      attributes: [],
      allAttributes: [],

      ValueTypeMap: valueTypeMap

    }
  },

  beforeCreate () {
    this.form = this.$form.createForm(this)
  },

  computed: {

    formItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      } : {}
    },

    horizontalFormItemLayout () {
      return {
        labelCol: { span: 5 },
        wrapperCol: { span: 12 }
      }
    },
    buttonItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        wrapperCol: { span: 14, offset: 4 }
      } : {}
    }

  },
  mounted () {
  },
  methods: {

    handleCreate () {
      this.drawerVisible = true
    },
    onClose () {
      this.form.resetFields()
      this.drawerVisible = false
    },
    onChange (e) {
      console.log(`checked = ${e}`)
    },

    handleEdit (record) {
      this.drawerVisible = true
      console.log(record)
      this.$nextTick(() => {
        this.form.setFieldsValue({

          id: record.id,
          alias: record.alias,
          name: record.name,
          value_type: record.value_type,
          is_list: record.is_list,
          is_unique: record.is_unique,
          is_index: record.is_index,
          is_password: record.is_password,
          is_link: record.is_link,
          is_sortable: record.is_sortable,
          choice_value: (record.choice_value || []).join('\n')

        })
      })
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          if (values.choice_value) {
            values.choice_value = values.choice_value.split('\n')
          }

          if (values.id) {
            this.updateAttribute(values.id, values)
          } else {
            this.createAttribute(values)
          }
        }
      })
    },
    updateAttribute (attrId, data) {
      updateAttributeById(attrId, data)
        .then(res => {
          this.$message.success(`更新成功`)
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createAttribute (data) {
      createAttribute(data)
        .then(res => {
          if (this.CITypeId) {
            createCITypeAttributes(this.CITypeId, { attr_id: [res.attr_id] })
              .then(res => {
                this.$message.success(`添加成功`)
                this.handleOk()
                this.onClose()
              }).catch(err => this.requestFailed(err))
          } else {
            this.$message.success(`添加成功`)
            this.handleOk()
            this.onClose()
          }
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    }

  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null
    }
  }

}
</script>

<style lang="less" scoped>
  .search {
    margin-bottom: 54px;
  }

  .fold {
    width: calc(100% - 216px);
    display: inline-block
  }

  .operator {
    margin-bottom: 18px;
  }
  .action-btn {
    margin-bottom: 1rem;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
