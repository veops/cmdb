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
        :label="$t('acl.name')"
      >
        <a-input
          name="name"
          :placeholder="$t('acl.name')"
          v-decorator="['name', {rules: [{ required: true, message: $t('acl.resourceTypeNameRequired')}]} ]"
        />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.description')"
      >
        <a-textarea :placeholder="$t('acl.descriptionTip')" name="description" :rows="4" v-decorator="['description', {rules: []} ]"/>
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.permission')"
      >
        <a-select mode="tags" v-model="perms" style="width: 100%" :placeholder="$t('acl.permissionNameRequired')">
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
        <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('button.submit') }}</a-button>
        <a-button @click="onClose">{{ $t('button.cancel') }}</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { addResourceType, updateResourceTypeById } from '@/api/acl/resource'

export default {
  name: 'ResourceForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: this.$t('acl.newResourceType'),
      drawerVisible: false,
      formLayout: 'vertical',
      perms: []
    }
  },

  beforeCreate () {
    this.form = this.$form.createForm(this)
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
    handleCreate () {
      this.drawerVisible = true
    },
    onClose () {
      this.form.resetFields()
      this.perms = []
      this.drawerVisible = false
    },
    onChange (e) {
      console.log(`checked = ${e}`)
    },

    handleEdit (record) {
      this.drawerVisible = true
      this.perms = record.perms
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          description: record.description
        })
      })
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
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
    updateResourceType (id, data) {
      updateResourceTypeById(id, data)
        .then(res => {
          this.$message.success(this.$t('tip.updateSuccess'))
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createResourceType (data) {
      addResourceType(data)
        .then(res => {
          this.$message.success(this.$t('tip.addSuccess'))
          this.handleOk()
          this.onClose()
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
      this.$message.error(`${msg}`)
    }

  },
  watch: {},
  props: {
    handleOk: {
      type: Function,
      default: null
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
