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
    <a-form-model-item :label="$t('cs.auth.cas.server')" prop="cas_server" :help="$t('cs.auth.cas.serverHelp')">
      <a-input v-model="form.cas_server" :placeholder="$t('cs.auth.cas.serverPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.validateServer')" prop="cas_validate_server" :help="$t('cs.auth.cas.validateServerHelp')">
      <a-input v-model="form.cas_validate_server" :placeholder="$t('cs.auth.cas.validateServerPlaceholder')" />
    </a-form-model-item>
    <SpanTitle>{{ $t('cs.auth.other') }}</SpanTitle>
    <a-form-model-item :label="$t('cs.auth.cas.loginRoute')" prop="cas_login_route">
      <a-input v-model="form.cas_login_route" placeholder="/cas/built-in/cas/login" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.logoutRoute')" prop="cas_logout_route">
      <a-input v-model="form.cas_logout_route" placeholder="/cas/built-in/cas/logout" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.validateRoute')" prop="cas_validate_route">
      <a-input v-model="form.cas_validate_route" placeholder="/cas/built-in/cas/serviceValidate" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.afterLoginRoute')" prop="cas_after_login">
      <a-input v-model="form.cas_after_login" :placeholder="$t('cs.auth.cas.afterLoginRoutePlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.cas.userMap')" prop="cas_user_map" :wrapper-col="{ span: 15 }">
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
      isJsonRight: true,
    }
  },
  computed: {
    rules() {
      return {
        enable: [{ required: true }],
        cas_server: [{ required: true, message: this.$t('cs.auth.cas.serverPlaceholder') }],
        cas_login_route: [{ required: true, message: this.$t('cs.auth.cas.loginRoutePlaceholder') }],
        cas_logout_route: [{ required: true, message: this.$t('cs.auth.cas.logoutRoutePlaceholder') }],
        cas_validate_route: [{ required: true, message: this.$t('cs.auth.cas.validateRoutePlaceholder') }],
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
