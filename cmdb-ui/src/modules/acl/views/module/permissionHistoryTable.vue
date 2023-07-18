<template>
  <div>
    <search-form
      ref="child"
      :attrList="permissionTableAttrList"
      @search="handleSearch"
      @expandChange="handleExpandChange"
      @searchFormReset="searchFormReset"
      @loadMoreData="loadMoreResources"
      @fetchData="fetchResources"
      @resourceClear="resourceClear"
    ></search-form>
    <vxe-table
      ref="xTable"
      stripe
      class="ops-stripe-table"
      resizable
      size="small"
      :data="tableData"
      :loading="loading"
      :height="`${windowHeight - windowHeightMinus}px`"
      :scroll-y="{ enabled: false }"
    >
      <vxe-column field="created_at" width="144px" title="操作时间">
        <template #default="{ row }">
          <span>{{ row.deleted_at || row.updated_at || row.created_at }}</span>
        </template>
      </vxe-column>
      <vxe-column field="operate_uid" width="130px" title="操作员"></vxe-column>
      <vxe-column field="operate_type" width="80px" title="操作">
        <template #default="{ row }">
          <a-tag :color="row.operate_type === 'grant' ? 'green' : 'red'">{{
            operateTypeMap.get(row.operate_type)
          }}</a-tag>
        </template>
      </vxe-column>
      <vxe-column field="rid" title="用户"></vxe-column>
      <vxe-column field="resource_type_id" title="资源类型"></vxe-column>
      <vxe-column field="resources" title="资源">
        <template #default="{ row }">
          <template v-if="row.resource_ids.length > 0">
            <a-tooltip placement="top">
              <template slot="title">
                <span>{{ row.resource_ids[0] }}</span>
              </template>
              <a-tag color="blue" v-for="(resource, index) in row.resource_ids" :key="'resources_' + resource + index">
                {{ resource }}
              </a-tag>
            </a-tooltip>
          </template>
          <template v-else-if="row.group_ids.length > 0">
            <a-tag color="blue" v-for="(group, index) in row.group_ids" :key="'groups_' + group + index">
              {{ group }}
            </a-tag>
          </template>
        </template>
      </vxe-column>
      <vxe-column title="权限">
        <template #default="{ row }">
          <a-tag v-for="(perm, index) in row.permission_ids" :key="'perms_' + perm + index">
            {{ perm }}
          </a-tag>
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
import Pager from './pager.vue'
import SearchForm from './searchForm.vue'
import { searchPermissonHistory } from '@/modules/acl/api/history'
import debounce from 'lodash/debounce'
export default {
  components: { SearchForm, Pager },
  props: {
    allResourceTypes: {
      type: Array,
      required: true,
    },
    allResources: {
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
    this.fetchResources = debounce(this.fetchResources, 800)
    return {
      isExpand: false,
      loading: true,
      app_id: this.$route.name.split('_')[0],
      tableData: [],
      operateTypeMap: new Map([
        ['grant', '授权'],
        ['revoke', '撤销'],
      ]),
      queryParams: {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
        start: '',
        end: '',
      },
      permissionTableAttrList: [
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
          alias: '用户',
          is_choice: true,
          name: 'rid',
          value_type: '2',
          choice_value: this.allRoles,
        },
        {
          alias: '资源类型',
          is_choice: true,
          name: 'resource_type_id',
          value_type: '2',
          choice_value: this.allResourceTypes,
        },
        {
          alias: '资源',
          is_choice: true,
          name: 'resource_id',
          value_type: '2',
          choice_value: this.allResources,
        },
        {
          alias: '操作',
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [{ 授权: 'grant' }, { 撤销: 'revoke' }],
        },
      ],
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
    allResources: {
      deep: true,
      immediate: true,
      handler(val) {
        this.permissionTableAttrList[4].choice_value = val
      },
    },
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowHeightMinus() {
      return this.isExpand ? 374 : 310
    },
    tableDataLength() {
      return this.tableData.length
    },
  },
  methods: {
    // 获取数据
    async getTable(queryParams) {
      try {
        this.loading = true
        const { data, id2groups, id2perms, id2resources, id2roles } = await searchPermissonHistory(
          this.handleQueryParams(queryParams)
        )
        data.forEach((item) => {
          item.operate_uid = this.allUsersMap.get(item.operate_uid)
          item.rid = id2roles[item.rid].name
          item.resource_type_id = this.allResourceTypesMap.get(item.resource_type_id)
          item.resource_ids.forEach((subItem, index) => {
            item.resource_ids[index] = id2resources[subItem].name
          })
          item.group_ids.forEach((subItem, index) => {
            item.group_ids[index] = id2groups[subItem].name
          })
          item.permission_ids.forEach((subItem, index) => {
            item.permission_ids[index] = id2perms[subItem].name
          })
        })
        this.tableData = data
      } finally {
        this.loading = false
      }
    },
    loadMoreResources(name, value) {
      if (name === 'resource_id') {
        this.$emit('loadMoreResources', value)
      }
    },
    resourceClear() {
      this.$emit('resourceClear')
    },
    fetchResources(value) {
      if (value === '') {
        this.$emit('reloadResources')
        return
      }
      this.$emit('fetchResources', value)
    },
    // 处理查询参数
    handleQueryParams(queryParams) {
      let q = ''
      for (const key in queryParams) {
        if (
          key !== 'page' &&
          key !== 'page_size' &&
          key !== 'app_id' &&
          key !== 'start' &&
          key !== 'end' &&
          queryParams[key] !== undefined
        ) {
          if (q) q += `,${key}:${queryParams[key]}`
          else q += `${key}:${queryParams[key]}`
          delete queryParams[key]
        }
      }
      const newQueryParams = { ...queryParams, q }
      return q ? newQueryParams : queryParams
    },

    // searchForm相关
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: 50,
        app_id: this.$route.name.split('_')[0],
      }
      this.getTable(this.queryParams)
    },
    handleSearch(queryParams) {
      this.queryParams = { ...queryParams, app_id: this.app_id }
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
  },
}
</script>

<style lang="less" scoped>
.ant-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
