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
      :edit-config="{ trigger: 'dblclick', mode: 'cell', showIcon: false }"
      @edit-closed="handleEditClose"
      @edit-actived="handleEditActived"
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
      <vxe-column field="constraint" :title="$t('cmdb.ciType.relationConstraint')">
        <template #default="{row}">
          {{ handleConstraint(row.constraint) }}
        </template>
      </vxe-column>
      <vxe-column :width="250" field="attributeAssociation" :edit-render="{}">
        <template #header>
          <span>
            <a-tooltip :title="$t('cmdb.ciType.attributeAssociationTip1')">
              <a><a-icon type="question-circle"/></a>
            </a-tooltip>
            {{ $t('cmdb.ciType.attributeAssociation') }}
            <span :style="{ fontSize: '10px', fontWeight: 'normal' }" class="text-color-4">{{
              $t('cmdb.ciType.attributeAssociationTip2')
            }}</span>
          </span>
        </template>
        <template #default="{row}">
          <span
            v-if="row.parent_attr_id && row.child_attr_id"
          >{{ getAttrNameById(type2attributes[row.parent_id], row.parent_attr_id) }}=>
            {{ getAttrNameById(type2attributes[row.child_id], row.child_attr_id) }}</span
          >
        </template>
        <template #edit="{ row }">
          <div style="display:inline-flex;align-items:center;">
            <a-select
              allowClear
              size="small"
              v-model="parent_attr_id"
              :getPopupContainer="(trigger) => trigger.parentNode"
              :style="{ width: '100px' }"
            >
              <a-select-option v-for="attr in filterAttributes(type2attributes[row.parent_id])" :key="attr.id">
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
            =>
            <a-select
              allowClear
              size="small"
              v-model="child_attr_id"
              :getPopupContainer="(trigger) => trigger.parentNode"
              :style="{ width: '100px' }"
            >
              <a-select-option v-for="attr in filterAttributes(type2attributes[row.child_id])" :key="attr.id">
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
          </div>
        </template>
      </vxe-column>
      <vxe-column field="operation" :title="$t('operation')" width="89px">
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
import { getCITypeRelations, deleteRelation, createRelation } from '@/modules/cmdb/api/CITypeRelation'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import CMDBGrant from '../../../components/cmdbGrant'

export default {
  data() {
    return {
      drawerVisible: false,
      tableData: [],
      relationTypeList: null,
      type2attributes: {},
      parent_attr_id: undefined,
      child_attr_id: undefined,
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
      const { relations, type2attributes } = await getCITypeRelations()
      this.tableData = relations
      this.type2attributes = type2attributes
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
    handleEditActived({ row }) {
      this.parent_attr_id = row?.parent_attr_id ?? undefined
      this.child_attr_id = row?.child_attr_id ?? undefined
    },
    async handleEditClose({ row }) {
      const { parent_id, child_id, constraint, relation_type_id } = row
      const { parent_attr_id = undefined, child_attr_id = undefined } = this
      if ((!parent_attr_id && child_attr_id) || (parent_attr_id && !child_attr_id)) {
        this.$message.warning(this.$t('cmdb.ciType.attributeAssociationTip3'))
        return
      }
      await createRelation(parent_id, child_id, {
        relation_type_id,
        constraint,
        parent_attr_id,
        child_attr_id,
      }).finally(() => {
        this.getMainData()
      })
    },
    getAttrNameById(attributes, id) {
      const _find = attributes.find((attr) => attr.id === id)
      return _find?.alias ?? _find?.name ?? id
    },
    filterAttributes(attributes) {
      // filter password/json/is_list
      return attributes.filter((attr) => !attr.is_password && !attr.is_list && attr.value_type !== '6')
    },
  },
}
</script>

<style></style>
