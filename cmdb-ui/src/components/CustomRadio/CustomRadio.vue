<template>
  <div class="custom-radio">
    <div
      :class="`custom-radio-inner custom-radio-inner-${layout || 'inline'}`"
      v-for="{ value: radioValue, label, layout } in radioList"
      :key="radioValue"
    >
      <a-radio @click="clickRadio(radioValue)" :checked="value === radioValue" :key="`raido_${radioValue}`">{{
        label
      }}</a-radio>
      <slot :name="`extra_${radioValue}`" v-bind="{ radioValue, label }"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomRadio',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Number],
      default: '',
    },
    radioList: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    clickRadio(radioValue) {
      this.$emit('change', radioValue)
    },
  },
}
</script>

<style lang="less" scoped>
.custom-radio {
  .custom-radio-inner {
    min-height: 40px;
  }
  .custom-radio-inner-inline {
    display: flex;
    align-items: center;
  }
  .custom-radio-inner-vertical label {
    line-height: 40px;
  }
}
</style>
