<template>
  <div class="operation-history-table">
    <search-form
      ref="child"
      :attrList="ciTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
      @searchFormChange="searchFormChange"
      @export="handleExport"
    ></search-form>
    <vxe-table
      ref="xTable"
      row-id="_XID"
      :loading="loading"
      border
      size="small"
      show-overflow="tooltip"
      show-header-overflow="tooltip"
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightOffset}px`"
      :span-method="mergeRowMethod"
      :scroll-y="{ enabled: false }"
      class="ops-unstripe-table"
    >
      <vxe-column field="created_at" min-width="160" :title="$t('cmdb.history.opreateTime')"></vxe-column>
      <vxe-column field="user" min-width="120" :title="$t('cmdb.history.user')">
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
      <vxe-column field="type_id" min-width="120" :title="$t('cmdb.ciType.ciType')"></vxe-column>
      <vxe-column field="show_attr_value" min-width="120" :title="$t('cmdb.ci.instance')"></vxe-column>
      <vxe-column field="operate_type" min-width="100" :title="$t('operation')">
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
                  v-for="(choice, index) in ciTableAttrList[4].choice_value"
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
      <vxe-column field="attr_alias" min-width="120" :title="$t('cmdb.history.attribute')"></vxe-column>
      <vxe-column :cell-type="'string'" field="old" min-width="200" :title="$t('cmdb.history.old')"></vxe-column>
      <vxe-column :cell-type="'string'" field="new" min-width="200" :title="$t('cmdb.history.new')"></vxe-column>
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
import Pager from '@/components/Pager'
import SearchForm from './searchForm.vue'
import OperateTypeTag from '../components/OperateTypeTag.vue'
import { getCIHistoryTable, getUsers } from '@/modules/cmdb/api/history'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import commonMixin from '../mixins/commonMixin'
import { PAGINATION_CONFIG } from '../constants'

export default {
  name: 'CiTable',
  components: { SearchForm, Pager, OperateTypeTag },
  mixins: [commonMixin],
  inject: ['reload'],
  data() {
    return {
      typeId: undefined,
      loading: true,
      typeList: null,
      userList: [],
      attrList: [],
      tableData: [],
      total: 0,
      isExpand: false,
      queryParams: {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
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
    ciTableAttrList() {
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
          alias: this.$t('cmdb.ciType.ciType'),
          is_choice: true,
          name: 'type_id',
          value_type: '2',
          choice_value: this.ciTypeChoices,
        },
        {
          alias: this.$t('cmdb.history.attribute'),
          is_choice: true,
          name: 'attr_id',
          value_type: '2',
          choice_value: this.attrChoices,
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
        {
          alias: 'CI ID',
          is_choice: false,
          name: 'ci_id',
          value_type: '2',
        },
      ]
    },
    ciTypeChoices() {
      if (!this.typeList) return []
      const choices = []
      this.typeList.forEach((alias, id) => {
        choices.push({ [alias]: id })
      })
      return choices
    },
    attrChoices() {
      return this.attrList || []
    }
  },
  watch: {
    locale() {
      this.reload()
    },
  },
  async created() {
    this.attrList = []
    this.$watch(
      () => this.attrList,
      () => {
        if (this.$refs.child) {
          delete this.$refs.child.queryParams.attr_id
        }
      }
    )
    await Promise.all([this.getUserList(), this.getTypes()])
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
        const res = await getCIHistoryTable(queryParams)
        const tempArr = []
        res.records.forEach((item) => {
          item[0].type_id = this.handleTypeId(item[0].type_id)
          item[1].forEach((subItem) => {
            subItem.operate_type = this.handleOperateType(subItem.operate_type)
            const tempObj = Object.assign(subItem, item[0])
            tempArr.push(tempObj)
          })
        })
        this.tableData = tempArr
        this.total = res.total
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
        const typesMap = new Map()
        res.ci_types.forEach((item) => {
          if (item.alias) {
            typesMap.set(item.id, item.alias)
          }
        })
        this.typeList = typesMap
      } catch (error) {
        this.handleError(error, 'fetch CI types')
      }
    },

    async getAttrs(type_id) {
      if (!type_id) {
        this.attrList = []
        return
      }
      try {
        const res = await getCITypeAttributesById(type_id)
        const attrsArr = []
        res.attributes.forEach((item) => {
          if (item.alias) {
            attrsArr.push({ [item.alias]: item.id })
          }
        })
        this.attrList = attrsArr
      } catch (error) {
        this.handleError(error, 'fetch attributes')
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
      this.getTable(this.queryParams)
    },

    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        start: '',
        end: '',
        username: '',
        ci_id: undefined,
        attr_id: undefined,
        operate_type: undefined,
      }
      this.attrList = []
      this.getTable(this.queryParams)
    },

    handleOperateType(operate_type) {
      return this.operateTypeMap.get(operate_type)
    },

    handleTypeId(type_id) {
      return this.typeList.get(type_id) ? this.typeList.get(type_id) : type_id
    },

    searchFormChange(queryParams) {
      if (this.typeId !== queryParams.type_id) {
        this.typeId = queryParams.type_id
        this.getAttrs(queryParams.type_id)
      }
      if (queryParams.type_id === undefined) {
        this.typeId = undefined
        if (this.$refs.child) {
          this.$refs.child.queryParams.attr_id = undefined
        }
      }
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['created_at', 'user', 'type_id', 'show_attr_value']
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
        const res = await getCIHistoryTable({
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
          item[0].type_id = this.handleTypeId(item[0].type_id)
          item[1].forEach((subItem) => {
            subItem.operate_type = this.handleOperateType(subItem.operate_type)
            subItem.new = subItem.new || ''
            subItem.old = subItem.old || ''
            const tempObj = Object.assign(subItem, item[0])
            data.push(tempObj)
          })
        })

        await this.$refs.xTable.exportData({
          filename: `${this.$t('cmdb.history.ciChange')}_${new Date().toISOString().split('T')[0]}`,
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
    }
  },
}
</script>

<style lang="less" scoped>
@import '../styles/table.less';
</style>
