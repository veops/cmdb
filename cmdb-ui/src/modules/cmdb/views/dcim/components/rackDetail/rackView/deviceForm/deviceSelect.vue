<template>
  <div class="device-select">
    <a-input-search
      @search="handleSearch"
    />

    <a-radio-group
      v-if="CIList.length"
      :value="currentSelect"
      class="device-select-group"
      @change="handleCIChange"
    >
      <a-radio
        v-for="(item) in CIList"
        :key="item.value"
        :value="item.value"
        class="device-select-item"
      >
        <a-tooltip :title="item.name" placement="topLeft">
          {{ item.name }}
        </a-tooltip>
      </a-radio>
    </a-radio-group>

    <div v-else class="device-select-null">
      <img class="device-select-null-img" :src="require(`@/assets/data_empty.png`)"></img>
      <div class="device-select-null-text">{{ $t('noData') }}</div>
    </div>

    <div class="device-select-pagination">
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
        @change="handleChangePage"
        @showSizeChange="onShowSizeChange"
      >
        <template slot="buildOptionText" slot-scope="props">
          <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
          <span v-if="props.value === '100000'">{{ $t('cmdb.ci.all') }}</span>
        </template>
      </a-pagination>
    </div>
  </div>
</template>

<script>
import { searchCI } from '@/modules/cmdb/api/ci'

export default {
  name: 'DeviceSelect',
  props: {
    currentSelect: {
      type: [Number, undefined],
      default: undefined
    },
    CITypeId: {
      type: [Number, undefined],
      default: undefined
    },
    currentCITYpe: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      page: 1,
      pageSize: 20,
      pageSizeOptions: ['20', '50', '100'],
      totalNumber: 0,
      CIList: [],

      searchValue: ''
    }
  },
  watch: {
    CITypeId: {
      immediate: true,
      deep: true,
      handler(newVal, oldVal) {
        this.page = 1
        this.searchValue = ''

        if (newVal && newVal !== oldVal) {
          this.getCIList()
        } else {
          this.CIList = []
          this.totalNumber = 0
        }
      }
    }
  },
  methods: {
    async getCIList() {
      const res = await searchCI({
        q: `_type:${this.CITypeId}${this.searchValue ? `,*${this.searchValue}*` : ''}`,
        count: this.pageSize,
        page: this.page
      })
      let CIList = res?.result || []

      const {
        show_key = '',
        unique_id = '',
        attributes = []
      } = this?.currentCITYpe || {}
      const unique_key = attributes?.find((attr) => attr?.id === unique_id)?.name || ''

      if (CIList.length) {
        CIList = CIList.map((item) => {
          return {
            value: item?._id,
            name: item?.[show_key] || item?.[unique_key] || item?._id || '',
            unitCount: item?.u_count ?? 0
          }
        })
      }

      this.CIList = CIList
      this.totalNumber = res?.numfound || 0
    },

    handleSearch(value) {
      this.searchValue = value
      this.page = 1
      this.getCIList()
    },

    handleChangePage(page) {
      this.page = page
      this.getCIList()
    },

    onShowSizeChange(_, pageSize) {
      this.page = 1
      this.pageSize = pageSize
      this.getCIList()
    },

    handleCIChange(e) {
      const value = e.target.value
      const findCI = this.CIList.find((item) => item.value === value)

      this.$emit('change', findCI)
    }
  }
}
</script>

<style lang="less" scoped>
.device-select {
  width: 650px;

  &-group {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    row-gap: 20px;
    margin: 12px 0px;
    max-height: 40vh;
    overflow-y: auto;
    overflow-x: hidden;
  }

  &-item {
    width: 48%;
    flex-shrink: 0;

    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
  }

  &-null {
    margin: 30px 0px;
    text-align: center;
    width: 100%;

    &-img {
      width: 130px;
    }

    &-text {
      margin-top: 12px;
    }
  }

  &-pagination {
    text-align: right;
    margin-top: 4px;
  }
}
</style>
