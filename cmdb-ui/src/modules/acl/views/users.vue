<template>
  <div class="acl-users">
    <div class="acl-users-header">
      <a-button v-if="isAclAdmin" @click="handleCreate" type="primary">{{ btnName }}</a-button>
      <a-input-search
        class="ops-input"
        allowClear
        :style="{ display: 'inline', marginLeft: '10px' }"
        placeholder="搜索 | 用户名、中文名"
        v-model="searchName"
      ></a-input-search>
    </div>
    <a-spin :spinning="loading">
      <vxe-grid
        stripe
        class="ops-stripe-table"
        :columns="tableColumns"
        :data="tableData"
        highlight-hover-row
        :height="`${windowHeight - 165}px`"
        size="small"
      >
        <template #block_default="{row}">
          <a-icon type="lock" v-if="row.block" />
        </template>
        <template #action_default="{row}">
          <template>
            <a :disabled="isAclAdmin ? false : true" @click="handleEdit(row)">
              <a-icon type="edit" />
            </a>
            <a-divider type="vertical" />
            <a-tooltip title="权限汇总">
              <a @click="handlePermCollect(row)"><a-icon type="solution"/></a>
            </a-tooltip>
          </template>
        </template>
      </vxe-grid>
    </a-spin>
    <userForm ref="userForm" :handleOk="handleOk"> </userForm>
    <perm-collect-form ref="permCollectForm"></perm-collect-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import userForm from './module/userForm'
import PermCollectForm from './module/permCollectForm'
import { deleteUserById, searchUser, getOnDutyUser } from '@/modules/acl/api/user'

export default {
  name: 'Users',
  components: {
    userForm,
    PermCollectForm,
  },
  data() {
    return {
      loading: false,
      tableColumns: [
        {
          title: '用户名',
          field: 'username',
          sortable: true,
          minWidth: '100px',
          fixed: 'left',
        },
        {
          title: '中文名',
          field: 'nickname',
          minWidth: '100px',
        },
        {
          title: '加入时间',
          field: 'date_joined',
          minWidth: '160px',
        },
        {
          title: '锁定',
          field: 'block',
          minWidth: '100px',
          slots: {
            default: 'block_default',
          },
        },
        {
          title: '操作',
          field: 'action',
          minWidth: '180px',
          fixed: 'right',
          slots: {
            default: 'action_default',
          },
        },
      ],
      onDutuUids: [],
      btnName: '新增用户',
      allUsers: [],
      tableData: [],
      searchName: '',
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  async beforeMount() {
    this.loading = true
    await getOnDutyUser().then((res) => {
      this.onDutuUids = res.map((i) => i.uid)
      this.search()
    })
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    isAclAdmin: function() {
      if (this.$store.state.user.roles.permissions.filter((item) => item === 'acl_admin').length > 0) {
        return true
      } else {
        return false
      }
    },
  },
  watch: {
    searchName: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal) {
          this.tableData = this.allUsers.filter(
            (item) =>
              item.username.toLowerCase().includes(newVal.toLowerCase()) ||
              item.nickname.toLowerCase().includes(newVal.toLowerCase())
          )
        } else {
          this.tableData = this.allUsers
        }
      },
    },
  },
  mounted() {},
  inject: ['reload'],

  methods: {
    search() {
      searchUser({ page_size: 10000 }).then((res) => {
        const ret = res.users.filter((u) => this.onDutuUids.includes(u.uid))
        this.allUsers = ret
        this.tableData = ret
        this.loading = false
      })
    },
    handlePermCollect(record) {
      this.$refs['permCollectForm'].collect(record)
    },
    handleEdit(record) {
      this.$refs.userForm.handleEdit(record)
    },
    handleDelete(record) {
      this.deleteUser(record.uid)
    },
    handleOk() {
      this.searchName = ''
      this.search()
    },
    handleCreate() {
      this.$refs.userForm.handleCreate()
    },
    deleteUser(attrId) {
      deleteUserById(attrId).then((res) => {
        this.$message.success(`删除成功`)
        this.handleOk()
      })
    },
  },
}
</script>

<style lang="less" scoped>
.acl-users {
  border-radius: 15px;
  background-color: #fff;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 24px;
  .acl-users-header {
    display: inline-flex;
    margin-bottom: 15px;
  }
}
</style>
