<template>
  <CustomDrawer
    :title="$t('acl.convenient')"
    width="500px"
    :maskClosable="false"
    :closable="true"
    :visible="visible"
    @close="handleClose"
  >
    <a-form :form="form">
      <a-form-item>
        <div slot="label" style="display: inline-block">
          <span>{{ $t('acl.roleList') }}</span>
          <a-divider type="vertical" />
          <a-switch
            style="display: inline-block"
            :checked-children="$t('user')"
            :un-checked-children="$t('acl.virtual')"
            @change="handleRoleTypeChange"
            v-model="roleType"
          />
        </div>
        <el-select
          :style="{ width: '100%' }"
          size="small"
          v-decorator="['roleIdList', { rules: [{ required: true, message: $t('acl.role_placeholder2') }] }]"
          multiple
          filterable
          :placeholder="$t('acl.role_placeholder3')"
        >
          <el-option v-for="role in allRoles" :key="role.id" :value="role.id" :label="role.name"></el-option>
        </el-select>
      </a-form-item>

      <a-form-item :label="$t('acl.permissionList')">
        <el-select
          :style="{ width: '100%' }"
          size="small"
          name="permName"
          v-decorator="['permName', { rules: [{ required: true, message: this.$t('acl.permission_placeholder') }] }]"
          multiple
          :placeholder="this.$t('acl.permission_placeholder')"
        >
          <el-option v-for="perm in allPerms" :key="perm.name" :value="perm.name" :label="perm.name"></el-option>
        </el-select>
      </a-form-item>
      <a-form-item :label="$t('acl.resourceName')">
        <a-textarea
          v-decorator="['resource_names', { rules: [{ required: true, message: $t('acl.resourceBatchTips') }] }]"
          :autoSize="{ minRows: 4 }"
          :placeholder="$t('acl.resourceBatchTips')"
        />
      </a-form-item>
      <div class="custom-drawer-bottom-action">
        <a-button @click="handleRevoke" type="danger" ghost>{{ $t('acl.revoke') }}</a-button>
        <a-button @click="handleSubmit" type="primary">{{ $t('grant') }}</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>

<script>
import { Select, Option } from 'element-ui'
import { searchRole } from '@/modules/acl/api/role'
import {
  getResourceTypePerms,
  setBatchRoleResourceByResourceName,
  setBatchRoleResourceRevokeByResourceName,
} from '@/modules/acl/api/permission'
export default {
  name: 'ResourceBatchPerm',
  components: { ElSelect: Select, ElOption: Option },
  data() {
    return {
      visible: false,
      resource_type_id: null,
      roleType: true,
      allRoles: [],
      allPerms: [],
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  methods: {
    open(currentTypeId) {
      this.visible = true
      this.resource_type_id = currentTypeId
      this.loadRoles(1)
      this.loadPerm(currentTypeId)
    },
    handleClose() {
      this.form.resetFields()
      this.roleType = true
      this.visible = false
    },
    handleRoleTypeChange(target) {
      this.loadRoles(Number(target))
    },
    loadRoles(isUserRole) {
      searchRole({ page_size: 9999, app_id: this.$route.name.split('_')[0], user_role: isUserRole }).then((res) => {
        this.allRoles = res.roles
      })
    },
    loadPerm(resourceTypeId) {
      getResourceTypePerms(resourceTypeId).then((res) => {
        this.allPerms = res
      })
    },
    handleSubmit() {
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log(values)
          values.roleIdList.forEach((roleId) => {
            setBatchRoleResourceByResourceName(roleId, {
              resource_names: values.resource_names.split('\n'),
              perms: values.permName,
              resource_type_id: this.resource_type_id,
            }).then((res) => {
              this.$message.success(this.$t('operateSuccess'))
              this.form.resetFields()
            })
          })
        }
      })
    },
    handleRevoke() {
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log(values)
          values.roleIdList.forEach((roleId) => {
            setBatchRoleResourceRevokeByResourceName(roleId, {
              resource_names: values.resource_names.split('\n'),
              perms: values.permName,
              resource_type_id: this.resource_type_id,
            }).then((res) => {
              this.$message.success(this.$t('operateSuccess'))
              this.form.resetFields()
            })
          })
        }
      })
    },
  },
}
</script>

<style></style>
