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
      </a-tabs>
    </a-card>
  </div>
</template>

<script>
import CiTable from './modules/ciTable.vue'
import RelationTable from './modules/relation.vue'
import TypeTable from './modules/typeTable.vue'
export default {
  name: 'Index',
  data() {
    return {
      userList: []
    }
  },
  components: {
    CiTable,
    RelationTable,
    TypeTable
  }
}
</script>

<style></style>
