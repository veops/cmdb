<template>
  <CustomDrawer
    :closable="false"
    :title="$t('acl.addResourceType')"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >
    <a-form :form="form" :layout="formLayout" @submit="handleSubmit">
      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" :label="$t('acl.typeName')">
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', { rules: [{ required: true, message: $t('acl.resourceNameInput') }] }]"
        />
      </a-form-item>

      <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" :label="$t('desc')">
        <a-textarea :placeholder="$t('acl.descInput')" name="description" :rows="4" />
      </a-form-item>

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        :label="$t('acl.permission')"
      >
        <div :style="{ borderBottom: '1px solid #E9E9E9' }">
          <a-checkbox :indeterminate="indeterminate" @change="onCheckAllChange" :checked="checkAll">
            {{ $t('checkAll') }}
          </a-checkbox>
        </div>
        <br />
        <a-checkbox-group :options="plainOptions" v-model="perms" @change="onPermChange" />
      </a-form-item>

      <a-form-item>
        <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
      </a-form-item>

      <div class="custom-drawer-bottom-action">
        <a-button @click="onClose">{{ $t('cancel') }}</a-button>
        <a-button @click="handleSubmit" type="primary">{{ $t('confirm') }}</a-button>
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
      drawerVisible: false,
      formLayout: 'vertical',
      perms: ['1'],
      indeterminate: true,
      checkAll: false,
      plainOptions: ['1', '2'],
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
  mounted() {},
  methods: {
    onPermChange(perms) {
      this.indeterminate = !!perms.length && perms.length < this.plainOptions.length
      this.checkAll = perms.length === this.plainOptions.length
    },
    onCheckAllChange(e) {
      Object.assign(this, {
        perms: e.target.checked ? this.plainOptions : [],
        indeterminate: false,
        checkAll: e.target.checked,
      })
    },
    handleCreate() {
      this.drawerVisible = true
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
    },
    onChange(e) {
      console.log(`checked = ${e}`)
    },

    handleEdit(record) {
      this.drawerVisible = true
      console.log(record)
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
        this.$message.success(this.$t('updateSuccess'))
        this.handleOk()
        this.onClose()
      })
      // .catch(err => this.requestFailed(err))
    },

    createResourceType(data) {
      addResourceType(data).then((res) => {
        this.$message.success(this.$t('addSuccess'))
        this.handleOk()
        this.onClose()
      })
    },
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
