<template>
  <div>
    <a-card :bordered="false">
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" :tab="$t('cmdb.history.ciChange')">
          <ci-table></ci-table>
        </a-tab-pane>
        <a-tab-pane key="2" :tab="$t('cmdb.history.relationChange')">
          <relation-table></relation-table>
        </a-tab-pane>
        <a-tab-pane key="3" :tab="$t('cmdb.history.ciTypeChange')">
          <type-table></type-table>
        </a-tab-pane>
        <a-tab-pane key="4" :tab="$t('cmdb.history.triggerHistory')">
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
