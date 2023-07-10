<template>
  <div>
    <vxe-table
      stripe
      class="ops-stripe-table"
      show-header-overflow
      show-overflow
      resizable
      :max-height="`${windowHeight - 183}px`"
      :data="tableData"
      :sort-config="{ defaultSort: { field: 'created_at', order: 'desc' } }"
    >
      <vxe-column field="created_at" title="创建时间" sortable width="159px"></vxe-column>
      <vxe-column field="parent.alias" title="源模型"></vxe-column>
      <vxe-column
        field="relation_type_id"
        title="关系"
        :filters="[{ data: '' }]"
        :filter-method="filterRelationMethod"
        :filter-recover-method="filterRelationRecoverMethod"
      >
        <template #filter="{ $panel, column }">
          <template v-for="(option, index) in column.filters">
            <input
              type="type"
              :key="index"
              v-model="option.data"
              @input="$panel.changeOption($event, !!option.data, option)"
              @keyup.enter="$panel.confirmFilter()"
              placeholder="按回车确认筛选"
            />
          </template>
        </template>
        <template #default="{ row }">
          <a-tag color="cyan">
            {{ row.relation_type.name }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="child.alias" title="目标模型"></vxe-column>
      <vxe-column field="constraint" title="关联约束"></vxe-column>
      <vxe-column field="authorization" title="授权" width="89px">
        <template #default="{ row }">
          <a @click="handleOpenGrant(row)"><a-icon type="user-add"/></a>
        </template>
      </vxe-column>
    </vxe-table>
    <CMDBGrant ref="cmdbGrant" resourceType="CITypeRelation" app_id="cmdb" />
  </div>
</template>

<script>
import { getCITypeRelations } from '@/modules/cmdb/api/CITypeRelation'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import CMDBGrant from '../../../components/cmdbGrant'

export default {
  data() {
    return {
      drawerVisible: false,
      tableData: [],
      relationTypeList: null,
      constraintMap: {
        '0': '一对多',
        '1': '一对一',
        '2': '多对多',
      },
    }
  },
  components: {
    CMDBGrant,
  },
  async created() {
    await this.getRelationTypes()
    await this.getMainData()
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  methods: {
    async getMainData() {
      const res = await getCITypeRelations()
      res.forEach((item) => {
        item.constraint = this.handleConstraint(item.constraint)
      })
      this.tableData = res
      console.log('MainData', res)
    },
    // 获取关系
    async getRelationTypes() {
      const res = await getRelationTypes()
      const relationTypeMap = new Map()
      res.forEach((item) => {
        relationTypeMap.set(item.id, item.name)
      })
      this.relationTypeList = relationTypeMap
      console.log('relationTypeList', this.relationTypeList)
    },
    // 转换关联关系
    handleConstraint(constraintId) {
      return this.constraintMap[constraintId]
    },
    handleOpenGrant(record) {
      console.log('record', record)
      console.log(`${record.parent.name} -> ${record.child.name}`)
      // this.$refs.grantDrawer.open({ name: `${record.parent.name} -> ${record.child.name}` })
      this.$refs.cmdbGrant.open({
        name: `${record.parent.name} -> ${record.child.name}`,
        typeRelationIds: [record.parent_id, record.child_id],
        cmdbGrantType: 'type_relation',
      })
    },
    filterRelationMethod({ option, row }) {
      return row.relation_type.name.includes(String(option.data))
    },
    filterRelationRecoverMethod({ option }) {
      option.data = ''
    },
    refresh() {
      this.getMainData()
    },
  },
}
</script>

<style></style>
