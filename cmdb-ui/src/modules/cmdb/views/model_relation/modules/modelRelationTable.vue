<template>
  <div>
    <vxe-table
      ref="xTable"
      stripe
      class="ops-stripe-table"
      show-header-overflow
      show-overflow
      resizable
      :height="`${windowHeight - 160}px`"
      :data="tableData"
      :sort-config="{ defaultSort: { field: 'created_at', order: 'desc' } }"
    >
      <vxe-column field="created_at" :title="$t('created_at')" sortable width="159px"></vxe-column>
      <vxe-column field="parent.alias" :title="$t('cmdb.ciType.sourceCIType')"></vxe-column>
      <vxe-column
        field="relation_type_id"
        :title="$t('cmdb.custom_dashboard.relation')"
        :filters="[{ data: '' }]"
        :filter-multiple="false"
      >
        <template #default="{ row }">
          <a-tag color="cyan">
            {{ row.relation_type.name }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="child.alias" :title="$t('cmdb.ciType.dstCIType')"></vxe-column>
      <vxe-column field="constraint" :title="$t('cmdb.ciType.relationConstraint')"></vxe-column>
      <vxe-column field="authorization" :title="$t('operation')" width="89px">
        <template #default="{ row }">
          <a-space>
            <a @click="handleOpenGrant(row)"><a-icon type="user-add"/></a>
            <a-popconfirm :title="$t('cmdb.ciType.confirmDelete2')" @confirm="deleteRelation(row)">
              <a :style="{ color: 'red' }"><ops-icon type="icon-xianxing-delete"/></a>
            </a-popconfirm>
          </a-space>
        </template>
      </vxe-column>
    </vxe-table>
    <CMDBGrant ref="cmdbGrant" resourceType="CITypeRelation" app_id="cmdb" />
  </div>
</template>

<script>
import { getCITypeRelations, deleteRelation } from '@/modules/cmdb/api/CITypeRelation'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import CMDBGrant from '../../../components/cmdbGrant'

export default {
  data() {
    return {
      drawerVisible: false,
      tableData: [],
      relationTypeList: null,
    }
  },
  components: {
    CMDBGrant,
  },
  created() {
    this.refresh()
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    constraintMap() {
      return {
        '0': this.$t('cmdb.ciType.one2Many'),
        '1': this.$t('cmdb.ciType.one2One'),
        '2': this.$t('cmdb.ciType.many2Many'),
      }
    },
  },
  methods: {
    async refresh() {
      await this.getRelationTypes()
      await this.getMainData()
    },
    async getMainData() {
      const res = await getCITypeRelations()
      res.forEach((item) => {
        item.constraint = this.handleConstraint(item.constraint)
      })
      this.tableData = res
    },
    // 获取关系
    async getRelationTypes() {
      const res = await getRelationTypes()
      this.relationTypeList = res.map((item) => ({ value: item.id, label: item.name }))
      const $table = this.$refs.xTable
      if ($table) {
        const nameColumn = $table.getColumnByField('relation_type_id')
        if (nameColumn) {
          $table.setFilter(nameColumn, this.relationTypeList)
        }
      }
    },
    // 转换关联关系
    handleConstraint(constraintId) {
      return this.constraintMap[constraintId]
    },
    handleOpenGrant(record) {
      this.$refs.cmdbGrant.open({
        name: `${record.parent.name} -> ${record.child.name}`,
        typeRelationIds: [record.parent_id, record.child_id],
        cmdbGrantType: 'type_relation',
      })
    },
    deleteRelation(row) {
      deleteRelation(row.parent_id, row.child_id).then((res) => {
        this.$message.success(this.$t('deleteSuccess'))
        this.getRelationTypes()
        this.refresh()
      })
    },
  },
}
</script>

<style></style>
