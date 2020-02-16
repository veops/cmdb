<template>
  <a-card :bordered="false">

    <div class="action-btn">
      <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem;">{{ $t('acl.newRole') }}</a-button>
    </div>

    <s-table
      :alert="options.alert"
      :columns="columns"
      :data="loadData"
      :rowKey="record=>record.id"
      :rowSelection="options.rowSelection"
      :pagination="{ showTotal: (total, range) => `${range[0]}-${range[1]} ${total} records in total`, pageSizeOptions: pageSizeOptions}"
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
        >{{ $t('button.query') }}</a-button>
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

      <span slot="is_app_admin" slot-scope="text">
        <a-icon type="check" v-if="text"/>
      </span>

      <span slot="inherit" slot-scope="key">
        <a-tag color="cyan" v-for="role in id2parents[key]" :key="role.id">{{ role.name }}</a-tag>
      </span>

      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">{{ $t('button.update') }}</a>
          <a-divider type="vertical"/>
          <a-popconfirm
            :title="$t('tip.confirmDelete')"
            @confirm="handleDelete(record)"
            @cancel="cancel"
            :okText="$t('button.yes')"
            :cancelText="$t('button.no')"
          >
            <a>{{ $t('tip.delete') }}</a>
          </a-popconfirm>
        </template>
      </span>
    </s-table>
    <roleForm ref="roleForm" :allRoles="allRoles" :id2parents="id2parents" :handleOk="handleOk"></roleForm>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import roleForm from './module/roleForm'
import { deleteRoleById, searchRole } from '@/api/acl/role'

export default {
  name: 'Index',
  components: {
    STable,
    roleForm
  },
  data () {
    return {
      scroll: { x: 1000, y: 500 },

      formLayout: 'vertical',

      allRoles: [],
      id2parents: {},
      pageSizeOptions: ['10', '25', '50', '100'],

      columnSearchText: {
        alias: '',
        name: ''
      },
      columns: [
        {
          title: this.$t('acl.roleName'),
          dataIndex: 'name',
          sorter: false,
          width: 150,
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
          title: this.$t('acl.isAppAdmin'),
          dataIndex: 'is_app_admin',
          width: 100,
          sorter: false,
          scopedSlots: { customRender: 'is_app_admin' }

        },
        {
          title: this.$t('acl.inheritedFrom'),
          dataIndex: 'id',
          sorter: false,
          width: 250,
          scopedSlots: { customRender: 'inherit' }

        },
        {
          title: this.$t('tip.operate'),
          dataIndex: 'action',
          width: 150,
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        parameter.app_id = this.$route.name.split('_')[0]
        parameter.page = parameter.pageNo
        parameter.page_size = parameter.pageSize
        delete parameter.pageNo
        delete parameter.pageSize
        Object.assign(parameter, this.queryParam)

        return searchRole(parameter)
          .then(res => {
            res.pageNo = res.page
            res.pageSize = res.total
            res.totalCount = res.numfound
            res.totalPage = Math.ceil(res.numfound / parameter.pageSize)
            res.data = res.roles

            this.allRoles = res.roles
            this.id2parents = res.id2parents
            return res
          })
      },

      mdl: {},
      advanced: false,
      queryParam: {},

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

    setScrollY () {
      this.scroll.y = window.innerHeight - this.$refs.table.$el.offsetTop - 200
    },

    handleAddRoleRelation (record) {
      this.$refs.AddRoleRelationForm.handleAddRoleRelation(record)
    },

    handleEdit (record) {
      this.$refs.roleForm.handleEdit(record)
    },
    handleDelete (record) {
      this.deleteRole(record.id)
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.$refs.roleForm.handleCreate()
    },

    deleteRole (id) {
      deleteRoleById(id)
        .then(res => {
          this.$message.success(this.$t('tip.deleteSuccess'))
          this.handleOk()
        })
        .catch(err => this.requestFailed(err))
    },
    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
      this.$message.error(`${msg}`)
    },
    cancel (e) {
      return false
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
