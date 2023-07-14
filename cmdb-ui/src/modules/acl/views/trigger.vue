<template>
  <div :style="{ backgroundColor: '#fff', padding: '24px' }">
    <div class="trigger-action-btn">
      <a-button type="primary" @click="handleCreateTrigger">新增触发器</a-button>
      <a-input-search
        class="ops-input"
        :style="{ display: 'inline', marginLeft: '10px', width: '200px' }"
        placeholder="搜索 | 名称"
        v-model="searchName"
        allowClear
        @search="filter"
      ></a-input-search>
    </div>

    <vxe-grid
      stripe
      size="mini"
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
        <a-tag v-if="row.enabled" color="#2db7f5">启用</a-tag>
        <a-tag v-else color="grey">禁用</a-tag>
      </template>
      <template #action_default="{row}">
        <a-space>
          <a-tooltip title="应用">
            <a @click="handleApplyTrigger(row)" :style="{ color: '#0f9d58' }"><a-icon type="appstore"/></a>
          </a-tooltip>
          <a-tooltip title="取消">
            <a @click="handleCancelTrigger(row)" :style="{ color: 'orange' }"><a-icon type="stop"/></a>
          </a-tooltip>
          <a-tooltip title="查看正则匹配结果">
            <a @click="handlePattern(row)" :style="{ color: 'purple' }"><a-icon type="eye"/></a>
          </a-tooltip>
          <a @click="handleEditTrigger(row)"><a-icon type="edit"/></a>
          <a @click="handleDeleteTrigger(row)" :style="{ color: 'red' }"><a-icon type="delete"/></a>
        </a-space>
      </template>
      <template slot="empty">
        <img :src="require(`@/assets/data_empty.png`)" />
        <p style="font-size: 14px; line-height: 17px; color: rgba(0, 0, 0, 0.6)">暂无数据</p>
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
      tableColumns: [
        {
          title: '名称',
          field: 'name',
          sortable: true,
          minWidth: '150px',
          fixed: 'left',
          showOverflow: 'tooltip',
        },
        {
          title: '资源名',
          field: 'wildcard',
          minWidth: '250px',
          showOverflow: 'tooltip',
          slots: {
            default: 'wildcard_default',
          },
        },
        {
          title: '资源类型',
          field: 'resource_type_id',
          minWidth: '100px',
          slots: {
            default: 'resourceTypeRender_default',
          },
        },
        {
          title: '创建人',
          field: 'users',
          minWidth: '150px',
          showOverflow: 'tooltip',
          slots: {
            default: 'users_default',
          },
        },
        {
          title: '角色',
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
          title: '权限',
          field: 'permissions',
          minWidth: '250px',
          slots: {
            default: 'permissions_default',
          },
        },
        {
          title: '状态',
          field: 'enabled',
          minWidth: '100px',
          slots: {
            default: 'enabled_default',
          },
        },
        {
          title: '操作',
          field: 'action',
          minWidth: '200px',
          fixed: 'right',
          slots: {
            default: 'action_default',
          },
        },
      ],
    }
  },
  created() {
    this.loadRoles()
    this.loadResourceTypeList()
  },
  beforeMount() {
    this.loadTriggers()
  },

  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    app_id() {
      return this.$route.name.split('_')[0]
    },
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
        title: '删除',
        content: '确认删除该触发器吗？',
        onOk() {
          deleteTrigger(record.id).then((res) => {
            that.$message.success('删除成功')
            that.loadTriggers()
          })
          // .catch(err => that.$httpError(err))
        },
      })
    },
    handleApplyTrigger(record) {
      const that = this
      this.$confirm({
        title: '规则应用',
        content: '是否确定应用该触发器？',
        onOk() {
          applyTrigger(record.id).then((res) => {
            that.$message.success('提交成功!')
          })
          // .catch(err => that.$httpError(err))
        },
      })
    },
    handleCancelTrigger(record) {
      const that = this
      this.$confirm({
        title: '规则应用',
        content: '是否取消应用该触发器?',
        onOk() {
          cancelTrigger(record.id).then((res) => {
            that.$message.success('提交成功！')
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
.trigger-action-btn {
  width: 100%;
  display: inline-flex;
  margin-bottom: 15px;
  align-items: center;
}
</style>
