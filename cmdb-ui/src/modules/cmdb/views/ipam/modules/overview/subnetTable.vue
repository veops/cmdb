<template>
  <div class="subnet-table">
    <div class="subnet-table-title">
      {{ $t('cmdb.ipam.onlineUsageStats') }}
    </div>

    <ops-table
      ref="xTable"
      show-overflow
      show-header-overflow
      highlight-hover-row
      :data="tableData"
      size="small"
      :height="tableHeight"
      :column-config="{ resizable: true }"
      class="ops-unstripe-table"
    >
      <vxe-table-column
        :title="$t('cmdb.ipam.subnetName')"
        :min-width="130"
        field="name"
      ></vxe-table-column>
      <vxe-table-column
        title="CIDR"
        field="cidr"
        :min-width="130"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.addressCount')"
        field="hosts_count"
        :min-width="70"
      ></vxe-table-column>
      <vxe-table-column
        :title="$t('cmdb.ipam.onlineRatio')"
        field="onlineRatio"
        :min-width="180"
      >
        <template #default="{ row }">
          <div class="subnet-table-ratio">
            <div class="subnet-table-ratio-value">
              {{ row.used_ratio }}%
            </div>
            <div class="subnet-table-ratio-progress">
              <div
                class="subnet-table-ratio-progress-content"
                :style="{
                  width: row.used_ratio + '%'
                }"
              ></div>
            </div>
            <div class="subnet-table-ratio-count">
              {{ row.used_count }}/{{ row.hosts_count }}
            </div>
          </div>
        </template>
      </vxe-table-column>

      <vxe-table-column
        :title="$t('cmdb.ipam.assigned')"
        field="assign_count"
        :min-width="70"
      ></vxe-table-column>

      <vxe-table-column
        :title="$t('cmdb.ipam.free')"
        field="free_count"
        :min-width="50"
      ></vxe-table-column>

      <vxe-table-column
        :title="$t('cmdb.ipam.scanEnable')"
        field="scan_enabled"
        :min-width="100"
      >
        <template #default="{ row }">
          <div class="subnet-table-scan-yes" v-if="row.scan_enabled">
            <a-icon class="subnet-table-scan-yes-icon" type="check-circle" theme="filled" />
            <div class="subnet-table-scan-yes-text">{{ $t('yes') }}</div>
          </div>
          <div class="subnet-table-scan-no" v-else>
            <a-icon class="subnet-table-scan-no-icon" type="close-circle" theme="filled" />
            <div class="subnet-table-scan-no-text">{{ $t('no') }}</div>
          </div>
        </template>
      </vxe-table-column>

      <vxe-table-column
        :title="$t('cmdb.ipam.lastScanTime')"
        field="last_scan_time"
        :min-width="100"
      ></vxe-table-column>
    </ops-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'SubnetTable',
  props: {
    tableData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {}
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 337}px`
    },
  },
  methods: {}
}
</script>

<style lang="less" scoped>
.subnet-table {
  width: 100%;
  margin-top: 20px;

  &-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 16px;
  }

  &-ratio {
    display: flex;
    align-items: center;

    &-value {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
    }

    &-progress {
      width: 84px;
      height: 6px;
      border-radius: 6px;
      background-color: #EBEFF8;
      margin-left: 12px;

      &-content {
        height: 6px;
        border-radius: 6px;
        background-color: #7F97FA;
      }
    }

    &-count {
      margin-left: 5px;
      font-size: 10px;
      font-weight: 400;
      color: #86909C;
    }
  }

  &-scan-yes {
    padding: 4px 7px;
    border-radius: 1px;
    background-color: #DCF3E3;
    display: inline-flex;
    align-items: center;
    justify-content: center;

    &-icon {
      font-size: 12px;
      color: #00B42A;
    }

    &-text {
      font-size: 12px;
      font-weight: 400;
      color: #30AD2D;
      margin-left: 4px;
    }
  }

  &-scan-no {
    padding: 0px 7px;
    border-radius: 1px;
    background-color: #E4E7ED;
    display: inline-flex;
    align-items: center;
    justify-content: center;

    &-icon {
      font-size: 12px;
      color: #A5A9BC;
    }

    &-text {
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;
      margin-left: 4px;
    }
  }
}
</style>
