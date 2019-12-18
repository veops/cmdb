<template>
  <a-drawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >

    <a-form :form="form" :layout="formLayout" @submit="handleAddParent">

      <a-form-item
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
        label="角色列表"
      >
        <a-select name="otherID" :filterOption="filterOption" v-decorator="['otherID', {rules: [{ required: true, message: '请选择另一个角色'}]} ]">
          <template v-for="role in allRoles">
            <a-select-option  v-if="role.id != current_record.id" :key="role.id">{{ role.name }}</a-select-option>
          </template>
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
        <a-button @click="handleAddParent" type="primary" style="margin-right: 1rem">关联父角色</a-button>
        <a-button @click="handleAddChild" type="primary" style="margin-right: 1rem">关联子角色</a-button>
        <a-button @click="onClose">取消</a-button>

      </div>

    </a-form>
  </a-drawer>

</template>

<script>
import { STable } from '@/components'
import { searchRole, addParentRole, addChildRole } from '@/api/acl/role'

export default {
  name: 'AddRoleRelationForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: '角色关联',
      drawerVisible: false,
      formLayout: 'vertical',
      allRoles: [],
      current_record: null
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
  methods: {
    filterOption (input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      )
    },
    onClose () {
      this.form.resetFields()
      this.drawerVisible = false
    },
    handleAddRoleRelation (record) {
      this.current_record = record
      this.drawerVisible = true
      this.$nextTick(() => {
        this.getAllRoles()
        this.form.setFieldsValue({
          id: record.id
        })
      })
    },
    handleAddParent (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          this.addParent(values.id, values.otherID)
        }
      })
    },
    handleAddChild (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          this.addChild(values.id, values.otherID)
        }
      })
    },
    getAllRoles () {
      searchRole({ page_size: 9999, app_id: this.$store.state.app.name }).then(res => {
        this.allRoles = res.roles
      })
    },
    addParent (id, otherID) {
      addParentRole(id, otherID)
        .then(res => {
          this.$message.success(`关联父角色成功`)
          this.handleOk()
          this.onClose()
        }).catch(err => this.requestFailed(err))
    },

    addChild (id, otherID) {
      addChildRole(id, otherID)
        .then(res => {
          this.$message.success(`关联子角色成功`)
          this.handleOk()
          this.onClose()
        })
        .catch(err => this.requestFailed(err))
    },

    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
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
