<template>
  <div class="search-table">
    <div class="search-table-header">
      <div class="table-tab">
        <div
          v-for="(tab) in tabList"
          :key="tab.value"
          :class="['table-tab-item', tabActive === tab.value ? 'table-tab-item_active' : '']"
          @click="clickTab(tab.value)"
        >
          {{ tab.value }}
          (<span class="table-tab-item-count">{{ tab.count }}</span>)
        </div>
      </div>

      <a-button
        v-if="tableData.ciList && tableData.ciList.length"
        type="primary"
        class="ops-button-ghost search-table-export"
        ghost
        @click="handleExport"
      >
        <ops-icon type="veops-export" />
        {{ $t('export') }}
      </a-button>
    </div>

    <ops-table
      ref="xTable"
      show-overflow
      :data="tableData.ciList"
      size="small"
      :height="`${tableHeight}px`"
      :cell-class-name="getCellClassName"
      :header-cell-class-name="getHeaderCellClassName"
      :checkbox-config="{ range: true }"
      :loading="isSearchLoading"
      :column-config="{ resizable: true }"
      :resizable-config="{ minWidth: 60 }"
      class="checkbox-hover-table"
      @checkbox-change="onSelectChange"
      @checkbox-all="onSelectChange"
      @checkbox-range-end="onSelectChange"
    >
      <vxe-table-column
        v-if="tableData.ciList && tableData.ciList.length"
        align="center"
        type="checkbox"
        width="60"
      >
        <template #default="{row}">
          {{ getRowSeq(row) }}
        </template>
      </vxe-table-column>

      <template
        v-if="returnPath && tableData.pathList && tableData.pathList.length"
      >
        <vxe-table-column
          v-for="(path, index) in tableData.pathList"
          class="table-path-column"
          :key="`${path.id}-${index}`"
          :title="tableData.pathList[index].name"
          :field="path.id"
          :show-header-overflow="false"
          :width="index !== tableData.pathList.length - 1 ? 160 : 100"
        >
          <template #header>
            <div class="table-path-header">
              <span
                class="table-path-header-name"
                :style="{
                  maxWidth: tableData.pathList[index].relation ? '70px' : '100%'
                }"
              >
                <a-tooltip :title="tableData.pathList[index].name">
                  {{ tableData.pathList[index].name }}
                </a-tooltip>
              </span>
              <div
                class="table-path-header-right"
                v-if="tableData.pathList[index].relation"
              >
                <span class="table-path-header-line">
                  <a-icon
                    type="caret-right"
                    class="table-path-header-line-arrow"
                  />
                </span>
                <span
                  class="table-path-header-relation"
                >
                  <span class="table-path-header-relation-text">
                    <a-tooltip :title="tableData.pathList[index].relation">
                      {{ tableData.pathList[index].relation }}
                    </a-tooltip>
                  </span>
                </span>
              </div>
            </div>
          </template>
          <template #default="{ row, columnIndex }">
            <span
              v-if="columnIndex === 1"
              v-html="markSearchValue(row.pathCI[path.id])"
            ></span>
            <span v-else >{{ row.pathCI[path.id] }}</span>
          </template>
        </vxe-table-column>
      </template>

      <template v-if="tableData.ciAttr && tableData.ciAttr.length">
        <vxe-table-column
          v-for="(attr, index) in tableData.ciAttr"
          :key="`${attr.name}_${index}`"
          :title="attr.alias || attr.name || ''"
          :field="attr.name"
          :width="attr.width"
          :show-header-overflow="true"
        >
          <template #default="{ row }">
            <AttrDisplay
              :attr="attr"
              :ci="row.targetCI"
              :referenceShowAttrNameMap="referenceShowAttrNameMap"
              :referenceCIIdMap="referenceCIIdMap"
            />
          </template>
        </vxe-table-column>
      </template>
    </ops-table>

    <BatchDownload
      ref="batchDownload"
      :showFileTypeSelect="false"
      @batchDownload="batchDownload"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import ExcelJS from 'exceljs'
import FileSaver from 'file-saver'
import AttrDisplay from '@/modules/cmdb/views/resource_search_2/resourceSearch/components/attrDisplay.vue'
import BatchDownload from '@/modules/cmdb/components/batchDownload/batchDownload.vue'

export default {
  name: 'CITable',
  components: {
    AttrDisplay,
    BatchDownload
  },
  props: {
    allTableData: {
      type: Object,
      default: () => {}
    },
    tabActive: {
      type: String,
      default: ''
    },
    returnPath: {
      type: Boolean,
      default: false
    },
    isHideSearchCondition: {
      type: Boolean,
      default: false,
    },
    referenceShowAttrNameMap: {
      type: Object,
      default: () => {}
    },
    referenceCIIdMap: {
      type: Object,
      default: () => {}
    },
    searchValue: {
      type: String,
      default: ''
    },
    isSearchLoading: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return this.isHideSearchCondition ? this.windowHeight - 308 : this.windowHeight - 458
    },
    tableData() {
      return this.allTableData?.[this.tabActive] || {}
    },
    tabList() {
      const keys = Object.keys(this.allTableData) || []
      return keys.map((key) => {
        return {
          value: key,
          count: this.allTableData?.[key]?.count || 0
        }
      })
    },
  },
  data() {
    return {}
  },
  methods: {
    markSearchValue(text) {
      if (!text || !this.searchValue) {
        return text
      }
      const regex = new RegExp(`(${this.searchValue})`, 'gi')
      return String(text).replace(
        regex,
        `<span style="background-color: #D3EEFE; padding: 0 2px;">$1</span>`
      )
    },

    clickTab(tab) {
      this.$emit('updateTab', tab)
    },

    getRowSeq(row) {
      const table = this.$refs?.['xTable']?.getVxetableRef?.() || null
      return table?.getRowSeq?.(row)
    },
    getCellClassName({ columnIndex }) {
      const pathLength = this.tableData?.pathList?.length
      if (columnIndex <= pathLength && this.returnPath) {
        return 'table-path-cell'
      }
      return ''
    },
    getHeaderCellClassName({ columnIndex }) {
      const pathLength = this.tableData?.pathList?.length
      if (columnIndex <= pathLength && this.returnPath) {
        return 'table-path-header-cell'
      }
      return ''
    },

    handleExport() {
      const preferenceAttrList = []
      if (this.returnPath && this.tableData?.pathList?.length) {
        preferenceAttrList.push(...this.tableData.pathList.map((path) => {
          return {
            name: path.id,
            alias: path.name
          }
        }))
      }

      if (this.tableData?.ciAttr?.length) {
        const ciAttr = _.cloneDeep(this.tableData.ciAttr)
        ciAttr.forEach((attr) => {
          attr.alias = attr.alias || attr.name
        })
        preferenceAttrList.push(...ciAttr)
      }

      this.$refs.batchDownload.open({
        preferenceAttrList,
        ciTypeName: this.tabActive || '',
      })
    },
    batchDownload({ checkedKeys, filename }) {
      const wb = new ExcelJS.Workbook()

      const tableRef = this.$refs.xTable.getVxetableRef()
      let tableData = _.cloneDeep([
        ...tableRef.getCheckboxReserveRecords(),
        ...tableRef.getCheckboxRecords(true),
      ])
      if (!tableData.length) {
        const { fullData } = tableRef.getTableData()
        tableData = _.cloneDeep(fullData)
      }

      const ws = wb.addWorksheet(this.tabActive)

      const pathColumns = []
      const targetColumns = []

      if (this.returnPath) {
        const pathFilter = this.tableData.pathList.filter((path) => checkedKeys.includes(path.id))

        pathFilter.forEach((path) => {
          pathColumns.push({
            header: path.name || '',
            key: path.id,
            width: 20,
          })
        })
      }

      const attrMap = new Map()
      const attrFilter = this.tableData.ciAttr.filter((attr) => checkedKeys.includes(attr.name))
      attrFilter.forEach((attr) => {
        attrMap.set(attr.name, attr)

        targetColumns.push({
          header: attr.alias || attr.name || '',
          key: attr.name,
          width: 20,
        })
      })

      ws.columns = [
        ...pathColumns,
        ...targetColumns
      ]

      tableData.forEach(({ pathCI, targetCI }) => {
        const row = {}
        if (this.returnPath) {
          pathColumns.forEach(({ key }) => {
            row[key] = pathCI?.[key] || ''
          })
        }

        targetColumns.forEach(({ key }) => {
          const value = targetCI?.[key] ?? null
          const attr = attrMap.get(key)
          if (attr.valueType === '6') {
            row[key] = value ? JSON.stringify(value) : value
          } else if (attr.is_list && Array.isArray(value)) {
            row[key] = value.join(',')
          } else {
            row[key] = value
          }
        })

        ws.addRow(row)
      })

      wb.xlsx.writeBuffer().then((buffer) => {
        const file = new Blob([buffer], {
          type: 'application/octet-stream',
        })
        FileSaver.saveAs(file, `${filename}.xlsx`)
      })

      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
    },

    onSelectChange() {
      console.log('onSelectChange')
    },
  }
}
</script>

<style lang="less" scoped>
.search-table {
  width: 100%;

  &-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between
  }

  &-export {
    flex-shrink: 0;
    margin-left: 12px;
  }

  .table-tab {
    display: flex;
    align-items: center;
    column-gap: 35px;
    padding-bottom: 6px;
    margin-bottom: 18px;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: hidden;

    &-item {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
      cursor: pointer;
      flex-shrink: 0;

      &-count {
        color: #2F54EB;
      }

      &_active {
        color: #2F54EB;
      }

      &:hover {
        color: #2F54EB;
      }
    }
  }

  .table-path-header {
    position: relative;
    display: flex;
    align-items: center;

    &-name {
      max-width: 80px;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
      position: relative;
      z-index: 1;
      flex-shrink: 0;
    }

    &-right {
      display: flex;
      align-items: center;
      width: 100%;
      margin-left: 10px;
      margin-right: -5px;
      position: relative;
    }

    &-line {
      width: 100%;
      height: 1px;
      position: relative;
      background-color: #CACDD9;
      z-index: 0;

      &-arrow {
        position: absolute;
        right: -6px;
        top: -6px;
        font-size: 12px;
        color: #CACDD9;
      }
    }

    &-relation {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #FFFFFF;
      border: solid 1px #E4E7ED;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
      border-radius: 22px;
      z-index: 2;
      max-width: 70px;
      width: fit-content;

      &-text {
        font-size: 12px;
        font-weight: 400;
        color: #A5A9BC;

        overflow: hidden;
        text-overflow: ellipsis;
        text-wrap: nowrap;
        width: 100%;
      }
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

  /deep/ .table-path-header-cell {
    background-color: #EBEFF8 !important;

    .vxe-cell--title {
      width: 100%;
      overflow: visible;
    }
  }

  /deep/ .table-path-cell {
    background-color: #F9FBFF;
  }

  /deep/ .attr-display {
    display: inline;
  }
}
</style>
