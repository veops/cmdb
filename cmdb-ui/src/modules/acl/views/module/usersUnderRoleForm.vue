<template>
  <CustomDrawer :closable="true" :visible="visible" width="500px" @close="handleClose" title="组用户">
    <a-form-item label="添加用户" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
      <a-row>
        <a-col span="15">
          <el-select v-model="selectedChildrenRole" multiple collapse-tags size="small" filterable>
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
          <a-button style="display: inline-block" @click="handleAddRole">确定</a-button>
        </a-col>
      </a-row>
    </a-form-item>
    <a-card>
      <a-row :gutter="24" v-for="(record, index) in records" :key="record.id" :style="{ marginBottom: '5px' }">
        <a-col :span="20">{{ index + 1 }}、{{ record.nickname }}</a-col>
        <a-col :span="4"><a-button type="danger" size="small" @click="handleRevokeUser(record)">移除</a-button></a-col>
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
    // filterOption(input, option) {
    //   return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    // },
    async handleAddRole() {
      // await this.selectedChildrenRole.forEach(item => {
      //   addParentRole(item, this.roleId, { app_id: this.$route.name.split('_')[0] }).then(res => {
      //     this.$message.success('添加成功')
      //   })
      //   // .catch(err=>{
      //   //   this.$httpError(err)
      //   // })

      // })
      await addBatchParentRole(this.roleId, {
        child_ids: this.selectedChildrenRole,
        app_id: this.$route.name.split('_')[0],
      })
      this.loadRecords(this.roleId)
      this.$message.success('添加完成')
      this.selectedChildrenRole = []
    },
    handleRevokeUser(record) {
      const that = this
      this.$confirm({
        content: '是否确定要移除该用户',
        onOk() {
          delParentRole(record.role.id, that.roleId, { app_id: that.$route.name.split('_')[0] }).then((res) => {
            that.$message.success('删除成功！')
            that.loadRecords(that.roleId)
          })
          // .catch(err=>that.$httpError(err))
        },
      })
    },
  },
}
</script>
