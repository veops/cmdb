<template>
  <a-form-item
    :label="$t('cmdb.ciType.referenceModel')"
    :extra="$t('cmdb.ciType.referenceModelTip1')"
    :label-col="formItemLayout.labelCol"
    :wrapper-col="formItemLayout.wrapperCol"
  >
    <a-select
      allowClear
      v-decorator="['reference_type_id', {
        rules: [{ required: true, message: $t('cmdb.ciType.referenceModelTip') }],
        initialValue: ''
      }]"
      showSearch
      optionFilterProp="title"
      @dropdownVisibleChange="handleDropdownVisibleChange"
    >
      <a-select-option
        v-for="(item) in options"
        :key="item.value"
        :title="item.label"
      >
        {{ item.label }}
      </a-select-option>
    </a-select>
  </a-form-item>
</template>

<script>
import { getCITypes } from '@/modules/cmdb/api/CIType'

export default {
  name: 'ReferenceModelSelect',
  props: {
    form: {
      type: Object,
      required: true,
    },
    isLazyRequire: {
      type: Boolean,
      default: true
    },
    formItemLayout: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      isInit: false,
      options: []
    }
  },
  mounted() {
    if (!this.isLazyRequire) {
      this.getSelectOptions()
    }
  },
  methods: {
    handleDropdownVisibleChange(open) {
      if (!this.isInit && open) {
        this.getSelectOptions()
      }
    },
    async getSelectOptions() {
      this.isInit = true
      const res = await getCITypes()

      this.options = res.ci_types.map((ciType) => {
        return {
          value: ciType.id,
          label: ciType?.alias || ciType?.name || ''
        }
      })
    }
  }
}
</script>
