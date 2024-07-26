<template>
  <a-tabs v-model="activeKey" size="small" :tabBarStyle="{ borderBottom: 'none' }">
    <a-tab-pane key="expr" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">{{ $t('cmdb.ciType.expr') }}</span>
      <a-textarea v-model="compute_expr" :placeholder="`{{a}}+{{b}}`" :rows="2" :disabled="!canDefineComputed" />
    </a-tab-pane>
    <a-tab-pane key="script" :disabled="!canDefineComputed">
      <span style="font-size:12px;" slot="tab">{{ $t('cmdb.ciType.code') }}</span>
      <codemirror
        style="z-index: 9999"
        :options="cmOptions"
        v-model="compute_script"
        @input="onCodeChange"
      ></codemirror>
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
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'

require('codemirror/mode/python/python.js')
export default {
  name: 'ComputedArea',
  components: {
    codemirror,
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
      compute_script: 'def computed(): \n    return',
      cmOptions: {
        lineNumbers: true,
        mode: 'python',
        height: '200px',
        theme: 'monokai',
        tabSize: 4,
        indentUnit: 4,
        lineWrapping: false,
        readOnly: !this.canDefineComputed,
        extraKeys: {
          Tab: (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection('add')
            } else {
              cm.replaceSelection(Array(cm.getOption('indentUnit') + 1).join(' '), 'end', '+input')
            }
          },
          'Shift-Tab': (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection('subtract')
            } else {
              const cursor = cm.getCursor()
              cm.setCursor({ line: cursor.line, ch: cursor.ch - 4 })
            }
          },
        },
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
    }
  },
}
</script>

<style></style>
