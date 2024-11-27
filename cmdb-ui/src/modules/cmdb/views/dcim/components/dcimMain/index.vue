<template>
  <div class="dcim-main" ref="rackMainRef">
    <div v-if="!roomId" class="dcim-main-null">
      <img class="dcim-main-null-img" :src="require(`@/modules/cmdb/assets/dcim/dcim_null.png`)"></img>
      <div class="dcim-main-null-tip">{{ $t('noData') }}</div>
      <div class="dcim-main-null-tip2">{{ $t('cmdb.dcim.roomNullTip') }}</div>
    </div>

    <template v-else>
      <DCIMStats :statsData="statsData" />

      <div class="dcim-main-row">
        <div class="dcim-main-filter">
          <a-input-search
            v-model="searchValue"
            :placeholder="$t('cmdb.dcim.rackSearchTip')"
            class="dcim-main-row-search"
          />

          <a-select
            class="dcim-main-row-select"
            :getPopupContainer="(trigger) => trigger.parentElement"
            v-model="currentRackType"
          >
            <a-icon slot="suffixIcon" type="caret-down" />
            <a-select-option
              v-for="(item) in rackTypeSelectOption"
              :key="item.value"
              :value="item.value"
              :class="item.value === 'unitAbnormal' ? 'dcim-main-row-select-unitAbnormal' : ''"
            >
              {{ item.label }}
            </a-select-option>
          </a-select>
        </div>

        <div class="dcim-main-row-right">
          <div class="dcim-main-layout">
            <div
              v-for="(item) in layoutList"
              :key="item.value"
              :class="['dcim-main-layout-item', currentLayout === item.value ?'dcim-main-layout-item-active' : '']"
              @click="handleChangeLayout(item.value)"
            >
              <ops-icon :type="item.icon" />
            </div>
          </div>

          <a-button
            type="primary"
            class="ops-button-ghost"
            ghost
            @click="addRack"
          >
            <a-icon type="plus-circle" />
            {{ $t('cmdb.dcim.addRack') }}
          </a-button>
        </div>
      </div>

      <div
        class="rack-wrap"
      >
        <RackGrid
          v-if="currentLayout === 'grid'"
          :rackList="filterRackList"
          @openRackDetail="openRackDetail"
        />

        <RackTable
          v-if="currentLayout === 'table'"
          :rackList="filterRackList"
          :columns="columns"
          :preferenceAttrList="preferenceAttrList"
          :CITypeId="rackCITYpe.id"
        />
      </div>

      <RackDetail
        ref="rackDetailRef"
        :roomId="roomId"
        :rackCITYpe="rackCITYpe"
        :rackList="rackList"
        @openForm="(data) => $emit('openForm', data)"
        @refreshRackList="getRackList"
      />
    </template>
  </div>
</template>

<script>
import _ from 'lodash'
import { DCIM_TYPE } from '../../constants.js'
import { getDCIMRacks } from '@/modules/cmdb/api/dcim.js'
import { getCITableColumns } from '@/modules/cmdb/utils/helper'

import DCIMStats from './dcimStats.vue'
import RackGrid from './rackGrid.vue'
import RackTable from './rackTable.vue'
import RackDetail from '../rackDetail/index.vue'

export default {
  name: 'DCIMMain',
  components: {
    DCIMStats,
    RackGrid,
    RackTable,
    RackDetail
  },
  props: {
    roomId: {
      type: String,
      default: ''
    },
    attrObj: {
      type: Object,
      default: () => {}
    },
    rackCITYpe: {
      type: Object,
      default: () => {}
    },
    preferenceAttrList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      searchValue: '',
      currentRackType: 'all',
      rackList: [],
      columns: [],

      statsData: {},

      currentLayout: 'grid',
      layoutList: [
        {
          value: 'grid',
          icon: 'veops-map_view'
        },
        {
          value: 'table',
          icon: 'monitor-list_view'
        }
      ]
    }
  },
  computed: {
    rackTypeSelectOption() {
      const selectOption = [
        {
          value: 'all',
          label: this.$t('all')
        }
      ]

      const rackTypeAttr = this.attrObj?.attributes?.find?.((item) => item.name === 'rack_type')
      if (rackTypeAttr?.choice_value?.length) {
        rackTypeAttr.choice_value.map((item) => {
          selectOption.push({
            value: item?.[0] || '',
            label: item?.[1]?.label || item?.[0] || ''
          })
        })
      }

      selectOption.push({
        value: 'unitAbnormal',
        label: this.$t('cmdb.dcim.unitAbnormal')
      })

      return selectOption
    },
    filterRackList() {
      let rackList = _.cloneDeep(this.rackList)

      if (this.searchValue) {
        rackList = rackList.filter((item) => item.name.indexOf(this.searchValue) !== -1)
      }

      if (this.currentRackType !== 'all') {
        if (this.currentRackType === 'unitAbnormal') {
          rackList = rackList.filter((item) => item.u_slot_abnormal)
        } else {
          rackList = rackList.filter((item) => item.rack_type === this.currentRackType)
        }
      }

      return rackList
    }
  },
  provide() {
    return {
      getRackList: this.getRackList,
      handleSearch: this.getRackList,
      attrList: () => {
        return this?.attrObj?.attributes || []
      },
      attributes: () => {
        return this.attrObj
      }
    }
  },
  watch: {
    roomId: {
      immediate: true,
      deep: true,
      handler(id) {
        if (id) {
          this.initData()
        } else {
          this.rackList = []
          this.statsData = {}
        }
      }
    }
  },
  methods: {
    async initData() {
      try {
        await this.getRackList()
      } catch (error) {
        console.log('initData error', error)
      }
    },

    async getRackList() {
      const res = await getDCIMRacks(this.roomId)
      const rackList = res?.result || []

      const jsonAttrList = this.preferenceAttrList.filter((attr) => attr.value_type === '6')
      rackList.forEach((item) => {
        item.free_u_count = item.free_u_count ?? 0
        item.u_count = item.u_count ?? 0
        item.u_used_count = item.u_count - item.free_u_count
        item.u_used_ratio = item.u_used_count > 0 && item.u_count > 0 ? Math.round((item.u_used_count / item.u_count) * 100) : 0

        jsonAttrList.forEach(
          (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
        )
      })

      this.getColumns(rackList)

      this.rackList = rackList
      this.statsData = res?.counter || {}
    },

    getColumns(data) {
      const width = this.$refs.rackMainRef.clientWidth - 50
      const columns = getCITableColumns(data, this.preferenceAttrList, width)
      columns.forEach((item) => {
        if (item.editRender) {
          item.editRender.enabled = false
        }
      })
      this.columns = columns
    },

    handleChangeLayout(value) {
      if (this.currentLayout !== value) {
        this.currentLayout = value
      }
    },

    addRack() {
      this.$emit('openForm', {
        dcimType: DCIM_TYPE.RACK,
        parentId: this.roomId
      })
    },

    openRackDetail(data) {
      this.$refs.rackDetailRef.open(data._id)
    }
  }
}
</script>

<style lang="less" scoped>
.dcim-main {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;

  &-null {
    width: 100%;
    padding-top: 95px;
    text-align: center;

    &-img {
      height: 200px;
    }

    &-tip {
      font-size: 14px;
      font-weight: 400;
      color: #86909C;
    }

    &-tip2 {
      font-size: 14px;
      font-weight: 400;
      color: #2F54EB;
    }
  }

  &-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    margin-top: 20px;

    &-search {
      width: 300px;
    }

    &-select {
      width: 120px;
      margin-left: 22px;
      flex-shrink: 0;

      /deep/ &-unitAbnormal {
        border-top: dashed 1px #e8e8e8;
      }
    }

    &-right {
      display: flex;
      align-items: center;
      column-gap: 21px;
    }
  }

  &-layout {
    display: flex;
    align-items: center;
    height: 32px;
    border: solid 1px #E4E7ED;

    &-item {
      height: 100%;
      width: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      cursor: pointer;

      &:not(:last-child) {
        border-right: solid 1px #E4E7ED;
      }

      &-active {
        color: #2F54EB;
        background-color: #F0F5FF;
      }

      &:hover {
        color: #2F54EB;
      }
    }
  }

  .rack-wrap {
    margin-top: 22px;
    margin-bottom: 22px;
    height: 100%;
    overflow: hidden;
  }
}
</style>
