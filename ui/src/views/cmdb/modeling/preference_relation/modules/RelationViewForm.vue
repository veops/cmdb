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
        label="关系视图名"
      >
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', {rules: [{ required: true, message: '请输入 关系视图名'}]} ]"
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
import { subscribeRelationView } from '@/api/cmdb/preference'

export default {
  name: 'RelationViewForm',
  data () {
    return {
      drawerTitle: '新增关系视图',
      drawerVisible: false,
      formLayout: 'vertical',
      crIds: []
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
  methods: {
    handleCreate (crIds) {
      this.crIds = crIds
      this.drawerVisible = true
    },
    onClose () {
      this.form.resetFields()
      this.drawerVisible = false
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.createRelationView(values)
        }
      })
    },

    createRelationView (data) {
      data.cr_ids = this.crIds
      subscribeRelationView(data)
        .then(res => {
          this.$message.success(`添加成功`)
          this.onClose()
          this.$emit('refresh')
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      console.log(err, 'error')
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
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
