<template>
  <a-select
    v-bind="$attrs"
    v-model="currenCIType"
    style="width: 100%"
    :showSearch="true"
    :filterOption="filterOption"
    :placeholder="placeholder || $t('placeholder2')"
  >
    <a-select-opt-group
      v-for="group in selectOptions"
      :key="group.id"
      :label="group.name || $t('other')"
    >
      <a-select-option
        v-for="type in group.ci_types"
        :key="type.id"
        :value="type.id"
        :data-alias="type.alias"
        :data-name="type.name"
      >
        {{ type.alias || type.name || $t('other') }}
        <span v-if="type.name" class="select-option-name">({{ type.name }})</span>
      </a-select-option>
    </a-select-opt-group>
  </a-select>
</template>

<script>
import _ from 'lodash'
import { getCITypeGroupsConfig } from '@/modules/cmdb/api/ciTypeGroup'

export default {
  name: 'CMDBTypeSelectAntd',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Number, Array],
      default: undefined,
    },
    CITypeGroup: {
      type: Array,
      default: undefined
    },
    placeholder: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      selectOptions: []
    }
  },
  computed: {
    currenCIType: {
      get() {
        return this.value
      },
      set(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.$emit('change', newVal)
        }
        return newVal
      },
    },
  },
  watch: {
    CITypeGroup: {
      deep: true,
      handler() {
        this.handleSelectOptions()
      }
    }
  },
  async mounted() {
    this.handleSelectOptions()
  },
  methods: {
    async handleSelectOptions() {
      let rawCITypeGroup = []
      if (this.CITypeGroup) {
        rawCITypeGroup = this.CITypeGroup
      } else {
        rawCITypeGroup = await getCITypeGroupsConfig({ need_other: true })
      }

      this.selectOptions = _.cloneDeep(rawCITypeGroup).filter((group) => group?.ci_types?.length)
    },
    filterOption(input, option) {
      const attrs = option?.data?.attrs || {}
      const alias = attrs?.['data-alias']?.toLowerCase?.() || ''
      const name = attrs?.['data-name']?.toLowerCase?.() || ''
      return alias.indexOf(input.toLowerCase()) >= 0 || name.indexOf(input.toLowerCase()) >= 0
    }
  },
}
</script>

<style lang="less" scoped>
.select-option-name {
  font-size: 12px;
  color: #A5A9BC;
}
</style>
