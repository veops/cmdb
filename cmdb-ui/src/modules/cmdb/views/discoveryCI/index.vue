<template>
  <TwoColumnLayout appName="cmdb-adc">
    <template #one>
      <div class="cmdb-adc-group" v-for="group in ci_types_list" :key="group.id">
        <p>
          <strong>{{ group.name || $t('other') }}</strong
          ><span :style="{ color: 'rgb(195, 205, 215)' }">({{ group.ci_types.length }})</span>
        </p>
        <div
          :class="{ 'cmdb-adc-side-item': true, 'cmdb-adc-side-item-selected': currentType === ciType.id }"
          v-for="ciType in group.ci_types"
          :key="ciType.id"
          @click="clickSidebar(ciType.id)"
        >
          <span class="cmdb-adc-side-icon">
            <template v-if="ciType.icon">
              <img v-if="ciType.icon.split('$$')[2]" :src="`/api/common-setting/v1/file/${ciType.icon.split('$$')[3]}`" />
              <ops-icon
                v-else
                :style="{
                  color: ciType.icon.split('$$')[1],
                  fontSize: '14px',
                }"
                :type="ciType.icon.split('$$')[0]"
              />
            </template>
            <span :style="{ color: '#2f54eb' }" v-else>{{ ciType.name[0].toUpperCase() }}</span>
          </span>
          <span :title="ciType.alias || ciType.name" class="cmdb-adc-side-name">{{ ciType.alias || ciType.name }}</span>
        </div>
      </div>
    </template>
    <template #two>
      <div id="discovery-ci">
        <AdcCounter :typeId="currentType" />
        <div class="discovery-ci-header">
          <a-input-search
            :placeholder="$t('cmdb.components.pleaseSearch')"
            :style="{ width: '200px', marginRight: '20px' }"
            @search="handleSearch"
            allowClear
          />
          <span class="ops-list-batch-action" v-show="selectedCount">
            <span @click="batchAccept">{{ $t('cmdb.ad.accept') }}</span>
            <a-divider type="vertical" />
            <span @click="batchDelete">{{ $t('delete') }}</span>
            <span>{{ $t('cmdb.ci.selectRows', { rows: selectedCount }) }}</span>
          </span>
          <div @click="clickLog" class="discovery-ci-log">
            <ops-icon type="a-cmdb-log1" />
            <span>{{ $t('cmdb.ad.log') }}</span>
          </div>
        </div>
        <ops-table
          show-overflow
          show-header-overflow
          resizable
          ref="xTable"
          size="mini"
          stripe
          class="ops-stripe-table checkbox-hover-table"
          :data="filterTableData"
          :height="tableHeight"
          :scroll-y="{ enabled: true, gt: 50 }"
          :scroll-x="{ enabled: true, gt: 0 }"
          @checkbox-change="onSelectChange"
          @checkbox-all="onSelectChange"
          @checkbox-range-end="onSelectChange"
          :checkbox-config="{ reserve: true, highlight: true, range: true }"
          :sort-config="{ remote: false, trigger: 'cell' }"
        >
          <vxe-column
            align="center"
            type="checkbox"
            width="60"
            fixed="left"
          >
            <template #default="{row}">
              {{ getRowSeq(row) }}
            </template>
          </vxe-column>
          <vxe-column
            v-for="(col, index) in columns"
            :key="`${col.field}_${index}`"
            :title="col.title"
            :field="col.field"
            :width="col.width"
            :sortable="col.sortable"
          >
            <template v-if="col.value_type === '6' || col.is_password" #default="{row}">
              <PasswordField
                v-if="col.is_password"
                :password="row[col.field]"
              />
              <span
                v-else-if="col.value_type === '6' && row[col.field]"
              >
                {{ row[col.field] }}
              </span>
            </template>
          </vxe-column>
          <vxe-column
            field="accept_by"
            :title="$t('cmdb.ad.acceptBy')"
            v-bind="columns.length ? { width: '80px' } : { minWidth: '80px' }"
            :filters="acceptByFilters"
          ></vxe-column>
          <vxe-column
            align="center"
            field="is_accept"
            :title="$t('cmdb.ad.isAccept')"
            v-bind="columns.length ? { width: '80px' } : { minWidth: '80px' }"
            :filters="[
              { label: $t('yes'), value: true },
              { label: $t('no'), value: false },
            ]"
            fixed="right"
          >
            <template #default="{row}">
              <ops-icon
                :type="row.is_accept ? 'cmdb-warehousing' : 'cmdb-not_warehousing'"
                :style="{ color: row.is_accept ? '#00B42A' : '#A5A9BC' }"
              />
            </template>
          </vxe-column>
          <vxe-column
            field="accept_time"
            :title="$t('cmdb.ad.acceptTime')"
            sortable
            v-bind="columns.length ? { width: '150px' } : { minWidth: '150px' }"
            fixed="right"
          ></vxe-column>
          <vxe-column
            :title="$t('operation')"
            v-bind="columns.length ? { width: '60px' } : { minWidth: '60px' }"
            align="center"
            fixed="right"
          >
            <template #default="{row}">
              <a-space>
                <a-tooltip :title="$t('cmdb.ad.accept')">
                  <a v-if="!row.is_accept" @click="accept(row)"><ops-icon type="cmdb-manual_warehousing"/></a>
                </a-tooltip>
                <a :style="{ color: 'red' }" @click="deleteADC(row)"><a-icon type="delete"/></a>
              </a-space>
            </template>
          </vxe-column>
          <template #empty>
            <div>
              <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
              <div>{{ $t('noData') }}</div>
            </div>
          </template>
        </ops-table>

        <a-modal
          v-model="logModalVisible"
          :footer="null"
          :width="596"
        >
          <div class="log-modal-title">{{ $t('cmdb.ad.log') }}</div>
          <p ref="logModelText" class="log-modal-text">
            <span
              v-for="(item, index) in logTextArray"
              :key="index"
              class="log-modal-text-item"
            >
              {{ item }}
            </span>
          </p>
        </a-modal>
      </div>
    </template>
  </TwoColumnLayout>
</template>

<script>
import _ from 'lodash'
import XEUtils from 'xe-utils'
import TwoColumnLayout from '@/components/TwoColumnLayout'
import AdcCounter from './components/adcCounter.vue'
import PasswordField from './components/passwordField.vue'

import {
  getADCCiTypes,
  getAdc,
  updateADCAccept,
  getADCCiTypesAttrs,
  deleteAdc,
  getAdcExecHistories
} from '../../api/discovery'
import { getCITableColumns } from '../../utils/helper'

export default {
  name: 'DiscoveryCI',
  components: {
    TwoColumnLayout,
    AdcCounter,
    PasswordField
  },
  data() {
    return {
      ci_types_list: [],
      currentType: null,
      attributes: [],
      tableData: [],
      columns: [],
      selectedRowKeys: [],
      searchValue: '',
      logModalVisible: false,
      logTextArray: [],
      acceptByFilters: [],
      selectedCount: 0,
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      return this.windowHeight - 240
    },
    filterTableData() {
      const { searchValue } = this
      if (searchValue) {
        const searchProps = this.attributes.map((item) => item.name)
        const rest = this.tableData.filter((item) =>
          searchProps.some(
            (key) =>
              XEUtils.toValueString(item[key])
                .toLowerCase()
                .indexOf(searchValue.toLowerCase()) > -1
          )
        )
        return rest
      }
      return this.tableData
    }
  },
  watch: {
    currentType: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          localStorage.setItem('ops_adc_typeid', newValue)
        }
      },
    },
    selectedRowKeys: {
      deep: true,
      immediate: true,
      handler(selectedRowKeys) {
        this.selectedCount = selectedRowKeys.length
      },
    },
  },
  mounted() {
    getADCCiTypes({ need_other: true }).then((res) => {
      this.ci_types_list = res.filter((item) => item.ci_types && item.ci_types.length)
      const _currentType = localStorage.getItem('ops_adc_typeid')
      if (_currentType) {
        this.clickSidebar(Number(_currentType))
        return
      }
      if (res && res.length && res[0].ci_types && res[0].ci_types.length) {
        this.clickSidebar(res[0].ci_types[0].id)
      }
    })
  },
  methods: {
    async clickSidebar(id) {
      this.currentType = id
      this.attributes = await getADCCiTypesAttrs(this.currentType)
      this.getAdc(true)
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.xTable.getVxetableRef().clearSort()
    },
    getAdc(isInit) {
      getAdc({
        type_id: this.currentType,
        page_size: 100000,
      }).then((res) => {
        const $table = this.$refs.xTable
        if ($table) {
          const nameColumn = $table.getVxetableRef().getColumnByField('accept_by')
          if (nameColumn) {
            const acceptByFilters = _.uniqBy(
              res.result
                .filter((item) => item.accept_by)
                .map((item) => ({
                  value: item.accept_by,
                  label: item.accept_by,
                })),
              'value'
            )
            $table.getVxetableRef().setFilter(
              nameColumn,
              acceptByFilters
            )
            this.acceptByFilters = acceptByFilters
          }
        }
        this.tableData = res.result.map((item) => ({ ..._.cloneDeep(item), ...item.instance }))
        if (isInit) {
          this.columns = this.getColumns(this.tableData, this.attributes)
          const xTable = this.$refs.xTable.getVxetableRef()
          xTable.refreshColumn()
        }
      })
    },
    getColumns(data, attrList) {
      const width = document.getElementById('discovery-ci').clientWidth - 50
      return getCITableColumns(data, attrList, width)
    },
    accept(row) {
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ad.confirmAccept'),
        onOk() {
          updateADCAccept(row.id).then(() => {
            that.$message.success(that.$t('cmdb.ad.acceptSuccess'))
            that.getAdc(false)
          })
        },
      })
    },
    deleteADC(row) {
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ad.deleteADC'),
        onOk() {
          deleteAdc(row.id).then(() => {
            that.$message.success(that.$t('deleteSuccess'))
            that.getAdc(false)
          })
        },
        onCancel() {},
      })
    },
    async batchAccept() {
      for (let i = 0; i < this.selectedRowKeys.length; i++) {
        await updateADCAccept(this.selectedRowKeys[i])
      }
      this.$message.success(this.$t('cmdb.ad.acceptSuccess'))
      this.getAdc(false)
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.xTable.getVxetableRef().clearSort()
    },
    async batchDelete() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ad.batchDelete'),
        async onOk() {
          for (let i = 0; i < that.selectedRowKeys.length; i++) {
            await deleteAdc(that.selectedRowKeys[i])
          }
          that.$message.success(that.$t('deleteSuccess'))
          that.getAdc(false)
          that.selectedRowKeys = []
          that.$refs.xTable.getVxetableRef().clearCheckboxRow()
          that.$refs.xTable.getVxetableRef().clearCheckboxReserve()
          that.$refs.xTable.getVxetableRef().clearSort()
        },
        onCancel() {},
      })
    },
    onSelectChange({ records, checked }) {
      this.selectedRowKeys = records.map((item) => item.id)
    },
    handleSearch(value) {
      this.searchValue = value
    },

    async clickLog() {
      this.logModalVisible = true
      const logRes = await getAdcExecHistories({
        type_id: this.currentType,
        page_size: 1000
      })
      let logTextArray = []
      if (logRes?.result?.length) {
        logTextArray = logRes.result.map((log) => {
          return `[${log.created_at}] ${log.stdout}`
        })
      }
      this.logTextArray = logTextArray
      this.$nextTick(() => {
        const textEl = this.$refs.logModelText
        if (textEl) {
          textEl.scrollTop = textEl.scrollHeight
        }
      })
    },
    getRowSeq(row) {
      return this.$refs.xTable.getVxetableRef().getRowSeq(row)
    }
  },
}
</script>

<style lang="less" scoped>
.cmdb-adc {
  .cmdb-adc-group {
    margin-bottom: 20px;
  }
  .cmdb-adc-side-item {
    .ops_popover_item();
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    .cmdb-adc-side-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 20px;
      height: 20px;
      border-radius: 2px;
      box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
      margin-right: 6px;
      background-color: #fff;
      img {
        max-height: 20px;
        max-width: 20px;
      }
    }
    .cmdb-adc-side-name {
      display: inline-block;
      width: calc(100% - 30px);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
  .cmdb-adc-side-item-selected {
    .ops_popover_item_selected();
    background-color: @primary-color_3;
  }

  .discovery-ci-header {
    display: flex;
    align-items: center;
    padding-top: 18px;
    padding-bottom: 10px;
  }

  .discovery-ci-log {
    cursor: pointer;
    background-color: #F4F9FF;
    border: solid 1px @primary-color_8;
    color: @primary-color;
    font-size: 12px;
    padding: 5px 12px;
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 6px;
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
}

.log-modal-title {
  font-size: 14px;
  font-weight: 500;
}

.log-modal-text {
  margin-top: 14px;
  padding: 12px;
  width: 100%;
  height: 312px;
  overflow: auto;
  border: solid 1px @border-color-base;
  background-color: #2f333d;

  &-item {
    color: #c5c8c6;
    width: 100%;
    display: block;
    white-space: pre-wrap;
    word-break: break-all;
  }
}
</style>
