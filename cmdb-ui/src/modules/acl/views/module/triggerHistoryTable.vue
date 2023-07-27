<template>
  <div>
    <search-form
      ref="child"
      :attrList="triggerTableAttrList"
      @searchFormReset="searchFormReset"
      @search="handleSearch"
    ></search-form>
    <vxe-table
      ref="xTable"
      stripe
      class="ops-stripe-table"
      :data="tableData"
      :loading="loading"
      size="small"
      resizable
      :height="`${windowHeight - 310}px`"
    >
      <vxe-column field="created_at" width="144px" title="操作时间"></vxe-column>
      <vxe-column field="operate_uid" width="130px" title="操作员"></vxe-column>
      <vxe-column field="operate_type" width="80px" title="操作">
        <template #default="{ row }">
          <a-tag :color="handleTagColor(row.operate_type)">
            {{ operateTypeMap.get(row.operate_type) }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="trigger_id" width="250px" title="触发器">
        <template #default="{ row }">
          <span>
            {{ row.current.name || row.origin.name }}
          </span>
        </template>
      </vxe-column>
      <vxe-column title="描述">
        <template #default="{ row }">
          <p>
            {{ row.changeDescription }}
          </p>
        </template>
      </vxe-column>
    </vxe-table>
    <pager
      :current-page.sync="queryParams.page"
      :page-size.sync="queryParams.page_size"
      :page-sizes="[50, 100, 200]"
      :total="tableDataLength"
      :isLoading="loading"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
      :style="{ marginTop: '10px' }"
    ></pager>
  </div>
</template>

<script>
import _ from 'lodash'
import Pager from './pager.vue'
import SearchForm from './searchForm.vue'
import { searchTriggerHistory } from '@/modules/acl/api/history'
export default {
  components: { SearchForm, Pager },
  props: {
    allUsers: {
      type: Array,
      required: true,
    },
    allRoles: {
      type: Array,
      required: true,
    },
    allTriggers: {
      type: Array,
      required: true,
    },
    allRolesMap: {
      type: Map,
      required: true,
    },
    allTriggersMap: {
      type: Map,
      required: true,
    },
    allUsersMap: {
      type: Map,
      required: true,
    },
    allResourceTypesMap: {
      type: Map,
      required: true,
    },
  },
  data() {
    return {
      app_id: this.$route.name.split('_')[0],
      loading: true,
      tableData: [],
      operateTypeMap: new Map([
        ['create', '新建'],
        ['update', '修改'],
        ['delete', '删除'],
        ['trigger_apply', '应用'],
        ['trigger_cancel', '取消'],
      ]),
      colorMap: new Map([
        ['create', 'green'],
        ['delete', 'red'],
        ['update', 'orange'],
        ['trigger_apply', 'green'],
        ['trigger_cancel', 'red'],
      ]),
      triggerTableAttrList: [
        {
          alias: '日期',
          is_choice: false,
          name: 'datetime',
          value_type: '3',
        },
        {
          alias: '操作员',
          is_choice: true,
          name: 'operate_uid',
          value_type: '2',
          choice_value: this.allUsers,
        },
        {
          alias: '操作',
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { 新建: 'create' },
            { 修改: 'update' },
            { 删除: 'delete' },
            { 应用: 'trigger_apply' },
            { 取消: 'trigger_cancel' },
          ],
        },
        {
          alias: '触发器',
          is_choice: true,
          name: 'trigger_id',
          value_type: '2',
          choice_value: this.allTriggers,
        },
      ],
      queryParams: {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
      },
    }
  },
  async created() {
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  watch: {
    '$route.name': async function(oldName, newName) {
      this.app_id = this.$route.name.split('_')[0]
      await this.getTable(this.queryParams)
    },
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableDataLength() {
      return this.tableData.length
    },
  },
  methods: {
    async getTable(queryParams) {
      try {
        this.loading = true
        const res = await searchTriggerHistory(this.handleQueryParams(queryParams))
        res.data.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type)
          item.trigger_id = this.allTriggersMap.get(item.trigger_id)
          item.operate_uid = this.allUsersMap.get(item.operate_uid)
        })
        this.tableData = res.data
      } finally {
        this.loading = false
      }
    },

    // pager相关
    onShowSizeChange(size) {
      this.queryParams.page_size = size
      this.queryParams.page = 1
      this.getTable(this.queryParams)
    },
    onChange(pageNum) {
      this.queryParams.page = pageNum
      this.getTable(this.queryParams)
    },

    // searchForm相关
    handleSearch(queryParams) {
      this.queryParams = queryParams
      this.queryParams.app_id = this.app_id
      this.getTable(this.queryParams)
    },
    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
      }
      this.getTable(this.queryParams)
    },

    handleChangeDescription(item, operate_type) {
      switch (operate_type) {
        // create
        case 'create': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `新增触发器：${item.current.name}\n资源类型：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，资源名：${item.current.wildcard}，角色：[${newStr}]\n权限：${item.current.permissions}\n状态：${
            item.current.enabled
          }`
          break
        }
        case 'update': {
          item.changeDescription = ''
          for (const key in item.origin) {
            const newVal = item.current[key]
            const oldVal = item.origin[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at' && key !== 'deleted_at' && key !== 'created_at') {
              if (oldVal === null) {
                const str = ` 【 ${key} : 改为 ${newVal} 】 `
                item.changeDescription += str
              } else {
                const str = ` 【 ${key} : 由 ${oldVal} 改为 ${newVal} 】 `
                item.changeDescription += ` 【 ${key} : 由 ${oldVal} 改为 ${newVal} 】 `
              }
            }
          }
          if (!item.changeDescription) item.changeDescription = '没有修改'
          break
        }
        case 'delete': {
          const str = item.origin.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `删除触发器：${item.origin.name}\n资源类型：${this.allResourceTypesMap.get(
            item.origin.resource_type_id
          )}，资源名：${item.origin.wildcard}，角色：[${newStr}]\n权限：${item.origin.permissions}\n状态：${
            item.origin.enabled
          }`
          break
        }
        case 'trigger_apply': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `应用触发器：${item.current.name}\n资源类型：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，资源名：${item.current.wildcard}，角色：[${newStr}]\n权限：${item.current.permissions}\n状态：${
            item.current.enabled
          }`
          break
        }
        case 'trigger_cancel': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `取消触发器：${item.current.name}\n资源类型：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，资源名：${item.current.wildcard}，角色：[${newStr}]\n权限：${item.current.permissions}\n状态：${
            item.current.enabled
          }`
          break
        }
      }
    },
    handleQueryParams(queryParams) {
      const _queryParams = _.cloneDeep(queryParams)

      let q = ''
      for (const key in _queryParams) {
        if (
          key !== 'page' &&
          key !== 'page_size' &&
          key !== 'app_id' &&
          key !== 'start' &&
          key !== 'end' &&
          _queryParams[key] !== undefined
        ) {
          if (q) {
            q += `,${key}:${_queryParams[key]}`
          } else {
            q += `${key}:${_queryParams[key]}`
          }
        }
      }
      const newQueryParams = { ..._queryParams, q }
      return q ? newQueryParams : _queryParams
    },
    handleTagColor(operateType) {
      return this.colorMap.get(operateType)
    },
  },
}
</script>

<style lang="less" scoped>
p {
  margin-bottom: 0;
}
.ant-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
