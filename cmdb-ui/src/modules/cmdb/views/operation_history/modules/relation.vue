<template>
  <div class="operation-history-table">
    <search-form
      :attrList="relationTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
      @export="handleExport"
    ></search-form>
    <vxe-table
      ref="xTable"
      :loading="loading"
      size="small"
      show-overflow="tooltip"
      show-header-overflow="tooltip"
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightOffset}px`"
      row-id="_XID"
      :scroll-y="{ enabled: false }"
      :span-method="mergeRowMethod"
      stripe
      class="ops-stripe-table"
    >
      <vxe-column field="created_at" width="165" :title="$t('cmdb.history.opreateTime')"></vxe-column>
      <vxe-column field="user" width="120" :title="$t('cmdb.history.user')">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon
              class="filter"
              :class="{ active: queryParams.username }"
              type="filter"
              theme="filled"
            />
            <div class="filter-content" slot="content">
              <a-input
                :placeholder="$t('cmdb.history.userTips')"
                size="small"
                v-model="queryParams.username"
                style="width: 200px"
                allowClear
              />
              <a-button type="link" class="filterButton" @click="filterUser">
                {{ $t('cmdb.history.filter') }}
              </a-button>
              <a-button type="link" class="filterResetButton" @click="filterUserReset">
                {{ $t('reset') }}
              </a-button>
            </div>
          </a-popover>
        </template>
      </vxe-column>
      <vxe-column field="operate_type" width="90" :title="$t('operation')">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon
              class="filter"
              :class="{ active: queryParams.operate_type !== undefined }"
              type="filter"
              theme="filled"
            />
            <div class="filter-content" slot="content">
              <a-select
                v-model="queryParams.operate_type"
                :placeholder="$t('cmdb.history.filterOperate')"
                show-search
                style="width: 200px"
                :filter-option="filterOption"
                allowClear
              >
                <a-select-option
                  :value="Object.values(choice)[0]"
                  :key="index"
                  v-for="(choice, index) in relationTableAttrList[4].choice_value"
                >
                  {{ Object.keys(choice)[0] }}
                </a-select-option>
              </a-select>
              <a-button type="link" class="filterButton" @click="filterOperate">
                {{ $t('cmdb.history.filter') }}
              </a-button>
              <a-button type="link" class="filterResetButton" @click="filterOperateReset">
                {{ $t('reset') }}
              </a-button>
            </div>
          </a-popover>
        </template>
        <template #default="{ row }">
          <operate-type-tag :operate-type="row.operate_type" />
        </template>
      </vxe-column>
      <vxe-column field="changeDescription" min-width="200" :title="$t('desc')">
        <template #default="{ row }">
          <div class="relation-description">
            <span v-if="row && row.first" class="ci-info source-ci">
              <span class="ci-type">{{ row.first.ci_type_alias }}</span>
              <span v-if="row.first.unique_alias && row.first[row.first.unique]" class="ci-detail">
                {{ row.first.unique_alias }}: {{ row.first[row.first.unique] }}
              </span>
            </span>

            <span class="relation-arrow">
              <a-icon type="arrow-right" />
            </span>

            <span class="relation-type">
              <a-tag v-if="row.changeDescription === $t('cmdb.history.noUpdate')" color="default">
                {{ row.relation_type_id }}
              </a-tag>
              <template v-else-if="row.operate_type.includes($t('update'))">
                <a-tag :key="index" color="orange" v-for="(tag, index) in row.changeArr">
                  {{ tag }}
                </a-tag>
              </template>
              <a-tag v-else-if="row.operate_type.includes($t('new'))" color="green">
                {{ row.relation_type_id }}
              </a-tag>
              <a-tag v-else-if="row.operate_type.includes($t('delete'))" color="red">
                {{ row.relation_type_id }}
              </a-tag>
            </span>

            <span class="relation-arrow">
              <a-icon type="arrow-right" />
            </span>

            <span v-if="row && row.second" class="ci-info target-ci">
              <span class="ci-type">{{ row.second.ci_type_alias }}</span>
              <span v-if="row.second.unique_alias && row.second[row.second.unique]" class="ci-detail">
                {{ row.second.unique_alias }}: {{ row.second[row.second.unique] }}
              </span>
            </span>
          </div>
        </template>
      </vxe-column>
    </vxe-table>
    <pager
      :current-page.sync="queryParams.page"
      :page-size.sync="queryParams.page_size"
      :page-sizes="PAGE_SIZE_OPTIONS"
      :total="total"
      :isLoading="loading"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
    ></pager>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import SearchForm from './searchForm'
import Pager from '@/components/Pager'
import OperateTypeTag from '../components/OperateTypeTag.vue'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getRelationTable, getUsers } from '@/modules/cmdb/api/history'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import commonMixin from '../mixins/commonMixin'
import { PAGINATION_CONFIG } from '../constants'

export default {
  name: 'RelationTable',
  components: { SearchForm, Pager, OperateTypeTag },
  mixins: [commonMixin],
  inject: ['reload'],
  data() {
    return {
      loading: true,
      isExpand: false,
      tableData: [],
      relationTypeList: null,
      total: 0,
      userList: [],
      queryParams: {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        start: '',
        end: '',
        username: '',
        first_ci_id: undefined,
        second_ci_id: undefined,
        operate_type: undefined,
      },
      PAGE_SIZE_OPTIONS: PAGINATION_CONFIG.PAGE_SIZE_OPTIONS
    }
  },
  computed: {
    ...mapState(['locale']),
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowHeightOffset() {
      return this.isExpand ? 446 : 381
    },
    operateTypeMap() {
      return new Map([
        ['0', this.$t('new')],
        ['1', this.$t('delete')],
        ['2', this.$t('update')],
      ])
    },
    relationTableAttrList() {
      return [
        {
          alias: this.$t('cmdb.ciType.date'),
          is_choice: false,
          name: 'datetime',
          value_type: '3',
        },
        {
          alias: this.$t('cmdb.history.user'),
          is_choice: true,
          name: 'username',
          value_type: '2',
          choice_value: this.userList,
        },
        {
          alias: this.$t('cmdb.history.sourceCI'),
          is_choice: false,
          name: 'first_ci_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('cmdb.history.targetCI'),
          is_choice: false,
          name: 'second_ci_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('operation'),
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { [this.$t('new')]: 0 },
            { [this.$t('delete')]: 1 },
            { [this.$t('update')]: 2 }
          ],
        },
      ]
    }
  },
  watch: {
    locale() {
      this.reload()
    },
  },
  async created() {
    await Promise.all([this.getRelationTypes(), this.getUserList(), this.getTypes()])
    await this.getTable(this.queryParams)
  },
  updated() {
    if (this.$refs.xTable && this.$refs.xTable.$el) {
      const wrapper = this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper')
      if (wrapper) {
        wrapper.scrollTop = 0
      }
    }
  },
  methods: {
    async getTable(queryParams) {
      try {
        this.loading = true
        const res = await getRelationTable(queryParams)
        const tempArr = []
        res.records.forEach((item) => {
          item[1].forEach((subItem) => {
            subItem.operate_type = this.handleOperateType(subItem.operate_type)
            subItem.relation_type_id = this.handleRelationType(subItem.relation_type_id)
            subItem.first = res.cis[String(subItem.first_ci_id)]
            subItem.second = res.cis[String(subItem.second_ci_id)]
            const tempObj = Object.assign(subItem, item[0])
            tempArr.push(tempObj)
          })
        })
        this.total = res.total
        this.tableData = tempArr
      } catch (error) {
        this.handleError(error, 'fetch data')
      } finally {
        this.loading = false
      }
    },

    async getUserList() {
      try {
        const res = await getUsers()
        const userList = _.uniqBy((res || []), 'nickname')
        this.userList = userList.map((x) => {
          const username = x.nickname
          return {
            [username]: username,
          }
        })
      } catch (error) {
        this.handleError(error, 'fetch users')
      }
    },

    async getTypes() {
      try {
        const res = await getCITypes()
        const typesArr = []
        res.ci_types.forEach((item) => {
          if (item.alias) {
            typesArr.push({ [item.alias]: item.id })
          }
        })
      } catch (error) {
        this.handleError(error, 'fetch CI types')
      }
    },

    async getRelationTypes() {
      try {
        const res = await getRelationTypes()
        const relationTypeMap = new Map()
        res.forEach((item) => {
          relationTypeMap.set(item.id, item.name)
        })
        this.relationTypeList = relationTypeMap
      } catch (error) {
        this.handleError(error, 'fetch relation types')
      }
    },

    onShowSizeChange(size) {
      this.queryParams.page_size = size
      this.queryParams.page = 1
      this.getTable(this.queryParams)
    },

    onChange(pageNum) {
      this.queryParams.page = pageNum
      this.getTable(this.queryParams)
    },

    handleExpandChange(expand) {
      this.isExpand = expand
    },

    handleSearch(queryParams) {
      this.queryParams = queryParams
      this.getTable(queryParams)
    },

    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        start: '',
        end: '',
        username: '',
        first_ci_id: undefined,
        second_ci_id: undefined,
        operate_type: undefined,
      }
      this.getTable(this.queryParams)
    },

    handleOperateType(operate_type) {
      return this.operateTypeMap.get(operate_type)
    },

    handleRelationType(relation_type_id) {
      return this.relationTypeList.get(relation_type_id)
    },

    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['created_at', 'user']
      return this.createMergeRowMethod(fields)({ row, _rowIndex, column, visibleData })
    },

    filterUser() {
      this.applyFilter()
    },

    filterUserReset() {
      this.applyFilter({ username: '' })
    },

    filterOperate() {
      this.applyFilter()
    },

    filterOperateReset() {
      this.applyFilter({ operate_type: undefined })
    },

    filterOption(input, option) {
      return option.componentOptions.children[0].text.indexOf(input) >= 0
    },

    async handleExport(params) {
      const hide = this.$message.loading(this.$t('loading'), 0)
      try {
        const res = await getRelationTable({
          ...params,
          page: this.queryParams.page,
          page_size: this.queryParams.page_size,
        })
        hide()

        if (!res.records || res.records.length === 0) {
          this.$message.warning(this.$t('noData'))
          return
        }

        const data = []
        res.records.forEach((item) => {
          item[1].forEach((subItem) => {
            subItem.operate_type = this.handleOperateType(subItem.operate_type)
            subItem.relation_type_id = this.handleRelationType(subItem.relation_type_id)
            subItem.first = res.cis[String(subItem.first_ci_id)]
            subItem.second = res.cis[String(subItem.second_ci_id)]

            const tempObj = Object.assign(subItem, item[0])

            tempObj.changeDescription = this.getExportChangeDescription(tempObj)

            data.push(tempObj)
          })
        })

        await this.$refs.xTable.exportData({
          filename: `${this.$t('cmdb.history.relationChange')}_${new Date().toISOString().split('T')[0]}`,
          sheetName: 'Sheet1',
          type: 'xlsx',
          types: ['xlsx'],
          isMerge: true,
          isColgroup: true,
          data,
        })

        this.$message.success(this.$t('exportSuccess'))
      } catch (error) {
        hide()
        this.handleError(error, 'export')
      }
    },

    getExportChangeDescription(item) {
      const first = item.first ? `${item.first.ci_type_alias}${item.first.unique_alias && item.first[item.first.unique] ? `（${item.first.unique_alias}：${item.first[item.first.unique]}）` : ''}` : ''
      const second = item.second ? `${item.second.ci_type_alias}${item.second.unique_alias && item.second[item.second.unique] ? `（${item.second.unique_alias}：${item.second[item.second.unique]}）` : ''}` : ''
      let center = ''
      if (item.changeDescription === this.$t('cmdb.history.noUpdate')) {
        center = item.relation_type_id
      } else if (item.operate_type.includes(this.$t('update'))) {
        center = item.changeArr.join(';')
      } else if (item.operate_type.includes(this.$t('new'))) {
        center = item.relation_type_id
      } else if (item.operate_type.includes(this.$t('delete'))) {
        center = item.relation_type_id
      }

      return `${first || ''} => ${center || ''} => ${second || ''}`
    }
  },
}
</script>

<style lang="less" scoped>
@import '../styles/table.less';

.relation-description {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  line-height: 22px;

  .ci-info {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: #f5f5f5;
    border-radius: 2px;
    border: 1px solid #d9d9d9;
    font-size: 13px;

    .ci-type {
      color: rgba(0, 0, 0, 0.85);
      font-weight: 600;
    }

    .ci-detail {
      color: rgba(0, 0, 0, 0.65);
      font-size: 12px;

      &:before {
        content: '(';
        margin-right: 2px;
      }

      &:after {
        content: ')';
        margin-left: 2px;
      }
    }

    &.source-ci {
      border-left: 3px solid @primary-color;
    }

    &.target-ci {
      border-left: 3px solid #52c41a;
    }
  }

  .relation-arrow {
    color: #8c8c8c;
    font-size: 14px;
    margin: 0 4px;
  }

  .relation-type {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
  }
}
</style>
