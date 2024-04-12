<template>
  <a-card :bordered="false" :bodyStyle="{ padding: '0' }">
    <a-tabs :activeKey="activeKey" @change="changeTab" class="ops-tab">
      <a-tab-pane key="1" :tab="$t('cmdb.ciType.attributes')">
        <AttributesTable ref="attributesTable" :CITypeId="CITypeId" :CITypeName="CITypeName"></AttributesTable>
      </a-tab-pane>
      <a-tab-pane key="2" :tab="$t('cmdb.ciType.relation')">
        <RelationTable :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
      </a-tab-pane>
      <a-tab-pane key="3" :tab="$t('cmdb.ciType.trigger')">
        <TriggerTable ref="triggerTable" :CITypeId="CITypeId"></TriggerTable>
      </a-tab-pane>
      <a-tab-pane key="4" :tab="$t('cmdb.ciType.attributeAD')">
        <AttrAD :CITypeId="CITypeId"></AttrAD>
      </a-tab-pane>
      <a-tab-pane key="5" :tab="$t('cmdb.ciType.relationAD')">
        <RelationAD :CITypeId="CITypeId"></RelationAD>
      </a-tab-pane>
      <a-tab-pane key="6" :tab="$t('cmdb.ciType.grant')">
        <GrantComp :CITypeId="CITypeId" resourceType="CIType" :resourceTypeName="CITypeName"></GrantComp>
        <div class="citype-detail-title">{{ $t('cmdb.components.relationGrant') }}</div>
        <RelationTable isInGrantComp :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
      </a-tab-pane>
    </a-tabs>
  </a-card>
</template>

<script>
import AttributesTable from './attributesTable'
import RelationTable from './relationTable'
import TriggerTable from './triggerTable.vue'
import AttrAD from './attrAD.vue'
import RelationAD from './relationAD.vue'
import GrantComp from '../../components/cmdbGrant/grantComp.vue'

export default {
  name: 'CITypeDetail',
  components: {
    AttributesTable,
    RelationTable,
    TriggerTable,
    AttrAD,
    RelationAD,
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
  methods: {
    changeTab(activeKey) {
      this.activeKey = activeKey
      this.$nextTick(() => {
        if (activeKey === '1') {
          this.$refs.attributesTable.getCITypeGroupData()
        }
        if (activeKey === '3') {
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
</style>
