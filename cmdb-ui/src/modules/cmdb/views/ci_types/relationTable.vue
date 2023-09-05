<template>
  <div :style="{ padding: '16px 24px 24px' }">
    <a-button
      style="margin-bottom: 10px"
      @click="handleCreate"
      type="primary"
      size="small"
      class="ops-button-primary"
      icon="plus"
    >新增关系</a-button
    >
    <vxe-table
      stripe
      :data="tableData"
      size="small"
      show-overflow
      highlight-hover-row
      keep-source
      :max-height="windowHeight - 180"
      class="ops-stripe-table"
      :row-class-name="rowClass"
    >
      <vxe-column field="source_ci_type_name" title="源模型英文名"></vxe-column>
      <vxe-column field="relation_type" title="关联类型">
        <template #default="{row}">
          <span style="color:#2f54eb" v-if="row.isParent">被</span>
          {{ row.relation_type }}
        </template>
      </vxe-column>
      <vxe-column field="alias" title="目标模型名"></vxe-column>
      <vxe-column field="constraint" title="关系约束">
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
      <vxe-column field="operation" title="操作" width="100">
        <template #default="{row}">
          <a-space v-if="!row.isParent && row.source_ci_type_id">
            <a @click="handleOpenGrant(row)"><a-icon type="user-add"/></a>
            <a-popconfirm title="确认删除？" @confirm="handleDelete(row)">
              <a style="color: red;"><a-icon type="delete"/></a>
            </a-popconfirm>
          </a-space>
        </template>
      </vxe-column>
      <template #empty>
        <div>
          <img :style="{ width: '100px' }" :src="require('@/assets/data_empty.png')" />
          <div>暂无数据</div>
        </div>
      </template>
    </vxe-table>
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
            name="source_ci_type_id"
            v-decorator="['source_ci_type_id', { rules: [{ required: true, message: '请选择源模型' }] }]"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in displayCITypes">{{
              CIType.alias
            }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="目标模型">
          <a-select
            showSearch
            name="ci_type_id"
            v-decorator="['ci_type_id', { rules: [{ required: true, message: '请选择目标模型' }] }]"
            :filterOption="filterOption"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in CITypes">
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
  },
  data() {
    return {
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
      tableData: [],
      parentTableData: [],
    }
  },
  computed: {
    displayCITypes() {
      return this.CITypes.filter((c) => c.id === this.CITypeId)
    },
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  async mounted() {
    this.getCITypes()
    this.getRelationTypes()
    await this.getCITypeParent()
    this.getData()
  },
  methods: {
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
    getData() {
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
        this.$message.success(`删除成功！`)
        this.handleOk()
      })
    },
    handleOk() {
      this.getData()
    },

    handleCreate() {
      this.drawerTitle = '新增关系'
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

          createRelation(values.source_ci_type_id, values.ci_type_id, values.relation_type_id, values.constraint).then(
            (res) => {
              this.$message.success(`添加成功`)
              this.onClose()
              this.handleOk()
            }
          )
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
