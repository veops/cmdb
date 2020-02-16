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
        :label-col="{span:6}"
        :wrapper-col="{span:12}"
        :label="$t('acl.roleName')"
      >
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', {rules: [{ required: true, message: $t('acl.roleNameRequired')}]} ]"
        />
      </a-form-item>
      <a-form-item
        :label-col="{span:6}"
        :wrapper-col="{span:12}"
        :label="$t('acl.inheritedFrom')"
      >
        <a-select
          v-model="selectedParents"
          :placeholder="$t('acl.selectInheritedRoles')"
          mode="multiple"
          :filterOption="filterOption">
          <template v-for="role in allRoles">
            <a-select-option v-if="current_id !== role.id" :key="role.id">{{ role.name }}</a-select-option>
          </template>
        </a-select>
      </a-form-item>
      <a-form-item
        :label-col="{span:8}"
        :wrapper-col="{span:10}"
        :label="$t('acl.isAppAdmin')"
      >
        <a-switch
          @change="onChange"
          name="is_app_admin"
          v-decorator="['is_app_admin', {rules: [], valuePropName: 'checked',} ]"
        />
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
import { addRole, updateRoleById, addParentRole, delParentRole } from '@/api/acl/role'

export default {
  name: 'RoleForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: this.$t('acl.newRole'),
      current_id: 0,
      drawerVisible: false,
      formLayout: 'vertical',
      selectedParents: [],
      oldParents: []
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
        labelCol: { span: 8 },
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
  methods: {
    filterOption (input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      )
    },
    handleCreate () {
      this.drawerTitle = this.$t('button.add')
      this.drawerVisible = true
    },
    onClose () {
      this.form.resetFields()
      this.selectedParents = []
      this.oldParents = []
      this.drawerVisible = false
    },
    onChange (e) {
      console.log(`checked = ${e}`)
    },

    handleEdit (record) {
      this.drawerTitle = this.$t('button.update')
      this.drawerVisible = true
      this.current_id = record.id
      const _parents = this.id2parents[record.id]
      if (_parents) {
        _parents.forEach(item => {
          this.selectedParents.push(item.id)
          this.oldParents.push(item.id)
        })
      }
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          is_app_admin: record.is_app_admin
        })
      })
    },

    handleSubmit (e) {
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
    updateRole (id, data) {
      this.updateParents(id)
      updateRoleById(id, data)
        .then(res => {
          this.$message.success(this.$t('tip.updateSuccess'))
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    createRole (data) {
      addRole(data)
        .then(res => {
          this.$message.success(this.$t('tip.addSuccess'))
          this.updateParents(res.id)
          this.handleOk()
          this.onClose()
        })
        .catch(err => this.requestFailed(err))
    },
    updateParents (id) {
      this.oldParents.forEach(item => {
        if (!this.selectedParents.includes(item)) {
          delParentRole(id, item).catch(err => this.requestFailed(err))
        }
      })
      this.selectedParents.forEach(item => {
        if (!this.oldParents.includes(item)) {
          addParentRole(id, item).catch(err => this.requestFailed(err))
        }
      })
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
    },
    allRoles: {
      type: Array,
      required: true
    },
    id2parents: {
      type: Object,
      required: true
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
