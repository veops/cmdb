<template>
  <a-card :bordered="false" :bodyStyle="{ padding: '0' }">
    <a-tabs :activeKey="activeKey" @change="changeTab" class="ops-tab">
      <a-tab-pane key="1" :tab="$t('cmdb.ciType.attributes')">
        <AttributesTable ref="attributesTable" :CITypeId="CITypeId" :CITypeName="CITypeName"></AttributesTable>
      </a-tab-pane>
      <a-tab-pane key="2" :tab="$t('cmdb.ciType.relation')">
        <RelationTable v-if="activeKey === '2'" :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
      </a-tab-pane>
      <a-tab-pane key="3" :tab="$t('cmdb.ciType.autoDiscoveryTab')">
        <ADTab v-if="activeKey === '3'" :CITypeId="CITypeId"></ADTab>
      </a-tab-pane>
      <a-tab-pane key="5" :tab="$t('cmdb.ciType.trigger')">
        <TriggerTable ref="triggerTable" :CITypeId="CITypeId"></TriggerTable>
      </a-tab-pane>
      <a-tab-pane key="oneterm">
        <template #tab>
          <div class="oneterm-sync-tab-title">
            <span>{{ $t('cmdb.ciType.onetermSyncTab') }}</span>
            <span class="oneterm-sync-tab-title-pro">Pro</span>
          </div>
        </template>
        <OnetermSyncTab v-if="activeKey === 'oneterm'" :CITypeId="CITypeId" :CITypeName="CITypeName"></OnetermSyncTab>
      </a-tab-pane>
      <a-tab-pane key="6" :tab="$t('cmdb.ciType.grant')">
        <div class="grant-config-wrap" :style="{ maxHeight: `${windowHeight - 150}px` }" v-if="activeKey === '6'">
          <GrantComp :CITypeId="CITypeId" resourceType="CIType" :resourceTypeName="CITypeName"></GrantComp>
          <div class="citype-detail-title">{{ $t('cmdb.components.relationGrant') }}</div>
          <RelationTable isInGrantComp :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
        </div>
      </a-tab-pane>

      <a-button
        slot="tabBarExtraContent"
        type="primary"
        ghost
        size="small"
        class="ops-button-ghost ops-tab-button"
        @click="jumpResourceView"
      >
        <ops-icon type="ops-cmdb-resource" />
        {{ $t('cmdb.menu.ciTable') }}
      </a-button>
    </a-tabs>
  </a-card>
</template>

<script>
import { mapState } from 'vuex'
import AttributesTable from './attributesTable'
import RelationTable from './relationTable'
import TriggerTable from './triggerTable.vue'
import ADTab from './adTab.vue'
import GrantComp from '../../components/cmdbGrant/grantComp.vue'
import OnetermSyncTab from './onetermSync/index.vue'

const ACTIVE_KEY_STORAGE_KEY = 'ops_model_config_tab_key'

export default {
  name: 'CITypeDetail',
  components: {
    AttributesTable,
    RelationTable,
    TriggerTable,
    ADTab,
    GrantComp,
    OnetermSyncTab
  },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
    CITypeName: {
      type: String,
      default: '',
    },
    preferenceData: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      activeKey: localStorage.getItem(ACTIVE_KEY_STORAGE_KEY) || '1',
    }
  },
  beforeCreate() {},
  mounted() {
    this.$nextTick(() => {
      switch (this.activeKey) {
        case '5':
          this.$refs.triggerTable.getTableData()
          break
        default:
          break
      }
    })
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  methods: {
    changeTab(activeKey) {
      this.activeKey = activeKey
      localStorage.setItem(ACTIVE_KEY_STORAGE_KEY, activeKey)
      this.$nextTick(() => {
        switch (activeKey) {
          case '1':
            this.$refs.attributesTable.getCITypeGroupData()
            break
          case '5':
            this.$refs.triggerTable.getTableData()
            break
          default:
            break
        }
      })
    },
    jumpResourceView() {
      const isSub = this?.preferenceData?.type_ids?.includes(this.CITypeId)

      if (!isSub) {
        this.$message.error(this.$t('cmdb.ciType.resourceViewTip'))
        return
      }
      localStorage.setItem('ops_ci_typeid', this.CITypeId)
      window.open('/cmdb/instances/types', '_blank')
    }
  },
}
</script>

<style lang="less" scoped>

.citype-detail-title {
  border-left: 4px solid @primary-color;
  padding-left: 10px;
  margin-left: 20px;
  margin-bottom: 10px;
}
.grant-config-wrap {
  overflow: auto;
}

.ops-tab.ant-tabs {
  /deep/ .ant-tabs-bar {
    .ant-tabs-tab:hover {
      color: @primary-color;
    }
  }

  .oneterm-sync-tab-title {
    display: flex;
    align-items: center;
    column-gap: 4px;

    &-pro {
      background-color: #E1EFFF;
      color: #2f54eb;
      font-size: 12px;
      font-weight: 400;
      padding: 0 3px;
    }
  }

  .ops-tab-button {
    margin: 0px 12px;
  }
}
</style>
