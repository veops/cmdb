<template>
  <div>
    <div class="control-group" v-if="controlType === 'choice'" >
      <div
        class="choice-group"
        @click="handleControlType('input')"
      >
        <a-icon class="choice-group-icon" type="caret-down" />
      </div>
      <treeselect
        class="custom-treeselect input-group"
        :style="{ '--custom-height': rowHeight }"
        :value="choiceValue"
        @input="(value) => handleChange('value', value)"
        :multiple="false"
        :clearable="false"
        searchable
        :options="curModelAttrList"
        :placeholder="$t('placeholder2')"
        :normalizer="
          (node) => {
            return {
              id: node.name,
              label: node.name,
              children: node.children,
            }
          }
        "
        appendToBody
        :zIndex="1050"
        :disabled="disabled"
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
    </div>
    <div class="control-group" v-else>
      <div
        class="text-group"
        @click="handleControlType('choice')"
      >
        <ops-icon class="text-group-icon" type="veops-text" />
      </div>
      <CIReferenceAttr
        v-if="getAttr(rule.property).is_reference && (rule.exp === 'is' || rule.exp === '~is')"
        class="select-filter"
        :referenceTypeId="getAttr(rule.property).reference_type_id"
        :value="rule.value"
        :disabled="disabled"
        @change="(value) => handleChange('value', value)"
      />
      <a-select
        v-else-if="getAttr(rule.property).is_bool && (rule.exp === 'is' || rule.exp === '~is')"
        class="select-filter"
        :disabled="disabled"
        :placeholder="$t('placeholder2')"
        :value="rule.value"
        @change="(value) => handleChange('value', value)"
      >
        <a-select-option key="1">
          true
        </a-select-option>
        <a-select-option key="0">
          false
        </a-select-option>
      </a-select>
      <div
        class="input-group"
        v-else-if="isChoiceByProperty(rule.property) && (rule.exp === 'is' || rule.exp === '~is')"
      >
        <treeselect
          class="custom-treeselect"
          :style="{ '--custom-height': rowHeight }"
          :value="rule.value"
          @input="(value) => handleChange('value', value)"
          :multiple="false"
          :clearable="false"
          searchable
          :options="getChoiceValueByProperty(rule.property)"
          :placeholder="$t('placeholder2')"
          :normalizer="
            (node) => {
              return {
                id: String(node[0] || ''),
                label: node[1] ? node[1].label || node[0] : node[0],
                children: node.children && node.children.length ? node.children : undefined,
              }
            }
          "
          appendToBody
          :zIndex="1050"
          :disabled="disabled"
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
      </div>
      <div
        compact
        v-else-if="rule.exp === 'range' || rule.exp === '~range'"
        class="input-group"
      >
        <a-input
          class="ops-input"
          :placeholder="$t('min')"
          :disabled="disabled"
          :value="rule.min"
          @change="(e) => handleChange('min', e.target.value)"
        />
        <span class="input-group-range-icon">~</span>
        <a-input
          class="ops-input"
          v-model="rule.max"
          :placeholder="$t('max')"
          :disabled="disabled"
          :value="rule.max"
          @change="(e) => handleChange('max', e.target.value)"
        />
      </div>
      <div class="input-group" compact v-else-if="rule.exp === 'compare'">
        <treeselect
          class="custom-treeselect"
          :style="{ width: '70px', '--custom-height': rowHeight, 'flex-shrink': 0 }"
          :value="rule.compareType"
          @input="(value) => handleChange('compareType', value)"
          :multiple="false"
          :clearable="false"
          searchable
          :options="compareTypeList"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: node.label,
                children: node.children,
              }
            }
          "
          appendToBody
          :zIndex="1050"
          :disabled="disabled"
        >
        </treeselect>
        <a-input :value="rule.value" @change="(e) => handleChange('value', e.target.value)" class="ops-input"/>
      </div>
      <div class="input-group" v-else-if="rule.exp !== 'value' && rule.exp !== '~value'">
        <a-input
          :value="rule.value"
          @change="(e) => handleChange('value', e.target.value)"
          :placeholder="rule.exp === 'in' || rule.exp === '~in' ? $t('cmdbFilterComp.split', { separator: ';' }) : ''"
          class="ops-input"
          :disabled="disabled"
        ></a-input>
      </div>
      <div v-else :style="{ width: '136px' }"></div>
    </div>
  </div>
</template>

<script>
import { compareTypeList } from '../constants.js'
import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'ValueControls',
  components: {
    CIReferenceAttr
  },
  props: {
    rule: {
      type: Object,
      default: () => {},
    },
    attrList: {
      type: Array,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    // 当前模型属性
    curModelAttrList: {
      type: Array,
      default: () => []
    },
    // 行高
    rowHeight: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      compareTypeList,
      controlType: 'input',
    }
  },
  computed: {
    choiceValue() {
      const regex = /\{\{([^}]+)\}\}/g
      const val = regex.exec(this?.rule?.value || '')
      return val ? val?.[1]?.trim() || '' : this?.value?.value || ''
    }
  },
  methods: {
    isChoiceByProperty(property) {
      const _find = this.attrList.find((item) => item.name === property)
      if (_find) {
        return _find.is_choice
      }
      return false
    },
    getChoiceValueByProperty(property) {
      const _find = this.attrList.find((item) => item.name === property)
      if (_find) {
        return _find.choice_value
      }
      return []
    },
    handleControlType(type) {
      this.controlType = type
    },
    handleChange(key, value) {
      if (this.controlType === 'choice' && key === 'value') {
        value = `{{ ${value} }}`
      }

      this.$emit('change', {
        ...this.rule,
        [key]: value
      })
    },
    getAttr(property) {
      return this.attrList.find((item) => item.name === property) || {}
    },
  }
}
</script>

<style lang="less" scoped>
.control-group {
  display: flex;
}

.input-group {
  display: flex;
  align-items: center;
  width: 136px;

  &-range-icon {
    margin: 0 8px;
  }

  input {
    height: 36px;
  }
}

.choice-group {
  width: 14px;
  height: 36px;
  flex-shrink: 0;
  background-color: #00B3CC;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &-icon {
    font-size: 12px;
    color: #FFFFFF;
  }
}

.text-group {
  width: 14px;
  height: 36px;
  flex-shrink: 0;
  background-color: #2F54EB;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &-icon {
    font-size: 12px;
    color: #FFFFFF;
  }
}

.select-filter {
  height: 36px;
  width: 136px;

  /deep/ .ant-select-selection {
    height: 36px;
    background: #f7f8fa;
    line-height: 36px;
    border: none;

    .ant-select-selection__rendered {
      height: 36px;
      line-height: 36px;
    }
  }
}
</style>
