<template>
  <a-drawer
    ref="customDrawer"
    v-bind="$attrs"
    v-on="$listeners"
    :closable="false"
    :placement="placement"
    :bodyStyle="{ maxHeight: bodyMaxHeight, overflow: 'auto', ...$attrs.bodyStyle }"
    :keyboard="false"
  >
    <div v-if="closable" :class="`custom-drawer-close custom-drawer-${placement}`" @click="clickCustomClose">
      <a-icon :type="closeIconType" />
    </div>
    <template v-if="hasTitle" slot="title">
      <slot name="title">{{ title }}</slot>
    </template>
    <slot></slot>
  </a-drawer>
</template>

<script>
export default {
  name: 'CustomDrawer',
  components: {},
  props: {
    closable: {
      type: Boolean,
      default: true,
    },
    placement: {
      type: String,
      default: 'right',
    },
    hasTitle: {
      type: Boolean,
      default: true,
    },
    hasFooter: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      default: '',
    },
  },
  computed: {
    closeIconType() {
      if (this.placement === 'top') return 'up'
      if (this.placement === 'bottom') return 'down'
      return this.placement || 'right'
    },
    customClass() {
      if (!this.placement) return 'right'
      return this.placement
    },
    bodyMaxHeight() {
      const titleHeight = this.hasTitle ? 55 : 0
      const footerHeight = this.hasFooter ? 53 : 0
      return `calc(100vh - ${titleHeight + footerHeight}px)`
    },
  },
  methods: {
    clickCustomClose() {
      this.$refs.customDrawer.close()
    },
  },
}
</script>

<style lang="less">

.custom-drawer-close {
  position: absolute;
  cursor: pointer;
  background: #custom_colors[color_1];
  color: white;
  text-align: center;
  transition: all 0.3s;
  z-index: 1;
  &:hover {
    background: #597ef7;
  }
}
.custom-drawer-right,
.custom-drawer-left {
  width: 14px;
  height: 50px;
  top: 50%;
  transform: translateY(-50%);
  line-height: 50px;
}
.custom-drawer-left {
  right: 0;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.custom-drawer-right {
  left: 0;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}
.custom-drawer-top,
.custom-drawer-bottom {
  width: 50px;
  height: 14px;
  left: 50%;
  transform: translateX(-50%);
  line-height: 14px;
}
.custom-drawer-top {
  bottom: 0;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
.custom-drawer-bottom {
  top: 0;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
</style>
