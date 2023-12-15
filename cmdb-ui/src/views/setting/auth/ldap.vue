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
    <a-form-model-item
      label="服务器地址"
      prop="ldap_server"
      help="例如: 192.168.1.6 或者  ldap://192.168.1.6 或者 ldap://192.168.1.6:389"
    >
      <a-input v-model="form.ldap_server" placeholder="请输入服务器地址" />
    </a-form-model-item>
    <a-form-model-item label="域" prop="ldap_domain">
      <a-input v-model="form.ldap_domain" placeholder="请输入域" />
    </a-form-model-item>
    <SpanTitle>用户</SpanTitle>
    <a-form-model-item
      label="用户名称"
      prop="ldap_user_dn"
      help="用户dn: cn={},ou=users,dc=xxx,dc=com   {}会替换成用户名"
    >
      <a-input v-model="form.ldap_user_dn" placeholder="请输入用户名称" />
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
      },
      rules: {
        enable: [{ required: true }],
        ldap_server: [{ required: true, message: '请输入服务器地址' }],
      },
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
