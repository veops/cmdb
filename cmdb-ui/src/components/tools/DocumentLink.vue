<template>
  <a-tooltip>
    <template slot="title">文档中心</template>
    <span class="document-link">
      <a-icon type="question-circle" @click="handleClick" />
    </span>
  </a-tooltip>
</template>
<script>
export default {
  name: 'DocumentLink',
  data() {
    return {}
  },
  methods: {
    handleClick() {
      window.open(`${location.origin}/docs`, '_blank')
    },
  },
}
</script>
<style lang="less" scoped>
@import '../../style/static.less';

.document-link {
  cursor: pointer;
  color: @layout-header-font-color;
  width: 40px;
  height: @layout-header-icon-height;
  line-height: @layout-header-icon-height;
  text-align: center;
  border-radius: 4px;
  &:hover {
    background: linear-gradient(0deg, rgba(0, 80, 201, 0.2) 0%, rgba(174, 207, 255, 0.06) 86.76%);
    color: @layout-header-font-selected-color;
  }
}
</style>
