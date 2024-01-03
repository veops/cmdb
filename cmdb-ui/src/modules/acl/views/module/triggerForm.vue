 <template>
  <CustomDrawer
    @close="handleClose"
    width="500"
    :title="`${triggerId ? $t('update') : $t('create')}${$t('acl.trigger')}`"
    :visible="visible"
    :maskClosable="false"
  >
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 15 }">
      <a-form-item :label="$t('name')">
        <a-input
          size="large"
          v-decorator="['name', { rules: [{ required: true, message: $t('acl.triggerNameInput') }] }]"
        >
        </a-input>
      </a-form-item>
      <a-form-item :label="$t('acl.resourceName')">
        <a-input size="large" v-decorator="['wildcard']" :placeholder="$t('acl.triggerTips1')"> </a-input>
      </a-form-item>
      <a-form-item :label="$t('acl.creator')">
        <el-select
          :style="{ width: '100%' }"
          filterable
          multiple
          v-decorator="['uid']"
          :placeholder="$t('placeholder2')"
        >
          <template v-for="role in roles">
            <el-option v-if="role.uid" :key="role.id" :value="role.uid" :label="role.name">{{ role.name }}</el-option>
          </template>
        </el-select>
      </a-form-item>
      <a-form-item :label="$t('acl.resourceType')">
        <el-select
          :style="{ width: '100%' }"
          @change="handleRTChange"
          :placeholder="$t('placeholder2')"
          v-decorator="['resource_type_id', { rules: [{ required: true, message: $t('acl.pleaseSelectType') }] }]"
        >
          <el-option
            v-for="resourceType in resourceTypeList"
            :key="resourceType.id"
            :value="resourceType.id"
            :label="resourceType.name"
          ></el-option>
        </el-select>
        <a-tooltip :title="$t('acl.viewMatchResult')">
          <a class="trigger-form-pattern" @click="handlePattern"><a-icon type="eye"/></a>
        </a-tooltip>
      </a-form-item>
      <a-form-item :label="$t('acl.role2')">
        <el-select
          :style="{ width: '100%' }"
          filterable
          multiple
          :placeholder="$t('placeholder2')"
          v-decorator="['roles', { rules: [{ required: true, message: $t('acl.role_placeholder2') }] }]"
        >
          <el-option v-for="role in roles" :key="role.id" :value="role.id" :label="role.name"></el-option>
        </el-select>
      </a-form-item>
      <a-form-item :label="$t('acl.permission')">
        <el-select
          :placeholder="$t('placeholder2')"
          :style="{ width: '100%' }"
          multiple
          v-decorator="['permissions', { rules: [{ required: true, message: $t('acl.permission_placeholder') }] }]"
        >
          <el-option
            v-for="perm in selectResourceTypePerms"
            :key="perm.id"
            :value="perm.name"
            :label="perm.name"
          ></el-option>
        </el-select>
      </a-form-item>
      <a-form-item :label="$t('acl.enable') / $t('acl.disable')">
        <a-switch v-decorator="['enabled', { rules: [], valuePropName: 'checked', initialValue: true }]" />
      </a-form-item>
    </a-form>
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
      <a-button @click="handleSubmit" type="primary">{{ $t('submit') }}</a-button>
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
            this.$message.success(this.$t('updateSuccess'))
            this.$emit('refresh')
          })
        } else {
          addTrigger({ ...values, app_id: this.app_id }).then((res) => {
            this.visible = false
            this.$message.success(this.$t('addSuccess'))
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
