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
        :label="$t('acl.username')"
      >
        <a-input
          name="username"
          :placeholder="$t('acl.username')"
          v-decorator="['username', {rules: [{ required: true, message: $t('acl.usernameRequired')}]} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.nickname')"
      >
        <a-input
          name="nickname"
          v-decorator="['nickname', {rules: []} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.password')"
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
        :label="$t('acl.department')"
      >
        <a-input
          name="department"
          v-decorator="['department', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.catalog')"
      >
        <a-input
          name="catalog"
          v-decorator="['catalog', {rules: []} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.email')"
      >
        <a-input
          name="email"
          v-decorator="[
            'email',
            {
              rules: [
                {
                  type: 'email',
                  message: $t('acl.emailValidate'),
                },
                {
                  required: true,
                  message: $t('acl.emailRequired'),
                },
              ],
            },
          ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.mobile')"
      >
        <a-input
          name="mobile"
          v-decorator="['mobile', {rules: [{message: $t('acl.mobileValidate'), pattern: /^1\d{10}$/ }]} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="horizontalFormItemLayout.labelCol"
        :wrapper-col="horizontalFormItemLayout.wrapperCol"
        :label="$t('acl.block')"
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
      drawerTitle: this.$t('acl.newUser'),
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
          this.$message.success(this.$t('tip.updateSuccess'))
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createUser (data) {
      addUser(data)
        .then(res => {
          this.$message.success(this.$t('tip.addSuccess'))
          this.handleOk()
          this.onClose()
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
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
