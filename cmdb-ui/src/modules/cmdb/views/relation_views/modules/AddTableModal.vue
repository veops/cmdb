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
        <ops-table
          ref="xTable"
          row-id="_id"
          :data="tableData"
          :height="tableHeight"
          highlight-hover-row
          :checkbox-config="{ reserve: true, highlight: true, range: true }"
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
                {{ getReferenceAttrValue(id, col) }}
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
        </ops-table>
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
import { getCITypes } from '@/modules/cmdb/api/CIType'

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

      referenceShowAttrNameMap: {},
      referenceCIIdMap: {}
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
        this.handleReferenceShowAttrName()
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
            const _table = this.$refs.xTable?.getVxetableRef?.()
            if (_table) {
              _table.refreshColumn()
            }
            this.loading = false
          })

          this.handleReferenceCIIdMap()
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

    async handleReferenceShowAttrName() {
      const needRequiredCITypeIds = this.preferenceAttrList?.filter((attr) => attr?.is_reference && attr?.reference_type_id).map((attr) => attr.reference_type_id) || []
      if (!needRequiredCITypeIds.length) {
        this.referenceShowAttrNameMap = {}
        return
      }

      const res = await getCITypes({
        type_ids: needRequiredCITypeIds.join(',')
      })

      const map = {}
      res.ci_types.forEach((ciType) => {
        map[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      this.referenceShowAttrNameMap = map
    },

    async handleReferenceCIIdMap() {
      const referenceTypeCol = this.preferenceAttrList.filter((attr) => attr?.is_reference && attr?.reference_type_id) || []
      if (!this.tableData?.length || !referenceTypeCol?.length) {
        this.referenceCIIdMap = {}
        return
      }

      const map = {}
      this.tableData.forEach((row) => {
        referenceTypeCol.forEach((col) => {
          const ids = Array.isArray(row[col.name]) ? row[col.name] : row[col.name] ? [row[col.name]] : []
          if (ids.length) {
            if (!map?.[col.reference_type_id]) {
              map[col.reference_type_id] = {}
            }
            ids.forEach((id) => {
              map[col.reference_type_id][id] = {}
            })
          }
        })
      })

      if (!Object.keys(map).length) {
        this.referenceCIIdMap = {}
        return
      }

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (map?.[item._type]?.[item._id]) {
            map[item._type][item._id] = item
          }
        })
      })

      this.referenceCIIdMap = map
    },

    getReferenceAttrValue(id, col) {
      const ci = this?.referenceCIIdMap?.[col?.reference_type_id]?.[id]
      if (!ci) {
        return id
      }

      const attrName = this.referenceShowAttrNameMap?.[col.reference_type_id]
      return ci?.[attrName] || id
    },

    onSelectChange() {},
    handleClose() {
      const _table = this.$refs.xTable?.getVxetableRef?.()
      if (_table) {
        _table.clearCheckboxRow()
      }

      this.currentPage = 1
      this.expression = ''
      this.isFocusExpression = false
      this.visible = false
      this.showCreateBtn = true
    },
    async handleOk() {
      const _table = this.$refs.xTable?.getVxetableRef?.()
      const selectRecordsCurrent = _table?.getCheckboxRecords?.() || []
      const selectRecordsReserved = _table?.getCheckboxReserveRecords?.() || []

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
