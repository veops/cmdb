<template>
  <a-modal
    :visible="visible"
    wrapClassName="ci-json-editor"
    :closable="false"
    :maskClosable="false"
    @cancel="handleCancel"
    width="50%"
    @ok="handleOk"
  >
    <vue-json-editor
      :style="{ '--custom-height': `${windowHeight - 300}px` }"
      v-model="jsonData"
      :showBtns="false"
      :mode="'code'"
      lang="zh"
      @has-error="onJsonError"
      @json-change="onJsonChange"
    />
  </a-modal>
</template>

<script>
import vueJsonEditor from 'vue-json-editor'
import { updateCI } from '@/modules/cmdb/api/ci'
export default {
  name: 'JsonEditor',
  components: { vueJsonEditor },
  data() {
    return {
      visible: false,
      jsonData: {},
      row: {},
      column: {},
      default_value_json_right: true,
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  methods: {
    open(column, row, jsonData) {
      this.visible = true
      if (row && row[column.property]) {
        this.jsonData = JSON.parse(row[column.property]) || {}
      } else {
        this.jsonData = {}
      }
      if (jsonData) {
        this.jsonData = jsonData
      }

      this.row = row
      this.column = column
    },
    handleCancel() {
      this.visible = false
    },
    handleOk() {
      if (this.row && this.column) {
        updateCI(this.row.ci_id || this.row._id, {
          [`${this.column.property}`]: this.default_value_json_right ? this.jsonData : {},
        }).then(() => {
          this.$message.success('保存成功！')
          this.handleCancel()
          this.$emit('jsonEditorOk', this.row, this.column, this.default_value_json_right ? this.jsonData : {})
        })
      } else {
        this.$emit('jsonEditorOk', this.jsonData)
        this.handleCancel()
      }
    },
    onJsonChange(value) {
      this.default_value_json_right = true
    },
    onJsonError() {
      this.default_value_json_right = false
    },
  },
}
</script>

<style lang="less">
.ci-json-editor {
  .jsoneditor-outer {
    height: var(--custom-height) !important;
    border: 1px solid #2f54eb;
  }
  div.jsoneditor-menu {
    background-color: #2f54eb;
  }
}
</style>
