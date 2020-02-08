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
        label="类型名"
      >
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', {rules: [{ required: true, message: '请输入资源名'}]} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="描述"
      >
        <a-textarea placeholder="请输入描述信息..." name="description" :rows="4" />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="权限"
      >
        <div :style="{ borderBottom: '1px solid #E9E9E9' }">
          <a-checkbox :indeterminate="indeterminate" @change="onCheckAllChange" :checked="checkAll">
            全选
          </a-checkbox>
        </div>
        <br />
        <a-checkbox-group :options="plainOptions" v-model="perms" @change="onPermChange" />

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
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('button.submit') }}</a-button>
        <a-button @click="onClose">{{ $t('button.cancel') }}</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { addResourceType, updateResourceTypeById } from '@/api/acl/resource'

export default {
  name: 'ResourceForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: '新增资源类型',
      drawerVisible: false,
      formLayout: 'vertical',
      perms: ['1'],
      indeterminate: true,
      checkAll: false,
      plainOptions: ['1', '2']
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
    onPermChange (perms) {
      this.indeterminate = !!perms.length && perms.length < this.plainOptions.length
      this.checkAll = perms.length === this.plainOptions.length
    },
    onCheckAllChange (e) {
      Object.assign(this, {
        perms: e.target.checked ? this.plainOptions : [],
        indeterminate: false,
        checkAll: e.target.checked
      })
    },
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
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          description: record.description
        })
      })
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.app_id = this.$route.name.split('_')[0]
          values.perms = this.perms
          if (values.id) {
            this.updateResourceType(values.id, values)
          } else {
            this.createResourceType(values)
          }
        }
      })
    },
    updateResourceType (id, data) {
      updateResourceTypeById(id, data)
        .then(res => {
          this.$message.success(`更新成功`)
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createResourceType (data) {
      addResourceType(data)
        .then(res => {
          this.$message.success(`添加成功`)
          this.handleOk()
          this.onClose()
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
