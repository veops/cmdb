<template>
  <a-modal width="700px" :title="title" :visible="visible" @cancel="handleCancel" @ok="handleOK">
    <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 14 }">
      <a-form-model-item :label="$t('cmdb.preference_relation.serviceTreeName')" prop="name">
        <a-input v-model="form.name" :placeholder="$t('cmdb.preference_relation.serviceTreeNamePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.preference_relation.public')" prop="is_public">
        <a-checkbox v-model="form.is_public"> </a-checkbox>
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.preference_relation.showLeafNode')" prop="is_show_leaf_node">
        <a-checkbox :checked="form.is_show_leaf_node" @change="changeLeaf"> </a-checkbox>
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.preference_relation.showTreeNode')" prop="is_show_tree_node">
        <a-checkbox v-model="form.is_show_tree_node"> </a-checkbox>
      </a-form-model-item>
      <a-form-model-item
        v-if="form.is_show_leaf_node && form.is_show_tree_node"
        :label="$t('cmdb.preference_relation.sort')"
        prop="sort"
      >
        <a-radio-group v-model="form.sort">
          <a-radio :value="1">
            {{ $t('cmdb.preference_relation.sort1') }}
          </a-radio>
          <a-radio :value="2">
            {{ $t('cmdb.preference_relation.sort2') }}
          </a-radio>
        </a-radio-group>
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
export default {
  name: 'ServiceTreeModal',
  data() {
    return {
      visible: false,
      type: 'add',
      originTreeData: {},
      form: {
        name: '',
        is_public: true,
        is_show_leaf_node: true,
        is_show_tree_node: false,
        sort: 1,
      },
      rules: {
        name: [{ required: true, message: this.$t('cmdb.preference_relation.serviceTreeNamePlaceholder') }],
        is_public: [{ required: false }],
        is_show_leaf_node: [{ required: true }],
        is_show_tree_node: [{ required: false }],
      },
    }
  },
  computed: {
    title() {
      if (this.type === 'edit') {
        return this.$t('cmdb.preference_relation.editServiceTree')
      }
      return this.$t('cmdb.preference_relation.newServiceTree')
    },
  },
  methods: {
    open(treeData = {}, type) {
      this.visible = true
      this.type = type
      this.originTreeData = { ...treeData }
      this.form = { name: '', is_public: true, is_show_leaf_node: true, is_show_tree_node: false, sort: 1, ...treeData }
    },
    handleCancel() {
      this.$refs.form.resetFields()
      this.visible = false
    },
    handleOK() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submitServiceTree', this.form, this.type, this.originTreeData?.name ?? undefined)
          this.handleCancel()
        }
      })
    },
    changeLeaf(e) {
      const checked = e.target.checked
      if (!checked) {
        this.$message.warning(this.$t('cmdb.preference_relation.tips4'))
        return
      }
      this.form = {
        ...this.form,
        is_show_leaf_node: checked,
      }
    },
  },
}
</script>

<style></style>
