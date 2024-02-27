<template>
  <div :style="{ height: '100%' }">
    <a-tabs v-if="hasPermission" class="ci-detail-tab" v-model="activeTabKey" @change="changeTab">
      <a @click="shareCi" slot="tabBarExtraContent" :style="{ marginRight: '24px' }">
        <a-icon type="share-alt" />
        {{ $t('cmdb.ci.share') }}
      </a>
      <a-tab-pane key="tab_1">
        <span slot="tab"><a-icon type="book" />{{ $t('cmdb.attribute') }}</span>
        <div class="ci-detail-attr">
          <el-descriptions
            :title="group.name || $t('other')"
            :key="group.name"
            v-for="group in attributeGroups"
            border
            :column="3"
          >
            <el-descriptions-item
              :label="`${attr.alias || attr.name}`"
              :key="attr.name"
              v-for="attr in group.attributes"
            >
              <CiDetailAttrContent :ci="ci" :attr="attr" @refresh="refresh" @updateCIByself="updateCIByself" />
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_2">
        <span slot="tab"><a-icon type="branches" />{{ $t('cmdb.relation') }}</span>
        <div :style="{ height: '100%', padding: '24px' }">
          <CiDetailRelation ref="ciDetailRelation" :ciId="ciId" :typeId="typeId" :ci="ci" />
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_3">
        <span slot="tab"><a-icon type="clock-circle" />{{ $t('cmdb.ci.history') }}</span>
        <div :style="{ padding: '24px', height: '100%' }">
          <vxe-table
            ref="xTable"
            :data="ciHistory"
            size="small"
            height="auto"
            :span-method="mergeRowMethod"
            border
            :scroll-y="{ enabled: false }"
            class="ops-stripe-table"
          >
            <vxe-table-column sortable field="created_at" :title="$t('created_at')"></vxe-table-column>
            <vxe-table-column
              field="username"
              :title="$t('user')"
              :filters="[]"
              :filter-method="filterUsernameMethod"
            ></vxe-table-column>
            <vxe-table-column
              field="operate_type"
              :filters="[
                { value: 0, label: $t('new') },
                { value: 1, label: $t('delete') },
                { value: 3, label: $t('update') },
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
              :title="$t('cmdb.attribute')"
              :filters="[]"
              :filter-method="filterAttrMethod"
            ></vxe-table-column>
            <vxe-table-column field="old" :title="$t('cmdb.history.old')"></vxe-table-column>
            <vxe-table-column field="new" :title="$t('cmdb.history.new')"></vxe-table-column>
          </vxe-table>
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_4">
        <span slot="tab"><ops-icon type="itsm_auto_trigger" />{{ $t('cmdb.history.triggerHistory') }}</span>
        <div :style="{ padding: '24px', height: '100%' }">
          <TriggerTable :ci_id="ci._id" />
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
import { Descriptions, DescriptionsItem } from 'element-ui'
import { getCITypeGroupById, getCITypes } from '@/modules/cmdb/api/CIType'
import { getCIHistory } from '@/modules/cmdb/api/history'
import { getCIById } from '@/modules/cmdb/api/ci'
import CiDetailAttrContent from './ciDetailAttrContent.vue'
import CiDetailRelation from './ciDetailRelation.vue'
import TriggerTable from '../../operation_history/modules/triggerTable.vue'
export default {
  name: 'CiDetailTab',
  components: {
    ElDescriptions: Descriptions,
    ElDescriptionsItem: DescriptionsItem,
    CiDetailAttrContent,
    CiDetailRelation,
    TriggerTable,
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
  },
  data() {
    return {
      ci: {},
      attributeGroups: [],
      activeTabKey: 'tab_1',
      rowSpanMap: {},
      ciHistory: [],
      ciId: null,
      ci_types: [],
      hasPermission: true,
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
    async create(ciId, activeTabKey = 'tab_1', ciDetailRelationKey = '1') {
      this.activeTabKey = activeTabKey
      if (activeTabKey === 'tab_2') {
        this.$nextTick(() => {
          this.$refs.ciDetailRelation.activeKey = ciDetailRelationKey
        })
      }
      this.ciId = ciId
      await this.getCI()
      if (this.hasPermission) {
        this.getAttributes()
        this.getCIHistory()
        getCITypes().then((res) => {
          this.ci_types = res.ci_types
        })
      }
    },
    getAttributes() {
      getCITypeGroupById(this.typeId, { need_other: 1 })
        .then((res) => {
          this.attributeGroups = res
        })
        .catch((e) => {})
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
        .catch((e) => {})
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
  .ci-detail-attr {
    height: 100%;
    overflow: auto;
    padding: 24px;
    .el-descriptions-item__content {
      cursor: default;
      &:hover a {
        opacity: 1 !important;
      }
    }
    .el-descriptions:first-child > .el-descriptions__header {
      margin-top: 0;
    }
    .el-descriptions__header {
      margin-bottom: 5px;
      margin-top: 20px;
    }
    .ant-form-item {
      margin-bottom: 0;
    }
    .ant-form-item-control {
      line-height: 19px;
    }
  }
}
</style>
