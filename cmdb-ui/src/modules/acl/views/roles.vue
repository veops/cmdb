<template>
  <div class="acl-role">
    <div class="roles-action-btn">
      <a-button @click="handleCreate" type="primary">{{ btnName }}</a-button>
      <a-input-search
        class="ops-input"
        allowClear
        :style="{ display: 'inline', marginLeft: '10px', width: '200px' }"
        placeholder="搜索 | 角色名"
        v-model="searchName"
        @search="
          () => {
            this.tablePage.currentPage = 1
            this.loadData()
          }
        "
      ></a-input-search>
      <a-checkbox :checked="is_all" @click="handleClickBoxChange">所有角色</a-checkbox>
    </div>
    <a-spin :spinning="loading">
      <vxe-table
        stripe
        class="ops-stripe-table"
        size="mini"
        resizable
        :data="tableData"
        :max-height="`${windowHeight - 185}px`"
        highlight-hover-row
        min-height="300px"
        :filter-config="{ remote: true }"
        @filter-change="filterTableMethod"
      >

        <vxe-table-column
          field="name"
          title="角色名"
          :min-width="150"
          align="left"
          fixed="left"
          sortable
          show-overflow>
        </vxe-table-column>

        <!-- 2 -->
        <vxe-table-column field="is_app_admin" title="管理员" :min-width="100" align="center">
          <template #default="{row}">
            <a-icon type="check" v-if="row.is_app_admin" />
          </template>
        </vxe-table-column>

        <vxe-table-column field="id" title="继承自" :min-width="150">
          <template #default="{row}">
            <a-tag color="cyan" v-for="role in id2parents[row.id]" :key="role.id">{{ role.name }}</a-tag>
          </template>
        </vxe-table-column>

        <vxe-table-column
          field="uid"
          title="虚拟角色"
          :min-width="100"
          align="center"
          :filters="[
            { label: '是', value: 1 },
            { label: '否', value: 0 },
          ]"
          :filterMultiple="false"
          :filter-method="({ value, row }) => {
            return value === !row.uid
          }">
          <template #default="{row}">
            {{ row.uid ? '否' : '是' }}
          </template>

        </vxe-table-column>

        <vxe-table-column field="action" title="操作" :min-width="150" fixed="right">
          <template #default="{row}">
            <div style="width:300px">
              <span>
                <a-tooltip title="资源列表">
                  <a
                    v-if="$route.name !== 'acl_roles'"
                    @click="handleDisplayUserResource(row)"
                  ><a-icon
                    type="file-search"
                  /></a>
                </a-tooltip>
                <a-divider type="vertical" />
                <div v-if="!row.uid" style="display: inline-block">
                  <a-tooltip
                    title="用户列表"
                  ><a @click="handleDisplayUserUnderRole(row)"><a-icon type="team"/></a
                  ></a-tooltip>
                  <a-divider type="vertical" />
                </div>
                <a @click="handleEdit(row)"><a-icon type="edit"/></a>
                <a-divider type="vertical" />
                <a-popconfirm title="确认删除?" @confirm="handleDelete(row)" @cancel="cancel" okText="是" cancelText="否">
                  <a style="color: red"><a-icon type="delete"/></a>
                </a-popconfirm>
              </span>
            </div>
          </template>
        </vxe-table-column>

        <template slot="empty">
          <img :src="require(`@/assets/data_empty.png`)" />
          <p style="font-size: 14px; line-height: 17px; color: rgba(0, 0, 0, 0.6)">暂无数据</p>
        </template>
      </vxe-table>
      <vxe-pager
        size="mini"
        :layouts="['Total', 'PrevPage', 'JumpNumber', 'NextPage', 'Sizes']"
        :current-page.sync="tablePage.currentPage"
        :page-size.sync="tablePage.pageSize"
        :total="tablePage.total"
        :page-sizes="pageSizeOptions"
        @page-change="handlePageChange"
      >
      </vxe-pager>
    </a-spin>

    <roleForm ref="roleForm" :allRoles="allRoles" :id2parents="id2parents" :handleOk="handleOk"></roleForm>
    <resource-user-form ref="ruf"></resource-user-form>
    <users-under-role-form ref="usersUnderRoleForm" :allRoles="allRoles"></users-under-role-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import roleForm from './module/roleForm'
import resourceUserForm from './module/resourceUserForm'
import usersUnderRoleForm from './module/usersUnderRoleForm'
import { deleteRoleById, searchRole } from '@/modules/acl/api/role'

export default {
  name: 'Roles',
  components: {
    roleForm,
    resourceUserForm,
    usersUnderRoleForm,
  },
  data() {
    return {
      loading: false,
      tablePage: {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      },
      tableColumns: [
        {
          title: '角色名',
          field: 'name',
          sortable: true,
          minWidth: '150px',
          fixed: 'left',
          showOverflow: 'tooltip',
        },
        {
          title: '管理员',
          field: 'is_app_admin',
          minWidth: '100px',
          align: 'center',
          slots: { default: 'is_app_admin_default' },
        },
        {
          title: '继承自',
          field: 'id',
          minWidth: '150px',
          slots: { default: 'inherit_default' },
        },
        {
          title: '虚拟角色',
          field: 'uid',
          minWidth: '100px',
          align: 'center',
          filters: [
            { label: '是', value: 1 },
            { label: '否', value: 0 },
          ],
          filterMultiple: false,
          filterMethod: ({ value, row }) => {
            return value === !row.uid
          },
          slots: { default: 'isVisualRole_default' },
        },
        {
          title: '操作',
          minWidth: '280px',
          field: 'action',
          fixed: 'right',
          slots: { default: 'action_default' },
        },
      ],
      btnName: '新增虚拟角色',
      is_all: this.$route.name === 'acl_roles',
      tableData: [],
      allRoles: [],
      id2parents: {},
      pageSizeOptions: [10, 25, 50, 100],
      searchName: '',
      filterTableValue: { user_role: 1, user_only: 0 },
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  watch: {
    '$route.name': function(newName, oldName) {
      this.tablePage = {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      }
      this.tableData = []
      this.allRoles = []
      this.loadData()
      this.initData()
    },
    searchName: {
      immediate: true,
      handler(newVal) {
        if (!newVal) {
          this.tablePage.currentPage = 1
          this.loadData()
        }
      },
    },
  },
  mounted() {
    this.initData()
  },
  inject: ['reload'],
  methods: {
    handleClickBoxChange() {
      this.is_all = !this.is_all
      this.$nextTick(() => {
        this.tablePage.currentPage = 1
        this.loadData()
      })
    },
    initData() {
      console.log(111)
      searchRole({
        app_id: this.$route.name.split('_')[0],
        page_size: 9999,
      }).then((res) => {
        this.allRoles = res.roles
      })
    },
    loadData() {
      console.log(222)
      this.loading = true
      const { currentPage, pageSize } = this.tablePage
      searchRole({
        ...this.filterTableValue,
        app_id: this.$route.name.split('_')[0],
        page_size: pageSize,
        page: currentPage,
        is_all: this.is_all,
        q: this.searchName,
      })
        .then((res) => {
          this.tableData = res.roles
          this.id2parents = res.id2parents
          this.tablePage.total = res.numfound
          this.loading = false
        })
        .catch(() => {
          this.loading = false
        })
    },
    handleDisplayUserResource(record) {
      this.$refs.ruf.loadUserResource(record)
    },
    handleDisplayUserUnderRole(record) {
      this.$refs.usersUnderRoleForm.handleProcessRole(record.id)
    },
    handleEdit(record) {
      this.$refs.roleForm.handleEdit(record)
    },
    handleDelete(record) {
      this.deleteRole(record.id)
    },
    handleOk() {
      this.loadData()
      this.initData()
    },

    handleCreate() {
      this.$refs.roleForm.handleCreate()
    },

    deleteRole(id) {
      deleteRoleById(id, { app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.$message.success(`删除成功`)
        this.handleOk()
      })
      // .catch(err => this.requestFailed(err))
    },
    // requestFailed(err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
    cancel(e) {
      return false
    },
    handlePageChange({ currentPage, pageSize }) {
      this.tablePage.currentPage = currentPage
      this.tablePage.pageSize = pageSize
      this.loadData()
    },
    filterTableMethod({ column, property, values, datas, filterList, $event }) {
      if (property === 'uid') {
        if (values[0] === 1) {
          this.filterTableValue = { user_role: 0 }
        } else if (values[0] === 0) {
          this.filterTableValue = {
            user_only: 1,
          }
        } else {
          this.filterTableValue = {
            user_role: 1,
            user_only: 0,
          }
        }
      }
      this.tablePage.currentPage = 1
      this.loadData()
    },
  },
}
</script>

<style lang="less">
.acl-role {
  background-color: #fff;
  padding: 24px;
  .roles-action-btn {
    width: 100%;
    display: inline-flex;
    margin-bottom: 15px;
    align-items: center;
    .ant-checkbox-wrapper {
      margin-left: auto;
    }
  }
  .vxe-table--filter-body {
    min-height: 60px;
  }
}
</style>
