<template>
  <a-modal v-model="visible" :title="`${$t('acl.groupMember')}${editRecord.name}`" :width="800" :footer="null">
    <div :style="{ maxHeight: '500px', overflow: 'auto' }">
      <a-tag :style="{ marginBottom: '5px' }" v-for="mem in members" :key="mem.name">
        {{ mem.name }}
      </a-tag>
    </div>
  </a-modal>
</template>
<script>
import { getResourceGroupItems } from '@/modules/acl/api/resource'
export default {
  name: 'ResourceGroupMember',
  data() {
    return {
      visible: false,
      editRecord: {},
      members: [],
    }
  },
  methods: {
    handleEdit(record) {
      this.visible = true
      this.editRecord = record
      this.loadMembers(record.id)
    },
    loadMembers(_id) {
      getResourceGroupItems(_id).then((res) => {
        this.members = res
      })
      // .catch(err => this.$httpError(err))
    },
  },
}
</script>
