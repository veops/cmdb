<template>
  <CustomDrawer
    title="便捷授权"
    width="500px"
    :maskClosable="false"
    :closable="true"
    :visible="visible"
    @close="handleClose"
  >
    <a-form :form="form">
      <a-form-item>
        <div slot="label" style="display: inline-block">
          <span>角色列表</span>
          <a-divider type="vertical" />
          <a-switch
            style="display: inline-block"
            checked-children="用户"
            un-checked-children="虚拟"
            @change="handleRoleTypeChange"
            v-model="roleType"
          />
        </div>
        <el-select
          :style="{ width: '100%' }"
          size="small"
          v-decorator="['roleIdList', { rules: [{ required: true, message: '请选择角色名称' }] }]"
          multiple
          filterable
          placeholder="请选择角色名称，可多选！"
        >
          <el-option v-for="role in allRoles" :key="role.id" :value="role.id" :label="role.name"></el-option>
        </el-select>
      </a-form-item>

      <a-form-item label="权限列表">
        <el-select
          :style="{ width: '100%' }"
          size="small"
          name="permName"
          v-decorator="['permName', { rules: [{ required: true, message: '请选择权限' }] }]"
          multiple
          placeholder="请选择权限，可多选！"
        >
          <el-option v-for="perm in allPerms" :key="perm.name" :value="perm.name" :label="perm.name"></el-option>
        </el-select>
      </a-form-item>
      <a-form-item label="资源名">
        <a-textarea
          v-decorator="['resource_names', { rules: [{ required: true, message: '请输入资源名，换行分隔' }] }]"
          :autoSize="{ minRows: 4 }"
          placeholder="请输入资源名，换行分隔"
        />
      </a-form-item>
      <div class="custom-drawer-bottom-action">
        <a-button @click="handleRevoke" type="danger" ghost>权限回收</a-button>
        <a-button @click="handleSubmit" type="primary">授权</a-button>
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
      searchRole({ page_size: 9999, app_id: this.$route.name.split('_')[0], user_role: isUserRole }).then(res => {
        this.allRoles = res.roles
      })
    },
    loadPerm(resourceTypeId) {
      getResourceTypePerms(resourceTypeId).then(res => {
        this.allPerms = res
      })
    },
    handleSubmit() {
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log(values)
          values.roleIdList.forEach(roleId => {
            setBatchRoleResourceByResourceName(roleId, {
              resource_names: values.resource_names.split('\n'),
              perms: values.permName,
              resource_type_id: this.resource_type_id,
            }).then(res => {
              this.$message.success('授权成功')
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
          values.roleIdList.forEach(roleId => {
            setBatchRoleResourceRevokeByResourceName(roleId, {
              resource_names: values.resource_names.split('\n'),
              perms: values.permName,
              resource_type_id: this.resource_type_id,
            }).then(res => {
              this.$message.success('权限回收成功')
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
