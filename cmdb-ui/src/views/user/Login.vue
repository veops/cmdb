<template>
  <div class="ops-login">
    <div class="ops-login-left">
      <span>维易科技<br />让运维更简单</span>
    </div>
    <div class="ops-login-right">
      <img src="../../assets/logo_VECMDB.png" />
      <a-form
        id="formLogin"
        ref="formLogin"
        :form="form"
        @submit="handleSubmit"
        hideRequiredMark
        :colon="false">
        <a-form-item label="用户名/邮箱">
          <a-input
            size="large"
            type="text"
            class="ops-input"
            v-decorator="[
              'username',
              {
                rules: [{ required: true, message: '请输入用户名或邮箱' }, { validator: handleUsernameOrEmail }],
                validateTrigger: 'change',
              },
            ]"
          >
          </a-input>
        </a-form-item>

        <a-form-item label="密码">
          <a-input
            size="large"
            type="password"
            autocomplete="false"
            class="ops-input"
            v-decorator="['password', { rules: [{ required: true, message: '请输入密码' }], validateTrigger: 'blur' }]"
          >
          </a-input>
        </a-form-item>

        <a-form-item>
          <a-checkbox v-decorator="['rememberMe', { valuePropName: 'checked' }]">自动登录</a-checkbox>
        </a-form-item>

        <a-form-item style="margin-top: 24px">
          <a-button
            size="large"
            type="primary"
            htmlType="submit"
            class="login-button"
            :loading="state.loginBtn"
            :disabled="state.loginBtn"
          >确定</a-button
          >
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script>
import md5 from 'md5'
import { mapActions } from 'vuex'
import { timeFix } from '@/utils/util'
import appConfig from '@/config/app.js'

export default {
  data() {
    return {
      customActiveKey: 'tab1',
      loginBtn: false,
      // login type: 0 email, 1 username, 2 telephone
      loginType: 0,
      requiredTwoStepCaptcha: false,
      stepCaptchaVisible: false,
      form: this.$form.createForm(this),
      state: {
        time: 60,
        loginBtn: false,
        // login type: 0 email, 1 username, 2 telephone
        loginType: 0,
        smsSendBtn: false,
      },
    }
  },
  created() {},
  methods: {
    ...mapActions(['Login', 'Logout']),
    // handler
    handleUsernameOrEmail(rule, value, callback) {
      const { state } = this
      const regex = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
      if (regex.test(value)) {
        state.loginType = 0
      } else {
        state.loginType = 1
      }
      callback()
    },
    handleSubmit(e) {
      e.preventDefault()
      const {
        form: { validateFields },
        state,
        customActiveKey,
        Login,
      } = this

      state.loginBtn = true

      const validateFieldsKey = customActiveKey === 'tab1' ? ['username', 'password'] : ['mobile', 'captcha']

      validateFields(validateFieldsKey, { force: true }, (err, values) => {
        if (!err) {
          console.log('login form', values)
          const loginParams = { ...values }
          delete loginParams.username
          loginParams[!state.loginType ? 'email' : 'username'] = values.username
          loginParams.password = appConfig.useEncryption?md5(values.password):values.password
          Login(loginParams)
            .then((res) => this.loginSuccess(res))
            .finally(() => {
              state.loginBtn = false
            })
        } else {
          setTimeout(() => {
            state.loginBtn = false
          }, 600)
        }
      })
    },

    loginSuccess(res) {
      console.log(res)
      this.$router.push({ path: this.$route.query.redirect })
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: '欢迎',
          description: `${timeFix()}，欢迎回来`,
        })
      }, 1000)
    },
  },
}
</script>

<style lang="less" scoped>
.ops-login {
  width: 100%;
  height: 100%;
  display: flex;
  min-width: 1000px;
  overflow-x: auto;
  .ops-login-left {
    position: relative;
    width: 50%;
    background: url('../../assets/login_bg.png') no-repeat;
    background-position: center;
    background-size: cover;
    > span {
      color: white;
      position: absolute;
      top: 10%;
      left: 50%;
      transform: translateX(-50%);
      font-size: 1.75vw;
      text-align: center;
    }
  }
  .ops-login-right {
    width: 50%;
    position: relative;
    padding: 10%;
    > img {
      width: 70%;
      margin-left: 15%;
    }
    .login-button {
      width: 100%;
    }
  }
}
</style>
