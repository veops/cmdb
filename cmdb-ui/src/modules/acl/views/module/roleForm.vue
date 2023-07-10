<template>
  <CustomDrawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="500px"
  >
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }" @submit="handleSubmit">
      <a-form-item label="角色名">
        <a-input
          name="name"
          placeholder="角色名"
          v-decorator="['name', { rules: [{ required: true, message: '请输入角色名' }] }]"
        />
      </a-form-item>
      <a-form-item v-if="$route.name.split('_')[0] !== 'acl'" label="密码">
        <a-input name="password" placeholder="密码" v-decorator="['password', { rules: [{ required: false }] }]" />
      </a-form-item>
      <!-- <a-form-item label="继承自">
        <a-select
          showSearch
          v-model="selectedParents"
          :filterOption="false"
          placeholder="可选择继承角色"
          mode="multiple"
        >
          <a-select-option v-for="role in scrollData" :key="role.id">{{ role.name }}</a-select-option>
        </a-select>
      </a-form-item> -->
      <a-form-item label="继承自">
        <el-select
          :style="{ width: '100%' }"
          size="small"
          v-model="selectedParents"
          multiple
          filterable
          placeholder="可选择继承角色"
        >
          <el-option v-for="role in allRoles" :key="role.id" :value="role.id" :label="role.name"></el-option>
        </el-select>
      </a-form-item>
      <a-form-item label="是否应用管理员">
        <a-switch
          @change="onChange"
          name="is_app_admin"
          v-decorator="['is_app_admin', { rules: [], valuePropName: 'checked' }]"
        />
      </a-form-item>
      <a-form-item>
        <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
      </a-form-item>

      <div class="custom-drawer-bottom-action">
        <a-button @click="onClose">取消</a-button>
        <a-button @click="handleSubmit" type="primary">确定</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>

<script>
import { Select, Option } from 'element-ui'
import { addRole, updateRoleById, delParentRole, addBatchParentRole } from '@/modules/acl/api/role'

export default {
  name: 'RoleForm',
  components: {
    ElSelect: Select,
    ElOption: Option,
  },
  data() {
    return {
      drawerTitle: '',
      current_id: 0,
      drawerVisible: false,
      selectedParents: [],
      oldParents: [],
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  computed: {},
  mounted() {
    console.log(this.$route)
  },
  methods: {
    // filterOption(input, option) {
    //   return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    // },
    handleCreate() {
      this.drawerTitle = '新增角色'
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.selectedParents = []
      this.oldParents = []
      this.drawerVisible = false
    },
    onChange(e) {
      console.log(`checked = ${e}`)
    },

    handleEdit(record) {
      this.drawerTitle = `编辑：${record.name}`
      this.drawerVisible = true
      this.current_id = record.id
      const _parents = this.id2parents[record.id]
      if (_parents) {
        _parents.forEach((item) => {
          this.selectedParents.push(item.id)
          this.oldParents.push(item.id)
        })
      }
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          is_app_admin: record.is_app_admin,
        })
      })
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.app_id = this.$route.name.split('_')[0]
          if (values.id) {
            this.updateRole(values.id, values)
          } else {
            this.createRole(values)
          }
        }
      })
    },
    updateRole(id, data) {
      this.updateParents(id)
      updateRoleById(id, { ...data, app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.$message.success(`更新成功`)
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },

    createRole(data) {
      addRole({ ...data, app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.$message.success(`添加成功`)
        this.updateParents(res.id)
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },
    updateParents(id) {
      this.oldParents.forEach((item) => {
        if (!this.selectedParents.includes(item)) {
          delParentRole(id, item, { app_id: this.$route.name.split('_')[0] })
          // .catch(err => this.requestFailed(err))
        }
      })
      this.selectedParents.forEach((item) => {
        if (!this.oldParents.includes(item)) {
          addBatchParentRole(item, {
            child_ids: [id],
            app_id: this.$route.name.split('_')[0],
          })
          // addParentRole(id, item, { app_id: this.$route.name.split('_')[0] })
          // .catch(err => this.requestFailed(err))
        }
      })
    },
    // requestFailed(err) {
    //   console.log(err)
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null,
    },
    allRoles: {
      type: Array,
      required: true,
    },
    id2parents: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}

.fold {
  width: calc(100% - 216px);
  display: inline-block;
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
