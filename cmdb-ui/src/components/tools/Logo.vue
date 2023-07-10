<template>
  <div class="logo">
    <img
      @click="jumpTo"
      v-if="showTitle && !collapsed"
      style="width: 100%; height: 100%; cursor: pointer"
      :src="file_name ? `/api/common-setting/v1/file/${file_name}` : require('@/assets/logo_VECMDB.png')"
    />
    <img
      @click="jumpTo"
      v-else
      style="width: 32px; height: 32px; margin-left: 24px; cursor: pointer"
      :src="small_file_name ? `/api/common-setting/v1/file/${small_file_name}` : require('@/assets/logo.png')"
    />
    <!-- <logo-svg/> -->
    <!-- <img v-if="showTitle" style="width:92px;height: 32px" src="@/assets/OneOps.png" /> -->
    <!-- <h1 v-if="showTitle">{{ title }}</h1> -->
  </div>
</template>

<script>
// import LogoSvg from '@/assets/logo.svg?inline'
import { mapState } from 'vuex'
export default {
  name: 'Logo',
  components: {
    // LogoSvg,
  },
  computed: {
    ...mapState({
      file_name: (state) => state.logo.file_name,
      small_file_name: (state) => state.logo.small_file_name,
    }),
  },
  props: {
    title: {
      type: String,
      default: 'OneOps',
      required: false,
    },
    showTitle: {
      type: Boolean,
      default: true,
      required: false,
    },
    collapsed: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    jumpTo() {
      if (this.$route.path !== '/cmdb/dashboard') {
        this.$router.push('/cmdb/dashboard')
      }
    },
  },
}
</script>
