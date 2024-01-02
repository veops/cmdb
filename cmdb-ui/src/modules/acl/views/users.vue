<template>
  <div class="acl-users">
    <div class="acl-users-header">
      <a-button v-if="isAclAdmin" @click="handleCreate" type="primary">{{ btnName }}</a-button>
      <a-input-search
        class="ops-input"
        allowClear
        :style="{ width: '300px', display: 'inline', marginLeft: '10px' }"
        :placeholder="`${$t('search')} | ${$t('acl.nickname')} 、 ${$t('acl.username')}`"
        v-model="searchName"
      ></a-input-search>
    </div>
    <a-spin :spinning="loading">
      <vxe-grid
        stripe
        class="ops-stripe-table"
        :columns="tableColumns"
        :data="tableData"
        show-overflow
        highlight-hover-row
        :height="`${windowHeight - 165}px`"
        size="small"
      >
        <template #block_default="{row}">
          <a-icon type="lock" v-if="row.block" />
        </template>
        <template #action_default="{row}">
          <a-space>
            <a :disabled="isAclAdmin ? false : true" @click="handleEdit(row)">
              <a-icon type="edit" />
            </a>
            <a-tooltip :title="$t('acl.summaryPermissions')">
              <a @click="handlePermCollect(row)"><a-icon type="solution"/></a>
            </a-tooltip>
            <a-popconfirm :title="$t('confirmDelete')" @confirm="deleteUser(row.uid)">
              <a :style="{ color: 'red' }"><ops-icon type="icon-xianxing-delete"/></a>
            </a-popconfirm>
          </a-space>
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
      onDutuUids: [],
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
    await this.getOnDutyUser()
    this.search()
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
    tableColumns() {
      return [
        {
          title: this.$t('acl.username'),
          field: 'username',
          sortable: true,
          minWidth: '100px',
          fixed: 'left',
        },
        {
          title: this.$t('acl.nickname'),
          field: 'nickname',
          minWidth: '100px',
        },
        {
          title: this.$t('acl.joined_at'),
          field: 'date_joined',
          minWidth: '160px',
          align: 'center',
          sortable: true,
        },
        {
          title: this.$t('acl.block'),
          field: 'block',
          width: '150px',
          align: 'center',
          slots: {
            default: 'block_default',
          },
        },
        {
          title: this.$t('operation'),
          field: 'action',
          width: '150px',
          fixed: 'right',
          align: 'center',
          slots: {
            default: 'action_default',
          },
        },
      ]
    },
    btnName() {
      return this.$t('acl.addUser')
    },
  },
  watch: {
    searchName: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal) {
          this.tableData = this.allUsers.filter(
            (item) =>
              (item.username && item.username.toLowerCase().includes(newVal.toLowerCase())) ||
              (item.nickname && item.nickname.toLowerCase().includes(newVal.toLowerCase()))
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
    async getOnDutyUser() {
      await getOnDutyUser().then((res) => {
        this.onDutuUids = res.map((i) => i.uid)
      })
    },
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
    async handleOk() {
      this.searchName = ''
      await this.getOnDutyUser()
      this.search()
    },
    handleCreate() {
      this.$refs.userForm.handleCreate()
    },
    deleteUser(uid) {
      deleteUserById(uid).then((res) => {
        this.$message.success(this.$t('deleteSuccess'))
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
