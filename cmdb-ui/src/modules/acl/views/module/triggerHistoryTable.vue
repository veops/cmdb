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
    tableDataLength() {
      return this.tableData.length
    },
    triggerTableAttrList() {
      return [
        {
          alias: this.$t('acl.date'),
          is_choice: false,
          name: 'datetime',
          value_type: '3',
        },
        {
          alias: this.$t('acl.operator'),
          is_choice: true,
          name: 'operate_uid',
          value_type: '2',
          choice_value: this.allUsers,
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
        {
          alias: this.$t('acl.trigger'),
          is_choice: true,
          name: 'trigger_id',
          value_type: '2',
          choice_value: this.allTriggers,
        },
      ]
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
      this.queryParams = { ...this.queryParams, ...queryParams }
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
          item.changeDescription = `${this.$t('acl.addTrigger')}: ${item.current.name}\n${this.$t('acl.resourceType')}: ：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，this.$t('acl.resourceName')：${item.current.wildcard}，${this.$t('acl.role2')}: [${newStr}]\n${this.$t('acl.permission')}: ${item.current.permissions}\n${this.$t('status')}: ${
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
                const str = ` 【 ${key} : -> ${newVal} 】 `
                item.changeDescription += str
              } else {
                const str = ` 【 ${key} : ${oldVal} -> ${newVal} 】 `
                item.changeDescription += ` 【 ${key} : ${oldVal} -> ${newVal} 】 `
              }
            }
          }
          if (!item.changeDescription) item.changeDescription = this.$t('acl.noChange')
          break
        }
        case 'delete': {
          const str = item.origin.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `${this.$t('acl.deleteTrigger')}: ${item.origin.name}\n${this.$t('acl.resourceType')}: ：${this.allResourceTypesMap.get(
            item.origin.resource_type_id
          )}，this.$t('acl.resourceName')：${item.origin.wildcard}，${this.$t('acl.role2')}: [${newStr}]\n${this.$t('acl.permission')}: ${item.origin.permissions}\n${this.$t('status')}: ${
            item.origin.enabled
          }`
          break
        }
        case 'trigger_apply': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `${this.$t('acl.applyTrigger')}: ${item.current.name}\n${this.$t('acl.resourceType')}: ：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，this.$t('acl.resourceName')：${item.current.wildcard}，${this.$t('acl.role2')}: [${newStr}]\n${this.$t('acl.permission')}: ${item.current.permissions}\n${this.$t('status')}: ${
            item.current.enabled
          }`
          break
        }
        case 'trigger_cancel': {
          const str = item.current.roles
          const newArr = str.slice(1, str.length - 1).split(', ')
          const newStr = newArr.map((i) => this.allRolesMap.get(Number(i))).join('，')
          item.changeDescription = `${this.$t('acl.cancelTrigger')}: ${item.current.name}\n${this.$t('acl.resourceType')}: ：${this.allResourceTypesMap.get(
            item.current.resource_type_id
          )}，this.$t('acl.resourceName')：${item.current.wildcard}，${this.$t('acl.role2')}: [${newStr}]\n${this.$t('acl.permission')}: ${item.current.permissions}\n${this.$t('status')}: ${
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
