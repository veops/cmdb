<template>
  <div>
    <a-button class="action-btn" @click="handleCreate" type="primary">新增关系</a-button>
    <s-table
      :alert="options.alert"
      :columns="columns"
      :data="loadData"
      :pagination="pagination"
      :rowKey="record=>record.id"
      :rowSelection="options.rowSelection"
      :showPagination="showPagination"
      ref="table"
      size="middle"
      :scroll="scroll"
    >

      <span slot="is_check" slot-scope="text">
        <a-icon type="check" v-if="text"/>
      </span>

      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleDelete(record)">删除</a>
        </template>
      </span>

    </s-table>
    <a-drawer
      :closable="false"
      :title="drawerTitle"
      :visible="visible"
      @close="onClose"
      placement="right"
      width="30%"
    >
      <a-form :form="form" :layout="formLayout" @submit="handleSubmit">

        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          label="源模型"
        >
          <a-select
            name="source_ci_type_id"
            style="width: 120px"
            v-decorator="['source_ci_type_id', {rules: [], } ]"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in CITypes" v-if="CITypeId === CIType.id">{{ CIType.alias }}</a-select-option>
          </a-select>

        </a-form-item>
        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          label="目标模型"
        >
          <a-select
            name="ci_type_id"
            style="width: 120px"
            v-decorator="['ci_type_id', {rules: [], } ]"
          >
            <a-select-option :value="CIType.id" :key="CIType.id" v-for="CIType in CITypes">{{ CIType.alias }}</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          label="关联关系"
        >
          <a-select
            name="relation_type_id"
            style="width: 120px"
            v-decorator="['relation_type_id', {rules: [], } ]"
          >
            <a-select-option :value="relationType.id" :key="relationType.id" v-for="relationType in relationTypes">{{ relationType.name }}
            </a-select-option>
          </a-select>

        </a-form-item>

        <div
          :style="{
            position: 'absolute',
            left: 0,
            bottom: 0,
            width: '100%',
            borderTop: '1px solid #e9e9e9',
            padding: '0.8rem 1rem',
            background: '#fff',

          }"
        >
          <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">确定</a-button>
          <a-button @click="onClose">取消</a-button>

        </div>
      </a-form>
    </a-drawer>

  </div>

</template>

<script>
import { createRelation, deleteRelation, getCITypeChildren } from '@/api/cmdb/CITypeRelation'
import { getRelationTypes } from '@/api/cmdb/relationType'
import { getCITypes } from '@/api/cmdb/CIType'

import { STable } from '@/components'
import PageView from '@/layouts/PageView'

export default {
  name: 'RelationTable',
  components: {
    PageView,
    STable
  },
  data () {
    return {
      CITypeId: parseInt(this.$route.params.CITypeId),
      CITypeName: this.$route.params.CITypeName,
      form: this.$form.createForm(this),
      scroll: { x: 1300, y: 600 },

      visible: false,

      drawerTitle: '',

      formLayout: 'vertical',

      CITypes: [],
      relationTypes: [],

      pagination: {
        defaultPageSize: 20
      },
      showPagination: false,
      columns: [
        {
          title: '源模型英文名',
          dataIndex: 'source_ci_type_name',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'source_ci_type_name' }
        },
        {
          title: '关联类型',
          dataIndex: 'relation_type',
          sorter: false,
          width: 100,
          scopedSlots: { customRender: 'name' }
        },
        {
          title: '目标模型名',
          dataIndex: 'alias',
          sorter: false,
          scopedSlots: { customRender: 'alias' }
        },
        {
          title: '操作',
          dataIndex: 'action',
          width: 100,
          fixed: 'right',
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        console.log('loadData.parameter', parameter)
        const CITypeId = this.CITypeId
        const CITypeName = this.CITypeName

        console.log('this CITypeId ', CITypeId, 'type', typeof CITypeName, 'CITypeName', CITypeName)

        return getCITypeChildren(this.CITypeId)
          .then(res => {
            let data = res.children

            data = data.map(function (obj, index) {
              obj.source_ci_type_name = CITypeName
              obj.source_ci_type_id = CITypeId
              return obj
            })

            return {
              data: data
            }
          })
      },

      mdl: {},
      // 高级搜索 展开/关闭
      advanced: false,
      // 查询参数
      queryParam: {},
      // custom table alert & rowSelection
      options: {
        alert: false,
        rowSelection: null
      },
      optionAlertShow: false

    }
  },
  beforeCreate () {
  },
  computed: {
    formItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      } : {}
    },

    horizontalFormItemLayout () {
      return {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      }
    },
    buttonItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        wrapperCol: { span: 14, offset: 4 }
      } : {}
    }
  },
  mounted () {
    this.getCITypes()
    this.getRelationTypes()
  },
  methods: {
    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 250
    },

    getCITypes () {
      getCITypes().then(res => {
        this.CITypes = res.ci_types
      })
    },
    getRelationTypes () {
      getRelationTypes().then(res => {
        this.relationTypes = res
      })
    },

    callback (key) {
      console.log(key)
    },
    handleDelete (record) {
      console.log(record)

      deleteRelation(record.source_ci_type_id, record.id)
        .then(res => {
          this.$message.success(`删除成功`)

          this.handleOk()
        }).catch(err => this.requestFailed(err))
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.drawerTitle = '新增关系'
      this.visible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({
          source_ci_type_id: this.CITypeId

        })
      })
    },

    onClose () {
      this.form.resetFields()
      this.visible = false
    },

    onChange (e) {
      console.log(`checked = ${e.target.checked}`)
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          // eslint-disable-next-line no-console
          console.log('Received values of form: ', values)

          createRelation(values.source_ci_type_id, values.ci_type_id, values.relation_type_id)
            .then(res => {
              this.$message.success(`添加成功`)
              this.onClose()
              this.handleOk()
            }).catch(err => this.requestFailed(err))
        }
      })
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    }

  },

  watch: {}

}
</script>

<style lang="less" scoped>
  .search {
    margin-bottom: 54px;
  }

  .fold {
    width: calc(100% - 216px);
    display: inline-block
  }

  .operator {
    margin-bottom: 18px;
  }

  .action-btn {
    margin-bottom: 1rem;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
