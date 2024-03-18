<template>
  <div :class="{ 'read-checkbox': true, 'ant-checkbox-wrapper': isHalfChecked }" @click="openReadGrantModal">
    <a-tooltip
      v-if="value && isHalfChecked"
      :title="valueKey === 'read_ci' ? filerPerimissions[this.rid].name || '' : ''"
    >
      <div v-if="value && isHalfChecked" :class="{ 'read-checkbox-half-checked': true, 'ant-checkbox': true }"></div>
    </a-tooltip>
    <a-checkbox v-else :checked="value" />
  </div>
</template>

<script>
export default {
  name: 'ReadCheckbox',
  inject: {
    provide_filerPerimissions: {
      from: 'filerPerimissions',
    },
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    valueKey: {
      type: String,
      default: 'read_attr',
    },
    rid: {
      type: Number,
      default: 0,
    },
  },
  computed: {
    filerPerimissions() {
      return this.provide_filerPerimissions()
    },
    filterKey() {
      if (this.valueKey === 'read_attr') {
        return 'attr_filter'
      }
      return 'ci_filter'
    },
    isHalfChecked() {
      if (this.filerPerimissions[this.rid]) {
        const _tempValue = this.filerPerimissions[this.rid][this.filterKey]
        return !!(_tempValue && _tempValue.length)
      }
      return false
    },
  },
  methods: {
    openReadGrantModal() {
      this.$emit('openReadGrantModal')
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.read-checkbox {
  .read-checkbox-half-checked {
    width: 16px;
    height: 16px;
    border: 1px solid #d9d9d9;
    border-radius: 2px;
    cursor: pointer;
    margin: 0;
    padding: 0;
    position: relative;
    overflow: hidden;
    &::after {
      content: '';
      position: absolute;
      width: 0;
      height: 0;
      //   background-color: #custom_colors[color_1];
      border-radius: 2px;
      border: 14px solid transparent;
      border-left-color: #custom_colors[color_1];
      transform: rotate(225deg);
      top: -16px;
      left: -17px;
    }
  }
}
</style>
