<template>
  <div class="model-relation">
    <a-button @click="handleCreate" type="primary" style="margin-bottom: 15px;" icon="plus">新增关系</a-button>
    <model-relation-table ref="table"></model-relation-table>
    <a-modal
      :closable="false"
      :title="drawerTitle"
      :visible="visible"
      @cancel="onClose"
      @ok="handleSubmit"
      width="500px"
    >
      <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
        <a-form-item label="源模型">
          <a-select
            showSearch
            name="source_ci_type_id"
            v-decorator="['source_ci_type_id', { rules: [{ required: true, message: '请选择源模型' }] }]"
            @change="handleSourceTypeChange"
            :filterOption="filterOption"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayCITypes">{{
              CIType.alias || CIType.name
            }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="目标模型">
          <a-select
            showSearch
            name="ci_type_id"
            v-decorator="['ci_type_id', { rules: [{ required: true, message: '请选择目标模型' }] }]"
            @change="handleTargetTypeChange"
            :filterOption="filterOption"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayTargetCITypes">
              {{ CIType.alias || CIType.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="关联关系">
          <a-select
            name="relation_type_id"
            v-decorator="['relation_type_id', { rules: [{ required: true, message: '请选择关联关系' }] }]"
          >
            <a-select-option :value="relationType.id" :key="relationType.id" v-for="relationType in relationTypes">{{
              relationType.name
            }}</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="关联约束">
          <a-select v-decorator="['constraint', { rules: [{ required: true, message: '请选择关联约束' }] }]">
            <a-select-option value="0">一对多</a-select-option>
            <a-select-option value="1">一对一</a-select-option>
            <a-select-option value="2">多对多</a-select-option>
          </a-select>
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
import { createRelation, deleteRelation, getRelationTypes } from '@/modules/cmdb/api/CITypeRelation'
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
      constraintMap: {
        '0': '一对多',
        '1': '一对一',
        '2': '多对多',
      },

      sourceCITypeId: undefined,
      targetCITypeId: undefined,
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
    },
    displayTargetCITypes() {
      return this.CITypes
    },
    CITypeId() {
      return this.currentCId
    },
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
            // 给未分组增加一个假的id
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
      this.drawerTitle = '新增关系'
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
          createRelation(values.source_ci_type_id, values.ci_type_id, values.relation_type_id, values.constraint).then(
            (res) => {
              this.$message.success(`添加成功`)
              this.onClose()
              this.handleOk()
            }
          )
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
        this.$message.success(`删除成功！`)

        this.handleOk()
      })
    },
    handleSourceTypeChange(value) {
      this.sourceCITypeId = value
    },
    handleTargetTypeChange(value) {
      this.targetCITypeId = value
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
  },
}
</script>

<style lang="less" scoped>
.model-relation {
  background-color: #fff;
  border-radius: 15px;
  padding: 24px;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
}
</style>
