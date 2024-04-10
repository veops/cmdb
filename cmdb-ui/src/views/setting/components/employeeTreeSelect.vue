<template>
  <treeselect
    :disable-branch-nodes="multiple ? false : true"
    :multiple="multiple"
    :options="employeeTreeSelectOption"
    :placeholder="readOnly ? '' : placeholder || $t('cs.components.selectEmployee')"
    v-model="treeValue"
    :max-height="200"
    :noChildrenText="$t('cs.components.empty')"
    :noOptionsText="$t('cs.components.empty')"
    :class="className ? className : 'ops-setting-treeselect'"
    value-consists-of="LEAF_PRIORITY"
    :limit="limit"
    :limitText="(count) => `+ ${count}`"
    v-bind="$attrs"
    appendToBody
    :zIndex="1050"
    :flat="flat"
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
      default: 'ops-setting-treeselect',
    },
    placeholder: {
      type: String,
      default: '',
    },
    idType: {
      type: Number,
      default: 1,
    },
    departmentKey: {
      type: String,
      default: 'department_id',
    },
    employeeKey: {
      type: String,
      default: 'employee_id',
    },
    limit: {
      type: Number,
      default: 20,
    },
    flat: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {}
  },
  inject: {
    provide_allTreeDepAndEmp: {
      from: 'provide_allTreeDepAndEmp',
    },
    readOnly: {
      from: 'readOnly',
      default: false,
    },
  },
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
      return formatOption(this.allTreeDepAndEmp, this.idType, false, this.departmentKey, this.employeeKey)
    },
  },
  methods: {},
}
</script>

<style scoped></style>
