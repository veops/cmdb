<template>
  <div class="circle-container">
    <div class="circle shadow-1"></div>
    <div class="circle shadow-2"></div>
    <div class="circle shadow-3"></div>
    <div class="circle inner-circle"></div>
    <div class="circle inner-shadow"></div>
  </div>
</template>

<script>
export default {
  name: 'RackHeaderCircle'
}
</script>

<style lang="less" scoped>
.circle-container {
  position: relative;
  width: 6px;
  height: 6px;

  .circle {
    position: absolute;
    border-radius: 50%;
    background-color: #20e757;
    width: 6px;
    height: 6px;
    top: 0px;
    left: 0px;
  }

  .shadow-1 {
    filter: blur(4px);
    opacity: 0.7;
  }

  .shadow-2 {
    filter: blur(2px);
    opacity: 0.8;
  }

  .shadow-3 {
    filter: blur(1px);
    opacity: 0.9;
  }

  .inner-circle {
    background-color: #6cffe5;
    width: 6px;
    height: 6px;
    top: 0px;
    left: 0px;
  }

  .inner-shadow {
    background-color: #6affe4;
    width: 4px;
    height: 4px;
    top: 0px;
    left: 0px;
    filter: blur(1px);
    opacity: 0.8;
  }
}
</style>
