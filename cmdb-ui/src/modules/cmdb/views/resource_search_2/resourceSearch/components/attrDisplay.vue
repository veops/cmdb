<template>
  <div :class="['attr-display', isEllipsis ? 'attr-display-ellipsis' : '']">
    <template v-if="attr.is_reference && ci[attr.name]" >
      <a
        v-for="(ciId) in (attr.is_list ? ci[attr.name] : [ci[attr.name]])"
        :key="ciId"
        :href="`/cmdb/cidetail/${attr.reference_type_id}/${ciId}`"
        target="_blank"
      >
        {{ getReferenceAttrValue(ciId) }}
      </a>
    </template>
    <span v-else-if="attr.value_type === '6' && ci[attr.name]">{{ JSON.stringify(ci[attr.name]) }}</span>
    <template v-else-if="attr.is_link && ci[attr.name]">
      <a
        v-for="(item, linkIndex) in (attr.is_list ? ci[attr.name] : [ci[attr.name]])"
        :key="linkIndex"
        :href="
          item.startsWith('http') || item.startsWith('https')
            ? `${item}`
            : `http://${item}`
        "
        target="_blank"
      >
        {{ getChoiceValueLabel(item) || item }}
      </a>
    </template>
    <PasswordField
      v-else-if="attr.is_password && ci[attr.name]"
      :ci_id="ci._id"
      :attr_id="attr.id"
    ></PasswordField>
    <template v-else-if="attr.is_choice">
      <span
        v-for="value in (attr.is_list ? ci[attr.name] : [ci[attr.name]])"
        :key="value"
        :style="{
          borderRadius: '4px',
          padding: '1px 5px',
          margin: '2px',
          ...getChoiceValueStyle(value),
        }"
      >
        <ops-icon
          :style="{ color: getChoiceValueIcon(attr, value).color }"
          :type="getChoiceValueIcon(attr, value).name"
        />
        <span
          v-html="markSearchValue(getChoiceValueLabel(value) || value)"
        ></span>
      </span>
    </template>
    <span
      v-else
      v-html="markSearchValue((attr.is_list && Array.isArray(ci[attr.name])) ? ci[attr.name].join(',') : ci[attr.name])"
    ></span>
  </div>
</template>

<script>
import PasswordField from '@/modules/cmdb/components/passwordField/index.vue'

export default {
  name: 'AttrDisplay',
  components: {
    PasswordField
  },
  props: {
    attr: {
      type: Object,
      default: () => {}
    },
    ci: {
      type: Object,
      default: () => {}
    },
    isEllipsis: {
      type: Boolean,
      default: false
    },
    referenceShowAttrNameMap: {
      type: Object,
      default: () => {}
    },
    referenceCIIdMap: {
      type: Object,
      default: () => {}
    },
    searchValue: {
      type: String,
      default: ''
    }
  },
  methods: {
    markSearchValue(text) {
      if (!text || !this.searchValue) {
        return text
      }
      const regex = new RegExp(`(${this.searchValue})`, 'gi')
      return String(text).replace(
        regex,
        `<span style="background-color: #D3EEFE; padding: 0 2px;">$1</span>`
      )
    },
    getChoiceValueStyle(attrValue) {
      const _find = this?.attr?.choice_value?.find?.((item) => String(item?.[0]) === String(attrValue))
      if (_find) {
        return _find?.[1]?.style || {}
      }
      return {}
    },
    getChoiceValueIcon(attrValue) {
      const _find = this?.attr?.choice_value?.find((item) => String(item?.[0]) === String(attrValue))
      if (_find) {
        return _find?.[1]?.icon || {}
      }
      return {}
    },
    getChoiceValueLabel(attrValue) {
      const _find = this?.attr?.choice_value?.find((item) => String(item?.[0]) === String(attrValue))
      if (_find) {
        return _find?.[1]?.label || ''
      }
      return ''
    },
    getReferenceAttrValue(id) {
      if (this.attr.referenceShowAttrNameMap?.[id]) {
        return this.attr.referenceShowAttrNameMap[id]
      }

      const ci = this?.referenceCIIdMap?.[this?.attr?.reference_type_id]?.[id]
      if (!ci) {
        return id
      }

      const attrName = this.referenceShowAttrNameMap?.[this?.attr.reference_type_id]
      return ci?.[attrName] || id
    },
  }
}
</script>

<style lang="less" scoped>
.attr-display {
  width: 100%;
  font-size: 14px;
  font-weight: 400;
  word-break: break-all;

  &-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
  }
}
</style>
