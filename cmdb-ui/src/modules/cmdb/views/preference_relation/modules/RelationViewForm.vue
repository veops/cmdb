<template>
  <CustomDrawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >
    <a-form :form="form" :layout="formLayout" @submit="handleSubmit">
      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="业务关系名">
        <a-input
          name="name"
          placeholder
          v-decorator="['name', { rules: [{ required: true, message: '请输入类型名' }] }]"
        />
      </a-form-item>

      <a-form-item>
        <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
      </a-form-item>

      <div class="custom-drawer-bottom-action">
        <a-button @click="onClose">取消</a-button>
        <a-button @click="handleSubmit" type="primary">提交</a-button>
      </div>
    </a-form>
  </CustomDrawer>
</template>

<script>
import { subscribeRelationView } from '@/modules/cmdb/api/preference'

export default {
  name: 'RelationViewForm',
  data() {
    return {
      drawerTitle: '新增业务关系',
      drawerVisible: false,
      formLayout: 'vertical',
      crIds: [],
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  computed: {
    formItemLayout() {
      const { formLayout } = this
      return formLayout === 'horizontal'
        ? {
            labelCol: { span: 4 },
            wrapperCol: { span: 14 },
          }
        : {}
    },

    horizontalFormItemLayout() {
      return {
        labelCol: { span: 5 },
        wrapperCol: { span: 12 },
      }
    },
    buttonItemLayout() {
      const { formLayout } = this
      return formLayout === 'horizontal'
        ? {
            wrapperCol: { span: 14, offset: 4 },
          }
        : {}
    },
  },
  methods: {
    handleCreate(crIds) {
      this.crIds = crIds
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.createRelationView(values)
        }
      })
    },

    createRelationView(data) {
      data.cr_ids = this.crIds
      subscribeRelationView(data).then(res => {
        this.$message.success('新增成功!')
        this.onClose()
        this.$emit('refresh')
      })
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
