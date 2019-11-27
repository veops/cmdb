<template>

  <a-modal
    :title="drawerTitle"
    v-model="drawerVisible"
    width="50%"
  >
    <template slot="footer">
      <a-button type="primary" @click="showChildrenDrawer">
        添加权限
      </a-button>
      <a-button key="back" @click="handleCancel">关闭</a-button>
    </template>

    <template>

      <a-list itemLayout="horizontal" :dataSource="resPerms">
        <a-list-item slot="renderItem" slot-scope="item">
          <span>{{ item[0] }}：  </span>
          <div>
            <a-tag color="cyan" v-for="perm in item[1]" :key="perm.rid" closable @close="deletePerm(perm.rid, perm.name)">{{ perm.name }}</a-tag>
          </div>
        </a-list-item>
      </a-list>
    </template>

    <a-drawer
      title="添加权限"
      width="30%"
      :closable="false"
      @close="onChildrenDrawerClose"
      :visible="childrenDrawer"
    >
      <a-form :form="form" @submit="handleSubmit">
        <a-form-item
          label="角色列表"
        >
          <a-select name="roleID" v-decorator="['roleID', {rules: []} ]">
            <a-select-option v-for="role in allRoles" :key="role.id">{{ role.name }}</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item
          label="权限列表"
        >
          <a-select name="permName" v-decorator="['permName', {rules: []} ]">
            <a-select-option v-for="perm in allPerms" :key="perm.name">{{ perm.name }}</a-select-option>
          </a-select>
        </a-form-item>
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
          <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">添加</a-button>
          <a-button @click="onChildrenDrawerClose">取消</a-button>

        </div>

      </a-form>
    </a-drawer>

  </a-modal>

</template>

<script>
import { STable } from '@/components'
import { getResourceTypePerms, getResourcePerms, deleteRoleResourcePerm, setRoleResourcePerm } from '@/api/acl/permission'
import { searchRole } from '@/api/acl/role'

export default {
  name: 'ResourceForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: '权限列表',
      drawerVisible: false,
      record: null,
      allPerms: [],
      resPerms: [],
      roleID: null,
      childrenDrawer: false,
      allRoles: []
    }
  },

  beforeCreate () {
    this.form = this.$form.createForm(this)
  },

  computed: {
  },
  mounted () {
  },
  methods: {
    showChildrenDrawer () {
      this.childrenDrawer = true
    },
    onChildrenDrawerClose () {
      this.childrenDrawer = false
    },
    handlePerm (record) {
      this.drawerVisible = true
      this.record = record
      this.getResPerms(record.id)

      this.$nextTick(() => {
        this.getAllRoles()
        this.getAllPerms(record.resource_type_id)
      })
    },
    getResPerms (resId) {
      getResourcePerms(resId).then(res => {
        var perms = []
        for (var key in res) {
          perms.push([key, res[key]])
        }
        this.resPerms = perms
      })
    },
    getAllPerms (resTypeId) {
      getResourceTypePerms(resTypeId).then(res => {
        this.allPerms = res
      })
    },
    deletePerm (roleID, permName) {
      deleteRoleResourcePerm(roleID, this.record.id, { perms: [permName] }).then(res => {
        this.$message.success(`删除成功`)
        this.handleOk()
      })
        .catch(err => this.requestFailed(err))
    },
    addPerm (roleID, permName) {
      setRoleResourcePerm(roleID, this.record.id, { perms: [permName] }).then(res => {
        this.$message.success(`添加成功`)
        this.handleOk()
      })
        .catch(err => this.requestFailed(err))
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.addPerm(values.roleID, values.permName)
        }
      })
    },
    getAllRoles () {
      searchRole({ page_size: 9999, app_id: this.$store.state.app.name }).then(res => {
        this.allRoles = res.roles
      })
    },
    handleCreate () {
      this.drawerVisible = true
    },
    handleCancel (e) {
      this.drawerVisible = false
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    }

  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null
    }
  }

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

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
