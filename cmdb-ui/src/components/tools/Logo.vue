<template>
  <div class="logo">
    <img
      @click="jumpTo"
      v-if="showTitle && !collapsed"
      style="width: 100%; height: 100%; cursor: pointer"
      :src="require('@/assets/logo_VECMDB.png')"
    />
    <img
      @click="jumpTo"
      v-else
      style="width: 32px; height: 32px; margin-left: 24px; cursor: pointer"
      :src="require('@/assets/logo.png')"
    />
  </div>
</template>

<script>
export default {
  name: 'Logo',
  components: {},
  computed: {},
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
