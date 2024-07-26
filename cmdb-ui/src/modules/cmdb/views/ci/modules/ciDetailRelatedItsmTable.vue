<template>
  <div :style="{ height: '100%' }" v-if="itsmInstalled">
    <vxe-table
      ref="xTable"
      show-overflow
      show-header-overflow
      resizable
      border
      size="small"
      class="ops-unstripe-table"
      :span-method="mergeRowMethod"
      :data="tableData"
      v-bind="ci_id ? { height: 'auto' } : { height: `${windowHeight - 225}px` }"
    >
      <template #empty>
        <a-empty :image-style="{ height: '100px' }" :style="{ paddingTop: '10%' }">
          <img slot="image" :src="require('@/assets/data_empty.png')" />
          <span slot="description"> {{ $t('noData') }} </span>
        </a-empty>
      </template>
      <vxe-column field="ticket.ticket_id" min-width="80" :title="$t('cmdb.history.ticketId')"> </vxe-column>
      <vxe-column field="ticket.created_at" width="160" :title="$t('cmdb.history.ticketStartTime')"> </vxe-column>
      <vxe-column field="ticket.creator_name" min-width="80" :title="$t('cmdb.history.ticketCreator')"> </vxe-column>
      <vxe-column field="ticket.title" min-width="150" :title="$t('cmdb.history.ticketTitle')">
        <template slot-scope="{ row }">
          <a target="_blank" :href="row.ticket.url">{{ row.ticket.title }}</a>
        </template>
      </vxe-column>
      <vxe-column field="ticket.node_finish_time" width="160" :title="$t('cmdb.history.ticketFinishTime')">
      </vxe-column>
      <vxe-column field="ticket.node_name" min-width="100" :title="$t('cmdb.history.ticketNodeName')"> </vxe-column>
      <vxe-table-column
        field="operate_type"
        min-width="100"
        :filters="[
          { value: 0, label: $t('new') },
          { value: 1, label: $t('delete') },
          { value: 2, label: $t('update') },
        ]"
        :filter-method="filterOperateMethod"
        :title="$t('operation')"
      >
        <template #default="{ row }">
          {{ operateTypeMap[row.operate_type] }}
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="attr_alias"
        min-width="100"
        :title="$t('cmdb.attribute')"
        :filters="[]"
        :filter-method="filterAttrMethod"
      >
      </vxe-table-column>
      <vxe-table-column field="old" min-width="100" :title="$t('cmdb.history.old')"></vxe-table-column>
      <vxe-table-column field="new" min-width="100" :title="$t('cmdb.history.new')"></vxe-table-column>
    </vxe-table>
    <div :style="{ textAlign: 'right' }" v-if="!ci_id">
      <a-pagination
        size="small"
        show-size-changer
        show-quick-jumper
        :page-size-options="pageSizeOptions"
        :current="tablePage.currentPage"
        :total="tablePage.totalResult"
        :show-total="(total, range) => $t('cmdb.history.totalItems', { total: total })"
        :page-size="tablePage.pageSize"
        :default-current="1"
        @change="pageOrSizeChange"
        @showSizeChange="pageOrSizeChange"
      >
      </a-pagination>
    </div>
  </div>
  <a-empty
    v-else
    :image-style="{
      height: '200px',
    }"
    :style="{ paddingTop: '10%' }"
  >
    <img slot="image" :src="require('@/modules/cmdb/assets/itsm_uninstalled.png')" />
    <span slot="description"> {{ $t('cmdb.history.itsmUninstalled') }} </span>
    <a-button href="https://veops.cn/apply" target="_blank" type="primary">
      {{ $t('cmdb.history.applyItsm') }}
    </a-button>
  </a-empty>
</template>

<script>
import { getCiRelatedTickets } from '../../../api/history'
export default {
  name: 'RelatedItsmTable',
  props: {
    ci_id: {
      type: Number,
      default: null,
    },
    ciHistory: {
      type: Array,
      default: () => [],
    },
    itsmInstalled: {
      type: Boolean,
      default: true,
    },
    attrList: {
      type: Function,
      default: () => [],
    }
  },
  data() {
    return {
      tableData: [],
      tablePage: {
        currentPage: 1,
        pageSize: 50,
        totalResult: 0,
      },
      pageSizeOptions: ['50', '100', '200'],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    operateTypeMap() {
      return {
        0: this.$t('new'),
        1: this.$t('delete'),
        2: this.$t('update'),
      }
    },
  },
  mounted() {
    this.updateTableData()
  },
  methods: {
    updateTableData(currentPage = 1, pageSize = this.tablePage.pageSize) {
      const params = { page: currentPage, page_size: pageSize, next_todo_ids: [] }
      if (this.ci_id) {
        const tableData = []
        this.ciHistory.forEach((item) => {
          if (item.ticket_id) {
            params.next_todo_ids.push(item.ticket_id)
            tableData.push(item)
          }
        })
        if (params.next_todo_ids.length) {
          getCiRelatedTickets(params)
            .then((res) => {
              const ticketId2Detail = {}
              res.forEach((item) => {
                ticketId2Detail[item.next_todo_id] = item
              })
              this.tableData = tableData.map((item) => {
                return {
                  ...item,
                  ticket: ticketId2Detail[item.ticket_id],
                }
              })
              this.updateAttrFilter()
            })
            .catch((e) => {})
        }
      } else {
      }
    },
    updateAttrFilter() {
      this.$nextTick(() => {
        const $table = this.$refs.xTable
        if ($table) {
          const attrColumn = $table.getColumnByField('attr_alias')
          if (attrColumn) {
            $table.setFilter(
              attrColumn,
              this.attrList().map((attr) => {
                return { value: attr.alias || attr.name, label: attr.alias || attr.name }
              })
            )
          }
        }
      })
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = [
        'ticket.ticket_id',
        'ticket.created_at',
        'ticket.creator_name',
        'ticket.title',
        'ticket.node_finish_time',
        'ticket.node_name',
      ]
      const cellValue1 = row.ticket.ticket_id
      const cellValue2 = row.ticket.node_name
      if (cellValue1 && cellValue2 && fields.includes(column.property)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow.ticket.ticket_id === cellValue1 && prevRow.ticket.node_name === cellValue2) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow.ticket.ticket_id === cellValue1 && nextRow.ticket.node_name === cellValue2) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },
    pageOrSizeChange(currentPage, pageSize) {
      this.updateTableData(currentPage, pageSize)
    },
    filterOperateMethod({ value, row, column }) {
      return Number(row.operate_type) === Number(value)
    },
    filterAttrMethod({ value, row, column }) {
      return row.attr_alias === value
    },
  },
}
</script>

<style></style>
