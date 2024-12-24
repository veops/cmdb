<template>
  <div class="list-wrap">
    <div class="list-wrap-bg" v-if="!filterList.length">
      <img :src="require('@/modules/cmdb/assets/resourceSearch/resource_search_bg_2.png')" />
    </div>

    <div v-if="tabList.length" class="list-tab">
      <div class="list-tab-left">
        <div class="list-tab-label">{{ $t('cmdb.ciType.currentPage') }}: </div>
        <div
          v-for="(tab) in tabList"
          :key="tab.id"
          :class="['list-tab-item', tab.id === currentTab ? 'list-tab-item-active' : '']"
          @click="clickTab(tab.id)"
        >
          <span class="list-tab-item-title">{{ tab.title }}</span>
          (<span class="list-tab-item-count">{{ tab.count }}</span>)
        </div>
      </div>

      <a-button
        icon="download"
        type="primary"
        class="ops-button-ghost list-tab-export"
        ghost
        @click="handleExport"
      >
        {{ $t('download') }}
      </a-button>
    </div>

    <div v-if="filterList.length" class="list-container">
      <div
        v-for="(item) in filterList"
        :key="item._id"
        :class="['list-card', detailCIId === item.ci._id ? 'list-card-selected' : '']"
        @click="clickInstance(item.ci._id, item.ciTypeObj.id)"
      >
        <div class="list-card-header">
          <div class="list-card-model">
            <CIIcon
              :icon="item.ciTypeObj.icon"
              :title="item.ciTypeObj.name"
            />
            <span class="list-card-model-title">{{ item.ciTypeObj.title }}</span>
          </div>
          <div class="list-card-title">{{ item.ci[item.ciTypeObj.showAttrName] }}</div>

          <ops-icon
            v-if="getFavorId(item.ci._id)"
            type="veops-collected"
            class="list-card-collect"
            :style="{ color: '#FAD337' }"
            @click.stop="deleteCollect(item.ci._id)"
          />

          <ops-icon
            v-else
            type="veops-collect"
            class="list-card-collect"
            :style="{ color: '#A5A9BC' }"
            @click.stop="addCollect(item)"
          />
        </div>
        <div class="list-card-attr">
          <div
            v-for="(attr) in item.attributes"
            :key="attr.name"
            class="list-card-attr-item"
          >
            <div class="list-card-attr-item-label">{{ attr.alias || attr.name || '' }}: </div>
            <div class="list-card-attr-item-value">
              <AttrDisplay
                :attr="attr"
                :ci="item.ci"
                :referenceShowAttrNameMap="referenceShowAttrNameMap"
                :referenceCIIdMap="referenceCIIdMap"
                :isEllipsis="true"
                :searchValue="searchValue"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExcelJS from 'exceljs'
import FileSaver from 'file-saver'
import moment from 'moment'

import AttrDisplay from './attrDisplay.vue'
import CIIcon from '@/modules/cmdb/components/ciIcon/index.vue'

export default {
  name: 'InstanceList',
  components: {
    AttrDisplay,
    CIIcon
  },
  props: {
    list: {
      type: Array,
      default: () => []
    },
    tabList: {
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
    favorList: {
      type: Array,
      default: () => []
    },
    detailCIId: {
      type: [String, Number],
      default: -1
    },
    searchValue: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      currentTab: ''
    }
  },
  computed: {
    filterList() {
      if (!this.currentTab || this.currentTab === -1) {
        return this.list
      }

      return this.list.filter((item) => item.ciTypeObj.id === this.currentTab)
    }
  },
  watch: {
    tabList: {
      immediate: true,
      deep: true,
      handler(newVal) {
        this.currentTab = newVal?.[0]?.id ?? ''
      }
    }
  },
  methods: {
    clickTab(id) {
      this.currentTab = id
    },

    getAttrLabel(attrName, attributes) {
      const label = attributes.find((attr) => attr.name === attrName)?.alias
      return label || attrName
    },

    clickInstance(id, ciTypeId) {
      this.$emit('showDetail', {
        id,
        ciTypeId,
      })
    },
    getFavorId(ciId) {
      const id = this.favorList.find((item) => item?.option?.CIId === ciId)?.id
      return id ?? null
    },

    addCollect(data) {
      this.$emit('addCollect', {
        CIId: data.ci._id,
        CITypeId: data.ciTypeObj.id,
        title: data.ci[data.ciTypeObj.showAttrName],
        icon: data.ciTypeObj.icon,
        CITypeTitle: data.ciTypeObj.name
      })
    },

    deleteCollect(ciId) {
      const favorId = this.getFavorId(ciId)
      if (favorId) {
        this.$emit('deleteCollect', favorId)
      }
    },

    handleExport() {
      const excel_name = `cmdb-${this.$t('cmdb.ciType.resourceSearch')}-${moment().format('YYYYMMDDHHmmss')}.xlsx`
      const wb = new ExcelJS.Workbook()

      this.tabList.map((sheet) => {
        if (sheet.id === -1) {
          return
        }

        const ws = wb.addWorksheet(sheet.title)
        this.handleSheetData({
          ws,
          sheet
        })
      })

      wb.xlsx.writeBuffer().then((buffer) => {
        const file = new Blob([buffer], {
          type: 'application/octet-stream',
        })
        FileSaver.saveAs(file, excel_name)
      })
    },

    handleSheetData({
      ws,
      sheet
    }) {
      const listData = this.list.filter((item) => item.ciTypeObj.id === sheet.id)
      if (!listData.length) {
        return
      }

      const columnMap = new Map()
      const columns = listData[0].attributes.filter((attr) => !attr.is_password).map((attr) => {
        columnMap.set(attr.name, attr)

        return {
          header: attr.alias || attr.name || '',
          key: attr.name,
          width: 20,
        }
      })

      ws.columns = columns

      listData.forEach((data) => {
        const row = {}
        columns.forEach(({ key }) => {
          const value = data?.ci?.[key] ?? null
          const attr = columnMap.get(key)
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
    }
  }
}
</script>

<style lang="less" scoped>
.list-wrap {
  width: 100%;
  height: 100%;
  flex-shrink: 1 !important;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  &-bg {
    width: 100%;
    padding-top: 90px;
    display: flex;
    justify-content: center;

    img {
      width: 300px;
    }
  }

  .list-tab {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    column-gap: 14px;

    &-left {
      display: flex;
      align-items: center;
      column-gap: 14px;
      row-gap: 7px;
      overflow-x: auto;
      max-width: 100%;
    }

    &-label {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
      flex-shrink: 0;
    }

    &-item {
      display: flex;
      align-items: center;
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
      cursor: pointer;
      flex-shrink: 0;

      &-count {
        color: #2F54EB;
      }

      &-active {
        color: #2F54EB;
      }

      &:hover {
        color: #2F54EB;
      }
    }

    &-export {
      margin-left: auto;
      flex-shrink: 0;
    }
  }

  .list-container {
    width: 100%;
    margin-top: 12px;
    height: 100%;
    overflow-y: auto;
    flex-shrink: 1;
    flex-grow: 0;

    .list-card {
      width: 100%;
      background-color: #FFF;
      border-radius: 4px;
      padding: 15px;
      cursor: pointer;

      &:not(:first-child) {
        margin-top: 16px;
      }

      &-selected {
        border: 1px solid #7F97FA;
        background-color: #F9FBFF;
      }

      &-header {
        display: flex;
        align-items: center;
      }

      &-model {
        border-radius: 24px;
        border: 1px solid #E4E7ED;
        background-color: #FFF;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 24px;
        padding: 0 13px;
        flex-shrink: 0;

        &-title {
          font-size: 12px;
          font-weight: 400;
          line-height: 24px;
          color: #1D2129;
          margin-left: 4px;
        }
      }

      &-title {
        margin-left: 11px;
        font-size: 14px;
        font-weight: 700;
        color: #1D2129;

        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        text-wrap: nowrap;
      }

      &-collect {
        font-size: 12px;
        margin-left: 9px;
        display: none;
      }

      &-attr {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        overflow: hidden;
        height: 25px;
        column-gap: 40px;
        row-gap: 20px;
        margin-top: 12px;

        &-item {
          flex-shrink: 0;
          max-width: calc((100% - 160px) / 5);
          display: flex;
          align-items: center;
          overflow: hidden;

          &-label {
            color: #86909C;
            font-size: 14px;
            font-weight: 400;
            flex-shrink: 0;
          }

          &-value {
            color: #1D2129;
            font-size: 14px;
            font-weight: 400;
            margin-left: 12px;
            overflow: hidden;
          }
        }
      }

      &:hover {
        box-shadow: ~'0px 2px 12px 0px @{primary-color}15';

        .list-card-collect {
          display: inline-block;
        }
      }
    }
  }
}
</style>
