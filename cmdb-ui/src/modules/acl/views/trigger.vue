<template>
  <div class="acl-trigger">
    <div class="acl-trigger-header">
      <a-button type="primary" @click="handleCreateTrigger">{{ $t('acl.addTrigger') }}</a-button>
      <a-input-search
        class="ops-input"
        :style="{ display: 'inline', marginLeft: '10px', width: '200px' }"
        :placeholder="`${$t('search')} | ${$t('name')}`"
        v-model="searchName"
        allowClear
        @search="filter"
      ></a-input-search>
    </div>

    <vxe-grid
      stripe
      size="small"
      class="ops-stripe-table"
      :columns="tableColumns"
      :data="filterTriggers"
      :max-height="`${windowHeight - 185}px`"
      highlight-hover-row
    >
      <template #wildcard_default="{row}">
        <div style="word-break: break-word">
          <span>{{ row.wildcard }}</span>
        </div>
      </template>
      <template #resourceTypeRender_default="{row}">
        {{
          resourceTypeList.filter((item) => item.id === row.resource_type_id)[0]
            ? resourceTypeList.filter((item) => item.id === row.resource_type_id)[0].name
            : 'unkown'
        }}
      </template>
      <template #users_default="{row}">
        <span
          v-for="(u, index) in row.users"
          :key="index"
        >{{ u }}<a-divider
          v-if="index < row.users.length - 1"
          type="vertical"
        /></span>
      </template>
      <template #permissions_default="{row}">
        <a-tag v-for="(p, index) in row.permissions" :key="index">{{ p }}</a-tag>
      </template>
      <template #enabled_default="{row}">
        <a-tag v-if="row.enabled" color="#2db7f5">{{ $t('acl.enable') }}</a-tag>
        <a-tag v-else color="grey">{{ $t('acl.disable') }}</a-tag>
      </template>
      <template #action_default="{row}">
        <a-space>
          <a-tooltip :title="$t('acl.apply')">
            <a @click="handleApplyTrigger(row)" :style="{ color: '#0f9d58' }"><a-icon type="appstore"/></a>
          </a-tooltip>
          <a-tooltip :title="$t('cancel')">
            <a @click="handleCancelTrigger(row)" :style="{ color: 'orange' }"><a-icon type="stop"/></a>
          </a-tooltip>
          <a-tooltip :title="$t('acl.viewMatchResult')">
            <a @click="handlePattern(row)" :style="{ color: 'purple' }"><a-icon type="eye"/></a>
          </a-tooltip>
          <a @click="handleEditTrigger(row)"><a-icon type="edit"/></a>
          <a @click="handleDeleteTrigger(row)" :style="{ color: 'red' }"><a-icon type="delete"/></a>
        </a-space>
      </template>
      <template slot="empty">
        <div>
          <img :style="{ width: '100px' }" :src="require('@/assets/data_empty.png')" />
          <div>{{ $t('noData') }}</div>
        </div>
      </template>
    </vxe-grid>
    <trigger-form
      ref="triggerForm"
      :roles="roles"
      :resourceTypeList="resourceTypeList"
      :id2perms="id2perms"
      @refresh="loadTriggers"
      :app_id="app_id"
    ></trigger-form>
    <TriggerPattern ref="triggerPattern" :roles="roles" />
  </div>
</template>
<script>
import { mapState } from 'vuex'
import TriggerForm from './module/triggerForm'
import TriggerPattern from './module/triggerPattern'
import { getTriggers, deleteTrigger, applyTrigger, cancelTrigger } from '@/modules/acl/api/trigger'
import { searchRole } from '@/modules/acl/api/role'
import { searchResourceType } from '@/modules/acl/api/resource'

export default {
  name: 'ACLTrigger',
  components: { TriggerForm, TriggerPattern },
  data() {
    return {
      roles: [],
      searchName: '',
      resourceTypeList: [],
      filterTriggers: [],
      triggers: [],
      id2parents: [],
      id2perms: {},
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    app_id() {
      return this.$route.name.split('_')[0]
    },
    tableColumns() {
      return [
        {
          title: this.$t('name'),
          field: 'name',
          sortable: true,
          minWidth: '150px',
          fixed: 'left',
          showOverflow: 'tooltip',
        },
        {
          title: this.$t('acl.resource'),
          field: 'wildcard',
          minWidth: '250px',
          showOverflow: 'tooltip',
          slots: {
            default: 'wildcard_default',
          },
        },
        {
          title: this.$t('acl.resourceType'),
          field: 'resource_type_id',
          minWidth: '120px',
          slots: {
            default: 'resourceTypeRender_default',
          },
        },
        {
          title: this.$t('acl.creator'),
          field: 'users',
          minWidth: '150px',
          showOverflow: 'tooltip',
          slots: {
            default: 'users_default',
          },
        },
        {
          title: this.$t('acl.allRole'),
          field: 'roles',
          minWidth: '150px',
          slots: {
            default: ({ row }) => {
              const roleNameList = row.roles.map((item) => {
                const temp = this.roles.find((a) => a.id === item)
                if (temp) {
                  return temp.name
                }
                return 'unknown'
              })
              return [
                <div>
                  {roleNameList.length <= 1 && roleNameList.map((item) => <span key={item}>{item}</span>)}
                  {roleNameList.length > 1 && (
                    <a-tooltip>
                      <template slot="title">
                        {roleNameList.map((item, idx) => (
                          <span>
                            <span key={item}>{item}</span>
                            {idx !== roleNameList.length - 1 && <a-divider type="vertical" />}
                          </span>
                        ))}
                      </template>
                      <span>{roleNameList[0]}...</span>
                    </a-tooltip>
                  )}
                </div>,
              ]
            },
          },
        },
        {
          title: this.$t('acl.permission'),
          field: 'permissions',
          minWidth: '250px',
          slots: {
            default: 'permissions_default',
          },
        },
        {
          title: this.$t('status'),
          field: 'enabled',
          minWidth: '100px',
          slots: {
            default: 'enabled_default',
          },
        },
        {
          title: this.$t('operation'),
          field: 'action',
          width: '120px',
          fixed: 'right',
          slots: {
            default: 'action_default',
          },
        },
      ]
    },
  },
  created() {
    this.loadRoles()
    this.loadResourceTypeList()
  },
  beforeMount() {
    this.loadTriggers()
  },
  methods: {
    loadTriggers() {
      this.searchName = ''
      getTriggers({ app_id: this.app_id }).then((res) => {
        this.triggers = res
        this.filterTriggers = res
      })
      // .catch(err => this.$httpError(err))
    },
    loadRoles() {
      searchRole({ app_id: this.app_id, page_size: 9999 }).then((res) => {
        this.roles = res.roles
        this.id2parents = res.id2parents
      })
      // .catch(err => this.$httpError(err))
    },
    loadResourceTypeList() {
      searchResourceType({ app_id: this.app_id, page_size: 9999 }).then((res) => {
        this.resourceTypeList = res['groups']
        this.id2perms = res['id2perms']
      })
      // .catch(err => this.$httpError(err))
    },
    handleCreateTrigger() {
      this.$refs.triggerForm.handleEdit(null)
    },
    handleDeleteTrigger(record) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('acl.confirmDeleteTrigger'),
        onOk() {
          deleteTrigger(record.id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadTriggers()
          })
          // .catch(err => that.$httpError(err))
        },
      })
    },
    handleApplyTrigger(record) {
      const that = this
      this.$confirm({
        title: that.$t('acl.ruleApply'),
        content: that.$t('acl.triggerTip1'),
        onOk() {
          applyTrigger(record.id).then((res) => {
            that.$message.success(that.$t('operateSuccess'))
          })
          // .catch(err => that.$httpError(err))
        },
      })
    },
    handleCancelTrigger(record) {
      const that = this
      this.$confirm({
        title: that.$t('acl.ruleApply'),
        content: that.$t('acl.triggerTip2'),
        onOk() {
          cancelTrigger(record.id).then((res) => {
            that.$message.success(that.$t('operateSuccess'))
          })
          // .catch(err => that.$httpError(err))
        },
      })
    },
    handleEditTrigger(record) {
      this.$refs.triggerForm.handleEdit(record)
    },
    filter() {
      if (this.searchName) {
        this.filterTriggers = this.triggers.filter((item) =>
          item.name.toLowerCase().includes(this.searchName.toLowerCase())
        )
      } else {
        this.filterTriggers = this.triggers
      }
    },
    handlePattern(row) {
      const { wildcard, uid, resource_type_id } = row
      this.$refs.triggerPattern.open({
        resource_type_id,
        app_id: this.app_id,
        owner: uid,
        pattern: wildcard,
      })
    },
  },
  watch: {
    '$route.name': function(oldName, newName) {
      this.loadTriggers()
    },
    searchName: {
      immediate: true,
      handler(newVal) {
        if (!newVal) {
          this.filter()
        }
      },
    },
  },
}
</script>
<style lang="less" scoped>
.acl-trigger {
  border-radius: 15px;
  background-color: #fff;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 24px;
  .acl-trigger-header {
    width: 100%;
    display: inline-flex;
    margin-bottom: 15px;
    align-items: center;
  }
}
</style>
