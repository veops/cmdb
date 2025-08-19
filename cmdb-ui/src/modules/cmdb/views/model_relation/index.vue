<template>
  <div class="model-relation">
    <a-button @click="handleCreate" type="primary" style="margin-bottom: 15px;" icon="plus">{{
      $t('cmdb.ciType.addRelation')
    }}</a-button>
    <model-relation-table ref="table"></model-relation-table>
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
          <CMDBTypeSelectAntd
            v-decorator="[
              'source_ci_type_id',
              { rules: [{ required: true, message: $t('cmdb.ciType.sourceCITypeTips') }] },
            ]"
            name="source_ci_type_id"
            :CITypeGroup="CITypeGroups"
            @change="handleSourceTypeChange"
          />
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.dstCIType')">
          <CMDBTypeSelectAntd
            v-decorator="[
              'ci_type_id',
              { rules: [{ required: true, message: $t('cmdb.ciType.dstCITypeTips') }] },
            ]"
            name="ci_type_id"
            :CITypeGroup="CITypeGroups"
            @change="handleTargetTypeChange"
          />
        </a-form-item>

        <a-form-item :label="$t('cmdb.ciType.relationType')">
          <a-select
            name="relation_type_id"
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
            v-decorator="[
              'constraint',
              { rules: [{ required: true, message: $t('cmdb.ciType.relationConstraintTips') }] },
            ]"
            @change="handleConstraintChange"
          >
            <a-select-option value="0">{{ $t('cmdb.ciType.one2Many') }}</a-select-option>
            <a-select-option value="1">{{ $t('cmdb.ciType.one2One') }}</a-select-option>
            <a-select-option value="2">{{ $t('cmdb.ciType.many2Many') }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.attributeAssociation')">
          <template #extra>
            <div>{{ $t('cmdb.ciType.attributeAssociationTip7') }}</div>
            <div>{{ $t('cmdb.ciType.attributeAssociationTip8') }}</div>
            <div>{{ $t('cmdb.ciType.attributeAssociationTip9') }}</div>
          </template>
          <a-row
            v-for="item in modalAttrList"
            :key="item.id"
          >
            <a-col :span="10">
              <a-form-item>
                <a-select
                  :placeholder="$t('cmdb.ciType.attributeAssociationTip4')"
                  optionFilterProp="title"
                  show-search
                  allowClear
                  v-model="item.parentAttrId"
                >
                  <a-select-option
                    v-for="attr in filterAttributes(modalParentAttributes, item.childAttrId, modalChildAttributes, 'parent')"
                    :key="attr.id"
                    :title="attr.alias || attr.name"
                  >
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
                  optionFilterProp="title"
                  show-search
                  allowClear
                  v-model="item.childAttrId"
                >
                  <a-select-option
                    v-for="attr in filterAttributes(modalChildAttributes, item.parentAttrId, modalParentAttributes, 'child')"
                    :key="attr.id"
                    :title="attr.alias || attr.name"
                  >
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
  </div>
</template>

<script>
import { searchResourceType } from '@/modules/acl/api/resource'
import { getCITypeGroupsConfig } from '@/modules/cmdb/api/ciTypeGroup'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { createRelation, deleteRelation, getRelationTypes } from '@/modules/cmdb/api/CITypeRelation'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { v4 as uuidv4 } from 'uuid'

import ModelRelationTable from './modules/modelRelationTable.vue'
import CMDBTypeSelectAntd from '@/modules/cmdb/components/cmdbTypeSelect/cmdbTypeSelectAntd'

export default {
  name: 'Index',
  components: {
    ModelRelationTable,
    CMDBTypeSelectAntd
  },
  data() {
    return {
      resource_type: {},
      CITypeGroups: [],
      currentId: null,

      form: this.$form.createForm(this),

      visible: false,

      drawerTitle: '',
      CITypes: [],
      relationTypes: [],

      sourceCITypeId: undefined,
      targetCITypeId: undefined,

      modalParentAttributes: [],
      modalChildAttributes: [],
      modalAttrList: [],
    }
  },
  computed: {
    currentCId() {
      if (this.currentId) {
        if (this.currentId.split('%')[1] !== 'null') {
          return Number(this.currentId.split('%')[1])
        }
        return null
      }
      return null
    },
    displayCITypes() {
      return this.CITypes
      // return this.CITypes.filter((c) => c.id !== this.targetCITypeId)
    },
    displayTargetCITypes() {
      return this.CITypes
      // return this.CITypes.filter((c) => c.id !== this.sourceCITypeId)
    },
    CITypeId() {
      return this.currentCId
    },
    constraintMap() {
      return {
        '0': this.$t('cmdb.ciType.one2Many'),
        '1': this.$t('cmdb.ciType.one2One'),
        '2': this.$t('cmdb.ciType.many2Many'),
      }
    }
  },
  provide() {
    return {
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  created() {
    this.getCITypes()
    this.getRelationTypes()
  },
  mounted() {
    const _currentId = localStorage.getItem('ops_cityps_currentId')
    if (_currentId) {
      this.currentId = _currentId
    }
    searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
      this.resource_type = { groups: res.groups, id2perms: res.id2perms }
    })
    this.loadCITypes(!_currentId)
  },
  methods: {
    async loadCITypes(isResetCurrentId = false) {
      const groups = await getCITypeGroupsConfig({ need_other: true })
      let alreadyReset = false
      if (isResetCurrentId) {
        this.currentId = null
      }
      this.$nextTick(() => {
        groups.forEach((g) => {
          if (!g.id) {
            g.id = -1
          }
          if (isResetCurrentId && !alreadyReset && g.ci_types && g.ci_types.length) {
            this.currentId = `${g.id}%${g.ci_types[0].id}%${g.ci_types[0].name}`
            alreadyReset = true
          }
          if (!g.ci_types) {
            g.ci_types = []
          }
        })
        this.CITypeGroups = groups
        localStorage.setItem('ops_cityps_currentId', this.currentId)
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
          source_ci_type_id: this.sourceCITypeId,
        })
      })
    },
    onClose() {
      this.form.resetFields()
      this.visible = false
      this.sourceCITypeId = undefined
      this.targetCITypeId = undefined
    },
    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
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
            this.handleOk()
          })
        }
      })
      this.sourceCITypeId = undefined
      this.targetCITypeId = undefined
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

    handleOk() {
      this.$refs.table.refresh()
    },
    handleDelete(record) {
      deleteRelation(record.source_ci_type_id, record.id).then((res) => {
        this.$message.success(this.$t('deleteSuccess'))

        this.handleOk()
      })
    },
    handleSourceTypeChange(value) {
      this.sourceCITypeId = value
      this.modalAttrList.forEach((item) => {
        item.parentAttrId = undefined
      })
      getCITypeAttributesById(value).then((res) => {
        this.modalParentAttributes = res?.attributes ?? []
      })
    },
    handleTargetTypeChange(value) {
      this.targetCITypeId = value
      this.modalAttrList.forEach((item) => {
        item.childAttrId = undefined
      })
      getCITypeAttributesById(value).then((res) => {
        this.modalChildAttributes = res?.attributes ?? []
      })
    },

    filterAttributes(attributes, relationAttrId, relationAttrs, type) {
      const relationAttr = relationAttrs.find((attr) => attr.id === relationAttrId)

      // filter password/json/longText/bool/reference
      let filterAttrs = attributes.filter((attr) => {
        if (attr.value_type === '2' && !attr.is_index) {
          return false
        }

        return !attr.is_password && attr.value_type !== '6' && !attr.is_bool && !attr.is_reference
      })

      if (relationAttr) {
        filterAttrs = filterAttrs.filter((attr) => attr.value_type === relationAttr?.value_type)
      }

      const constraintValue = Number(this.form.getFieldValue('constraint'))
      if (
        (constraintValue === 0 && type === 'child') ||
        constraintValue === 1 ||
        (constraintValue === 2 && relationAttr?.is_list)
      ) {
        return filterAttrs.filter((attr) => !attr.is_list)
      }

      return filterAttrs
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
    },

    handleConstraintChange() {
      this.modalAttrList.forEach((item) => {
        item.parentAttrId = undefined
        item.childAttrId = undefined
      })
    }
  },
}
</script>

<style lang="less" scoped>
.model-relation {
  background-color: #fff;
  border-radius: @border-radius-box;
  padding: 24px;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
}

.modal-attribute-action {
  margin-left: 5px;
}

.model-select-name {
  font-size: 12px;
  color: #A5A9BC;
}
</style>
