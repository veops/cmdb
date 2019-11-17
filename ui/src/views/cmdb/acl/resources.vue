<template>
  <a-card :bordered="false">
    <a-form layout="inline">
      <a-row :gutter="48">
        <a-col :md="3" :sm="24">
          <div class="action-btn">
            <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem;">{{ btnName }}</a-button>
          </div>
        </a-col>
        <a-col :md="8" :sm="24">
          <a-form-item label="应用列表">
            <a-select placeholder="请选择" v-model="queryParam.app_id">
              <a-select-option v-for="app in appList" :key="app.id" :label="app.name" :value="app.id">{{ app.name }}</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>

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
        >重置</a-button>
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

      <span slot="app_id" slot-scope="text">
        <template>{{ text }}</template>
      </span>

      <span slot="resource_type_id" slot-scope="text">
        <a-icon type="check" v-if="text"/>
      </span>

      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">编辑</a>
          <a-divider type="vertical"/>

          <a-popconfirm
            title="确认删除?"
            @confirm="handleDelete(record)"
            @cancel="cancel"
            okText="是"
            cancelText="否"
          >
            <a>删除</a>
          </a-popconfirm>
        </template>
      </span>

    </s-table>
    <resourceForm ref="resourceForm" :handleOk="handleOk"> </resourceForm>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import resourceForm from './module/resourceForm'
import { deleteResourceById, searchResource } from '@/api/acl/resource'

export default {
  name: 'Index',
  components: {
    STable,
    resourceForm
  },
  data () {
    return {
      appList: [{
        id: '1',
        name: '默认应用'
      }],
      scroll: { x: 1000, y: 500 },
      btnName: '新增资源',

      formLayout: 'vertical',

      allResources: [],
      pageSizeOptions: ['10', '25', '50', '100'],

      columnSearchText: {
        alias: '',
        name: ''
      },
      columns: [
        {
          title: '资源名',
          dataIndex: 'name',
          sorter: false,
          width: 50,
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
          title: '应用',
          dataIndex: 'app_id',
          width: 50,
          sorter: false,
          scopedSlots: { customRender: 'app_id' }
        },
        {
          title: '资源类型',
          dataIndex: 'resource_type_id',
          width: 50,
          sorter: false,
          scopedSlots: { customRender: 'resource_type_id' }

        },
        {
          title: '操作',
          dataIndex: 'action',
          width: 150,
          fixed: 'right',
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        Object.assign(parameter, this.queryParam)
        console.log('loadData.parameter', parameter)

        return searchResource(parameter)
          .then(res => {
            res.pageNo = res.page
            res.pageSize = res.total
            res.totalCount = res.numfound
            res.totalPage = Math.ceil(res.numfound / parameter.pageSize)
            res.data = res.resources

            console.log('loadData.res', res)
            this.allResources = res.resources
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

  created () {
    this.queryParam.app_id = this.appList[0].id
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
    this.searchResources(this.queryParam)
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
    searchResources (params) {
      searchResource(params).then(res => {
        this.allResources = res.resources
      })
    },

    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 200
    },

    handleEdit (record) {
      this.$refs.resourceForm.handleEdit(record)
    },
    handleDelete (record) {
      this.deleteResource(record.id)
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.$refs.resourceForm.handleCreate()
    },

    deleteResource (id) {
      deleteResourceById(id)
        .then(res => {
          this.$message.success(`删除成功`)
          this.handleOk()
        })
        .catch(err => this.requestFailed(err))
    },
    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    },
    cancel () {

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
