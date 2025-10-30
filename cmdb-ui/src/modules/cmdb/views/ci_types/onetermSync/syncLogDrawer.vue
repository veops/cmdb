<template>
  <a-drawer
    :title="$t('cmdb.ciType.onetermSync.syncLog')"
    :width="900"
    :visible="visible"
    :bodyStyle="{ paddingBottom: '80px' }"
    @close="handleClose"
  >
    <div class="sync-log-drawer">
      <!-- Filter Section -->
      <div class="filter-section">
        <a-row :gutter="16">
          <a-col :span="8">
            <a-input-search
              v-model="filterParams.search"
              :placeholder="$t('cmdb.ciType.onetermSync.searchCIName')"
              @search="handleSearch"
              allowClear
            >
              <a-icon slot="prefix" type="search" />
            </a-input-search>
          </a-col>
          <a-col :span="6">
            <a-select
              v-model="filterParams.status"
              :placeholder="$t('cmdb.ciType.onetermSync.filterByStatus')"
              style="width: 100%"
              allowClear
              @change="handleSearch"
            >
              <a-select-option value="success">
                <a-icon type="check-circle" style="color: #52c41a;" />
                {{ $t('cmdb.ciType.onetermSync.success') }}
              </a-select-option>
              <a-select-option value="failed">
                <a-icon type="close-circle" style="color: #f5222d;" />
                {{ $t('cmdb.ciType.onetermSync.failed') }}
              </a-select-option>
              <a-select-option value="skipped">
                <a-icon type="minus-circle" style="color: #d9d9d9;" />
                {{ $t('cmdb.ciType.onetermSync.skipped') }}
              </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="10">
            <a-range-picker
              v-model="filterParams.timeRange"
              :placeholder="[$t('cmdb.ciType.onetermSync.startTime'), $t('cmdb.ciType.onetermSync.endTime')]"
              style="width: 100%"
              format="YYYY-MM-DD HH:mm"
              :showTime="{ format: 'HH:mm' }"
              @change="handleSearch"
            />
          </a-col>
        </a-row>
      </div>

      <!-- Log Table -->
      <a-table
        :columns="columns"
        :dataSource="logData"
        :loading="loading"
        :pagination="pagination"
        :scroll="{ x: 800, y: 'calc(100vh - 400px)' }"
        rowKey="id"
        @change="handleTableChange"
        size="middle"
      >
        <template #time="text">
          <span>{{ formatTime(text) }}</span>
        </template>

        <template #ci_name="text, record">
          <a @click="viewCI(record.ci_id)">
            <a-icon type="database" style="margin-right: 4px;" />
            {{ text }}
          </a>
        </template>

        <template #status="text">
          <a-badge
            :status="getStatusBadge(text)"
            :text="getStatusLabel(text)"
          />
        </template>

        <template #details="text, record">
          <div class="details-cell">
            <span v-if="record.status === 'success'" class="success-msg">
              {{ text || $t('cmdb.ciType.onetermSync.syncSuccess') }}
            </span>
            <a-tooltip v-else-if="record.status === 'failed'" :title="text">
              <span class="error-msg">
                <a-icon type="exclamation-circle" />
                {{ truncateText(text, 30) }}
              </span>
            </a-tooltip>
            <span v-else class="skipped-msg">
              {{ text || $t('cmdb.ciType.onetermSync.noChanges') }}
            </span>
          </div>
        </template>

        <template #action="record">
          <a-space>
            <a-button
              v-if="record.status === 'failed'"
              type="link"
              size="small"
              @click="handleRetry(record)"
            >
              <a-icon type="redo" />
              {{ $t('cmdb.ciType.onetermSync.retry') }}
            </a-button>
            <a-button
              type="link"
              size="small"
              @click="viewDetails(record)"
            >
              <a-icon type="eye" />
              {{ $t('cmdb.ciType.onetermSync.viewDetails') }}
            </a-button>
          </a-space>
        </template>
      </a-table>

      <!-- Statistics Footer -->
      <div class="stats-footer">
        <a-space size="large">
          <span>
            {{ $t('cmdb.ciType.onetermSync.totalRecords') }}:
            <a-tag color="blue">{{ pagination.total }}</a-tag>
          </span>
          <span>
            {{ $t('cmdb.ciType.onetermSync.successCount') }}:
            <a-tag color="green">{{ stats.success }}</a-tag>
          </span>
          <span>
            {{ $t('cmdb.ciType.onetermSync.failedCount') }}:
            <a-tag color="red">{{ stats.failed }}</a-tag>
          </span>
          <span>
            {{ $t('cmdb.ciType.onetermSync.skippedCount') }}:
            <a-tag color="default">{{ stats.skipped }}</a-tag>
          </span>
        </a-space>
      </div>
    </div>

    <!-- Log Details Modal -->
    <a-modal
      v-model="detailsModalVisible"
      :title="$t('cmdb.ciType.onetermSync.logDetails')"
      :footer="null"
      width="700px"
    >
      <div v-if="currentLog" class="log-details">
        <a-descriptions bordered :column="1" size="small">
          <a-descriptions-item :label="$t('cmdb.ciType.onetermSync.syncTime')">
            {{ formatTime(currentLog.created_at) }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('cmdb.ciType.onetermSync.ciName')">
            <a @click="viewCI(currentLog.ci_id)">{{ currentLog.ci_name }}</a>
          </a-descriptions-item>
          <a-descriptions-item :label="$t('cmdb.ciType.onetermSync.operation')">
            <a-tag :color="getOperationColor(currentLog.operation)">
              {{ getOperationLabel(currentLog.operation) }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item :label="$t('cmdb.ciType.onetermSync.status')">
            <a-badge
              :status="getStatusBadge(currentLog.status)"
              :text="getStatusLabel(currentLog.status)"
            />
          </a-descriptions-item>
          <a-descriptions-item
            v-if="currentLog.asset_id"
            :label="$t('cmdb.ciType.onetermSync.onetermAssetId')"
          >
            {{ currentLog.asset_id }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('cmdb.ciType.onetermSync.details')">
            <pre class="details-content">{{ currentLog.details || '-' }}</pre>
          </a-descriptions-item>
          <a-descriptions-item
            v-if="currentLog.changes"
            :label="$t('cmdb.ciType.onetermSync.changes')"
          >
            <pre class="changes-content">{{ formatChanges(currentLog.changes) }}</pre>
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </a-modal>
  </a-drawer>
</template>

<script>
import moment from 'moment'

export default {
  name: 'SyncLogDrawer',
  props: {
    ciTypeId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      visible: false,
      loading: false,
      detailsModalVisible: false,
      currentLog: null,
      logData: [],
      filterParams: {
        search: '',
        status: undefined,
        timeRange: [],
      },
      pagination: {
        current: 1,
        pageSize: 20,
        total: 0,
        showSizeChanger: true,
        showQuickJumper: true,
        pageSizeOptions: ['10', '20', '50', '100'],
        showTotal: (total) => `${this.$t('cmdb.ciType.onetermSync.totalRecords')}: ${total}`,
      },
      stats: {
        success: 0,
        failed: 0,
        skipped: 0,
      },
      columns: [
        {
          title: this.$t('cmdb.ciType.onetermSync.syncTime'),
          dataIndex: 'created_at',
          width: 180,
          scopedSlots: { customRender: 'time' },
          sorter: true,
        },
        {
          title: this.$t('cmdb.ciType.onetermSync.ciName'),
          dataIndex: 'ci_name',
          width: 180,
          scopedSlots: { customRender: 'ci_name' },
        },
        {
          title: this.$t('cmdb.ciType.onetermSync.status'),
          dataIndex: 'status',
          width: 120,
          scopedSlots: { customRender: 'status' },
        },
        {
          title: this.$t('cmdb.ciType.onetermSync.details'),
          dataIndex: 'details',
          ellipsis: true,
          scopedSlots: { customRender: 'details' },
        },
        {
          title: this.$t('operation'),
          width: 200,
          scopedSlots: { customRender: 'action' },
        },
      ],
    }
  },
  methods: {
    open() {
      this.visible = true
      this.loadLogData()
    },

    handleClose() {
      this.visible = false
      this.resetFilter()
    },

    resetFilter() {
      this.filterParams = {
        search: '',
        status: undefined,
        timeRange: [],
      }
      this.pagination.current = 1
    },

    async loadLogData() {
      // *
    },

    handleSearch() {
      this.pagination.current = 1
      this.loadLogData()
    },

    handleTableChange(pagination, filters, sorter) {
      this.pagination.current = pagination.current
      this.pagination.pageSize = pagination.pageSize
      this.loadLogData()
    },

    formatTime(time) {
      return moment(time).format('YYYY-MM-DD HH:mm:ss')
    },

    getOperationColor(operation) {
      const colorMap = {
        create: 'green',
        update: 'blue',
        delete: 'red',
        sync: 'purple',
      }
      return colorMap[operation] || 'default'
    },

    getOperationLabel(operation) {
      const labelMap = {
        create: this.$t('cmdb.ciType.onetermSync.create'),
        update: this.$t('cmdb.ciType.onetermSync.update'),
        delete: this.$t('cmdb.ciType.onetermSync.delete'),
        sync: this.$t('cmdb.ciType.onetermSync.sync'),
      }
      return labelMap[operation] || operation
    },

    getStatusBadge(status) {
      const badgeMap = {
        success: 'success',
        failed: 'error',
        skipped: 'default',
      }
      return badgeMap[status] || 'default'
    },

    getStatusLabel(status) {
      const labelMap = {
        success: this.$t('cmdb.ciType.onetermSync.success'),
        failed: this.$t('cmdb.ciType.onetermSync.failed'),
        skipped: this.$t('cmdb.ciType.onetermSync.skipped'),
      }
      return labelMap[status] || status
    },

    truncateText(text, maxLength) {
      if (!text) return '-'
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    },

    formatChanges(changes) {
      if (!changes) return '-'
      if (typeof changes === 'string') {
        try {
          return JSON.stringify(JSON.parse(changes), null, 2)
        } catch {
          return changes
        }
      }
      return JSON.stringify(changes, null, 2)
    },

    viewCI(ciId) {
      if (!ciId || !this.ciTypeId) return
      // 跳转到CI详情页
      window.open(`/cmdb/cidetail/${this.ciTypeId}/${ciId}`, '_blank')
    },

    viewDetails(record) {
      this.currentLog = record
      this.detailsModalVisible = true
    },

    async handleRetry() {
      // *
    },
  },
}
</script>

<style lang="less" scoped>
.sync-log-drawer {
  .filter-section {
    margin-bottom: 16px;
    padding: 16px;
    background: #fafafa;
    border-radius: 4px;
  }

  .details-cell {
    .success-msg {
      color: #52c41a;
    }

    .error-msg {
      color: #f5222d;
      cursor: pointer;
      width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
      display: block;

      .anticon {
        margin-right: 4px;
      }
    }

    .skipped-msg {
      color: #999;
    }
  }

  .stats-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 16px 24px;
    background: #fafafa;
    border-top: 1px solid #f0f0f0;
  }

  /deep/ .ant-table {
    margin-bottom: 60px;

    .ant-table-tbody > tr > td {
      padding: 12px 16px;
    }

    .ant-table-tbody > tr:hover > td {
      background: #f5f5f5;
    }
  }
}

.log-details {
  .details-content,
  .changes-content {
    margin: 0;
    padding: 12px;
    background: #f5f5f5;
    border-radius: 4px;
    font-size: 12px;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 300px;
    overflow-y: auto;
  }
}
</style>
