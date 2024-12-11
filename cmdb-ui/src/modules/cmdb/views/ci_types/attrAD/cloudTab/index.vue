<template>
  <div class="cloud-tabs">
    <div
      v-for="(item) in tabList"
      :key="item.key"
      :class="['cloud-tabs-item', activeKey === item.key ? 'cloud-tabs-item-active' : '']"
      @click="clickTab(item.key)"
    >
      {{ $t(item.text) }}
    </div>
  </div>
</template>

<script>
import { tabList, TAB_KEY } from '../constants.js'

export default {
  name: 'CloudTab',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: String,
      default: TAB_KEY.CUSTOM,
    },
  },
  computed: {
    activeKey: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit('change', newValue)
      }
    },
  },
  data() {
    return {
      tabList
    }
  },
  methods: {
    clickTab(key) {
      this.$emit('change', key)
    }
  }
}
</script>

<style lang="less" scoped >
.cloud-tabs {
  display: flex;
  align-items: center;
  margin-bottom: 26px;

  &-item {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 400;
    color: @text-color_2;
    background-color: @primary-color_7;
    width: 105px;
    height: 32px;
    cursor: pointer;

    &-active {
      border: solid 1px @primary-color_8;
      background-color: @primary-color_4;
      color: @primary-color;
    }

    &:hover {
      color: @primary-color;
    }
  }
}
</style>
