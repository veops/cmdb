<template>
  <CustomDrawer :title="title" width="500px" :closable="false" :visible="visible" @close="closeForm">
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
      <div class="custom-drawer-bottom-action">
        <a-button @click="closeForm">取消</a-button>
        <a-button @click="handleSubmit" type="primary" :loading="loading">确定</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>
<script>
import { Select, Option } from 'element-ui'
import { searchRole } from '@/modules/acl/api/role'
import {
  getResourceTypePerms,
  setRoleResourcePerm,
  setRoleResourceGroupPerm,
  setBatchRoleResourcePerm,
  setBatchRoleResourceGroupPerm,
  setBatchRoleResourceRevoke,
  setBatchRoleResourceGroupRevoke,
} from '@/modules/acl/api/permission'

export default {
  name: 'ResourcePermManageForm',
  components: { ElSelect: Select, ElOption: Option },
  data() {
    return {
      isGroup: false,
      allRoles: [],
      allPerms: [],
      visible: false,
      instance: {} || [], // 当前对象or批量授权的数组
      type: 'grant', // grant or revoke
      title: '',
      loading: false,
    }
  },
  props: {
    groupTypeMessage: {
      required: true,
      type: Object,
    },
  },
  computed: {},
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  mounted() {
    this.loadRoles(1)
  },
  methods: {
    handleRoleTypeChange(target) {
      if (!target) {
        this.loadRoles(1)
      } else {
        this.loadRoles(0)
      }
    },
    loadRoles(isUserRole) {
      searchRole({ page_size: 9999, app_id: this.$route.name.split('_')[0], user_role: isUserRole }).then((res) => {
        this.allRoles = res.roles
      })
      // .catch(err => this.requestFailed(err))
    },
    loadPerm(resourceTypeId) {
      getResourceTypePerms(resourceTypeId).then((res) => {
        this.allPerms = res
      })
      // .catch(err => this.requestFailed(err))
    },
    closeForm() {
      this.visible = false
      this.form.resetFields()
      this.$emit('close')
    },
    editPerm(record, isGroup, type = 'grant') {
      this.isGroup = isGroup
      this.visible = true
      this.instance = record
      this.type = type
      if (Array.isArray(record)) {
        this.loadPerm(record[0]['resource_type_id'])
        this.title = `${type === 'grant' ? '批量授权' : '批量权限回收'}`
      } else {
        this.title = `添加授权：${record.name}`
        this.loadPerm(record['resource_type_id'])
      }
    },
    // requestFailed(err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.roleIdList.forEach((roleId) => {
            const params = { perms: values.permName, app_id: this.$route.name.split('_')[0] }
            this.loading = true
            if (!this.isGroup) {
              if (Array.isArray(this.instance)) {
                // const promises = this.instance.map(item => {
                //   return setRoleResourcePerm(roleId, item.id, params)
                // })
                // Promise.all(promises).then(() => {
                //   this.$message.success('添加授权成功')
                // })
                if (this.type === 'grant') {
                  setBatchRoleResourcePerm(roleId, { ...params, resource_ids: this.instance.map((a) => a.id) })
                    .then((res) => {
                      this.$message.success('添加授权成功')
                    })
                    .finally(() => {
                      this.loading = false
                    })
                } else {
                  setBatchRoleResourceRevoke(roleId, { ...params, resource_ids: this.instance.map((a) => a.id) })
                    .then((res) => {
                      this.$message.success('批量权限回收成功')
                    })
                    .finally(() => {
                      this.loading = false
                    })
                }
              } else {
                setRoleResourcePerm(roleId, this.instance.id, params)
                  .then((res) => {
                    this.$message.success('添加授权成功')
                  })
                  .finally(() => {
                    this.loading = false
                  })
              }
            } else {
              if (Array.isArray(this.instance)) {
                // const promises = this.instance.map(item => {
                //   return setRoleResourceGroupPerm(roleId, item.id, params)
                // })
                // Promise.all(promises).then(() => {
                //   this.$message.success('添加授权成功')
                // })
                if (this.type === 'grant') {
                  setBatchRoleResourceGroupPerm(roleId, { ...params, group_ids: this.instance.map((a) => a.id) })
                    .then((res) => {
                      this.$message.success('添加授权成功')
                    })
                    .finally(() => {
                      this.loading = false
                    })
                } else {
                  setBatchRoleResourceGroupRevoke(roleId, {
                    ...params,
                    group_ids: this.instance.map((a) => a.id),
                  })
                    .then((res) => {
                      this.$message.success('批量权限回收成功')
                    })
                    .finally(() => {
                      this.loading = false
                    })
                }
              } else {
                setRoleResourceGroupPerm(roleId, this.instance.id, params)
                  .then((res) => {
                    this.$message.success('添加授权成功')
                  })
                  .finally(() => {
                    this.loading = false
                  })
              }
            }
          })
        }
      })
    },
  },
}
</script>
<style lang="less" scoped></style>
