<template>
  <a-form-model ref="form" :model="form" :label-col="labelCol" :wrapper-col="wrapperCol" :rules="rules">
    <SpanTitle>基本</SpanTitle>
    <a-form-model-item
      label="自动跳转到第三方登录页"
      prop="auto_redirect"
      help="如果关闭，则会弹出跳转到第三方登录页的确认，点取消按钮会进入系统内置的登录页"
    >
      <a-switch
        :checked="Boolean(form.auto_redirect)"
        @change="
          () => {
            $set(form, 'auto_redirect', Number(!form.auto_redirect))
          }
        "
      />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
import SpanTitle from '../components/spanTitle.vue'
export default {
  name: 'AuthCommonConfig',
  components: { SpanTitle },
  data() {
    return {
      labelCol: { span: 5 },
      wrapperCol: { span: 10 },
      form: {
        auto_redirect: 0,
      },
      rules: {
        auto_redirect: [{ required: true }],
      },
    }
  },
  methods: {
    setData(data) {
      if (data) {
        this.form = data
      } else {
        this.form = { auto_redirect: 0 }
      }
    },
    getData(callback) {
      this.$refs.form.validate((valid) => {
        if (valid) {
          callback(this.form)
        }
      })
    },
  },
}
</script>

<style></style>
