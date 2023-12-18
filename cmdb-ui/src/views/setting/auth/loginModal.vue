<template>
  <a-modal :visible="visible" @cancel="handleCancel" @ok="handleOK">
    <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }">
      <a-form-item label="用户名/邮箱">
        <a-input
          v-decorator="[
            'username',
            {
              rules: [{ required: true, message: '请输入用户名或邮箱' }],
              validateTrigger: 'change',
            },
          ]"
        >
        </a-input>
      </a-form-item>
      <a-form-item label="密码">
        <a-input
          type="password"
          autocomplete="false"
          v-decorator="['password', { rules: [{ required: true, message: '请输入密码' }], validateTrigger: 'blur' }]"
        >
        </a-input>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

  <script>
  export default {
    name: 'LoginModal',
    data() {
      return {
        visible: false,
        form: this.$form.createForm(this),
      }
    },
    methods: {
      open() {
        this.visible = true
      },
      handleCancel() {
        this.visible = false
      },
      handleOK() {
        this.form.validateFields((err, values) => {
          if (!err) {
            this.$emit('handleOK', values)
            this.handleCancel()
          }
        })
      },
    },
  }
  </script>

  <style></style>
