<template>
  <CustomDrawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="500px"
  >
    <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item label="类型名">
        <a-input
          name="name"
          placeholder="类型名称"
          v-decorator="['name', { rules: [{ required: true, message: '请输入类型名' }] }]"
        />
      </a-form-item>

      <a-form-item label="描述">
        <a-textarea
          placeholder="请输入描述信息..."
          name="description"
          :rows="4"
          v-decorator="['description', { rules: [] }]"
        />
      </a-form-item>

      <a-form-item label="权限">
        <a-select mode="tags" v-model="perms" style="width: 100%" placeholder="请输入权限名..."> </a-select>
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
import { addResourceType, updateResourceTypeById } from '@/modules/acl/api/resource'

export default {
  name: 'ResourceForm',
  data() {
    return {
      drawerTitle: '新增资源类型',
      drawerVisible: false,
      perms: [],
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  computed: {},
  mounted() {},
  methods: {
    handleCreate() {
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.perms = []
      this.drawerVisible = false
    },
    onChange(e) {
      console.log(`checked = ${e}`)
    },

    handleEdit(record) {
      this.drawerVisible = true
      console.log(record)
      this.perms = record.perms
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          description: record.description,
        })
      })
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)

          values.app_id = this.$route.name.split('_')[0]
          values.perms = this.perms
          if (values.id) {
            this.updateResourceType(values.id, values)
          } else {
            this.createResourceType(values)
          }
        }
      })
    },
    updateResourceType(id, data) {
      updateResourceTypeById(id, data).then((res) => {
        this.$message.success(`更新成功`)
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },

    createResourceType(data) {
      addResourceType(data).then((res) => {
        this.$message.success(`添加成功`)
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },

    // requestFailed (err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // }
  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null,
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
