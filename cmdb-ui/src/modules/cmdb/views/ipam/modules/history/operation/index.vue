<template>
  <div class="operate">
    <a-input-search
      class="operate-search"
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
      class="ops-unstripe-table operate-table"
      :filter-config="{ remote: true }"
      :sort-config="{ remote: true, trigger: 'cell' }"
      :column-config="{ resizable: true }"
      @filter-change="handlefilterChange"
      @sort-change="handleSortChange"
    >
      <vxe-table-column
        :title="$t('cmdb.ipam.operateTime')"
        sortable
        field="created_at"
        :width="150"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.operateUser')"
        field="uid"
        :filters="userFilters"
        :width="130"
      >
        <template #default="{row}">
          {{ row.nickname }}
        </template>
      </vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.operateType')"
        field="operate_type"
        :filters="operateTypeFilters"
        :width="150"
      >
        <template #default="{row}">
          <div
            v-if="row.operate_type"
            class="operate-table-type"
            :style="{
              backgroundColor: OPERATE_TYPE_COLOR[row.operate_type].backgroundColor,
              color: OPERATE_TYPE_COLOR[row.operate_type].color
            }"
          >
            {{ $t(OPERATE_TYPE_TEXT[row.operate_type]) }}
          </div>
        </template>
      </vxe-table-column>
      <vxe-table-column
        title="CIDR"
        field="cidr"
        :width="150"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.description')"
        field="description"
      ></vxe-table-column>
    </ops-table>

    <div class="operate-pagination">
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
import _ from 'lodash'
import { mapState } from 'vuex'
import { OPERATE_TYPE_TEXT, OPERATE_TYPE_COLOR, OPERATE_TYPE } from './constants.js'
import { getIPAMHistoryOperate } from '@/modules/cmdb/api/ipam.js'

export default {
  name: 'Operate',
  data() {
    return {
      OPERATE_TYPE_TEXT,
      OPERATE_TYPE_COLOR,
      searchValue: '',

      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
      tableData: [],
      totalNumber: 0,
      getTableDataParams: {
        reverse: 1
      },
      userFilters: []
    }
  },
  computed: {
    ...mapState({
      allEmployees: (state) => state.user.allEmployees,
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 308}px`
    },
    operateTypeFilters() {
      const filters = Object.values(OPERATE_TYPE).map((key) => {
        return {
          value: key,
          label: this.$t(OPERATE_TYPE_TEXT[key])
        }
      })
      return filters
    }
  },
  mounted() {
    this.getTableData()
  },
  methods: {
    async getTableData() {
      const res = await getIPAMHistoryOperate({
        page: this.page,
        page_size: this.pageSize,
        ...this.getTableDataParams
      })

      const tableData = res?.result || []
      const userFilters = []
      const defaultUserChecked = this.getTableDataParams.uid ? this.getTableDataParams.uid.split(',') : []

      tableData.forEach((item) => {
        const nickname = this.allEmployees?.find?.((user) => user?.acl_uid === item?.uid)?.nickname
        item.nickname = nickname
        userFilters.push({
          label: nickname,
          value: item.uid,
          checked: defaultUserChecked.includes(String(item.uid))
        })
      })

      this.totalNumber = res?.numfound || 0
      this.tableData = tableData
      this.userFilters = _.uniqBy(userFilters, 'value')
    },
    handleSearch(v) {
      if (v) {
        this.getTableDataParams.cidr = `*${v}*`
      } else if (this.getTableDataParams.cidr) {
        delete this.getTableDataParams.cidr
      }
      this.page = 1
      this.getTableData()
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

    handlefilterChange({ field, values }) {
      this.page = 1
      const value = values.join(',')
      if (!value && this.getTableDataParams[field]) {
        delete this.getTableDataParams[field]
      } else {
        this.getTableDataParams[field] = values.join(',')
      }
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
.operate {
  width: 100%;

  &-search {
    width: 244px;
    margin-bottom: 22px;
  }

  &-table {
    &-type {
      display: inline-block;
      font-size: 12px;
      font-weight: 400;
      padding: 0 9px;
      height: 22px;
      line-height: 22px;
      border-radius: 1px;
    }
  }

  &-pagination {
    text-align: right;
    margin-top: 4px;
  }
}
</style>
