<template>
  <div v-if="allCITypes.length" class="ci-relation-table">
    <CIDetailTableTitle :title="$t('cmdb.relation')" />

    <div class="ci-relation-table-wrap">
      <div class="ci-relation-table-tab">
        <div
          v-for="(item) in tabList"
          :key="item.value"
          :class="`tab-item ${item.value === currentTab ? 'tab-item-active' : ''}`"
          @click="clickTab(item.value)"
        >
          <span class="tab-item-name">
            <a-tooltip :title="item.name">
              <span class="tab-item-name-text">{{ item.name }}</span>
            </a-tooltip>
            <span
              v-if="item.count"
              class="tab-item-name-count"
            >
              ({{ item.count }})
            </span>
          </span>
          <span
            v-if="item.value === currentTab && item.showAdd"
            class="tab-item-add"
            @click="openAddModal(item)"
          >
            <a-icon type="plus" />
          </span>
        </div>
      </div>

      <div
        class="ci-relation-table-container"
        v-if="tableIDList.length"
      >
        <div
          v-for="(item) in tableIDList"
          :key="item.id"
          class="ci-relation-table-item"
        >
          <div
            v-if="currentTab === 'all'"
            class="ci-relation-table-item-name"
          >
            <span class="ci-relation-table-item-name-text">{{ item.name }}</span>
            <span class="ci-relation-table-item-name-count">({{ item.count }})</span>
          </div>

          <vxe-grid
            bordered
            size="mini"
            :columns="allColumns[item.id]"
            :data="allCIList[item.id]"
            overflow
            showOverflow="tooltip"
            showHeaderOverflow="tooltip"
            resizable
            class="ops-stripe-table"
            max-height="300px"
          >
            <template #reference_default="{ row, column }">
              <a
                v-for="(id) in (column.params.attr.is_list ? row[column.field] : [row[column.field]])"
                :key="id"
                :href="`/cmdb/cidetail/${column.params.attr.reference_type_id}/${id}`"
                target="_blank"
              >
                {{ getReferenceName(id, column) }}
              </a>
            </template>
            <template #operation_default="{ row }">
              <a-popconfirm
                arrowPointAtCenter
                :title="$t('cmdb.ci.confirmDeleteRelation')"
                @confirm="deleteRelation(row)"
              >
                <a
                  :disabled="!allCanEdit[item.id]"
                  :style="{
                    color: !allCanEdit[item.id] ? 'rgba(0, 0, 0, 0.25)' : 'red',
                  }"
                >
                  <a-icon type="delete" />
                </a>
              </a-popconfirm>
            </template>
          </vxe-grid>
        </div>
      </div>
    </div>

    <AddTableModal ref="addTableModal" @reload="refreshTableData" />
  </div>
</template>

<script>
import _ from 'lodash'
import { getCanEditByParentIdChildId } from '@/modules/cmdb/api/CITypeRelation'
import { deleteCIRelationView } from '@/modules/cmdb/api/CIRelation'
import { searchCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'

import CIDetailTableTitle from './ciDetailTableTitle.vue'
import AddTableModal from '@/modules/cmdb/views/relation_views/modules/AddTableModal.vue'

export default {
  name: 'CIRelationTable',
  components: {
    CIDetailTableTitle,
    AddTableModal
  },
  inject: {
    ci_types: { from: 'ci_types' },
    relationViewRefreshNumber: {
      from: 'relationViewRefreshNumber',
      default: () => null,
    },
  },
  props: {
    ciId: {
      type: Number,
      default: 0,
    },
    typeId: {
      type: Number,
      default: 0,
    },
    ci: {
      type: Object,
      default: () => {},
    },
    relationData: {
      type: Object,
      default: () => {}
    }
  },

  data() {
    return {
      tabList: [],
      currentTab: 'all',
      allCITypes: [],
      allColumns: {},
      allJSONAttr: {},
      allCIList: {},
      allCanEdit: {},
      referenceCINameMap: {}
    }
  },

  computed: {
    tableIDList() {
      let baseIDs = []

      switch (this.currentTab) {
        case 'all':
          baseIDs = this.tabList.filter((item) => item.value !== 'all').map((item) => item.value)
          break
        default:
          baseIDs = [this.currentTab]
          break
      }

      return baseIDs.filter((id) => this.allCIList?.[id]?.length).map((id) => {
        const findTab = this.tabList.find((item) => item.value === id) || {}

        return {
          id,
          name: findTab?.name || '',
          count: findTab?.count || ''
        }
      })
    }
  },

  watch: {
    relationData: {
      immediate: true,
      deep: true,
      handler(val) {
        this.init(val)
      }
    }
  },

  methods: {
    async init(relationData) {
      const ci_types_list = this.ci_types()
      const _findCiType = ci_types_list.find((item) => item.id === this.typeId)
      if (!_findCiType) {
        return
      }

      const cloneRelationData = _.cloneDeep(relationData)

      const allCITypes = _.uniqBy(
        [
          ...cloneRelationData.parentCITypeList,
          ...cloneRelationData.childCITypeList
        ],
        'id'
      )
      await this.handleSubscribeAttributes(allCITypes)

      const {
        columns: parentColumns,
        jsonAttr: parentJSONAttr,
      } = this.handleCITypeList(cloneRelationData.parentCITypeList, true)
      const {
        columns: childColumns,
        jsonAttr: childJSONAttr,
      } = this.handleCITypeList(cloneRelationData.childCITypeList, false)

      this.allCITypes = allCITypes
      this.allColumns = {
        ...parentColumns,
        ...childColumns
      }
      this.allJSONAttr = {
        ...parentJSONAttr,
        ...childJSONAttr
      }

      await this.getCanEditList(this.allCITypes)

      const [parentCIs, childCIs] = await Promise.all([
        this.handleCIList(cloneRelationData.parentCIList, true),
        this.handleCIList(cloneRelationData.childCIList, false)
      ])
      this.allCIList = {
        ...parentCIs,
        ...childCIs
      }

      const tabList = this.allCITypes.map((item) => {
        return {
          name: item?.alias ?? item?.name ?? '',
          value: item.id,
          count: this.allCIList?.[item.id]?.length || 0,
          showAdd: this.allCanEdit?.[item.id] ?? false
        }
      })
      tabList.unshift({
        name: this.$t('all'),
        value: 'all',
        count: Object.values(this.allCIList).reduce((acc, cur) => acc + (cur?.length || 0), 0),
        showAdd: false
      })
      this.tabList = tabList

      this.handleReferenceCINameMap()
    },

    handleCITypeList(list, isParent) {
      const CIColumns = {}
      const CIJSONAttr = {}

      list.forEach((item) => {
        const columns = []
        const jsonAttr = []

        item.isParent = isParent
        item.attributes.forEach((attr) => {
          const column = {
            key: 'p_' + attr.id,
            field: attr.name,
            title: attr.alias,
            minWidth: '100px',
            params: {
              attr
            },
          }
          if (attr.is_reference) {
            column.slots = {
              default: 'reference_default'
            }
          }
          columns.push(column)

          if (attr.value_type === '6') {
            jsonAttr.push(attr.name)
          }
        })
        CIJSONAttr[item.id] = jsonAttr
        CIColumns[item.id] = columns
        CIColumns[item.id].push({
          key: 'p_operation',
          field: 'operation',
          title: this.$t('operation'),
          width: '60px',
          fixed: 'right',
          slots: {
            default: 'operation_default',
          },
          align: 'center',
        })
      })

      return {
        columns: CIColumns,
        jsonAttr: CIJSONAttr
      }
    },

    async getCanEditList(allCITypes) {
      const promises = allCITypes.map((ciType) => {
        let parentId = ciType.id
        let childId = this.typeId

        if (!ciType.isParent) {
          parentId = this.typeId
          childId = ciType.id
        }

        return getCanEditByParentIdChildId(parentId, childId).then((res) => {
          return { id: ciType.id, canEdit: res.result }
        })
      })

      const allCanEdit = {}

      const res = await Promise.all(promises)
      if (res?.length) {
        res.map((item) => {
          allCanEdit[item.id] = item.canEdit
        })
      }

      this.allCanEdit = allCanEdit
    },

    async handleSubscribeAttributes(allCITypes) {
      const promises = allCITypes.map((ciType, index) => {
        return getSubscribeAttributes(ciType.id).then((res) => {
          return {
            ...(res || {}),
            id: ciType.id,
            indexInAll: index
          }
        })
      })
      const res = await Promise.all(promises)

      if (res?.length) {
        res.forEach((item) => {
          if (
            allCITypes?.[item.indexInAll]?.attributes &&
            item?.is_subscribed
          ) {
            allCITypes[item.indexInAll].attributes = item.attributes
          }
        })
      }

      return allCITypes
    },

    async handleCIList(ciList, isParent) {
      const cis = {}
      ciList.forEach((item) => {
        this.allJSONAttr[item._type].forEach((attr) => {
          item[`${attr}`] = item[`${attr}`] ? JSON.stringify(item[`${attr}`]) : ''
        })
        this.formatCI(item)
        item.isParent = isParent

        if (item._type in cis) {
          cis[item._type].push(item)
        } else {
          cis[item._type] = [item]
        }
      })

      return cis
    },

    formatCI(ci) {
      Object.keys(ci).forEach((key) => {
        const attr = this.allColumns?.[ci?._type]?.find((item) => item?.params?.attr?.name === key)?.params?.attr
        if (attr?.is_choice && attr?.choice_value?.length) {
          if (attr?.is_list) {
            ci[key] = ci[key].map((value) => {
              const label = attr?.choice_value?.find((choice) => choice?.[0] === value)?.[1]?.label
              return label || ci[key]
            })
          } else {
            const label = attr?.choice_value?.find((choice) => choice?.[0] === ci[key])?.[1]?.label
            ci[key] = label || ci[key]
          }
        }
      })

      return ci
    },

    async handleReferenceCINameMap() {
      const referenceCINameMap = {}
      this.allCITypes.forEach((CIType) => {
        CIType.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            const currentCIList = this.allCIList[CIType.id]
            if (currentCIList?.length) {
              currentCIList.forEach((ci) => {
                const ids = Array.isArray(ci[attr.name]) ? ci[attr.name] : ci[attr.name] ? [ci[attr.name]] : []

                if (ids.length) {
                  if (!referenceCINameMap?.[attr.reference_type_id]) {
                    referenceCINameMap[attr.reference_type_id] = {}
                  }
                  ids.forEach((id) => {
                    referenceCINameMap[attr.reference_type_id][id] = ''
                  })
                }
              })
            }
          }
        })
      })

      if (!Object.keys(referenceCINameMap).length) {
        return
      }

      const allRes = await Promise.all(
        Object.keys(referenceCINameMap).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(referenceCINameMap[key]).join(';')})`,
            count: 9999
          })
        })
      )
      const CITypeList = this.ci_types()
      const showNameMap = {}

      Object.keys(referenceCINameMap).forEach((id) => {
        const CIType = CITypeList.find((CIType) => Number(CIType.id) === Number(id))

        showNameMap[id] = {
          show_name: CIType?.show_name,
          unique_key: CIType?.unique_key
        }
      })

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (referenceCINameMap?.[item._type]?.[item._id] === '') {
            const showName = showNameMap?.[item._type]

            referenceCINameMap[item._type][item._id] = item?.[showName?.show_name] ?? item?.[showName?.unique_key] ?? ''
          }
        })
      })

      this.referenceCINameMap = referenceCINameMap
    },

    getReferenceName(id, column) {
      const typeId = column?.params?.attr?.reference_type_id
      return this.referenceCINameMap?.[typeId]?.[id] || id
    },

    clickTab(value) {
      this.currentTab = value
    },

    deleteRelation(row) {
      const first_ci_id = row?.isParent ? row?._id : this.ciId
      const second_ci_id = row?.isParent ? this.ciId : row?._id

      deleteCIRelationView(first_ci_id, second_ci_id).then(() => {
        this.refreshTableData()
        if (this.relationViewRefreshNumber) {
          this.relationViewRefreshNumber()
        }
      })
    },

    openAddModal(tabData) {
      const ciType = this.allCITypes.find((item) => item.id === tabData.value)

      this.$refs.addTableModal.openModal(
        {
          [`${this.ci.unique}`]: this.ci?.[this.ci.unique]
        },
        this.ciId,
        ciType,
        ciType?.isParent ? 'parents' : 'children'
      )
    },

    async refreshTableData() {
      this.$emit('refreshRelationCI')
    }
  }
}
</script>

<style lang="less" scoped>
.ci-relation-table {
  width: 100%;
  margin-top: 32px;

  &-wrap {
    border: solid 1px #E4E7ED;
    border-top: none;
    display: flex;
    width: 100%;
  }

  &-tab {
    flex-shrink: 0;
    width: 160px;
    max-height: 300px;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 6px 0px;
    border-right: solid 1px #E4E7ED;

    .tab-item {
      height: 32px;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-left: 16px;
      padding-right: 10px;
      background-color: #FFFFFF;
      cursor: pointer;

      &-name {
        font-size: 14px;
        color: @text-color_1;
        display: flex;
        align-items: baseline;
        max-width: calc(100% - 16px);

        &-text {
          text-overflow: ellipsis;
          text-wrap: nowrap;
          overflow: hidden;
          color: @text-color_2;
        }

        &-count {
          color: @text-color_3;
          font-size: 12px;
        }
      }

      &-add {
        width: 14px;
        height: 14px;
        border-radius: 14px;
        background-color: #FFFFFF;
        display: none;
        align-items: center;
        justify-content: center;
        color: @primary-color;
        font-size: 12px;
      }

      &-active {
        background-color: #F0F5FF;

        .tab-item-name-text {
          color: @text-color_1;
        }
      }

      &:hover {
        .tab-item-name-text {
          color: @text-color_1;
        }

        .tab-item-add {
          display: flex;
        }
      }
    }
  }

  &-container {
    width: 100%;
    padding: 15px 17px;
    overflow: hidden;
    min-height: 300px;
  }

  &-item {
    margin-bottom: 16px;

    &-name {
      margin-bottom: 12px;
      font-size: 14px;
      font-weight: 700;
      color: @text-color_1;

      display: flex;
      align-items: baseline;

      &-count {
        font-size: 12px;
        color: @text-color_3;
      }
    }
  }
}
</style>
