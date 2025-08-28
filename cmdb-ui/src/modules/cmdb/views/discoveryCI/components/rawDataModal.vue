<template>
  <a-modal
    :title="$t('cmdb.ad.viewRawData')"
    :visible="visible"
    wrapClassName="ci-json-editor"
    width="50%"
    :footer="null"
    @cancel="handleCancel"
  >
    <vue-json-editor
      v-model="jsonData"
      :style="{ '--custom-height': `${windowHeight - 300}px` }"
      :showBtns="false"
      :mode="'code'"
      lang="zh"
    />
  </a-modal>
</template>

<script>
import vueJsonEditor from 'vue-json-editor'

export default {
  name: 'RawDataModal',
  components: { vueJsonEditor },
  data() {
    return {
      visible: false,
      jsonData: {},
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  methods: {
    open(jsonData) {
      this.visible = true
      this.jsonData = jsonData
    },
    handleCancel() {
      this.visible = false
      this.jsonData = {}
    }
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
