<template>
  <div>
    <div id="search-form-bar" class="search-form-bar">
      <div :style="{ display: 'inline-flex', alignItems: 'center' }">
        <a-space>
          <treeselect
            v-if="type === 'resourceSearch'"
            class="custom-treeselect"
            :style="{ width: '250px', marginRight: '10px', '--custom-height': '32px' }"
            v-model="currenCiType"
            :multiple="true"
            :clearable="true"
            searchable
            :options="ciTypeGroup"
            :limit="1"
            :limitText="(count) => `+ ${count}`"
            value-consists-of="LEAF_PRIORITY"
            placeholder="模型"
            @close="closeCiTypeGroup"
            @open="openCiTypeGroup"
            @input="inputCiTypeGroup"
            :normalizer="
              (node) => {
                return {
                  id: node.id || -1,
                  label: node.alias || node.name || '其他',
                  title: node.alias || node.name || '其他',
                  children: node.ci_types,
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
          <a-input
            v-model="fuzzySearch"
            :style="{ display: 'inline-block', width: '244px' }"
            placeholder="请查找"
            @pressEnter="emitRefresh"
            class="ops-input ops-input-radius"
          >
            <a-icon
              type="search"
              slot="suffix"
              :style="{ color: fuzzySearch ? '#2f54eb' : '', cursor: 'pointer' }"
              @click="emitRefresh"
            />
            <a-tooltip slot="prefix" placement="bottom" :overlayStyle="{ maxWidth: '550px' }">
              <template slot="title">
                1、json属性不能搜索<br />2、搜索内容包括逗号，则需转义 \,<br />3、只搜索索引属性，非索引属性使用条件过滤
              </template>
              <a><a-icon type="question-circle"/></a>
            </a-tooltip>
          </a-input>
          <FilterComp
            ref="filterComp"
            :canSearchPreferenceAttrList="canSearchPreferenceAttrList"
            @setExpFromFilter="setExpFromFilter"
            :expression="expression"
            placement="bottomLeft"
          >
            <div slot="popover_item" class="search-form-bar-filter">
              <a-icon class="search-form-bar-filter-icon" type="filter" />
              条件过滤
              <a-icon class="search-form-bar-filter-icon" type="down" />
            </div>
          </FilterComp>
          <a-input
            v-if="isShowExpression"
            v-model="expression"
            v-show="!selectedRowKeys.length"
            @focus="
              () => {
                isFocusExpression = true
              }
            "
            @blur="
              () => {
                isFocusExpression = false
              }
            "
            class="ci-searchform-expression"
            :style="{ width }"
            :placeholder="placeholder"
            @keyup.enter="emitRefresh"
          >
            <a-icon slot="suffix" type="copy" @click="handleCopyExpression" />
          </a-input>
          <slot></slot>
        </a-space>
      </div>
      <a-space>
        <a-button @click="reset" size="small">重置</a-button>
        <a-tooltip title="属性说明" v-if="type === 'relationView'">
          <a
            @click="
              () => {
                $refs.metadataDrawer.open(typeId)
              }
            "
          ><a-icon
            v-if="type === 'relationView'"
            type="question-circle"
          /></a>
        </a-tooltip>
      </a-space>
    </div>
    <MetadataDrawer ref="metadataDrawer" />
  </div>
</template>

<script>
import _ from 'lodash'
import Treeselect from '@riophae/vue-treeselect'
import MetadataDrawer from '../../views/ci/modules/MetadataDrawer.vue'
import FilterComp from '@/components/CMDBFilterComp'
import { getCITypeGroups } from '../../api/ciTypeGroup'
export default {
  name: 'SearchForm',
  components: { MetadataDrawer, FilterComp, Treeselect },
  props: {
    preferenceAttrList: {
      type: Array,
      required: true,
    },
    isShowExpression: {
      type: Boolean,
      default: true,
    },
    typeId: {
      type: Number,
      default: null,
    },
    type: {
      type: String,
      default: '',
    },
    selectedRowKeys: {
      type: Array,
      default: () => [],
    }
  },
  data() {
    return {
      // 高级搜索 展开/关闭
      advanced: false,
      queryParam: {},
      isFocusExpression: false,
      expression: '',
      fuzzySearch: '',
      currenCiType: [],
      ciTypeGroup: [],
      lastCiType: [],
    }
  },

  computed: {
    placeholder() {
      return this.isFocusExpression ? '例：q=hostname:*0.0.0.0*' : '表达式'
    },
    width() {
      return '200px'
    },
    canSearchPreferenceAttrList() {
      return this.preferenceAttrList.filter((item) => item.value_type !== '6')
    },
  },
  watch: {
    '$route.path': function(newValue, oldValue) {
      this.queryParam = {}
      this.expression = ''
      this.fuzzySearch = ''
    },
  },
  inject: ['setPreferenceSearchCurrent'],
  mounted() {
    if (this.type === 'resourceSearch') {
      this.getCITypeGroups()
    }
  },
  methods: {
    getCITypeGroups() {
      getCITypeGroups({ need_other: true }).then((res) => {
        this.ciTypeGroup = res
          .filter((item) => item.ci_types && item.ci_types.length)
          .map((item) => {
            item.id = `parent_${item.id || -1}`
            return { ..._.cloneDeep(item) }
          })
      })
    },
    reset() {
      this.queryParam = {}
      this.expression = ''
      this.fuzzySearch = ''
      this.currenCiType = []
      this.emitRefresh()
    },
    setExpFromFilter(filterExp) {
      const regSort = /(?<=sort=).+/g
      const expSort = this.expression.match(regSort) ? this.expression.match(regSort)[0] : undefined
      let expression = ''
      if (filterExp) {
        expression = `q=${filterExp}`
      }
      if (expSort) {
        expression += `&sort=${expSort}`
      }
      this.expression = expression
      this.emitRefresh()
    },
    handleSubmit() {
      this.$refs.filterComp.handleSubmit()
    },
    openCiTypeGroup() {
      this.lastCiType = _.cloneDeep(this.currenCiType)
    },
    closeCiTypeGroup(value) {
      if (!_.isEqual(value, this.lastCiType)) {
        this.$emit('updateAllAttributesList', value)
      }
    },
    inputCiTypeGroup(value) {
      console.log(value)
      if (!value || !value.length) {
        this.$emit('updateAllAttributesList', value)
      }
    },
    emitRefresh() {
      this.setPreferenceSearchCurrent(null)
      this.$nextTick(() => {
        this.$emit('refresh', true)
      })
    },
    handleCopyExpression() {
      this.$emit('copyExpression')
    },
  },
}
</script>
<style lang="less">
@import '../../views/index.less';
.ci-searchform-expression {
  > input {
    border-bottom: 2px solid #d9d9d9;
    border-top: none;
    border-left: none;
    border-right: none;
    &:hover,
    &:focus {
      border-bottom: 2px solid #2f54eb;
    }
    &:focus {
      box-shadow: 0 2px 2px -2px #1f78d133;
    }
  }
  .ant-input-suffix {
    color: #2f54eb;
    cursor: pointer;
  }
}
.cmdb-search-form {
  .ant-form-item-label {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>

<style lang="less" scoped>
@import '~@/style/static.less';

.search-form-bar {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .search-form-bar-filter {
    .ops_display_wrapper();
    .search-form-bar-filter-icon {
      color: #custom_colors[color_1];
      font-size: 12px;
    }
  }
}
</style>
