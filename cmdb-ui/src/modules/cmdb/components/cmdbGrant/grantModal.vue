<template>
  <a-modal :title="title" :visible="visible" @ok="handleOk" @cancel="handleCancel" destroyOnClose>
    <EmployeeTransfer
      :isDisabledAllCompany="true"
      v-if="type === 'depart'"
      uniqueKey="acl_rid"
      ref="employeeTransfer"
      :height="350"
    />
  </a-modal>
</template>

<script>
import EmployeeTransfer from '@/components/EmployeeTransfer'
export default {
  name: 'GrantModal',
  components: { EmployeeTransfer },
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
      const params = this.$refs.employeeTransfer.getValues()
      this.handleCancel()
      this.$emit('handleOk', params)
    },
    handleCancel() {
      this.visible = false
    },
  },
}
</script>

<style></style>
