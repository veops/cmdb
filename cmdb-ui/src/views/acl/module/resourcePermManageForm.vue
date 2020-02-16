<template>
  <a-drawer
    :title="$t('acl.addPermTip')+instance.name"
    width="30%"
    :closable="true"
    :visible="visible"
    @close="closeForm"
  >
    <a-form :form="form">
      <a-form-item
        :label="$t('acl.roleList')"
      >
        <a-select
          showSearch
          name="roleIdList"
          v-decorator="['roleIdList', {rules: []} ]"
          mode="multiple"
          :placeholder="$t('acl.selectRoleTip')"
          :filterOption="filterOption">
          <a-select-option v-for="role in allRoles" :key="role.id">{{ role.name }}</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item
        :label="$t('acl.permList')"
      >
        <a-select name="permName" v-decorator="['permName', {rules: []} ]" mode="multiple" :placeholder="$t('acl.selectPermTip')">
          <a-select-option v-for="perm in allPerms" :key="perm.name">{{ perm.name }}</a-select-option>
        </a-select>
      </a-form-item>
      <div class="btn-group">
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('acl.add') }}</a-button>
        <a-button @click="closeForm">{{ $t('button.cancel') }}</a-button>
      </div>

    </a-form>
  </a-drawer>
</template>
<script>
import { searchRole } from '@/api/acl/role'
import { getResourceTypePerms, setRoleResourcePerm } from '@/api/acl/permission'

export default {
  name: 'ResourcePermManageForm',
  data () {
    return {
      allRoles: [],
      allPerms: [],
      visible: false,
      instance: {}
    }
  },
  props: {
    groupTypeMessage: {
      required: true,
      type: Object
    }
  },
  beforeCreate () {
    this.form = this.$form.createForm(this)
  },

  mounted () {
    this.loadRoles()
  },
  methods: {
    loadRoles () {
      searchRole({ page_size: 9999, app_id: this.$route.name.split('_')[0], user_role: 1 }).then(res => {
        this.allRoles = res.roles
      }).catch(err => this.requestFailed(err))
    },
    loadPerm (resourceTypeId) {
      getResourceTypePerms(resourceTypeId).then(res => {
        this.allPerms = res
      }).catch(err => this.requestFailed(err))
    },
    closeForm () {
      this.visible = false
      this.form.resetFields()
    },
    editPerm (record) {
      this.visible = true
      this.instance = record
      this.loadPerm(record['resource_type_id'])
    },
    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
      this.$message.error(`${msg}`)
    },
    filterOption (input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      )
    },
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.roleIdList.forEach(roleId => {
            setRoleResourcePerm(roleId, this.instance.id, { perms: values.permName }).then(
              res => { this.$message.info(this.$t('tip.addSuccess')) }).catch(
              err => this.requestFailed(err))
          })
        }
      })
    }
  }
}
</script>
<style lang="less" scoped>
  .btn-group {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    border-top: 1px solid #e9e9e9;
    padding: 0.8rem 1rem;
    background: #fff;
  }
</style>
