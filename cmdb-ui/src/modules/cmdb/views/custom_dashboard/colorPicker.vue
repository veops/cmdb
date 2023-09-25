<template>
  <div class="color-picker">
    <div
      :style="{
        background: Array.isArray(item) ? `linear-gradient(to bottom, ${item[0]} 0%, ${item[1]} 100%)` : item,
      }"
      :class="{ 'color-picker-box': true, 'color-picker-box-selected': isEqual(currenColor, item) }"
      v-for="item in colorList"
      :key="Array.isArray(item) ? item.join() : item"
      @click="changeColor(item)"
    ></div>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: 'ColorPicker',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Array],
      default: null,
    },
    colorList: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    currenColor: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
        return val
      },
    },
  },
  methods: {
    isEqual: _.isEqual,
    changeColor(item) {
      this.$emit('change', item)
    },
  },
}
</script>

<style lang="less" scoped>
.color-picker {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  .color-picker-box {
    width: 19px;
    height: 19px;
    border: 1px solid #dae2e7;
    border-radius: 1px;
    cursor: pointer;
  }
  .color-picker-box-selected {
    position: relative;
    &:after {
      content: '';
      position: absolute;
      width: 24px;
      height: 24px;
      border: 1px solid #43bbff;
      top: -3px;
      left: -3px;
    }
  }
}
</style>
