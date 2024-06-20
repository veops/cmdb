<template>
  <div class="relation-table" :style="{ padding: '0 20px 20px' }">
    <a-button
      v-if="!isInGrantComp"
      style="margin-bottom: 10px"
      @click="handleCreate"
      type="primary"
      size="small"
      icon="plus"
    >{{ $t('cmdb.ciType.addRelation') }}</a-button
    >
    <vxe-table
      ref="xTable"
      stripe
      :data="tableData"
      size="small"
      show-overflow
      show-header-overflow
      highlight-hover-row
      keep-source
      class="ops-stripe-table"
      min-height="500"
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
              .split(' ')
              .reverse()
              .join(' ')
          }}</span>
          <span v-else>{{ constraintMap[row.constraint] }}</span>
        </template>
      </vxe-column>
      <vxe-column :width="300" field="attributeAssociation" :edit-render="{}">
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
          <template
            v-for="item in row.parentAndChildAttrList"
          >
            <div
              :key="item.id"
              v-if="item.parentAttrId && item.childAttrId"
            >
              {{ getAttrNameById(row.isParent ? row.attributes : attributes, item.parentAttrId) }}=>
              {{ getAttrNameById(row.isParent ? attributes : row.attributes, item.childAttrId) }}
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
                v-for="attr in filterAttributes(row.isParent ? row.attributes : attributes)"
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
                v-for="attr in filterAttributes(row.isParent ? attributes : row.attributes)"
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
          <a-row
            v-for="item in modalAttrList"
            :key="item.id"
          >
            <a-col :span="10">
              <a-form-item>
                <a-select
                  :placeholder="$t('cmdb.ciType.attributeAssociationTip4')"
                  allowClear
                  v-model="item.parentAttrId"
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
            <a-col :span="9">
              <a-form-item>
                <a-select
                  :placeholder="$t('cmdb.ciType.attributeAssociationTip5')"
                  allowClear
                  v-model="item.childAttrId"
                >
                  <a-select-option v-for="attr in filterAttributes(modalChildAttributes)" :key="attr.id">
                    {{ attr.alias || attr.name }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="3">
              <a
                class="modal-attribute-action"
                @click="removeModalAttr(item.id)"
              >
                <a-icon type="minus-circle" />
              </a>
              <a
                class="modal-attribute-action"
                @click="addModalAttr"
              >
                <a-icon type="plus-circle" />
              </a>
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
import { v4 as uuidv4 } from 'uuid'

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
      tableAttrList: [],
      modalAttrList: [],
      modalChildAttributes: [],
      currentEditData: null,
      isContinueCloseEdit: false,
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
      await this.getCITypeChildren()
    },
    async getCITypeParent() {
      await getCITypeParent(this.CITypeId).then((res) => {
        this.parentTableData = res.parents.map((item) => {
          const parentAndChildAttrList = this.handleAttrList(item)

          return {
            ...item,
            parentAndChildAttrList,
            source_ci_type_name: this.CITypeName,
            source_ci_type_id: this.CITypeId,
            isParent: true,
          }
        })
      })
    },
    async getCITypeChildren() {
      await getCITypeChildren(this.CITypeId).then((res) => {
        const data = res.children.map((obj) => {
          const parentAndChildAttrList = this.handleAttrList(obj)

          return {
            ...obj,
            parentAndChildAttrList,
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
      this.$set(this, 'modalAttrList', [
        {
          id: uuidv4(),
          parentAttrId: undefined,
          childAttrId: undefined
        }
      ])
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
          } = values

          const {
            parent_attr_ids,
            child_attr_ids,
            validate
          } = this.handleValidateAttrList(this.modalAttrList)
          if (!validate) {
            return
          }

          createRelation(source_ci_type_id, ci_type_id, {
            relation_type_id,
            constraint,
            parent_attr_ids,
            child_attr_ids,
          }).then((res) => {
            this.$message.success(this.$t('addSuccess'))
            this.onClose()
            this.getData()
          })
        }
      })
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
      this.$nextTick(async () => {
        if (this.isContinueCloseEdit) {
          const editRecord = this.$refs.xTable.getEditRecord()
          const { row: editRow, column } = editRecord
          this.currentEditData = {
            row: editRow,
            column
          }
          return
        }
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
        this.$set(this, 'tableAttrList', tableAttrList)
      })
    },
    async handleEditClose({ row }) {
      if (this.currentEditData) {
        this.currentEditData = null
        return
      }

      this.isContinueCloseEdit = true

      const { source_ci_type_id: parentId, id: childrenId, constraint, relation_type } = row
      const _find = this.relationTypes.find((item) => item.name === relation_type)
      const relation_type_id = _find?.id

      const {
        parent_attr_ids,
        child_attr_ids,
        validate
      } = this.handleValidateAttrList(this.tableAttrList)
      if (!validate) {
        this.isContinueCloseEdit = false
        return
      }

      await createRelation(row.isParent ? childrenId : parentId, row.isParent ? parentId : childrenId, {
        relation_type_id,
        constraint,
        parent_attr_ids,
        child_attr_ids,
      }).finally(async () => {
        await this.getData()
        this.isContinueCloseEdit = false

        if (this.currentEditData) {
          setTimeout(async () => {
            const { fullData } = this.$refs.xTable.getTableData()
            const findEdit = fullData.find((item) => item.id === this?.currentEditData?.row?.id)
            await this.$refs.xTable.setEditRow(findEdit, 'attributeAssociation')
          })
        }
      })
    },
    getAttrNameById(attributes, id) {
      const _find = attributes.find((attr) => attr.id === id)
      return _find?.alias ?? _find?.name ?? id
    },
    changeChild(value) {
      this.modalAttrList.forEach((item) => {
        item.childAttrId = undefined
      })
      getCITypeAttributesById(value).then((res) => {
        this.modalChildAttributes = res?.attributes ?? []
      })
    },
    filterAttributes(attributes) {
      // filter password/json/is_list
      return attributes.filter((attr) => !attr.is_password && !attr.is_list && attr.value_type !== '6')
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

    addModalAttr() {
      this.modalAttrList.push({
        id: uuidv4(),
        parentAttrId: undefined,
        childAttrId: undefined
      })
    },

    removeModalAttr(id) {
      if (this.modalAttrList.length <= 1) {
        this.$message.error(this.$t('cmdb.ciType.attributeAssociationTip6'))
        return
      }
      const index = this.modalAttrList.findIndex((item) => item.id === id)
      if (index !== -1) {
        this.modalAttrList.splice(index, 1)
      }
    }
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
}

.modal-attribute-action {
  margin-left: 5px;
}
</style>

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
