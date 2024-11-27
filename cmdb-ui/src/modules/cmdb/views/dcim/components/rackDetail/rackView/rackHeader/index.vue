<template>
  <div class="rack-header">
    <div class="rack-header-part-1">
      <div
        class="rack-header-part-1-line"
        :style="{
          backgroundColor: viewType === 'front' ? '#A4FFF8' : '#FFFFFF'
        }"
      ></div>
    </div>

    <div
      class="rack-header-part-2"
      :style="{
        padding: viewType === 'front' ? '0 8px' : '0 22px'
      }"
    >
      <div
        v-if="viewType === 'front'"
        class="rack-header-part-2-left"
      >
        <RackHeaderCircle/>
        <RackHeaderCircle/>
        <RackHeaderCircle/>
      </div>

      <div class="rack-header-part-2-right">
        <div
          v-for="(item) in 300"
          :key="item"
          class="rack-header-part-2-right-item"
        >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RackHeaderCircle from './rackHeaderCircle.vue'

export default {
  name: 'RackHeader',
  components: {
    RackHeaderCircle
  },
  props: {
    viewType: {
      type: String,
      default: 'front'
    }
  }
}
</script>

<style lang="less" scoped>
.rack-header {
  width: 100%;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  overflow: hidden;

  &-part-1 {
    height: 5px;
    width: 100%;
    background-color: #3D4151;
    padding-top: 3px;

    &-line {
      width: 100%;
      height: 0.5px;
    }
  }

  &-part-2 {
    height: 21px;
    width: 100%;
    background-color: #86909C;
    border-bottom: solid 1px #FFFFFF;
    display: flex;
    align-items: center;
    padding: 0 8px;

    &-left {
      display: flex;
      align-items: center;
      column-gap: 5px;
      margin-right: 7px;
      flex-shrink: 0;
    }

    &-right {
      display: flex;
      flex-wrap: wrap;
      gap: 2px;
      width: 100%;
      height: 10px;
      overflow: hidden;

      &-item {
        width: 1px;
        height: 1px;
        background-color: #C8CDD2;
        flex-shrink: 0;
      }
    }
  }
}
</style>
