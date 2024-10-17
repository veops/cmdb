<template>
  <div class="resource-search">
    <div class="resource-search-tab">
      <div
        v-for="(tab) in tabList"
        :key="tab.value"
        :class="['resource-search-tab-item', tabActive === tab.value ? 'resource-search-tab-item_active' : '']"
        @click="tabActive = tab.value"
      >
        {{ $t(tab.lable) }}
      </div>
    </div>

    <template v-if="isInit">
      <ResourceSearchCom
        v-show="tabActive === 'resourceSearch'"
        :CITypeGroup="CITypeGroup"
        :allCITypes="allCITypes"
      />
      <RelationSearch
        v-show="tabActive === 'relationSearch'"
        :CITypeGroup="CITypeGroup"
        :allCITypes="allCITypes"
      />
    </template>
  </div>
</template>

<script>
import { getCITypeGroups } from '@/modules/cmdb/api/ciTypeGroup'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { mapState } from 'vuex'

import ResourceSearchCom from './resourceSearch/index.vue'
import RelationSearch from './relationSearch/index.vue'

export default {
  name: 'ResourceSearch',
  components: {
    ResourceSearchCom,
    RelationSearch
  },
  data() {
    return {
      tabActive: 'resourceSearch',
      tabList: [
        {
          lable: 'cmdb.ciType.resourceSearch',
          value: 'resourceSearch'
        },
        {
          lable: 'cmdb.relationSearch.relationSearch',
          value: 'relationSearch'
        }
      ],
      CITypeGroup: [],
      allCITypes: [],
      isInit: false,
    }
  },
  computed: {
    ...mapState({
      cmdbSearchValue: (state) => state.app.cmdbSearchValue,
    }),
  },
  watch: {
    cmdbSearchValue: {
      immediate: true,
      deep: true,
      handler() {
        this.tabActive = 'resourceSearch'
      }
    }
  },
  async mounted() {
    try {
      await Promise.all([
        this.getCITypeGroups(),
        this.getAllCITypes()
      ])
    } catch (error) {
      console.log('resource search mounted fail', error)
    }

    this.isInit = true
  },
  methods: {
    async getCITypeGroups() {
      const res = await getCITypeGroups({ need_other: true })

      this.CITypeGroup = res
        .filter((item) => item?.ci_types?.length)
        .map((item) => {
          item.id = `parent_${item.id || -1}`
          return item
        })
    },

    async getAllCITypes() {
      const res = await getCITypes()
      this.allCITypes = res?.ci_types
    },
  },
}
</script>

<style lang="less" scoped>
.resource-search {
  width: 100%;
  height: 100%;

  &-tab {
    display: flex;
    align-items: center;
    margin-bottom: 12px;

    &-item {
      padding-right: 8px;
      margin-right: 8px;
      font-size: 14px;
      font-weight: 400;
      color: #86909C;
      cursor: pointer;

      &:not(:last-child) {
        border-right: solid 1px #E4E7ED;
      }

      &:hover {
        color: #2F54EB;
      }

      &_active {
        color: #2F54EB;
      }
    }
  }
}
</style>
