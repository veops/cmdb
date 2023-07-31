<template>
  <div>
    <search-form
      ref="child"
      :attrList="resourceTableAttrList"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
    ></search-form>
    <vxe-table
      ref="xTable"
      stripe
      class="ops-stripe-table"
      size="small"
      :data="tableData"
      resizable
      :loading="loading"
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
      <vxe-column field="link_id" title="资源类型名">
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
      <vxe-column field="source" width="100px" title="来源"></vxe-column>
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
import { searchResourceHistory } from '@/modules/acl/api/history'
export default {
  components: { SearchForm, Pager },
  props: {
    allResourceTypes: {
      type: Array,
      required: true,
    },
    allUsers: {
      type: Array,
      required: true,
    },
    allRoles: {
      type: Array,
      required: true,
    },
    allRolesMap: {
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
      loading: true,
      checked: false,
      tableData: [],
      app_id: this.$route.name.split('_')[0],
      resourceTableAttrList: [
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
          choice_value: [{ 新建: 'create' }, { 修改: 'update' }, { 删除: 'delete' }],
        },
        {
          alias: '资源类型',
          is_choice: true,
          name: 'link_id',
          value_type: '2',
          choice_value: this.allResourceTypes,
        },
      ],
      operateTypeMap: new Map([
        ['create', '新建'],
        ['update', '修改'],
        ['delete', '删除'],
      ]),
      colorMap: new Map([
        ['create', 'green'],
        ['update', 'orange'],
        ['delete', 'red'],
      ]),
      queryParams: {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
        scope: 'resource_type',
        start: '',
        end: '',
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
        const { data } = await searchResourceHistory(this.handleQueryParams(queryParams))
        data.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type)
          item.operate_uid = this.allUsersMap.get(item.operate_uid)
        })
        this.tableData = data
      } finally {
        this.loading = false
      }
    },

    // searchForm相关
    handleSearch(queryParams) {
      this.queryParams = { ...this.queryParams, ...queryParams, app_id: this.app_id, scope: 'resource_type' }
      this.getTable(this.queryParams)
    },
    searchFormReset() {
      this.$refs.child.checked = false
      this.checked = false
      this.queryParams = {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
        scope: 'resource_type',
      }
      this.getTable(this.queryParams)
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

    handleQueryParams(queryParams) {
      const _queryParams = _.cloneDeep(queryParams)

      let flag = false
      let q = _queryParams.q ? _queryParams.q : ''
      for (const key in _queryParams) {
        if (
          key !== 'page' &&
          key !== 'page_size' &&
          key !== 'app_id' &&
          key !== 'q' &&
          key !== 'start' &&
          key !== 'end' &&
          _queryParams[key] !== undefined
        ) {
          flag = true
          if (q) q += `,${key}:${_queryParams[key]}`
          else q += `${key}:${_queryParams[key]}`
          delete _queryParams[key]
        }
      }
      const newQueryParams = { ..._queryParams, q }
      return flag ? newQueryParams : _queryParams
    },
    handleTagColor(operateType) {
      return this.colorMap.get(operateType)
    },
    handleChangeDescription(item, operate_type) {
      switch (operate_type) {
        // create
        case 'create': {
          item.changeDescription = `新增资源类型：${item.current.name}\n描述：${item.current.description}\n权限：${item.extra.permission_ids.current}`
          break
        }
        case 'update': {
          item.changeDescription = ''
          for (const key in item.origin) {
            const newVal = item.current[key]
            const oldVal = item.origin[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at' && key !== 'deleted_at' && key !== 'created_at') {
              if (oldVal === null || oldVal === '') {
                const str = ` 【 ${key} : 改为 ${newVal} 】 \n`
                item.changeDescription += str
              } else {
                const str = ` 【 ${key} : 由 ${oldVal} 改为 ${newVal} 】 \n`
                item.changeDescription += str
              }
            }
          }
          const currentPerms = item.extra.permission_ids.current
          const originPerms = item.extra.permission_ids.origin
          if (!_.isEqual(currentPerms, originPerms)) {
            item.changeDescription += ` 【 permission_ids : 由 ${originPerms} 改为 ${currentPerms} 】 `
          }
          if (!item.changeDescription) item.changeDescription = '没有修改'
          break
        }
        case 'delete': {
          item.changeDescription = `删除资源类型：${item.origin.name}\n描述：${item.origin.description}\n权限：${item.extra.permission_ids.origin}`
          break
        }
      }
    },
  },
}
</script>

<style lang="less" scoped>
.row {
  margin-top: 5px;
}
.ant-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
p {
  margin-bottom: 0;
}
</style>
