<template>
  <div class="model-relation-table">
    <vxe-table
      ref="xTable"
      stripe
      class="ops-stripe-table"
      show-header-overflow
      show-overflow
      resizable
      :scroll-y="{enabled: false}"
      :height="`${windowHeight - 160}px`"
      :data="tableData"
      :sort-config="{ defaultSort: { field: 'created_at', order: 'desc' } }"
      :edit-config="{ trigger: 'dblclick', mode: 'cell', showIcon: false }"
      @edit-closed="handleEditClose"
      @edit-actived="handleEditActived"
    >
      <vxe-column field="created_at" :title="$t('created_at')" sortable width="170"></vxe-column>
      <vxe-column field="parent.alias" :title="$t('cmdb.ciType.sourceCIType')"></vxe-column>
      <vxe-column
        field="relation_type_id"
        :title="$t('cmdb.custom_dashboard.relation')"
        :filters="relationTypeList"
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
      <vxe-column :width="300" field="attributeAssociation" :edit-render="{}">
        <template #header>
          <span>
            <a-tooltip>
              <template #title>
                <div>{{ $t('cmdb.ciType.attributeAssociationTip1') }}</div>
                <div>{{ $t('cmdb.ciType.attributeAssociationTip7') }}</div>
                <div>{{ $t('cmdb.ciType.attributeAssociationTip8') }}</div>
                <div>{{ $t('cmdb.ciType.attributeAssociationTip9') }}</div>
              </template>
              <a><a-icon type="question-circle"/></a>
            </a-tooltip>
            {{ $t('cmdb.ciType.attributeAssociation') }}
            <span :style="{ fontSize: '10px', fontWeight: 'normal' }" class="text-color-4">{{
              $t('cmdb.ciType.attributeAssociationTip2')
            }}</span>
          </span>
        </template>
        <template #default="{row}">
          <template
            v-for="item in row.parentAndChildAttrList"
          >
            <div
              :key="item.id"
              v-if="item.parentAttrId && item.childAttrId"
            >
              {{ getAttrNameById(type2attributes[row.parent_id], item.parentAttrId) }}=>
              {{ getAttrNameById(type2attributes[row.child_id], item.childAttrId) }}
            </div>
          </template>
        </template>
        <template #edit="{ row }">
          <div
            v-for="item in tableAttrList"
            :key="item.id"
            class="table-attribute-row"
          >
            <a-select
              allowClear
              size="small"
              v-model="item.parentAttrId"
              :getPopupContainer="(trigger) => trigger.parentNode"
              :style="{ width: '100px' }"
              show-search
              optionFilterProp="title"
            >
              <a-select-option
                v-for="attr in filterAttributes(row, item.childAttrId, 'parent')"
                :key="attr.id"
                :value="attr.id"
                :title="attr.alias || attr.name"
              >
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
            <span class="table-attribute-row-link">=></span>
            <a-select
              allowClear
              size="small"
              v-model="item.childAttrId"
              :getPopupContainer="(trigger) => trigger.parentNode"
              :style="{ width: '100px' }"
              show-search
              optionFilterProp="title"
            >
              <a-select-option
                v-for="attr in filterAttributes(row, item.parentAttrId, 'child')"
                :key="attr.id"
                :value="attr.id"
                :title="attr.alias || attr.name"
              >
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
            <a
              class="table-attribute-row-action"
              @click="removeTableAttr(item.id)"
            >
              <a-icon type="minus-circle" />
            </a>
            <a
              class="table-attribute-row-action"
              @click="addTableAttr"
            >
              <a-icon type="plus-circle" />
            </a>
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
import { v4 as uuidv4 } from 'uuid'
import { getCITypeRelations, deleteRelation, createRelation } from '@/modules/cmdb/api/CITypeRelation'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import CMDBGrant from '../../../components/cmdbGrant'

export default {
  data() {
    return {
      drawerVisible: false,
      tableData: [],
      relationTypeList: [],
      type2attributes: {},
      tableAttrList: [],
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
      this.tableData = relations.map((item) => {
        const parentAndChildAttrList = this.handleAttrList(item)
        return {
          ...item,
          parentAndChildAttrList
        }
      })
      this.type2attributes = type2attributes
    },

    handleAttrList(data) {
      const length = Math.min(data?.parent_attr_ids?.length || 0, data.child_attr_ids?.length || 0)
      const parentAndChildAttrList = []
      for (let i = 0; i < length; i++) {
        parentAndChildAttrList.push({
          id: uuidv4(),
          parentAttrId: data?.parent_attr_ids?.[i] ?? '',
          childAttrId: data?.child_attr_ids?.[i] ?? ''
        })
      }
      return parentAndChildAttrList
    },

    // 获取关系
    async getRelationTypes() {
      const res = await getRelationTypes()
      this.relationTypeList = res.map((item) => ({ value: item.id, label: item.name }))
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
      const tableAttrList = []

      const length = Math.min(row?.parent_attr_ids?.length || 0, row.child_attr_ids?.length || 0)
      if (length) {
        for (let i = 0; i < length; i++) {
          tableAttrList.push({
            id: uuidv4(),
            parentAttrId: row?.parent_attr_ids?.[i] ?? undefined,
            childAttrId: row?.child_attr_ids?.[i] ?? undefined
          })
        }
      } else {
        tableAttrList.push({
          id: uuidv4(),
          parentAttrId: undefined,
          childAttrId: undefined
        })
      }
      console.log('handleEditActived', tableAttrList)
      this.$set(this, 'tableAttrList', tableAttrList)
    },

    /**
     * 校验属性列表
     * @param {*} attrList
     */
     handleValidateAttrList(attrList) {
      const parent_attr_ids = []
      const child_attr_ids = []
      attrList.map((attr) => {
        if (attr.parentAttrId) {
          parent_attr_ids.push(attr.parentAttrId)
        }
        if (attr.childAttrId) {
          child_attr_ids.push(attr.childAttrId)
        }
      })

      if (parent_attr_ids.length !== child_attr_ids.length) {
        this.$message.warning(this.$t('cmdb.ciType.attributeAssociationTip3'))
        return {
          validate: false
        }
      }

      return {
        validate: true,
        parent_attr_ids,
        child_attr_ids
      }
    },

    async handleEditClose({ row }) {
      const { parent_id, child_id, constraint, relation_type_id } = row

      const {
        parent_attr_ids,
        child_attr_ids,
        validate
      } = this.handleValidateAttrList(this.tableAttrList)
      if (!validate) {
        return
      }

      await createRelation(parent_id, child_id, {
        relation_type_id,
        constraint,
        parent_attr_ids,
        child_attr_ids,
      }).finally(() => {
        this.getMainData()
      })
    },
    getAttrNameById(attributes, id) {
      const _find = attributes.find((attr) => attr.id === id)
      return _find?.alias ?? _find?.name ?? id
    },

    filterAttributes(row, relationAttrId, type) {
      const { parent_id, child_id, constraint } = row
      const currentAttrs = this.type2attributes?.[child_id] || []

      const relationAttrs = this.type2attributes?.[parent_id] || []
      const relationAttr = relationAttrs.find((attr) => attr.id === relationAttrId)

      // filter password/json/longText/bool/reference
      let filterAttrs = currentAttrs.filter((attr) => {
        if (attr.value_type === '2' && !attr.is_index) {
          return false
        }

        return !attr.is_password && attr.value_type !== '6' && !attr.is_bool && !attr.is_reference
      })

      if (relationAttr) {
        filterAttrs = filterAttrs.filter((attr) => attr.value_type === relationAttr?.value_type)
      }

      const constraintValue = Number(constraint)
      if (
        (constraintValue === 0 && type === 'child') ||
        constraintValue === 1 ||
        (constraintValue === 2 && relationAttr?.is_list)
      ) {
        return filterAttrs.filter((attr) => !attr.is_list)
      }

      return filterAttrs
    },

    addTableAttr() {
      this.tableAttrList.push({
        id: uuidv4(),
        parentAttrId: undefined,
        childAttrId: undefined
      })
    },
    removeTableAttr(id) {
      if (this.tableAttrList.length <= 1) {
        this.$message.error(this.$t('cmdb.ciType.attributeAssociationTip6'))
        return
      }
      const index = this.tableAttrList.findIndex((item) => item.id === id)
      if (index !== -1) {
        this.tableAttrList.splice(index, 1)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.relation-table {
  /deep/ .vxe-cell {
    max-height: max-content !important;
  }
}
.table-attribute-row {
  display: inline-flex;
  align-items: center;
  margin-top: 5px;

  &:last-child {
    margin-bottom: 5px;
  }

  &-link {
    margin: 0 5px;
  }

  &-action {
    margin-left: 5px;
  }

  /deep/ .ant-select-selection {
    box-shadow: none;
  }
}
</style>
