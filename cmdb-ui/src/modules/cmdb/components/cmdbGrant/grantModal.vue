<template>
  <a-modal :title="title" :visible="visible" @ok="handleOk" @cancel="handleCancel" destroyOnClose>
    <EmployeeTransfer
      :isDisabledAllCompany="true"
      v-if="type === 'depart'"
      uniqueKey="acl_rid"
      ref="employeeTransfer"
      :height="350"
    />
    <RoleTransfer app_id="cmdb" :height="350" ref="roleTransfer" v-if="type === 'role'" />
  </a-modal>
</template>

<script>
import EmployeeTransfer from '@/components/EmployeeTransfer'
import RoleTransfer from '@/components/RoleTransfer'
export default {
  name: 'GrantModal',
  components: { EmployeeTransfer, RoleTransfer },
  data() {
    return {
      visible: false,
      type: 'depart',
    }
  },
  computed: {
    title() {
      if (this.type === 'depart') {
        return '授权用户/部门'
      }
      return '授权角色'
    },
  },
  methods: {
    open(type) {
      this.visible = true
      this.type = type
    },
    handleOk() {
      let params
      if (this.type === 'depart') {
        params = this.$refs.employeeTransfer.getValues()
      }
      if (this.type === 'role') {
        params = this.$refs.roleTransfer.getValues()
      }
      this.handleCancel()
      this.$emit('handleOk', params, this.type)
    },
    handleCancel() {
      this.visible = false
    },
  },
}
</script>

<style></style>
