<template>
  <a-card :bordered="false">
    <div>
      <a-list :grid="{ gutter: 12, column: 12 }" style="height: 40px;clear: both">
        <a-list-item
          v-for="rtype in allResourceTypes"
          :key="rtype.id"
          :class="{'bottom-border':currentType.name===rtype.name}"
          style="text-align: center;height: 30px; margin:0 30px"
        >
          <a
            @click="loadCurrentType(rtype)"
            :style="currentType.name === rtype.name?'color:#108ee9':'color:grey'">
            <span style="font-size: 18px">{{ rtype.name }}</span>
          </a>
        </a-list-item>
      </a-list>
    </div>
    <a-divider style="margin-top: -16px" />
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
      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handlePerm(record)">查看授权</a>
          <a-divider type="vertical"/>
          <a @click="handlePermManage(record)">授权</a>
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
    <resourceForm ref="resourceForm" @fresh="handleOk"> </resourceForm>
    <resourcePermForm ref="resourcePermForm"> </resourcePermForm>
    <ResourcePermManageForm ref="resourcePermManageForm" :groupTypeMessage="currentType"></ResourcePermManageForm>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import resourceForm from './module/resourceForm'
import resourcePermForm from './module/resourcePermForm'
import ResourcePermManageForm from './module/resourcePermManageForm'
import { deleteResourceById, searchResource, searchResourceType } from '@/api/acl/resource'

export default {
  name: 'Index',
  components: {
    STable,
    resourceForm,
    resourcePermForm,
    ResourcePermManageForm
  },
  data () {
    return {
      scroll: { x: 1000, y: 500 },
      btnName: '新增资源',
      allResourceTypes: [],
      currentType: { id: 0 },
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
          title: '创建时间',
          width: 200,
          dataIndex: 'created_at'
        },
        {
          title: '最后修改时间',
          width: 200,
          dataIndex: 'updated_at'
        },
        {
          title: '操作',
          dataIndex: 'action',
          width: 150,
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        parameter.app_id = this.$route.name.split('_')[0]
        parameter.page = parameter.pageNo
        parameter.page_size = parameter.pageSize
        parameter.resource_type_id = this.currentType.id
        delete parameter.pageNo
        delete parameter.pageSize
        Object.assign(parameter, this.queryParam)
        return searchResource(parameter)
          .then(res => {
            res.pageNo = res.page
            res.pageSize = res.total
            res.totalCount = res.numfound
            res.totalPage = Math.ceil(res.numfound / parameter.pageSize)
            res.data = res.resources
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
    this.setScrollY()
    this.getAllResourceTypes()
  },
  inject: ['reload'],

  methods: {
    getAllResourceTypes () {
      searchResourceType({ page_size: 9999, app_id: this.$route.name.split('_')[0] }).then(res => {
        this.allResourceTypes = res.groups
        this.loadCurrentType(res.groups[0])
      })
    },
    handlePermManage (record) {
      this.$refs.resourcePermManageForm.editPerm(record)
    },
    loadCurrentType (rtype) {
      if (rtype) {
        this.currentType = rtype
      }
      this.$refs.table.refresh()
    },
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

    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 200
    },
    handlePerm (record) {
      this.$refs.resourcePermForm.handlePerm(record)
    },
    handleDelete (record) {
      this.deleteResource(record.id)
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.$refs.resourceForm.handleCreate(this.currentType)
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
  .bottom-border {
  border-bottom: cornflowerblue 2px solid;
  z-index: 1;
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
