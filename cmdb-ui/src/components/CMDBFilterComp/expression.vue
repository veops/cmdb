<template>
  <div>
    <a-space :style="{ display: 'flex', marginBottom: '10px' }" v-for="(item, index) in ruleList" :key="item.id">
      <div :style="{ width: '50px', height: '24px', position: 'relative' }">
        <treeselect
          v-if="index"
          class="custom-treeselect"
          :style="{ width: '50px', '--custom-height': '24px', position: 'absolute', top: '-17px', left: 0 }"
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
        >
        </treeselect>
      </div>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '130px', '--custom-height': '24px' }"
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
      >
        <div
          :title="node.label"
          slot="option-label"
          slot-scope="{ node }"
          :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
        >
          <ValueTypeMapIcon :attr="node.raw" />
          {{ node.label }}
        </div>
        <div
          :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          slot="value-label"
          slot-scope="{ node }"
        >
          <ValueTypeMapIcon :attr="node.raw" /> {{ node.label }}
        </div>
      </treeselect>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '100px', '--custom-height': '24px' }"
        v-model="item.exp"
        :multiple="false"
        :clearable="false"
        searchable
        :options="[...getExpListByProperty(item.property), ...advancedExpList]"
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
      >
      </treeselect>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '175px', '--custom-height': '24px' }"
        v-model="item.value"
        :multiple="false"
        :clearable="false"
        searchable
        v-if="isChoiceByProperty(item.property) && (item.exp === 'is' || item.exp === '~is')"
        :options="getChoiceValueByProperty(item.property)"
        placeholder="请选择"
        :normalizer="
          (node) => {
            return {
              id: node[0],
              label: node[0],
              children: node.children,
            }
          }
        "
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
      <a-input-group
        size="small"
        compact
        v-else-if="item.exp === 'range' || item.exp === '~range'"
        :style="{ width: '175px' }"
      >
        <a-input class="ops-input" size="small" v-model="item.min" :style="{ width: '78px' }" placeholder="最小值" />
        ~
        <a-input class="ops-input" size="small" v-model="item.max" :style="{ width: '78px' }" placeholder="最大值" />
      </a-input-group>
      <a-input-group size="small" compact v-else-if="item.exp === 'compare'" :style="{ width: '175px' }">
        <treeselect
          class="custom-treeselect"
          :style="{ width: '60px', '--custom-height': '24px' }"
          v-model="item.compareType"
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
        >
        </treeselect>
        <a-input class="ops-input" v-model="item.value" size="small" style="width: 113px" />
      </a-input-group>
      <a-input
        v-else-if="item.exp !== 'value' && item.exp !== '~value'"
        size="small"
        v-model="item.value"
        :placeholder="item.exp === 'in' || item.exp === '~in' ? '以 ; 分隔' : ''"
        class="ops-input"
      ></a-input>
      <div v-else :style="{ width: '175px' }"></div>
      <a-tooltip title="复制">
        <a class="operation" @click="handleCopyRule(item)"><ops-icon type="icon-xianxing-copy"/></a>
      </a-tooltip>
      <a-tooltip title="删除">
        <a class="operation" @click="handleDeleteRule(item)"><ops-icon type="icon-xianxing-delete"/></a>
      </a-tooltip>
    </a-space>
    <div class="table-filter-add">
      <a @click="handleAddRule">+ 新增</a>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import { ruleTypeList, expList, advancedExpList, compareTypeList } from './constants'
import ValueTypeMapIcon from '../CMDBValueTypeMapIcon'

export default {
  name: 'Expression',
  components: { ValueTypeMapIcon },
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
  },
  data() {
    return {
      ruleTypeList,
      expList,
      advancedExpList,
      compareTypeList,
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
  },
  methods: {
    getExpListByProperty(property) {
      if (property) {
        const _find = this.canSearchPreferenceAttrList.find((item) => item.name === property)
        if (_find && ['0', '1', '3', '4', '5'].includes(_find.value_type)) {
          return [
            { value: 'is', label: '等于' },
            { value: '~is', label: '不等于' },
            { value: '~value', label: '为空' }, // 为空的定义有点绕
            { value: 'value', label: '不为空' },
          ]
        }
        return this.expList
      }
      return this.expList
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
  },
}
</script>

<style></style>
