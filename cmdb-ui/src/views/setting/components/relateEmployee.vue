<template>
  <a-modal title="关联员工" :visible="visible" @cancel="handleCancel" @ok="handleOK">
    <EmployeeTreeSelect v-model="values" :multiple="true" />
  </a-modal>
</template>

<script>
import EmployeeTreeSelect from './employeeTreeSelect.vue'
export default {
  name: 'RelateEmployee',
  components: { EmployeeTreeSelect },
  data() {
    return {
      visible: false,
      values: [],
    }
  },
  methods: {
    open() {
      this.visible = true
    },
    handleCancel() {
      this.visible = false
      this.values = []
    },
    handleOK() {
      this.$emit('relate', {
        action: 'add',
        employee_id_list: this.values.filter((item) => String(item).includes('-')).map((item) => item.split('-')[1]),
      })
      this.handleCancel()
    },
  },
}
</script>

<style></style>
