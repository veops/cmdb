<template>
  <treeselect
    :disable-branch-nodes="multiple ? false : true"
    :multiple="multiple"
    :options="employeeTreeSelectOption"
    placeholder="请选择员工"
    v-model="treeValue"
    :max-height="200"
    noChildrenText="空"
    noOptionsText="空"
    :class="className ? className: 'ops-setting-treeselect'"
    value-consists-of="LEAF_PRIORITY"
    :limit="20"
    :limitText="(count) => `+ ${count}`"
    v-bind="$attrs"
    appendToBody
    :zIndex="1050"
  >
  </treeselect>
</template>

<script>
import Treeselect from '@riophae/vue-treeselect'
import { formatOption } from '@/utils/util'
export default {
  name: 'EmployeeTreeSelect',
  components: {
    Treeselect,
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Array, Number, null],
      default: null,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    className: {
      type: String,
      default: 'ops-setting-treeselect'
    }
  },
  data() {
    return {}
  },
  inject: ['provide_allTreeDepAndEmp'],
  computed: {
    treeValue: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
        return val
      },
    },
    allTreeDepAndEmp() {
      return this.provide_allTreeDepAndEmp()
    },
    employeeTreeSelectOption() {
      return formatOption(this.allTreeDepAndEmp)
    },
  },
  methods: {},
}
</script>

<style scoped>
</style>
