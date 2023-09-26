<template>
  <CustomDrawer
    width="80%"
    placement="left"
    @close="
      () => {
        visible = false
      }
    "
    :visible="visible"
    :hasTitle="false"
    :hasFooter="false"
    :bodyStyle="{ padding: 0, height: '100vh' }"
    wrapClassName="ci-detail"
    destroyOnClose
  >
    <a-tabs v-model="activeTabKey" @change="changeTab">
      <a-tab-pane key="tab_1">
        <span slot="tab"><a-icon type="book" />属性</span>
        <div :style="{ maxHeight: `${windowHeight - 44}px`, overflow: 'auto', padding: '24px' }" class="ci-detail-attr">
          <el-descriptions
            :title="group.name || '其他'"
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
              <CiDetailAttrContent :ci="ci" :attr="attr" @refresh="refresh" />
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_2">
        <span slot="tab"><a-icon type="branches" />关系</span>
        <div :style="{ padding: '24px' }">
          <CiDetailRelation ref="ciDetailRelation" :ciId="ciId" :typeId="typeId" :ci="ci" />
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_3">
        <span slot="tab"><a-icon type="clock-circle" />操作历史</span>
        <div :style="{ padding: '24px', height: 'calc(100vh - 44px)' }">
          <vxe-table
            ref="xTable"
            :data="ciHistory"
            size="small"
            :max-height="`${windowHeight - 94}px`"
            :span-method="mergeRowMethod"
            border
            :scroll-y="{ enabled: false }"
            class="ops-stripe-table"
          >
            <vxe-table-column sortable field="created_at" title="时间"></vxe-table-column>
            <vxe-table-column
              field="username"
              title="用户"
              :filters="[]"
              :filter-method="filterUsernameMethod"
            ></vxe-table-column>
            <vxe-table-column
              field="operate_type"
              :filters="[
                { value: 0, label: '新增' },
                { value: 1, label: '删除' },
                { value: 3, label: '修改' },
              ]"
              :filter-method="filterOperateMethod"
              title="操作"
            >
              <template #default="{ row }">
                {{ operateTypeMap[row.operate_type] }}
              </template>
            </vxe-table-column>
            <vxe-table-column
              field="attr_alias"
              title="属性"
              :filters="[]"
              :filter-method="filterAttrMethod"
            ></vxe-table-column>
            <vxe-table-column field="old" title="旧"></vxe-table-column>
            <vxe-table-column field="new" title="新"></vxe-table-column>
          </vxe-table>
        </div>
      </a-tab-pane>
      <a-tab-pane key="tab_4">
        <span slot="tab"><ops-icon type="itsm_auto_trigger" />触发历史</span>
        <div :style="{ padding: '24px', height: 'calc(100vh - 44px)' }">
          <TriggerTable :ci_id="ci._id" />
        </div>
      </a-tab-pane>
    </a-tabs>
  </CustomDrawer>
</template>

<script>
import { Descriptions, DescriptionsItem } from 'element-ui'
import { getCITypeGroupById, getCITypes } from '@/modules/cmdb/api/CIType'
import { getCIHistory } from '@/modules/cmdb/api/history'
import { getCIById } from '@/modules/cmdb/api/ci'
import CiDetailAttrContent from './ciDetailAttrContent.vue'
import CiDetailRelation from './ciDetailRelation.vue'
import TriggerTable from '../../operation_history/modules/triggerTable.vue'

export default {
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
    const operateTypeMap = {
      0: '新增',
      1: '删除',
      2: '修改',
    }
    return {
      operateTypeMap,
      visible: false,
      ci: {},
      attributeGroups: [],
      activeTabKey: 'tab_1',
      rowSpanMap: {},
      ciHistory: [],
      ciId: null,
      ci_types: [],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  provide() {
    return {
      ci_types: () => {
        return this.ci_types
      },
    }
  },
  inject: ['reload', 'handleSearch', 'attrList'],
  methods: {
    create(ciId, activeTabKey = 'tab_1', ciDetailRelationKey = '1') {
      this.visible = true
      this.activeTabKey = activeTabKey
      if (activeTabKey === 'tab_2') {
        this.$nextTick(() => {
          this.$refs.ciDetailRelation.activeKey = ciDetailRelationKey
        })
      }
      this.ciId = ciId
      this.getAttributes()
      this.getCI()
      this.getCIHistory()
      getCITypes().then((res) => {
        this.ci_types = res.ci_types
      })
    },
    getAttributes() {
      getCITypeGroupById(this.typeId, { need_other: 1 })
        .then((res) => {
          this.attributeGroups = res
        })
        .catch((e) => {})
    },
    getCI() {
      getCIById(this.ciId)
        .then((res) => {
          // this.ci = res.ci
          this.ci = res.result[0]
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
          this.reload()
        } else {
          this.handleSearch()
        }
      }, 500)
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['created_at', 'username']
      const cellValue = row[column.property]
      if (cellValue && fields.includes(column.property)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow[column.property] === cellValue) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow[column.property] === cellValue) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },
  },
}
</script>

<style lang="less" scoped></style>
<style lang="less">
.ci-detail {
  .ant-tabs-bar {
    margin: 0;
  }
  .ci-detail-attr {
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
