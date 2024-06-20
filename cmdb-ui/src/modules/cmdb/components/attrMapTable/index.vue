<template>
  <div class="attr-map-table">
    <div class="attr-map-table-left">
      <div class="attr-map-table-title">{{ $t('cmdb.ciType.attributes') }}</div>
      <vxe-table
        ref="attr-xTable-left"
        size="mini"
        :data="tableData"
        :scroll-y="{ enabled: true }"
        :min-height="78"
      >
        <vxe-column field="attr" :title="$t('name')">
          <template #default="{ row }">
            <div class="attr-select">
              <span
                v-if="uniqueKey"
                :style="{
                  opacity: uniqueKey === row.name ? 1 : 0
                }"
                class="attr-select-unique"
              >
                *
              </span>
              <vxe-select
                filterable
                clearable
                v-model="row.attr"
                type="text"
                :options="ciTypeAttributes"
                transfer
                :placeholder="$t('cmdb.ciType.attrMapTableAttrPlaceholder')"
              ></vxe-select>
            </div>
          </template>
        </vxe-column>
      </vxe-table>
    </div>
    <div class="attr-map-table-right">
      <div class="attr-map-table-title">{{ $t('cmdb.ciType.autoDiscovery') }}</div>
      <vxe-table
        ref="attr-xTable-right"
        size="mini"
        show-overflow
        show-header-overflow
        :data="tableData"
        :scroll-y="{ enabled: true }"
        :row-config="{ height: 42 }"
        :min-height="78"
      >
        <vxe-column field="name" :title="$t('name')"></vxe-column>
        <vxe-column field="type" :title="$t('type')"></vxe-column>
        <vxe-column v-if="ruleType !== 'agent'" field="example" :title="$t('cmdb.components.example')">
          <template #default="{row}">
            <span v-if="row.type === 'json'">{{ JSON.stringify(row.example) }}</span>
            <span v-else>{{ row.example }}</span>
          </template>
        </vxe-column>
        <vxe-column field="desc" :title="$t('desc')"></vxe-column>
      </vxe-table>
    </div>
    <div class="attr-map-table-link">
      <div
        v-for="item in tableData"
        :key="item._X_ROW_KEY"
        class="attr-map-table-link-item"
      >
        <div class="attr-map-table-link-left"></div>
        <div class="attr-map-table-link-right"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AttrMapTable',
  props: {
    tableData: {
      type: Array,
      default: () => [],
    },
    ciTypeAttributes: {
      type: Array,
      default: () => [],
    },
    ruleType: {
      type: String,
      default: '',
    },
    uniqueKey: {
      type: String,
      default: '',
    }
  },
  data() {
    return {}
  },
  methods: {
    getTableData() {
      const leftTable = this.$refs?.['attr-xTable-left']
      const rightTable = this.$refs?.['attr-xTable-right']
      const { fullData: leftFullData } = leftTable.getTableData()
      const { fullData: rightFullData } = rightTable.getTableData()
      const fullData = leftFullData.map((item, index) => {
        return {
          ...(rightFullData?.[index] || {}),
          ...(item || {})
        }
      })
      return {
        fullData
      }
    },
  }
}
</script>

<style lang="less" scoped>
.attr-map-table {
  display: flex;
  justify-content: space-between;
  position: relative;

  &-left {
    width: 30%;
  }

  &-right {
    width: calc(70% - 60px);
  }

  &-title {
    font-size: 14px;
    font-weight: 700;
    line-height: 22px;
    margin-bottom: 12px;
  }

  &-link {
    position: absolute;
    z-index: 10;
    bottom: 0;
    left: calc(30% - 6px);
    width: 66px;

    &-item {
      position: relative;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: calc(42px - 12px);
      width: 100%;

      &:last-child {
        margin-bottom: calc(21px - 6px);
      }

      &::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 1px;
        background-color: @border-color-base;
        z-index: -1;
      }
    }

    &-left {
      width: 12px;
      height: 12px;
      background-color: @primary-color;
      border: solid 3px #E2E7FC;
      border-radius: 50%;
    }

    &-right {
      width: 2px;
      height: 10px;
      border-radius: 1px 0px 0px 1px;
      background-color: @primary-color;
    }
  }

  .attr-select {
    display: flex;
    align-items: center;
    gap: 10px;

    &-unique {
      color: #FD4C6A;
    }
  }
}
</style>
