<template>
  <div class="line-wrapper">
    <span class="name">{{ name }}</span>
    <div class="default-process">
      <div class="real-process" :style="{ '--custom-width': `${(number * 100) / total}%` }">
        <img class="image_dot" :src="require(`../../assets/fullscreen/process_line_dot-${type}.png`)" />
        <img class="image_funnel" :src="require(`../../assets/fullscreen/process_line_funnel-${type}.png`)" />
      </div>
    </div>
    <span class="number">
      <span>{{ number }}</span>
      <span>/{{ total }}</span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'ProcessLine',
  props: {
    total: {
      type: Number,
      default: 0,
    },
    number: {
      type: Number,
      default: 0,
    },
    name: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'application',
    },
  },
}
</script>

<style lang="less">
@import './index.less';
</style>
