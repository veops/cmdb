<template>
  <TwoColumnLayout appName="cmdb-adc">
    <template #one>
      <div v-for="group in ci_types_list" :key="group.id">
        <div>
          <strong>{{ group.name || '其他' }}</strong
          ><span :style="{ color: 'rgb(195, 205, 215)' }">({{ group.ci_types.length }})</span>
        </div>
        <div
          :class="{ 'cmdb-adc-side-item': true, 'cmdb-adc-side-item-selected': currentType === type.id }"
          v-for="type in group.ci_types"
          :key="type.id"
          @click="clickSidebar(type.id)"
        >
          <span class="cmdb-adc-side-icon">
            <ops-icon
              :style="{
                color: type.icon.split('$$')[1],
                fontSize: '14px',
              }"
              v-if="type.icon"
              :type="type.icon.split('$$')[0]"
            />
            <span :style="{ color: '#2f54eb' }" v-else>{{ type.name[0].toUpperCase() }}</span>
          </span>
          <span :title="type.alias || type.name" class="cmdb-adc-side-name">{{ type.alias || type.name }}</span>
        </div>
      </div>
    </template>
    <template #two>
      <div id="discovery-ci">
        <a-input-search
          placeholder="请查找"
          class="ops-input ops-input-radius"
          :style="{ width: '200px', marginRight: '20px', marginBottom: '10px' }"
          @search="handleSearch"
          allowClear
        />
        <div class="ops-list-batch-action" :style="{ marginBottom: '10px' }" v-show="!!selectedRowKeys.length">
          <span @click="batchAccept">入库</span>
          <a-divider type="vertical" />
          <span @click="batchDelete">删除</span>
          <span>选取：{{ selectedRowKeys.length }} 项</span>
        </div>
        <ops-table
          show-overflow
          show-header-overflow
          resizable
          ref="xTable"
          size="mini"
          stripe
          class="ops-stripe-table"
          :data="filterTableData"
          :height="tableHeight"
          :scroll-y="{ enabled: true, gt: 50 }"
          :scroll-x="{ enabled: true, gt: 0 }"
          @checkbox-change="onSelectChange"
          @checkbox-all="onSelectChange"
          @checkbox-range-end="onSelectChange"
          :checkbox-config="{reserve: true, highlight: true, range: true}"
          :sort-config="{ remote: false, trigger: 'cell' }"
        >
          <vxe-column align="center" type="checkbox" width="60"></vxe-column>
          <vxe-column
            v-for="col in columns"
            :key="col.field"
            :title="col.title"
            :field="col.field"
            :width="col.width"
            :sortable="col.sortable"
          >
            <template v-if="col.value_type === '6'" #default="{row}">
              <span v-if="col.value_type === '6' && row[col.field]">{{ row[col.field] }}</span>
            </template>
          </vxe-column>
          <vxe-column
            align="center"
            field="is_accept"
            title="是否入库"
            v-bind="columns.length ? { width: '100px' } : { minWidth: '100px' }"
            :filters="[
              { label: '是', value: true },
              { label: '否', value: false },
            ]"
          >
            <template #default="{row}">
              {{ row.is_accept ? '是' : '否' }}
            </template>
          </vxe-column>
          <vxe-column
            field="accept_by"
            title="入库人"
            v-bind="columns.length ? { width: '80px' } : { minWidth: '80px' }"
            :filters="[]"
          ></vxe-column>
          <vxe-column
            field="accept_time"
            title="入库时间"
            sortable
            v-bind="columns.length ? { width: '130px' } : { minWidth: '130px' }"
          ></vxe-column>
          <vxe-column title="操作" v-bind="columns.length ? { width: '60px' } : { minWidth: '60px' }" align="center">
            <template #default="{row}">
              <a-space>
                <a-tooltip title="入库">
                  <a v-if="!row.is_accept" @click="accept(row)"><ops-icon type="icon-xianxing-edit"/></a>
                </a-tooltip>
                <a :style="{ color: 'red' }" @click="deleteADC(row)"><ops-icon type="icon-xianxing-delete"/></a>
              </a-space>
            </template>
          </vxe-column>
          <template #empty>
            <div>
              <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
              <div>暂无数据</div>
            </div>
          </template>
        </ops-table>
      </div>
    </template>
  </TwoColumnLayout>
</template>

<script>
import _ from 'lodash'
import XEUtils from 'xe-utils'
import TwoColumnLayout from '@/components/TwoColumnLayout'
import { getADCCiTypes, getAdc, updateADCAccept, getADCCiTypesAttrs, deleteAdc } from '../../api/discovery'
import { getCITableColumns } from '../../utils/helper'
export default {
  name: 'DiscoveryCI',
  components: { TwoColumnLayout },
  data() {
    return {
      ci_types_list: [],
      currentType: null,
      attributes: [],
      tableData: [],
      columns: [],
      selectedRowKeys: [],
      searchValue: '',
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      return this.windowHeight - 140
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
    },
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
  },
  mounted() {
    getADCCiTypes({ need_other: true }).then((res) => {
      this.ci_types_list = res.filter((item) => item.ci_types && item.ci_types.length)
      const _currentType = localStorage.getItem('ops_adc_typeid')
      if (_currentType) {
        this.clickSidebar(Number(_currentType))
        return
      }
      if (res && res.length) {
        this.clickSidebar(res[0].id)
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
            $table.getVxetableRef().setFilter(
              nameColumn,
              _.uniqBy(
                res.result
                  .filter((item) => item.accept_by)
                  .map((item) => ({
                    value: item.accept_by,
                    label: item.accept_by,
                  })),
                'value'
              )
            )
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
        title: '警告',
        content: `确认入库？`,
        onOk() {
          updateADCAccept(row.id).then(() => {
            that.$message.success('入库成功')
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
        title: '警告',
        content: `确认删除该条数据？`,
        onOk() {
          deleteAdc(row.id).then(() => {
            that.$message.success('删除成功')
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
      this.$message.success('入库成功')
      this.getAdc(false)
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.xTable.getVxetableRef().clearSort()
    },
    async batchDelete() {
      const that = this
      this.$confirm({
        title: '警告',
        content: `确认删除这些数据？`,
        async onOk() {
          for (let i = 0; i < that.selectedRowKeys.length; i++) {
            await deleteAdc(that.selectedRowKeys[i])
          }
          that.$message.success('删除成功')
          that.getAdc(false)
          that.selectedRowKeys = []
          that.$refs.xTable.getVxetableRef().clearCheckboxRow()
          that.$refs.xTable.getVxetableRef().clearCheckboxReserve()
          that.$refs.xTable.getVxetableRef().clearSort()
        },
        onCancel() {},
      })
    },
    onSelectChange({ records, checked, row }) {
      this.selectedRowKeys = records.map((item) => item.id)
    },
    handleSearch(value) {
      this.searchValue = value
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.cmdb-adc {
  .cmdb-adc-side-item {
    .ops_popover_item();
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    .cmdb-adc-side-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 20px;
      height: 20px;
      border-radius: 2px;
      box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
      margin-right: 6px;
      background-color: #fff;
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
    background-color: #custom_colors[color_2];
  }
}
</style>