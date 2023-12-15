<template>
  <div class="ops-logout">
    <div
      class="ops-logout-box"
      v-if="_enable_list && _enable_list.length === 1 && time && !loading && !auth_auto_redirect"
    >
      <img src="../../assets/ops_logout.png" />
      <p v-if="_enable_list && _enable_list.length">
        <strong>您即将跳转至{{ _enable_list[0].auth_type }}</strong>
      </p>
      <p>
        <span style="color:#2f54eb">{{ time }}</span>
        秒后自动跳转
      </p>
      <a-space size="large">
        <a-button type="primary" @click="handleConfirm">确认</a-button>
        <a-button @click="handleCancel">取消</a-button>
      </a-space>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'Logout',
  data() {
    return {
      interval: null,
      time: 5,
      loading: false,
    }
  },
  computed: {
    ...mapState({ auth_enable: (state) => state?.user?.auth_enable ?? {} }),
    enable_list() {
      return this.auth_enable.enable_list ?? []
    },
    _enable_list() {
      return this.enable_list.filter((en) => en.auth_type !== 'LDAP')
    },
    auth_auto_redirect() {
      return this.auth_enable.auth_auto_redirect ?? 0
    },
  },
  watch: {
    time: {
      immediate: true,
      handler(newValue) {
        if (!newValue) {
          if (this.interval) {
            clearInterval(this.interval)
            this.interval = null
          }
          if (this._enable_list.length === 1) {
            this.Login({ userInfo: {}, auth_type: this._enable_list[0].auth_type })
          }
        }
      },
    },
  },
  async mounted() {
    this.loading = true
    await this.GetAuthDataEnable()
    this.loading = false
    if (!this._enable_list.length || this._enable_list.length > 1) {
      this.$router.push('/user/login')
    }
    if (this.auth_auto_redirect) {
      this.time = 0
    } else {
      this.time = 5
    }
    if (this.time) {
      this.interval = setInterval(() => {
        this.time--
      }, 1000)
    }
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval)
      this.interval = null
    }
  },
  methods: {
    ...mapActions(['Login', 'GetAuthDataEnable']),
    handleConfirm() {
      if (this._enable_list.length === 1) {
        this.Login({ userInfo: {}, auth_type: this._enable_list[0].auth_type })
      }
    },
    handleCancel() {
      this.$router.push('/user/login')
    },
  },
}
</script>

<style lang="less" scoped>
.ops-logout {
  background-color: #f0f5ff;
  width: 100%;
  height: 100%;
  position: relative;
  .ops-logout-box {
    width: 450px;
    height: 275px;
    border-radius: 12px;
    background-color: #fff;
    position: absolute;
    left: 50%;
    top: 30%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    img {
      width: 80%;
    }
  }
}
</style>
