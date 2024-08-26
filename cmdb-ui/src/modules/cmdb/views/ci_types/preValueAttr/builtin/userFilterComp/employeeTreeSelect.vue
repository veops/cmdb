<template>
  <treeselect
    class="employee-tree-select"
    :style="{ width: '100px' }"
    :disable-branch-nodes="!multiple"
    :multiple="multiple"
    :options="employeeTreeSelectOption"
    :placeholder="readOnly ? '' : placeholder || $t('cs.components.selectEmployee')"
    v-model="treeValue"
    :max-height="150"
    :noChildrenText="$t('cs.components.empty')"
    :noOptionsText="$t('cs.components.empty')"
    :class="className ? className : 'ops-setting-treeselect'"
    value-consists-of="LEAF_PRIORITY"
    :limit="limit"
    :limitText="(count) => `+ ${count}`"
    v-bind="$attrs"
    :zIndex="1050"
    :flat="flat"
  >
    <div
      :title="node.label"
      slot="option-label"
      slot-scope="{ node }"
      :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
    >
      {{ node.label }}
    </div>
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
      default: 3,
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
      default: () => {
        return () => {
          return []
        }
      }
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
      const option = formatOption(this.allTreeDepAndEmp, this.idType, false, this.departmentKey, this.employeeKey)
      return option
    },
  },
  methods: {},
}
</script>

<style lang="less" scoped>
.employee-tree-select {
  /deep/ .vue-treeselect__menu {
    width: 100px;
    overflow-x: auto;

    & > .vue-treeselect__list {
      width: fit-content;
      min-width: 100%;
    }

    .vue-treeselect__label-container {
      width: max-content;
    }

    .vue-treeselect__option {
      width: max-content;
      min-width: 100%;
    }
  }
}
</style>
