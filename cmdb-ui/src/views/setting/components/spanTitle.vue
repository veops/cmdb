<template>
  <a-row>
    <a-col :span="span">
      <div class="ops-setting-spantitle"><slot></slot></div>
    </a-col>
  </a-row>
</template>

<script>
export default {
  name: 'SpanTitle',
  props: {
    span: {
      type: Number,
      default: 3,
    },
  },
}
</script>

<style lang="less" scoped>
.ops-setting-spantitle {
  height: 28px;
  margin-bottom: 12px;
  line-height: 28px;
  padding-left: 12px;
  font-weight: 700;
  color: #000;
  border-left: 3px solid @primary-color;
}
</style>
