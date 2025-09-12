<template>
  <div id="ciIndex" class="cmdb-ci">
    <a-spin :tip="loadTip" :spinning="loading" >
      <div class="cmdb-views-header">
        <span>
          <span class="cmdb-views-header-title">{{ CIType.alias || CIType.name }}</span>
          <span
            @click="
              () => {
                $refs.metadataDrawer.open(typeId)
              }
            "
            class="cmdb-views-header-metadata"
          >
            <a-icon type="info-circle" />{{ $t('cmdb.ci.attributeDesc') }}
          </span>
        </span>
        <a-space>
          <a-button
            type="primary"
            class="ops-button-ghost"
            ghost
            @click="$refs.create.handleOpen(true, 'create')"
          ><ops-icon type="veops-increase" />
            {{ $t('create') }}
          </a-button>
          <EditAttrsPopover :typeId="typeId" class="operation-icon" @refresh="refreshAfterEditAttrs">
            <a-button
              type="primary"
              ghost
              class="ops-button-ghost"
            ><ops-icon type="veops-configuration_table" />{{ $t('cmdb.configTable') }}</a-button
            >
          </EditAttrsPopover>
          <a-dropdown v-model="visible">
            <a-button type="primary" ghost class="ops-button-ghost">···</a-button>
            <a-menu slot="overlay" @click="handleMenuClick">
              <a-menu-item @click="handlePerm" key="grant">
                <a-icon type="user-add" />
                {{ $t('grant') }}
              </a-menu-item>
              <a-menu-item
                v-if="!autoSub.enabled"
                key="cancelSub"
                @click="unsubscribe"
              >
                <a-icon type="star" />
                {{ $t('cmdb.preference.cancelSub') }}
              </a-menu-item>
              <a-menu-item
                key="citypeConfig"
                @click="handleCITypeConfig"
              >
                <ops-icon type="ops-cmdb-citype" />
                {{ $t('cmdb.menu.citypeManage') }}
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </a-space>
      </div>
      <div class="cmdb-ci-main">
        <SearchForm
          ref="search"
          @refresh="handleSearch"
          :preferenceAttrList="preferenceAttrList"
          :typeId="typeId"
          :selectedRowKeys="selectedRowKeys"
          @copyExpression="copyExpression"
        >
          <PreferenceSearch
            ref="preferenceSearch"
            v-show="!selectedRowKeys.length"
            @getQAndSort="getQAndSort"
            @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
          />
          <div class="ops-list-batch-action" v-show="!!selectedRowKeys.length">
            <span @click="$refs.create.handleOpen(true, 'update')">{{ $t('update') }}</span>
            <a-divider type="vertical" />
            <span @click="openBatchDownload">{{ $t('download') }}</span>
            <a-divider type="vertical" />
            <span @click="batchDelete">{{ $t('delete') }}</span>
            <a-divider type="vertical" />
            <span @click="batchRollback">{{ $t('cmdb.ci.rollback') }}</span>
            <span>{{ $t('cmdb.ci.selectRows', { rows: selectedRowKeys.length }) }}</span>
          </div>
        </SearchForm>
        <CiDetailDrawer ref="detail" :typeId="typeId" />

        <CITable
          ref="xTable"
          :id="`cmdb-ci-${typeId}`"
          :loading="loading"
          :attrList="preferenceAttrList"
          :columns="columns"
          :passwordValue="passwordValue"
          :data="instanceList"
          :height="tableHeight"
          @onSelectChange="onSelectChange"
          @edit-closed="handleEditClose"
          @edit-actived="handleEditActived"
          @sort-change="handleSortCol"
          @openDetail="openDetail"
          @deleteCI="deleteCI"
        />

        <div :style="{ textAlign: 'right', marginTop: '4px' }">
          <a-pagination
            :showSizeChanger="true"
            :current="currentPage"
            size="small"
            :total="totalNumber"
            show-quick-jumper
            :page-size="pageSize"
            :page-size-options="pageSizeOptions"
            @showSizeChange="onShowSizeChange"
            :show-total="
              (total, range) =>
                $t('pagination.total', {
                  range0: range[0],
                  range1: range[1],
                  total,
                })
            "
            @change="
              (page) => {
                currentPage = page
              }
            "
          >
            <template slot="buildOptionText" slot-scope="props">
              <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
              <span v-if="props.value === '100000'">{{ $t('cmdb.ci.all') }}</span>
            </template>
          </a-pagination>
        </div>
        <create-instance-form
          ref="create"
          :typeIdFromProp="typeId"
          @reload="reloadData"
          @submit="batchUpdate"
        />
        <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
        <CiRollbackForm ref="ciRollbackForm" @batchRollbackAsync="batchRollbackAsync($event)" :ciIds="selectedRowKeys" />
        <MetadataDrawer ref="metadataDrawer" />
        <CMDBGrant ref="cmdbGrant" resourceTypeName="CIType" app_id="cmdb" />
      </div>
    </a-spin>
  </div>
</template>

<script>
import _ from 'lodash'
import Sortable from 'sortablejs'

import { searchCI, updateCI, deleteCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes, subscribeCIType, subscribeTreeView } from '@/modules/cmdb/api/preference'
import { getCITypeAttributesById, getAttrPassword } from '@/modules/cmdb/api/CITypeAttr'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import { CIBaselineRollback } from '@/modules/cmdb/api/history'

import { getCITableColumns } from '../../utils/helper'
import { intersection } from '@/utils/functions/set'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import MetadataDrawer from './modules/MetadataDrawer.vue'
import CMDBGrant from '../../components/cmdbGrant'
import CiRollbackForm from './modules/ciRollbackForm.vue'
import SearchForm from '@/modules/cmdb/components/searchForm/SearchForm.vue'
import CreateInstanceForm from './modules/CreateInstanceForm'
import CiDetailDrawer from './modules/ciDetailDrawer.vue'
import EditAttrsPopover from './modules/editAttrsPopover'
import CITable from '@/modules/cmdb/components/ciTable/index.vue'

export default {
  name: 'InstanceList',
  components: {
    SearchForm,
    CreateInstanceForm,
    CiDetailDrawer,
    EditAttrsPopover,
    BatchDownload,
    PreferenceSearch,
    MetadataDrawer,
    CMDBGrant,
    CiRollbackForm,
    CITable
  },
  props: {
    typeId: {
      type: Number,
      default: undefined
    },
    CIType: {
      type: Object,
      default: () => {}
    },
    autoSub: {
      type: Object,
      default: () => {}
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      // if (this.selectedRowKeys && this.selectedRowKeys.length) {
      //   return this.windowHeight - 246
      // }
      return this.windowHeight - 240
    },
  },
  data() {
    return {
      tableData: [],
      loading: false,
      currentPage: 1,
      pageSizeOptions: ['50', '100', '200', '100000'],
      pageSize: 50,
      totalNumber: 0,
      loadTip: '',
      form: this.$form.createForm(this),
      preferenceAttrList: [],

      instanceList: [],
      columns: [],
      // custom table alert & rowSelection
      selectedRowKeys: [],
      // Check whether to edit
      initialInstanceList: [],
      sortByTable: undefined,
      isEditActive: false,
      attrList: [],
      attributes: {},
      // Table drag parameters
      tableDragClassName: [],

      resource_type: {},

      initialPasswordValue: {},
      passwordValue: {},
      lastEditCiId: null,
      isContinueCloseEdit: true,
      visible: false,
    }
  },
  watch: {
    currentPage: function(newVal, oldVal) {
      this.loadTableData(this.sortByTable)
    },
  },
  provide() {
    return {
      handleSearch: this.handleSearch,
      setPreferenceSearchCurrent: this.setPreferenceSearchCurrent,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      },
      filterCompPreferenceSearch: () => {
        return { type_id: this.typeId }
      },
      resource_type: () => {
        return this.resource_type
      }
    }
  },
  async mounted() {
    this.loading = true
    await this.getAttributeList()
    await this.loadPreferenceAttrList()
    await this.loadTableData()
    this.loading = false

    this.$nextTick(() => {
      const loadingNode = document.getElementsByClassName('ant-drawer-mask')
      if (loadingNode?.style) {
        loadingNode.style.zIndex = 8
      }
    })
    setTimeout(() => {
      this.columnDrop()
    }, 1000)
  },
  beforeDestroy() {
    // window.onkeypress = null
    if (this.sortable) {
      this.sortable.destroy()
    }
  },
  methods: {
    async getAttributeList() {
      await getCITypeAttributesById(this.typeId).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },
    handleSearch() {
      this.$refs.xTable.getVxetableRef().clearSort()
      this.sortByTable = undefined
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.reloadData()
        } else {
          this.currentPage = 1
        }
      })
    },
    async loadTableData(sortByTable = undefined) {
      try {
        this.loading = true
        // If fuzzy search is possible, queryParam can be deleted later.
        // const queryParams = this.$refs['search'].queryParam || {}
        const fuzzySearch = this.$refs['search'].fuzzySearch
        const expression = this.$refs['search'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
        const regSort = /(?<=sort=).+/g

        const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
        let sort
        if (sortByTable) {
          sort = sortByTable
        } else {
          sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
        }
        const res = await searchCI({
          q: `_type:${this.typeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
          count: this.pageSize,
          page: this.currentPage,
          sort,
        })
        this.totalNumber = res['numfound']
        this.columns = this.getColumns(res.result, this.preferenceAttrList)
        this.columns.forEach((col) => {
          if (col.is_password) {
            this.initialPasswordValue[col.field] = ''
            this.passwordValue[col.field] = ''
          }
        })
        const jsonAttrList = this.attrList.filter((attr) => attr.value_type === '6')
        this.instanceList = res['result'].map((item) => {
          jsonAttrList.forEach(
            (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
          )
          return { ..._.cloneDeep(item) }
        })
        this.initialInstanceList = _.cloneDeep(this.instanceList)
        this.$nextTick(() => {
          // this.setSelectRows()
          this.$refs.xTable.getVxetableRef().refreshColumn()
        })
      } finally {
        this.loading = false
      }
    },
    getColumns(data, attrList) {
      const width = document.getElementById('ciIndex').clientWidth - 50
      return getCITableColumns(data, attrList, width)
    },
    setSelectRows() {
      const cached = new Set(this.selectedRowKeys)
      const loaded = new Set(this.instanceList.map((i) => i.ci_id || i._id))

      const inter = Array.from(intersection(cached, loaded))

      if (inter.length === this.instanceList.length) {
        this.$refs['xTable'].getVxetableRef().setAllCheckboxRow(true)
      } else {
        const rows = []
        inter.forEach((rid) => {
          rows.push(this.$refs['xTable'].getVxetableRef().getRowById(rid))
        })
        this.$refs['xTable'].getVxetableRef().setCheckboxRow(rows, true)
      }
    },
    async loadPreferenceAttrList() {
      const subscribed = await getSubscribeAttributes(this.typeId)
      this.preferenceAttrList = subscribed.attributes // All columns that have been subscribed
    },
    onSelectChange(records) {
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
    },
    reloadData() {
      this.loadTableData()
    },

    handleEditClose({ row, rowIndex, column }) {
      if (!this.isContinueCloseEdit) {
        return
      }
      const $table = this.$refs['xTable'].getVxetableRef()
      const data = {}
      this.columns.forEach((item) => {
        if (
          !(item.field in this.initialPasswordValue) &&
          !_.isEqual(row[item.field], this.initialInstanceList[rowIndex][item.field])
        ) {
          data[item.field] = row[item.field] ?? null
        }
      })
      Object.keys(this.initialPasswordValue).forEach((key) => {
        if (this.initialPasswordValue[key] !== this.passwordValue[key]) {
          data[key] = this.passwordValue[key]
          row[key] = this.passwordValue[key]
        }
      })
      this.isEditActive = false
      this.lastEditCiId = null
      if (JSON.stringify(data) !== '{}') {
        updateCI(row.ci_id || row._id, data)
          .then(() => {
            this.$message.success(this.$t('saveSuccess'))
            $table.reloadRow(row, null)
            const _initialInstanceList = _.cloneDeep(this.initialInstanceList)
            _initialInstanceList[rowIndex] = {
              ..._initialInstanceList[rowIndex],
              ...data,
            }
            this.initialInstanceList = _initialInstanceList
          })
          .catch((err) => {
            console.log(err)
            this.loadTableData()
          })
      }
      this.columns.forEach((col) => {
        if (col.is_password) {
          this.initialPasswordValue[col.field] = ''
          this.passwordValue[col.field] = ''
        }
      })
    },

    async openBatchDownload() {
      this.$refs.batchDownload.open({
        preferenceAttrList: this.preferenceAttrList.filter((attr) => !attr?.is_reference),
        ciTypeName: this.CIType.alias || this.CIType.name,
      })
    },
    batchDownload({ filename, type, checkedKeys }) {
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.attrList.find((attr) => attr.name === key)
        if (_find && _find.value_type === '6') jsonAttrList.push(key)
      })
      const data = _.cloneDeep([
        ...this.$refs.xTable.getVxetableRef().getCheckboxReserveRecords(),
        ...this.$refs.xTable.getVxetableRef().getCheckboxRecords(true),
      ])
      this.$refs.xTable.getVxetableRef().exportData({
        filename,
        type,
        columnFilterMethod({ column }) {
          return checkedKeys.includes(column.property)
        },
        data: [
          ...data.map((item) => {
            jsonAttrList.forEach((jsonAttr) => (item[jsonAttr] = item[jsonAttr] ? JSON.stringify(item[jsonAttr]) : ''))
            return { ...item }
          }),
        ],
      })
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
    },
    batchUpdate(values) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ci.batchUpdateConfirm'),
        async onOk() {
          that.batchUpdateAsync(values)
        },
      })
    },
    async batchUpdateAsync(values) {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.batchUpdateInProgress') + '...'
      const payload = {}
      Object.keys(values).forEach((key) => {
        // Field values support blanking
        // There are currently field values that do not support blanking and will be returned by the backend.
        if (values[key] === undefined || values[key] === null) {
          payload[key] = null
        } else {
          payload[key] = values[key]
        }
      })
      this.$refs.create.visible = false
      const key = 'updatable'
      let errorMsg = ''
      for (let i = 0; i < this.selectedRowKeys.length; i++) {
        await updateCI(this.selectedRowKeys[i], payload, false)
          .then(() => {
            successNum += 1
          })
          .catch((error) => {
            errorMsg = errorMsg + '\n' + `${this.selectedRowKeys[i]}:${error.response?.data?.message ?? ''}`
            this.$notification.warning({
              key,
              message: this.$t('warning'),
              description: errorMsg,
              duration: 0,
              style: { whiteSpace: 'break-spaces', overflow: 'auto', maxHeight: this.windowHeight - 80 + 'px' },
            })
            errorNum += 1
          })
          .finally(() => {
            this.loadTip = this.$t('cmdb.ci.batchUpdateInProgress2', {
              total: this.selectedRowKeys.length,
              successNum: successNum,
              errorNum: errorNum,
            })
          })
      }
      this.loading = false
      this.loadTip = ''
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.reloadData()
    },
    batchDelete() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          that.batchDeleteAsync()
        },
      })
    },
    async batchDeleteAsync() {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.batchDeleting')
      const floor = Math.ceil(this.selectedRowKeys.length / 6)
      for (let i = 0; i < floor; i++) {
        const itemList = this.selectedRowKeys.slice(6 * i, 6 * i + 6)
        const promises = itemList.map((x) => deleteCI(x, false))
        await Promise.allSettled(promises)
          .then((res) => {
            res.forEach((r) => {
              if (r.status === 'fulfilled') {
                successNum += 1
              } else {
                errorNum += 1
              }
            })
          })
          .finally(() => {
            this.loadTip = this.$t('cmdb.ci.batchDeleting2', {
              total: this.selectedRowKeys.length,
              successNum: successNum,
              errorNum: errorNum,
            })
          })
      }
      this.loading = false
      this.loadTip = ''
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData()
        } else {
          this.currentPage = 1
        }
      })
    },
    deleteCI(record) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            // that.$refs.table.refresh(true)
            that.$message.success(that.$t('deleteSuccess'))
            that.reloadData()
          })
        },
      })
    },
    batchRollback() {
      this.$nextTick(() => {
        this.$refs.ciRollbackForm.onOpen(true)
      })
    },
    async batchRollbackAsync(params) {
      const mask = document.querySelector('.ant-drawer-mask')
      const oldValue = mask.style.zIndex
      mask.style.zIndex = 2
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.rollbackingTips')
      const floor = Math.ceil(this.selectedRowKeys.length / 6)
      for (let i = 0; i < floor; i++) {
        const itemList = this.selectedRowKeys.slice(6 * i, 6 * i + 6)
        const promises = itemList.map((x) => CIBaselineRollback(x, params))
        await Promise.allSettled(promises)
          .then((res) => {
            res.forEach((r) => {
              if (r.status === 'fulfilled') {
                successNum += 1
              } else {
                errorNum += 1
              }
            })
          })
          .finally(() => {
            this.loadTip = this.$t('cmdb.ci.batchRollbacking', {
              total: this.selectedRowKeys.length,
              successNum: successNum,
              errorNum: errorNum,
            })
          })
      }
      this.loading = false
      this.loadTip = ''
      mask.style.zIndex = oldValue
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData()
        } else {
          this.currentPage = 1
        }
      })
    },
    async refreshAfterEditAttrs() {
      await this.loadPreferenceAttrList()
      await this.loadTableData()
    },
    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize
      if (this.currentPage === 1) {
        this.reloadData()
      } else {
        this.currentPage = 1
      }
      setTimeout(() => {
        // this.setSelectRows()
      }, 500)
    },
    handleSortCol({ column, property, order, sortBy, sortList, $event }) {
      let sortByTable
      if (order === 'asc') {
        sortByTable = property
      } else if (order === 'desc') {
        sortByTable = `-${property}`
      }
      this.sortByTable = sortByTable
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData(sortByTable)
        } else {
          this.currentPage = 1
        }
      })
    },
    columnDrop() {
      this.$nextTick(() => {
        const xTable = this.$refs?.xTable?.getVxetableRef?.()
        if (!xTable) {
          return
        }

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
              xTable.loadColumn(tableColumn)
            },
          }
        )
      })
    },
    handleEditActived() {
      this.isEditActive = true
      const passwordCol = this.columns.filter((col) => col.is_password)
      this.$nextTick(() => {
        const editRecord = this.$refs.xTable.getVxetableRef().getEditRecord()
        const { row, column } = editRecord
        if (passwordCol.length && this.lastEditCiId !== row._id) {
          this.$nextTick(async () => {
            for (let i = 0; i < passwordCol.length; i++) {
              await getAttrPassword(row._id, passwordCol[i].attr_id).then((res) => {
                this.initialPasswordValue[passwordCol[i].field] = res.value
                this.passwordValue[passwordCol[i].field] = res.value
              })
            }
            this.isContinueCloseEdit = false
            await this.$refs.xTable.getVxetableRef().clearEdit()
            this.isContinueCloseEdit = true
            this.$nextTick(() => {
              this.$refs.xTable.getVxetableRef().setEditCell(row, column.field)
            })
          })
        }
        this.lastEditCiId = row._id
      })
    },
    getQAndSort() {
      const fuzzySearch = this.$refs['search'].fuzzySearch || ''
      const expression = this.$refs['search'].expression || ''
      this.$refs.preferenceSearch.savePreference({ fuzzySearch, expression })
    },
    setParamsFromPreferenceSearch(item) {
      const { fuzzySearch, expression } = item.option
      this.$refs.search.fuzzySearch = fuzzySearch
      this.$refs.search.expression = expression
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.xTable.getVxetableRef().clearSort()
      this.sortByTable = undefined
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData()
        } else {
          this.currentPage = 1
        }
      })
    },
    setPreferenceSearchCurrent(id = null) {
      this.$refs.preferenceSearch.currentPreferenceSearch = id
    },
    copyExpression() {
      const expression = this.$refs['search'].expression || ''
      const fuzzySearch = this.$refs['search'].fuzzySearch

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      const text = `q=_type:${this.typeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },
    unsubscribe() {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.preference.confirmcancelSub2', {
          name: `${this.CIType.alias || this.CIType.name}`,
        }),
        onOk: () => {
          const promises = [subscribeCIType(this.typeId, ''), subscribeTreeView(this.typeId, '')]
          Promise.all(promises).then(() => {
            this.$message.success(this.$t('cmdb.preference.cancelSubSuccess'))
            this.$emit('unSubscribe')
          })
        },
      })
    },

    handleCITypeConfig() {
      const { id, name } = this.CIType || {}
      if (id && name) {
        roleHasPermissionToGrant({
          app_id: 'cmdb',
          resource_type_name: 'CIType',
          perm: 'config',
          resource_name: name,
        }).then((res) => {
          if (res?.result) {
            const storageId = `null%${id}%${name}`
            localStorage.setItem('ops_cityps_currentId', storageId)
            localStorage.setItem('ops_model_config_tab_key', '1')
            window.open('/cmdb/ci_types', '_blank')
          } else {
            this.$message.error(this.$t('noPermission'))
          }
        })
      }
    },

    handlePerm() {
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'CIType',
        perm: 'grant',
        resource_name: this.CIType.name,
      }).then((res) => {
        if (res.result) {
          searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
            this.resource_type = { groups: res.groups, id2perms: res.id2perms }
            this.$nextTick(() => {
              this.$refs.cmdbGrant.open({
                name: this.CIType.name,
                cmdbGrantType: 'ci',
                CITypeId: this.typeId,
              })
            })
          })
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },
    handleMenuClick(e) {
      if (e.key === 'grant') {
        this.visible = false
      }
    },
    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$refs.detail.create(id, activeTabKey, ciDetailRelationKey)
    }
  },
}
</script>

<style lang="less">
@import '../index.less';
</style>

<style lang="less" scoped>
.cmdb-ci {
  background-color: #fff;
  padding: 20px;
  border-radius: @border-radius-box;
  height: calc(100vh - 64px);
  overflow: auto;
  margin-bottom: -24px;
}
</style>
