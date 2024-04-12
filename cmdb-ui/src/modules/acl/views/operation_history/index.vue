<template>
  <div class="acl-operation-history">
    <a-tabs default-active-key="1">
      <a-tab-pane key="1" :tab="$t('acl.permissionChange')">
        <permisson-table></permisson-table>
      </a-tab-pane>
      <a-tab-pane key="2" :tab="$t('acl.roleChange')">
        <role-history-table></role-history-table>
      </a-tab-pane>
      <a-tab-pane key="3" :tab="$t('acl.resourceChange')">
        <resource-history-table></resource-history-table>
      </a-tab-pane>
      <a-tab-pane key="4" :tab="$t('acl.resourceTypeChange')">
        <resource-type-history-table></resource-type-history-table>
      </a-tab-pane>
      <a-tab-pane key="5" :tab="$t('acl.triggerChange')">
        <trigger-history-table></trigger-history-table>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import permissonTable from './modules/permissionTable.vue'
import resourceHistoryTable from './modules/resourceHistoryTable.vue'
import resourceTypeHistoryTable from './modules/resourceTypeHistoryTable.vue'
import roleHistoryTable from './modules/roleHistoryTable.vue'
import triggerHistoryTable from './modules/triggerHistoryTable.vue'
export default {
  components: { permissonTable, resourceHistoryTable, resourceTypeHistoryTable, roleHistoryTable, triggerHistoryTable },
}
</script>

<style lang="less" scoped>

.acl-operation-history {
  border-radius: @border-radius-box;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 24px;
  background-color: #fff;
}
</style>
