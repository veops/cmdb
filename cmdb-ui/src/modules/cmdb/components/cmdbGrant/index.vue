<template>
  <a-modal width="800px" :visible="visible" @ok="handleOk" @cancel="handleCancel" :bodyStyle="{ padding: 0 }">
    <GrantComp
      :resourceType="resourceType"
      :app_id="app_id"
      :cmdbGrantType="cmdbGrantType"
      :resourceTypeName="resourceTypeName"
      :typeRelationIds="typeRelationIds"
      :CITypeId="CITypeId"
      :isModal="true"
    />
  </a-modal>
</template>

<script>
import GrantComp from './grantComp.vue'
export default {
  name: 'CMDBGrant',
  components: { GrantComp },
  props: {
    resourceType: {
      type: String,
      default: 'CIType',
    },
    app_id: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      visible: false,
      resourceTypeName: '',
      typeRelationIds: [],
      cmdbGrantType: '',
      CITypeId: null,
    }
  },
  methods: {
    open({ name, typeRelationIds = [], cmdbGrantType, CITypeId }) {
      this.visible = true
      this.resourceTypeName = name
      this.typeRelationIds = typeRelationIds
      this.cmdbGrantType = cmdbGrantType
      this.CITypeId = CITypeId
    },
    handleOk() {
      this.handleCancel()
    },
    handleCancel() {
      this.visible = false
    },
  },
}
</script>

<style></style>
