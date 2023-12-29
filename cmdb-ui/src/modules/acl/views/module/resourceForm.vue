<template>
  <CustomDrawer
    :closable="false"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="30%"
  >
    <a-form :form="form" @submit="handleSubmit" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-item :label="$t('acl.resourceName')">
        <a-input
          name="name"
          placeholder=""
          v-decorator="['name', { rules: [{ required: true, message: $t('acl.resourceNameInput') }] }]"
        />
      </a-form-item>

      <a-form-item :label="$t('acl.resourceType')">
        <a-select v-model="selectedTypeId">
          <a-select-option v-for="type in allTypes" :key="type.id">{{ type.name }}</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item :label="$t('acl.isGroup')">
        <a-radio-group v-model="isGroup">
          <a-radio :value="true">
            {{ $t('yes') }}
          </a-radio>
          <a-radio :value="false">
            {{ $t('no') }}
          </a-radio>
        </a-radio-group>
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
/* eslint-disable */
import { addResource, searchResourceType } from '@/modules/acl/api/resource'
import { addResourceGroup } from '@/modules/acl/api/resource'

export default {
  name: 'ResourceForm',
  data() {
    return {
      drawerVisible: false,
      allTypes: [],
      isGroup: false,
      selectedTypeId: 0,
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },

  created() {
    this.getAllResourceTypes()
  },

  computed: {
    drawerTitle() {
      return this.$t('acl.addResource')
    },
  },
  mounted() {},
  methods: {
    getAllResourceTypes() {
      searchResourceType({ page_size: 9999, app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.allTypes = res.groups
      })
    },
    handleCreate(defaultType) {
      this.drawerVisible = true
      this.$nextTick(() => {
        this.selectedTypeId = defaultType.id
      })
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
      this.$emit('fresh')
    },
    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          values.type_id = this.selectedTypeId
          values.app_id = this.$route.name.split('_')[0]
          if (values.id) {
            this.$message.error(this.$t('acl.errorTips'))
          } else {
            this.createResource(values)
          }
        }
      })
    },
    createResource(data) {
      if (!this.isGroup) {
        addResource(data).then((res) => {
          this.$message.success(this.$t('addSuccess'))
          this.onClose()
        })
        // .catch(err => this.requestFailed(err))
      } else {
        addResourceGroup(data).then((res) => {
          this.$message.success(this.$t('addSuccess'))
          this.onClose()
        })
      }
    },
  },
  watch: {
    '$route.name': function(newValue, oldValue) {
      this.getAllResourceTypes()
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
