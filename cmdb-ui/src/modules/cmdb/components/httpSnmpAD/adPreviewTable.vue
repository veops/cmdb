<template>
  <vxe-table
    size="mini"
    stripe
    class="ops-stripe-table"
    show-overflow
    keep-source
    ref="xTable"
    resizable
    height="100%"
    :data="tableData"
    :scroll-y="{enabled: true}"
  >
    <vxe-column field="name" :title="$t('name')" width="100"> </vxe-column>
    <vxe-column field="type" :title="$t('type')" width="80"> </vxe-column>
    <vxe-column field="example" :title="$t('cmdb.components.example')">
      <template #default="{row}">
        <span v-if="row.type === 'object'">{{ row.example ? JSON.stringify(row.example) : '' }}</span>
        <span v-else>{{ row.example }}</span>
      </template>
    </vxe-column>
    <vxe-column field="desc" :title="$t('desc')"> </vxe-column>
  </vxe-table>
</template>

<script>
export default {
  name: 'ADPreviewTable',
  props: {
    tableData: {
      type: Array,
      default: () => [],
    },
  }
}
</script>

<style lang="less" scoped>
</style>
