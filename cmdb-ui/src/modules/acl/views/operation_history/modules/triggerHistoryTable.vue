<template>
  <div>
    <search-form
      ref="child"
      :attrList="triggerTableAttrList"
      @searchFormReset="searchFormReset"
      @search="handleSearch"
      @expandChange="handleExpandChange"
      @searchFormChange="searchFormChange"
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
import Pager from '../../module/pager.vue'
import SearchForm from '../../module/searchForm.vue'
import { searchTriggerHistory } from '@/modules/acl/api/history'
import { getTriggers } from '@/modules/acl/api/trigger'
import { searchUser } from '@/modules/acl/api/user'
import { searchApp } from '@/modules/acl/api/app'
export default {
  components: { SearchForm, Pager },
  data() {
    return {
      app_id: undefined,
      loading: true,
      isExpand: false,
      tableData: [],
      allResourceTypes: [],
      allResources: [],
      allUsers: [],
      allRoles: [],
      allTriggers: [],
      allApps: [],
      allRolesMap: new Map(),
      allUsersMap: new Map(),
      allResourceTypesMap: new Map(),
      allResourcesMap: new Map(),
      allTriggersMap: new Map(),
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
          alias: '应用',
          is_choice: true,
          name: 'app_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: '操作员',
          is_choice: true,
          name: 'operate_uid',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: '触发器',
          is_choice: true,
          name: 'trigger_id',
          value_type: '2',
          choice_value: [],
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
      ],
      queryParams: {
        page: 1,
        page_size: 50,
        start: '',
        end: '',
      },
    }
  },
  async created() {
    this.$watch(
      function() {
        return this.triggerTableAttrList[3].choice_value
      },
      function() {
        delete this.$refs.child.queryParams.trigger_id
      }
    )
    await Promise.all([this.getAllApps(), this.getAllUsers()])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
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
    async getTable(queryParams) {
      try {
        this.loading = true
        const { data, id2resource_types, id2roles } = await searchTriggerHistory(this.handleQueryParams(queryParams))
        data.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type, id2resource_types, id2roles)
          item.trigger_id = this.allTriggersMap.get(item.trigger_id)
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
      this.triggerTableAttrList[1].choice_value = this.allApps
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
      this.triggerTableAttrList[2].choice_value = this.allUsers
    },
    async getTriggers(app_id) {
      if (!app_id) {
        this.triggerTableAttrList[3].choice_value = []
        return
      }
      const res = await getTriggers({ app_id: app_id })
      const allTriggers = []
      const allTriggersMap = new Map()
      res.forEach((item) => {
        allTriggers.push({ [item.name]: item.id })
        allTriggersMap.set(item.id, item.name)
      })
      this.allTriggers = allTriggers
      this.allTriggersMap = allTriggersMap
      this.triggerTableAttrList[3].choice_value = this.allTriggers
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
        page_size: 50,
      }
      this.getTable(this.queryParams)
    },
    async searchFormChange(queryParams) {
      if (this.app_id !== queryParams.app_id) {
        this.app_id = queryParams.app_id
        await this.getTriggers(this.app_id)
      }
      if (queryParams.app_id === undefined) {
        this.app_id = undefined
        this.$refs.child.queryParams.trigger_id = undefined
      }
    },

    handleChangeDescription(item, operate_type, id2resource_types, id2roles) {
      switch (operate_type) {
        // create
        case 'create': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.current
          item.changeDescription = `新增触发器：${name}\n资源类型：${
            id2resource_types[resource_type_id].name
          }，资源名：${wildcard || ''}，角色：[${newStr}]\n权限：${permissions}\n状态：${enabled}`
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
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.origin
          item.changeDescription = `删除触发器：${name}\n资源类型：${
            id2resource_types[resource_type_id].name
          }，资源名：${wildcard || ''}，角色：[${newStr}]\n权限：${permissions}\n状态：${enabled}`
          break
        }
        case 'trigger_apply': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.current
          item.changeDescription = `应用触发器：${name}\n资源类型：${
            id2resource_types[resource_type_id].name
          }，资源名：${wildcard || ''}，角色：[${newStr}]\n权限：${permissions}\n状态：${enabled}`
          break
        }
        case 'trigger_cancel': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.current
          item.changeDescription = `取消触发器：${name}\n资源类型：${
            id2resource_types[resource_type_id].name
          }，资源名：${wildcard || ''}，角色：[${newStr}]\n权限：${permissions}\n状态：${enabled}`
          break
        }
      }
    },
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
          if (q) {
            q += `,${key}:${queryParams[key]}`
          } else {
            q += `${key}:${queryParams[key]}`
          }
        }
      }
      const newQueryParams = { ...queryParams, q }
      return q ? newQueryParams : queryParams
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
