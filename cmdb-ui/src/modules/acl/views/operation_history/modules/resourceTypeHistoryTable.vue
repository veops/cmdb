<template>
  <div>
    <search-form
      ref="child"
      :attrList="resourceTableAttrList"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
      @searchFormChange="searchFormChange"
      @expandChange="handleExpandChange"
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
    >
      <vxe-column field="created_at" width="144px" :title="$t('acl.operateTime')"></vxe-column>
      <vxe-column field="operate_uid" width="130px" :title="$t('acl.operator')"></vxe-column>
      <vxe-column field="operate_type" width="100px" :title="$t('operation')">
        <template #default="{ row }">
          <a-tag :color="handleTagColor(row.operate_type)">
            {{ operateTypeMap.get(row.operate_type) }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="link_id" width="159px" :title="$t('acl.resourceTypeName')">
        <template #default="{ row }">
          <span>
            {{ row.current.name || row.origin.name }}
          </span>
        </template>
      </vxe-column>
      <vxe-column :title="$t('desc')">
        <template #default="{ row }">
          <p>
            {{ row.changeDescription }}
          </p>
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
import Pager from '@/components/Pager'
import SearchForm from '../../module/searchForm.vue'
import { searchResourceHistory } from '@/modules/acl/api/history'
import { searchUser } from '@/modules/acl/api/user'
import { searchResourceType } from '@/modules/acl/api/resource'
import { searchApp } from '@/modules/acl/api/app'
export default {
  components: { SearchForm, Pager },
  data() {
    return {
      loading: true,
      checked: false,
      isExpand: false,
      app_id: undefined,
      tableData: [],
      allResourceTypes: [],
      allUsers: [],
      allApps: [],
      allUsersMap: new Map(),
      allResourcesMap: new Map(),
      colorMap: new Map([
        ['create', 'green'],
        ['update', 'orange'],
        ['delete', 'red'],
      ]),
      queryParams: {
        page: 1,
        page_size: 50,
        scope: 'resource_type',
        start: '',
        end: '',
      },
      resourceTableAttrList: [
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
          alias: this.$t('acl.resourceType'),
          is_choice: true,
          name: 'link_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: this.$t('operation'),
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { [this.$t('create')]: 'create' },
            { [this.$t('update')]: 'update' },
            { [this.$t('delete')]: 'delete' },
          ],
        },
      ],
    }
  },
  async created() {
    this.$watch(
      function() {
        return this.resourceTableAttrList[3].choice_value
      },
      function() {
        delete this.$refs.child.queryParams.link_id
      }
    )
    await Promise.all([this.getAllApps(), this.getAllUsers()])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  computed: {
    operateTypeMap() {
      return new Map([
        ['create', this.$t('create')],
        ['update', this.$t('update')],
        ['delete', this.$t('delete')],
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
    async getAllApps() {
      const { apps } = await searchApp()
      const allApps = []
      apps.forEach((item) => {
        allApps.push({ [item.name]: item.id })
      })
      this.allApps = allApps
      this.resourceTableAttrList[1].choice_value = this.allApps
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
      this.resourceTableAttrList[2].choice_value = this.allUsers
    },
    async getAllResourceTypes(app_id) {
      if (!app_id) {
        this.resourceTableAttrList[3].choice_value = []
        return
      }
      const { groups } = await searchResourceType({
        page: 1,
        page_size: 9999,
        app_id: app_id,
      })
      const allResourceTypes = []
      groups.forEach((item) => {
        allResourceTypes.push({ [item.name]: item.id })
      })
      this.allResourceTypes = allResourceTypes
      this.resourceTableAttrList[3].choice_value = this.allResourceTypes
    },

    // searchForm相关
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    handleSearch(queryParams) {
      this.queryParams = { ...this.queryParams, ...queryParams, scope: 'resource_type' }
      this.getTable(this.queryParams)
    },
    searchFormReset() {
      this.$refs.child.checked = false
      this.checked = false
      this.queryParams = {
        page: 1,
        page_size: 50,
        scope: 'resource_type',
      }
      this.getTable(this.queryParams)
    },
    async searchFormChange(queryParams) {
      if (this.app_id !== queryParams.app_id) {
        this.app_id = queryParams.app_id
        await this.getAllResourceTypes(this.app_id)
      }
      if (queryParams.app_id === undefined) {
        this.app_id = undefined
        this.$refs.child.queryParams.link_id = undefined
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
          const description = item.current?.description === undefined ? this.$t('acl.none') : item.current?.description
          const permission =
            item.extra.permission_ids?.current === undefined ? this.$t('acl.none') : item.extra.permission_ids?.current
          item.changeDescription = `${this.$t('acl.addResourceType')}：${item.current.name}\n${this.$t(
            'desc'
          )}：${description}\n${this.$t('acl.permission')}：${permission}`
          break
        }
        case 'update': {
          item.changeDescription = ''
          for (const key in item.origin) {
            const newVal = item.current[key]
            const oldVal = item.origin[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at' && key !== 'deleted_at' && key !== 'created_at') {
              if (oldVal === null || oldVal === '') {
                const str = ` 【 ${key} : -> ${newVal} 】 \n`
                item.changeDescription += str
              } else {
                const str = ` 【 ${key} : ${oldVal} -> ${newVal} 】 \n`
                item.changeDescription += str
              }
            }
          }
          const currentPerms =
            item.extra.permission_ids?.current === undefined ? this.$t('acl.none') : item.extra.permission_ids?.current
          const originPerms =
            item.extra.permission_ids?.origin === undefined ? this.$t('acl.none') : item.extra.permission_ids?.origin
          if (!_.isEqual(currentPerms, originPerms)) {
            item.changeDescription += ` 【 permission_ids : ${originPerms} -> ${currentPerms} 】 `
          }
          if (!item.changeDescription) item.changeDescription = this.$t('acl.noChange')
          break
        }
        case 'delete': {
          const description = item.origin?.description === undefined ? this.$t('acl.none') : item.origin?.description
          const permission =
            item.extra.permission_ids?.origin === undefined ? this.$t('acl.none') : item.extra.permission_ids?.origin
          item.changeDescription = `${this.$t('acl.deleteResourceType')}: ${item.origin.name}\n${this.$t(
            'desc'
          )}：${description}\n${this.$t('acl.permission')}: ${permission}`
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
