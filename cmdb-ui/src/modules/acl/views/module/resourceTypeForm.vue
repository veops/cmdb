<template>
  <CustomDrawer
    :closable="false"
    :title="$t('acl.addResourceType')"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="500px"
  >
    <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item :label="$t('acl.typeName')">
        <a-input
          name="name"
          :placeholder="$t('acl.typeName')"
          v-decorator="['name', { rules: [{ required: true, message: $t('acl.typeNameInput') }] }]"
        />
      </a-form-item>

      <a-form-item :label="$t('desc')">
        <a-textarea
          :placeholder="$t('acl.descInput')"
          name="description"
          :rows="4"
          v-decorator="['description', { rules: [] }]"
        />
      </a-form-item>

      <a-form-item :label="$t('acl.permission')">
        <a-select mode="tags" v-model="perms" style="width: 100%" :placeholder="$t('acl.permInput')"> </a-select>
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
