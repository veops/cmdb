<template>
  <a-form-model ref="form" :model="form" :label-col="labelCol" :wrapper-col="wrapperCol" :rules="rules">
    <SpanTitle>基本</SpanTitle>
    <a-form-model-item label="是否启用" prop="enable">
      <a-switch
        :checked="Boolean(form.enable)"
        @change="
          () => {
            $set(form, 'enable', Number(!form.enable))
          }
        "
      />
    </a-form-model-item>
    <a-form-model-item label="服务端地址" prop="cas_server" help="不包括url path，例如https://xxx.com">
      <a-input v-model="form.cas_server" placeholder="请输入服务端地址" />
    </a-form-model-item>
    <a-form-model-item label="验证服务端地址" prop="cas_validate_server" help="不包括url path，例如https://xxx.com">
      <a-input v-model="form.cas_validate_server" placeholder="请输入验证服务端地址" />
    </a-form-model-item>
    <SpanTitle>其他</SpanTitle>
    <a-form-model-item label="登录路由" prop="cas_login_route">
      <a-input v-model="form.cas_login_route" placeholder="/cas/built-in/cas/login" />
    </a-form-model-item>
    <a-form-model-item label="注销路由" prop="cas_logout_route">
      <a-input v-model="form.cas_logout_route" placeholder="/cas/built-in/cas/logout" />
    </a-form-model-item>
    <a-form-model-item label="验证路由" prop="cas_validate_route">
      <a-input v-model="form.cas_validate_route" placeholder="/cas/built-in/cas/serviceValidate" />
    </a-form-model-item>
    <a-form-model-item label="重定向路由" prop="cas_after_login">
      <a-input v-model="form.cas_after_login" placeholder="请输入重定向路由" />
    </a-form-model-item>
    <a-form-model-item label="用户属性映射" prop="cas_user_map" :wrapper-col="{ span: 15 }">
      <vue-json-editor
        :style="{ '--custom-height': `${200}px` }"
        v-model="form.cas_user_map"
        :showBtns="false"
        mode="code"
        lang="zh"
        @json-change="onJsonChange"
        @has-error="onJsonError"
      />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
import _ from 'lodash'
import vueJsonEditor from 'vue-json-editor'
import SpanTitle from '../components/spanTitle.vue'
export default {
  name: 'CAS',
  components: { SpanTitle, vueJsonEditor },
  data() {
    const defaultForm = {
      enable: 0,
      cas_server: '',
      cas_validate_server: '',
      cas_login_route: '',
      cas_logout_route: '',
      cas_validate_route: '',
      cas_after_login: '/',
      cas_user_map: {
        username: { tag: 'cas:user' },
        nickname: { tag: 'cas:attribute', attrs: { name: 'displayName' } },
        email: { tag: 'cas:attribute', attrs: { name: 'email' } },
        mobile: { tag: 'cas:attribute', attrs: { name: 'phone' } },
        avatar: { tag: 'cas:attribute', attrs: { name: 'avatar' } },
      },
    }
    return {
      defaultForm,
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      form: _.cloneDeep(defaultForm),
      rules: {
        enable: [{ required: true }],
        cas_server: [{ required: true, message: '请输入服务端地址' }],
        cas_login_route: [{ required: true, message: '请输入登录路由' }],
        cas_logout_route: [{ required: true, message: '请输入注销路由' }],
        cas_validate_route: [{ required: true, message: '请输入验证路由' }],
      },
      isJsonRight: true,
    }
  },
  methods: {
    setData(data) {
      if (data) {
        this.form = data
      } else {
        this.form = _.cloneDeep(this.defaultForm)
      }
    },
    getData(callback) {
      this.$refs.form.validate((valid) => {
        if (valid && this.isJsonRight) {
          callback(this.form)
        }
      })
    },
    onJsonChange(value) {
      this.isJsonRight = true
    },
    onJsonError() {
      this.isJsonRight = false
    },
  },
}
</script>

<style></style>
