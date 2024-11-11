<template>
  <a-modal
    :visible="visible"
    :title="$t(actionType === 'edit' ? 'cmdb.ipam.editCatalog' : 'cmdb.ipam.addCatalog')"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="catelogFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 5 }"
      :wrapper-col="{ span: 19 }"
    >
      <a-form-model-item
        :label="$t('cmdb.ipam.catalogName')"
        prop="name"
      >
        <a-input
          :placeholder="$t('placeholder1')"
          v-model="form.name"
        />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { postIPAMScope, putIPAMScope } from '@/modules/cmdb/api/ipam.js'

export default {
  name: 'CatalogForm',
  data() {
    return {
      visible: false,
      nodeId: null,
      actionType: 'create',
      form: {
        name: ''
      },
      formRules: {
        name: [
          {
            required: true, message: this.$t('placeholder1')
          }
        ]
      }
    }
  },
  methods: {
    open({
      nodeId,
      type,
      name
    }) {
      this.nodeId = nodeId || null
      this.actionType = type || 'create'
      this.form.name = name || ''
      this.visible = true
    },

    handleCancel() {
      this.visible = false
      this.form.name = ''
      this.actionType = 'create'
      this.nodeId = null

      this.$refs.catelogFormRef.clearValidate()
    },

    handleOk() {
      this.$refs.catelogFormRef.validate(async (valid) => {
        if (!valid) {
          return
        }

        if (this.actionType === 'edit') {
          await putIPAMScope(this.nodeId, {
            name: this.form.name
          })
          this.$message.success(this.$t('editSuccess'))
        } else {
          await postIPAMScope({
            parent_id: this.nodeId,
            name: this.form.name
          })
          this.$message.success(this.$t('addSuccess'))
        }

        this.$emit('ok')
        this.handleCancel()
      })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
