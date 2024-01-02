<template>
  <CustomDrawer @close="handleClose" width="500" :title="title" :visible="visible" :closable="false">
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item :label="$t('acl.app')">
        <a-input v-decorator="['name', { rules: [{ required: true, message: $t('acl.appNameInput') }] }]"> </a-input>
      </a-form-item>
      <a-form-item :label="$t('desc')">
        <a-input v-decorator="['description', { rules: [{ required: true, message: $t('acl.descInput') }] }]">
        </a-input>
      </a-form-item>
      <a-form-item label="AppId">
        <a-input v-decorator="['app_id', { rules: [{ required: false }] }]" :disabled="mode === 'update'"> </a-input>
      </a-form-item>
      <a-form-item label="SecretKey">
        <a-input v-decorator="['secret_key', { rules: [{ required: false }] }]" :disabled="mode === 'update'">
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input v-decorator="['id']" type="hidden" />
      </a-form-item>
    </a-form>
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
      <a-button @click="handleSubmit" type="primary">{{ $t('submit') }}</a-button>
    </div>
  </CustomDrawer>
</template>
<script>
import { addApp, updateApp, getApp } from '@/modules/acl/api/app'

export default {
  name: 'AppForm',
  data() {
    return {
      visible: false,
      mode: 'create',
    }
  },
  computed: {
    title() {
      return this.$t('acl.addApp')
    },
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handleEdit(ele) {
      this.visible = true
      if (ele) {
        this.title = this.$t('updateApp')
        this.mode = 'update'
        console.log(ele)
        const { name, description } = ele
        getApp(ele.id).then((res) => {
          const { app_id, secret_key } = res
          this.$nextTick(() => {
            this.form.setFieldsValue({ name, description, app_id, secret_key, id: ele.id })
          })
        })
      } else {
        this.mode = 'create'
        this.title = this.$t('acl.addApp')
      }
    },
    handleClose() {
      this.visible = false
      this.form.resetFields()
    },
    async handleSubmit() {
      this.form.validateFields(async (err, values) => {
        if (err) {
          return
        }
        if (values.id) {
          await updateApp(values.id, values).then((res) => {
            this.$message.success(this.$t('updateSuccess'))
          })
        } else {
          await addApp(values).then((res) => {
            this.$message.success(this.$t('addSuccess'))
          })
        }
        this.handleClose()
        this.$emit('refresh')
      })
    },
  },
}
</script>
