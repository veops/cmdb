<template>
  <div>
    <a-card :bordered="false">
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="CI变更">
          <ci-table></ci-table>
        </a-tab-pane>
        <a-tab-pane key="2" tab="关系变更">
          <relation-table></relation-table>
        </a-tab-pane>
        <a-tab-pane key="3" tab="模型变更">
          <type-table></type-table>
        </a-tab-pane>
        <a-tab-pane key="4" tab="触发历史">
          <TriggerTable></TriggerTable>
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
      userList: [],
    }
  },
}
</script>

<style></style>
