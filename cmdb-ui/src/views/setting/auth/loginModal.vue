<template>
  <a-modal :visible="visible" @cancel="handleCancel" @ok="handleOK">
    <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }">
      <a-form-item :label="$t('cs.auth.usernameOrEmail')">
        <a-input
          v-decorator="[
            'username',
            {
              rules: [{ required: true, message: $t('cs.auth.usernameOrEmailPlaceholder') }],
              validateTrigger: 'change',
            },
          ]"
        >
        </a-input>
      </a-form-item>
      <a-form-item :label="$t('cs.auth.password')">
        <a-input
          type="password"
          autocomplete="false"
          v-decorator="['password', { rules: [{ required: true, message: $t('cs.auth.passwordPlaceholder') }], validateTrigger: 'blur' }]"
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
