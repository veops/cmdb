<template>
  <div class="operation-history">
    <a-card :bordered="false" :body-style="{ padding: '16px 24px' }">
      <a-tabs v-model="activeKey" default-active-key="1" :animated="false">
        <a-tab-pane key="1">
          <span slot="tab">
            <a-icon type="profile" />
            {{ $t('cmdb.history.ciChange') }}
          </span>
          <ci-table v-if="activeKey === '1'"></ci-table>
        </a-tab-pane>
        <a-tab-pane key="2">
          <span slot="tab">
            <a-icon type="share-alt" />
            {{ $t('cmdb.history.relationChange') }}
          </span>
          <relation-table v-if="activeKey === '2'"></relation-table>
        </a-tab-pane>
        <a-tab-pane key="3">
          <span slot="tab">
            <a-icon type="apartment" />
            {{ $t('cmdb.history.ciTypeChange') }}
          </span>
          <type-table v-if="activeKey === '3'"></type-table>
        </a-tab-pane>
        <a-tab-pane key="4">
          <span slot="tab">
            <a-icon type="thunderbolt" />
            {{ $t('cmdb.history.triggerHistory') }}
          </span>
          <trigger-table v-if="activeKey === '4'"></trigger-table>
        </a-tab-pane>
      </a-tabs>
    </a-card>
  </div>
</template>

<script>
import CiTable from './modules/ciTable.vue'
import RelationTable from './modules/relation.vue'
import TypeTable from './modules/typeTable.vue'
import TriggerTable from './modules/triggerTable.vue'
export default {
  name: 'OperationHistory',
  components: {
    CiTable,
    RelationTable,
    TypeTable,
    TriggerTable,
  },
  data() {
    return {
      activeKey: '1'
    }
  },
}
</script>

<style lang="less" scoped>
.operation-history {
  :deep(.ant-card-body) {
    padding: 16px 24px;
  }

  :deep(.ant-tabs) {
    .ant-tabs-bar {
      margin-bottom: 0;
      border-bottom: 1px solid #e8e8e8;
    }

    .ant-tabs-nav {
      .ant-tabs-tab {
        padding: 12px 0;
        margin-right: 32px;
        font-size: 14px;
        line-height: 22px;

        .anticon {
          margin-right: 8px;
          font-size: 14px;
        }

        &:hover {
          color: @primary-color;
        }
      }

      .ant-tabs-tab-active {
        font-weight: 500;
        color: @primary-color;
      }
    }

    .ant-tabs-content {
      padding-top: 16px;
    }
  }
}
</style>
