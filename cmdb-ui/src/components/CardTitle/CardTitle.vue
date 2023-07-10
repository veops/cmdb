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
  border-top-left-radius: 15px;
  font-size: 1vw;
  height: 2.2vw;
  color: #011d93;
  background: linear-gradient(270deg, rgba(206, 226, 255, 0) -6.74%, #d2e4ff 96.74%);
  padding: 5px 10px;
  display: inline-block;
  font-weight: 500;
}
</style>
