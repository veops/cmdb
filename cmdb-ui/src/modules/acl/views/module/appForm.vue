<template>
  <CustomDrawer @close="handleClose" width="500" :title="title" :visible="visible" :closable="false">
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item label="应用名称">
        <a-input v-decorator="['name', { rules: [{ required: true, message: '请输入应用名称' }] }]"> </a-input>
      </a-form-item>
      <a-form-item label="描述">
        <a-input v-decorator="['description', { rules: [{ required: true, message: '请输入描述' }] }]"> </a-input>
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
      <a-button @click="handleClose">取消</a-button>
      <a-button @click="handleSubmit" type="primary">提交</a-button>
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
      title: '创建应用',
      mode: 'create',
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handleEdit(ele) {
      this.visible = true
      if (ele) {
        this.title = '修改应用'
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
        this.title = '创建应用'
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
            this.$message.success('修改成功！')
          })
        } else {
          await addApp(values).then((res) => {
            this.$message.success('创建成功!')
          })
        }
        this.handleClose()
        this.$emit('refresh')
      })
    },
  },
}
</script>
