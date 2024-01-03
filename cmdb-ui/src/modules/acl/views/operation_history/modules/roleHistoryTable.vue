<template>
  <div>
    <search-form
      ref="child"
      :attrList="roleTableAttrList"
      :hasSwitch="true"
      :switchValue="$t('acl.roleRelation')"
      @onSwitchChange="onSwitchChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
    ></search-form>
    <vxe-table
      stripe
      class="ops-stripe-table"
      ref="xTable"
      resizable
      size="small"
      :data="tableData"
      :loading="loading"
      :height="`${windowHeight - 310}px`"
    >
      <vxe-column field="created_at" width="144px" :title="$t('acl.operateTime')"></vxe-column>
      <vxe-column field="operate_uid" width="130px" :title="$t('acl.operator')"></vxe-column>
      <vxe-column field="operate_type" width="112px" :title="$t('operation')">
        <template #default="{ row }">
          <template>
            <a-tag :color="handleTagColor(row.operate_type)">{{ operateTypeMap.get(row.operate_type) }}</a-tag>
          </template>
        </template>
      </vxe-column>
      <vxe-column :title="checked ? $t('acl.role2') : $t('acl.role2')">
        <template #default="{ row }">
          <template v-if="!checked">
            <a-tag color="blue">{{ row.current.name || row.origin.name }}</a-tag>
          </template>
          <template v-else>
            <a-tag v-for="(id, index) in row.extra.child_ids" :key="'child_ids_' + id + index" color="blue">{{
              id
            }}</a-tag>
          </template>
        </template>
      </vxe-column>
      <vxe-column :title="checked ? $t('acl.inheritedFrom') : $t('acl.admin')" :width="checked ? '350px' : '80px'">
        <template #default="{ row }">
          <template v-if="!checked">
            <a-icon type="check" v-if="row.current.is_app_admin" />
          </template>
          <template v-else>
            <a-tag v-for="(id, index) in row.extra.parent_ids" :key="'parent_ids_' + id + index" color="cyan">{{
              id
            }}</a-tag>
          </template>
        </template>
      </vxe-column>
      <vxe-column :title="$t('desc')" v-if="!checked">
        <template #default="{ row }">
          <p>
            {{ row.description }}
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
import Pager from '../../module/pager.vue'
import SearchForm from '../../module/searchForm.vue'
import { searchRoleHistory } from '@/modules/acl/api/history'
import { searchApp } from '@/modules/acl/api/app'
import { searchUser } from '@/modules/acl/api/user'
export default {
  components: { SearchForm, Pager },
  data() {
    return {
      loading: true,
      checked: false,
      app_id: undefined,
      tableData: [],
      allApps: [],
      allUsers: [],
      allRoles: [],
      allRolesMap: new Map(),
      allUsersMap: new Map(),
      colorMap: new Map([
        ['create', 'green'],
        ['delete', 'red'],
        ['update', 'orange'],
        ['role_relation_add', 'green'],
        ['role_relation_delete', 'red'],
      ]),
      queryParams: {
        page: 1,
        page_size: 50,
        scope: 'role',
        start: '',
        end: '',
      },
      roleTableAttrList: [
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
          alias: this.$t('operation'),
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { [this.$t('create')]: 'create' },
            { [this.$t('update')]: 'update' },
            { [this.$t('delete')]: 'delete' },
            { [this.$t('acl.roleRelationAdd')]: 'role_relation_add' },
            { [this.$t('acl.roleRelationDelete')]: 'role_relation_delete' },
          ],
        },
      ],
    }
  },
  computed: {
    operateTypeMap() {
      return new Map([
        ['create', this.$t('create')],
        ['update', this.$t('update')],
        ['delete', this.$t('delete')],
        ['role_relation_add', this.$t('acl.roleRelationAdd')],
        ['role_relation_delete', this.$t('acl.roleRelationDelete')],
      ])
    },
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableDataLength() {
      return this.tableData.length
    },
  },
  async created() {
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
        const { data, id2roles, id2perms, id2resources } = await searchRoleHistory(this.handleQueryParams(queryParams))
        data.forEach((item) => {
          item.operate_uid = this.allUsersMap.get(item.operate_uid)
          if (item.operate_type === 'role_relation_add' || item.operate_type === 'role_relation_delete') {
            item.extra.child_ids.forEach((subItem, index) => {
              item.extra.child_ids[index] = id2roles[subItem].name
            })
            item.extra.parent_ids.forEach((subItem, index) => {
              item.extra.parent_ids[index] = id2roles[subItem].name
            })
          } else {
            this.handleChangeDescription(item, item.operate_type, id2roles, id2perms, id2resources)
          }
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
      this.roleTableAttrList[1].choice_value = this.allApps
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
      this.roleTableAttrList[2].choice_value = this.allUsers
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
    onSwitchChange(checked) {
      this.checked = checked
      this.queryParams.scope = checked ? 'role_relation' : 'role'
      this.queryParams.page = 1
      this.getTable(this.queryParams)
    },
    handleSearch(queryParams) {
      this.queryParams = { ...this.queryParams, ...queryParams, scope: this.checked ? 'role_relation' : 'role' }
      this.getTable(this.queryParams)
    },
    searchFormReset() {
      this.$refs.child.checked = false
      this.checked = false
      this.queryParams = {
        page: 1,
        page_size: 50,
        scope: this.checked ? 'role_relation' : 'role',
      }
      this.getTable(this.queryParams)
    },

    // 处理查询参数
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
    // 处理tag颜色
    handleTagColor(operateType) {
      return this.colorMap.get(operateType)
    },
    handleChangeDescription(item, operate_type, id2roles, id2perms, id2resources) {
      switch (operate_type) {
        // create
        case 'create': {
          item.description = `${this.$t('acl.addRole')}${item.current.name}`
          break
        }
        case 'update': {
          item.description = ''
          for (const key in item.origin) {
            const newVal = item.current[key]
            const oldVal = item.origin[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at' && key !== 'deleted_at' && key !== 'created_at') {
              if (oldVal === null) {
                const str = ` 【 ${key} : -> ${newVal} 】 `
                item.description += str
              } else {
                item.description += ` 【 ${key} : ${oldVal} -> ${newVal} 】 `
              }
            }
          }
          if (!item.description) item.description = this.$t('acl.noChange')
          break
        }
        case 'delete': {
          const {
            extra: { child_ids, parent_ids, role_permissions },
          } = item
          child_ids.forEach((subItem, index) => {
            child_ids[index] = id2roles[subItem].name
          })
          parent_ids.forEach((subItem, index) => {
            parent_ids[index] = id2roles[subItem].name
          })

          const resourceMap = new Map()
          const permsArr = []
          role_permissions.forEach((subItem) => {
            const resource_id = subItem.resource_id
            const perm_id = subItem.perm_id
            if (resourceMap.has(resource_id)) {
              let resource_perms = resourceMap.get(resource_id)
              resource_perms += `,${id2perms[perm_id].name}`
              resourceMap.set(resource_id, resource_perms)
            } else {
              resourceMap.set(resource_id, String(id2perms[perm_id].name))
            }
          })
          resourceMap.forEach((value, key) => {
            permsArr.push(`${id2resources[key].name}：${value}`)
          })
          item.description = `${this.$t('acl.heir')}：${child_ids}\n${this.$t(
            'acl.inheritedFrom'
          )}：${parent_ids}\n${this.$t('acl.involvingRP')}：\n${permsArr.join(`\n`)}`
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
