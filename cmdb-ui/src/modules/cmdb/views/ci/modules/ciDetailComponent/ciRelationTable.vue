<template>
  <div v-if="allCITypes.length" class="ci-relation-table">
    <CIDetailTableTitle :title="$t('cmdb.relation')" />

    <div class="ci-relation-table-wrap">
      <div class="ci-relation-table-tab">
        <div
          v-for="(group) in tabList"
          :key="group.key"
          class="tab-group"
        >
          <div
            v-if="group.name"
            class="tab-group-name"
          >
            {{ group.name }}
          </div>
          <div
            v-for="(item) in group.list"
            :key="item.key"
            :class="`tab-item ${item.key === currentTab ? 'tab-item-active' : ''}`"
            :style="{
              paddingLeft: item.key === 'all' ? '8px' : '16px'
            }"
            @click="clickTab(item.key)"
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
              v-if="item.key === currentTab && item.showAdd"
              class="tab-item-add"
              @click="openAddModal(item)"
            >
              <a-icon type="plus" />
            </span>
          </div>
        </div>
      </div>

      <div
        class="ci-relation-table-container"
        v-if="tableIDList.length"
      >
        <div
          v-for="(item) in tableIDList"
          :key="item.key"
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
            :columns="allColumns[item.value]"
            :data="allCIList[item.key]"
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
                  :disabled="!allCanEdit[item.value]"
                  :style="{
                    color: !allCanEdit[item.value] ? 'rgba(0, 0, 0, 0.25)' : 'red',
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

const PARENT_KEY = 'parents'
const CHILDREN_KEY = 'children'

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
    tabListFlat() {
      return this.tabList.reduce((list, group) => list.concat(group.list), [])
    },
    tableIDList() {
      const baseKeys = this.currentTab === 'all'
        ? this.tabListFlat.filter(item => item.value !== 'all').map(item => item.key)
        : [this.currentTab]

      return baseKeys.filter((key) => this.allCIList?.[key]?.length).map((key) => {
        const findTab = this.tabListFlat.find((item) => item.key === key) || {}

        let name = findTab?.name || ''
        if (name && findTab?.value === this.ci._type) {
          name = `${findTab?.isParent ? this.$t('cmdb.ci.upstream') : this.$t('cmdb.ci.downstream')} - ${name}`
        }

        return {
          key,
          value: findTab?.value || '',
          name,
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

      const tabList = []

      tabList[0] = {
        name: '',
        key: 'all',
        list: [{
          name: this.$t('all'),
          key: 'all',
          value: 'all',
          count: Object.values(this.allCIList).reduce((acc, cur) => acc + (cur?.length || 0), 0),
          showAdd: false
        }]
      }
      tabList[1] = {
        name: this.$t('cmdb.ci.upstream'),
        key: PARENT_KEY,
        list: this.buildTabList(cloneRelationData.parentCITypeList, PARENT_KEY, true)
      }
      tabList[2] = {
        name: this.$t('cmdb.ci.downstream'),
        key: CHILDREN_KEY,
        list: this.buildTabList(cloneRelationData.childCITypeList, CHILDREN_KEY, false)
      }
      this.tabList = tabList

      this.handleReferenceCINameMap()
    },

    buildTabList(list, keyPrefix, isParent) {
      return list.map((item) => {
        const key = `${keyPrefix}-${item.id}`
        return {
          name: item?.alias ?? item?.name ?? '',
          key,
          isParent,
          value: item.id,
          count: this.allCIList?.[key]?.length || 0,
          showAdd: this.allCanEdit?.[item.id] ?? false
        }
      })
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
        const CIKey = `${isParent ? PARENT_KEY : CHILDREN_KEY}-${item._type}`

        if (CIKey in cis) {
          cis[CIKey].push(item)
        } else {
          cis[CIKey] = [item]
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
        const CIKey = `${CIType.isParent ? PARENT_KEY : CHILDREN_KEY}-${CIType.id}`

        CIType.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            const currentCIList = this.allCIList[CIKey]
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

    clickTab(key) {
      this.currentTab = key
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
        tabData?.isParent ? 'parents' : 'children'
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
  margin-top: 16px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  overflow: hidden;

  &-wrap {
    border: none;
    display: flex;
    width: 100%;
  }

  &-tab {
    flex-shrink: 0;
    width: 180px;
    min-height: 300px;
    max-height: 600px;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 8px 0px;
    border-right: solid 1px #e8eaed;
    background: #f8f9fb;

    .tab-group {
      width: 100%;

      &-name {
        padding-left: 12px;
        height: 32px;
        line-height: 32px;
        width: 100%;
        font-weight: 600;
        font-size: 12px;
        color: @text-color_3;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
    }

    .tab-item {
      height: 36px;
      width: calc(100% - 16px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-left: 16px;
      padding-right: 10px;
      margin: 2px 8px;
      border-radius: 4px;
      background-color: transparent;
      cursor: pointer;
      transition: all 0.2s ease;
      column-gap: 6px;

      &-name {
        font-size: 13px;
        color: @text-color_1;
        display: flex;
        align-items: baseline;
        max-width: calc(100% - 28px);

        &-text {
          text-overflow: ellipsis;
          text-wrap: nowrap;
          overflow: hidden;
          color: @text-color_2;
        }

        &-count {
          color: @text-color_3;
          font-size: 12px;
          margin-left: 4px;
        }
      }

      &-add {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        background-color: @primary-color;
        display: none;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 12px;
        flex-shrink: 0;
      }

      &-active {
        background-color: @primary-color_6;
        border-left: 3px solid @primary-color;
        padding-left: 13px;

        .tab-item-name-text {
          color: @text-color_1;
          font-weight: 500;
        }
      }

      &:hover {
        background-color: @primary-color_7;

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
    padding: 20px;
    min-height: 300px;
    background: #ffffff;
    min-height: 300px;
    max-height: 600px;
    overflow-y: auto;
    overflow-x: hidden;
  }

  &-item {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }

    &-name {
      margin-bottom: 12px;
      font-size: 14px;
      font-weight: 600;
      color: @text-color_1;
      display: flex;
      align-items: baseline;
      padding-left: 12px;
      position: relative;

      &::before {
        content: "";
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 14px;
        background: @primary-color;
        border-radius: 2px;
      }

      &-text {
        flex: 1;
      }

      &-count {
        font-size: 12px;
        color: @text-color_3;
        margin-left: 6px;
      }
    }
  }
}
</style>
