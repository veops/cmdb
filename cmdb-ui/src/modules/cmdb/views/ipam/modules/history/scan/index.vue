<template>
  <div class="scan">
    <a-input-search
      class="scan-search"
      @search="handleSearch"
    />

    <ops-table
      ref="xTable"
      size="small"
      show-overflow
      show-header-overflow
      highlight-hover-row
      :data="tableData"
      :height="tableHeight"
      :column-config="{ resizable: true }"
      class="ops-unstripe-table scan-table"
    >
      <vxe-table-column
        title="CIDR"
        field="cidr"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.ipNumber')"
        field="ip_num"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.startTime')"
        field="start_at"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.endTime')"
        field="end_at"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.scanningTime')"
        field="scanning_time"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.isSuccess')"
        field="status"
      >
        <template #default="{ row }">
          <div class="scan-table-success" v-if="row.status === 0">
            <a-icon class="scan-table-success-icon" type="check-circle" theme="filled" />
            <div class="scan-table-success-text">{{ $t('success') }}</div>
          </div>
          <div class="scan-table-fail" v-else>
            <a-icon class="scan-table-fail-icon" type="close-circle" theme="filled" />
            <div class="scan-table-fail-text">{{ $t('fail') }}</div>
          </div>
        </template>
      </vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.viewResult')"
        field="operation"
        :show-overflow="false"
      >
        <template #default="{ row }">
          <a-popover placement="left">
            <span class="scan-table-operation">
              {{ row.status === 0 ? row.ips ? row.ips.join(', ') : '' : row.stdout }}
            </span>
            <template slot="content">
              <div
                v-if="row.status === 0"
                class="scan-table-ip"
              >
                <div
                  v-for="(ip, index) in row.ips"
                  :key="index"
                  class="scan-table-ip-item"
                >
                  {{ ip }}
                </div>
              </div>
              <div
                v-else
                class="scan-table-error-log"
              >
                {{ row.stdout }}
              </div>
            </template>
          </a-popover>
        </template>
      </vxe-table-column>
    </ops-table>

    <div class="scan-pagination">
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
import moment from 'moment'
import { mapState } from 'vuex'
import { getIPAMHistoryScan } from '@/modules/cmdb/api/ipam.js'

export default {
  name: 'Scan',
  data() {
    return {
      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
      tableData: [],
      totalNumber: 0,
      getTableDataParams: {},
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 308}px`
    },
  },
  mounted() {
    this.getTableData()
  },
  methods: {
    async getTableData() {
      const res = await getIPAMHistoryScan({
        page: this.page,
        page_size: this.pageSize,
        reverse: 1,
        ...this.getTableDataParams
      })

      const tableData = res?.result || []

      tableData.forEach((item) => {
        if (item.start_at && item.end_at) {
          const startAt = moment(item.start_at)
          const endAt = moment(item.end_at)
          item.scanning_time = `${endAt.diff(startAt, 'seconds')}s`
        }
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

    handleSearch(v) {
      if (v) {
        this.getTableDataParams.cidr = `*${v}*`
      } else if (this.getTableDataParams.cidr) {
        delete this.getTableDataParams.cidr
      }
      this.page = 1
      this.getTableData()
    }
  }
}
</script>

<style lang="less" scoped>
.scan {
  width: 100%;

  &-search {
    width: 244px;
    margin-bottom: 22px;
  }

  &-table {
    &-success {
      padding: 4px 7px;
      border-radius: 1px;
      background-color: #DCF3E3;
      display: inline-flex;
      align-items: center;
      justify-content: center;

      &-icon {
        font-size: 12px;
        color: #00B42A;
      }

      &-text {
        font-size: 12px;
        font-weight: 400;
        color: #30AD2D;
        margin-left: 4px;
      }
    }

    &-fail {
      padding: 0px 7px;
      border-radius: 1px;
      background-color: #FFECE8;
      display: inline-flex;
      align-items: center;
      justify-content: center;

      &-icon {
        font-size: 12px;
        color: #FD4C6A;
      }

      &-text {
        font-size: 12px;
        font-weight: 400;
        color: #FD4C6A;
        margin-left: 4px;
      }
    }

    &-operation {
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
    }

    &-ip {
      width: 100%;
      max-height: 216px;
      overflow-y: auto;
      overflow-x: hidden;
      border: solid 1px #F0F1F5;

      &-item {
        height: 36px;
        line-height: 36px;
        padding: 0 12px;
        font-size: 14px;
        font-weight: 400;
        color: #1D2129;

        &:not(:last-child) {
          border-bottom: solid 1px #F0F1F5;
        }
      }
    }

    &-error-log {
      max-width: 200px;
      max-height: 200px;
      overflow-y: auto;
      overflow-x: hidden;
    }
  }

  &-pagination {
    text-align: right;
    margin-top: 4px;
  }
}
</style>
