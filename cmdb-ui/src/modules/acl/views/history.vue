<template>
  <div class="acl-history">
    <a-tabs default-active-key="1">
      <a-tab-pane key="1" :tab="$t('acl.permissionChange')">
        <permisson-history-table
          v-if="isloaded"
          :allResourceTypes="allResourceTypes"
          :allResources="allResources"
          :allUsers="allUsers"
          :allRoles="allRoles"
          :allRolesMap="allRolesMap"
          :allUsersMap="allUsersMap"
          :allResourceTypesMap="allResourceTypesMap"
          @loadMoreResources="loadMoreResources"
          @reloadResources="reloadResources"
          @fetchResources="fetchResources"
          @resourceClear="resourceClear"
        ></permisson-history-table>
      </a-tab-pane>
      <a-tab-pane key="2" :tab="$t('acl.roleChange')">
        <role-history-table
          v-if="isloaded"
          :allUsers="allUsers"
          :allRoles="allRoles"
          :allRolesMap="allRolesMap"
          :allUsersMap="allUsersMap"
        ></role-history-table>
      </a-tab-pane>
      <a-tab-pane key="3" :tab="$t('acl.resourceChange')">
        <resource-history-table
          v-if="isloaded"
          :allResources="allResources"
          :allUsers="allUsers"
          :allRoles="allRoles"
          :allRolesMap="allRolesMap"
          :allUsersMap="allUsersMap"
          :allResourcesMap="allResourcesMap"
          @loadMoreResources="loadMoreResources"
          @reloadResources="reloadResources"
          @fetchResources="fetchResources"
          @resourceClear="resourceClear"
        ></resource-history-table>
      </a-tab-pane>
      <a-tab-pane key="4" :tab="$t('acl.resourceTypeChange')">
        <resource-type-history-table
          v-if="isloaded"
          :allResourceTypes="allResourceTypes"
          :allUsers="allUsers"
          :allRoles="allRoles"
          :allRolesMap="allRolesMap"
          :allUsersMap="allUsersMap"
          :allResourceTypesMap="allResourceTypesMap"
        ></resource-type-history-table>
      </a-tab-pane>
      <a-tab-pane key="5" :tab="$t('acl.triggerChange')">
        <trigger-history-table
          v-if="isloaded"
          :allTriggers="allTriggers"
          :allUsers="allUsers"
          :allRoles="allRoles"
          :allRolesMap="allRolesMap"
          :allUsersMap="allUsersMap"
          :allTriggersMap="allTriggersMap"
          :allResourceTypesMap="allResourceTypesMap"
        ></trigger-history-table>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import permissonHistoryTable from './module/permissionHistoryTable.vue'
import roleHistoryTable from './module/roleHistoryTable.vue'
import resourceHistoryTable from './module/resourceHistoryTable.vue'
import triggerHistoryTable from './module/triggerHistoryTable.vue'
import resourceTypeHistoryTable from './module/resourceTypeHistoryTable.vue'
import { getTriggers } from '@/modules/acl/api/trigger'
import { searchRole } from '@/modules/acl/api/role'
import { searchUser } from '@/modules/acl/api/user'
import { searchResource, searchResourceType } from '@/modules/acl/api/resource'
export default {
  components: {
    permissonHistoryTable,
    roleHistoryTable,
    resourceHistoryTable,
    triggerHistoryTable,
    resourceTypeHistoryTable,
  },
  data() {
    return {
      app_id: this.$route.name.split('_')[0],
      isloaded: false,
      resourcesNum: 0,
      resourcesPage: 1,
      allResourceTypes: [],
      allResources: [],
      allUsers: [],
      allRoles: [],
      allTriggers: [],
      allRolesMap: new Map(),
      allUsersMap: new Map(),
      allResourceTypesMap: new Map(),
      allResourcesMap: new Map(),
      allTriggersMap: new Map(),
    }
  },
  async created() {
    await this.initData()
    this.isloaded = true
  },
  watch: {
    '$route.name': async function(oldName, newName) {
      try {
        this.isloaded = false
        this.app_id = this.$route.name.split('_')[0]
        this.allResources = []
        this.resourcesPage = 1
        await this.initData()
      } finally {
        this.isloaded = true
      }
    },
  },
  methods: {
    async initData() {
      await Promise.all([
        this.getAllRoles(),
        this.getAllUsers(),
        this.getAllResourceTypes(),
        this.getAllResources(1),
        this.getTriggers(),
      ])
    },
    async getAllRoles() {
      const { roles } = await searchRole({ app_id: this.app_id, page_size: 9999 })
      const allRoles = []
      const allRolesMap = new Map()
      roles.forEach((item) => {
        allRoles.push({ [item.name]: item.id })
        allRolesMap.set(item.id, item.name)
      })
      this.allRoles = allRoles
      this.allRolesMap = allRolesMap
    },
    async getAllUsers() {
      const { users } = await searchUser({ page_size: 10000 })
      const allUsers = []
      const allUsersMap = new Map()
      users.forEach((item) => {
        allUsers.push({ [item.nickname]: item.uid })
        allUsersMap.set(item.uid, item.nickname)
      })
      this.allUsers = allUsers
      this.allUsersMap = allUsersMap
    },
    async getAllResourceTypes() {
      const { groups } = await searchResourceType({ app_id: this.app_id, page_size: 9999, page: 1 })
      const allResourceTypes = []
      const allResourceTypesMap = new Map()
      groups.forEach((item) => {
        allResourceTypes.push({ [item.name]: item.id })
        allResourceTypesMap.set(item.id, item.name)
      })
      this.allResourceTypes = allResourceTypes
      this.allResourceTypesMap = allResourceTypesMap
    },
    async getAllResources(page = 1, value = undefined) {
      const { resources, numfound } = await searchResource({
        page: page,
        page_size: 50,
        app_id: this.app_id,
        q: value,
      })
      this.resourcesNum = numfound
      const allResources = this.allResources
      const allResourcesMap = this.allResourcesMap
      resources.forEach((item) => {
        allResources.push({ [item.name]: item.id })
        allResourcesMap.set(item.id, item.name)
      })
      this.allResources = allResources
      this.allResourcesMap = allResourcesMap
    },
    reloadResources() {
      this.resourcesPage = 1
      this.allResources = []
      this.allResourcesMap = new Map()
      this.getAllResources()
    },
    loadMoreResources(value) {
      if (this.allResources.length < this.resourcesNum) {
        let currentPage = this.resourcesPage
        this.getAllResources(++currentPage, value)
        this.resourcesPage = currentPage
      }
    },
    resourceClear() {
      this.resourcesPage = 1
      this.allResources = []
      this.getAllResources()
    },
    async fetchResources(value) {
      const allResources = []
      const allResourcesMap = new Map()
      const { resources, numfound } = await searchResource({
        page: 1,
        page_size: 50,
        app_id: this.app_id,
        q: value,
      })
      this.resourcesNum = numfound
      this.resourcesPage = 1
      resources.forEach((item) => {
        allResources.push({ [item.name]: item.id })
        allResourcesMap.set(item.id, item.name)
      })
      this.allResources = allResources
      this.allResourcesMap = allResourcesMap
    },
    async getTriggers() {
      const res = await getTriggers({ app_id: this.app_id })
      const allTriggers = []
      const allTriggersMap = new Map()
      res.forEach((item) => {
        allTriggers.push({ [item.name]: item.id })
        allTriggersMap.set(item.id, item.name)
      })
      this.allTriggers = allTriggers
      this.allTriggersMap = allTriggersMap
    },
  },
}
</script>

<style lang="less" scoped>

.acl-history {
  border-radius: @border-radius-box;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 24px;
  background-color: #fff;
}
</style>
