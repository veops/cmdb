<template>
  <div>
    <a-popover
      v-if="isDropdown"
      v-model="visible"
      trigger="click"
      :placement="placement"
      overlayClassName="table-filter"
      @visibleChange="visibleChange"
    >
      <slot name="popover_item">
        <a-button type="primary" ghost>条件过滤<a-icon type="filter"/></a-button>
      </slot>
      <template slot="content">
        <Expression
          v-model="ruleList"
          :canSearchPreferenceAttrList="canSearchPreferenceAttrList.filter((attr) => !attr.is_password)"
        />
        <a-divider :style="{ margin: '10px 0' }" />
        <div style="width:534px">
          <a-space :style="{ display: 'flex', justifyContent: 'flex-end' }">
            <a-button type="primary" size="small" @click="handleSubmit">确定</a-button>
            <a-button size="small" @click="handleClear">清空</a-button>
          </a-space>
        </div>
      </template>
    </a-popover>
    <Expression
      v-else
      v-model="ruleList"
      :canSearchPreferenceAttrList="canSearchPreferenceAttrList.filter((attr) => !attr.is_password)"
    />
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import Expression from './expression.vue'
import { advancedExpList, compareTypeList } from './constants'

export default {
  name: 'FilterComp',
  components: { Expression },
  props: {
    canSearchPreferenceAttrList: {
      type: Array,
      required: true,
      default: () => [],
    },
    expression: {
      type: String,
      default: '',
    },
    regQ: {
      type: String,
      default: '(?<=q=).+(?=&)|(?<=q=).+$',
    },
    placement: {
      type: String,
      default: 'bottomRight',
    },
    isDropdown: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      advancedExpList,
      compareTypeList,
      visible: false,
      ruleList: [],
      filterExp: '',
    }
  },

  methods: {
    visibleChange(open, isInitOne = true) {
      // isInitOne  初始化exp为空时，ruleList是否默认给一条
      //   const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const exp = this.expression.match(new RegExp(this.regQ, 'g'))
        ? this.expression.match(new RegExp(this.regQ, 'g'))[0]
        : null
      if (open && exp) {
        const expArray = exp.split(',').map((item) => {
          let has_not = ''
          const key = item.split(':')[0]
          const val = item
            .split(':')
            .slice(1)
            .join(':')
          let type, property, exp, value, min, max, compareType
          if (key.includes('-')) {
            type = 'or'
            if (key.includes('~')) {
              property = key.substring(2)
              has_not = '~'
            } else {
              property = key.substring(1)
            }
          } else {
            type = 'and'
            if (key.includes('~')) {
              property = key.substring(1)
              has_not = '~'
            } else {
              property = key
            }
          }

          const in_reg = /(?<=\().+(?=\))/g
          const range_reg = /(?<=\[).+(?=\])/g
          const compare_reg = /(?<=>=|<=|>(?!=)|<(?!=)).+/
          if (val === '*') {
            exp = has_not + 'value'
            value = ''
          } else if (in_reg.test(val)) {
            exp = has_not + 'in'
            value = val.match(in_reg)[0]
          } else if (range_reg.test(val)) {
            exp = has_not + 'range'
            value = val.match(range_reg)[0]
            min = value.split('_TO_')[0]
            max = value.split('_TO_')[1]
          } else if (compare_reg.test(val)) {
            exp = has_not + 'compare'
            value = val.match(compare_reg)[0]
            const _compareType = val.substring(0, val.match(compare_reg)['index'])
            const idx = compareTypeList.findIndex((item) => item.label === _compareType)
            compareType = compareTypeList[idx].value
          } else if (!val.includes('*')) {
            exp = has_not + 'is'
            value = val
          } else {
            const resList = [
              ['contain', /(?<=\*).*(?=\*)/g],
              ['end_with', /(?<=\*).+/g],
              ['start_with', /.+(?=\*)/g],
            ]
            for (let i = 0; i < 3; i++) {
              const reg = resList[i]
              if (reg[1].test(val)) {
                exp = has_not + reg[0]
                value = val.match(reg[1])[0]
                break
              }
            }
          }
          return {
            id: uuidv4(),
            type,
            property,
            exp,
            value,
            min,
            max,
            compareType,
          }
        })
        this.ruleList = [...expArray]
      } else if (open) {
        const _canSearchPreferenceAttrList = this.canSearchPreferenceAttrList.filter((attr) => !attr.is_password)
        this.ruleList = isInitOne
          ? [
              {
                id: uuidv4(),
                type: 'and',
                property:
                  _canSearchPreferenceAttrList && _canSearchPreferenceAttrList.length
                    ? _canSearchPreferenceAttrList[0].name
                    : undefined,
                exp: 'is',
                value: null,
              },
            ]
          : []
      }
    },
    handleClear() {
      this.ruleList = [
        {
          id: uuidv4(),
          type: 'and',
          property: this.canSearchPreferenceAttrList[0].name,
          exp: 'is',
          value: null,
        },
      ]
      this.filterExp = ''
      this.visible = false
      this.$emit('setExpFromFilter', this.filterExp)
    },
    handleSubmit() {
      if (this.ruleList && this.ruleList.length) {
        this.ruleList[0].type = 'and' // 增删后，以防万一第一个不是and
        this.filterExp = ''
        const expList = this.ruleList.map((rule) => {
          let singleRuleExp = ''
          let _exp = rule.exp
          if (rule.type === 'or') {
            singleRuleExp += '-'
          }
          if (rule.exp.includes('~')) {
            singleRuleExp += '~'
            _exp = rule.exp.split('~')[1]
          }
          singleRuleExp += `${rule.property}:`
          if (_exp === 'is') {
            singleRuleExp += `${rule.value ?? ''}`
          }
          if (_exp === 'contain') {
            singleRuleExp += `*${rule.value ?? ''}*`
          }
          if (_exp === 'start_with') {
            singleRuleExp += `${rule.value ?? ''}*`
          }
          if (_exp === 'end_with') {
            singleRuleExp += `*${rule.value ?? ''}`
          }
          if (_exp === 'value') {
            singleRuleExp += `*`
          }
          if (_exp === 'in') {
            singleRuleExp += `(${rule.value ?? ''})`
          }
          if (_exp === 'range') {
            singleRuleExp += `[${rule.min}_TO_${rule.max}]`
          }
          if (_exp === 'compare') {
            const idx = compareTypeList.findIndex((item) => item.value === rule.compareType)
            singleRuleExp += `${compareTypeList[idx].label}${rule.value ?? ''}`
          }
          return singleRuleExp
        })
        this.filterExp = expList.join(',')
        this.$emit('setExpFromFilter', this.filterExp)
      } else {
        this.$emit('setExpFromFilter', '')
      }
      this.visible = false
    },
  },
}
</script>

<style lang="less" scoped>
.table-filter {
  .table-filter-add {
    margin-top: 10px;
    & > a {
      padding: 2px 8px;
      &:hover {
        background-color: #f0faff;
        border-radius: 5px;
      }
    }
  }
  .table-filter-extra-icon {
    padding: 0px 2px;
    &:hover {
      display: inline-block;
      border-radius: 5px;
      background-color: #f0faff;
    }
  }
}
</style>

<style lang="less">
.table-filter-extra-operation {
  .ant-popover-inner-content {
    padding: 3px 4px;
    .operation {
      cursor: pointer;
      width: 90px;
      height: 30px;
      line-height: 30px;
      padding: 3px 4px;
      border-radius: 5px;
      transition: all 0.3s;
      &:hover {
        background-color: #f0faff;
      }
      > .anticon {
        margin-right: 10px;
      }
    }
  }
}
</style>
