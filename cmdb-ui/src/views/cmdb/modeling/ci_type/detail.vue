<template>
  <a-card :bordered="false">

    <a-tabs defaultActiveKey="1">
      <a-tab-pane key="1" :tab="$t('ciType.typeAttribute')">

        <AttributesTable></AttributesTable>

      </a-tab-pane>
      <a-tab-pane forceRender key="2" :tab="$t('ciType.typeRelation')">
        <RelationTable :CITypeId="CITypeId" :CITypeName="CITypeName"></RelationTable>

      </a-tab-pane>

      <a-tab-pane forceRender key="3" :tab="$t('ciType.requiredCheck')">
        <CheckTable></CheckTable>

      </a-tab-pane>

      <a-tab-pane forceRender key="4" :tab="$t('ciType.defaultShowAttribute')">
        <DefaultShowTable></DefaultShowTable>

      </a-tab-pane>

      <a-tab-pane forceRender key="5" :tab="$t('ciType.attributeGroup')">
        <Group></Group>

      </a-tab-pane>
    </a-tabs>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import AttributesTable from './attributesTable'
import RelationTable from './relationTable'
import CheckTable from './checkTable'
import DefaultShowTable from './defaultShowTable'
import Group from './group'

export default {
  name: 'CITypeDetail',
  components: {
    STable,
    AttributesTable,
    RelationTable,
    CheckTable,
    DefaultShowTable,
    Group
  },
  data () {
    return {
      CITypeId: this.$route.params.CITypeId,
      CITypeName: this.$route.params.CITypeName
    }
  },
  beforeCreate () {
  },
  mounted () {

  },
  methods: {
  },
  watch: {}

}
</script>

<style lang="less" scoped>
  .search {
    margin-bottom: 54px;
  }

  .fold {
    width: calc(100% - 216px);
    display: inline-block
  }

  .operator {
    margin-bottom: 18px;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
