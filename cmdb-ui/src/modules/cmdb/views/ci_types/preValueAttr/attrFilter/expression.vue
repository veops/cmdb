<template>
  <div>
    <a-space :style="{ display: 'flex', marginBottom: '10px' }" v-for="(item, index) in ruleList" :key="item.id">
      <div v-if="ruleList.length > 1" :style="{ width: '60px', height: rowHeight, position: 'relative' }">
        <treeselect
          v-if="index !== 0"
          class="custom-treeselect"
          :style="{ width: '60px', '--custom-height': rowHeight, position: 'absolute', top: '-24px' }"
          v-model="item.type"
          :multiple="false"
          :clearable="false"
          searchable
          :options="ruleTypeList"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: node.label,
                children: node.children,
              }
            }
          "
          :disabled="disabled"
        >
        </treeselect>
      </div>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '120px', '--custom-height': rowHeight }"
        v-model="item.property"
        :multiple="false"
        :clearable="false"
        searchable
        :options="canSearchPreferenceAttrList"
        :normalizer="
          (node) => {
            return {
              id: node.name,
              label: node.alias || node.name,
              children: node.children,
            }
          }
        "
        appendToBody
        :zIndex="1050"
        :disabled="disabled"
      >
        <div
          v-if="node.id !== '$count'"
          :title="node.label"
          slot="option-label"
          slot-scope="{ node }"
          class="property-label"
        >
          <ValueTypeMapIcon :attr="node.raw" />
          {{ node.label }}
        </div>
        <div
          v-else
          :title="node.label"
          slot="option-label"
          slot-scope="{ node }"
          class="property-label"
          :style="{ borderBottom: '1px solid #E4E7ED', marginBottom: '8px' }"
        >
          <ValueTypeMapIcon :attr="node.raw" />
          {{ node.label }}
        </div>
        <div
          class="property-label"
          slot="value-label"
          slot-scope="{ node }"
        >
          <ValueTypeMapIcon :attr="node.raw" /> {{ node.label }}
        </div>
      </treeselect>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '90px', '--custom-height': rowHeight }"
        v-model="item.exp"
        :multiple="false"
        :clearable="false"
        searchable
        :options="getExpListByProperty(item.property)"
        :normalizer="
          (node) => {
            return {
              id: node.value,
              label: node.label,
              children: node.children,
            }
          }
        "
        @select="(value) => handleChangeExp(value, item, index)"
        appendToBody
        :zIndex="1050"
        :disabled="disabled"
      >
      </treeselect>
      <ValueControls
        :rule="ruleList[index]"
        :attrList="canSearchPreferenceAttrList"
        :disabled="disabled"
        :curModelAttrList="curModelAttrList"
        :rowHeight="rowHeight"
        @change="(value) => handleChangeValue(value, index)"
      />
      <template v-if="!disabled">
        <a-tooltip :title="$t('copy')">
          <a class="operation" @click="handleCopyRule(item)"><ops-icon type="veops-copy"/></a>
        </a-tooltip>
        <a-tooltip :title="$t('delete')">
          <a class="operation" @click="handleDeleteRule(item)"><a-icon type="minus-circle"/></a>
        </a-tooltip>
        <a-tooltip :title="$t('cmdbFilterComp.addHere')">
          <a class="operation" @click="handleAddRuleAt(item)"><a-icon type="plus-circle"/></a>
        </a-tooltip>
      </template>
    </a-space>
    <div class="table-filter-add" v-if="!disabled && ruleList.length === 0">
      <a @click="handleAddRule">+ {{ $t('new') }}</a>
    </div>
    <div class="attr-filter-tip">{{ $t('cmdb.ciType.attrFilterTip') }}{{ isOpenSource ? ` (${$t('cmdb.enterpriseVersionTip')})` : '' }}</div>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import { ruleTypeList, expList, advancedExpList, compareTypeList } from '../constants.js'
import ValueTypeMapIcon from '@/components/CMDBValueTypeMapIcon'
import ValueControls from './valueControls.vue'

export default {
  name: 'Expression',
  components: {
    ValueTypeMapIcon,
    ValueControls
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    canSearchPreferenceAttrList: {
      type: Array,
      required: true,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    curModelAttrList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      compareTypeList,
      rowHeight: '36px'
    }
  },
  computed: {
    ruleList: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
        return val
      },
    },
    ruleTypeList() {
      return ruleTypeList()
    },
    expList() {
      return expList()
    },
    advancedExpList() {
      return advancedExpList()
    },
  },
  methods: {
    getExpListByProperty(property) {
      if (property === '$count') {
        return [
          { value: 'is', label: this.$t('cmdbFilterComp.is') },
          { value: '~is', label: this.$t('cmdbFilterComp.~is') },
          { value: 'compare', label: this.$t('cmdbFilterComp.compare') }
        ]
      }
      if (property) {
        const _find = this.canSearchPreferenceAttrList.find((item) => item.name === property)
        if (_find && ['0', '1', '3', '4', '5'].includes(_find.value_type)) {
          return [
            { value: 'is', label: this.$t('cmdbFilterComp.is') },
            { value: '~is', label: this.$t('cmdbFilterComp.~is') },
            { value: '~value', label: this.$t('cmdbFilterComp.~value') }, // 为空的定义有点绕
            { value: 'value', label: this.$t('cmdbFilterComp.value') },
            ...this.advancedExpList
          ]
        }
      }
      return [...this.expList, ...this.advancedExpList]
    },
    isChoiceByProperty(property) {
      const _find = this.canSearchPreferenceAttrList.find((item) => item.name === property)
      if (_find) {
        return _find.is_choice
      }
      return false
    },
    handleAddRule() {
      this.ruleList.push({
        id: uuidv4(),
        type: 'and',
        property: this.canSearchPreferenceAttrList[0]?.name,
        exp: 'is',
        value: null,
      })
      this.$emit('change', this.ruleList)
    },
    handleCopyRule(item) {
      this.ruleList.push({ ...item, id: uuidv4() })
      this.$emit('change', this.ruleList)
    },
    handleDeleteRule(item) {
      const idx = this.ruleList.findIndex((r) => r.id === item.id)
      if (idx > -1) {
        this.ruleList.splice(idx, 1)
      }
      this.$emit('change', this.ruleList)
    },
    handleAddRuleAt(item) {
      const idx = this.ruleList.findIndex((r) => r.id === item.id)
      if (idx > -1) {
        this.ruleList.splice(idx + 1, 0, {
          id: uuidv4(),
          type: 'and',
          property: this.canSearchPreferenceAttrList[0]?.name,
          exp: 'is',
          value: null,
        })
      }
      this.$emit('change', this.ruleList)
    },
    getChoiceValueByProperty(property) {
      const _find = this.canSearchPreferenceAttrList.find((item) => item.name === property)
      if (_find) {
        return _find.choice_value
      }
      return []
    },
    handleChangeExp({ value }, item, index) {
      const _ruleList = _.cloneDeep(this.ruleList)
      if (value === 'range') {
        _ruleList[index] = {
          ..._ruleList[index],
          min: '',
          max: '',
          exp: value,
        }
      } else if (value === 'compare') {
        _ruleList[index] = {
          ..._ruleList[index],
          compareType: '1',
          exp: value,
        }
      } else {
        _ruleList[index] = {
          ..._ruleList[index],
          exp: value,
        }
      }
      this.ruleList = _ruleList
      this.$emit('change', this.ruleList)
    },

    handleChangeValue(value, index) {
      const _ruleList = _.cloneDeep(this.ruleList)
      _ruleList[index] = value
      this.$emit('change', _ruleList)
    }
  },
}
</script>

<style lang="less" scoped>
.input-group {
  display: flex;
  align-items: center;
  width: 150px;

  &-range-icon {
    margin: 0 8px;
  }

  input {
    height: 36px;
  }
}

.property-label {
  width: 100%;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden
}

.attr-filter-tip {
  color: #86909C;
  font-size: 12px;
  font-weight: 400;
}
</style>
