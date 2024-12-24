<template>
  <div
    class="resource-search"
    :style="{ height: `${windowHeight - 131}px` }"
  >
    <div v-if="!isSearch" class="resource-search-before">
      <div class="resource-search-title">
        <ops-icon class="resource-search-title-icon" type="veops-resource11" />
        <span class="resource-search-title-text">{{ $t('cmdb.ciType.resourceSearch') }}</span>
      </div>
      <SearchInput
        ref="searchInputRef"
        :CITypeGroup="CITypeGroup"
        :allAttributesList="allAttributesList"
        :searchValue="searchValue"
        :selectCITypeIds="selectCITypeIds"
        :expression="expression"
        :searchMode="currentSearchMode"
        @changeFilter="changeFilter"
        @updateAllAttributesList="updateAllAttributesList"
        @saveCondition="saveCondition"
        @updateSearchMode="updateSearchMode"
      />
      <HistoryList
        :recentList="recentList"
        :favorList="favorList"
        :detailCIId="detailCIId"
        @clickRecent="clickRecent"
        @deleteRecent="deleteRecent"
        @clearRecent="clearRecent"
        @deleteCollect="deleteCollect"
        @showDetail="clickFavor"
      />

      <img class="resource-search-before-bg" :src="require('@/modules/cmdb/assets/resourceSearch/resource_search_bg_1.png')" />
    </div>

    <div class="resource-search-after" v-else>
      <div
        class="resource-search-after-left"
        :style="{ width: showInstanceDetail ? '70%' : '100%' }"
      >
        <SearchInput
          ref="searchInputRef"
          classType="after"
          :CITypeGroup="CITypeGroup"
          :allAttributesList="allAttributesList"
          :searchValue="searchValue"
          :selectCITypeIds="selectCITypeIds"
          :expression="expression"
          :searchMode="currentSearchMode"
          @changeFilter="changeFilter"
          @updateAllAttributesList="updateAllAttributesList"
          @saveCondition="saveCondition"
          @updateSearchMode="updateSearchMode"
        />
        <HistoryList
          :recentList="recentList"
          :favorList="favorList"
          :detailCIId="detailCIId"
          @clickRecent="clickRecent"
          @deleteRecent="deleteRecent"
          @clearRecent="clearRecent"
          @deleteCollect="deleteCollect"
          @showDetail="clickFavor"
        />
        <div class="resource-search-divider"></div>
        <InstanceList
          :list="instanceList"
          :tabList="ciTabList"
          :referenceShowAttrNameMap="referenceShowAttrNameMap"
          :referenceCIIdMap="referenceCIIdMap"
          :favorList="favorList"
          :detailCIId="detailCIId"
          :searchValue="currentSearchValue"
          @showDetail="showDetail"
          @addCollect="addCollect"
          @deleteCollect="deleteCollect"
        />

        <div class="resource-search-pagination">
          <a-pagination
            :showSizeChanger="true"
            :current="currentPage"
            size="small"
            :total="totalNumber"
            show-quick-jumper
            :page-size="pageSize"
            :page-size-options="pageSizeOptions"
            @showSizeChange="handlePageSizeChange"
            :show-total="
              (total, range) =>
                $t('pagination.total', {
                  range0: range[0],
                  range1: range[1],
                  total,
                })
            "
            @change="changePage"
          >
            <template slot="buildOptionText" slot-scope="props">
              <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
              <span v-if="props.value === '100000'">{{ $t('all') }}</span>
            </template>
          </a-pagination>
        </div>
      </div>

      <div v-if="showInstanceDetail" class="resource-search-after-right">
        <InstanceDetail
          :CIId="detailCIId"
          :CITypeId="detailCITypeId"
          :favorList="favorList"
          @addCollect="addCollect"
          @deleteCollect="deleteCollect"
          @hideDetail="hideDetail"
        />
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import { getPreferenceSearch, savePreferenceSearch, getSubscribeAttributes, deletePreferenceSearch } from '@/modules/cmdb/api/preference'
import { searchAttributes, getCITypeAttributesByTypeIds } from '@/modules/cmdb/api/CITypeAttr'
import { searchCI } from '@/modules/cmdb/api/ci'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { SEARCH_MODE } from './constants.js'

import SearchInput from './components/searchInput.vue'
import HistoryList from './components/historyList.vue'
import InstanceList from './components/instanceList.vue'
import InstanceDetail from './components/instanceDetail.vue'

export default {
  name: 'ResourceSearchCom',
  components: {
    SearchInput,
    HistoryList,
    InstanceList,
    InstanceDetail
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
      // 筛选条件
      searchValue: '', // 搜索框
      selectCITypeIds: [], // 已选模型
      expression: '', // 筛选语句
      currentSearchValue: '', // 当前已搜索语句

      recentList: [], // 最近搜索
      favorList: [], // 我的收藏
      allAttributesList: [],

      isSearch: false, // 是否搜索过
      currentPage: 1,
      pageSizeOptions: ['50', '100', '200', '100000'],
      pageSize: 50,
      totalNumber: 0,
      ciTabList: [],
      instanceList: [],
      referenceShowAttrNameMap: {},
      referenceCIIdMap: {},

      showInstanceDetail: false,
      detailCIId: -1,
      detailCITypeId: -1,
      currentSearchMode: SEARCH_MODE.NORMAL,
    }
  },
  computed: {
    ...mapState({
      cmdbSearchValue: (state) => state.app.cmdbSearchValue,
    }),
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  watch: {
    cmdbSearchValue: {
      handler(value) {
        this.searchValue = value
        this.saveCondition(true)
      }
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    async initData() {
      await this.getFavorList()

      this.$nextTick(async () => {
        if (this.cmdbSearchValue) {
          this.searchValue = this.cmdbSearchValue
          this.saveCondition(true)
        } else {
          await this.getRecentList()
        }
      })

      await this.getAllAttr()
    },

    async getRecentList() {
      const recentList = await getPreferenceSearch({
        name: '__recent__'
      })
      recentList.sort((a, b) => b.id - a.id)
      this.recentList = recentList
    },

    async getFavorList() {
      const favorList = await getPreferenceSearch({
        name: '__favor__'
      })
      favorList.sort((a, b) => b.id - a.id)
      this.favorList = favorList
    },

    async getAllAttr() {
      const res = await searchAttributes({ page_size: 9999 })
      this.allAttributesList = res.attributes
      this.originAllAttributesList = res.attributes
    },

    async updateAllAttributesList(value) {
      if (value && value.length) {
        const res = await getCITypeAttributesByTypeIds({ type_ids: value.join(',') })
        this.allAttributesList = res.attributes
      } else {
        this.allAttributesList = this.originAllAttributesList
      }
    },

    async saveCondition(isSubmit) {
      if (
        this.searchValue ||
        this.expression ||
        this.selectCITypeIds.length
      ) {
        const needDeleteList = []
        const differentList = []
        this.recentList.forEach((item) => {
          const option = item.option
          if (
            option.searchValue === this.searchValue &&
            option.expression === this.expression &&
            _.isEqual(option.ciTypeIds, this.selectCITypeIds) &&
            option.searchMode === this.currentSearchMode
          ) {
            needDeleteList.push(item.id)
          } else {
            differentList.push(item.id)
          }
        })
        if (differentList.length >= 10) {
          needDeleteList.push(...differentList.slice(9))
        }
        if (needDeleteList.length) {
          await Promise.all(
            needDeleteList.map((id) => deletePreferenceSearch(id))
          )
        }

        const ciTypeNames = this.selectCITypeIds.map((id) => {
          const ciType = this.allCITypes.find((item) => item.id === id)
          return ciType?.alias || ciType?.name || id
        })

        await savePreferenceSearch({
          option: {
            searchValue: this.searchValue,
            expression: this.expression,
            ciTypeIds: this.selectCITypeIds,
            ciTypeNames,
            searchMode: this.currentSearchMode
          },
          name: '__recent__'
        })
        this.getRecentList()
      }

      if (isSubmit) {
        this.isSearch = true
        this.currentPage = 1
        this.hideDetail()
        this.loadInstance()
      }
    },

    async deleteRecent(id) {
      await deletePreferenceSearch(id)
      this.getRecentList()
    },

    async clearRecent() {
      const deletePromises = this.recentList.map((item) => {
        return deletePreferenceSearch(item.id)
      })
      await Promise.all(deletePromises)
      this.getRecentList()
    },

    async loadInstance() {
      const { selectCITypeIds, expression, searchValue } = this
      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null

      const ciTypeIds = [...selectCITypeIds]
      if (!ciTypeIds.length) {
        this.CITypeGroup.forEach((item) => {
          const ids = item.ci_types.map((ci_type) => ci_type.id)
          ciTypeIds.push(...ids)
        })
      }

      let querySearchValue = ''
      if (searchValue) {
        if (
          this.currentSearchMode === SEARCH_MODE.COLUMN &&
          searchValue.includes('\n')
        ) {
          const values = searchValue.split('\n').filter(v => v.trim())
          querySearchValue = `,(${values.join(';')})`
        } else {
          querySearchValue = `,*${searchValue}*`
        }
      }

      const res = await searchCI({
        q: `${ciTypeIds?.length ? `_type:(${ciTypeIds.join(';')})` : ''}${exp ? `,${exp}` : ''}${querySearchValue}`,
        count: this.pageSize,
        page: this.currentPage,
        sort: '_type'
      })
      this.currentSearchValue = searchValue

      this.totalNumber = res?.numfound ?? 0
      if (!res?.result?.length) {
        this.ciTabList = []
        this.instanceList = []
      }

      const ciTabMap = new Map()

      let list = res.result
      list.forEach((item) => {
        const ciType = this.allCITypes.find((type) => type.id === item._type)
        if (ciTabMap.has(item._type)) {
          ciTabMap.get(item._type).count++
        } else {
          ciTabMap.set(item._type, {
            id: item._type,
            count: 1,
            title: ciType?.alias || ciType?.name || '',
          })
        }
      })

      const mapEntries = [...ciTabMap.entries()]
      const subscribedPromises = mapEntries.map((item) => {
        return getSubscribeAttributes(item[0])
      })
      const subscribedRes = await Promise.all(subscribedPromises)
      list = list.map((item) => {
        const subscribedIndex = mapEntries.findIndex((mapValue) => mapValue[0] === item._type)
        const subscribedAttr = subscribedRes?.[subscribedIndex]?.attributes || []
        const obj = {
          ci: item,
          ciTypeObj: {},
          attributes: subscribedAttr
        }

        const ciType = this.allCITypes.find((type) => type.id === item._type)
        obj.ciTypeObj = {
          showAttrName: ciType?.show_name || ciType?.unique_key || '',
          icon: ciType?.icon || '',
          title: ciType?.alias || ciType?.name || '',
          name: ciType?.name || '',
          id: ciType.id
        }

        return obj
      })

      this.instanceList = list
      const ciTabList = [...ciTabMap.values()]
      if (list?.length) {
        ciTabList.unshift({
          id: -1,
          title: this.$t('all'),
          count: list?.length
        })
      }
      this.ciTabList = ciTabList

      // 处理引用属性
      const allAttr = []
      subscribedRes.map((item) => {
        allAttr.push(...item.attributes)
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
      this.instanceList.forEach(({ ci }) => {
        needRequiredCIType.forEach((col) => {
          const ids = Array.isArray(ci[col.name]) ? ci[col.name] : ci[col.name] ? [ci[col.name]] : []
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

    clickRecent(data) {
      this.updateAllAttributesList(data.ciTypeIds || [])
      this.isSearch = true
      this.currentPage = 1
      this.searchValue = data?.searchValue || ''
      this.expression = data?.expression || ''
      this.selectCITypeIds = data?.ciTypeIds || []
      this.currentSearchMode = data?.searchMode || 'normal'

      this.hideDetail()
      this.loadInstance()
    },

    handlePageSizeChange(_, pageSize) {
      this.pageSize = pageSize
      this.currentPage = 1
      this.loadInstance()
    },

    changePage(page) {
      this.currentPage = page
      this.loadInstance()
    },

    changeFilter(data) {
      this[data.name] = data.value
    },

    showDetail(data) {
      this.detailCIId = data.id
      this.detailCITypeId = data.ciTypeId
      this.showInstanceDetail = true
    },

    hideDetail() {
      this.detailCIId = -1
      this.detailCITypeId = -1
      this.showInstanceDetail = false
    },

    async addCollect(data) {
      if (this?.favorList?.length >= 10) {
        const deletePromises = this.favorList.slice(9).map((item) => {
          return deletePreferenceSearch(item.id)
        })
        await Promise.all(deletePromises)
      }
      await savePreferenceSearch({
        option: {
          ...data
        },
        name: '__favor__'
      })
      this.getFavorList()
    },

    async deleteCollect(id) {
      await deletePreferenceSearch(id)
      this.getFavorList()
    },

    clickFavor(data) {
      this.isSearch = true
      this.showDetail(data)
    },

    updateSearchMode(mode) {
      this.currentSearchMode = mode
    }
  }
}
</script>

<style lang="less" scoped>
.resource-search {
  width: 100%;
  height: 100%;
  position: relative;

  &-before {
    width: 100%;
    max-width: 718px;
    height: 100%;
    margin: 0 auto;
    padding-top: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;

    & > div {
      position: relative;
      z-index: 1;
    }

    &-bg {
      position: absolute;
      left: -24px;
      bottom: -24px;
      width: calc(100% + 48px);
      z-index: 0;
    }
  }

  &-title {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 25px;

    &-icon {
      font-size: 28px;
    }

    &-text {
      margin-left: 10px;
      font-size: 20px;
      font-weight: 700;
      color: #1D2129;
    }
  }

  &-after {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;

    &-left {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;

      & > div {
        flex-shrink: 0;
      }
    }

    &-right {
      margin-left: 20px;
      width: calc(30% - 20px);
      flex-shrink: 0;
    }
  }

  &-divider {
    width: 100%;
    height: 1px;
    background-color: #E4E7ED;
    margin: 20px 0;
  }

  &-pagination {
    text-align: right;
    margin: 12px 0px;
  }
}
</style>
