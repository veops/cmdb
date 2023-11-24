<template>
  <a-modal
    v-model="visible"
    width="90%"
    :closable="false"
    :centered="true"
    :maskClosable="false"
    :destroyOnClose="true"
    @cancel="handleClose"
    @ok="handleOk"
  >
    <div :style="{ width: '100%' }" id="add-table-modal">
      <a-spin :spinning="loading">
        <SearchForm
          ref="searchForm"
          :typeId="addTypeId"
          :preferenceAttrList="preferenceAttrList"
          @refresh="handleSearch"
        />
        <vxe-table
          ref="xTable"
          row-id="_id"
          :data="tableData"
          :height="tableHeight"
          highlight-hover-row
          :checkbox-config="{ reserve: true }"
          @checkbox-change="onSelectChange"
          @checkbox-all="onSelectChange"
          show-overflow="tooltip"
          show-header-overflow="tooltip"
          :scroll-y="{ enabled: true, gt: 50 }"
          :scroll-x="{ enabled: true, gt: 0 }"
          class="ops-stripe-table"
        >
          <vxe-column align="center" type="checkbox" width="60" fixed="left"></vxe-column>
          <vxe-table-column
            v-for="col in columns"
            :key="col.field"
            :title="col.title"
            :field="col.field"
            :width="col.width"
            :sortable="col.sortable"
          >
            <template #default="{row}" v-if="col.value_type === '6'">
              <span v-if="col.value_type === '6' && row[col.field]">{{ JSON.stringify(row[col.field]) }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <a-pagination
          v-model="currentPage"
          size="small"
          :total="totalNumber"
          show-quick-jumper
          :page-size="50"
          :show-total="(total, range) => `当前${range[0]}-${range[1]} 共 ${total}条记录`"
          :style="{ textAlign: 'right', marginTop: '10px' }"
          @change="handleChangePage"
        />
      </a-spin>
    </div>
  </a-modal>
</template>

<script>
/* eslint-disable no-useless-escape */
import { searchCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { batchUpdateCIRelationChildren, batchUpdateCIRelationParents } from '@/modules/cmdb/api/CIRelation'
import { getCITableColumns } from '../../../utils/helper'
import SearchForm from '../../../components/searchForm/SearchForm.vue'
export default {
  name: 'AddTableModal',
  components: { SearchForm },
  data() {
    return {
      visible: false,
      currentPage: 1,
      totalNumber: 0,
      tableData: [],
      columns: [],
      ciObj: {},
      ciId: null,
      addTypeId: null,
      loading: false,
      expression: '',
      isFocusExpression: false,
      type: 'children',
      preferenceAttrList: [],
      ancestor_ids: undefined,
    }
  },
  computed: {
    tableHeight() {
      return this.$store.state.windowHeight - 250
    },
    placeholder() {
      return this.isFocusExpression ? '例：q=os_version:centos&sort=os_version' : '表达式搜索'
    },
    width() {
      return this.isFocusExpression ? '500px' : '100px'
    },
  },
  watch: {},
  methods: {
    async openModal(ciObj, ciId, addTypeId, type, ancestor_ids = undefined) {
      this.visible = true
      this.ciObj = ciObj
      this.ciId = ciId
      this.addTypeId = addTypeId
      this.type = type
      this.ancestor_ids = ancestor_ids
      await getSubscribeAttributes(addTypeId).then((res) => {
        this.preferenceAttrList = res.attributes // 已经订阅的全部列
      })
      this.getTableData(true)
    },
    async getTableData(isInit) {
      if (this.addTypeId) {
        await this.fetchData(isInit)
      }
    },
    async fetchData(isInit) {
      this.loading = true
      let sort, fuzzySearch, expression, exp
      if (!isInit) {
        fuzzySearch = this.$refs['searchForm'].fuzzySearch
        expression = this.$refs['searchForm'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

        exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      }

      const res = await searchCI({
        q: `_type:${this.addTypeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
        count: 50,
        page: this.currentPage,
        sort,
      })
      this.tableData = res.result
      this.totalNumber = res.numfound
      this.columns = this.getColumns(res.result, this.preferenceAttrList)
      this.$nextTick(() => {
        const _table = this.$refs.xTable
        if (_table) {
          _table.refreshColumn()
        }
        this.loading = false
      })
    },
    getColumns(data, attrList) {
      const modalDom = document.getElementById('add-table-modal')
      if (modalDom) {
        const width = modalDom.clientWidth - 50
        return getCITableColumns(data, attrList, width)
      }
      return []
    },
    onSelectChange() {},
    handleClose() {
      this.$refs.xTable.clearCheckboxRow()
      this.currentPage = 1
      this.expression = ''
      this.isFocusExpression = false
      this.visible = false
    },
    async handleOk() {
      const selectRecordsCurrent = this.$refs.xTable.getCheckboxRecords()
      const selectRecordsReserved = this.$refs.xTable.getCheckboxReserveRecords()
      const ciIds = [...selectRecordsCurrent, ...selectRecordsReserved].map((record) => record._id)
      if (ciIds.length) {
        if (this.type === 'children') {
          await batchUpdateCIRelationChildren(ciIds, [this.ciId], this.ancestor_ids)
        } else {
          await batchUpdateCIRelationParents(ciIds, [this.ciId])
        }
        setTimeout(() => {
          this.$message.success('添加成功！')
          this.handleClose()
          this.$emit('reload')
        }, 500)
      }
    },
    handleSearch() {
      this.currentPage = 1
      this.fetchData()
    },
    handleChangePage(page, pageSize) {
      this.currentPage = page
      this.fetchData()
    },
  },
}
</script>

<style lang="less" scoped></style>
