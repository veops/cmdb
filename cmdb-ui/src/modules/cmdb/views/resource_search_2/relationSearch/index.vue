<template>
  <div
    ref="relationSearchRef"
    class="relation-search"
    :style="{ height: `${windowHeight - 131}px` }"
  >
    <div class="relation-search-wrap">
      <div
        v-if="!isSearch"
        class="relation-search-title"
      >
        <ops-icon class="relation-search-title-icon" type="veops-relationship2" />
        <div class="relation-search-title-text">{{ $t('cmdb.relationSearch.relationSearch') }}</div>
      </div>

      <div
        v-if="isHideSearchCondition"
        class="relation-search-expand"
      >
        <div class="relation-search-expand-line"></div>

        <div class="relation-search-expand-right">
          <div
            class="relation-search-expand-handle"
            @click="isHideSearchCondition = false"
          >
            <a-icon
              type="down"
              class="relation-search-expand-icon"
            />
          </div>
          <div
            class="relation-search-expand-text"
            @click="isHideSearchCondition = false"
          >
            {{ $t('cmdb.relationSearch.expandCondition') }}
          </div>
        </div>
      </div>

      <SearchCondition
        v-else
        :CITypeGroup="CITypeGroup"
        :sourceCIType="sourceCIType"
        :sourceCITypeSearchValue="sourceCITypeSearchValue"
        :sourceAllAttributesList="sourceAllAttributesList"
        :sourceExpression="sourceExpression"
        :targetCITypes="targetCITypes"
        :targetCITypeGroup="targetCITypeGroup"
        :targetAllAttributesList="targetAllAttributesList"
        :targetExpression="targetExpression"
        :returnPath="returnPath"
        :allPath="allPath"
        :selectedPath="selectedPath"
        :isSearch="isSearch"
        :isSearchLoading="isSearchLoading"
        @changeData="changeData"
        @search="handleSearch"
        @hideSearchCondition="isHideSearchCondition = true"
        @clickFavor="clickFavor"
      />

      <div
        v-if="isSearch"
        class="relation-search-main"
      >
        <CITable
          :allTableData="allTableData"
          :tabActive="tableTabActive"
          :returnPath="returnPath"
          :isHideSearchCondition="isHideSearchCondition"
          :referenceShowAttrNameMap="referenceShowAttrNameMap"
          :referenceCIIdMap="referenceCIIdMap"
          :searchValue="sourceCITypeSearchValue"
          :isSearchLoading="isSearchLoading"
          @updateTab="(tab) => tableTabActive = tab"
        />

        <div class="relation-search-pagination">
          <a-pagination
            :showSizeChanger="true"
            :current="page"
            size="small"
            :total="totalNumber"
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
      </div>
    </div>

    <img
      v-if="!isSearch"
      class="relation-search-bg"
      :src="require('@/modules/cmdb/assets/resourceSearch/resource_search_bg_1.png')"
    />
  </div>
</template>

<script>
import _ from 'lodash'

import { getCITypeAttributesByTypeIds } from '@/modules/cmdb/api/CITypeAttr'
import { getRecursive_level2children, getCITypeRelationPath } from '@/modules/cmdb/api/CITypeRelation'
import { searchCIRelationPath } from '@/modules/cmdb/api/CIRelation'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { searchCI } from '@/modules/cmdb/api/ci'
import { strLength } from '@/modules/cmdb/utils/helper.js'

import SearchCondition from './components/searchCondition.vue'
import CITable from './components/ciTable.vue'

export default {
  name: 'RelationSearch',
  components: {
    SearchCondition,
    CITable
  },
  props: {
    CITypeGroup: {
      type: Array,
      default: () => []
    },
    allCITypes: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isSearch: false, // 是否搜索
      isHideSearchCondition: false, // 是否隐藏搜索条件
      isWatchData: true, // 是否监听数据变化
      isSearchLoading: false, // 搜索中

      sourceCIType: undefined, // 已选源模型
      sourceCITypeSearchValue: '', // 源模型搜索关键词
      sourceAllAttributesList: [], // 源模型所有属性
      sourceExpression: '', // 源模型表达式

      targetCITypes: [], // 目标模型
      targetCITypeGroup: {}, // 目标模型分组
      targetAllAttributesList: [], // 目标模型所有属性
      targetExpression: '', // 目标模型表达式

      returnPath: true, // 表格是否展示路径详情
      allPath: [], // 所有路径选项
      selectedPath: [], // 已选择路径

      // table
      page: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200'],
      allTableData: {}, // 表格数据
      totalNumber: 0, // 数据总数
      tableTabActive: '', // 当前 table tab
      referenceShowAttrNameMap: {},
      referenceCIIdMap: {},
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    watchParams() {
      return {
        sourceCIType: this.sourceCIType,
        targetCITypes: this.targetCITypes
      }
    },
  },
  watch: {
    sourceCIType: {
      immediate: true,
      deep: true,
      handler(id) {
        if (this.isWatchData) {
          this.sourceExpression = ''

          this.targetCITypes = []
          this.targetAllAttributesList = []
          this.targetExpression = ''

          this.selectedPath = []

          this.getTargetCITypeGroup(id)
          this.updateSourceAllAttributesList(id)
        }
      }
    },
    targetCITypes: {
      immediate: true,
      deep: true,
      handler(ids) {
        if (this.isWatchData) {
          this.selectedPath = []
          this.targetExpression = ''
          this.updateTargetAllAttributesList(ids)
        }
      }
    },
    watchParams: {
      immediate: true,
      deep: true,
      handler(data) {
        if (this.isWatchData) {
          this.updateAllPath(data)
        }
      }
    }
  },
  methods: {
    changeData(data) {
      this[data.name] = data.value
    },

    async updateSourceAllAttributesList(id) {
      if (id) {
        const res = await getCITypeAttributesByTypeIds({ type_ids: id })
        this.sourceAllAttributesList = res.attributes
      } else {
        this.sourceAllAttributesList = []
      }
    },

    async getTargetCITypeGroup(id) {
      let targetCITypeGroup = {}
      if (id) {
        const res = await getRecursive_level2children(id)
        targetCITypeGroup = res
      }
      this.targetCITypeGroup = targetCITypeGroup
    },

    async updateTargetAllAttributesList(ids) {
      if (ids?.length) {
        const res = await getCITypeAttributesByTypeIds({ type_ids: ids.join(',') })
        this.targetAllAttributesList = res.attributes
      } else {
        this.targetAllAttributesList = []
      }
    },

    async updateAllPath(data) {
      let allPath = []
      if (
        data.sourceCIType &&
        data?.targetCITypes?.length
      ) {
        const params = {
          source_type_id: data.sourceCIType,
          target_type_ids: data.targetCITypes.join(',')
        }

        const res = await getCITypeRelationPath(params)

        if (res?.paths?.length) {
          const sourceCIType = this.allCITypes.find((ciType) => ciType.id === data.sourceCIType)
          const sourceCITypeName = sourceCIType?.alias || sourceCIType?.name || ''
          const targetCITypeList = Object.values(this.targetCITypeGroup).reduce((acc, cur) => acc.concat(cur), [])

          allPath = res.paths.map((ids) => {
            const [sourceId, ...targetIds] = ids
            const pathNames = [sourceCITypeName]

            targetIds.forEach((id) => {
              const ciType = targetCITypeList.find((item) => item.id === id)
              if (ciType) {
                pathNames.push(ciType.alias || ciType.name)
              }
            })

            return {
              value: ids.join(','),
              sourceId,
              targetIds,
              pathNames: pathNames.join('-'),
            }
          })
        }
      }

      this.allPath = allPath
    },

    async loadCI() {
      this.isSearchLoading = true

      const path = this.selectedPath.map((item) => {
        return item?.split(',')?.map((id) => Number(id)) || []
      })

      const params = {
        page: this.page,
        page_size: this.pageSize,
        source: {
          type_id: this.sourceCIType
        },
        target: {
          type_ids: this.targetCITypes
        },
        path
      }

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const sourceExp = this.sourceExpression.match(regQ) ? this.sourceExpression.match(regQ)[0] : null
      const targetExp = this.targetExpression.match(regQ) ? this.targetExpression.match(regQ)[0] : null
      const sourceSearch = `${sourceExp ? `${sourceExp}` : ''}${this.sourceCITypeSearchValue ? `,*${this.sourceCITypeSearchValue}*` : ''}`

      if (sourceSearch) {
        params.source.q = sourceSearch
      }
      if (targetExp) {
        params.target.q = targetExp
      }

      let res = {}
      const tableData = {}
      const typeId2Attr = {}
      let pathKeyList = []

      try {
        res = await searchCIRelationPath(params)

        pathKeyList = Object.keys(res.paths)
        const filterAllPath = this.allPath.filter((path) => pathKeyList.includes(path.pathNames))
        const typeIds = _.uniq(
          filterAllPath.map((item) => item?.targetIds?.[item?.targetIds?.length - 1])
        )

        const promises = typeIds.map((id) => {
          return getSubscribeAttributes(id)
        })
        const subscribedRes = await Promise.all(promises)
        typeIds.forEach((id, index) => {
          const attrList = subscribedRes?.[index]?.attributes || []
          typeId2Attr[id] = attrList
        })
      } catch (error) {
        this.isSearchLoading = false
        this.allTableData = {}
        this.totalNumber = 0
        this.tableTabActive = ''
        return
      }

      pathKeyList.forEach((key) => {
        const pathObj = this.allPath.find((path) => path.pathNames === key)

        const pathIdList = pathObj?.value?.split(',') || []
        const pathNameList = key?.split('-') || []

        const pathList = pathNameList.map((name, index) => {
          let relation = ''
          if (index < pathNameList.length - 1) {
            const targetName = pathNameList[index + 1]
            const sourceRelation = res?.relation_types?.[name]

            if (sourceRelation) {
              if (Object.keys(sourceRelation)?.includes?.(targetName)) {
                relation = sourceRelation?.[targetName] || ''
              }
            }
          }

          return {
            id: pathIdList?.[index] || '',
            name,
            relation
          }
        })

        tableData[key] = {
          key,
          count: res.paths?.[key]?.length || 0,
          pathList,
          ciAttr: [],
          ciList: []
        }

        if (pathObj) {
          const firstIds = res?.paths?.[key]?.[0]
          const targetId = firstIds[firstIds.length - 1]
          const ciTypeId = (res?.id2ci?.[targetId] || {})?._type
          if (ciTypeId) {
            tableData[key].ciAttr = typeId2Attr[ciTypeId]
          }

          tableData[key].ciList = res.paths[key].map((ids) => {
            const pathCI = {}
            ids.map((id) => {
              const ci = res?.id2ci?.[id] || {}
              const showAttr = res?.type2show_key?.[ci._type] || ''
              pathCI[ci._type] = ci?.[showAttr] ?? ''
            })

            const targetId = ids[ids.length - 1]
            const targetCI = res?.id2ci?.[targetId] || {}

            return {
              pathCI,
              targetCI
            }
          })

          let totalWidth = 0
          tableData[key].ciAttr.forEach((attr) => {
            const lengthList = tableData[key].ciList.map(({ targetCI }) => {
              return strLength(targetCI[attr.name])
            })

            attr.width = Math.round(Math.min(Math.max(100, ...lengthList), 350))
            totalWidth += attr.width
          })

          // ci 表格宽度 = 容器宽度 - path 列宽 - checkbox 宽度
          const wrapWidth = this.$refs?.relationSearchRef?.clientWidth - (tableData?.[key]?.pathList.length || 0) * 160 - 60

          if (wrapWidth && totalWidth < wrapWidth) {
            tableData[key].ciAttr.forEach((attr) => {
              delete attr.width
            })
          }
        }
      })

      this.$set(this, 'allTableData', tableData)
      this.allTableData = tableData
      this.totalNumber = res?.numfound ?? 0
      this.tableTabActive = Object.keys(tableData)?.[0] || ''
      this.isSearch = true
      this.isSearchLoading = false

      const allAttr = []
      Object.values(typeId2Attr).map((attrList) => {
        allAttr.push(...attrList)
      })
      this.handlePerference(_.uniqBy(allAttr, 'id'))
    },

    handlePerference(allAttr) {
      let needRequiredCIType = []
      allAttr.forEach((attr) => {
        if (attr?.is_reference && attr?.reference_type_id) {
          needRequiredCIType.push(attr)
        }
      })
      needRequiredCIType = _.uniq(needRequiredCIType, 'id')

      if (!needRequiredCIType.length) {
        this.referenceShowAttrNameMap = {}
        this.referenceCIIdMap = {}
        return
      }

      this.handleReferenceShowAttrName(needRequiredCIType)
      this.handleReferenceCIIdMap(needRequiredCIType)
    },

    async handleReferenceShowAttrName(needRequiredCIType) {
      const res = await getCITypes({
        type_ids: needRequiredCIType.map((col) => col.reference_type_id).join(',')
      })

      const map = {}
      res.ci_types.forEach((ciType) => {
        map[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      this.referenceShowAttrNameMap = map
    },

    async handleReferenceCIIdMap(needRequiredCIType) {
      const map = {}

      Object.values(this.allTableData).forEach((item) => {
        const ciList = item?.ciList || []
        ciList.forEach(({ targetCI }) => {
          needRequiredCIType.forEach((col) => {
            const ids = Array.isArray(targetCI[col.name]) ? targetCI[col.name] : targetCI[col.name] ? [targetCI[col.name]] : []
            if (ids.length) {
              if (!map?.[col.reference_type_id]) {
                map[col.reference_type_id] = {}
              }
              ids.forEach((id) => {
                map[col.reference_type_id][id] = {}
              })
            }
          })
        })
      })

      if (!Object.keys(map).length) {
        this.referenceCIIdMap = {}
        return
      }

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (map?.[item._type]?.[item._id]) {
            map[item._type][item._id] = item
          }
        })
      })

      this.referenceCIIdMap = map
    },

    handlePageSizeChange(_, pageSize) {
      this.pageSize = pageSize
      this.page = 1
      this.loadCI()
    },

    changePage(page) {
      this.page = page
      this.loadCI()
    },

    handleSearch() {
      this.page = 1
      this.loadCI()
    },

    clickFavor(option) {
      this.isWatchData = false

      this.$nextTick(async () => {
        this.sourceCIType = option?.sourceCIType || undefined
        this.sourceCITypeSearchValue = option?.searchValue || ''
        this.sourceExpression = option?.sourceExpression || ''
        this.targetCITypes = option?.targetCITypes || []
        this.targetExpression = option?.targetExpression || ''
        this.selectedPath = option?.selectedPath || []

        await Promise.all([
          this.getTargetCITypeGroup(this.sourceCIType),
          this.updateSourceAllAttributesList(this.sourceCIType),
          this.updateTargetAllAttributesList(this.targetCITypes)
        ])
        await this.updateAllPath({
          sourceCIType: this.sourceCIType,
          targetCITypes: this.targetCITypes
        })

        this.isWatchData = true
        this.page = 1

        this.loadCI()
      })
    }
  }
}
</script>

<style lang="less" scoped>
.relation-search {
  width: 100%;
  height: 100%;
  position: relative;

  &-wrap {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 1;
  }

  &-title {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 30px;
    margin-top: 100px;

    &-icon {
      font-size: 28px;
      margin-right: 10px;
    }

    &-text {
      font-size: 20px;
      font-weight: 700;
      color: #1D2129;
    }
  }

  &-expand {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;

    &-line {
      width: 650px;
      height: 1px;
      background-color: #E4E7ED;
    }

    &-icon {
      font-size: 12px;
      color: #86909C;
    }

    &-text {
      margin-left: 5px;
      font-size: 12px;
      font-weight: 400;
      color: #A5A9BC;
    }

    &-handle {
      width: 14px;
      height: 14px;
      background-color: #EBEFF8;
      border-radius: 1px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    &-right {
      flex-shrink: 0;
      display: flex;
      align-items: center;
      cursor: pointer;

      &:hover {
        .relation-search-expand-handle {
          background-color: @primary-color_4;
        }

        .relation-search-expand-icon {
          color: @primary-color;
        }

        .relation-search-expand-text {
          color: @primary-color;
        }
      }
    }
  }

  &-bg {
    position: absolute;
    left: -24px;
    bottom: -24px;
    width: calc(100% + 48px);
    z-index: 0;
  }

  &-main {
    width: calc(100% + 48px);
    // height: 100%;
    background-color: #FFFFFF;
    padding: 24px;
  }

  &-pagination {
    text-align: right;
    margin-top: 12px;
  }
}
</style>
