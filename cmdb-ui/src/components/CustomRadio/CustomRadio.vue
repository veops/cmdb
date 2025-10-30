<template>
  <div class="custom-radio">
    <div
      v-for="radio in radioList"
      :class="`custom-radio-inner custom-radio-inner-${radio.layout || 'inline'}`"
      :key="radio.value"
    >
      <a-radio @click="clickRadio(radio.value)" :checked="value === radio.value" :key="`raido_${radio.value}`">
        <slot :name="`label_${radio.value}`" :radio="radio">
          {{ radio.label }}
        </slot>
      </a-radio>
      <slot
        :name="`extra_${radio.value}`"
        v-bind="{ radioValue: radio.value, label: radio.label }"
      ></slot>
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
