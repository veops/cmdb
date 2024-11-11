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
        >
          <a-button
            v-if="showCreateBtn"
            @click="
              () => {
                $refs.createInstanceForm.handleOpen(true, 'create')
              }
            "
            slot="extraContent"
            type="primary"
            size="small"
          >新增</a-button
          >
        </SearchForm>
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
            <template v-if="col.is_reference" #default="{row}">
              <a
                v-for="(id) in (col.is_list ? row[col.field] : [row[col.field]])"
                :key="id"
                :href="`/cmdb/cidetail/${col.reference_type_id}/${id}`"
                target="_blank"
              >
                {{ id }}
              </a>
            </template>
            <template #default="{row}" v-else-if="col.is_choice">
              <span
                v-for="value in (col.is_list ? row[col.field] : [row[col.field]])"
                :key="value"
              >
                {{ getChoiceValueLabel(col, value) || value }}
              </span>
            </template>
            <template #default="{row}" v-else-if="col.value_type == '6'">
              <span v-if="col.value_type == '6' && row[col.field]">{{ JSON.stringify(row[col.field]) }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <a-pagination
          v-model="currentPage"
          size="small"
          :total="totalNumber"
          show-quick-jumper
          :page-size="50"
          :show-total="
            (total, range) =>
              $t('pagination.total', {
                range0: range[0],
                range1: range[1],
                total,
              })
          "
          :style="{ textAlign: 'right', marginTop: '10px' }"
          @change="handleChangePage"
        />
      </a-spin>
    </div>
    <CreateInstanceForm
      ref="createInstanceForm"
      :typeIdFromRelation="addTypeId"
      @reload="
        () => {
          currentPage = 1
          getTableData(true)
        }
      "
    />
  </a-modal>
</template>

<script>
import { searchCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { batchUpdateCIRelationChildren, batchUpdateCIRelationParents } from '@/modules/cmdb/api/CIRelation'
import { getCITableColumns } from '../../../utils/helper'
import SearchForm from '../../../components/searchForm/SearchForm.vue'
import CreateInstanceForm from '../../ci/modules/CreateInstanceForm.vue'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { SUB_NET_CITYPE_NAME, SCOPE_CITYPE_NAME, ADDRESS_CITYPE_NAME } from '@/modules/cmdb/views/ipam/constants.js'

export default {
  name: 'AddTableModal',
  components: { SearchForm, CreateInstanceForm },
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
      attrList1: [],
      showCreateBtn: true, // 是否展示新增按钮
    }
  },
  computed: {
    tableHeight() {
      return this.$store.state.windowHeight - 250
    },
    placeholder() {
      return this.isFocusExpression ? this.$t('cmdb.serviceTreetips1') : this.$t('cmdb.serviceTreetips2')
    },
    width() {
      return this.isFocusExpression ? '500px' : '100px'
    },
  },
  provide() {
    return {
      attrList: () => {
        return this.attrList
      },
    }
  },
  watch: {},
  methods: {
    async openModal(ciObj, ciId, addType, type, ancestor_ids = undefined) {
      console.log(ciObj, ciId, addType, type)
      this.visible = true
      this.ciObj = ciObj
      this.ciId = ciId
      this.addTypeId = addType.id
      this.type = type
      this.ancestor_ids = ancestor_ids
      this.showCreateBtn = ![SUB_NET_CITYPE_NAME, SCOPE_CITYPE_NAME, ADDRESS_CITYPE_NAME].includes(addType.name)

      await getSubscribeAttributes(this.addTypeId).then((res) => {
        this.preferenceAttrList = res.attributes // 已经订阅的全部列
      })
      getCITypeAttributesById(this.addTypeId).then((res) => {
        this.attrList = res.attributes
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
      // if (isInit) {
      //   const subscribed = await getSubscribeAttributes(this.addTypeId)
      //   this.preferenceAttrList = subscribed.attributes // 已经订阅的全部列
      // }
      let sort, fuzzySearch, expression, exp
      if (!isInit) {
        fuzzySearch = this.$refs['searchForm'].fuzzySearch
        expression = this.$refs['searchForm'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

        exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      }

      await searchCI({
        q: `_type:${this.addTypeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
        count: 50,
        page: this.currentPage,
        sort,
      })
        .then((res) => {
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
        })
        .catch(() => {
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
      this.showCreateBtn = true
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
          this.$message.success(this.$t('addSuccess'))
          this.handleClose()
          this.$emit('reload')
        }, 500)
      } else {
        this.handleClose()
        this.$emit('reload')
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

    getChoiceValueLabel(col, colValue) {
      const _find = col.filters.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.label || ''
      }
      return ''
    },
  },
}
</script>

<style lang="less" scoped></style>
