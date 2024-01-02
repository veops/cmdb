<template>
  <a-popover
    v-model="visible"
    trigger="click"
    :placement="placement"
    overlayClassName="table-filter"
    @visibleChange="visibleChange"
  >
    <slot name="popover_item">
      <a-button type="primary" ghost>{{ $t('cs.components.conditionFilter') }}<a-icon type="filter"/></a-button>
    </slot>
    <template slot="content">
      <svg
        :style="{ position: 'absolute', top: '0', left: '0', width: '110px', height: '100%', zIndex: '-1' }"
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        height="100%"
        width="100%"
        id="svgDom"
      ></svg>
      <a-space :style="{ display: 'flex', marginBottom: '10px' }" v-for="(item, index) in ruleList" :key="item.id">
        <div :style="{ width: '50px', height: '24px', position: 'relative' }">
          <treeselect
            v-if="index"
            class="custom-treeselect"
            :style="{ width: '50px', '--custom-height': '24px', position: 'absolute', top: '-17px', left: 0 }"
            v-model="item.relation"
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
          v-model="item.column"
          :multiple="false"
          :clearable="false"
          searchable
          :options="canSearchPreferenceAttrList"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: node.label,
                children: node.children,
              }
            }
          "
        >value
          <div
            :title="node.label"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            <!-- <ValueTypeMapIcon :attr="node.raw" /> -->
            {{ node.label }}
          </div>
          <div
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
            slot="value-label"
            slot-scope="{ node }"
          >
            <!-- <ValueTypeMapIcon :attr="node.raw" /> -->
            {{ node.label }}
          </div>
        </treeselect>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '100px', '--custom-height': '24px' }"
          v-model="item.operator"
          :multiple="false"
          :clearable="false"
          searchable
          :options="[...expList, ...compareTypeList]"
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
          v-if="isChoiceByProperty(item.column) && (item.operator === 1 || item.operator === 2)"
          :options="getChoiceValueByProperty(item.column)"
          :placeholder="$t('cs.components.selectPlaceholder')"
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
          <div
            :title="node.label"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            {{ node.label }}
          </div>
        </treeselect>
        <div v-else-if="item.column === 'direct_supervisor_id' && (item.operator === 1 || item.operator === 2)" style="width: 175px">
          <EmployeeTreeSelect v-model="item.value" className="custom-treeselect"/>
        </div>
        <a-input
          v-else-if="item.operator !== 7 && item.operator !== 8"
          size="small"
          v-model="item.value"
          :placeholder="item.exp === 'in' || item.exp === '~in' ? $t('cs.components.operatorInPlaceholder') : ''"
          class="ops-input"
        ></a-input>
        <!-- <div v-else :style="{ width: '175px' }"></div> -->
        <a-tooltip :title="$t('cs.components.copy')">
          <a class="operation" @click="handleCopyRule(item)"><a-icon type="copy"/></a>
        </a-tooltip>
        <a-tooltip :title="$t('delete')">
          <a class="operation" @click="handleDeleteRule(item)" :style="{ color: 'red' }"><a-icon type="delete"/></a>
        </a-tooltip>

      </a-space>
      <div class="table-filter-add">
        <a @click="handleAddRule">+ {{ $t('new') }}</a>
      </div>
      <a-divider :style="{ margin: '10px 0' }" />
      <div style="width:534px">
        <a-space :style="{ display: 'flex', justifyContent: 'flex-end' }">
          <a-button type="primary" size="small" @click="handleSubmit">{{ $t('confirm') }}</a-button>
          <a-button size="small" @click="handleClear">{{ $t('clear') }}</a-button>
        </a-space>
      </div>
    </template>
  </a-popover>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import Treeselect from '@riophae/vue-treeselect'
import { ruleTypeList, expList, advancedExpList, compareTypeList } from './constants'
import DepartmentTreeSelect from '../../components/departmentTreeSelect.vue'
import EmployeeTreeSelect from '../../components/employeeTreeSelect.vue'

export default {
  name: 'FilterComp',
  components: {
    //   ValueTypeMapIcon,
    Treeselect,
    DepartmentTreeSelect,
    EmployeeTreeSelect },
  props: {
    canSearchPreferenceAttrList: {
      type: Array,
      required: true,
      default: () => [],
    },
    regQ: {
      type: String,
      default: '(?<=q=).+(?=&)|(?<=q=).+$',
    },
    placement: {
      type: String,
      default: 'bottomRight',
    },
  },
  data() {
    return {
      ruleTypeList,
      expList,
      advancedExpList,
      compareTypeList,
      visible: false,
      ruleList: [],
      filterExp: '',
    }
  },
  inject: ['provide_allFlatEmployees'],
  computed: {
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    }
  },
  methods: {
    visibleChange(open) {
      //   const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const _exp = this.ruleList.length
        ? this.ruleList
        : null
      if (open && _exp) {
        _exp.forEach((item, index) => {
          if (item.column === 'direct_supervisor_id' && item.value) {
            if (!(item.value + '').includes('-')) {
              const _find = this.allFlatEmployees.find((v) => v.employee_id === item.value)
              _exp[index].value = `${_find.department_id}-${item.value}`
            }
          }
        })
        this.ruleList = _exp
      } else if (open) {
        this.ruleList = [
          {
            id: uuidv4(),
            relation: '&',
            column: this.canSearchPreferenceAttrList[0].value,
            operator: 1,
            value: null,
          },
        ]
      }
    },
    handleAddRule() {
      this.ruleList.push({
        id: uuidv4(),
        relation: '&',
        column: this.canSearchPreferenceAttrList[0].value,
        operator: 1,
        value: null,
      })
    },
    handleCopyRule(item) {
      this.ruleList.push({ ...item, id: uuidv4() })
    },
    handleDeleteRule(item) {
      const idx = this.ruleList.findIndex((r) => r.id === item.id)
      if (idx > -1) {
        this.ruleList.splice(idx, 1)
      }
    },
    handleClear() {
      this.ruleList = [
        {
          id: uuidv4(),
          relation: '&',
          column: this.canSearchPreferenceAttrList[0].value,
          operator: 1,
          value: null,
        },
      ]
      this.filterExp = []
      this.visible = false
      this.$emit('setExpFromFilter', this.filterExp)
    },
    handleSubmit() {
      if (this.ruleList && this.ruleList.length) {
        const getDataFromRuleList = this.ruleList
        getDataFromRuleList.forEach((item, index) => {
          if (item.column === 'direct_supervisor_id') {
            getDataFromRuleList[index].value = item.value ? (item.value + '').includes('-') ? +item.value.split('-')[1] : +item.value : 0
          }
        })
        getDataFromRuleList[0].relation = '&' // 增删后，以防万一第一个不是and
        this.$emit('setExpFromFilter', getDataFromRuleList)
      } else {
        this.$emit('setExpFromFilter', '')
      }
      this.visible = false
    },
    handleChangeExp({ value }, item, index) {
      const _ruleList = _.cloneDeep(this.ruleList)
      if (value === 7 || value === 8) {
         _ruleList[index] = {
          ..._ruleList[index],
          value: null,
          operator: value
        }
      } else {
        _ruleList[index] = {
          ..._ruleList[index],
          operator: value,
        }
      }
      this.ruleList = _ruleList
    },
    filterOption(input, option) {
      return option.componentOptions.children[1].children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
    // getExpListByProperty(column) {
    //   if (column) {
    //     const _find = this.canSearchPreferenceAttrList.find((item) => item.value === column)
    //     if (_find && ['0', '1', '3', '4', '5'].includes(_find.value_type)) {
    //       return [
    //         { value: 'is', label: '等于' },
    //         { value: '~is', label: '不等于' },
    //         { value: '~value', label: '为空' }, // 为空的定义有点绕
    //         { value: 'value', label: '不为空' },
    //       ]
    //     }
    //     return this.expList
    //   }
    //   return this.expList
    // },
    isChoiceByProperty(column) {
      const _find = this.canSearchPreferenceAttrList.find((item) => item.value === column)
      if (_find) {
        return _find.is_choice
      }
      return false
    },
    getChoiceValueByProperty(column) {
      const _find = this.canSearchPreferenceAttrList.find((item) => item.value === column)
      if (_find) {
        return _find.choice_value
      }
      return []
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

<style lang="less" scoped>
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
