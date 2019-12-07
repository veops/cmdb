<template>
  <a-drawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >

    <a-form :form="form" :layout="formLayout" @submit="handleSubmit">

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="资源名"
      >
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', {rules: [{ required: true, message: '请输入资源名'}]} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="资源类型"
      >
        <a-select name="type_id" v-decorator="['type_id', {rules: []} ]">
          <a-select-option v-for="type in allTypes" :key="type.id">{{ type.name }}</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item>
        <a-input
          name="id"
          type="hidden"
          v-decorator="['id', {rules: []} ]"
        />
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
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">确定</a-button>
        <a-button @click="onClose">取消</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { addResource, searchResourceType } from '@/api/acl/resource'

export default {
  name: 'ResourceForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: '新增资源',
      drawerVisible: false,
      formLayout: 'vertical',
      allTypes: []
    }
  },

  beforeCreate () {
    this.form = this.$form.createForm(this)
  },

  created () {
    this.getAllResourceTypes()
  },

  computed: {

    formItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      } : {}
    },

    horizontalFormItemLayout () {
      return {
        labelCol: { span: 5 },
        wrapperCol: { span: 12 }
      }
    },
    buttonItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        wrapperCol: { span: 14, offset: 4 }
      } : {}
    }

  },
  mounted () {
  },
  methods: {
    getAllResourceTypes () {
      searchResourceType({ page_size: 9999, app_id: this.$route.name.split('_')[0] }).then(res => {
        this.allTypes = res.groups
      })
    },
    handleCreate (defaultType) {
      this.drawerVisible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({ type_id: defaultType.id })
      })
    },
    onClose () {
      this.form.resetFields()
      this.drawerVisible = false
      this.$emit('fresh')
    },
    onChange (e) {
      console.log(`checked = ${e}`)
    },
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          values.app_id = this.$route.name.split('_')[0]
          if (values.id) {
            this.updateResource(values.id, values)
          } else {
            this.createResource(values)
          }
        }
      })
    },
    createResource (data) {
      addResource(data)
        .then(res => {
          this.$message.success(`添加成功`)
          this.onClose()
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
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
