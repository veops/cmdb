<template>
  <div
    ref="deviceListRef"
    class="device-list"
  >
    <div class="device-list-tabs">
      <div
        v-for="(item) in tabs"
        :key="item.id"
        :class="[
          'device-list-tabs-item',
          item.id === tabActive ? 'device-list-tabs-item_active' : ''
        ]"
        @click="clickTab(item.id)"
      >
        <CIIcon :icon="item.icon" />
        <span class="device-list-tabs-item-name" >{{ item.alias || item.name }}</span>
      </div>
    </div>

    <CITable
      ref="xTable"
      :attrList="preferenceAttrList"
      :columns="columns"
      :data="deviceList"
      :height="tableHeight"
      :showCheckbox="false"
      :showDelete="false"
      :sortConfig="{ remote: false, trigger: 'default' }"
      @openDetail="openDetail"
    />

    <CIDetailDrawer
      v-if="tabActive"
      ref="CIdetailRef"
      :typeId="tabActive"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { getCITableColumns } from '@/modules/cmdb/utils/helper'

import CIIcon from '@/modules/cmdb/components/ciIcon/index.vue'
import CITable from '@/modules/cmdb/components/ciTable/index.vue'
import CIDetailDrawer from '@/modules/cmdb/views/ci/modules/ciDetailDrawer.vue'

export default {
  name: 'DeviceList',
  components: {
    CIIcon,
    CITable,
    CIDetailDrawer
  },
  props: {
    allDeviceList: {
      type: Array,
      default: () => []
    },
    CITypeRelations: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      tabActive: '',
      tabs: [],

      preferenceAttrList: [],
      deviceList: [],
      columns: [],
      deviceCIType: {}
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 210}px`
    },
  },
  inject: [
    'getDeviceList',
    'getRackList'
  ],
  provide() {
    return {
      handleSearch: this.refreshData,
      attrList: () => {
        return this?.deviceCIType?.attributes || []
      },
      attributes: () => {
        return {
          attributes: this?.deviceCIType?.attributes || [],
          unique_id: this?.deviceCIType?.unique_id || 0,
          unique: this?.deviceCIType?.show_key || ''
        }
      }
    }
  },
  watch: {
    allDeviceList: {
      immediate: true,
      deep: true,
      handler() {
        this.initData()
      }
    }
  },
  methods: {
    initData() {
      const tabs = []
      this.allDeviceList.forEach((item) => {
        const CIType = this.CITypeRelations.find((CIType) => CIType.id === item._type)

        tabs.push({
          icon: CIType.icon,
          name: item.ci_type,
          alias: item.ci_type_alias,
          id: item._type
        })
      })

      this.clickTab(tabs?.[0]?.id ?? '')
      this.tabs = _.uniqBy(tabs, 'id')
    },

    clickTab(id) {
      if (id !== this.tabActive) {
        this.tabActive = id

        if (this.tabActive) {
          this.initTableData()
        } else {
          this.columns = []
          this.deviceList = []
        }
      }
    },

    async initTableData() {
      const subscribed = await getSubscribeAttributes(this.tabActive)
      this.preferenceAttrList = subscribed.attributes

      const deviceList = this.allDeviceList.filter((item) => item._type === this.tabActive)

      const deviceCIType = this.CITypeRelations.find((item) => item.id === this.tabActive)
      this.deviceCIType = deviceCIType || {}

      this.getColumns(deviceList)
      this.deviceList = deviceList
    },

    getColumns(data) {
      const width = this.$refs.deviceListRef.clientWidth - 50
      const columns = getCITableColumns(data, this.preferenceAttrList, width)
      columns.forEach((item) => {
        if (item.editRender) {
          item.editRender.enabled = false
        }
      })
      this.columns = columns
    },

    refreshData() {
      this.getDeviceList()
      this.getRackList()
    },

    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$refs.CIdetailRef.create(id, activeTabKey, ciDetailRelationKey)
    },
  }
}
</script>

<style lang="less" scoped>
.device-list {
  width: 100%;

  &-tabs {
    display: flex;
    flex-wrap: wrap;
    column-gap: 9px;
    row-gap: 5px;
    margin-bottom: 18px;

    &-item {
      flex-shrink: 0;
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 4px 12px;
      background-color: #F7F8FA;
      border-radius: 1px;
      border: solid 1px transparent;
      max-width: 100%;

      &-name {
        margin-left: 4px;
        font-size: 12px;
        font-weight: 400;
        color: #1D2129;

        text-overflow: ellipsis;
        overflow: hidden;
        text-wrap: nowrap;
      }

      &_active {
        border-color: #B1C9FF;
        background-color: #F9FBFF;
      }

      &:hover {
        .device-list-tabs-item-name {
          color: #3F75FF;
        }
      }
    }
  }
}
</style>
