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
          <a-select
            showSearch
            name="source_ci_type_id"
            v-decorator="[
              'source_ci_type_id',
              { rules: [{ required: true, message: $t('cmdb.ciType.sourceCITypeTips') }] },
            ]"
            @change="handleSourceTypeChange"
            :filterOption="filterOption"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayCITypes">{{
              CIType.alias || CIType.name
            }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.dstCIType')">
          <a-select
            showSearch
            name="ci_type_id"
            v-decorator="['ci_type_id', { rules: [{ required: true, message: $t('cmdb.ciType.dstCITypeTips') }] }]"
            @change="handleTargetTypeChange"
            :filterOption="filterOption"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayTargetCITypes">
              {{ CIType.alias || CIType.name }}
            </a-select-option>
          </a-select>
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
                  <a-select-option v-for="attr in filterAttributes(modalParentAttributes)" :key="attr.id">
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
  </div>
</template>

<script>
import ModelRelationTable from './modules/modelRelationTable.vue'
import { searchResourceType } from '@/modules/acl/api/resource'
import { getCITypeGroupsConfig } from '@/modules/cmdb/api/ciTypeGroup'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { createRelation, deleteRelation, getCITypeChildren, getRelationTypes } from '@/modules/cmdb/api/CITypeRelation'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'

export default {
  name: 'Index',
  components: {
    ModelRelationTable,
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
    },
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
            this.handleOk()
          })
        }
      })
      this.sourceCITypeId = undefined
      this.targetCITypeId = undefined
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
      this.form.setFieldsValue({ parent_attr_id: undefined })
      getCITypeAttributesById(value).then((res) => {
        this.modalParentAttributes = res?.attributes ?? []
      })
    },
    handleTargetTypeChange(value) {
      this.targetCITypeId = value
      this.form.setFieldsValue({ child_attr_id: undefined })
      getCITypeAttributesById(value).then((res) => {
        this.modalChildAttributes = res?.attributes ?? []
      })
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
    filterAttributes(attributes) {
      // filter password/json/is_list
      return attributes.filter((attr) => !attr.is_password && !attr.is_list && attr.value_type !== '6')
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';

.model-relation {
  background-color: #fff;
  border-radius: @border-radius-box;
  padding: 24px;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
}
</style>
