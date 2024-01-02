<template>
  <a-form-model ref="form" :model="form" :label-col="labelCol" :wrapper-col="wrapperCol" :rules="rules">
    <SpanTitle>{{ $t('cs.auth.basic') }}</SpanTitle>
    <a-form-model-item :label="$t('cs.auth.isEnable')" prop="enable">
      <a-switch
        :checked="Boolean(form.enable)"
        @change="
          () => {
            $set(form, 'enable', Number(!form.enable))
          }
        "
      />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.oauth2.clientId')" prop="client_id">
      <a-input v-model="form.client_id" :placeholder="$t('cs.auth.oauth2.clientIdPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.oauth2.clientSecret')" prop="client_secret">
      <a-input v-model="form.client_secret" :placeholder="$t('cs.auth.oauth2.clientSecretPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.oauth2.authorizeUrl')" prop="authorize_url">
      <a-input v-model="form.authorize_url" :placeholder="$t('cs.auth.oauth2.authorizeUrlPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.oauth2.tokenUrl')" prop="token_url">
      <a-input v-model="form.token_url" :placeholder="$t('cs.auth.oauth2.tokenUrlPlaceholder')" />
    </a-form-model-item>
    <SpanTitle>其他</SpanTitle>
    <a-form-model-item :label="$t('cs.auth.oauth2.userInfo')" prop="user_info" :wrapper-col="{ span: 15 }">
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
    <a-form-model-item :label="$t('cs.auth.oauth2.scopes')" prop="scopes">
      <a-select mode="tags" v-model="form.scopes" :placeholder="$t('cs.auth.oauth2.scopesPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.afterLoginRoute')" prop="after_login">
      <a-input v-model="form.after_login" :placeholder="$t('cs.auth.cas.afterLoginRoutePlaceholder')" />
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
      isJsonRight: true,
    }
  },
  computed: {
    rules() {
      return {
        enable: [{ required: true }],
        client_id: [{ required: true, message: this.$t('cs.auth.oauth2.clientIdPlaceholder') }],
        client_secret: [{ required: true, message: this.$t('cs.auth.oauth2.clientSecretPlaceholder') }],
      }
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
