<template>
  <a-card :bordered="false">

    <div class="action-btn">
      <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem;">{{ $t('acl.newUser') }}</a-button>
    </div>

    <s-table
      :alert="options.alert"
      :columns="columns"
      :data="loadData"
      :rowKey="record=>record.uid"
      :rowSelection="options.rowSelection"
      :scroll="scroll"
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

      <template slot="usernameSearchRender" slot-scope="text">
        <span v-if="columnSearchText.name">
          <template v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${columnSearchText.username})|(?=${columnSearchText.username})`, 'i'))">
            <mark v-if="fragment.toLowerCase() === columnSearchText.name.toLowerCase()" :key="i" class="highlight">{{ fragment }}</mark>
            <template v-else>{{ fragment }}</template>
          </template>
        </span>
        <template v-else>{{ text }}</template>
      </template>

      <template slot="nicknameSearchRender" slot-scope="text">
        <span v-if="columnSearchText.alias">
          <template v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${columnSearchText.nickname})|(?=${columnSearchText.nickname})`, 'i'))">
            <mark v-if="fragment.toLowerCase() === columnSearchText.alias.toLowerCase()" :key="i" class="highlight">{{ fragment }}</mark>
            <template v-else>{{ fragment }}</template>
          </template>
        </span>
        <template v-else>{{ text }}</template>
      </template>

      <span slot="is_check" slot-scope="text">
        <a-icon type="check" v-if="text"/>
      </span>
      <span slot="block" slot-scope="text">
        <a-icon type="lock" v-if="text"/>
      </span>

      <span slot="action" slot-scope="text, record">
        <template>
          <a @click="handleEdit(record)">{{ $t('tip.edit') }}</a>
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
    <userForm ref="userForm" :handleOk="handleOk"> </userForm>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import userForm from './module/userForm'
import { deleteUserById, searchUser } from '@/api/acl/user'

export default {
  name: 'Index',
  components: {
    STable,
    userForm
  },
  data () {
    return {
      scroll: { x: 1300, y: 500 },

      CITypeName: this.$route.params.CITypeName,
      CITypeId: this.$route.params.CITypeId,

      formLayout: 'vertical',

      allUsers: [],
      pageSizeOptions: ['10', '25', '50', '100'],

      columnSearchText: {
        alias: '',
        name: ''
      },
      columns: [
        {
          title: this.$t('acl.username'),
          dataIndex: 'username',
          sorter: false,
          width: 150,
          scopedSlots: {
            customRender: 'usernameSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.username && record.username.toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus()
              }, 0)
            }
          }
        },
        {
          title: this.$t('acl.nickname'),
          dataIndex: 'nickname',
          sorter: false,
          width: 150,
          scopedSlots: {
            customRender: 'nicknameSearchRender',
            filterDropdown: 'filterDropdown',
            filterIcon: 'filterIcon'
          },
          onFilter: (value, record) => record.nickname && record.nickname.toLowerCase().includes(value.toLowerCase()),
          onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
              setTimeout(() => {
                this.searchInput.focus()
              }, 0)
            }
          }
        },
        {
          title: this.$t('acl.department'),
          dataIndex: 'department',
          width: 100,
          sorter: false,
          scopedSlots: { customRender: 'department' }

        },
        {
          title: this.$t('acl.catalog'),
          dataIndex: 'catalog',
          sorter: false,
          width: 100,
          scopedSlots: { customRender: 'catalog' }

        },
        {
          title: this.$t('acl.email'),
          dataIndex: 'email',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'email' }

        },
        {
          title: this.$t('acl.mobile'),
          dataIndex: 'mobile',
          sorter: false,
          width: 150,
          scopedSlots: { customRender: 'mobile' }

        },
        {
          title: this.$t('acl.joinedAt'),
          dataIndex: 'date_joined',
          sorter: false,
          width: 200,
          scopedSlots: { customRender: 'date_joined' }

        },
        {
          title: this.$t('acl.block'),
          dataIndex: 'block',
          width: 100,
          scopedSlots: { customRender: 'block' }
        },
        {
          title: this.$t('tip.operate'),
          dataIndex: 'action',
          width: 150,
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        parameter.page = parameter.pageNo
        parameter.page_size = parameter.pageSize
        delete parameter.pageNo
        delete parameter.pageSize
        Object.assign(parameter, this.queryParam)

        return searchUser(parameter)
          .then(res => {
            res.pageNo = res.page
            res.pageSize = res.total
            res.totalCount = res.numfound
            res.totalPage = Math.ceil(res.numfound / parameter.pageSize)
            res.data = res.users

            this.allUsers = res.users
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
    },
    cancel () {
      return false
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

    handleEdit (record) {
      this.$refs.userForm.handleEdit(record)
    },
    handleDelete (record) {
      this.deleteUser(record.uid)
    },
    handleOk () {
      this.$refs.table.refresh()
    },

    handleCreate () {
      this.$refs.userForm.handleCreate()
    },

    deleteUser (attrId) {
      deleteUserById(attrId)
        .then(res => {
          this.$message.success(this.$t('tip.deleteSuccess'))
          this.handleOk()
        })
        .catch(err => this.requestFailed(err))
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
    padding: 0;
  }
  .ant-table-body {
  overflow: auto;
  }
  .ant-table-content{
    overflow: auto;
  }
</style>
