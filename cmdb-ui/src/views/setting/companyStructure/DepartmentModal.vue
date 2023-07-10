<template>
  <a-modal
    destroyOnClose
    width="500px"
    v-model="visible"
    :title="type === 'add' ? '创建子部门' : '编辑部门'"
    layout="inline"
    @cancel="close"
  >
    <a-form-model
      ref="departmentFormData"
      :model="departmentFormData"
      :rules="rules"
      :label-col="labelCol"
      :wrapper-col="wrapperCol"
    >
      <a-form-model-item ref="title" label="部门名称" prop="department_name">
        <a-input v-model="departmentFormData.department_name" placeholder="请输入部门名称" />
      </a-form-model-item>
      <a-form-model-item label="上级部门" prop="department_parent_id">
        <DepartmentTreeSelect v-model="departmentFormData.department_parent_id" />
        <!-- <Treeselect
          v-else
          :multiple="false"
          :options="currentDepartmentParentList"
          v-model="departmentFormData.department_parent_id"
          class="ops-setting-treeselect"
          placeholder="请选择上级部门"
          :normalizer="
            (node) => {
              return {
                id: node.department_id,
                label: node.department_name,
                children: node.children,
              }
            }
          "
        /> -->
      </a-form-model-item>
      <a-form-model-item label="部门负责人" prop="department_director_id">
        <EmployeeTreeSelect v-model="departmentFormData.department_director_id" />
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button key="back" @click="close"> 取消 </a-button>
      <a-button key="submit" type="primary" @click="departmentModalHandleOk"> 确定 </a-button>
    </template>
  </a-modal>
</template>

<script>
import Treeselect from '@riophae/vue-treeselect'
import { getParentDepartmentList, putDepartmentById, postDepartment } from '@/api/company'
import EmployeeTreeSelect from '../components/employeeTreeSelect.vue'
import DepartmentTreeSelect from '../components/departmentTreeSelect.vue'
import Bus from './eventBus/bus'
export default {
  name: 'DepartmentModal',
  components: { Treeselect, EmployeeTreeSelect, DepartmentTreeSelect },
  data() {
    return {
      labelCol: { span: 5 },
      wrapperCol: { span: 19 },
      visible: false,
      departmentFormData: {
        department_name: '',
        department_parent_id: '',
        department_director_id: undefined,
      },
      rules: {
        department_name: [{ required: true, message: '请输入部门名称' }],
        department_parent_id: [{ required: true, message: '请选择上级部门' }],
      },
      currentDepartmentParentList: [],
      selectDepartment: {},
      type: 'add',
    }
  },
  inject: ['provide_allFlatEmployees'],
  computed: {
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    },
  },
  mounted() {},
  methods: {
    async open({ type, selectDepartment }) {
      this.selectDepartment = selectDepartment
      this.type = type
      const { title, parentId, leaderId, id } = selectDepartment
      let department_director_id
      if (type === 'add') {
        this.departmentFormData = {
          department_name: '',
          department_parent_id: id,
          department_director_id,
        }
      } else if (type === 'edit') {
        const res = await getParentDepartmentList({ department_id: id })
        this.currentDepartmentParentList = res
        if (leaderId) {
          const _find = this.allFlatEmployees.find((item) => item.employee_id === leaderId)
          department_director_id = `${_find.department_id}-${leaderId}`
        }
        this.departmentFormData = {
          department_name: title,
          department_parent_id: parentId,
          department_director_id,
        }
      }
      this.visible = true
    },
    close() {
      this.selectDepartment = {}
      this.visible = false
    },
    async departmentModalHandleOk() {
      this.$refs.departmentFormData.validate(async (valid) => {
        if (valid) {
          const { department_director_id } = this.departmentFormData
          const params = {
            ...this.departmentFormData,
            department_director_id: department_director_id
              ? String(department_director_id).split('-')[String(department_director_id).split('-').length - 1]
              : undefined,
          }
          if (this.type === 'edit') {
            await putDepartmentById(this.selectDepartment.id, params)
          } else if (this.type === 'add') {
            await postDepartment(params)
          }
          this.$message.success('操作成功')
          this.$emit('refresh')
          Bus.$emit('updateAllIncludeDepartment')
          this.close()
        }
      })
    },
  },
}
</script>

<style></style>
