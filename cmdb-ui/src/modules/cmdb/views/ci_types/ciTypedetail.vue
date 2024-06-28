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
      <a-tab-pane key="6" :tab="$t('cmdb.ciType.grant')">
        <div class="grant-config-wrap" :style="{ maxHeight: `${windowHeight - 150}px` }" v-if="activeKey === '6'">
          <GrantComp :CITypeId="CITypeId" resourceType="CIType" :resourceTypeName="CITypeName"></GrantComp>
          <div class="citype-detail-title">{{ $t('cmdb.components.relationGrant') }}</div>
          <RelationTable isInGrantComp :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
        </div>
      </a-tab-pane>
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

export default {
  name: 'CITypeDetail',
  components: {
    AttributesTable,
    RelationTable,
    TriggerTable,
    ADTab,
    GrantComp,
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
  },
  data() {
    return {
      activeKey: '1',
    }
  },
  beforeCreate() {},
  mounted() {},
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  methods: {
    changeTab(activeKey) {
      this.activeKey = activeKey
      this.$nextTick(() => {
        if (activeKey === '1') {
          this.$refs.attributesTable.getCITypeGroupData()
        }
        if (activeKey === '5') {
          this.$refs.triggerTable.getTableData()
        }
      })
    },
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
</style>
