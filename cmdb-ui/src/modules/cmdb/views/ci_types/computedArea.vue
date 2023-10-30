<template>
  <a-tabs v-model="activeKey" size="small" :tabBarStyle="{ borderBottom: 'none' }">
    <a-tab-pane key="expr" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">表达式</span>
      <a-textarea v-model="compute_expr" :placeholder="`{{a}}+{{b}}`" :rows="2" :disabled="!canDefineComputed" />
    </a-tab-pane>
    <a-tab-pane key="script" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">代码</span>
      <codemirror style="z-index: 9999" :options="cmOptions" v-model="compute_script"></codemirror>
    </a-tab-pane>
    <template slot="tabBarExtraContent" v-if="showCalcComputed">
      <a-button type="primary" size="small" @click="handleCalcComputed">
        应用
      </a-button>
      <a-tooltip title="所有CI触发计算">
        <a-icon type="question-circle" style="margin-left:5px" />
      </a-tooltip>
    </template>
  </a-tabs>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'

require('codemirror/mode/python/python.js')
export default {
  name: 'ComputedArea',
  components: { codemirror },
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
      compute_script: 'def computed(): \n    return',
      cmOptions: {
        lineNumbers: true,
        mode: 'python',
        height: '200px',
        theme: 'monokai',
        tabSize: 4,
        lineWrapping: true,
        readOnly: !this.canDefineComputed,
      },
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
      this.compute_script = compute_script || 'def computed(): \n    return'
      if (compute_script) {
        this.activeKey = 'script'
      } else {
        this.activeKey = 'expr'
      }
    },
    handleCalcComputed() {
      const that = this
      this.$confirm({
        title: '警告',
        content: `确认触发将保存当前配置及触发所有CI的计算？`,
        onOk() {
          that.$emit('handleCalcComputed')
        },
      })
    },
  },
}
</script>

<style></style>
