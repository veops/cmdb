<template>
  <div class="ops-card-title">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'CardTitle',
}
</script>

<style lang="less" scoped>
.ops-card-title {
  border-top-left-radius: 3px;
  font-size: 16px;
  height: 42px;
  line-height: 42px;
  color: @primary-color;
  background: linear-gradient(270deg, #fff -6.74%, fade(@primary-color, 8%) 96.74%);
  padding: 0 20px;
  display: inline-block;
  font-weight: 600;
}
</style>
