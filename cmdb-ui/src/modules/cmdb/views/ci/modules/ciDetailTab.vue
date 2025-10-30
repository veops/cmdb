<template>
  <div :style="{ height: '100%' }">
    <a-tabs v-if="hasPermission" class="ci-detail-tab" v-model="activeTabKey" @change="changeTab">
      <a @click="shareCi" slot="tabBarExtraContent" :style="{ marginRight: '24px' }">
        <a-icon type="share-alt" />
        {{ $t('cmdb.ci.share') }}
      </a>
      <a-tab-pane key="tab_1">
        <span slot="tab"><a-icon type="book" />{{ $t('cmdb.ci.detail') }}</span>

        <div class="ci-detail-table">
          <CIDetailTitle :ci="ci" :ci_types="ci_types" />

          <div class="ci-detail-table-attr">
            <CIDetailTableTitle :title="$t('cmdb.attribute')" />

            <div class="ci-detail-table-attr-wrap">
              <div
                v-for="group in attributeGroups"
                :key="group.name"
                class="ci-detail-table-attr-group"
              >
                <div class="ci-detail-table-attr-group-name">
                  {{ group.name || $t('other') }}
                </div>

                <div class="ci-detail-attrs-grid">
                  <div
                    v-for="attr in group.attributes"
                    :key="attr.name"
                    :class="['ci-detail-attr-item', attr._isTableFormatDisplay ? 'ci-detail-attr-item-full' : '']"
                  >
                    <div class="ci-detail-attr-label">
                      <a-tooltip :title="attr.alias || attr.name">
                        <span class="ci-detail-attr-label-text">{{ attr.alias || attr.name }}</span>
                      </a-tooltip>
                      <span class="ci-detail-attr-label-colon">:</span>
                    </div>
                    <div class="ci-detail-attr-content">
                      <CIDetailAttrContent
                        :ci="ci"
                        :attr="attr"
                        :attributeGroups="attributeGroups"
                        @refresh="refresh"
                        @updateCIByself="updateCIByself"
                        @refreshReferenceAttr="handleReferenceAttr"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <CIRelationTable
            :ciId="ciId"
            :typeId="typeId"
            :ci="ci"
            :relationData="relationData"
            @refreshRelationCI="refreshRelationCI(ciId)"
          />
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_2">
        <span slot="tab"><a-icon type="branches" />{{ $t('cmdb.ci.topo') }}</span>
        <div :style="{ height: '100%', padding: '24px', overflow: 'auto' }">
          <CIDetailRelation
            :ciId="ciId"
            :typeId="typeId"
            :ci="ci"
            :relationData="relationData"
          />
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_3">
        <span slot="tab"><a-icon type="clock-circle" />{{ $t('cmdb.ci.changeHistory') }}</span>
        <div class="ci-history-container">
          <!-- Statistics Information Card -->
          <div class="ci-history-stats">
            <div
              v-for="stat in ciHistoryStatsList"
              :key="stat.type"
              class="ci-history-stat-card"
            >
              <div :class="`stat-icon stat-icon-${stat.type}`">
                <a-icon :type="stat.icon" />
              </div>
              <div class="stat-content">
                <div class="stat-label">{{ $t(stat.label) }}</div>
                <div class="stat-value">{{ stat.value === 'total' ? ciHistory.length : getOperateTypeCount(stat.value) }}</div>
              </div>
            </div>
          </div>

          <!-- Operation Button Group -->
          <div class="ci-history-actions">
            <a-button type="primary" class="ops-button-ghost" ghost @click="handleRollbackCI()">
              <ops-icon type="shishizhuangtai" />
              {{ $t('cmdb.ci.rollback') }}
            </a-button>
            <a-button type="primary" class="ops-button-ghost" ghost @click="handleExport">
              <ops-icon type="veops-export" />
              {{ $t('export') }}
            </a-button>
          </div>
          <CIRollbackForm ref="ciRollbackForm" :ciIds="[ciId]" @getCIHistory="getCIHistory" />

          <!-- Change Log Table -->
          <vxe-table
            ref="xTable"
            show-overflow
            show-header-overflow
            :data="ciHistory"
            size="small"
            :height="tableHeight - 130"
            highlight-hover-row
            :span-method="mergeRowMethod"
            :scroll-y="{ enabled: false, gt: 20 }"
            :scroll-x="{ enabled: false, gt: 0 }"
            border
            resizable
            class="ops-unstripe-table ci-history-table"
          >
            <template #empty>
              <a-empty :image-style="{ height: '100px' }" :style="{ paddingTop: '10%' }">
                <img slot="image" :src="require('@/assets/data_empty.png')" />
                <span slot="description"> {{ $t('noData') }} </span>
              </a-empty>
            </template>
            <vxe-table-column sortable field="created_at" :title="$t('created_at')" width="180"></vxe-table-column>
            <vxe-table-column
              field="username"
              :title="$t('user')"
              :filters="[]"
              :filter-method="filterUsernameMethod"
              width="140"
            ></vxe-table-column>
            <vxe-table-column
              field="operate_type"
              :filters="[
                { value: 0, label: $t('new') },
                { value: 1, label: $t('delete') },
                { value: 2, label: $t('update') },
              ]"
              :filter-method="filterOperateMethod"
              :title="$t('operation')"
              width="120"
            >
              <template #default="{ row }">
                <OperateTypeTag :operateType="operateTypeMap[row.operate_type]" :showIcon="false" />
              </template>
            </vxe-table-column>
            <vxe-table-column
              field="attr_alias"
              :title="$t('cmdb.attribute')"
              :filters="[]"
              :filter-method="filterAttrMethod"
              width="180"
            >
              <template #default="{ row }">
                <a-tag color="blue" :style="{ borderRadius: '4px' }">{{ row.attr_alias }}</a-tag>
              </template>
            </vxe-table-column>
            <vxe-table-column :cell-type="'string'" field="old" :title="$t('cmdb.history.old')" min-width="200">
              <template #default="{ row }">
                <div class="ci-history-value ci-history-value-old">
                  <span v-if="row.value_type === '6'">{{ JSON.parse(row.old) }}</span>
                  <span v-else>{{ row.old || '-' }}</span>
                </div>
              </template>
            </vxe-table-column>
            <vxe-table-column :cell-type="'string'" field="new" :title="$t('cmdb.history.new')" min-width="200">
              <template #default="{ row }">
                <div class="ci-history-value ci-history-value-new">
                  <span v-if="row.value_type === '6'">{{ JSON.parse(row.new) }}</span>
                  <span v-else>{{ row.new || '-' }}</span>
                </div>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_4">
        <span slot="tab"><ops-icon type="itsm_auto_trigger" />{{ $t('cmdb.history.triggerHistory') }}</span>
        <div :style="{ padding: '24px', height: '100%' }">
          <TriggerTable :ci_id="ci._id" />
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_5">
        <span slot="tab"><ops-icon type="itsm-association" />{{ $t('cmdb.ci.relITSM') }}</span>
        <div :style="{ padding: '24px', height: '100%' }">
          <RelatedItsmTable ref="relatedITSMTable" :ci_id="ci._id" :ciHistory="ciHistory" :itsmInstalled="itsmInstalled" :attrList="attrList" />
        </div>
      </a-tab-pane>
    </a-tabs>
    <a-empty
      v-else
      :image-style="{
        height: '100px',
      }"
      :style="{ paddingTop: '20%' }"
    >
      <img slot="image" :src="require('@/assets/data_empty.png')" />
      <span slot="description"> {{ $t('cmdb.ci.noPermission') }} </span>
    </a-empty>
  </div>
</template>

<script>
import _ from 'lodash'
import { getCITypeGroupById, getCITypes } from '@/modules/cmdb/api/CIType'
import { getCIHistory, judgeItsmInstalled } from '@/modules/cmdb/api/history'
import { getCIById, searchCI } from '@/modules/cmdb/api/ci'

import RelationMixin from './ciDetailMixin/relationMixin.js'

import CIDetailTitle from './ciDetailComponent/ciDetailTitle.vue'
import CIDetailTableTitle from './ciDetailComponent/ciDetailTableTitle.vue'
import CIDetailAttrContent from './ciDetailAttrContent.vue'
import CIRelationTable from './ciDetailComponent/ciRelationTable.vue'
import CIDetailRelation from './ciDetailRelation.vue'
import TriggerTable from '../../operation_history/modules/triggerTable.vue'
import RelatedItsmTable from './ciDetailRelatedItsmTable.vue'
import CIRollbackForm from './ciRollbackForm.vue'
import OperateTypeTag from '../../operation_history/components/OperateTypeTag.vue'

export default {
  name: 'CiDetailTab',
  mixins: [RelationMixin],
  components: {
    CIDetailAttrContent,
    CIDetailRelation,
    TriggerTable,
    RelatedItsmTable,
    CIRollbackForm,
    CIDetailTitle,
    CIDetailTableTitle,
    CIRelationTable,
    OperateTypeTag
  },
  props: {
    typeId: {
      type: Number,
      required: true,
    },
    treeViewsLevels: {
      type: Array,
      default: () => [],
    },
    attributeHistoryTableHeight: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      ci: {},
      item: [],
      attributeGroups: [],
      activeTabKey: 'tab_1',
      rowSpanMap: {},
      ciHistory: [],
      ciId: null,
      ci_types: [],
      hasPermission: true,
      itsmInstalled: true,
      tableHeight: this.attributeHistoryTableHeight || (this.$store.state.windowHeight - 130),
      initQueryLoading: true,
      ciHistoryStatsList: [
        {
          label: 'cmdb.history.totalChanges',
          icon: 'history',
          type: 'total',
          value: 'total',
        },
        {
          label: 'new',
          icon: 'plus-circle',
          type: 'new',
          value: 0,
        },
        {
          label: 'update',
          icon: 'edit',
          type: 'update',
          value: 2,
        },
        {
          label: 'delete',
          icon: 'delete',
          type: 'delete',
          value: 1,
        }
      ]
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
  provide() {
    return {
      ci_types: () => {
        return this.ci_types
      },
    }
  },
  inject: {
    reload: {
      from: 'reload',
      default: null,
    },
    handleSearch: {
      from: 'handleSearch',
      default: null,
    },
    attrList: {
      from: 'attrList',
      default: () => [],
    },
  },
  methods: {
    async create(ciId, activeTabKey = 'tab_1') {
      this.initQueryLoading = true
      this.activeTabKey = activeTabKey
      this.ciId = ciId

      await this.getCI()
      await this.judgeItsmInstalled()
      if (this.hasPermission) {
        this.getAttributes()
        this.getCIHistory()
        const ciTypeRes = await getCITypes()
        this.ci_types = ciTypeRes.ci_types

        this.initRelationData(this.typeId, this.ciId)
      }
      this.initQueryLoading = false
    },
    getAttributes() {
      getCITypeGroupById(this.typeId, { need_other: 1 })
        .then((res) => {
          this.attributeGroups = (res || []).filter((group) => group?.attributes?.length)

          this.handleReferenceAttr()
        })
        .catch((e) => {})
    },

    async handleReferenceAttr() {
      const map = {}
      this.attributeGroups.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id && this.ci[attr.name]) {
            const ids = Array.isArray(this.ci[attr.name]) ? this.ci[attr.name] : this.ci[attr.name] ? [this.ci[attr.name]] : []
            if (ids.length) {
              if (!map?.[attr.reference_type_id]) {
                map[attr.reference_type_id] = {}
              }
              ids.forEach((id) => {
                map[attr.reference_type_id][id] = {}
              })
            }
          }
        })
      })

      if (!Object.keys(map).length) {
        return
      }

      const ciTypesRes = await getCITypes({
        type_ids: Object.keys(map).join(',')
      })
      const showAttrNameMap = {}
      ciTypesRes.ci_types.forEach((ciType) => {
        showAttrNameMap[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      const ciNameMap = {}
      allRes.forEach((res) => {
        res.result.forEach((item) => {
          ciNameMap[item._id] = item
        })
      })

      const newAttrGroups = _.cloneDeep(this.attributeGroups)

      newAttrGroups.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            attr.showAttrName = showAttrNameMap?.[attr?.reference_type_id] || ''

            const referenceShowAttrNameMap = {}
            const referenceCIIds = this.ci[attr.name];
            (Array.isArray(referenceCIIds) ? referenceCIIds : referenceCIIds ? [referenceCIIds] : []).forEach((id) => {
              referenceShowAttrNameMap[id] = ciNameMap?.[id]?.[attr.showAttrName] ?? id
            })
            attr.referenceShowAttrNameMap = referenceShowAttrNameMap
          }
        })
      })

      this.$set(this, 'attributeGroups', newAttrGroups)
    },

    async getCI() {
      await getCIById(this.ciId)
        .then((res) => {
          if (res.result.length) {
            this.ci = res.result[0]
          } else {
            this.hasPermission = false
          }
        })
        .catch((e) => {
          if (e.response.status === 404) {
            this.itsmInstalled = false
          }
        })
    },
    async judgeItsmInstalled() {
      await judgeItsmInstalled().catch((e) => {
        this.itsmInstalled = false
      })
    },

    getCIHistory() {
      getCIHistory(this.ciId)
        .then((res) => {
          this.ciHistory = res

          const rowSpanMap = {}
          let startIndex = 0
          let startCount = 1
          res.forEach((item, index) => {
            if (index === 0) {
              return
            }
            if (res[index].record_id === res[startIndex].record_id) {
              startCount += 1
              rowSpanMap[index] = 0
              if (index === res.length - 1) {
                rowSpanMap[startIndex] = startCount
              }
            } else {
              rowSpanMap[startIndex] = startCount
              startIndex = index
              startCount = 1
              if (index === res.length - 1) {
                rowSpanMap[index] = 1
              }
            }
          })
          this.rowSpanMap = rowSpanMap
        })
        .catch((e) => {
          console.log(e)
        })
    },
    changeTab(key) {
      this.activeTabKey = key
      if (key === 'tab_3') {
        this.$nextTick(() => {
          const $table = this.$refs.xTable
          if ($table) {
            const usernameColumn = $table.getColumnByField('username')
            const attrColumn = $table.getColumnByField('attr_alias')
            if (usernameColumn) {
              const usernameList = [...new Set(this.ciHistory.map((item) => item.username))]
              $table.setFilter(
                usernameColumn,
                usernameList.map((item) => {
                  return {
                    value: item,
                    label: item,
                  }
                })
              )
            }
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
      }
    },
    filterUsernameMethod({ value, row, column }) {
      return row.username === value
    },
    filterOperateMethod({ value, row, column }) {
      return Number(row.operate_type) === Number(value)
    },
    filterAttrMethod({ value, row, column }) {
      return row.attr_alias === value
    },
    refresh(editAttrName) {
      this.getCI()
      const _find = this.treeViewsLevels.find((level) => level.name === editAttrName)
      // 修改的字段为树形视图订阅的字段 则全部reload
      setTimeout(() => {
        if (_find) {
          if (this.reload) {
            this.reload()
          }
        } else {
          if (this.handleSearch) {
            this.handleSearch()
          }
        }
      }, 500)
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['created_at', 'username']
      const cellValue1 = row['created_at']
      const cellValue2 = row['username']
      if (cellValue1 && cellValue2 && fields.includes(column.property)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow['created_at'] === cellValue1 && prevRow['username'] === cellValue2) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow['created_at'] === cellValue1 && nextRow['username'] === cellValue2) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },
    updateCIByself(params, editAttrName) {
      const _ci = { ..._.cloneDeep(this.ci), ...params }
      this.ci = _ci
      const _find = this.treeViewsLevels.find((level) => level.name === editAttrName)
      // 修改的字段为树形视图订阅的字段 则全部reload
      setTimeout(() => {
        if (_find) {
          if (this.reload) {
            this.reload()
          }
        } else {
          if (this.handleSearch) {
            this.handleSearch()
          }
        }
      }, 500)
    },
    shareCi() {
      const text = `${document.location.host}/cmdb/cidetail/${this.typeId}/${this.ciId}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },
    handleRollbackCI() {
      this.$nextTick(() => {
        this.$refs.ciRollbackForm.onOpen()
      })
    },
    async handleExport() {
      this.$refs.xTable.exportData({
        filename: this.$t('cmdb.ci.history'),
        sheetName: 'Sheet1',
        type: 'xlsx',
        types: ['xlsx', 'csv', 'html', 'xml', 'txt'],
        data: this.ciHistory,
        isMerge: true,
        isColgroup: true,
      })
    },

    getOperateTypeCount(operateType) {
      return this.ciHistory.filter((item) => Number(item.operate_type) === Number(operateType)).length
    }
  },
}
</script>

<style lang="less">
.ci-detail-tab {
  height: 100%;
  .ant-tabs-content {
    height: calc(100% - 45px);
    .ant-tabs-tabpane {
      height: 100%;
    }
  }
  .ant-tabs-bar {
    margin: 0;
  }
  .ant-tabs-extra-content {
    line-height: 44px;
  }
  .ci-detail-table {
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 20px;
    background-color: #f5f7fa;

    &-attr {
      width: 100%;
      margin-top: 16px;

      &-wrap {
        padding: 20px;
        width: 100%;
        border: none;
        background: #ffffff;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
      }

      &-group {
        &:not(:last-child) {
          margin-bottom: 24px;
          padding-bottom: 24px;
          border-bottom: 1px solid #e8eaed;
        }

        &-name {
          font-size: 14px;
          font-weight: 600;
          color: @text-color_1;
          margin-bottom: 16px;
          width: 100%;
          text-align: left;
          display: flex;
          align-items: center;
          position: relative;
          padding-left: 12px;
          line-height: 16px;

          &::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 4px;
            height: 16px;
            background: @primary-color;
            border-radius: 2px;
          }
        }
      }
    }
  }

  // 属性Grid布局
  .ci-detail-attrs-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px 18px;
  }

  .ci-detail-attr-item {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 8px;
    padding: 8px 12px;
    transition: background-color 0.2s ease;
    border-radius: 4px;
    min-height: 28px;
    align-items: center;

    &:hover {
      background-color: #f8f9fb;
    }

    &-full {
      grid-column: ~"1 / -1";
      grid-template-columns: 120px 1fr;
      align-items: flex-start;
    }
  }

  .ci-detail-attr-label {
    font-size: 13px;
    font-weight: 500;
    color: @text-color_3;
    display: flex;
    align-items: center;
    white-space: nowrap;

    &-text {
      overflow: hidden;
      text-overflow: ellipsis;
    }

    &-colon {
      flex-shrink: 0;
      margin-left: 2px;
    }
  }

  .ci-detail-attr-content {
    overflow-wrap: break-word;
    font-size: 13px;
    color: @text-color_1;
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 28px;

    > span {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
      min-width: 0;
    }

    .ant-form-item {
      margin-bottom: 0;
    }

    a[opacity] {
      flex-shrink: 0;
      display: flex;
      align-items: center;
      height: 32px;
    }

    &:hover a {
      opacity: 1 !important;
    }
  }

  .ci-detail-table {
    .ant-form-item {
      margin-bottom: 0;
    }
    .ant-form-item-control {
      line-height: 19px;
    }
  }
}

// CI变更记录页面样式
.ci-history-container {
  padding: 24px;
  height: 100%;
  background-color: #f5f7fa;
  overflow-y: auto;
}

// 统计信息卡片
.ci-history-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.ci-history-stat-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fb 100%);
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eaed;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  .stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;

    &.stat-icon-total {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
    }

    &.stat-icon-new {
      background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
      color: #fff;
    }

    &.stat-icon-update {
      background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
      color: #fff;
    }

    &.stat-icon-delete {
      background: linear-gradient(135deg, #f5222d 0%, #cf1322 100%);
      color: #fff;
    }
  }

  .stat-content {
    flex: 1;
  }

  .stat-label {
    font-size: 13px;
    color: @text-color_3;
    margin-bottom: 4px;
  }

  .stat-value {
    font-size: 22px;
    font-weight: 600;
    color: @text-color_1;
    line-height: 1;
  }
}

// 操作按钮组
.ci-history-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

// 变更记录表格
.ci-history-table {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;

  .ci-history-time {
    display: flex;
    align-items: center;
    gap: 8px;

    .time-icon {
      color: @primary-color;
      font-size: 14px;
    }
  }

  .ci-history-user {
    display: flex;
    align-items: center;
  }

  .ci-history-value {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 13px;
    min-height: 32px;
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap-mode: nowrap;

    &.ci-history-value-old {
      background-color: #f5f5f5;
      color: #8c8c8c;
      border: 1px solid #d9d9d9;
    }

    &.ci-history-value-new {
      background-color: #e6f7ff;
      color: @primary-color;
      border: 1px solid #91d5ff;
    }
  }
}
</style>
