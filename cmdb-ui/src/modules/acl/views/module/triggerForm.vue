<template>
  <CustomDrawer
    @close="handleClose"
    width="500"
    :title="`${triggerId ? '修改' : '新建'}触发器`"
    :visible="visible"
    :maskClosable="false"
  >
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 15 }">
      <a-form-item label="触发器名">
        <a-input size="large" v-decorator="['name', { rules: [{ required: true, message: '请输入触发器名' }] }]">
        </a-input>
      </a-form-item>
      <a-form-item label="资源名">
        <a-input size="large" v-decorator="['wildcard']" placeholder="优先正则模式（次通配符）"> </a-input>
      </a-form-item>
      <a-form-item label="创建人">
        <el-select :style="{ width: '100%' }" filterable multiple v-decorator="['uid']">
          <template v-for="role in roles">
            <el-option v-if="role.uid" :key="role.id" :value="role.uid" :label="role.name">{{ role.name }}</el-option>
          </template>
        </el-select>
      </a-form-item>
      <a-form-item label="资源类型">
        <el-select
          :style="{ width: '100%' }"
          @change="handleRTChange"
          v-decorator="['resource_type_id', { rules: [{ required: true, message: '请选择资源类型' }] }]"
        >
          <el-option
            v-for="resourceType in resourceTypeList"
            :key="resourceType.id"
            :value="resourceType.id"
            :label="resourceType.name"
          ></el-option>
        </el-select>
        <a-tooltip title="查看正则匹配结果">
          <a class="trigger-form-pattern" @click="handlePattern"><a-icon type="eye"/></a>
        </a-tooltip>
      </a-form-item>
      <a-form-item label="角色">
        <el-select
          :style="{ width: '100%' }"
          filterable
          multiple
          v-decorator="['roles', { rules: [{ required: true, message: '请选择角色' }] }]"
        >
          <el-option v-for="role in roles" :key="role.id" :value="role.id" :label="role.name"></el-option>
        </el-select>
      </a-form-item>
      <a-form-item label="权限">
        <el-select
          :style="{ width: '100%' }"
          multiple
          v-decorator="['permissions', { rules: [{ required: true, message: '请选择权限' }] }]"
        >
          <el-option
            v-for="perm in selectResourceTypePerms"
            :key="perm.id"
            :value="perm.name"
            :label="perm.name"
          ></el-option>
        </el-select>
      </a-form-item>
      <a-form-item label="启用/禁用">
        <a-switch v-decorator="['enabled', { rules: [], valuePropName: 'checked', initialValue: true }]" />
      </a-form-item>
    </a-form>
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleClose">取消</a-button>
      <a-button @click="handleSubmit" type="primary">提交</a-button>
    </div>
    <TriggerPattern ref="triggerPattern" :roles="roles" />
  </CustomDrawer>
</template>
<script>
import { Select, Option, Input } from 'element-ui'
import { addTrigger, updateTrigger } from '@/modules/acl/api/trigger'
import TagSelectOption from '@/components/TagSelect/TagSelectOption'
import TriggerPattern from '../module/triggerPattern'

export default {
  name: 'TriggerForm',
  components: {
    TagSelectOption,
    TriggerPattern,
    ElSelect: Select,
    ElOption: Option,
    ElInput: Input,
  },
  data() {
    return {
      visible: false,
      triggerId: null,
      selectResourceTypePerms: [],
      form: this.$form.createForm(this),
    }
  },
  props: {
    roles: {
      required: true,
      type: Array,
    },
    resourceTypeList: {
      required: true,
      type: Array,
    },
    id2perms: {
      required: true,
      type: Object,
    },
    // eslint-disable-next-line vue/prop-name-casing
    app_id: {
      required: true,
      type: String,
    },
  },
  beforeCreate() {},
  methods: {
    handleEdit(ele) {
      this.form.resetFields()
      this.visible = true
      if (ele) {
        this.triggerId = ele.id
        this.$nextTick(() => {
          this.selectResourceTypePerms = this.id2perms[ele.resource_type_id]
          const { name, wildcard, uid, resource_type_id, roles, permissions, enabled } = ele
          this.form.setFieldsValue({
            name,
            wildcard,
            uid,
            resource_type_id,
            permissions,
            enabled,
            roles: roles.map((x) => Number(x)),
          })
        })
      } else {
        this.triggerId = null
      }
    },
    handleClose() {
      this.$nextTick(() => {
        this.visible = false
      })
    },
    handleRTChange(value) {
      this.selectResourceTypePerms = this.id2perms[value]
    },
    // filterOption(input, option) {
    //   return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    // },
    handleSubmit() {
      this.form.validateFields((err, values) => {
        if (err) {
          return
        }

        if (this.triggerId) {
          updateTrigger(this.triggerId, { ...values, app_id: this.app_id }).then((res) => {
            this.visible = false
            this.$message.success('修改成功！')
            this.$emit('refresh')
          })
        } else {
          addTrigger({ ...values, app_id: this.app_id }).then((res) => {
            this.visible = false
            this.$message.success('创建成功!')
            this.$emit('refresh')
          })
        }
      })
    },
    handlePattern() {
      this.form.validateFields(['wildcard', 'uid', 'resource_type_id'], (err, values) => {
        if (!err) {
          const { wildcard, uid, resource_type_id } = values
          console.log(values)
          this.$refs.triggerPattern.open({
            resource_type_id,
            app_id: this.app_id,
            owner: uid,
            pattern: wildcard,
          })
        }
      })
    },
  },
}
</script>

<style lang="less" scoped>
.trigger-form-pattern {
  position: absolute;
  right: -20px;
}
</style>
