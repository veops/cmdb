<template>
  <div class="operation-log">
    <ops-table
      ref="xTable"
      size="small"
      show-overflow
      show-header-overflow
      highlight-hover-row
      :data="tableData"
      :height="tableHeight"
      :sort-config="{ remote: true }"
      @sort-change="handleSortChange"
    >
      <vxe-table-column
        :title="$t('cmdb.dcim.operationTime')"
        field="created_at"
        sortable
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.dcim.operationUser')"
        field="operationUser"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.dcim.operationType')"
        field="operate_type"
      >
        <template #default="{ row }">
          <div
            class="operation-log-device-type"
            :style="{
              backgroundColor: row.deviceTypeData.backgroundColor,
              color: row.deviceTypeData.textColor
            }"
          >
            {{ $t(row.deviceTypeData.name) }}
          </div>
        </template>
      </vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.dcim.deviceType')"
        field="deviceType"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.dcim.deviceName')"
        field="deviceName"
      ></vxe-table-column>
    </ops-table>

    <div class="operation-log-pagination">
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
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getDCIMHistoryOperate } from '@/modules/cmdb/api/dcim.js'

export default {
  name: 'OperationLog',
  props: {
    rackId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
      totalNumber: 0,
      tableData: [],
      getTableDataParams: {
        reverse: 1
      },

      deviceTypeMap: {
        0: {
          textColor: '#00B42A',
          backgroundColor: '#F6FFED',
          name: 'cmdb.dcim.addDevice'
        },
        1: {
          textColor: '#FD4C6A',
          backgroundColor: '#FFECE8',
          name: 'cmdb.dcim.removeDevice'
        },
        2: {
          textColor: '#FF7D00',
          backgroundColor: '#FFECCF',
          name: 'cmdb.dcim.moveDevice'
        }
      }
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
      allEmployees: (state) => state.user.allEmployees,
    }),
    tableHeight() {
      return `${this.windowHeight - 187}px`
    },
  },
  mounted() {
    this.getTableData()
  },
  methods: {
    async getTableData() {
      const res = await getDCIMHistoryOperate({
        rack_id: this.rackId,
        count: this.pageSize,
        page: this.page,
        ...this.getTableDataParams
      })

      const tableData = res?.result || []
      tableData.forEach((item) => {
        const ci = res?.id2ci?.[item?.ci_id] || {}
        const showKey = res?.type2show_key?.[ci?._type] || ''
        const user = this.allEmployees.find((emp) => item.uid === emp.acl_uid)

        item.operationUser = user?.nickname || ''
        item.deviceType = ci?.ci_type_alias || ''
        item.deviceName = ci?.[showKey] || item?.ci_id || ''
        item.deviceTypeData = this.deviceTypeMap?.[item?.operate_type] || {}
      })

      this.tableData = tableData
      this.totalNumber = res?.numfound || 0
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
    handleSortChange(data) {
      if (data?.order === 'asc') {
        this.getTableDataParams.reverse = 0
      } else {
        this.getTableDataParams.reverse = 1
      }
      this.page = 1
      this.getTableData()
    }
  }
}
</script>

<style lang="less" scoped>
.operation-log {
  &-device-type {
    font-size: 12px;
    font-weight: 400;
    line-height: 22px;
    height: 22px;
    padding: 0 9px;
    border-radius: 1px;
    display: inline-block;
  }

  &-pagination {
    text-align: right;
    margin-top: 4px;
  }
}
</style>
