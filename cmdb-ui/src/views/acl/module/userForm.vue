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
        label="用户名(英文)"
      >
        <a-input
          name="username"
          placeholder="英文名"
          v-decorator="['username', {rules: [{ required: true, message: '请输入用户名'}]} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="中文名"
      >
        <a-input
          name="nickname"
          v-decorator="['nickname', {rules: []} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="密码"
      >
        <a-input
          type="password"
          name="password"
          v-decorator="['password', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="部门"
      >
        <a-input
          name="department"
          v-decorator="['department', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="小组"
      >
        <a-input
          name="catalog"
          v-decorator="['catalog', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="邮箱"
      >
        <a-input
          name="email"
          v-decorator="[
            'email',
            {
              rules: [
                {
                  type: 'email',
                  message: '请输入正确的邮箱！',
                },
                {
                  required: true,
                  message: '请输入邮箱',
                },
              ],
            },
          ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="手机号码"
      >
        <a-input
          name="mobile"
          v-decorator="['mobile', {rules: [{message: '请输入正确的手机号码', pattern: /^1\d{10}$/ }]} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        label="是否锁定"
      >
        <a-switch
          @change="onChange"
          name="block"
          v-decorator="['block', {rules: [], valuePropName: 'checked',} ]"
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
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('button.submit') }}</a-button>
        <a-button @click="onClose">{{ $t('button.cancel') }}</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { addUser, updateUserById } from '@/api/acl/user'

export default {
  name: 'AttributeForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: '新增用户',
      drawerVisible: false,
      formLayout: 'vertical'
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
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.uid,
          username: record.username,
          nickname: record.nickname,
          password: record.password,
          department: record.department,
          catalog: record.catalog,
          email: record.email,
          mobile: record.mobile,
          block: record.block
        })
      })
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          if (values.id) {
            this.updateUser(values.id, values)
          } else {
            this.createUser(values)
          }
        }
      })
    },
    updateUser (attrId, data) {
      updateUserById(attrId, data)
        .then(res => {
          this.$message.success(`更新成功`)
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createUser (data) {
      addUser(data)
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
