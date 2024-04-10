<template>
  <CustomDrawer :closable="true" :visible="visible" width="500px" @close="handleClose" :title="$t('acl.groupUser')">
    <a-form-item :label="$t('acl.addUser')" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
      <a-row>
        <a-col span="15">
          <el-select
            v-model="selectedChildrenRole"
            multiple
            collapse-tags
            size="small"
            filterable
            :placeholder="$t('placeholder2')">
            <el-option
              class="drop-down-render"
              v-for="role in allRoles"
              :key="role.id"
              :value="role.id"
              :label="role.name"
            ></el-option>
          </el-select>
        </a-col>
        <a-col span="5" offset="1">
          <a-button style="display: inline-block" @click="handleAddRole">{{ $t('confirm') }}</a-button>
        </a-col>
      </a-row>
    </a-form-item>
    <a-card>
      <a-row :gutter="24" v-for="(record, index) in records" :key="record.id" :style="{ marginBottom: '5px' }">
        <a-col :span="20">{{ index + 1 }}、{{ record.nickname }}</a-col>
        <a-col
          :span="4"
        ><a-button type="danger" size="small" @click="handleRevokeUser(record)">{{
          $t('acl.remove')
        }}</a-button></a-col
        >
      </a-row>
    </a-card>
  </CustomDrawer>
</template>

<script>
import { getUsersUnderRole, delParentRole, addBatchParentRole } from '@/modules/acl/api/role'
import { Select, Option } from 'element-ui'
export default {
  name: 'UsersUnderRoleForm',
  components: { ElSelect: Select, ElOption: Option },
  props: {
    allRoles: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      visible: false,
      records: [],
      roleId: 0,
      selectedChildrenRole: [],
    }
  },
  mounted() {},
  methods: {
    handleClose() {
      this.visible = false
    },
    loadRecords(roleId) {
      getUsersUnderRole(roleId, { app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.records = res['users']
      })
      // .catch(err=> this.$httpError(err))
    },
    handleProcessRole(roleId) {
      this.roleId = roleId
      this.visible = true
      this.loadRecords(roleId)
    },
    async handleAddRole() {
      await addBatchParentRole(this.roleId, {
        child_ids: this.selectedChildrenRole,
        app_id: this.$route.name.split('_')[0],
      })
      this.loadRecords(this.roleId)
      this.$message.success(this.$t('addSuccess'))
      this.selectedChildrenRole = []
    },
    handleRevokeUser(record) {
      const that = this
      this.$confirm({
        content: that.$t('acl.deleteUserConfirm'),
        onOk() {
          delParentRole(record.role.id, that.roleId, { app_id: that.$route.name.split('_')[0] }).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadRecords(that.roleId)
          })
          // .catch(err=>that.$httpError(err))
        },
      })
    },
  },
}
</script>
