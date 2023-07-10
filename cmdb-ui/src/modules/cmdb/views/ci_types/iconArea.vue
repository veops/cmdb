<template>
  <div class="icon-area">
    <div class="icon-area-item">
      <span :style="{ marginRight: '15px' }"></span>
      <CustomIconSelect v-model="customIcon" />
    </div>
  </div>
</template>

<script>
import CustomIconSelect from '@/components/CustomIconSelect'

export default {
  name: 'IconArea',
  components: { CustomIconSelect },
  data() {
    return {
      customIcon: { name: '', color: '' },
    }
  },
  methods: {
    getIcon() {
      if (this.customIcon.name) {
        return this.customIcon
      }
      return undefined
    },
    setIcon(icon) {
      if (icon && icon.name) {
        this.customIcon = { ...icon }
      } else {
        this.customIcon = { name: '', color: '' }
      }
    },
  },
}
</script>

<style lang="less" scoped>
.icon-area {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  .icon-area-item {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    > span {
      font-size: 10px;
    }
  }
}
</style>
