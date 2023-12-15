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
    <a-form-model-item label="客户端ID" prop="client_id">
      <a-input v-model="form.client_id" placeholder="请输入客户端ID" />
    </a-form-model-item>
    <a-form-model-item label="客户端密钥" prop="client_secret">
      <a-input v-model="form.client_secret" placeholder="请输入客户端密钥" />
    </a-form-model-item>
    <a-form-model-item label="授权链接" prop="authorize_url">
      <a-input v-model="form.authorize_url" placeholder="请输入授权链接" />
    </a-form-model-item>
    <a-form-model-item label="令牌链接" prop="token_url">
      <a-input v-model="form.token_url" placeholder="请输入令牌链接" />
    </a-form-model-item>
    <SpanTitle>其他</SpanTitle>
    <a-form-model-item label="用户信息" prop="user_info" :wrapper-col="{ span: 15 }">
      <vue-json-editor
        :style="{ '--custom-height': `${200}px` }"
        v-model="form.user_info"
        :showBtns="false"
        mode="code"
        lang="zh"
        @json-change="onJsonChange"
        @has-error="onJsonError"
      />
    </a-form-model-item>
    <a-form-model-item label="范围" prop="scopes">
      <a-select mode="tags" v-model="form.scopes" placeholder="请输入范围" />
    </a-form-model-item>
    <a-form-model-item label="重定向路由" prop="after_login">
      <a-input v-model="form.after_login" placeholder="请输入重定向路由" />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
import _ from 'lodash'
import vueJsonEditor from 'vue-json-editor'
import SpanTitle from '../components/spanTitle.vue'
export default {
  name: 'OAUTH2',
  components: { SpanTitle, vueJsonEditor },
  props: {
    data_type: {
      type: String,
      default: 'OAUTH2',
    },
  },
  data() {
    const defaultForm = {
      enable: 0,
      client_id: '',
      client_secret: '',
      authorize_url: '',
      token_url: '',
      user_info: {
        url: 'https://{your-OAuth2Server-hostname}/api/userinfo',
        email: 'email',
        username: 'name',
        avatar: 'picture',
      },
      scopes: this.data_type === 'OAUTH2' ? ['profile', 'email'] : ['profile', 'email', 'openId'],
      after_login: '/',
    }
    return {
      defaultForm,
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      form: _.cloneDeep(defaultForm),
      rules: {
        enable: [{ required: true }],
        client_id: [{ required: true, message: '请输入客户端ID' }],
        client_secret: [{ required: true, message: '请输入客户端密钥' }],
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
