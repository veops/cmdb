<template>
  <div>
    <span v-if="!isShow">{{ showPassword }}</span>
    <span v-else>{{ password }}</span>
    <a
      class="password-eye"
      @click="switchPassword"
    >
      <a-icon :type="isShow ? 'eye-invisible' : 'eye'"/>
    </a>
  </div>
</template>

<script>
export default {
  name: 'PasswordField',
  props: {
    password: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      isShow: false,
      showPassword: '******',
    }
  },
  methods: {
    switchPassword() {
      this.isShow = !this.isShow
    },
  },
}
</script>

<style lang="less" scoped>
.password-eye {
  margin-left: 10px
}
</style>
