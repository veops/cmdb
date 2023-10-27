<template>
  <div>
    <span v-if="!isShow && !isTableLoading">{{ showPassword }}</span>
    <span v-else>{{ password }}</span>
    <a :style="{ marginLeft: '10px' }" @click="getPassword"><a-icon :type="isShow ? 'eye-invisible' : 'eye'"/></a>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getAttrPassword } from '../../api/CITypeAttr'
export default {
  name: 'PasswordField',
  props: {
    ci_id: {
      type: Number,
      default: 0,
    },
    attr_id: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      isShow: false,
      password: '',
    }
  },
  computed: {
    showPassword() {
      return '******'
    },
    ...mapState('cmdbStore', ['isTableLoading']),
  },
  methods: {
    getPassword() {
      if (this.isShow) {
        this.isShow = false
      } else {
        getAttrPassword(this.ci_id, this.attr_id).then((res) => {
          this.password = res.value
          this.isShow = true
        })
      }
    },
  },
}
</script>

<style></style>
