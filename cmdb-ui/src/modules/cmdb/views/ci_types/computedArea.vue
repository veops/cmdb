<template>
  <a-tabs v-model="activeKey" size="small" :tabBarStyle="{ borderBottom: 'none' }" @change="handleTabsChange">
    <a-tab-pane key="expr" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">{{ $t('cmdb.ciType.expr') }}</span>
      <a-textarea v-model="compute_expr" :placeholder="`{{a}}+{{b}}`" :rows="2" :disabled="!canDefineComputed" />
    </a-tab-pane>
    <a-tab-pane key="script" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">{{ $t('cmdb.ciType.code') }}</span>
      <MonacoCodeEditor
        v-model="compute_script"
        language="python"
        :height="360"
        storage-key="cmdbComputedAreaMonacoEditorConfig"
        @change="onCodeChange"
      />
    </a-tab-pane>
    <template slot="tabBarExtraContent">
      <a-button size="small" @click="showAllPropDrawer">
        {{ $t('cmdb.ciType.viewAllAttr') }}
      </a-button>
      <AllAttrDrawer ref="allAttrDrawer" />

      <template v-if="showCalcComputed">
        <a-button style="margin: 0px 5px;" type="primary" size="small" @click="handleCalcComputed">
          {{ $t('cmdb.ciType.apply') }}
        </a-button>
        <a-tooltip :title="$t('cmdb.ciType.computeForAllCITips')">
          <a-icon type="question-circle" />
        </a-tooltip>
      </template>
    </template>
  </a-tabs>
</template>

<script>
import AllAttrDrawer from './allAttrDrawer.vue'
import MonacoCodeEditor from '@/components/MonacoCodeEditor'

export default {
  name: 'ComputedArea',
  components: {
    MonacoCodeEditor,
    AllAttrDrawer
  },
  props: {
    canDefineComputed: {
      type: Boolean,
      default: true,
    },
    showCalcComputed: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      activeKey: 'expr', // expr script
      compute_expr: '',
      compute_script: this.$t('cmdb.ciType.computedScriptTemplate'),
    }
  },
  methods: {
    getData() {
      const { activeKey, compute_expr, compute_script } = this
      if (activeKey === 'expr') {
        return { compute_expr, compute_script: null }
      } else if (activeKey === 'script') {
        return { compute_script, compute_expr: null }
      }
    },
    setData(data) {
      const { compute_expr, compute_script } = data
      this.compute_expr = compute_expr
      this.compute_script = compute_script || this.$t('cmdb.ciType.computedScriptTemplate')
      if (compute_script) {
        this.activeKey = 'script'
      } else {
        this.activeKey = 'expr'
      }
    },
    handleCalcComputed() {
      const that = this
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.ciType.confirmcomputeForAllCITips'),
        onOk() {
          that.$emit('handleCalcComputed')
        },
      })
    },
    onCodeChange(v) {
      this.compute_script = v.replace('\t', '    ')
    },
    showAllPropDrawer() {
      this.$refs.allAttrDrawer.open()
    },

    handleTabsChange(activeKey) {
      console.log('handleTabsChange', activeKey)
    }
  },
}
</script>

<style></style>
