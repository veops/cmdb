<template>
  <treeselect
    :multiple="false"
    :options="departemntTreeSelectOption"
    :placeholder="readOnly ? '' : $t('cs.companyStructure.selectDepartment')"
    v-model="treeValue"
    :normalizer="normalizer"
    :noChildrenText="$t('cs.components.empty')"
    :noOptionsText="$t('cs.components.empty')"
    :class="className ? className : 'ops-setting-treeselect'"
    v-bind="$attrs"
    appendToBody
    :zIndex="1050"
  />
</template>

<script>
import Treeselect from '@riophae/vue-treeselect'
export default {
  name: 'DepartmentTreeSelect',
  components: { Treeselect },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Array, Number, null],
      default: null,
    },
    className: {
      type: String,
      default: 'ops-setting-treeselect',
    },
  },
  data() {
    return {
      normalizer: (node) => {
        if (node.sub_departments && node.sub_departments.length) {
          return {
            id: node.department_id,
            label: node.department_name,
            children: node.sub_departments,
          }
        }
        return {
          id: node.department_id,
          label: node.department_name,
        }
      },
    }
  },
  inject: {
    provide_allTreeDepartment: {
      from: 'provide_allTreeDepartment',
    },
    readOnly: {
      from: 'readOnly',
      default: false,
    },
  },
  computed: {
    departemntTreeSelectOption() {
      return this.provide_allTreeDepartment()
    },
    treeValue: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
        return val
      },
    },
  },
}
</script>

<style></style>
