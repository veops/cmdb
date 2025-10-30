<template>
  <div class="operation-history-table">
    <search-form
      :attrList="typeTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
      @export="handleExport"
    ></search-form>
    <vxe-table
      ref="xTable"
      :loading="loading"
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightMinus}px`"
      row-id="_XID"
      size="small"
      :row-config="{ isHover: true }"
      stripe
      class="ops-stripe-table"
    >
      <vxe-column field="created_at" width="165" :title="$t('cmdb.history.opreateTime')"></vxe-column>
      <vxe-column field="user" width="120" :title="$t('cmdb.history.user')"></vxe-column>
      <vxe-column field="operate_type" width="140" :title="$t('operation')">
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
                  v-for="(choice, index) in typeTableAttrList[1].choice_value"
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
      <vxe-column field="type_id" :title="$t('cmdb.ciType.ciType')" width="150">
        <template #default="{ row }">
          {{ row.operate_type === $t('cmdb.history.deleteCIType') ? row.change.alias : row.type_id }}
        </template>
      </vxe-column>
      <vxe-column field="changeDescription" :title="$t('desc')" min-width="200">
        <template #default="{ row }">
          <div v-if="row.changeDescription === $t('cmdb.history.noUpdate')" class="change-text">
            {{ row.changeDescription }}
          </div>
          <template v-else-if="row.operate_type.includes($t('update'))">
            <div :key="index" class="change-text update-text" v-for="(tag, index) in row.changeArr">
              {{ tag }}
            </div>
          </template>
          <div class="change-text new-text" v-else-if="row.operate_type.includes($t('new'))">
            {{ row.changeDescription }}
          </div>
          <div class="change-text delete-text" v-else-if="row.operate_type.includes($t('delete'))">
            {{ row.changeDescription }}
          </div>
        </template>
      </vxe-column>
    </vxe-table>
    <a-row class="row" type="flex" justify="end">
      <a-col>
        <a-pagination
          size="small"
          v-model="current"
          :page-size-options="pageSizeOptions"
          :total="numfound"
          show-size-changer
          :page-size="pageSize"
          @change="onChange"
          @showSizeChange="onShowSizeChange"
          :show-total="(total) => $t('cmdb.history.totalItems', { total: total })"
        >
        </a-pagination>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SearchForm from './searchForm'
import OperateTypeTag from '../components/OperateTypeTag.vue'
import { getCITypesTable, getUsers } from '@/modules/cmdb/api/history'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
import { deepCompare } from '@/modules/cmdb/utils/objectDiff'
import { PAGINATION_CONFIG } from '../constants'
import commonMixin from '../mixins/commonMixin'

export default {
  name: 'TypeTable',
  components: { SearchForm, OperateTypeTag },
  mixins: [commonMixin],
  inject: ['reload'],
  data() {
    return {
      loading: true,
      relationTypeList: null,
      typeList: null,
      userList: [],
      pageSizeOptions: PAGINATION_CONFIG.PAGE_SIZE_OPTIONS.map(String),
      isExpand: false,
      current: 1,
      pageSize: 50,
      total: 0,
      numfound: 0,
      tableData: [],
      queryParams: {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        type_id: undefined,
        operate_type: undefined,
      },
      ciTypeChoices: [],
    }
  },
  async created() {
    await Promise.all([this.getRelationTypes(), this.getTypes(), this.getUserList()])
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
      return this.isExpand ? 446 : 381
    },
    operateTypeMap() {
      return new Map([
        ['0', this.$t('cmdb.history.addCIType')],
        ['1', this.$t('cmdb.history.updateCIType')],
        ['2', this.$t('cmdb.history.deleteCIType')],
        ['3', this.$t('cmdb.history.addAttribute')],
        ['4', this.$t('cmdb.history.updateAttribute')],
        ['5', this.$t('cmdb.history.deleteAttribute')],
        ['6', this.$t('cmdb.history.addTrigger')],
        ['7', this.$t('cmdb.history.updateTrigger')],
        ['8', this.$t('cmdb.history.deleteTrigger')],
        ['9', this.$t('cmdb.history.addUniqueConstraint')],
        ['10', this.$t('cmdb.history.updateUniqueConstraint')],
        ['11', this.$t('cmdb.history.deleteUniqueConstraint')],
        ['12', this.$t('cmdb.history.addRelation')],
        ['13', this.$t('cmdb.history.deleteRelation')],
        ['14', this.$t('cmdb.history.addReconciliation')],
        ['15', this.$t('cmdb.history.updateReconciliation')],
        ['16', this.$t('cmdb.history.deleteReconciliation')],
      ])
    },
    typeTableAttrList() {
      return [
        {
          alias: this.$t('cmdb.ciType.ciType'),
          is_choice: true,
          name: 'type_id',
          value_type: '2',
          choice_value: this.ciTypeChoices,
        },
        {
          alias: this.$t('operation'),
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { [this.$t('cmdb.history.addCIType')]: 0 },
            { [this.$t('cmdb.history.updateCIType')]: 1 },
            { [this.$t('cmdb.history.deleteCIType')]: 2 },
            { [this.$t('cmdb.history.addAttribute')]: 3 },
            { [this.$t('cmdb.history.updateAttribute')]: 4 },
            { [this.$t('cmdb.history.deleteAttribute')]: 5 },
            { [this.$t('cmdb.history.addTrigger')]: 6 },
            { [this.$t('cmdb.history.updateTrigger')]: 7 },
            { [this.$t('cmdb.history.deleteTrigger')]: 8 },
            { [this.$t('cmdb.history.addUniqueConstraint')]: 9 },
            { [this.$t('cmdb.history.updateUniqueConstraint')]: 10 },
            { [this.$t('cmdb.history.deleteUniqueConstraint')]: 11 },
            { [this.$t('cmdb.history.addRelation')]: 12 },
            { [this.$t('cmdb.history.deleteRelation')]: 13 },
            { [this.$t('cmdb.history.addReconciliation')]: 14 },
            { [this.$t('cmdb.history.updateReconciliation')]: 15 },
            { [this.$t('cmdb.history.deleteReconciliation')]: 16 },
          ],
        },
      ]
    },
  },
  watch: {
    current(val) {
      this.queryParams.page = val
    },
    pageSize(val) {
      this.queryParams.page_size = val
    },
    locale() {
      this.reload()
    },
  },
  methods: {
    async getTable(queryParams) {
      try {
        this.loading = true
        const res = await getCITypesTable(queryParams)
        res.result.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type)
          item.operate_type = this.handleOperateType(item.operate_type)
          item.type_id = this.handleTypeId(item.type_id)
          item.uid = this.handleUID(item.uid)
        })
        this.tableData = res.result
        this.pageSize = res.page_size
        this.current = res.page
        this.numfound = res.numfound
        this.total = res.total
      } finally {
        this.loading = false
      }
    },
    async getTypes() {
      try {
        const res = await getCITypes()
        const typesArr = []
        const typesMap = new Map()
        res.ci_types.forEach((item) => {
          if (item.alias) {
            typesMap.set(item.id, item.alias)
            typesArr.push({ [item.alias]: item.id })
          }
        })
        this.typeList = typesMap
        this.ciTypeChoices = typesArr
      } catch (error) {
        this.handleError(error, 'fetch CI types')
      }
    },
    async getUserList() {
      try {
        const res = await getUsers()
        const userListMap = new Map()
        res.forEach((item) => {
          userListMap.set(item.uid, item.nickname)
        })
        this.userList = userListMap
      } catch (error) {
        this.handleError(error, 'fetch users')
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
    onChange(current) {
      this.current = current
      this.getTable(this.queryParams)
    },
    onShowSizeChange(current, size) {
      this.current = 1
      this.pageSize = size
      this.getTable(this.queryParams)
    },
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    handleSearch(queryParams) {
      this.current = 1
      this.queryParams = queryParams
      this.getTable(this.queryParams)
    },
    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        type_id: undefined,
        operate_type: undefined,
      }
      this.getTable(this.queryParams)
    },
    handleOperateType(operate_type) {
      return this.operateTypeMap.get(operate_type)
    },
    handleTypeId(type_id) {
      return this.typeList.get(type_id) ? this.typeList.get(type_id) : type_id
    },
    handleUID(uid) {
      return this.userList.get(uid)
    },
    handleRelationType(relation_type_id) {
      return this.relationTypeList.get(relation_type_id)
    },
    handleChangeDescription(item, operate_type) {
      switch (operate_type) {
        // add CIType
        case '0': {
          item.changeDescription = this.$t('cmdb.history.addCIType') + ': ' + item.change.alias
          break
        }
        // update CIType
        case '1': {
          item.changeArr = []
          const diffs = this.deepCompare({
            obj1: item?.change?.old,
            obj2: item?.change?.new,
            ignoreKeys: ['updated_at']
          })
          for (const val of diffs) {
            const str = ` [ ${val.path} :  ${val.value1} -> ${val.value2} ] `
            item.changeDescription += str
            item.changeArr.push(str)
          }
          if (!item.changeDescription) item.changeDescription = this.$t('cmdb.history.noModifications')
          break
        }
        // delete CIType
        case '2': {
          item.changeDescription = this.$t('cmdb.history.deleteCIType') + ': ' + `${item.change.alias}`
          break
        }
        // add Attribute
        case '3': {
          item.changeDescription = `${this.$t('cmdb.history.attr')}：${item.change.alias}`
          break
        }
        // update Attribute
        case '4': {
          item.changeArr = []
          const diffs = this.deepCompare({
            obj1: item?.change?.old,
            obj2: item?.change?.new,
            ignoreKeys: ['updated_at']
          })
          for (const val of diffs) {
            const str = ` [ ${val.path} :  ${val.value1} -> ${val.value2} ] `
            item.changeDescription += str
            item.changeArr.push(str)
          }
          if (!item.changeDescription) item.changeDescription = this.$t('cmdb.history.noModifications')
          break
        }
        // delete Attribute
        case '5': {
          item.changeDescription = `${this.$t('delete')}：${item.change.alias}`
          break
        }
        // add trigger
        case '6': {
          item.changeDescription = `${this.$t('cmdb.history.addTrigger')}：${item?.change?.option?.name || ''}`
          break
        }
        // update trigger
        case '7': {
          item.changeArr = []
          const diffs = this.deepCompare({
            obj1: item?.change?.old,
            obj2: item?.change?.new,
            directDeepKeys: ['notifies'],
            ignoreKeys: ['updated_at']
          })
          for (const val of diffs) {
            const str = ` [ ${val.path} :  ${val.value1} -> ${val.value2} ] `
            item.changeDescription += str
            item.changeArr.push(str)
          }
          if (!item.changeDescription) item.changeDescription = this.$t('cmdb.history.noModifications')
          break
        }
        // delete trigger
        case '8': {
          item.changeDescription = `${this.$t('cmdb.history.deleteTrigger')}：${item?.change?.option?.name || ''}`
          break
        }
        // add unique constraint
        case '9': {
          item.changeDescription = `${this.$t('cmdb.history.attrId')}：[${item.change.attr_ids}]`
          break
        }
        // update unique constraint
        case '10': {
          item.changeArr = []
          const oldVal = item.change.old.attr_ids
          const newVal = item.change.new.attr_ids
          const str = `${this.$t('cmdb.history.attrId')}：[${oldVal}] -> [${newVal}]`
          item.changeDescription = str
          item.changeArr.push(str)
          break
        }
        // delete unique constraint
        case '11': {
          item.changeDescription = `${this.$t('cmdb.history.attrId')}：[${item.change.attr_ids}]`
          break
        }
        // add relation
        case '12': {
          item.changeDescription = `${this.$t('new')}：${item.change.parent.alias} -> ${this.handleRelationType(
            item.change.relation_type_id
          )} -> ${item.change.child.alias}`
          break
        }
        // delete relation
        case '13': {
          item.changeDescription = `${this.$t('delete')}：${item.change.parent_id.alias} -> ${this.handleRelationType(
            item.change.relation_type_id
          )} -> ${item.change.child.alias}`
          break
        }
        case '14': {
          item.changeDescription = this.$t('cmdb.history.addReconciliation') + ': ' + item.change.name || item.change.alias
          break
        }
        case '15': {
          item.changeArr = []
          const diffs = this.deepCompare({
            obj1: item?.change?.old,
            obj2: item?.change?.new,
            directDeepKeys: ['notifies'],
            ignoreKeys: ['updated_at']
          })
          for (const val of diffs) {
            const str = ` [ ${val.path} :  ${val.value1} -> ${val.value2} ] `
            item.changeDescription += str
            item.changeArr.push(str)
          }
          if (!item.changeDescription) item.changeDescription = this.$t('cmdb.history.updateReconciliation')
          break
        }
        case '16': {
          item.changeDescription = this.$t('cmdb.history.deleteReconciliation') + ': ' + item.change.name || item.change.alias
          break
        }
      }
    },

    deepCompare(options) {
      return deepCompare(options)
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
        const res = await getCITypesTable({
          ...params,
          page: this.queryParams.page,
          page_size: this.queryParams.page_size,
        })
        hide()

        if (!res.result || res.result.length === 0) {
          this.$message.warning(this.$t('noData'))
          return
        }

        res.result.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type)
          item.operate_type = this.handleOperateType(item.operate_type)
          item.type_id = this.handleTypeId(item.type_id)
          item.uid = this.handleUID(item.uid)
          if (item.operate_type.includes(this.$t('update'))) {
            item.changeDescription = item.changeArr.join(';')
          }
        })

        await this.$refs.xTable.exportData({
          filename: `${this.$t('cmdb.history.ciTypeChange')}_${new Date().toISOString().split('T')[0]}`,
          sheetName: 'Sheet1',
          type: 'xlsx',
          types: ['xlsx'],
          isMerge: true,
          isColgroup: true,
          data: res.result,
        })

        this.$message.success(this.$t('exportSuccess'))
      } catch (error) {
        hide()
        this.handleError(error, 'export')
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '../styles/table.less';

.row {
  margin-top: 5px;
}
</style>
