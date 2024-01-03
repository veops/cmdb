<template>
  <div class="ops-setting-structure" :style="{ height: `${windowHeight - 64}px` }">
    <!-- 侧边栏 -->
    <SplitPane
      :min="200"
      :max="500"
      :paneLengthPixel.sync="paneLengthPixel"
      appName="setting-structure"
      triggerColor="#F0F5FF"
      :triggerLength="18"
    >
      <template #one>
        <div class="ops-setting-structure-sidebar">
          <div
            :id="`ops-setting-structure-sidebar-group-${group.id}`"
            v-for="(group, groupIndex) in groupData"
            :key="group.id"
          >
            <div
              class="ops-setting-structure-sidebar-group-header"
              :class="{ 'group-selected': groupIndex === activeGroupIndex }"
            >
              <div class="ops-setting-structure-sidebar-group-header-avatar">
                <a-icon :type="group.icon"/>
              </div>
              <span
                class="ops-setting-structure-sidebar-group-header-title"
                @click="
                  clickSelectGroup(groupIndex)
                "
                :id="[group.id === 0 ? 'employee' : 'department']"
              >
                {{ group.title }}
              </span>
            </div>
            <CollapseTransition>
              <div
                class="ops-setting-structure-sidebar-group-category"
                v-show="activeGroupIndex === groupIndex && activeGroupIndex === 0"
              >
                <div
                  :class="{
                    'ops-setting-structure-sidebar-group-category-item': true,
                    'item-selected': 0 === block_status,
                  }"
                >
                  <div class="ops-setting-structure-sidebar-group-category-item-title" @click="clickSelectItem(0)">
                    <div class="item-title">
                      {{ $t('cs.companyStructure.activeEmployee') }}
                    </div>
                    <div class="item-count">
                      <div class="item-count-before">{{ activeEmployeeCount }}</div>
                    </div>
                  </div>
                </div>
                <div
                  :class="{
                    'ops-setting-structure-sidebar-group-category-item': true,
                    'item-selected': 1 === block_status,
                  }"
                >
                  <div class="ops-setting-structure-sidebar-group-category-item-title" @click="clickSelectItem(1)">
                    <div class="item-title">
                      {{ $t('cs.companyStructure.blockEmployee') }}
                    </div>
                    <div class="item-count">
                      <div class="item-count-before">{{ deactiveEmployeeCount }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </CollapseTransition>
            <ul :style="{ marginTop: '10px' }" v-if="activeGroupIndex === groupIndex && activeGroupIndex === 1">
              <CategroyTree
                v-for="(subTree, subIndex) in departmentList"
                :id="subTree.id"
                :key="subTree.id"
                :TreeData="subTree"
                :showLine="subIndex !== departmentList.length - 1"
                icon="setting-structure-depart1"
              />
            </ul>
          </div>
        </div>
      </template>
      <template #two>
        <!-- 表格区 -->
        <div class="ops-setting-structure-main">
          <!-- 搜索,批量操作,添加功能 -->
          <div class="ops-setting-structure-main-controller">
            <div class="ops-setting-structure-main-controller-top">
              <div class="ops-setting-structure-main-controller-serch">
                <div class="input-serch">
                  <a-input-search
                    allow-clear
                    v-model="filterName"
                    :style="{ minWidth: '200px' }"
                    class="ops-input ops-input-radius"
                    :placeholder="$t('cs.role.inputNameOrEmail')"
                    @search="updateTableDataByFilter()"
                  />
                </div>
                <!-- 筛选框 -->
                <div class="Screening-box" v-if="activeGroupIndex === 1" style="background-color: rgb(240, 245, 255) ;">
                  <a-popover
                    @visibleChange="visibleChange"
                    trigger="click"
                    placement="bottom"
                    ref="ScreeningBoxScenePopover"
                    overlayClassName="Screening-box-scene-popover"
                  >
                    <template slot="content">
                      <div
                        v-for="item in sceneList"
                        :key="item.value"
                        :class="{
                          'history-scene-item': true,
                          'history-scene-item-selected': currentScene === item.value,
                        }"
                        @click="clickScene(item)"
                      >
                        {{ item.label }}
                      </div>
                    </template>
                    <span :style="{ whiteSpace: 'nowrap' }">
                      <a-icon class="screening-box-scene-icon" type="filter"/>
                      {{ getCurrentSceneLabel() }}
                      <a-icon class="screening-box-scene-icon" :type="displayTimeIcon"/>
                    </span>
                  </a-popover>
                </div>
                <SearchForm
                  ref="search"
                  :canSearchPreferenceAttrList="canSearchPreferenceAttrList"
                  @refresh="handleSearch"/>
              </div>
              <div>
                <a-space v-if="isEditable">
                  <a-button
                    @click="openEmployeeModal({}, 'add')"
                    size="small"
                    type="primary"
                    shape="circle"
                    icon="plus"
                    ghost
                  />
                  <a-button type="primary" size="small" ghost @click="batchUpload">
                    {{ $t('cs.companyStructure.batchImport') }}
                  </a-button>
                  <template v-if="activeGroupIndex === 1 && selectDepartment.hasOwnProperty('id')">
                    <a-button type="primary" size="small" ghost @click="openDepartmentModal('add')">
                      {{ $t('cs.companyStructure.createSubDepartment') }}
                    </a-button>
                    <a-button
                      type="primary"
                      size="small"
                      ghost
                      @click="openDepartmentModal('edit')"
                      v-if="selectDepartment.id"
                    >
                      {{ $t('cs.companyStructure.editDepartment') }}
                    </a-button>
                    <a-button v-if="selectDepartment.id" type="danger" size="small" ghost @click="deleteDepartment">
                      {{ $t('cs.companyStructure.deleteDepartment') }}
                    </a-button>
                  </template>
                </a-space>
              </div>
            </div>
            <div class="ops-setting-batch">
              <div>
                <div :style="{ marginTop: '8px' }" class="ops-list-batch-action" v-show="!!selectedRowKeys.length">
                  <span @click="downloadEmployeeAll">{{ $t('cs.companyStructure.downloadAll') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="exportSelectEvent">{{ $t('cs.companyStructure.downloadSelected') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="openBatchModal('department_id')">{{ $t('cs.companyStructure.editDepartment') }}</span>
                  <a-divider type="vertical"/>
                  <span
                    @click="openBatchModal('direct_supervisor_id')">{{ $t('cs.companyStructure.editDirectSupervisor') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="openBatchModal('position_name')">{{ $t('cs.companyStructure.editPosition') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="openBatchModal('password')">{{ $t('cs.companyStructure.resetPassword') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="openBatchModal('block', null, 1)">{{ $t('cs.companyStructure.block') }}</span>
                  <a-divider type="vertical"/>
                  <span @click="openBatchModal('block', null, 0)">{{ $t('cs.companyStructure.recover') }}</span>
                  <a-divider type="vertical"/>
                  <span>{{ $t('selectRows', {rows: selectedRowKeys.length}) }}</span>
                </div>
              </div>
              <!-- <div>
                <a-space :style="{ marginRight: '0px'}">
                  <a-button @click="reset" size="small">重置</a-button>
                </a-space>
              </div> -->
            </div>
          </div>
          <!-- 批量操作对话框 -->
          <BatchModal ref="BatchModal" @refresh="updateAll"/>
          <!-- 部门表单对话框 -->
          <DepartmentModal ref="DepartmentModal" @refresh="clickSelectGroup(1)"/>
          <!-- 员工表单对话框 -->
          <EmployeeModal ref="EmployeeModal" @refresh="updateAll"/>

          <!-- 表格展示 -->
          <EmployeeTable
            ref="employeeTable"
            :tableData="tableData"
            :tableHeight="tableHeight"
            @sortChangeEvent="sortChangeEvent"
            @filterChangeEvent="filterChangeEvent"
            @onSelectChange="onSelectChange"
            @openEmployeeModal="openEmployeeModal"
            @openBatchModal="openBatchModal"
            @tranferAttributes="getAttributes"
            :isEditable="isEditable"
            :loading="loading"
          >
          </EmployeeTable>
          <!-- 分页 -->
          <div class="ops-setting-structure-main-pagination">
            <a-pagination
              size="small"
              show-size-changer
              show-quick-jumper
              :page-size-options="pageSizeOptions"
              :current="tablePage.currentPage"
              :total="tablePage.totalResult"
              :show-total="(total, range) => $t('pagination.total', { range0: range[0], range1: range[1], total:total })"
              :page-size="tablePage.pageSize"
              :default-current="1"
              @change="pageOrSizeChange"
              @showSizeChange="pageOrSizeChange"
            >
              <template #buildOptionText="props">
                <span v-if="props.value !== '9999'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
                <span v-else>{{ $t('all') }}</span>
              </template>
            </a-pagination>
          </div>
        </div>
      </template>
    </SplitPane>
    <BatchUpload
      ref="batchUpload"
      @refresh="
        () => {
          updateAll()
          getAllFlatEmployees()
          getAllDepAndEmployee()
          getAllFlatDepartment()
          getAllTreeDepartment()
          clickSelectGroup(1)
        }
      "
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SplitPane from '@/components/SplitPane'
import CollapseTransition from '@/components/CollapseTransition'
import Bus from './eventBus/bus'
import CategroyTree from './CategoryTree'
import BatchUpload from './BatchUpload'
import BatchModal from './BatchModal.vue'
import EmployeeModal from './EmployeeModal.vue'
import DepartmentModal from './DepartmentModal.vue'
import EmployeeTable from '../components/employeeTable.vue'
import { getDepartmentList, deleteDepartmentById, getAllDepartmentList, getAllDepAndEmployee } from '@/api/company'
import { getEmployeeList, getEmployeeCount, downloadAllEmployee, getEmployeeListByFilter } from '@/api/employee'
import { mixinPermissions } from '@/utils/mixin'
import SearchForm from '../components/SearchForm.vue'

export default {
  name: 'CompanyStructure',
  mixins: [mixinPermissions],
  components: {
    CategroyTree,
    SplitPane,
    BatchUpload,
    CollapseTransition,
    BatchModal,
    EmployeeModal,
    DepartmentModal,
    EmployeeTable,
    SearchForm
  },
  data() {
    return {
      isActive: '',
      visible: true,
      localStorageKey: 'itsm-company-strcutre',
      localStoragePaneLengthPixel: 'setting-structure-paneLengthPixel',
      displayTimeIcon: 'down',
      currentScene: '',
      // historySceneitemSelected: 'history-scene-item-selected',
      // historySceneItem: 'history-scene-item',
      paneLengthPixel: 204,
      tableData: [],
      activeEmployeeCount: 0,
      deactiveEmployeeCount: 0,
      selectedRowKeys: [],
      tablePage: {
        currentPage: 1,
        pageSize: 50,
        totalResult: 0,
      },
      filterName: '',
      activeGroupIndex: 0,
      block_status: -1,
      // 部门数据
      departmentList: [],
      selectDepartment: {},
      tableSortData: '',
      tableFilterData: {},
      allFlatEmployees: [],
      allFlatDepartments: [],
      allTreeDepartment: [],
      allTreeDepAndEmp: [],
      isFolder: false,
      attributes: [],
      pageSizeOptions: ['50', '100', '200', '9999'],
      expression: [],
      loading: false
    }
  },
  // created() {
  //   this.init()
  // },
  // mounted() {
  //   console.log(this.$refs.refDemo.style)
  //   this.$refs.refDemo.style.backgroundColor = '#f0f5ff'
  //   this.$refs.refDemo.style.color = '#2f54eb'
  // },
  // watch: {
  //   handleValue() {
  //     if (this.dagHistoryScenePopover) {
  //       this.dagHistoryScenePopover.visible = false
  //     }
  //   }
  // },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      if (this.selectedRowKeys.length) {
        return this.windowHeight - 215
      }
      return this.windowHeight - 180
    },
    isEditable() {
      return this.hasDetailPermission('backend', '公司架构', ['update'])
    },
    canSearchPreferenceAttrList() {
      return [
        { label: this.$t('cs.companyStructure.nickname'), value: 'nickname' },
        { label: this.$t('cs.companyStructure.username'), value: 'username' },
        { label: this.$t('cs.companyStructure.email'), value: 'email' },
        {
          label: this.$t('cs.companyStructure.sex'),
          value: 'sex',
          is_choice: true,
          choice_value: [
              { label: this.$t('cs.companyStructure.male'), value: '男' },
            { label: this.$t('cs.companyStructure.female'), value: '女' }]
        },
        { label: this.$t('cs.companyStructure.mobile'), value: 'mobile' },
        { label: this.$t('cs.companyStructure.departmentName'), value: 'department_name' },
        { label: this.$t('cs.companyStructure.positionName'), value: 'position_name' },
        { label: this.$t('cs.companyStructure.departmentDirector'), value: 'direct_supervisor_id' },
      ]
    },
    sceneList () {
      return [
        {
          label: this.$t('all'),
          value: -1,
        },
        {
          label: this.$t('cs.companyStructure.activeEmployee'),
          value: 0,
        },
        {
          label: this.$t('cs.companyStructure.blockEmployee'),
          value: 1,
        },
      ]
    },
    groupData () {
      return [
        {
          id: 0,
          title: this.$t('cs.companyStructure.employee'),
          icon: 'user',
        },
        {
          id: 1,
          title: this.$t('cs.companyStructure.departmentName'),
          icon: 'apartment',
        },
      ]
    }
  },
  provide() {
    return {
      provide_allFlatEmployees: () => {
        return this.allFlatEmployees
      },
      provide_allFlatDepartments: () => {
        return this.allFlatDepartments
      },
      provide_allTreeDepartment: () => {
        return this.allTreeDepartment
      },
      provide_allTreeDepAndEmp: () => {
        return this.allTreeDepAndEmp
      },
      handleSearch: this.handleSearch,
    }
  },
  async created() {
    const storageData = localStorage.getItem(this.localStorageKey)
    const storage_paneLengthPixel = parseFloat(localStorage.getItem(this.localStoragePaneLengthPixel))
    if (storage_paneLengthPixel) {
      this.paneLengthPixel = storage_paneLengthPixel
    }
    if (storageData) {
      this.currentScene = Number(storageData)
    } else {
      this.currentScene = 0
    }
    // console.log(this.currentScene)
    // this.init()
    this.clickSelectGroup(0).then(val => {
      this.clickSelectItem(0)
    })
    Bus.$on('updataAllIncludeEmployees', () => {
      this.getAllFlatEmployees()
      this.getAllDepAndEmployee()
    })
    Bus.$on('updateAllIncludeDepartment', () => {
      this.getAllFlatDepartment()
      this.getAllTreeDepartment()
      this.getAllDepAndEmployee()
    })
    Bus.$on('selectDepartment', (department) => {
      this.selectDepartment = department
      this.updateTableDataByFilter()
    })
    Bus.$on('reqChildren', async () => {
      // console.log('id', this.selectDepartment.id)
      const children = await this.reqDepartmentList(this.selectDepartment.id)
      // console.log('children', children)
      // console.log('选中列表中的部门', this.findDepartmentById(this.departmentList, this.selectDepartment.id))
      this.findDepartmentById(this.departmentList, this.selectDepartment.id).children = children
    })
    Bus.$on('clickSelectGroup', async (index) => {
      this.clickSelectGroup(index)
    })
    Bus.$on('changeSelectedRowKeys', (selectedRowKeys) => {
      this.selectedRowKeys = selectedRowKeys
    })
    this.getAllFlatEmployees()
    this.getAllFlatDepartment()
    this.getAllTreeDepartment()
    this.getAllDepAndEmployee()
  },
  beforeDestroy() {
    Bus.$off('updataAllIncludeEmployees')
    Bus.$off('updateAllIncludeDepartment')
    Bus.$off('selectDepartment')
    Bus.$off('reqChildren')
    Bus.$off('changeSelectedRowKeys')
  },
  methods: {
    // mouseOver: function() {
    //         this.isClick = 'item-count-after'
    //   },
    // mouseLeave: function() {
    //       this.isClick = 'item-count-before'
    // },
    // init() {
    //   const storageData = localStorage.getItem(this.localStorageKey)
    //   if (storageData) {
    //     this.$emit('changeScene', storageData, true)
    //   }
    // },
    visibleChange(visible) {
      this.displayTimeIcon = visible ? 'up' : 'down'
    },
    getAttributes(attributes) {
      this.attributes = attributes
      this.setSearchPreferenceAttrList()
    },
    setSearchPreferenceAttrList() {
      this.canSearchPreferenceAttrList.forEach((item) => {
        if (!this.attributes.includes(item.value)) {
          this.canSearchPreferenceAttrList = this.canSearchPreferenceAttrList.filter(v => v.value !== item.value)
        }
      })
    },
    clickScene(item) {
      this.currentScene = item.value
      localStorage.setItem(this.localStorageKey, item.value)
      if (this.$refs.ScreeningBoxScenePopover) {
        //     console.log(this.$refs.ScreeningBoxScenePopover)
        this.$refs.ScreeningBoxScenePopover.$refs.tooltip.onVisibleChange(false)
      }
      document.getElementById('department').click()
      // this.currentPage = 1
      // this.updateTableData(1)
      // this.departmentList = this.reqDepartmentList(-1)
    },
    clickHandler(event) {
      this.isActive = event.target.innerText
    },
    getCurrentSceneLabel() {
      const _find = this.sceneList.find((item) => item.value === this.currentScene)
      //  console.log(this.currentScene, this.sceneList, _find)
      return _find?.label || ''
    },
    getAllDepAndEmployee() {
      getAllDepAndEmployee({ block: 0 }).then((res) => {
        this.allTreeDepAndEmp = res
      })
    },
    getAllFlatEmployees() {
      getEmployeeList({ block_status: -1, page_size: 99999 }).then((res) => {
        this.allFlatEmployees = res.data_list
      })
    },
    getAllFlatDepartment() {
      getAllDepartmentList({ is_tree: 0 }).then((res) => {
        this.allFlatDepartments = res
      })
    },
    getAllTreeDepartment() {
      getAllDepartmentList({ is_tree: 1 }).then((res) => {
        this.allTreeDepartment = res
      })
    },
    async updateCount() {
      const [res1, res2] = await Promise.all([
        getEmployeeCount({ block_status: 0 }),
        getEmployeeCount({ block_status: 1 }),
      ])
      this.activeEmployeeCount = res1.employee_count
      this.deactiveEmployeeCount = res2.employee_count
    },
    async updateTableData(currentPage = 1, pageSize = this.tablePage.pageSize) {
      this.selectedRowKeys = []
      let reqEmployeeData = null
      if (this.activeGroupIndex === 0) {
        reqEmployeeData = await getEmployeeList({
          ...this.tableFilterData,
          block_status: this.block_status,
          page: currentPage,
          page_size: pageSize,
          search: this.filterName,
          order: this.tableSortData || 'direct_supervisor_id',
        })
      } else if (this.activeGroupIndex === 1) {
        reqEmployeeData = await getEmployeeList({
          ...this.tableFilterData,
          block_status: this.currentScene,
          department_id: this.selectDepartment.id,
          page: currentPage,
          page_size: pageSize,
          search: this.filterName,
          order: this.tableSortData || 'direct_supervisor_id',
        })
      }
      this.tableData = this.FilterTableData(reqEmployeeData)
      this.tablePage = {
        ...this.tablePage,
        currentPage: reqEmployeeData.page,
        pageSize: reqEmployeeData.page_size,
        totalResult: reqEmployeeData.total,
      }
    },
    async updateTableDataByFilter(currentPage = 1, pageSize = this.tablePage.pageSize) {
      this.loading = true
      this.selectedRowKeys = []
      let reqEmployeeData = null
      if (this.activeGroupIndex === 0) {
        reqEmployeeData = await getEmployeeListByFilter({
          ...this.tableFilterData,
          conditions: this.expression,
          block_status: this.block_status,
          page: currentPage,
          page_size: pageSize,
          search: this.filterName,
          order: this.tableSortData || 'direct_supervisor_id',
        })
      } else if (this.activeGroupIndex === 1) {
        reqEmployeeData = await getEmployeeListByFilter({
          ...this.tableFilterData,
          conditions: this.expression,
          block_status: this.currentScene,
          department_id: this.selectDepartment.id,
          page: currentPage,
          page_size: pageSize,
          search: this.filterName,
          order: this.tableSortData || 'direct_supervisor_id',
        })
      }
      this.tableData = this.FilterTableData(reqEmployeeData)
      this.tablePage = {
        ...this.tablePage,
        currentPage: reqEmployeeData.page,
        pageSize: reqEmployeeData.page_size,
        totalResult: reqEmployeeData.total,
      }
      this.loading = false
    },
    FilterTableData(reqEmployeeData) {
      const tableData = reqEmployeeData.data_list
      // 筛选教育经历数组中学历最高的一条记录
      if (reqEmployeeData.data_list.length) {
        if (reqEmployeeData.data_list[0].educational_experience) {
          // reqEmployeeData.data_list.forEach((row, row_index) => {
          for (let index = 0, len = reqEmployeeData.data_list.length; index < len; index++) {
            const educational_experience = reqEmployeeData.data_list[index].educational_experience
            if (educational_experience) {
              if (educational_experience.length > 1) {
                let max_index = 0
                educational_experience.forEach((item, index) => {
                  if (index < educational_experience.length - 1) {
                    max_index = item.graduation_year > educational_experience[index + 1].graduation_year ? index : index + 1
                  }
                })
                tableData[index].school = educational_experience[max_index].school
                tableData[index].major = educational_experience[max_index].major
                tableData[index].education = educational_experience[max_index].education
                tableData[index].graduation_year = educational_experience[max_index].graduation_year
              } else if (educational_experience.length === 1) {
                tableData[index].school = educational_experience[0].school
                tableData[index].major = educational_experience[0].major
                tableData[index].education = educational_experience[0].education
                tableData[index].graduation_year = educational_experience[0].graduation_year
              } else {
                tableData[index].school = ''
                tableData[index].major = ''
                tableData[index].education = ''
                tableData[index].graduation_year = ''
              }
            }
          }
        }
        // 筛选子女信息中第一位展示在employeeTable
        if (reqEmployeeData.data_list[0].children_information) {
          // reqEmployeeData.data_list.forEach((row, row_index) => {
          for (let row_index = 0, len = reqEmployeeData.data_list.length; row_index < len; row_index++) {
            const children_information = reqEmployeeData.data_list[row_index].children_information
            if (children_information) {
              if (children_information.length) {
                tableData[row_index].name = children_information[0].name
                tableData[row_index].gender = children_information[0].gender
                tableData[row_index].birthday = children_information[0].birthday
                tableData[row_index].parental_leave_left = children_information[0].parental_leave_left
              } else {
                tableData[row_index].name = ''
                tableData[row_index].gender = ''
                tableData[row_index].birthday = ''
                tableData[row_index].parental_leave_left = ''
              }
            }
          }
        }
      }
      return tableData
    },
    updateAll() {
      // this.expression = []
      this.updateCount()
      this.updateTableDataByFilter()
    },
    async clickSelectGroup(index) {
      this.activeGroupIndex = null
      if (index === 0) {
        this.activeGroupIndex = index
        this.block_status = -1
        this.updateAll()
      }
      if (index === 1) {
        this.selectDepartment = {}
        this.activeGroupIndex = index
        this.departmentList = await this.reqDepartmentList(-1)
        Bus.$emit('resettoggle', false)
        // Bus.$emit('changeActiveId', null)
        // Bus.$emit('asFatherSelected', null)
        this.updateTableDataByFilter()
      }
    },
    async clickSelectItem(block_status) {
      this.block_status = block_status
      this.updateTableDataByFilter()
    },
    // 分页器方法
    async pageOrSizeChange(currentPage, pageSize) {
      this.updateTableDataByFilter(currentPage, pageSize)
    },
    openEmployeeModal(row, type) {
      const cloneRow = JSON.parse(JSON.stringify(row))
      this.$refs.EmployeeModal.open(cloneRow, type)
    },
    async downloadEmployeeAll() {
      let block_status = -1
      if (this.activeGroupIndex === 0) {
        block_status = this.block_status
      } else {
        block_status = this.currentScene
      }
      downloadAllEmployee({ block_status: block_status }).then(res => {
        const content = res
        const blob = new Blob([content], { type: 'application/vnd.ms-excel' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'all_employee_info.xlsx'
        a.click()
        window.URL.revokeObjectURL(url)
      })
      this.$refs.employeeTable.getVxetableRef().clearCheckboxRow()
      this.$refs.employeeTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.employeeTable.getVxetableRef().clearSort()
      this.tableSortData = undefined
      this.selectedRowKeys = []
    },
    reset() {
      this.filterName = ''
      this.$refs.filterComp.expression = []
      this.updateTableDataByFilter()
    },
    handleSearch(expression) {
      this.expression = expression
      this.selectedRowKeys = []
      // this.$refs.employeeTable.clearCheckboxRow()
      // this.$refs.employeeTable.clearCheckboxReserve()
      // this.$refs.employeeTable.clearSort()
      // this.tableSortData = undefined
      this.$nextTick(() => {
        if (this.tablePage.currentPage === 1) {
          this.updateTableDataByFilter()
        } else {
          this.tablePage.currentPage = 1
          this.updateTableDataByFilter()
        }
      })
    },
    //  -----------------------------------------部门操作----------------------------------------------
    findDepartmentById(departmentList, id) {
      // if (!departmentList.length) return
      for (let i = 0; i < departmentList.length; i++) {
        const item = departmentList[i]
        if (item.id === id) {
          return item
        }
        if (item.children && item.children.length) {
          const res = this.findDepartmentById(item.children, id)
          if (res) return res
        }
      }
    },
    // 处理获取的部门数据
    transformDepartmentData(departmentList) {
      if (!departmentList.length) return
      const department_transform_list = []
      departmentList.forEach(async (department) => {
        const {
          department_id,
          department_name,
          department_parent_id,
          department_director_id,
          has_sub,
          employee_count,
        } = department
        const department_transform = {
          id: department_id,
          title: department_name,
          parentId: department_parent_id,
          leaderId: department_director_id,
          hasSub: has_sub,
          children: [],
          count: employee_count,
        }
        department_transform_list.push(department_transform)
      })
      return department_transform_list
    },
    // 请求部门数据
    async reqDepartmentList(departmentId) {
      const res = (await getDepartmentList({ department_parent_id: departmentId, block: this.currentScene })).departments
      return this.transformDepartmentData(res)
    },
    openDepartmentModal(type) {
      if (this.selectDepartment.hasOwnProperty('id')) {
        this.$refs.DepartmentModal.open({ type, selectDepartment: this.selectDepartment })
      } else {
        this.$message.error(this.$t('cs.companyStructure.selectDepartment'))
      }
    },
    async deleteDepartment() {
      const that = this
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('confirmDelete2', { name: this.selectDepartment.title }),
        onOk() {
          deleteDepartmentById(that.selectDepartment.id).then((res) => {
            that.clickSelectGroup(1)
            that.$message.success(that.$t('deleteSuccess'))
            Bus.$emit('updateAllIncludeDepartment')
          })
        },
      })
    },
    // -----------------------------------------批量操作--------------------------------------------
    onSelectChange({ records }) {
      this.selectedRowKeys = records
    },
    async openBatchModal(type, row, state) {
      if (row) {
        row = [JSON.parse(JSON.stringify(row))]
      } else {
        row = this.selectedRowKeys
      }
      this.$refs.BatchModal.open({ type, selectedRowKeys: row, state })
    },
    batchUpload() {
      this.$refs.batchUpload.open()
    },
    sortChangeEvent({ sortList }) {
      this.tableSortData = sortList
          .map((item) => {
            return `${item.order === 'asc' ? '' : '-'}${item.property}`
          })
          .join(',')
      this.updateTableDataByFilter()
    },
    filterChangeEvent({ column, property, values, datas, filterList, $event }) {
      if (property === 'roles') {
        this.tableFilterData = {
          ...this.tableFilterData,
          // role_id_list: values && values.length ? values.join(',') : undefined,
          role_id_list: values && values.length ? values : undefined,
        }
      } else if (property === 'is_internship') {
        this.tableFilterData = {
          ...this.tableFilterData,
          is_internship: values && values.length ? values[0] : undefined,
        }
      }
      this.updateTableDataByFilter()
    },
    exportSelectEvent() {
      Bus.$emit('reqExportSelectEvent')
    },
  },
}
</script>
<style lang="less" scoped>
@import '~@/style/static.less';
.ops-setting-structure {
  margin-bottom: -24px;
  width: 100%;
  .ops-setting-structure-sidebar {
    height: 100%;
    padding: 15px;
    border-radius: 15px;
    overflow-y: hidden;
    &:hover {
      overflow-y: overlay;
    }
    background-color: #fff;
    .ops-setting-structure-sidebar-group-header {
      display: inline-flex;
      align-items: center;
      width: 100%;
      height: 42px;
      padding: 0 10px;
      border-radius: 8px;
      &:hover {
        background-color: #e1efff;
        .ops-setting-structure-sidebar-group-header-title {
          color: #custom_colors[color_1];
        }
      }
      .ops-setting-structure-sidebar-group-header-avatar {
        width: 26px;
        height: 26px;
        background-color: #ced2e3;
        border-radius: 4px;
        > i {
          width: 26px;
          height: 26px;
          padding-top: 3px;
          font-size: 20px;
          color: #fff;
        }
      }
      .ops-setting-structure-sidebar-group-header-title {
        margin-left: 8px;
        font-size: 16px;
        font-weight: 500;
        color: #000;
        cursor: pointer;
        user-select: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 120px;
      }
    }
    .ops-setting-structure-sidebar-group-category {
      width: 100%;
      .ops-setting-structure-sidebar-group-category-item {
        display: flex;
        align-items: center;
        height: 30px;
        position: relative;
        padding-left: 8px;
        color: rgba(0, 0, 0, 0.7);
        font-size: 14px;
        width: 100%;
        &:hover {
          color: #custom_colors[color_1];
          &::before {
            background-color: #custom_colors[color_1];
          }
        }
        &::before {
          content: '';
          display: inline-block;
          width: 5px;
          height: 5px;
          background-color: #cacaca;
          border-radius: 50%;
          margin-right: 10px;
        }
        &:not(:last-child)::after {
          content: '';
          position: absolute;
          width: 1px;
          height: 25px;
          background-color: rgba(0, 0, 0, 0.1);
          top: 18px;
          left: 10px;
        }
        .ops-setting-structure-sidebar-group-category-item-title {
          position: relative;
          display: flex;
          justify-content: space-between;
          align-items: center;
          //  display: inline-block;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          //  width: 155px;
          width: 100%;
          cursor: pointer;
          user-select: none;
          font-size: 15px;

          flex-wrap: wrap;
          .item-title {
            display: inline-block;
            // width: 30%;
            // height: 40%;
            margin: 8px;
          }
          .item-count-after {
            //position: absolute;
            display: inline-block;
            margin: 0 auto;
            width: 27px;
            height: 15px;
            background: #ffffff;
            border-radius: 2px;
            text-align: center;
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 10px;
            line-height: 12px;
            color: #2f54eb;
          }
          .item-count-before {
            display: inline-block;
            margin: 0 auto;
            width: 27px;
            height: 15px;
            background: #e1efff;
            border-radius: 2px;
            text-align: center;
            font-family: 'Inter';
            font-style: normal;
            font-weight: 400;
            font-size: 10px;
            line-height: 12px;
            color: #9094a6;
          }
        }
      }
      .item-selected {
        color: #custom_colors[color_1];
        &::before {
          background-color: #custom_colors[color_1];
        }
      }
    }
    .group-selected {
      background-color: #e1efff;
      .ops-setting-structure-sidebar-group-header-avatar {
        background-color: #custom_colors[color_1];
      }
      .ops-setting-structure-sidebar-group-header-title {
        color: #custom_colors[color_1];
      }
    }
  }

  .ops-setting-structure-main {
    padding: 12px;
    background-color: #fff;
    overflow-y: auto;
    border-radius: 15px;
    .ops-setting-structure-main-controller {
      // height: 70px;
      margin-bottom: 12px;
      .ops-setting-structure-main-controller-top {
        width: 100%;
        display: flex;
        justify-content: space-between;
        height: 40px;
        .ops-setting-structure-main-controller-serch {
          float: left;
          display: flex;
          .Screening-box {
            margin-left: 10px;
            display: inline-block;
            .ops_display_wrapper(#fff);
            .screening-box-scene-icon {
              color: #custom_colors[color_1];
              font-size: 12px;
            }
            .history-scene-item {
              //.ops_popover_item();
              cursor: pointer;
              padding: 5px 10px;
            }
          }
          .search-form-bar-filter {
            .ops_display_wrapper();
            .search-form-bar-filter-icon {
              color: #custom_colors[color_1];
              font-size: 12px;
            }

          }
        }
      }

      .ops-setting-batch {
        width: 100%;
        display: flex;
        justify-content: space-between;
        .ops-list-batch-action {
          height: 27px;
          .ant-divider,
          .ant-divider-vertical {
            margin: 0;
          }
        }
      }

    }
    .ops-setting-structure-main-pagination {
      width: 100%;
      margin-top: 12px;
      display: inline-flex;
      justify-content: flex-end;
    }
  }
}
.Screening-box-scene-popover {
  .history-scene-item {
    //.ops_popover_item();
    cursor: pointer;
    padding: 5px 10px;
  }
  .history-scene-item-selected {
    //.ops_popover_item_selected();
    background-color: #f0f5ff;
    color: #2f54eb;
  }
}
</style>
<style lang="less">
.Screening-box-scene-popover {
  .ant-popover-inner-content {
    padding: 0;
    width: 186px;
  }
}
</style>
