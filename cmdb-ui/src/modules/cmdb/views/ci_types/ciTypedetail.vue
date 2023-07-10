<template>
  <a-card :bordered="false" :bodyStyle="{ padding: '0' }">
    <a-tabs :activeKey="activeKey" @change="changeTab" class="ops-tab" type="card">
      <a-tab-pane key="1" tab="模型属性">
        <AttributesTable ref="attributesTable" :CITypeId="CITypeId" :CITypeName="CITypeName"></AttributesTable>
      </a-tab-pane>
      <a-tab-pane forceRender key="2" tab="模型关联">
        <RelationTable :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>
      </a-tab-pane>
      <a-tab-pane key="3" tab="触发器">
        <TriggerTable ref="triggerTable" :CITypeId="CITypeId"></TriggerTable>
      </a-tab-pane>
      <a-tab-pane key="4" tab="属性自动发现">
        <AttrAD :CITypeId="CITypeId"></AttrAD>
      </a-tab-pane>
      <a-tab-pane key="5" tab="关系自动发现">
        <RelationAD :CITypeId="CITypeId"></RelationAD>
      </a-tab-pane>
      <a-tab-pane key="6" tab="权限设置">
        <GrantComp :CITypeId="CITypeId" resourceType="CIType" :resourceTypeName="CITypeName"></GrantComp>
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

<style lang="less" scoped></style>
