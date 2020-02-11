<template>
  <div>
    <a-button class="action-btn" @click="handleCreate" type="primary">批量修改</a-button>
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

        <a-transfer
          :dataSource="transferData"
          :render="item=>item.title"
          :selectedKeys="transferSelectedKeys"
          :targetKeys="transferTargetKeys"
          :titles="['当前项', '已选项']"
          :listStyle="{
            height: '600px',
            width: '42%'

          }"
          showSearch
          @change="handleTransferChange"
          @scroll="handleTransferScroll"
          @selectChange="handleTransferSelectChange"
        />

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

import { STable } from '@/components'
import { getCITypeAttributesByName, updateCITypeAttributesById } from '@/api/cmdb/CITypeAttr'

export default {
  name: 'DefaultShowTable',
  components: {
    STable
  },
  data () {
    return {

      CITypeId: this.$route.params.CITypeId,
      CITypeName: this.$route.params.CITypeName,

      form: this.$form.createForm(this),
      scroll: { x: 1000, y: 600 },

      visible: false,

      drawerTitle: '',

      formLayout: 'vertical',

      transferData: [],
      transferTargetKeys: [],
      transferSelectedKeys: [],
      originTargetKeys: [],

      attributes: [],

      pagination: {
        defaultPageSize: 20
      },
      showPagination: false,
      columns: [
        {
          title: '属性名',
          dataIndex: 'alias',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'alias' }
        },
        {
          title: '属性英文名',
          dataIndex: 'name',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'name' }
        },
        {
          title: '默认显示',
          dataIndex: 'default_show',
          sorter: false,
          scopedSlots: { customRender: 'is_check' }

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
        return getCITypeAttributesByName(this.CITypeName)
          .then(res => {
            this.attributes = res.attributes
            this.setTransferData()

            return {
              data: this.attributes.filter(o => o.default_show)
            }
          })
      },

      mdl: {},
      // 高级搜索 展开/关闭
      advanced: false,
      // 查询参数
      queryParam: {},
      // 表头

      selectedRowKeys: [],
      selectedRows: [],

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

    removeTransferKeys () {
      const { originTargetKeys, transferTargetKeys } = this
      return originTargetKeys.filter(v => !originTargetKeys.includes(v) || !transferTargetKeys.includes(v))
    },

    addTransferKeys () {
      const { originTargetKeys, transferTargetKeys } = this
      return transferTargetKeys.filter(v => !transferTargetKeys.includes(v) || !originTargetKeys.includes(v))
    },

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

  },
  methods: {

    setTransferData () {
      const data = []
      const target = []
      this.attributes.forEach(
        function (i) {
          data.push({
            key: i.id.toString(),
            title: i.alias,
            description: ''
          })
          if (i.default_show) {
            target.push(i.id.toString())
          }
        }
      )
      this.transferData = data
      this.transferTargetKeys = target
      this.originTargetKeys = target
    },
    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 250
    },

    handleTransferChange (nextTargetKeys, direction, moveKeys) {
      this.transferTargetKeys = nextTargetKeys

      console.log('targetKeys: ', nextTargetKeys)
      console.log('direction: ', direction)
      console.log('moveKeys: ', moveKeys)
      console.log('addTransferKeys: ', this.addTransferKeys)
      console.log('removeTransferKeys: ', this.removeTransferKeys)
    },

    handleTransferSelectChange (sourceSelectedKeys, targetSelectedKeys) {
      this.transferSelectedKeys = [...sourceSelectedKeys, ...targetSelectedKeys]
      console.log('sourceSelectedKeys: ', sourceSelectedKeys)
      console.log('targetSelectedKeys: ', targetSelectedKeys)
    },
    handleTransferScroll (direction, e) {
      console.log('direction:', direction)
      console.log('target:', e.target)
    },

    handleDelete (record) {
      console.log(record)

      updateCITypeAttributesById(this.CITypeId, { attributes: [{ attr_id: record.id, default_show: false }] })
        .then(res => {
          this.$message.success(`删除成功`)
          this.handleOk()
        })
        .catch(err => this.requestFailed(err))
    },
    handleOk () {
      this.$refs.table.refresh()
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },

    handleCreate () {
      this.drawerTitle = '批量修改'
      this.visible = true
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
      if (this.addTransferKeys || this.removeTransferKeys) {
        const requestData = []
        this.addTransferKeys.forEach(function (k) {
          const data = { 'attr_id': k, 'default_show': true }
          requestData.push(data)
        })

        this.removeTransferKeys.forEach(function (k) {
          const data = { 'attr_id': k, 'default_show': false }
          requestData.push(data)
        })

        const CITypeId = this.CITypeId

        updateCITypeAttributesById(CITypeId, { attributes: requestData }).then(
          res => {
            this.$message.success(`更新成功`)
            this.visible = false
            this.handleOk()
          }
        ).catch(err => {
          this.requestFailed(err)
        })
      }
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
  .ant-transfer {
    margin-bottom: 1rem;
  }
  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
