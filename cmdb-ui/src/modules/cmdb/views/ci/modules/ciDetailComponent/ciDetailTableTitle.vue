<template>
  <div class="ci-detail-table-title">
    {{ title }}
  </div>
</template>

<script>
export default {
  name: 'CIDetailTableTitle',
  props: {
    title: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="less" scoped>
.ci-detail-table-title {
  height: 42px;
  width: 100%;
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 700;
  color: @text-color_1;
  padding: 0px 20px;
  position: relative;
  overflow: hidden;
  background: #EBF0F9;
  border-radius: 8px 8px 0 0;

  &::before {
    content: "";
    height: 44px;
    width: 300px;
    background: #F8F9FD60;
    transform: rotate(40deg);

    position: absolute;
    top: 0px;
    left: 25%;
  }

  &::after {
    content: "";
    height: 44px;
    width: 300px;
    background: #F8F9FD60;
    transform: rotate(40deg);

    position: absolute;
    top: 0px;
    left: calc(25% + 100px);
  }
}
</style>
