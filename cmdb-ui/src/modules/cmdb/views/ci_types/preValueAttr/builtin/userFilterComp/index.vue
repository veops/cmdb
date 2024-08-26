<template>
  <div class="user-filter">
    <a-button
      v-if="!ruleList.length"
      type="primary"
      ghost
      size="small"
      class="add-btn"
      @click="handleAddRule"
    >
      <a-icon type="plus" />
      {{ $t('add') }}
    </a-button>
    <template v-else>
      <a-space :style="{ display: 'flex', marginBottom: '10px' }" v-for="(item, index) in ruleList" :key="item.id">
        <div :style="{ width: '50px', height: '24px', position: 'relative' }">
          <treeselect
            v-if="index"
            class="custom-treeselect"
            :style="{ width: '50px', '--custom-height': '36px', position: 'absolute', top: '-30px', left: 0 }"
            v-model="item.relation"
            :multiple="false"
            :clearable="false"
            searchable
            :options="ruleTypeList"
            :normalizer="
              (node) => {
                return {
                  id: node.value,
                  label: $t(node.label),
                  children: node.children,
                }
              }
            "
          >
          </treeselect>
        </div>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '140px', '--custom-height': '36px' }"
          v-model="item.column"
          :multiple="false"
          :clearable="false"
          searchable
          :options="userFilterSelect"
          :maxHeight="150"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: $t(node.label),
                children: node.children,
              }
            }
          "
        >
          <div
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            <a-tooltip :title="$t(node.label)">
              {{ $t(node.label) }}
            </a-tooltip>
          </div>
          <div
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
            slot="value-label"
            slot-scope="{ node }"
          >
            <a-tooltip :title="$t(node.label)">
              {{ $t(node.label) }}
            </a-tooltip>
          </div>
        </treeselect>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '90px', '--custom-height': '36px' }"
          v-model="item.operator"
          :multiple="false"
          :clearable="false"
          searchable
          :options="[...expList, ...compareTypeList]"
          :maxHeight="150"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: $t(node.label),
                children: node.children,
              }
            }
          "
          @select="(value) => handleChangeExp(value, item, index)"
        >
          <div
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            <a-tooltip :title="$t(node.label)">
              {{ $t(node.label) }}
            </a-tooltip>
          </div>
          <div
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
            slot="value-label"
            slot-scope="{ node }"
          >
            <a-tooltip :title="$t(node.label)">
              {{ $t(node.label) }}
            </a-tooltip>
          </div>
        </treeselect>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '100px', '--custom-height': '36px' }"
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
                label: $t(node.label),
                children: node.children,
              }
            }
          "
        >
          <div
            :title="$t(node.label)"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            {{ $t(node.label) }}
          </div>
        </treeselect>
        <div v-else-if="item.column === 'direct_supervisor_id' && (item.operator === 1 || item.operator === 2)">
          <EmployeeTreeSelect v-model="item.value" className="custom-treeselect"/>
        </div>
        <a-input
          v-else-if="item.operator !== 7 && item.operator !== 8"
          size="small"
          v-model="item.value"
          :placeholder="item.exp === 'in' || item.exp === '~in' ? $t('cs.components.operatorInPlaceholder') : ''"
          class="ops-input"
        ></a-input>
        <a-tooltip :title="$t('cs.components.copy')">
          <a class="operation" @click="handleCopyRule(item)"><ops-icon type="veops-copy"/></a>
        </a-tooltip>
        <a-tooltip :title="$t('delete')">
          <a class="operation" @click="handleDeleteRule(item)"><ops-icon type="veops-reduce"/></a>
        </a-tooltip>
        <a-tooltip :title="$t('add')">
          <a class="operation" @click="handleAddRule"><ops-icon type="veops-increase"/></a>
        </a-tooltip>
      </a-space>
    </template>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import Treeselect from '@riophae/vue-treeselect'
import { ruleTypeList, expList, compareTypeList } from './constants'
import { USER_FILTER_SELECT } from '../constants'
import EmployeeTreeSelect from './employeeTreeSelect.vue'

export default {
  name: 'UserFilterComp',
  components: {
    Treeselect,
    EmployeeTreeSelect
  },
  data() {
    return {
      USER_FILTER_SELECT,
      ruleTypeList,
      expList,
      compareTypeList,
      ruleList: [],
      filterExp: '',
      userFilterSelect: [],
    }
  },
  methods: {
    async setRuleList(ruleList) {
      this.ruleList = ruleList?.length ? ruleList : []
    },
    handleAddRule() {
      this.ruleList.push({
        id: uuidv4(),
        relation: '&',
        column: this.userFilterSelect?.[0]?.value ?? null,
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

    getRuleList() {
      if (this.ruleList && this.ruleList.length) {
        const ruleList = _.cloneDeep(this.ruleList)
        ruleList.forEach((item, index) => {
          if (item.column === 'direct_supervisor_id') {
            ruleList[index].value = item.value ? (item.value + '').includes('-') ? +item.value.split('-')[1] : +item.value : 0
          }
        })
        if (ruleList?.length > 0) {
          ruleList[0].relation = '&'
        }

        return ruleList.map((rule) => {
          return _.omit(rule, 'id')
        })
      }

      return []
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
    isChoiceByProperty(column) {
      const _find = this.userFilterSelect.find((item) => item.value === column)
      if (_find) {
        return _find.is_choice
      }
      return false
    },
    getChoiceValueByProperty(column) {
      const _find = this.userFilterSelect.find((item) => item.value === column)
      if (_find) {
        return _find.choice_value
      }
      return []
    },
  },
}
</script>

<style lang="less" scoped>
.user-filter {
  display: flex;
  flex-direction: column;
  line-height: 36px;

  .ops-input {
    height: 36px;
    width: 100px;
  }
}

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

.add-btn {
  font-size: 12px;
  width: 80px;
  margin-top: 10px;
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
