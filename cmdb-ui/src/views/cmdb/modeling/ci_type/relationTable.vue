<template>
  <div>
    <a-button class="action-btn" @click="handleCreate" type="primary">{{ $t('ciType.newRelation') }}</a-button>
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
          <a @click="handleDelete(record)">{{ $t('tip.delete') }}</a>
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
          :label="$t('ciType.sourceCIType')"
        >
          <a-select
            name="source_ci_type_id"
            style="width: 120px"
            v-decorator="['source_ci_type_id', {rules: [], } ]"
          >
            <template v-for="CIType in CITypes">
              <a-select-option :value="CIType.id" :key="CIType.id" v-if="CITypeId == CIType.id">{{ CIType.alias }}</a-select-option>
            </template>
          </a-select>

        </a-form-item>
        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          :label="$t('ciType.targetCIType')"
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
          :label="$t('ciType.relationType')"
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
          <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('button.submit') }}</a-button>
          <a-button @click="onClose">{{ $t('button.cancel') }}</a-button>

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
          title: this.$t('ciType.sourceCIType') + this.$t('ciType.name'),
          dataIndex: 'source_ci_type_name',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'source_ci_type_name' }
        },
        {
          title: this.$t('ciType.relationType'),
          dataIndex: 'relation_type',
          sorter: false,
          width: 100,
          scopedSlots: { customRender: 'name' }
        },
        {
          title: this.$t('ciType.targetCIType') + this.$t('ciType.alias'),
          dataIndex: 'alias',
          sorter: false,
          scopedSlots: { customRender: 'alias' }
        },
        {
          title: this.$t('tip.operate'),
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
      advanced: false,
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
          this.$message.success(this.$t('tip.deleteSuccess'))

          this.handleOk()
        }).catch(err => this.requestFailed(err))
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.drawerTitle = this.$t('ciType.newRelation')
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
              this.$message.success(this.$t('tip.addSuccess'))
              this.onClose()
              this.handleOk()
            }).catch(err => this.requestFailed(err))
        }
      })
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
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
