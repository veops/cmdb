<template>
  <div class="ip-table">
    <ops-table
      ref="xTable"
      size="small"
      show-overflow
      show-header-overflow
      highlight-hover-row
      :data="tableData"
      :row-config="{ useKey: true, keyField: 'ip' }"
      :column-config="{ resizable: true }"
      :checkbox-config="{ highlight: true, reserve: true, range: true }"
      :height="tableHeight"
      class="ops-unstripe-table checkbox-hover-table"
      @checkbox-change="onSelectChange"
      @checkbox-all="onSelectChange"
      @checkbox-range-end="onSelectRangeEnd"
    >
      <vxe-table-column
        align="center"
        type="checkbox"
        :width="60"
      >
        <template #default="{row}">
          {{ getRowSeq(row) }}
        </template>
      </vxe-table-column>

      <vxe-table-column
        v-for="(col) in columns"
        :key="col.field"
        :title="col.title"
        :field="col.field"
        :width="columnWidth[col.field] || undefined"
      >
        <template
          v-if="col.field === '_ip_status' || col.is_link || col.is_reference || col.is_choice"
          #default="{ row }"
        >
          <div v-if="col.field === '_ip_status'" class="ip-table-status">
            <div
              class="ip-table-status-dot"
              :style="{
                backgroundColor: `${STATUS_COLOR[row._ip_status]}22`
              }"
            >
              <div
                class="ip-table-status-dot-content"
                :style="{
                  backgroundColor: STATUS_COLOR[row._ip_status]
                }"
              ></div>
            </div>
            <div
              class="ip-table-status-text"
            >
              {{ $t(STATUS_LABEL[row._ip_status]) }}
            </div>
          </div>
          <template v-if="col.is_reference && row[col.field]" >
            <a
              v-for="(ciId) in (col.is_list ? row[col.field] : [row[col.field]])"
              :key="ciId"
              :href="`/cmdb/cidetail/${col.reference_type_id}/${ciId}`"
              target="_blank"
            >
              {{ getReferenceAttrValue(ciId, col) }}
            </a>
          </template>
          <template v-else-if="col.is_link && row[col.field]">
            <a
              v-for="(linkItem, linkIndex) in (col.is_list ? row[col.field] : [row[col.field]])"
              :key="linkIndex"
              :href="
                linkItem.startsWith('http') || linkItem.startsWith('https')
                  ? `${linkItem}`
                  : `http://${linkItem}`
              "
              target="_blank"
            >
              {{ getChoiceValueLabel(col, linkItem) || linkItem }}
            </a>
          </template>
          <template v-else-if="col.is_choice && row[col.field]">
            <span
              v-for="value in (col.is_list ? row[col.field] : [row[col.field]])"
              :key="value"
              class="column-default-choice"
            >
              {{ getChoiceValueLabel(col, value) || value }}
            </span>
          </template>
        </template>
      </vxe-table-column>

      <vxe-table-column
        :title="$t('operation')"
        :width="80"
        fixed="right"
      >
        <template #default="{ row }">
          <div class="ip-table-operation">
            <template v-if="[ADDRESS_STATUS.ONLINE_ASSIGNED, ADDRESS_STATUS.OFFLINE_ASSIGNED].includes(row._ip_status)">
              <a-tooltip :title="$t('cmdb.ipam.editAssignAddress')">
                <a @click="assignAddress(row)"><ops-icon type="veops-edit" /></a>
              </a-tooltip>
              <a-tooltip :title="$t('cmdb.ipam.recycle')">
                <a @click="clickRecycle(row)"><ops-icon type="veops-recycle" /></a>
              </a-tooltip>
            </template>
            <a-tooltip v-else :title="$t('cmdb.ipam.assign')">
              <a @click="assignAddress(row)"><ops-icon type="monitor-add2" /></a>
            </a-tooltip>

            <a-tooltip v-if="row._ip_status !== ADDRESS_STATUS.OFFLINE_UNASSIGNED" :title="$t('cmdb.ci.viewRelation')">
              <a @click="openRelation(row)">
                <a-icon type="retweet" />
              </a>
            </a-tooltip>
          </div>
        </template>
      </vxe-table-column>
    </ops-table>
    <div class="ip-table-pagination">
      <a-pagination
        :showSizeChanger="true"
        :current="page"
        size="small"
        :total="allTableData.length"
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
        @showSizeChange="handlePageSizeChange"
        @change="changePage"
      >
        <template slot="buildOptionText" slot-scope="props">
          <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
          <span v-if="props.value === '100000'">{{ $t('all') }}</span>
        </template>
      </a-pagination>
    </div>

    <CIDetailDrawer ref="detail" :typeId="addressCITypeId" />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import { STATUS_COLOR, STATUS_LABEL, ADDRESS_STATUS } from './constants.js'

import CIDetailDrawer from '@/modules/cmdb/views/ci/modules/ciDetailDrawer.vue'

export default {
  name: 'TableIP',
  components: {
    CIDetailDrawer
  },
  props: {
    columns: {
      type: Array,
      default: () => []
    },
    allTableData: {
      type: Array,
      default: () => []
    },
    referenceShowAttrNameMap: {
      type: Object,
      default: () => {}
    },
    referenceCIIdMap: {
      type: Object,
      default: () => {}
    },
    columnWidth: {
      type: Object,
      default: () => {}
    },
    addressCITypeId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      STATUS_COLOR,
      STATUS_LABEL,
      ADDRESS_STATUS,
      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 270}px`
    },
    tableData() {
      const start = (this.page - 1) * this.pageSize
      const end = start + this.pageSize
      const tableData = this.allTableData.slice(start, end)

      return _.cloneDeep(tableData)
    }
  },
  watch: {
    allTableData: {
      immediate: true,
      handler() {
        this.page = 1
      }
    }
  },
  methods: {
    getRowSeq(row) {
      const table = this.$refs?.['xTable']?.getVxetableRef?.() || null
      return table?.getRowSeq?.(row)
    },

    handlePageSizeChange(_, pageSize) {
      this.pageSize = pageSize
      this.page = 1
    },

    changePage(page) {
      this.page = page
    },

    assignAddress(data) {
      this.$emit('openAssign', data)
    },

    clickRecycle(data) {
      this.$emit('recycle', data.ip)
    },

    getCheckedTableData(clearCheckbox = true) {
      const tableRef = this.$refs.xTable.getVxetableRef()
      let tableData = _.cloneDeep([
        ...tableRef.getCheckboxReserveRecords(),
        ...tableRef.getCheckboxRecords(true),
      ])
      if (!tableData.length) {
        const { fullData } = tableRef.getTableData()
        tableData = _.cloneDeep(fullData)
      }

      if (clearCheckbox) {
        this.clearCheckbox()
      }

      return tableData
    },

    clearCheckbox() {
      const tableRef = this.$refs?.xTable?.getVxetableRef?.()
      if (tableRef) {
        tableRef.clearCheckboxRow()
        tableRef.clearCheckboxReserve()
      }
    },

    getReferenceAttrValue(id, col) {
      const ci = this?.referenceCIIdMap?.[col?.reference_type_id]?.[id]
      if (!ci) {
        return id
      }

      const attrName = this.referenceShowAttrNameMap?.[col.reference_type_id]
      return ci?.[attrName] || id
    },

    getChoiceValueLabel(col, colValue) {
      const _find = col?.choice_value?.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find?.[1]?.label || ''
      }
      return ''
    },

    onSelectChange() {
      const xTable = this.$refs.xTable.getVxetableRef()
      const records = [...xTable.getCheckboxRecords(), ...xTable.getCheckboxReserveRecords()]
      const ips = records.map((item) => item.ip)
      this.$emit('selectChange', ips)
    },

    onSelectRangeEnd({ records }) {
      const ips = records?.map?.((item) => item.ip) || []
      this.$emit('selectChange', ips)
    },

    openRelation(row) {
      if (row._id) {
        this.$refs.detail.create(row._id, 'tab_2', '2')
      }
    }
  }
}
</script>

<style lang="less" scoped>
.ip-table {
  &-status {
    display: flex;
    align-items: center;

    &-dot {
      width: 12px;
      height: 12px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;

      &-content {
        width: 6px;
        height: 6px;
        border-radius: 6px;
      }
    }

    &-text {
      margin-left: 4px;
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;
    }
  }

  &-operation {
    display: flex;
    align-items: center;
    column-gap: 12px;
  }

  &-pagination {
    text-align: right;
    margin-top: 12px;
  }
}

.checkbox-hover-table {
  /deep/ .vxe-table--body-wrapper {
    .vxe-checkbox--label {
      display: inline;
      padding-left: 0px !important;
      color: #bfbfbf;
    }

    .vxe-icon-checkbox-unchecked {
      display: none;
    }

    .vxe-icon-checkbox-checked ~ .vxe-checkbox--label {
      display: none;
    }

    .vxe-cell--checkbox {
      &:hover {
        .vxe-icon-checkbox-unchecked {
          display: inline;
        }

        .vxe-checkbox--label {
          display: none;
        }
      }
    }
  }
}
</style>
