<template>

  <div>
    <div class="action-btn">
      <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem;">{{ singleAttrAction.btnName }}</a-button>
      <a-button @click="handleUpdate" type="primary">{{ batchBindAttrAction.btnName }}</a-button>
    </div>

    <s-table
      :alert="options.alert"
      :columns="columns"
      :data="loadData"
      :rowKey="record=>record.id"
      :rowSelection="options.rowSelection"
      :scroll="scroll"
      :showPagination="showPagination"
      ref="table"
      size="middle"

    >
      <div slot="filterDropdown" slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }" class="custom-filter-dropdown">
        <a-input
          v-ant-ref="c => searchInput = c"
          :placeholder="`Search ${column.dataIndex}`"
          :value="selectedKeys[0]"
          @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
          @pressEnter="() => handleSearch(selectedKeys, confirm, column)"
          style="width: 188px; margin-bottom: 8px; display: block;"
        />
        <a-button
          type="primary"
          @click="() => handleSearch(selectedKeys, confirm, column)"
          icon="search"
          size="small"
          style="width: 90px; margin-right: 8px"
        >Search</a-button>
        <a-button
          @click="() => handleReset(clearFilters, column)"
          size="small"
          style="width: 90px"
        >Reset</a-button>
      </div>
      <a-icon slot="filterIcon" slot-scope="filtered" type="search" :style="{ color: filtered ? '#108ee9' : undefined }" />

      <template slot="nameSearchRender" slot-scope="text">
        <span v-if="columnSearchText.name">
          <template v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${columnSearchText.name})|(?=${columnSearchText.name})`, 'i'))">
            <mark v-if="fragment.toLowerCase() === columnSearchText.name.toLowerCase()" :key="i" class="highlight">{{ fragment }}</mark>
            <template v-else>{{ fragment }}</template>
          </template>
        </span>
        <template v-else>{{ text }}</template>
      </template>

      <template slot="aliasSearchRender" slot-scope="text">
        <span v-if="columnSearchText.alias">
          <template v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${columnSearchText.alias})|(?=${columnSearchText.alias})`, 'i'))">
            <mark v-if="fragment.toLowerCase() === columnSearchText.alias.toLowerCase()" :key="i" class="highlight">{{ fragment }}</mark>
            <template v-else>{{ fragment }}</template>
          </template>
        </span>
        <template v-else>{{ text }}</template>
      </template>

      <span slot="is_check" slot-scope="text">
        <a-icon type="check" v-if="text"/>
      </span>

      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">编辑</a>
          <a-divider type="vertical"/>

          <a-popconfirm
            title="确认删除?"
            @confirm="handleDelete(record)"
            okText="是"
            cancelText="否"
          >
            <a>删除</a>
          </a-popconfirm>
        </template>
      </span>

    </s-table>
    <AttributeForm ref="attributeForm" :handleOk="handleOk"> </AttributeForm>

    <a-drawer
      :closable="false"
      :title="batchBindAttrAction.drawerTitle"
      :visible="batchBindAttrAction.drawerVisible"
      @close="onBatchBindAttrActionClose"
      placement="right"
      width="30%"
    >
      <a-form :form="form" :layout="formLayout" @submit="handleBatchUpdateSubmit" style="margin-bottom: 5rem">

        <a-transfer
          :dataSource="transferData"
          :render="item=>item.title"
          :selectedKeys="transferSelectedKeys"
          :targetKeys="transferTargetKeys"
          :titles="['当前项', '已选项']"
          :listStyle="{
            height: '600px',
            width: '40%',
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
          <a-button @click="handleBatchUpdateSubmit" type="primary" style="margin-right: 1rem">确定</a-button>
          <a-button @click="onBatchBindAttrActionClose">取消</a-button>

        </div>
      </a-form>

    </a-drawer>
  </div>
</template>

<script>
import {
  createCITypeAttributes,
  deleteCITypeAttributesById,
  getCITypeAttributesByName,
  searchAttributes
} from '@/api/cmdb/CITypeAttr'
import { STable } from '@/components'
import { mixin, mixinDevice } from '@/utils/mixin'
import AttributeForm from '@/views/cmdb/modeling/attributes/module/attributeForm'
import { valueTypeMap } from '@/views/cmdb/modeling/attributes/module/const'

export default {
  name: 'AttributesTable',
  mixins: [mixin, mixinDevice],
  components: {
    STable,
    AttributeForm
  },
  data () {
    return {
      form: this.$form.createForm(this),
      scroll: { x: 1030, y: 600 },
      singleAttrAction: {
        btnName: '新增属性',
        drawerTitle: '新增属性',
        drawerVisible: false
      },
      batchBindAttrAction: {
        btnName: '绑定属性',
        drawerTitle: '绑定属性',
        drawerVisible: false
      },

      CITypeName: this.$route.params.CITypeName,
      CITypeId: this.$route.params.CITypeId,

      formLayout: 'vertical',

      attributes: [],
      allAttributes: [],
      transferData: [],
      transferTargetKeys: [],
      transferSelectedKeys: [],
      originTargetKeys: [],

      ValueTypeMap: valueTypeMap,
      pagination: {
        defaultPageSize: 20
      },
      showPagination: false,
      columnSearchText: {
        alias: '',
        name: ''
      },
      columns: [
        {
          title: '名称',
          dataIndex: 'alias',
          sorter: false,
          width: 200,
          scopedSlots: {
            customRender: 'aliasSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.alias.toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus()
              }, 0)
            }
          }
        },
        {
          title: '英文名',
          dataIndex: 'name',
          sorter: false,
          width: 200,
          scopedSlots: {
            customRender: 'nameSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.name.toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus()
              }, 0)
            }
          }
        },
        {
          title: '类型',
          dataIndex: 'value_type',
          sorter: false,
          width: 100,
          scopedSlots: { customRender: 'value_type' },
          customRender: (text) => valueTypeMap[text]

        },
        {
          title: '唯一',
          dataIndex: 'is_unique',
          width: 50,
          sorter: false,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '索引',
          dataIndex: 'is_index',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '排序',
          dataIndex: 'is_sortable',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '链接',
          dataIndex: 'is_link',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '密码',
          dataIndex: 'is_password',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '列表',
          dataIndex: 'is_list',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

        },
        {
          title: '必须',
          dataIndex: 'is_required',
          sorter: false,
          width: 50,
          scopedSlots: { customRender: 'is_check' }

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
              data: res.attributes

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
  inject: ['reload'],
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
        labelCol: { span: 5 },
        wrapperCol: { span: 12 }
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
    this.getAttributes()
    this.setScrollY()
  },
  methods: {
    handleSearch (selectedKeys, confirm, column) {
      confirm()
      this.columnSearchText[column.dataIndex] = selectedKeys[0]
    },

    handleReset (clearFilters, column) {
      clearFilters()
      this.columnSearchText[column.dataIndex] = ''
    },

    getAttributes () {
      searchAttributes({ page_size: 10000 }).then(res => {
        this.allAttributes = res.attributes
      })
    },
    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 250
    },

    setTransferData () {
      const data = []
      const target = []

      this.attributes.forEach(i => target.push(i.id.toString()))

      this.allAttributes.forEach(i => data.push({
        key: i.id.toString(),
        title: i.alias,
        description: ''
      }))

      this.transferData = data
      this.transferTargetKeys = target
      this.originTargetKeys = target
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

    callback (key) {
      console.log(key)
    },

    handleEdit (record) {
      this.$refs.attributeForm.handleEdit(record)
    },
    handleDelete (record) {
      this.unbindAttribute([record.id])
        .then(res => {
          this.$message.success(`删除成功`)
          this.handleOk()
        }).catch(err => this.requestFailed(err))
    },
    handleOk () {
      this.$refs.table.refresh()
      this.reload()
    },
    handleCreate () {
      this.$refs.attributeForm.handleCreate()
    },

    handleUpdate () {
      this.setTransferData()
      this.batchBindAttrAction.drawerVisible = true
    },

    onBatchBindAttrActionClose () {
      this.batchBindAttrAction.drawerVisible = false
    },

    onChange (e) {
      console.log(`checked = ${e}`)
    },

    handleBatchUpdateSubmit (e) {
      e.preventDefault()
      const p = []
      if (this.addTransferKeys && this.addTransferKeys.length) {
        p.push(this.bindAttribute(this.addTransferKeys))
      }

      if (this.removeTransferKeys && this.removeTransferKeys.length) {
        p.push(this.unbindAttribute(this.removeTransferKeys))
      }
      const that = this
      Promise.all(p).then(function (values) {
        console.log(values)
        that.$message.success(`修改成功`)
        that.handleOk()
        that.onBatchBindAttrActionClose()
      }).catch(err => that.requestFailed(err))
    },

    bindAttribute (attrIds) {
      return createCITypeAttributes(this.CITypeId, { attr_id: attrIds })
    },
    unbindAttribute (attrIds) {
      return deleteCITypeAttributesById(this.CITypeId, { attr_id: attrIds })
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    }

  },
  props: {
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

  .fixedWidthTable table {
    table-layout: fixed;
  }

  .fixedWidthTable .ant-table-tbody > tr > td {
    word-wrap: break-word;
    word-break: break-all;
  }
  .custom-filter-dropdown {
    padding: 8px;
    border-radius: 4px;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .15);
  }

  .highlight {
    background-color: rgb(255, 192, 105);
    padding: 0px;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
