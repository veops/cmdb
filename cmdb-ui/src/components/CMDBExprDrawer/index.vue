<template>
  <CustomDrawer
    width="1000px"
    :visible="visible"
    @close="handleClose"
    :hasTitle="false"
    :hasFooter="false"
    :closable="false"
    :bodyStyle="{ padding: '24px 12px' }"
    :placement="placement"
  >
    <ResourceSearch :fromCronJob="true" @copySuccess="copySuccess" />
  </CustomDrawer>
</template>

<script>
import ResourceSearch from '@/modules/cmdb/views/resource_search'
export default {
  name: 'CMDBExprDrawer',
  components: { ResourceSearch },
  props: {
    placement: {
      type: String,
      default: 'right',
    },
  },
  data() {
    return {
      visible: false,
    }
  },
  methods: {
    open() {
      this.visible = true
    },
    handleClose() {
      this.visible = false
    },
    copySuccess(text) {
      this.$emit('copySuccess', text)
      this.handleClose()
    },
  },
}
</script>

<style></style>
