<template>
  <div>
    <search-form
      :attrList="relationTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
    ></search-form>
    <vxe-table
      ref="xTable"
      :loading="loading"
      size="small"
      show-overflow="tooltip"
      show-header-overflow="tooltip"
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightMinus}px`"
      row-id="_XID"
      :scroll-y="{ enabled: false }"
      :span-method="mergeRowMethod"
      stripe
      class="ops-stripe-table"
    >
      <vxe-column field="created_at" width="159px" :title="$t('cmdb.history.opreateTime')"></vxe-column>
      <vxe-column field="user" width="100px" :title="$t('cmdb.history.user')">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon class="filter" type="filter" theme="filled" />
            <a slot="content">
              <a-input
                :placeholder="$t('cmdb.history.userTips')"
                size="small"
                v-model="queryParams.username"
                style="width: 200px"
                allowClear
              />
              <a-button type="link" class="filterButton" @click="filterUser">{{ $t('cmdb.history.filter') }}</a-button>
              <a-button type="link" class="filterResetButton" @click="filterUserReset">{{ $t('reset') }}</a-button>
            </a>
          </a-popover>
        </template>
      </vxe-column>
      <vxe-column field="operate_type" width="89px" :title="$t('operation')">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon class="filter" type="filter" theme="filled" />
            <a slot="content">
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
              <a-button type="link" class="filterButton" @click="filterOperate">{{
                $t('cmdb.history.filter')
              }}</a-button>
              <a-button type="link" class="filterResetButton" @click="filterOperateReset">{{ $t('reset') }}</a-button>
            </a>
          </a-popover>
        </template>
        <template #default="{ row }">
          <a-tag color="green" v-if="row.operate_type.includes($t('new'))">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="orange" v-else-if="row.operate_type.includes($t('update'))">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="red" v-else>
            {{ row.operate_type }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="changeDescription" :title="$t('desc')">
        <template #default="{ row }">
          <a-tag v-if="row && row.first">
            {{
              `${row.first.ci_type_alias}${
                row.first.unique_alias && row.first[row.first.unique]
                  ? `（${row.first.unique_alias}：${row.first[row.first.unique]}）`
                  : ''
              }`
            }}
          </a-tag>
          <a-tag v-if="row.changeDescription === $t('cmdb.history.noUpdate')">
            {{ row.relation_type_id }}
          </a-tag>
          <template v-else-if="row.operate_type.includes($t('update'))">
            <a-tag :key="index" color="orange" v-for="(tag, index) in row.changeArr">
              {{ tag }}
            </a-tag>
          </template>
          <a-tag color="green" v-else-if="row.operate_type.includes($t('new'))" :style="{ fontWeight: 'bolder' }">
            {{ row.relation_type_id }}
          </a-tag>
          <a-tag color="red" v-else-if="row.operate_type.includes($t('delete'))">
            {{ row.relation_type_id }}
          </a-tag>
          <a-tag v-if="row && row.second">
            {{
              `${row.second.ci_type_alias}${
                row.second.unique_alias && row.second[row.second.unique]
                  ? `（${row.second.unique_alias}：${row.second[row.second.unique]}）`
                  : ''
              }`
            }}
          </a-tag>
        </template>
      </vxe-column>
    </vxe-table>
    <pager
      :current-page.sync="queryParams.page"
      :page-size.sync="queryParams.page_size"
      :page-sizes="[50, 100, 200]"
      :total="total"
      :isLoading="loading"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
    ></pager>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SearchForm from './searchForm'
import Pager from './pager.vue'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getRelationTable, getUsers } from '@/modules/cmdb/api/history'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
export default {
  name: 'RelationTable',
  components: { SearchForm, Pager },
  inject: ['reload'],
  data() {
    return {
      visible: false,
      loading: true,
      isExpand: false,
      tableData: [],
      relationTypeList: null,
      total: 0,
      userList: [],
      queryParams: {
        page: 1,
        page_size: 50,
        start: '',
        end: '',
        username: '',
        first_ci_id: undefined,
        second_ci_id: undefined,
        operate_type: undefined,
      },
      relationTableAttrList: [
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
          choice_value: [],
        },
        {
          alias: 'FirstCI_ID',
          is_choice: false,
          name: 'first_ci_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: 'SecondCI_ID',
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
          choice_value: [{ [this.$t('new')]: 0 }, { [this.$t('delete')]: 1 }, { [this.$t('update')]: 2 }],
        },
      ],
    }
  },
  async created() {
    await Promise.all([this.getRelationTypes(), this.getUserList(), this.getTypes()])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  computed: {
    ...mapState(['locale']),
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowHeightMinus() {
      return this.isExpand ? 396 : 331
    },
    operateTypeMap() {
      return new Map([
        ['0', this.$t('new')],
        ['1', this.$t('delete')],
        ['2', this.$t('update')],
      ])
    },
  },
  watch: {
    locale() {
      this.reload()
    },
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
      } finally {
        this.loading = false
      }
    },
    async getUserList() {
      const res = await getUsers()
      this.userList = res.map((x) => {
        const username = x.nickname
        const obj = {
          [username]: username,
        }
        return obj
      })
      this.relationTableAttrList[1].choice_value = this.userList
    },
    async getTypes() {
      const res = await getCITypes()
      const typesArr = []
      res.ci_types.forEach((item) => {
        const tempObj = {}
        tempObj[item.alias] = item.id
        if (item.alias) {
          typesArr.push(tempObj)
        }
      })
      this.relationTableAttrList[2].choice_value = typesArr
      this.relationTableAttrList[3].choice_value = typesArr
    },
    async getRelationTypes() {
      const res = await getRelationTypes()
      const relationTypeMap = new Map()
      res.forEach((item) => {
        relationTypeMap.set(item.id, item.name)
      })
      this.relationTypeList = relationTypeMap
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
        page_size: 50,
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
      const cellValue = row[column.property]
      const created_at = row['created_at']
      if (column.property === 'created_at') {
        if (cellValue && fields.includes(column.property)) {
          const prevRow = visibleData[_rowIndex - 1]
          let nextRow = visibleData[_rowIndex + 1]
          if (prevRow && prevRow[column.property] === cellValue) {
            return { rowspan: 0, colspan: 0 }
          } else {
            let countRowspan = 1
            while (nextRow && nextRow[column.property] === cellValue) {
              nextRow = visibleData[++countRowspan + _rowIndex]
            }
            if (countRowspan > 1) {
              return { rowspan: countRowspan, colspan: 1 }
            }
          }
        }
      } else if (column.property === 'user') {
        if (cellValue && fields.includes(column.property)) {
          const prevRow = visibleData[_rowIndex - 1]
          let nextRow = visibleData[_rowIndex + 1]
          if (prevRow && prevRow[column.property] === cellValue && prevRow['created_at'] === created_at) {
            return { rowspan: 0, colspan: 0 }
          } else {
            let countRowspan = 1
            while (nextRow && nextRow[column.property] === cellValue && nextRow['created_at'] === created_at) {
              nextRow = visibleData[++countRowspan + _rowIndex]
            }
            if (countRowspan > 1) {
              return { rowspan: countRowspan, colspan: 1 }
            }
          }
        }
      }
    },
    filterUser() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.getTable(this.queryParams)
    },
    filterUserReset() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.queryParams.username = ''
      this.getTable(this.queryParams)
    },
    filterOperate() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.getTable(this.queryParams)
    },
    filterOperateReset() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.queryParams.operate_type = undefined
      this.getTable(this.queryParams)
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.indexOf(input) >= 0
    },
  },
}
</script>

<style lang="less" scoped>
.filter {
  margin-left: 10px;
  color: #c0c4cc;
  cursor: pointer;
  &:hover {
    color: #606266;
  }
}
</style>
