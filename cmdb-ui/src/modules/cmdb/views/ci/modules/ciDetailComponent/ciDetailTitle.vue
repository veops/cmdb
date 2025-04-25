<template>
  <div class="ci-detail-title">
    <CIIcon :icon="icon" size="20" />
    <span class="ci-detail-title-text">{{ title }}</span>
  </div>
</template>

<script>
import CIIcon from '@/modules/cmdb/components/ciIcon'

export default {
  name: 'CIDetailTitle',
  components: {
    CIIcon
  },
  props: {
    ci: {
      type: Object,
      default: () => {}
    },
    ci_types: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      icon: '',
      title: ''
    }
  },
  computed: {
    findCIType() {
      return this.ci_types?.find?.((item) => item?.id === this.ci?._type) || {}
    }
  },
  watch: {
    findCIType: {
      deep: true,
      immediate: true,
      handler(val) {
        this.icon = val?.icon || ''
        this.title = this?.ci?.[val?.show_name] || this?.ci?.[val?.unique_key] || ''
      },
    }
  }
}
</script>

<style lang="less" scoped>
.ci-detail-title {
  display: flex;
  align-items: center;
  width: 100%;
  column-gap: 9px;

  &-text {
    width: 100%;
    font-size: 16px;
    font-weight: 700;
    color: @text-color_1;
  }
}
</style>
