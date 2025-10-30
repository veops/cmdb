<template>
  <div class="oneterm-sync-tab">
    <!-- Basic Configuration Block -->
    <a-card class="config-card" :bordered="false">
      <div slot="title" class="card-title">
        <a-icon type="setting" theme="filled" />
        <span>{{ $t('cmdb.ciType.onetermSync.basicConfig') }}</span>
      </div>

      <a-form-model
        ref="form"
        :model="syncConfig"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-model-item :label="$t('cmdb.ciType.onetermSync.enableSync')">
          <a-switch v-model="syncConfig.enabled" @change="handleEnableChange" />
          <div class="ant-form-explain">{{ $t('cmdb.ciType.onetermSync.enableSyncHint') }}</div>
        </a-form-model-item>

        <a-form-model-item :label="$t('cmdb.ciType.onetermSync.protocols')">
          <a-select
            v-model="syncConfig.protocols"
            mode="multiple"
            style="width: 400px"
            :placeholder="$t('cmdb.ciType.onetermSync.selectProtocols')"
          >
            <a-select-option
              v-for="protocol in protocols"
              :key="protocol.value"
              :value="protocol.value"
            >
              <ops-icon :type="protocol.icon" />
              {{ protocol.label }}
            </a-select-option>
          </a-select>
          <div class="ant-form-explain">{{ $t('cmdb.ciType.onetermSync.protocolsHint') }}</div>
        </a-form-model-item>

        <a-form-model-item :label="$t('cmdb.ciType.onetermSync.autoSync')">
          <a-switch v-model="syncConfig.auto_sync" />
          <div class="ant-form-explain">{{ $t('cmdb.ciType.onetermSync.autoSyncHint') }}</div>
        </a-form-model-item>
      </a-form-model>
    </a-card>

    <!-- Attribute Mapping Block -->
    <a-card class="config-card" :bordered="false">
      <div slot="title" class="card-title">
        <a-icon type="swap" />
        <span>{{ $t('cmdb.ciType.onetermSync.attributeMapping') }}</span>
      </div>

      <AttributeMappingTable
        :ciTypeId="CITypeId"
        :mappings="syncConfig.attribute_mapping"
        :syncStrategy="syncConfig.sync_strategy"
        @change="handleMappingChange"
      />
    </a-card>

    <!-- Advanced Config Block -->
    <a-card class="config-card" :bordered="false">
      <div slot="title" class="card-title">
        <a-icon type="tool" theme="filled" />
        <span>{{ $t('cmdb.ciType.onetermSync.advancedConfig') }}</span>
      </div>

      <AdvancedConfig
        :config="syncConfig"
        :ciTypeId="CITypeId"
        @change="handleAdvancedConfigChange"
      />
    </a-card>

    <!-- Sync Status Block -->
    <a-card
      class="config-card"
      :bordered="false"
    >
      <div slot="title" class="card-title">
        <a-icon type="dashboard" theme="filled" />
        <span>{{ $t('cmdb.ciType.onetermSync.syncStatus') }}</span>
      </div>

      <SyncStatus
        :ciTypeId="CITypeId"
        :stats="syncConfig.sync_stats"
        @refresh="loadSyncStats"
      />
    </a-card>

    <!-- Footer Actions -->
    <div class="footer-actions">
      <a-button @click="handleCancel" style="margin-right: 12px;">
        {{ $t('cancel') }}
      </a-button>
      <a-button disabled type="primary" @click="handleSave">
        {{ $t('save') }}
        <a-tooltip placement="topRight" :title="$t('cmdb.ciType.onetermSync.unableUseTip')">
          <a-icon type="info-circle" style="pointer-events: auto;" />
        </a-tooltip>
      </a-button>
    </div>

    <!-- Sync Log Drawer -->
    <SyncLogDrawer ref="syncLogDrawer" :ciTypeId="CITypeId" />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import AttributeMappingTable from './attributeMappingTable.vue'
import AdvancedConfig from './advancedConfig.vue'
import SyncStatus from './syncStatus.vue'
import SyncLogDrawer from './syncLogDrawer.vue'
import { DEFAULT_ATTR_MAPPING } from './constants'

export default {
  name: 'OnetermSyncTab',
  components: {
    AttributeMappingTable,
    AdvancedConfig,
    SyncStatus,
    SyncLogDrawer,
  },
  props: {
    CITypeId: {
      type: Number,
      required: true,
    },
    CITypeName: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      syncConfig: {
        enabled: false,
        protocols: ['ssh'],
        auto_sync: true,
        attribute_mapping: _.cloneDeep(DEFAULT_ATTR_MAPPING),
        asset_name_template: '',
        folder_rule: {
          type: 'fixed',
          path: 'Default',
        },
        sync_stats: {
          total: 0,
          synced: 0,
          failed: 0,
        },
      },
      isSavedConfig: false,
      originalConfig: null,
      protocols: [
        { value: 'ssh', label: 'SSH', icon: 'a-oneterm-ssh2' },
        { value: 'rdp', label: 'RDP', icon: 'a-oneterm-ssh1' },
        { value: 'mysql', label: 'MySQL', icon: 'oneterm-mysql' },
        { value: 'redis', label: 'Redis', icon: 'oneterm-redis' },
        { value: 'postgresql', label: 'PostgreSQL', icon: 'a-postgreSQL1' },
        { value: 'telnet', label: 'Telnet', icon: 'a-telnet1' },
        { value: 'vnc', label: 'VNC', icon: 'oneterm-rdp' },
      ],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  mounted() {
    this.loadConfig()
    this.loadSyncStats()
  },
  methods: {
    async loadConfig() {
      // *
    },

    handleEnableChange(enabled) {
      if (enabled && !this.syncConfig.attribute_mapping.length) {
        this.syncConfig.attribute_mapping = _.cloneDeep(DEFAULT_ATTR_MAPPING)
      }
    },

    handleMappingChange(mappings) {
      this.syncConfig.attribute_mapping = mappings
    },

    handleAdvancedConfigChange(config) {
      // Deep merge for nested objects like folder_rule
      if (config.folder_rule) {
        this.syncConfig.folder_rule = { ...this.syncConfig.folder_rule, ...config.folder_rule }
      }
      if (config.asset_name_template !== undefined) {
        this.syncConfig.asset_name_template = config.asset_name_template
      }
    },

    async handleSave() {
      // Validate configuration
      const requiredFields = this.syncConfig.attribute_mapping.filter((m) => m.required)
      const missingFields = requiredFields.filter((m) => !m.cmdb_attr)
      if (missingFields.length) {
        this.$message.warning(this.$t('cmdb.ciType.onetermSync.missingRequiredMapping'))
        return
      }

      // Check for duplicate mappings
      const attrCounts = {}
      this.syncConfig.attribute_mapping.forEach((m) => {
        if (m.cmdb_attr) {
          attrCounts[m.cmdb_attr] = (attrCounts[m.cmdb_attr] || 0) + 1
        }
      })
      const duplicates = Object.keys(attrCounts).filter((attr) => attrCounts[attr] > 1)
      if (duplicates.length) {
        this.$message.warning(
          this.$t('cmdb.ciType.onetermSync.duplicateMapping', { attr: duplicates[0] })
        )
        return
      }

      if (!this.syncConfig.asset_name_template) {
        this.$message.warning(this.$t('cmdb.ciType.onetermSync.assetNameTemplateRequired'))
        return
      }
      console.log('syncConfig', this.syncConfig)
    },

    handleCancel() {
      if (this.originalConfig) {
        this.syncConfig = JSON.parse(JSON.stringify(this.originalConfig))
      }
      this.$message.info(this.$t('cmdb.ciType.onetermSync.canceledChanges'))
    },

    async loadSyncStats() {
      // *
    },

    openSyncLog() {
      this.$refs.syncLogDrawer.open()
    },
  },
}
</script>

<style lang="less" scoped>
.oneterm-sync-tab {
  padding: 0;
  max-height: calc(100vh - 130px);
  overflow-y: auto;

  .config-card {
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

    /deep/ .ant-card-head-title {
      padding: 12px 0;
    }

    .card-title {
      display: flex;
      align-items: center;
      font-size: 15px;
      font-weight: 500;
      color: @text-color_2;

      .anticon,
      .ops-icon {
        margin-right: 8px;
        font-size: 16px;
        color: @primary-color;
      }
    }

    /deep/ .ant-card-head {
      border-bottom: 1px solid #f0f0f0;
      background: #fafafa;
    }

    /deep/ .ant-card-body {
      padding: 24px;
    }
  }

  .footer-actions {
    position: sticky;
    bottom: 0;
    padding: 16px 24px;
    background: #fff;
    border-top: 1px solid #f0f0f0;
    text-align: right;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
    z-index: 10;
  }
}
</style>
