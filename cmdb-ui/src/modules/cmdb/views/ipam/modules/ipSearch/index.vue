<template>
  <div ref="wrapRef">
    <a-spin :tip="loadTip" :spinning="loading" >
      <div class="table-header">
        <SearchForm
          ref="search"
          :preferenceAttrList="preferenceAttrList"
          :typeId="addressCITypeId"
          :selectedRowKeys="selectedRowKeys"
          @copyExpression="copyExpression"
          @refresh="handleSearch"
        >
          <div class="ops-list-batch-action" v-show="!!selectedRowKeys.length">
            <span @click="$refs.create.handleOpen(true, 'update')">{{ $t('update') }}</span>
            <a-divider type="vertical" />
            <span @click="openBatchDownload">{{ $t('download') }}</span>
            <a-divider type="vertical" />
            <span @click="batchDelete">{{ $t('delete') }}</span>
            <span>{{ $t('cmdb.ci.selectRows', { rows: selectedRowKeys.length }) }}</span>
          </div>
        </SearchForm>

        <div class="table-header-right">
          <EditAttrsPopover
            :typeId="addressCITypeId"
            @refresh="refreshAfterEditAttrs"
          >
            <a-button
              type="primary"
              ghost
              class="ops-button-ghost"
            >
              <ops-icon type="veops-configuration_table" />
              {{ $t('cmdb.configTable') }}
            </a-button>
          </EditAttrsPopover>
        </div>
      </div>

      <CITable
        ref="xTable"
        :loading="loading"
        :attrList="preferenceAttrList"
        :columns="columns"
        :data="instanceList"
        :height="tableHeight"
        @sort-change="handleSortCol"
        @openDetail="openDetail"
        @deleteCI="deleteCI"
        @onSelectChange="onSelectChange"
      />

      <div class="table-pagination">
        <a-pagination
          :showSizeChanger="true"
          :current="page"
          size="small"
          :total="totalNumber"
          show-quick-jumper
          :page-size="pageSize"
          :page-size-options="pageSizeOptions"
          :show-total="
            (total, range) =>
              $t('pagination.total', {
                range0: range[0],
                range1: range[1],
                total,
              })
          "
          @change="handleChangePage"
          @showSizeChange="onShowSizeChange"
        >
          <template slot="buildOptionText" slot-scope="props">
            <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
            <span v-if="props.value === '100000'">{{ $t('cmdb.ci.all') }}</span>
          </template>
        </a-pagination>
      </div>
    </a-spin>

    <BatchDownload
      ref="batchDownload"
      :showFileTypeSelect="false"
      @batchDownload="batchDownload"
    />

    <CIDetailDrawer ref="detail" :typeId="addressCITypeId" />

    <CreateInstanceForm
      ref="create"
      :typeIdFromRelation="addressCITypeId"
      @submit="batchUpdate"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import ExcelJS from 'exceljs'
import FileSaver from 'file-saver'
import { searchCI, deleteCI, updateCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCITableColumns } from '@/modules/cmdb/utils/helper'

import SearchForm from '@/modules/cmdb/components/searchForm/SearchForm.vue'
import CITable from '@/modules/cmdb/components/ciTable/index.vue'
import BatchDownload from '@/modules/cmdb/components/batchDownload/batchDownload.vue'
import CIDetailDrawer from '@/modules/cmdb/views/ci/modules/ciDetailDrawer.vue'
import EditAttrsPopover from '@/modules/cmdb/views/ci/modules/editAttrsPopover.vue'
import CreateInstanceForm from '@/modules/cmdb/views/ci/modules/CreateInstanceForm'

export default {
  name: 'IPSearch',
  components: {
    SearchForm,
    CITable,
    BatchDownload,
    CIDetailDrawer,
    EditAttrsPopover,
    CreateInstanceForm
  },
  props: {
    addressCIType: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
      loading: false,
      loadTip: '',
      sortByTable: undefined,

      instanceList: [],
      totalNumber: 0,
      columns: [],
      preferenceAttrList: [],
      attrList: [],
      attributes: {},
      selectedRowKeys: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return this.windowHeight - 260
    },
    addressCITypeId() {
      return this.addressCIType?.id || null
    }
  },
  provide() {
    return {
      handleSearch: this.getTableData,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      }
    }
  },
  async mounted() {
    this.$nextTick(async () => {
      if (this.addressCITypeId) {
        await this.getAttributeList()
        await this.getPreferenceAttrList()
        this.getTableData()
      }
    })
  },
  methods: {
    async getAttributeList() {
      await getCITypeAttributesById(this.addressCITypeId).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },

    async getPreferenceAttrList() {
      const subscribed = await getSubscribeAttributes(this.addressCITypeId)
      this.preferenceAttrList = subscribed.attributes
    },

    async getTableData() {
      try {
        this.loading = true
        const fuzzySearch = this.$refs['search'].fuzzySearch
        const expression = this.$refs['search'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
        const regSort = /(?<=sort=).+/g
        const exp = expression.match(regQ) ? expression.match(regQ)[0] : null

        let sort
        if (this.sortByTable) {
          sort = this.sortByTable
        } else {
          sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
        }

        const res = await searchCI({
          q: `_type:${this.addressCITypeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
          count: this.pageSize,
          page: this.page,
          sort,
        })

        this.totalNumber = res?.numfound
        const instanceList = res.result

        const jsonAttrList = this.preferenceAttrList.filter((attr) => attr.value_type === '6')
        instanceList.forEach((item) => {
          jsonAttrList.forEach(
            (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
          )
        })

        this.getColumns(instanceList)
        this.instanceList = instanceList
      } finally {
        this.loading = false
      }
    },

    getColumns(data) {
      const width = this.$refs.wrapRef.clientWidth - 50
      const columns = getCITableColumns(data, this.preferenceAttrList, width)
      columns.forEach((item) => {
        if (item.editRender) {
          item.editRender.enabled = false
        }
      })
      this.columns = columns
    },

    copyExpression() {
      const expression = this.$refs['search'].expression || ''
      const fuzzySearch = this.$refs['search'].fuzzySearch

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      const text = `q=_type:${this.addressCITypeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
    },

    handleSearch() {
      this.$refs.xTable.getVxetableRef().clearSort()
      this.$nextTick(() => {
        this.page = 1
        this.getTableData()
      })
    },

    handleChangePage(page) {
      this.page = page
      this.getTableData()
    },

    onShowSizeChange(_, pageSize) {
      this.page = 1
      this.pageSize = pageSize
      this.getTableData()
    },

    handleSortCol({ property, order }) {
      let sortByTable
      if (order === 'asc') {
        sortByTable = property
      } else if (order === 'desc') {
        sortByTable = `-${property}`
      }

      this.sortByTable = sortByTable
      this.$nextTick(() => {
        this.page = 1
        this.getTableData()
      })
    },

    openBatchDownload() {
      this.$refs.batchDownload.open({
        preferenceAttrList: this.preferenceAttrList,
        ciTypeName: this.$t('cmdb.ipam.ipSearch') || '',
      })
    },

    batchDownload({ checkedKeys, filename }) {
      const wb = new ExcelJS.Workbook()

      const tableRef = this.$refs.xTable.getVxetableRef()
      let tableData = _.cloneDeep([
        ...tableRef.getCheckboxReserveRecords(),
        ...tableRef.getCheckboxRecords(true),
      ])
      if (!tableData.length) {
        const { fullData } = tableRef.getTableData()
        tableData = _.cloneDeep(fullData)
      }

      const ws = wb.addWorksheet(this.tabActive)
      const columns = []

      const attrMap = new Map()
      this.columns.filter((col) => checkedKeys.includes(col.field)).map((col) => {
        attrMap.set(col.field, col)

        columns.push({
          header: col.title || '',
          key: col.field,
          width: 20,
        })
      })

      ws.columns = columns

      tableData.forEach((item) => {
        const row = {}

        columns.forEach(({ key }) => {
          const value = item?.[key] ?? null
          const attr = attrMap.get(key)
          if (attr.valueType === '6') {
            row[key] = value ? JSON.stringify(value) : value
          } else if (attr.is_list && Array.isArray(value)) {
            row[key] = value.join(',')
          } else {
            row[key] = value
          }
        })

        ws.addRow(row)
      })

      wb.xlsx.writeBuffer().then((buffer) => {
        const file = new Blob([buffer], {
          type: 'application/octet-stream',
        })
        FileSaver.saveAs(file, `${filename}.xlsx`)
      })

      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
    },

    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$refs.detail.create(id, activeTabKey, ciDetailRelationKey)
    },

    async refreshAfterEditAttrs() {
      await this.getPreferenceAttrList()
      this.getTableData()
    },

    deleteCI(record) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('confirmDelete'),
        onOk: () => {
          deleteCI(record.ci_id || record._id).then(() => {
            this.$message.success(this.$t('deleteSuccess'))
            this.getTableData()
          })
        },
      })
    },

    onSelectChange(records) {
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
    },

    batchDelete() {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('confirmDelete'),
        onOk: () => {
          this.batchDeleteAsync()
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
        this.page = 1
        this.getTableData()
      })
    },

    batchUpdate(values) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.ci.batchUpdateConfirm'),
        onOk: () => {
          this.batchUpdateAsync(values)
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
      this.getTableData()
    },
  }
}
</script>

<style lang="less" scoped>
.table-header {
  display: flex;
  align-items: baseline;
  width: 100%;
  justify-content: space-between;

  &-right {
    display: flex;
    align-items: center;
    column-gap: 12px;
  }
}
.table-pagination {
  text-align: right;
  margin-top: 4px;
}
</style>
