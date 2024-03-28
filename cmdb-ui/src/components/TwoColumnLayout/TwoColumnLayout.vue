<template>
  <div class="two-column-layout" :style="{ height: `${windowHeight - 64}px` }">
    <SplitPane
      :min="200"
      :max="500"
      :paneLengthPixel.sync="paneLengthPixel"
      :appName="appName"
      :triggerColor="triggerColor"
      :triggerLength="18"
    >
      <template #one>
        <div class="two-column-layout-sidebar">
          <slot name="one"></slot>
        </div>
      </template>
      <template #two>
        <div class="two-column-layout-main">
          <slot name="two"></slot>
        </div>
      </template>
    </SplitPane>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SplitPane from '@/components/SplitPane'
export default {
  name: 'TwoColumnLayout',
  components: { SplitPane },
  props: {
    appName: {
      type: String,
      default: '',
    },
    triggerColor: {
      type: String,
      default: '#f7f8fa',
    },
  },
  data() {
    return {
      paneLengthPixel: 204,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';

.two-column-layout {
  margin-bottom: -24px;
  width: 100%;
  .two-column-layout-sidebar {
    height: 100%;
    border-radius: 15px;
    overflow-y: auto;
  }
  .two-column-layout-main {
    height: 100%;
    padding: 12px;
    background-color: #fff;
    overflow-y: auto;
    border-radius: @border-radius-box;
  }
}
</style>
