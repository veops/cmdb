<template>
  <div class="history">
    <div class="history-tab">
      <div
        v-for="(item) in tabs"
        :key="item.key"
        :class="['history-tab-item', activeKey === item.key ? 'history-tab-item-active' : '']"
        @click="activeKey = item.key"
      >
        {{ $t(item.title) }}
      </div>
    </div>

    <div class="history-main">
      <Operation
        v-if="activeKey === 'operation'"
        ref="operationRef"
      />
      <Scan v-if="activeKey === 'scan'" />
    </div>
  </div>
</template>

<script>
import Operation from './operation/index.vue'
import Scan from './scan/index.vue'

export default {
  name: 'HistoryLog',
  components: {
    Operation,
    Scan
  },
  data() {
    return {
      activeKey: 'operation',
      tabs: [
        {
          key: 'operation',
          title: 'cmdb.ipam.operationLog'
        },
        {
          key: 'scan',
          title: 'cmdb.ipam.scanLog'
        }
      ]
    }
  },
  methods: {
    refreshData() {
      if (this.activeKey === 'operation' && this.$refs.operationRef) {
        this.$refs.operationRef.getTableData()
      }
    }
  }
}
</script>

<style lang="less" scoped>
.history {
  width: 100%;

  &-tab {
    display: inline-flex;
    align-items: center;
    border: solid 1px #E4E7ED;

    &-item {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 32px;
      padding: 0 20px;
      background-color: #FFFFFF;
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
      cursor: pointer;

      &:hover {
        color: #2F54EB;
      }

      &-active {
        background-color: #2F54EB;
        color: #FFFFFF !important;
      }
    }
  }

  &-main {
    width: 100%;
    margin-top: 16px;
  }
}
</style>
