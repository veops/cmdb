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
      <vxe-column field="created_at" width="144px" :title="$t('acl.operateTime')"></vxe-column>
      <vxe-column field="operate_uid" width="130px" :title="$t('acl.operator')"></vxe-column>
      <vxe-column field="operate_type" width="100px" :title="$t('operation')">
        <template #default="{ row }">
          <a-tag :color="handleTagColor(row.operate_type)">
            {{ operateTypeMap.get(row.operate_type) }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="trigger_id" width="250px" :title="$t('acl.trigger')">
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
import { searchTriggerHistory } from '@/modules/acl/api/history'
import { getTriggers } from '@/modules/acl/api/trigger'
import { searchUser } from '@/modules/acl/api/user'
import { searchApp } from '@/modules/acl/api/app'
export default {
  name: 'TriggerHistoryTable',
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
      colorMap: new Map([
        ['create', 'green'],
        ['delete', 'red'],
        ['update', 'orange'],
        ['trigger_apply', 'green'],
        ['trigger_cancel', 'red'],
      ]),
      queryParams: {
        page: 1,
        page_size: 50,
        start: '',
        end: '',
      },
      triggerTableAttrList: [
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
          alias: this.$t('acl.trigger'),
          is_choice: true,
          name: 'trigger_id',
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
            { [this.$t('acl.apply')]: 'trigger_apply' },
            { [this.$t('cancel')]: 'trigger_cancel' },
          ],
        },
      ],
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
    operateTypeMap() {
      return new Map([
        ['create', this.$t('create')],
        ['update', this.$t('update')],
        ['delete', this.$t('delete')],
        ['trigger_apply', this.$t('acl.apply')],
        ['trigger_cancel', this.$t('cancel')],
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
      this.queryParams = { ...this.queryParams, ...queryParams }
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
          item.changeDescription = `${this.$t('acl.addTrigger')}:${name}\n${this.$t('acl.resourceType')}: ${
            id2resource_types[resource_type_id].name
          }，this.$t('acl.resourceName')：${wildcard || ''}，${this.$t(
            'acl.role2'
          )}:[${newStr}]\nthis.$t('acl.permssion')}: ${permissions}\n${this.$t('status')}: ${enabled}`
          break
        }
        case 'update': {
          item.changeDescription = ''
          for (const key in item.origin) {
            const newVal = item.current[key]
            const oldVal = item.origin[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at' && key !== 'deleted_at' && key !== 'created_at') {
              if (oldVal === null) {
                const str = ` 【 ${key} : -> ${newVal} 】 `
                item.changeDescription += str
              } else {
                item.changeDescription += ` 【 ${key} :${oldVal} -> ${newVal} 】 `
              }
            }
          }
          if (!item.changeDescription) item.changeDescription = this.$t('acl.noChange')
          break
        }
        case 'delete': {
          const str = item.origin.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.origin
          item.changeDescription = `${this.$t('acl.deleteTrigger')}: ${name}\n${this.$t('acl.resourceType')}: ${
            id2resource_types[resource_type_id].name
          }，${this.$t('acl.resourceName')}: ${wildcard || ''}，${this.$t(
            'acl.role2'
          )}:[${newStr}]\nthis.$t('acl.permssion')}: ${permissions}\n${this.$t('status')}: ${enabled}`
          break
        }
        case 'trigger_apply': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.current
          item.changeDescription = `${this.$t('acl.applyTrigger')}: ${name}\n${this.$t('acl.resourceType')}: ${
            id2resource_types[resource_type_id].name
          }，${this.$t('acl.resourceName')}: ${wildcard || ''}，${this.$t(
            'acl.role2'
          )}:[${newStr}]\nthis.$t('acl.permssion')}: ${permissions}\n${this.$t('status')}: ${enabled}`
          break
        }
        case 'trigger_cancel': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => id2roles[i].name).join('，')
          const { name, resource_type_id, wildcard, permissions, enabled } = item.current
          item.changeDescription = `${this.$t('acl.cancelTrigger')}: ${name}\n${this.$t('acl.resourceType')}: ${
            id2resource_types[resource_type_id].name
          }，${this.$t('acl.resourceName')}: ${wildcard || ''}，${this.$t(
            'acl.role2'
          )}:[${newStr}]\nthis.$t('acl.permssion')}: ${permissions}\n${this.$t('status')}: ${enabled}`
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
