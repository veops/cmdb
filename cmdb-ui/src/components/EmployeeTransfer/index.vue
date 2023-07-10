<template>
  <div class="employee-transfer" :style="{ '--custom-height': `${height}px` }">
    <div class="employee-transfer-left" v-if="!readOnly">
      <treeselect
        :disable-branch-nodes="disableBranchNodes"
        :flat="true"
        :multiple="true"
        :options="employeeTreeSelectOption"
        placeholder="请输入搜索内容"
        v-model="treeValue"
        :max-height="height - 50"
        noChildrenText="空"
        noOptionsText="空"
        :clearable="false"
        :always-open="true"
        :default-expand-level="1"
        :class="{ 'employee-transfer': true, 'employee-transfer-has-input': !!inputValue }"
        @search-change="changeInputValue"
        noResultsText="暂无数据"
        openDirection="below"
      >
      </treeselect>
    </div>
    <div class="employee-transfer-operation" v-if="!readOnly">
      <div @click="handleRight" class="operation-right"><a-icon type="right" /></div>
      <br />
      <div @click="handleLeft" class="operation-left"><a-icon type="left" /></div>
    </div>
    <div class="employee-transfer-right">
      <div
        :class="{
          'employee-transfer-right-item': true,
          'employee-transfer-right-selected': !readOnly && selectedRight.includes(right),
        }"
        v-for="right in rightData"
        :key="right"
        @click="handleSelectedRight(right)"
      >
        {{ getLabel(right) }}
      </div>
    </div>
  </div>
</template>

<script>
import { getAllDepAndEmployee, getAllDepartmentList } from '@/api/company'
import { getEmployeeList } from '@/api/employee'
import { formatOption } from '@/utils/util'

export default {
  name: 'EmployeeTransfer',
  inject: {
    getDataBySelf: {
      from: 'getDataBySelf',
      default: true,
    },
    provide_allTreeDepAndEmp: {
      default: () => null,
    },
    provide_allFlatDepartments: {
      default: () => null,
    },
    provide_allFlatEmployees: {
      default: () => null,
    },
  },
  props: {
    height: {
      type: Number,
      default: 260,
    },
    disableBranchNodes: {
      type: Boolean,
      default: false,
    },
    uniqueKey: {
      type: String,
      default: '',
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    isDisabledAllCompany: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      default_allTreeDepAndEmp: [],
      treeValue: [],
      inputValue: '',
      rightData: [],
      selectedRight: [],
      default_allFlatDepartments: [],
      default_allFlatEmployees: [],
    }
  },
  computed: {
    employeeTreeSelectOption() {
      return formatOption(
        this.allTreeDepAndEmp,
        2,
        this.isDisabledAllCompany,
        this.uniqueKey || 'department_id',
        this.uniqueKey || 'employee_id'
      )
    },
    allTreeDepAndEmp() {
      if (this.getDataBySelf) {
        return this.default_allTreeDepAndEmp
      }
      return this.provide_allTreeDepAndEmp()
    },
    allFlatDepartments() {
      if (this.getDataBySelf) {
        return this.default_allFlatDepartments
      }
      return this.provide_allFlatDepartments()
    },
    allFlatEmployees() {
      if (this.getDataBySelf) {
        return this.default_allFlatEmployees
      }
      return this.provide_allFlatEmployees()
    },
  },
  mounted() {
    if (this.getDataBySelf) {
      getAllDepAndEmployee({ block: 0 }).then((res) => {
        this.default_allTreeDepAndEmp = res
      })
      // 获取全部员工和部门的平铺列表
      getEmployeeList({ block_status: 0, page_size: 99999 }).then((res) => {
        this.default_allFlatEmployees = res.data_list
      })
      getAllDepartmentList({ is_tree: 0 }).then((res) => {
        this.default_allFlatDepartments = res
      })
    }
  },
  methods: {
    setValues({ rightData }) {
      this.rightData = rightData
    },
    getValues() {
      const department = []
      const user = []
      this.rightData.forEach((item) => {
        const _split = item.split('-')
        if (_split[0] === 'department') {
          department.push(Number(_split[1]))
        } else {
          user.push(Number(_split[1]))
        }
      })
      const _idx = department.findIndex((item) => item === 0)
      if (_idx > -1) {
        department.splice(_idx, 1)
        department.unshift(-1)
      }
      return {
        department,
        user,
      }
    },
    changeInputValue(value) {
      this.inputValue = value
    },
    handleRight() {
      this.rightData = [...new Set([...this.treeValue, ...this.rightData])]
      this.treeValue = []
      this.selectedRight = []
    },
    handleLeft() {
      this.selectedRight.forEach((id) => {
        const _idx = this.rightData.findIndex((item) => item === id)
        if (_idx > -1) {
          this.rightData.splice(_idx, 1)
        }
      })
      this.selectedRight = []
    },
    handleSelectedRight(id) {
      const _idx = this.selectedRight.findIndex((item) => item === id)
      if (_idx > -1) {
        this.selectedRight.splice(_idx, 1)
      } else {
        this.selectedRight.push(id)
      }
    },
    getLabel(id) {
      const _split = id.split('-')
      const type = _split[0]
      const _id = Number(_split[1])
      if (type === 'department') {
        const _find = this.allFlatDepartments.find((item) => item[this.uniqueKey || 'department_id'] === _id)
        return _find?.department_name ?? ''
      } else {
        const _find = this.allFlatEmployees.find((item) => item[this.uniqueKey || 'employee_id'] === _id)
        return _find?.nickname ?? ''
      }
    },
  },
}
</script>

<style lang="less">
@import '~@/style/static.less';
.employee-transfer {
  width: 100%;
  .vue-treeselect__multi-value-item-container {
    display: none;
  }
  .vue-treeselect__menu {
    border: none;
    box-shadow: none;
    margin-top: 10px;
    background-color: #f9fbff;
    margin-top: 0 !important;
  }
}
.employee-transfer.vue-treeselect--open.vue-treeselect--open-below .vue-treeselect__control {
  border-radius: 2px;
  width: 90%;
  margin-left: 5%;
  border-color: rgba(0, 0, 0, 0.1);
}
.employee-transfer.vue-treeselect--has-value {
  .vue-treeselect-helper-hide {
    display: block;
  }
}
.employee-transfer.employee-transfer-has-input {
  .vue-treeselect-helper-hide {
    display: none;
  }
}
</style>

<style lang="less" scoped>
@import '~@/style/static.less';
.employee-transfer {
  display: flex;
  justify-content: space-between;
  & &-left,
  & &-right {
    width: 40%;
    background-color: #f9fbff;
    padding-top: 12px;
    border: 1px solid #e4e7ed;
    border-radius: 4px;
    height: var(--custom-height);
  }
  & &-right {
    padding-top: 12px;
    overflow: auto;
    .employee-transfer-right-item {
      cursor: pointer;
      padding: 2px 12px;
      margin: 2px 0;
    }
    .employee-transfer-right-selected {
      background-color: #f0f5ff;
    }
  }
  & &-operation {
    width: 10%;
    height: var(--custom-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .operation-left,
    .operation-right {
      width: 20px;
      height: 20px;
      border-radius: 2px;
      background-color: #custom_colors[color_2];
      color: #custom_colors[color_1];
      display: inline-flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      &:hover {
        background-color: #custom_colors[color_1];
        color: #fff;
      }
    }
  }
}
</style>
