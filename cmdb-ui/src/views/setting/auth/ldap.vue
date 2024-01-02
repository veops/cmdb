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
    <a-form-model-item
      :label="$t('cs.auth.ldap.serverAddress')"
      prop="ldap_server"
      :help="$t('cs.auth.ldap.serverAddressHelp')"
    >
      <a-input v-model="form.ldap_server" :placeholder="$t('cs.auth.ldap.serverAddressPlaceholder')" />
    </a-form-model-item>
    <a-form-model-item :label="$t('cs.auth.ldap.domain')" prop="ldap_domain">
      <a-input v-model="form.ldap_domain" :placeholder="$t('cs.auth.ldap.domainPlaceholder')" />
    </a-form-model-item>
    <SpanTitle>{{ $t('cs.auth.ldap.user') }}</SpanTitle>
    <a-form-model-item
      :label="$t('cs.auth.ldap.username')"
      prop="ldap_user_dn"
      :help="$t('cs.auth.ldap.userHelp')"
    >
      <a-input v-model="form.ldap_user_dn" :placeholder="$t('cs.auth.ldap.userPlaceholder')" />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
import SpanTitle from '../components/spanTitle.vue'
export default {
  name: 'LDAP',
  components: { SpanTitle },
  data() {
    return {
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      form: {
        enable: 0,
        ldap_server: '',
        ldap_domain: '',
        ldap_user_dn: 'cn={},ou=users,dc=xxx,dc=com',
      }
    }
  },
  computed: {
    rules() {
      return {
        enable: [{ required: true }],
        ldap_server: [{ required: true, message: this.$t('cs.auth.ldap.domainPlaceholder') }],
      }
    }
  },
  methods: {
    setData(data) {
      if (data) {
        this.form = { ...data }
      } else {
        this.form = {
          enable: 0,
          ldap_server: '',
          ldap_domain: '',
          ldap_user_dn: 'cn={},ou=users,dc=xxx,dc=com',
        }
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
