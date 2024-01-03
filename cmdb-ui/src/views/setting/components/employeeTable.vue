<template>
  <vxe-table
    ref="employeeTable"
    border="none"
    stripe
    :data="tableData"
    show-overflow
    show-header-overflow
    highlight-hover-row
    size="small"
    class="ops-stripe-table"
    :height="tableHeight"
    :loading="loading"
    :sort-config="{ remote: true, trigger: 'cell', multiple: true }"
    @sort-change="sortChangeEvent"
    :column-config="{ resizable: true }"
    @checkbox-change="onSelectChange"
    @checkbox-all="onSelectChange"
    :filter-config="{ remote: true }"
    @filter-change="filterChangeEvent"
    :tooltip-config="{ contentMethod: contentMethod }"
    :column-key="true"
    :row-key="true"
  >
    <vxe-column type="checkbox" width="60px" v-if="isEditable && attributes.length" fixed="left"></vxe-column>
    <vxe-column
      field="nickname"
      min-width="100px"
      :title="$t('cs.companyStructure.nickname')"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'nickname') !== -1 && attributes.findIndex((v) => v == 'nickname') !== -1"
      key="nickname"
      fixed="left"
    >
      <template #default="{ row }">
        <div
          :style="{
            display: 'inline-block',
            width: '6px',
            marginBottom: '1px',
            height: '6px',
            borderRadius: '50%',
            backgroundColor: row.block ? '#ff6767' : '#49cc90',
            marginRight: '8px',
          }"
        ></div>
        <div :style="{ display: 'inline-block' }">{{ row.nickname }}</div>
      </template>
    </vxe-column>
    <vxe-column
      field="username"
      :title="$t('cs.companyStructure.username')"
      min-width="120px"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'username') !== -1 && attributes.findIndex((v) => v == 'username') !== -1"
      key="username"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.username') }}</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="email"
      :title="$t('cs.companyStructure.email')"
      min-width="140px"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'email') !== -1 && attributes.findIndex((v) => v == 'email') !== -1"
      key="email"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.email') }}</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="sex"
      :title="$t('cs.companyStructure.sex')"
      width="70px"
      sortable
      align="center"
      v-if="checkedCols.findIndex((v) => v == 'sex') !== -1 && attributes.findIndex((v) => v == 'sex') !== -1"
      key="sex"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.sex') }}</span>
        </span>
      </template>
      <template #default="{row}">
        <span v-if="row.sex === '男'">{{ $t('cs.companyStructure.male') }}</span>
        <span v-if="row.sex === '女'">{{ $t('cs.companyStructure.female') }}</span>
      </template>
    </vxe-column>
    <vxe-column
      field="mobile"
      :title="$t('cs.companyStructure.mobile')"
      min-width="100px"
      v-if="checkedCols.findIndex((v) => v == 'mobile') !== -1 && attributes.findIndex((v) => v == 'mobile') !== -1"
      sortable
      key="mobile"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.mobile') }}</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="department_name"
      :title="$t('cs.companyStructure.departmentName')"
      min-width="90px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'department_name') !== -1 &&
          attributes.findIndex((v) => v == 'department_name') !== -1
      "
      key="department_name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.departmentName') }}</span>
        </span>
      </template>
      <template #default="{ row }">
        <!-- {{ getDepartmentName(allFlatDepartments, row.department_id) }} -->
        {{ row.department_name }}
      </template>
    </vxe-column>
    <vxe-column
      field="position_name"
      :title="$t('cs.companyStructure.positionName')"
      min-width="120px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'position_name') !== -1 &&
          attributes.findIndex((v) => v == 'position_name') !== -1
      "
      key="position_name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.positionName') }}</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="direct_supervisor_id"
      :title="$t('cs.companyStructure.supervisor')"
      min-width="120px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'direct_supervisor_id') !== -1 &&
          attributes.findIndex((v) => v == 'direct_supervisor_id') !== -1
      "
      key="direct_supervisor_id"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>{{ $t('cs.companyStructure.supervisor') }}</span>
        </span>
      </template>
      <template #default="{ row }">
        <span v-if="row.direct_supervisor_id !== 0">{{
          getDirectorName(allFlatEmployees, row.direct_supervisor_id)
        }}</span>
      </template>
    </vxe-column>
    <vxe-column
      field="control"
      width="100px"
      align="center"
      v-if="isEditable && attributes.length"
      fixed="right"
      key="control"
    >
      <template #header>
        <span>{{ $t('operation') }}</span>
        <template>
          <a-popover
            :title="$t('cs.companyStructure.selectDisplayColumn')"
            placement="bottom"
            v-model="visible"
            trigger="click"
            v-if="tableType == 'structure'"
            @visibleChange="visibleChange"
            destroyTooltipOnHide
          >
            <template slot="content">
              <div :style="{ maxHeight: `${windowHeight - 320}px`, overflowY: 'auto', width: '160px' }">
                <a-checkbox-group v-model="unsbmitCheckedCols" :options="options" style="display: grid;">
                </a-checkbox-group>
              </div>
              <div
                :style="{
                  marginTop: '5px',
                  height: '20px',
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'flex-end',
                }"
              >
                <a-button :style="{ marginRight: '10px' }" size="small" @click="handleCancel">{{ $t('cancel') }}</a-button>
                <a-button size="small" @click="handleSubmit" type="primary">{{ $t('confirm') }}</a-button>
              </div>
            </template>
            <a-icon type="control" style="cursor: pointer;" />
          </a-popover>
        </template>
      </template>
      <template #default="{ row }">
        <a-space v-if="tableType === 'structure'">
          <a><a-icon type="edit" @click="openEmployeeModal(row, 'edit')"/></a>
          <a-tooltip>
            <template slot="title">
              {{ $t('cs.companyStructure.resetPassword') }}
            </template>
            <a><a-icon type="reload" @click="openBatchModal('password', row)"/></a>
          </a-tooltip>
          <a-tooltip v-if="!row.block">
            <template slot="title">
              {{ $t('cs.companyStructure.block') }}
            </template>
            <a :style="{ color: 'red' }" @click="openBatchModal('block', row, 1)">
              <ops-icon type="icon-xianxing-weilianjie" />
            </a>
          </a-tooltip>
          <a-tooltip v-else>
            <template slot="title">
              {{ $t('cs.companyStructure.recover') }}
            </template>
            <a @click="openBatchModal('block', row, 0)">
              <ops-icon type="icon-xianxing-yilianjie" />
            </a>
          </a-tooltip>
        </a-space>
        <a-tooltip v-else>
          <template slot="title">
            {{ $t('cs.role.remove') }}
          </template>
          <a :style="{ color: 'red' }" @click="removeEmployee(row)">
            <ops-icon type="icon-xianxing-shanchuyonghu" />
          </a>
        </a-tooltip>
      </template>
    </vxe-column>
    <template #empty>
      <div>
        <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
        <div>{{ $t('noData') }}</div>
      </div>
    </template>
  </vxe-table>
</template>

<script>
import { mapState } from 'vuex'
import { getDepartmentName, getDirectorName } from '@/utils/util'
import Bus from '../companyStructure/eventBus/bus'
import Sortable from 'sortablejs'
import XEUtils from 'xe-utils'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'

export default {
  name: 'EmployeeTable',
  components: { OpsMoveIcon },
  props: {
    tableData: {
      type: Array,
      default: () => [],
    },
    tableHeight: {
      type: Number,
      default: 0,
    },
    tableType: {
      type: String,
      default: 'structure',
    },
    isEditable: {
      type: Boolean,
      default: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    const options = [
      { label: this.$t('cs.companyStructure.nickname'), value: 'nickname' },
      { label: this.$t('cs.companyStructure.username'), value: 'username' },
      { label: this.$t('cs.companyStructure.email'), value: 'email' },
      { label: this.$t('cs.companyStructure.sex'), value: 'sex' },
      { label: this.$t('cs.companyStructure.mobile'), value: 'mobile' },
      { label: this.$t('cs.companyStructure.departmentName'), value: 'department_name' },
      { label: this.$t('cs.companyStructure.positionName'), value: 'position_name' },
      { label: this.$t('cs.companyStructure.supervisor'), value: 'direct_supervisor_id' },
    ]
    const checkedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols')) || [
      'nickname',
      'username',
      'email',
      'sex',
      'mobile',
      'department_name',
      'position_name',
      'direct_supervisor_id',
    ]
    return {
      filterRoleList: [],
      options,
      checkedCols,
      unsbmitCheckedCols: [],
      visible: false,
      tableDragClassName: [], // 表格拖拽的参数
      attributes: [],
    }
  },
  inject: ['provide_allFlatEmployees', 'provide_allFlatDepartments'],
  computed: {
    internOptions() {
      return [
        { label: this.$t('cs.companyStructure.fullTime'), value: 0 },
        { label: this.$t('cs.companyStructure.internship'), value: 1 },
      ]
    },
    internMap() {
      return [
        {
          id: 0,
          label: this.$t('cs.companyStructure.fullTime'),
        },
        {
          id: 1,
          label: this.$t('cs.companyStructure.internship'),
        },
      ]
    },
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    },
    allFlatDepartments() {
      return this.provide_allFlatDepartments()
    },
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  created() {
    Bus.$on('reqExportSelectEvent', () => {
      this.exportExcel()
    })
    this.unsbmitCheckedCols = this.checkedCols
  },
  beforeDestroy() {
    Bus.$off('reqExportSelectEvent')
  },
  mounted() {
    // 无编辑权限移除字段的缓存
    if (!this.isEditable && localStorage.getItem('setting-table-CheckedCols')) {
      localStorage.removeItem('setting-table-CheckedCols')
    }
    setTimeout(() => {
      // table拖拽
      this.columnDrop()
    }, 1000)
  },
  watch: {
    tableData(newVal, oldVal) {
      newVal && this.initAttributes()
    },
  },
  methods: {
    getDepartmentName,
    getDirectorName,
    getVxetableRef() {
      return this.$refs.employeeTable
    },
    initAttributes() {
      // 过滤用户没有权限的字段
      if (this.tableData.length) {
        const attributes = Object.keys(this.tableData[0]) // 获取用户有查看权限的所有字段
        // attributes = attributes.filter(v => v !== 'nickname')
        this.options.forEach((item) => {
          if (!attributes.includes(item.value)) {
            if (!attributes.includes('educational_experience') && !attributes.includes('children_information')) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('educational_experience') &&
              (item.value !== 'school' ||
                item.value !== 'major' ||
                item.value !== 'education' ||
                item.value !== 'graduation_year') &&
              !attributes.includes('children_information')
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('children_information') &&
              (item.value !== 'name' ||
                item.value !== 'gender' ||
                item.value !== 'birthday' ||
                item.value !== 'parental_leave_left') &&
              !attributes.includes('educational_experience')
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('educational_experience') &&
              attributes.includes('children_information') &&
              ![
                'school',
                'major',
                'education',
                'graduation_year',
                'name',
                'gender',
                'birthday',
                'parental_leave_left',
              ].includes(item.value)
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            }
          }
        })
        this.attributes = attributes
        localStorage.setItem('setting-table-attributes', JSON.stringify(this.attributes))
      } else {
        if (localStorage.getItem('setting-table-attributes')) {
          this.attributes = JSON.parse(localStorage.getItem('setting-table-attributes'))
        } else {
          this.attributes = []
          this.options = []
        }
      }
      Bus.$emit('getAttributes', this.attributes)
      this.$emit('tranferAttributes', this.attributes)
    },
    getIsInterInship(is_internship) {
      return this.internMap.filter((item) => item.id === is_internship)[0]['label']
    },
    sortChangeEvent(data) {
      this.$emit('sortChangeEvent', data)
    },
    filterChangeEvent(data) {
      this.$emit('filterChangeEvent', data)
    },
    onSelectChange(data) {
      this.$emit('onSelectChange', data)
    },
    openEmployeeModal(row, type) {
      this.$emit('openEmployeeModal', row, type)
    },
    openBatchModal(type, row, state) {
      this.$emit('openBatchModal', type, row, state)
    },
    removeEmployee(row) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cs.role.confirmRemoveEmployee'),
        onOk() {
          that.$emit('removeEmployee', row)
        },
      })
    },
    contentMethod({ column }) {
      if (column.property === 'role') {
        return ''
      }
      return null
    },
    // table中上次登录时间如果后端返回None则显示为空
    formatDate(row) {
      if (row.cellValue === 'None') {
        return ''
      } else {
        return XEUtils.toDateString(row.cellValue, 'yyyy-MM-dd HH:mm:ss')
      }
    },
    // onChange(checkedValues) {
    //   localStorage.setItem('setting-table-CheckedCols', JSON.stringify(checkedValues))
    // },
    visibleChange(changeValue) {
      // 避免用户勾选字段时popover自动关闭
      if (!changeValue) {
        this.visible = true
      }
    },
    handleCancel() {
      if (JSON.parse(localStorage.getItem('setting-table-CheckedCols'))) {
        this.unsbmitCheckedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols'))
      } else {
        this.unsbmitCheckedCols = this.checkedCols
      }
      this.visible = false
    },
    handleSubmit() {
      this.visible = false
      localStorage.setItem('setting-table-CheckedCols', JSON.stringify(this.unsbmitCheckedCols))
      this.$nextTick(() => {
        this.checkedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols'))
      })
    },
    // 导出excel
    exportExcel() {
      const now = new Date()
      const year = now.getFullYear() // 获取完整的年份(4位,1970-????)
      const month = now.getMonth() + 1 // 获取当前月份(0-11,0代表1月)
      const today = now.getDate() // 获取当前日(1-31)
      const hour = now.getHours() // 获取当前小时数(0-23)
      const minute = now.getMinutes() // 获取当前分钟数(0-59)
      const second = now.getSeconds() // 获取当前秒数(0-59)
      const now_time =
        year +
        this.fillZero(month) +
        this.fillZero(today) +
        this.fillZero(hour) +
        this.fillZero(minute) +
        this.fillZero(second)
      this.$refs.employeeTable.exportData({
        data: this.$refs.employeeTable.getCheckboxRecords().map((item) => {
          return {
            ...item,
            is_internship: item.is_internship ? '实习生' : '正式',
            direct_supervisor_id: getDirectorName(this.allFlatEmployees, item.direct_supervisor_id),
          }
        }),
        filename: 'employee-' + now_time,
        sheetName: 'Sheet1',
        type: 'xlsx',
        types: ['xlsx', 'csv', 'html', 'xml', 'txt'],
        useStyle: true, // 是否导出样式
        isFooter: false, // 是否导出表尾（比如合计）
        // 过滤那个字段导出
        columnFilterMethod: function(column, $columnIndex) {
          return !(column.$columnIndex === 0)
          // 0是复选框 不导出
        },
      })
      this.$refs.employeeTable.clearCheckboxRow()
      this.$refs.employeeTable.clearCheckboxReserve()
      this.$refs.employeeTable.clearSort()
      this.tableSortData = undefined
      Bus.$emit('changeSelectedRowKeys', [])
    },
    fillZero(str) {
      let realNum
      if (str < 10) {
        realNum = '0' + str
      } else {
        realNum = str
      }
      return realNum
    },
    columnDrop() {
      this.$nextTick(() => {
        if (this.$refs.employeeTable) {
          const xTable = this.$refs.employeeTable
          this.sortable = Sortable.create(
            xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row'),
            {
              handle: '.vxe-handle',
              onChoose: () => {
                const header = xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row')
                const classNameList = []
                header.childNodes.forEach((item) => {
                  classNameList.push(item.classList[1])
                })
                this.tableDragClassName = classNameList
              },
              onEnd: (params) => {
                // 由于开启了虚拟滚动，newIndex和oldIndex是虚拟的
                const { newIndex, oldIndex } = params
                // 从tableDragClassName拿到colid
                const fromColid = this.tableDragClassName[oldIndex]
                const toColid = this.tableDragClassName[newIndex]
                const fromColumn = xTable.getColumnById(fromColid)
                const toColumn = xTable.getColumnById(toColid)
                const fromIndex = xTable.getColumnIndex(fromColumn)
                const toIndex = xTable.getColumnIndex(toColumn)
                const tableColumn = xTable.getColumns()
                const currRow = tableColumn.splice(fromIndex, 1)[0]
                tableColumn.splice(toIndex, 0, currRow)
                xTable.reloadColumn(tableColumn)
              },
            }
          )
        }
      })
    },
  },
}
</script>
<style lang="less" scoped>
.vxe-handle {
  cursor: move;
  .move-icon {
    display: none;
    width: 17px;
    height: 17px;
    display: none;
    position: absolute;
    left: -3px;
    top: 12px;
  }
  &:hover > .move-icon {
    display: inline !important;
  }
}
</style>
