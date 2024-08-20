<template>
  <div class="reference-attr-select-wrap">
    <a-select
      v-bind="$attrs"
      v-model="selectCIIds"
      optionFilterProp="title"
      :mode="isList ? 'multiple' : 'default'"
      showSearch
      allowClear
      :getPopupContainer="(trigger) => trigger.parentElement"
      class="reference-attr-select"
      :maxTagCount="2"
      @dropdownVisibleChange="handleDropdownVisibleChange"
      @search="handleSearch"
      @change="handleChange"
    >
      <template v-if="!isInit">
        <a-select-option
          v-for="(item) in initSelectOption"
          :key="item.key"
          :title="item.title"
        >
          {{ item.title }}
        </a-select-option>
      </template>
      <a-select-option
        v-for="(item) in options"
        :key="item.key"
        :title="item.title"
      >
        {{ item.title }}
      </a-select-option>
    </a-select>
  </div>
</template>

<script>
import _ from 'lodash'
import debounce from 'lodash/debounce'
import { searchCI, getCIType } from '@/api/cmdb'

export default {
  name: 'CIReferenceAttr',
  props: {
    value: {
      type: [Number, String, Array],
      default: () => '',
    },
    isList: {
      type: Boolean,
      default: false,
    },
    referenceShowAttrName: {
      type: String,
      default: ''
    },
    referenceTypeId: {
      type: [String, Number],
      default: ''
    },
    initSelectOption: {
      type: Array,
      default: () => []
    }
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  data() {
    return {
      isInit: false,
      options: [],
      innerReferenceShowAttrName: ''
    }
  },
  watch: {
    referenceTypeId: {
      immediate: true,
      deep: true,
      handler() {
        this.isInit = false
      }
    }
  },
  computed: {
    selectCIIds: {
      get() {
        if (this.isList) {
          return this.value || []
        } else {
          return this.value ? Number(this.value) : ''
        }
      },
      set(val) {
        this.$emit('change', val ?? (this.isList ? [] : null))
        return val
      },
    },
  },
  methods: {
    async handleDropdownVisibleChange(open) {
      if (!this.isInit && open && this.referenceTypeId) {
        this.isInit = true

        if (!this.referenceShowAttrName) {
          const res = await getCIType(this.referenceTypeId)
          const ciType = res?.ci_types?.[0]
          this.innerReferenceShowAttrName = ciType?.show_name || ciType?.unique_name || ''
        }

        const attrName = this.referenceShowAttrName || this.innerReferenceShowAttrName || ''
        if (!attrName) {
          return
        }

        const res = await searchCI({
          q: `_type:${this.referenceTypeId}`,
          fl: attrName,
          count: 25,
        })

        let options = res?.result?.map((item) => {
          return {
            key: item._id,
            title: String(item?.[attrName] ?? '')
          }
        })

        options = _.uniqBy([...this.initSelectOption, ...options], 'key')

        this.options = options
      }
    },

    handleSearch: debounce(async function(v) {
      const attrName = this.referenceShowAttrName || this.innerReferenceShowAttrName || ''

      if (!attrName || !this.referenceTypeId) {
        return
      }

      const res = await searchCI({
        q: `_type:${this.referenceTypeId}${v ? ',*' + v + '*' : ''}`,
        fl: attrName,
        count: v ? 100 : 25,
      })

      this.options = res?.result?.map((item) => {
        return {
          key: item._id,
          title: String(item?.[attrName] ?? '')
        }
      })
    }, 300),

    handleChange(v) {
      if (Array.isArray(v) ? !v.length : !v) {
        this.handleSearch()
      }
    }
  }
}
</script>

<style lang="less" scoped>
.reference-attr-select-wrap {
  width: 100%;

  .reference-attr-select {
    width: 100%;

    /deep/ .ant-select-dropdown {
      z-index: 15;
    }
  }
}
</style>
