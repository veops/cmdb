<template>
  <div>
    <search-form
      ref="child"
      :attrList="permissionTableAttrList"
      @search="handleSearch"
      @expandChange="handleExpandChange"
      @searchFormReset="searchFormReset"
      @searchFormChange="searchFormChange"
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
      <vxe-column field="created_at" width="144px" :title="$t('acl.operateTime')">
        <template #default="{ row }">
          <span>{{ row.deleted_at || row.updated_at || row.created_at }}</span>
        </template>
      </vxe-column>
      <vxe-column field="operate_uid" width="130px" :title="$t('acl.operator')"></vxe-column>
      <vxe-column field="operate_type" width="100px" :title="$t('operation')">
        <template #default="{ row }">
          <a-tag :color="row.operate_type === 'grant' ? 'green' : 'red'">{{
            operateTypeMap.get(row.operate_type)
          }}</a-tag>
        </template>
      </vxe-column>
      <vxe-column field="rid" :title="$t('user')"></vxe-column>
      <vxe-column field="resource_type_id" :title="$t('acl.resourceType')"></vxe-column>
      <vxe-column field="resources" :title="$t('acl.resource')">
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
      <vxe-column :title="$t('acl.permission')">
        <template #default="{ row }">
          <a-tag v-for="(perm, index) in row.permission_ids" :key="'perms_' + perm + index">
            {{ perm }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="source" width="100px" :title="$t('acl.source')"></vxe-column>
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
import debounce from 'lodash/debounce'
import Pager from '@/components/Pager'
import SearchForm from '../../module/searchForm.vue'
import { searchApp } from '@/modules/acl/api/app'
import { searchPermissonHistory } from '@/modules/acl/api/history'
import { searchRole } from '@/modules/acl/api/role'
import { searchUser } from '@/modules/acl/api/user'
import { searchResource, searchResourceType } from '@/modules/acl/api/resource'
export default {
  components: { SearchForm, Pager },
  data() {
    this.fetchResources = debounce(this.fetchResources, 800)
    return {
      app_id: undefined,
      resource_id: undefined,
      isExpand: false,
      loading: true,
      resourcesPage: 1,
      resourcesNum: 0,
      tableData: [],
      allRoles: [],
      allUsers: [],
      allResourceTypes: [],
      allResources: [],
      allApps: [],
      allRolesMap: new Map(),
      allUsersMap: new Map(),
      allResourceTypesMap: new Map(),
      queryParams: {
        page: 1,
        page_size: 50,
        start: '',
        end: '',
      },
      permissionTableAttrList: [
        {
          alias: this.$t('acl.date'),
          is_choice: false,
          name: 'datetime',
          value_type: '3',
        },
        {
          alias: this.$t('acl.app'),
          is_choice: true,
          name: 'app_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('acl.operator'),
          is_choice: true,
          name: 'operate_uid',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('user'),
          is_choice: true,
          name: 'rid',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('acl.resourceType'),
          is_choice: true,
          name: 'resource_type_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('acl.resource'),
          is_choice: true,
          name: 'resource_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('operation'),
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [{ [this.$t('grant')]: 'grant' }, { [this.$t('acl.cancel')]: 'revoke' }],
        },
      ],
    }
  },
  computed: {
    operateTypeMap() {
      return new Map([
        ['grant', this.$t('grant')],
        ['revoke', this.$t('acl.cancel')],
      ])
    },
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
  async created() {
    this.$watch(
      function () {
        return this.permissionTableAttrList[3].choice_value
      },
      function () {
        delete this.$refs.child.queryParams.rid
        delete this.$refs.child.queryParams.resource_type_id
        delete this.$refs.child.queryParams.resource_id
      }
    )
    await Promise.all([this.getAllApps(), this.getAllUsers()])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  methods: {
    async getTable(queryParams) {
      try {
        this.loading = true
        const { data, id2groups, id2perms, id2resources, id2roles, id2resource_types } = await searchPermissonHistory(
          this.handleQueryParams(queryParams)
        )
        data.forEach((item) => {
          item.rid = id2roles[item.rid].name
          item.operate_uid = this.allUsersMap.get(item.operate_uid)
          // 脏数据清除后可删
          if (id2resource_types[item.resource_type_id]) {
            item.resource_type_id = id2resource_types[item.resource_type_id].name
          }
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
    async getAllApps() {
      const res = await searchApp()
      const allApps = []
      res.apps.forEach((item) => {
        allApps.push({ [item.name]: item.id })
      })
      this.allApps = allApps
      this.permissionTableAttrList[1].choice_value = this.allApps
    },
    async getAllRoles(app_id) {
      if (!app_id) {
        this.permissionTableAttrList[3].choice_value = []
        return
      }
      const { roles } = await searchRole({
        page_size: 9999,
        app_id: app_id,
      })
      const allRoles = []
      roles.forEach((item) => {
        allRoles.push({ [item.name]: item.id })
      })
      this.allRoles = allRoles
      this.permissionTableAttrList[3].choice_value = this.allRoles
    },
    async getAllUsers() {
      const { users } = await searchUser({ page_size: 10000, app_id: 'acl' })
      const allUsers = []
      const allUsersMap = new Map()
      users.forEach((item) => {
        allUsers.push({ [item.nickname]: item.uid })
        allUsersMap.set(item.uid, item.nickname)
      })
      this.allUsers = allUsers
      this.allUsersMap = allUsersMap
      this.permissionTableAttrList[2].choice_value = this.allUsers
    },
    async getAllResourceTypes(app_id) {
      if (!app_id) {
        this.permissionTableAttrList[4].choice_value = []
        return
      }
      const { groups } = await searchResourceType({
        page_size: 9999,
        page: 1,
        app_id: app_id,
      })
      const allResourceTypes = []
      groups.forEach((item) => {
        allResourceTypes.push({ [item.name]: item.id })
      })
      this.allResourceTypes = allResourceTypes
      this.permissionTableAttrList[4].choice_value = this.allResourceTypes
    },
    async getAllResources(app_id, page, value = undefined) {
      if (!app_id) {
        this.permissionTableAttrList[5].choice_value = []
        return
      }
      const { resources, numfound } = await searchResource({
        page: page,
        page_size: 50,
        app_id: app_id,
        q: value,
      })
      this.resourcesNum = numfound
      const allResources = this.allResources
      resources.forEach((item) => {
        allResources.push({ [item.name]: item.id })
      })
      this.allResources = allResources
      this.permissionTableAttrList[5].choice_value = this.allResources
    },
    loadMoreResources(name, value) {
      if (name === 'resource_id' && this.allResources.length < this.resourcesNum) {
        let currentPage = this.resourcesPage
        this.getAllResources(this.app_id, ++currentPage, value)
        this.resourcesPage = currentPage
      }
    },
    resourceClear() {
      this.resourcesPage = 1
      this.allResources = []
      this.getAllResources(this.app_id, 1)
    },
    async fetchResources(value) {
      this.allResources = []
      const allResources = []
      if (!this.app_id) {
        this.permissionTableAttrList[5].choice_value = []
        return
      }
      this.resourcesPage = 1
      if (value === '') {
        this.getAllResources(this.app_id, 1)
        return
      }
      const { resources, numfound } = await searchResource({
        page: 1,
        page_size: 50,
        app_id: this.app_id,
        q: value,
      })
      this.resourcesNum = numfound
      resources.forEach((item) => {
        allResources.push({ [item.name]: item.id })
      })
      this.allResources = allResources
      this.permissionTableAttrList[5].choice_value = this.allResources
    },

    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: 50,
      }
      this.resourcesPage = 1
      this.resourcesNum = 0
      this.getTable(this.queryParams)
    },
    handleSearch(queryParams) {
      this.queryParams = { ...this.queryParams, ...queryParams }
      this.getTable(this.queryParams)
    },
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    async searchFormChange(queryParams) {
      if (this.app_id !== queryParams.app_id) {
        this.app_id = queryParams.app_id
        this.allResources = []
        this.resourcesPage = 1
        this.resourcesNum = 0
        await Promise.all([
          this.getAllRoles(this.app_id),
          this.getAllResourceTypes(this.app_id),
          this.getAllResources(this.app_id, this.resourcesPage),
        ])
      }
      if (queryParams.app_id === undefined) {
        this.app_id = undefined
        this.$refs.child.queryParams.rid = undefined
        this.$refs.child.queryParams.resource_type_id = undefined
        this.$refs.child.queryParams.resource_id = undefined
        this.allResources = []
        this.resourcesPage = 1
        this.resourcesNum = 0
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
          if (q) q += `,${key}:${_queryParams[key]}`
          else q += `${key}:${_queryParams[key]}`
          delete _queryParams[key]
        }
      }
      const newQueryParams = { ..._queryParams, q }
      return q ? newQueryParams : _queryParams
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
