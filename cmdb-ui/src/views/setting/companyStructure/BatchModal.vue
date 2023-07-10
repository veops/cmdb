<template>
  <a-modal
    destroyOnClose
    dialogClass="ops-modal"
    width="500px"
    v-model="visible"
    :title="title"
    layout="inline"
    @cancel="close"
  >
    <a-form-model v-if="visible && batchProps.type === 'department_id'">
      <div :style="{ width: '420px', display: 'inline-block', margin: '0 7px' }">
        <div :style="{ height: '40px', lineHeight: '40px' }">选择部门:</div>
        <DepartmentTreeSelect v-model="batchForm.value"> </DepartmentTreeSelect>
      </div>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'direct_supervisor_id'" ref="ruleForm">
      <div :style="{ width: '420px', display: 'inline-block', margin: '0 7px' }">
        <div :style="{ height: '40px', lineHeight: '40px' }">选择上级:</div>
        <EmployeeTreeSelect v-model="batchForm.value" />
      </div>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'position_name'">
      <a-form-model-item label="编辑岗位">
        <a-input v-model="batchForm.value" />
      </a-form-model-item>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'annual_leave'">
      <a-form-model-item label="编辑年假">
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="batchForm.value"
          placeholder="请输入年假"
          :formatter="(value) => `${value} 天`"
        />
      </a-form-model-item>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'password'" ref="batchForm" :model="batchForm" :rules="rules">
      <a-form-model-item label="重置密码" prop="password">
        <a-input-password v-model="batchForm.value" />
      </a-form-model-item>
      <a-form-model-item label="确认密码" prop="repeatPassword">
        <a-input-password v-model="batchForm.confirmValue" />
      </a-form-model-item>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'block' && batchProps.state === 1">
      <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px', marginRight: '10px' }" />
      <span v-if="batchProps.selectedRowKeys.length > 1">这些用户将会被禁用，是否继续?</span>
      <span v-else>该用户将会被禁用，是否继续?</span>
    </a-form-model>
    <a-form-model v-else-if="batchProps.type === 'block' && batchProps.state === 0">
      <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px', marginRight: '10px' }" />
      <span v-if="batchProps.selectedRowKeys.length > 1">这些用户将会被恢复，是否继续?</span>
      <span v-else>该用户将会被恢复，是否继续?</span>
    </a-form-model>
    <template slot="footer">
      <a-button key="back" @click="close"> 取消 </a-button>
      <a-button key="submit" type="primary" @click="batchModalHandleOk"> 确定 </a-button>
    </template>
  </a-modal>
</template>
<script>
import Treeselect from '@riophae/vue-treeselect'
import { batchEditEmployee } from '@/api/employee'
import EmployeeTreeSelect from '../components/employeeTreeSelect.vue'
import DepartmentTreeSelect from '../components/departmentTreeSelect.vue'
import { getDirectorName } from '@/utils/util'
import Bus from './eventBus/bus'
export default {
  components: { Treeselect, DepartmentTreeSelect, EmployeeTreeSelect },
  inject: ['provide_allFlatEmployees'],
  data() {
    const validatePass = (rule, value, callback) => {
      console.log(this.batchForm)
      if (this.batchForm.value === '') {
        callback(new Error('请输入密码'))
      } else {
        this.$refs.batchForm.validateField('repeatPassword')
        callback()
      }
    }
    const validatePass2 = (rule, value, callback) => {
      console.log(this.batchForm)
      if (this.batchForm.confirmValue === '') {
        callback(new Error('请输入密码'))
      } else if (this.batchForm.confirmValue !== this.batchForm.value) {
        callback(new Error('两次密码不一致'))
      } else {
        callback()
      }
    }
    return {
      visible: false,
      batchProps: {},
      batchForm: {
        value: '',
        confirmValue: '',
      },
      title: '',
      rules: {
        password: [{ required: true, validator: validatePass, trigger: 'blur' }],
        repeatPassword: [{ required: true, validator: validatePass2, trigger: 'blur' }],
      },
    }
  },
  computed: {
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    },
  },
  methods: {
    open(batchProps) {
      this.visible = true
      this.batchProps = batchProps
      const { type, selectedRowKeys, state } = batchProps
      this.title = '批量编辑'
      if (type === 'department_id') {
        this.batchForm.value = null
      } else if (type === 'direct_supervisor_id') {
        this.batchForm.value = undefined
      } else if (type === 'password') {
        if (selectedRowKeys.length <= 1) {
          this.title = '重置密码'
        }
      } else if (type === 'block') {
        this.batchForm.value = state
        if (selectedRowKeys.length <= 1) {
          this.title = state ? '禁用' : '恢复'
        }
      }
    },
    close() {
      this.batchForm.value = ''
      this.batchForm.confirmValue = ''
      this.visible = false
    },
    async batchModalHandleOk() {
      if (this.batchProps.type === 'direct_supervisor_id') {
        this.batchForm.value = this.batchForm.value
          ? this.batchForm.value.includes('-')
            ? Number(this.batchForm.value.split('-')[1])
            : Number(this.batchForm.value)
          : 0
      }
      if (this.batchProps.type === 'password') {
        this.$refs.batchForm.validate(async (valid) => {
          if (valid) {
            this.sendReq()
          }
        })
      } else {
        this.sendReq()
      }
    },
    async sendReq() {
      const employeeIdList = this.batchProps.selectedRowKeys.map((item) => item.employee_id)
      const res = await batchEditEmployee({
        column_name: this.batchProps.type,
        column_value: this.batchForm.value,
        employee_id_list: employeeIdList,
      })
      if (res.length) {
        this.$notification.error({
          message: '操作失败',
          description: res
            .map((item) => `${getDirectorName(this.allFlatEmployees, item.employee_id)}：${item.err}`)
            .join('\n'),
          duration: null,
          style: {
            width: '600px',
            marginLeft: `${335 - 600}px`,
            whiteSpace: 'pre-line',
          },
        })
      } else {
        this.$message.success('操作成功')
      }
      if (this.batchProps.type === 'department_id') {
        Bus.$emit('clickSelectGroup', 1)
      } else {
        this.$emit('refresh')
      }
      Bus.$emit('updataAllIncludeEmployees')
      this.close()
    },
  },
}
</script>
