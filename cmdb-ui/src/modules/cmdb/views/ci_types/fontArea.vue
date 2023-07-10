<template>
  <div class="attributes-font">
    <div
      @click="changeFontStyle('fontWeight', 'bold')"
      :class="`attributes-font-icon ${fontOptions.fontWeight === 'bold' ? 'attributes-font-icon-selected' : ''}`"
    >
      <a-icon type="bold" />
    </div>
    <div
      @click="changeFontStyle('fontStyle', 'italic')"
      :class="`attributes-font-icon ${fontOptions.fontStyle === 'italic' ? 'attributes-font-icon-selected' : ''}`"
    >
      <a-icon type="italic" />
    </div>
    <div
      @click="changeFontStyle('textDecoration', 'underline')"
      :class="
        `attributes-font-icon ${fontOptions.textDecoration === 'underline' ? 'attributes-font-icon-selected' : ''}`
      "
    >
      <a-icon type="underline" />
    </div>
    <div :style="{ width: '100px', marginLeft: '10px', display: 'inline-flex', alignItems: 'center' }">
      <a-icon type="font-colors" /><el-color-picker size="mini" v-model="fontOptions.color"> </el-color-picker>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: 'FontArea',
  data() {
    return {
      fontOptions: {
        color: '#606266',
        fontWeight: 'initial',
        textDecoration: 'initial',
        fontStyle: 'initial', // 'italic'
      },
    }
  },
  methods: {
    changeFontStyle(key, value) {
      this.fontOptions = {
        ...this.fontOptions,
        [key]: this.fontOptions[key] === value ? 'initial' : value,
      }
    },
    getData() {
      const flag = _.isEqual(this.fontOptions, {
        color: '#606266',
        fontWeight: 'initial',
        textDecoration: 'initial',
        fontStyle: 'initial',
      })
      if (flag) {
        return undefined
      } else {
        return this.fontOptions
      }
    },
    setData({ fontOptions = {} }) {
      this.fontOptions = {
        color: '#606266',
        fontWeight: 'initial',
        textDecoration: 'initial',
        fontStyle: 'initial', // 'italic'
        ...fontOptions,
      }
    },
  },
}
</script>

<style lang="less" scoped>
.attributes-font {
  display: flex;
  align-items: center;
  height: 40px;
  .attributes-font-icon {
    cursor: pointer;
    display: inline-block;
    width: 30px;
    height: 30px;
    position: relative;
    margin: 0 5px;
    border: 1px solid #fff;
    &:hover {
      background-color: #eeeeee;
      border-color: #606266;
    }
    > i {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  }
  .attributes-font-icon-selected {
    background-color: #eeeeee;
  }
}
</style>
