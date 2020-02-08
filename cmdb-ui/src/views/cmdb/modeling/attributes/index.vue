<template>
  <a-card :bordered="false">

    <div class="action-btn">
      <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem;">{{ btnName }}</a-button>
    </div>

    <s-table
      :alert="options.alert"
      :columns="columns"
      :data="loadData"
      :rowKey="record=>record.id"
      :rowSelection="options.rowSelection"
      :scroll="scroll"
      :pagination="{ showTotal: (total, range) => `${range[0]}-${range[1]} 共 ${total} 条记录`, pageSizeOptions: pageSizeOptions}"
      showPagination="auto"
      :pageSize="25"
      ref="table"
      size="middle"

    >
      <div slot="filterDropdown" slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }" class="custom-filter-dropdown">
        <a-input
          v-ant-ref="c => searchInput = c"
          :placeholder="` ${column.title}`"
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
        >搜索</a-button>
        <a-button
          @click="() => handleReset(clearFilters, column)"
          size="small"
          style="width: 90px"
        >{{ $t('button.reset') }}</a-button>
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
          <a @click="handleEdit(record)">{{ $t('tip.edit') }}</a>
          <a-divider type="vertical"/>

          <a-popconfirm
            title="确认删除?"
            @confirm="handleDelete(record)"
            okText="是"
            cancelText="否"
          >
            <a>{{ $t('tip.delete') }}</a>
          </a-popconfirm>
        </template>
      </span>

    </s-table>
    <AttributeForm ref="attributeForm" :handleOk="handleOk"> </AttributeForm>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import AttributeForm from './module/attributeForm'
import { valueTypeMap } from './module/const'
import { deleteAttributesById, searchAttributes } from '@/api/cmdb/CITypeAttr'

export default {
  name: 'Index',
  components: {
    STable,
    AttributeForm
  },
  data () {
    return {
      scroll: { x: 1000, y: 500 },
      btnName: '新增属性',

      CITypeName: this.$route.params.CITypeName,
      CITypeId: this.$route.params.CITypeId,

      formLayout: 'vertical',

      attributes: [],
      allAttributes: [],
      transferData: [],
      transferTargetKeys: [],
      transferSelectedKeys: [],
      originTargetKeys: [],
      pageSizeOptions: ['10', '25', '50', '100'],

      columnSearchText: {
        alias: '',
        name: ''
      },
      columns: [
        {
          title: '名称',
          dataIndex: 'alias',
          sorter: false,
          width: 250,
          scopedSlots: {
            customRender: 'aliasSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.alias && record.alias.toLowerCase().includes(value.toLowerCase()),
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
          width: 250,
          scopedSlots: {
            customRender: 'nameSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.name && record.name.toLowerCase().includes(value.toLowerCase()),
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
          width: 80,
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
        parameter['page_size'] = parameter['pageSize']
        parameter['page'] = parameter['pageNo']
        Object.assign(parameter, this.queryParam)
        console.log('loadData.parameter', parameter)

        return searchAttributes(parameter)
          .then(res => {
            res.pageNo = res.page
            res.pageSize = res.total
            res.totalCount = res.numfound
            res.totalPage = Math.ceil(res.numfound / parameter.pageSize)
            res.data = res.attributes

            console.log('loadData.res', res)
            this.allAttributes = res.attributes
            return res
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
    this.form = this.$form.createForm(this)
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
  inject: ['reload'],

  methods: {
    handleSearch (selectedKeys, confirm, column) {
      confirm()
      this.columnSearchText[column.dataIndex] = selectedKeys[0]
      this.queryParam[column.dataIndex] = selectedKeys[0]
    },

    handleReset (clearFilters, column) {
      clearFilters()
      this.columnSearchText[column.dataIndex] = ''
      this.queryParam[column.dataIndex] = ''
    },
    getAttributes () {
      searchAttributes().then(res => {
        this.allAttributes = res.attributes
      })
    },

    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 200
    },

    handleEdit (record) {
      this.$refs.attributeForm.handleEdit(record)
    },
    handleDelete (record) {
      this.deleteAttribute(record.id)
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.$refs.attributeForm.handleCreate()
    },

    deleteAttribute (attrId) {
      deleteAttributesById(attrId)
        .then(res => {
          this.$message.success(`删除成功`)
          this.handleOk()
        })
        .catch(err => this.requestFailed(err))
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
