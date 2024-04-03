<template>
  <div :style="{ padding: '0 20px 20px' }">
    <a-button
      v-if="!isInGrantComp"
      style="margin-bottom: 10px"
      @click="handleCreate"
      type="primary"
      size="small"
      class="ops-button-primary"
      icon="plus"
    >{{ $t('cmdb.ciType.addRelation') }}</a-button
    >
    <vxe-table
      stripe
      :data="tableData"
      size="small"
      show-overflow
      show-header-overflow
      highlight-hover-row
      keep-source
      :height="windowHeight - 190"
      class="ops-stripe-table"
      :row-class-name="rowClass"
      :edit-config="{ trigger: 'dblclick', mode: 'cell', showIcon: false }"
      resizable
      @edit-closed="handleEditClose"
      @edit-actived="handleEditActived"
    >
      <vxe-column field="source_ci_type_name" :title="$t('cmdb.ciType.sourceCIType')"></vxe-column>
      <vxe-column field="relation_type" :title="$t('cmdb.ciType.relationType')">
        <template #default="{row}">
          <span style="color:#2f54eb" v-if="row.isParent">{{ $t('cmdb.ciType.isParent') }}</span>
          {{ row.relation_type }}
        </template>
      </vxe-column>
      <vxe-column field="alias" :title="$t('cmdb.ciType.dstCIType')"></vxe-column>
      <vxe-column field="constraint" :title="$t('cmdb.ciType.relationConstraint')">
        <template #default="{row}">
          <span v-if="row.isParent && constraintMap[row.constraint]">{{
            constraintMap[row.constraint]
              .split('')
              .reverse()
              .join('')
          }}</span>
          <span v-else>{{ constraintMap[row.constraint] }}</span>
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
          >{{ getAttrNameById(row.isParent ? row.attributes : attributes, row.parent_attr_id) }}=>
            {{ getAttrNameById(row.isParent ? attributes : row.attributes, row.child_attr_id) }}</span
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
              <a-select-option
                v-for="attr in filterAttributes(row.isParent ? row.attributes : attributes)"
                :key="attr.id"
              >
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
              <a-select-option
                v-for="attr in filterAttributes(row.isParent ? attributes : row.attributes)"
                :key="attr.id"
              >
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
          </div>
        </template>
      </vxe-column>
      <vxe-column field="operation" :title="$t('operation')" width="100">
        <template #default="{row}">
          <a-space v-if="!row.isParent && row.source_ci_type_id">
            <a @click="handleOpenGrant(row)"><a-icon type="user-add"/></a>
            <a-popconfirm v-if="!isInGrantComp" :title="$t('cmdb.ciType.confirmDelete2')" @confirm="handleDelete(row)">
              <a style="color: red;"><a-icon type="delete"/></a>
            </a-popconfirm>
          </a-space>
        </template>
      </vxe-column>
      <template #empty>
        <div>
          <img :style="{ width: '100px' }" :src="require('@/assets/data_empty.png')" />
          <div>{{ $t('noData') }}</div>
        </div>
      </template>
    </vxe-table>
    <a-modal
      :closable="false"
      :title="drawerTitle"
      :visible="visible"
      @cancel="onClose"
      @ok="handleSubmit"
      width="700px"
    >
      <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
        <a-form-item :label="$t('cmdb.ciType.sourceCIType')">
          <a-select
            name="source_ci_type_id"
            :placeholder="$t('cmdb.ciType.sourceCITypeTips')"
            v-decorator="[
              'source_ci_type_id',
              { rules: [{ required: true, message: $t('cmdb.ciType.sourceCITypeTips') }] },
            ]"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayCITypes">{{
              CIType.alias
            }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.dstCIType')">
          <a-select
            showSearch
            name="ci_type_id"
            :placeholder="$t('cmdb.ciType.dstCITypeTips')"
            v-decorator="['ci_type_id', { rules: [{ required: true, message: $t('cmdb.ciType.dstCITypeTips') }] }]"
            :filterOption="filterOption"
            @change="changeChild"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in CITypes">
              {{ CIType.alias || CIType.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item :label="$t('cmdb.ciType.relationType')">
          <a-select
            name="relation_type_id"
            :placeholder="$t('cmdb.ciType.relationTypeTips')"
            v-decorator="[
              'relation_type_id',
              { rules: [{ required: true, message: $t('cmdb.ciType.relationTypeTips') }] },
            ]"
          >
            <a-select-option :value="relationType.id" :key="relationType.id" v-for="relationType in relationTypes">{{
              relationType.name
            }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.relationConstraint')">
          <a-select
            :placeholder="$t('cmdb.ciType.relationConstraintTips')"
            v-decorator="[
              'constraint',
              { rules: [{ required: true, message: $t('cmdb.ciType.relationConstraintTips') }] },
            ]"
          >
            <a-select-option value="0">{{ $t('cmdb.ciType.one2Many') }}</a-select-option>
            <a-select-option value="1">{{ $t('cmdb.ciType.one2One') }}</a-select-option>
            <a-select-option value="2">{{ $t('cmdb.ciType.many2Many') }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.attributeAssociation')">
          <a-row>
            <a-col :span="11">
              <a-form-item>
                <a-select
                  :placeholder="$t('cmdb.ciType.attributeAssociationTip4')"
                  allowClear
                  v-decorator="['parent_attr_id', { rules: [{ required: false }] }]"
                >
                  <a-select-option v-for="attr in filterAttributes(attributes)" :key="attr.id">
                    {{ attr.alias || attr.name }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="2" :style="{ textAlign: 'center' }">
              =>
            </a-col>
            <a-col :span="11">
              <a-form-item>
                <a-select
                  :placeholder="$t('cmdb.ciType.attributeAssociationTip5')"
                  allowClear
                  v-decorator="['child_attr_id', { rules: [{ required: false }] }]"
                >
                  <a-select-option v-for="attr in filterAttributes(modalChildAttributes)" :key="attr.id">
                    {{ attr.alias || attr.name }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form-item>
      </a-form>
    </a-modal>
    <CMDBGrant ref="cmdbGrant" resourceType="CITypeRelation" app_id="cmdb" />
  </div>
</template>

<script>
import {
  createRelation,
  deleteRelation,
  getCITypeChildren,
  getCITypeParent,
  getRelationTypes,
} from '@/modules/cmdb/api/CITypeRelation'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'

import CMDBGrant from '../../components/cmdbGrant'

export default {
  name: 'RelationTable',
  components: {
    CMDBGrant,
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
    isInGrantComp: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      form: this.$form.createForm(this),
      visible: false,
      drawerTitle: '',
      CITypes: [],
      relationTypes: [],
      tableData: [],
      parentTableData: [],
      attributes: [],
      parent_attr_id: undefined,
      child_attr_id: undefined,
      modalChildAttributes: [],
    }
  },
  computed: {
    displayCITypes() {
      return this.CITypes.filter((c) => c.id === this.CITypeId)
    },
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
  async mounted() {
    getCITypeAttributesById(this.CITypeId).then((res) => {
      this.attributes = res?.attributes ?? []
    })
    this.getCITypes()
    this.getRelationTypes()
    this.getData()
  },
  methods: {
    async getData() {
      if (!this.isInGrantComp) {
        await this.getCITypeParent()
      }
      this.getCITypeChildren()
    },
    async getCITypeParent() {
      await getCITypeParent(this.CITypeId).then((res) => {
        this.parentTableData = res.parents.map((item) => {
          return {
            ...item,
            source_ci_type_name: this.CITypeName,
            source_ci_type_id: this.CITypeId,
            isParent: true,
          }
        })
      })
    },
    getCITypeChildren() {
      getCITypeChildren(this.CITypeId).then((res) => {
        const data = res.children.map((obj) => {
          return {
            ...obj,
            source_ci_type_name: this.CITypeName,
            source_ci_type_id: this.CITypeId,
          }
        })
        if (this.parentTableData && this.parentTableData.length) {
          this.tableData = [...data, { isDivider: true }, ...this.parentTableData]
        } else {
          this.tableData = data
        }
      })
    },
    getCITypes() {
      getCITypes().then((res) => {
        this.CITypes = res.ci_types
      })
    },
    getRelationTypes() {
      getRelationTypes().then((res) => {
        this.relationTypes = res
      })
    },
    handleDelete(record) {
      deleteRelation(record.source_ci_type_id, record.id).then((res) => {
        this.$message.success(this.$t('deleteSuccess'))
        this.getData()
      })
    },

    handleCreate() {
      this.drawerTitle = this.$t('cmdb.ciType.addRelation')
      this.visible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({
          source_ci_type_id: this.CITypeId,
        })
      })
    },

    onClose() {
      this.form.resetFields()
      this.visible = false
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          // eslint-disable-next-line no-console
          console.log('Received values of form: ', values)
          const {
            source_ci_type_id,
            ci_type_id,
            relation_type_id,
            constraint,
            parent_attr_id = undefined,
            child_attr_id = undefined,
          } = values

          if ((!parent_attr_id && child_attr_id) || (parent_attr_id && !child_attr_id)) {
            this.$message.warning(this.$t('cmdb.ciType.attributeAssociationTip3'))
            return
          }
          createRelation(source_ci_type_id, ci_type_id, {
            relation_type_id,
            constraint,
            parent_attr_id,
            child_attr_id,
          }).then((res) => {
            this.$message.success(this.$t('addSuccess'))
            this.onClose()
            this.getData()
          })
        }
      })
    },
    handleOpenGrant(record) {
      this.$refs.cmdbGrant.open({
        name: `${record.source_ci_type_name} -> ${record.name}`,
        typeRelationIds: [record.source_ci_type_id, record.id],
        cmdbGrantType: 'type_relation',
      })
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
    rowClass({ row }) {
      if (row.isDivider) return 'relation-table-divider'
      if (row.isParent) return 'relation-table-parent'
    },
    handleEditActived({ row }) {
      this.parent_attr_id = row?.parent_attr_id ?? undefined
      this.child_attr_id = row?.child_attr_id ?? undefined
    },
    async handleEditClose({ row }) {
      const { source_ci_type_id: parentId, id: childrenId, constraint, relation_type } = row
      const { parent_attr_id, child_attr_id } = this
      const _find = this.relationTypes.find((item) => item.name === relation_type)
      const relation_type_id = _find?.id
      if ((!parent_attr_id && child_attr_id) || (parent_attr_id && !child_attr_id)) {
        this.$message.warning(this.$t('cmdb.ciType.attributeAssociationTip3'))
        return
      }
      await createRelation(row.isParent ? childrenId : parentId, row.isParent ? parentId : childrenId, {
        relation_type_id,
        constraint,
        parent_attr_id,
        child_attr_id,
      }).finally(() => {
        this.getData()
      })
    },
    getAttrNameById(attributes, id) {
      const _find = attributes.find((attr) => attr.id === id)
      return _find?.alias ?? _find?.name ?? id
    },
    changeChild(value) {
      this.form.setFieldsValue({ child_attr_id: undefined })
      getCITypeAttributesById(value).then((res) => {
        this.modalChildAttributes = res?.attributes ?? []
      })
    },
    filterAttributes(attributes) {
      // filter password/json/is_list
      return attributes.filter((attr) => !attr.is_password && !attr.is_list && attr.value_type !== '6')
    },
  },
}
</script>

<style lang="less">
.ops-stripe-table .vxe-body--row.row--stripe.relation-table-divider {
  background-color: #b1b8d3 !important;
}
.ops-stripe-table .vxe-body--row.relation-table-parent {
  background-color: #f5f8ff !important;
}
.relation-table-divider {
  td {
    height: 1px !important;
    line-height: 1px !important;
  }
}
</style>
