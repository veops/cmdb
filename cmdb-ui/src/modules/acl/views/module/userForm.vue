<template>
  <CustomDrawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="500px"
  >
    <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item :label="$t('acl.username')">
        <a-input
          name="username"
          :placeholder="$t('acl.username_placeholder')"
          v-decorator="['username', { rules: [{ required: true, message: $t('acl.username_placeholder') }] }]"
        />
      </a-form-item>
      <a-form-item :label="$t('acl.nickname')">
        <a-input
          name="nickname"
          :placeholder="$t('acl.nickname_placeholder')"
          v-decorator="['nickname', { rules: [] }]"
        />
      </a-form-item>
      <a-form-item :label="$t('acl.password')">
        <a-input
          type="password"
          name="password"
          :placeholder="$t('acl.password_placeholder')"
          v-decorator="['password', { rules: [{ required: true, message: $t('acl.password_placeholder') }] }]"
        />
      </a-form-item>

      <a-form-item :label="$t('acl.department')">
        <a-input name="department" v-decorator="['department', { rules: [] }]" />
      </a-form-item>

      <a-form-item :label="$t('acl.group')">
        <a-input name="catalog" v-decorator="['catalog', { rules: [] }]" />
      </a-form-item>

      <a-form-item :label="$t('acl.email')">
        <a-input
          name="email"
          v-decorator="[
            'email',
            {
              rules: [
                {
                  type: 'email',
                  message: $t('acl.email_placeholder'),
                },
                {
                  required: true,
                  message: $t('acl.email_placeholder'),
                },
              ],
            },
          ]"
        />
      </a-form-item>

      <a-form-item :label="$t('acl.mobile')">
        <a-input
          name="mobile"
          v-decorator="['mobile', { rules: [{ message: $t('acl.mobileTips'), pattern: /^1\d{10}$/ }] }]"
        />
      </a-form-item>

      <a-form-item :label="$t('acl.isBlock')">
        <a-switch @change="onChange" name="block" v-decorator="['block', { rules: [], valuePropName: 'checked' }]" />
      </a-form-item>

      <a-form-item>
        <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
      </a-form-item>

      <div class="custom-drawer-bottom-action">
        <a-button @click="onClose">{{ $t('cancel') }}</a-button>
        <a-button @click="handleSubmit" type="primary">{{ $t('confirm') }}</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>

<script>
import { addUser, updateUserById } from '@/modules/acl/api/user'

export default {
  name: 'AttributeForm',
  data() {
    return {
      drawerVisible: false,
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  computed: {
    drawerTitle() {
      return this.$t('acl.addUser')
    },
  },
  mounted() {},
  methods: {
    handleCreate() {
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
    },
    onChange(e) {
      console.log(`checked = ${e}`)
    },

    handleEdit(record) {
      this.drawerVisible = true
      console.log(record)
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
          block: record.block,
        })
      })
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)

          if (values.id) {
            this.updateUser(values.id, values)
          } else {
            this.createUser(values)
          }
        }
      })
    },
    updateUser(attrId, data) {
      updateUserById(attrId, data).then((res) => {
        this.$message.success(this.$t('updateSuccess'))
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },

    createUser(data) {
      addUser(data).then((res) => {
        this.$message.success(this.$t('addSuccess'))
        this.handleOk()
        this.onClose()
      })
    },
  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null,
    },
  },
}
</script>

<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}

.fold {
  width: calc(100% - 216px);
  display: inline-block;
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
