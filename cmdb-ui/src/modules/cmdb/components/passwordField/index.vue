<template>
  <div>
    <span v-if="!isShow && !isTableLoading">{{ showPassword }}</span>
    <span v-else>{{ password }}</span>
    <a
      :style="{ marginLeft: '10px' }"
      @click="
        () => {
          isShow = !isShow
        }
      "
    ><a-icon
      :type="isShow ? 'eye-invisible' : 'eye'"
    /></a>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'PasswordField',
  props: {
    password: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      isShow: false,
    }
  },
  computed: {
    showPassword() {
      return '******'
    },
    ...mapState('cmdbStore', ['isTableLoading']),
  },
}
</script>

<style></style>
