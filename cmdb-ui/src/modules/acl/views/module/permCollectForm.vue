<template>
  <CustomDrawer
    :title="`${$t('acl.summaryPermissions')}: ${user.nickname}`"
    :visible="visible"
    placement="left"
    width="100%"
    @close="visible = false"
    :hasFooter="false"
  >
    <a-tabs @change="handleSwitchApp">
      <a-tab-pane
        v-for="app in displayApps"
        :key="app.id"
        :tab="app.name.slice(0, 1).toUpperCase() + app.name.slice(1)"
      >
        <a-tabs
          v-if="resourceTypes && resourceTypes.length"
          :animated="false"
          v-model="currentResourceId"
          @change="loadResource()"
        >
          <a-tab-pane v-for="rType in resourceTypes" :key="rType.id" :tab="rType.name">
            <a-spin :spinning="spinning">
              <vxe-table :max-height="`${windowHeight - 230}px`" :data="resources" ref="rTable">
                <vxe-column
                  field="name"
                  :title="$t('acl.resourceName')"
                  width="30%"
                  :filters="[{ data: '' }]"
                  :filter-method="filterNameMethod"
                  :filter-recover-method="filterNameRecoverMethod"
                >
                  <template #filter="{ $panel, column }">
                    <template v-for="(option, index) in column.filters">
                      <input
                        class="my-input"
                        type="type"
                        :key="index"
                        v-model="option.data"
                        @input="$panel.changeOption($event, !!option.data, option)"
                        @keyup.enter="$panel.confirmFilter()"
                        :placeholder="$t('acl.pressEnter')"
                      />
                    </template>
                  </template>
                </vxe-column>
                <vxe-column field="permissions" :title="$t('acl.permissionList')" width="70%">
                  <template #default="{row}">
                    <a-tag color="cyan" v-for="(r, index) in row.permissions" :key="index">{{ r }}</a-tag>
                  </template>
                </vxe-column>
              </vxe-table>
            </a-spin>
          </a-tab-pane>
        </a-tabs>
      </a-tab-pane>
    </a-tabs>
  </CustomDrawer>
</template>
<script>
import { mapState } from 'vuex'
import { searchApp, searchRole } from '@/modules/acl/api/app'
import { searchResourceType } from '@/modules/acl/api/resource'
import { searchPermResourceByRoleId } from '@/modules/acl/api/permission'

export default {
  name: 'PermCollectForm',
  data() {
    return {
      spinning: false,
      visible: false,
      user: {},
      roles: [],
      apps: [],
      currentAppId: 0,
      currentResourceId: 0,
      resourceTypes: [],
      resourceTypePerms: [],
      resources: [],
      columnSearchText: {
        name: '',
      },
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    displayApps() {
      const roles = this.$store.state.user.roles.permissions
      if (roles.includes('acl_admin')) {
        return this.apps
      }
      return this.apps.filter((item) => {
        if (roles.includes(`${item.name}_admin`)) {
          return true
        }
        return false
      })
    },
  },
  async mounted() {
    await this.loadApps()
  },
  methods: {
    collect(user) {
      this.user = user
      this.visible = true
      setTimeout(() => {
        this.loadResource()
      }, 500)
    },
    handleSearch(selectedKeys, confirm, column) {
      confirm()
      this.columnSearchText[column.dataIndex] = selectedKeys[0]
    },
    handleReset(clearFilters, column) {
      clearFilters()
      this.columnSearchText[column.dataIndex] = ''
    },
    async loadRoles(_appId) {
      const res = await searchRole({ app_id: _appId, page_size: 9999, is_all: true })
      this.roles = res.roles.filter((item) => item.uid)
    },
    async handleSwitchApp(appId) {
      this.currentAppId = appId
      await this.loadResourceTypes(appId)
    },
    async loadApps() {
      const res = await searchApp()
      this.apps = res.apps
      if (this.displayApps[0]) {
        this.currentAppId = this.displayApps[0].id
        await this.loadRoles(this.apps[0].id)
        await this.loadResourceTypes(this.displayApps[0].id)
      } else {
        this.$message.info('No apps!')
      }
    },
    async loadResourceTypes(appId) {
      const res = await searchResourceType({ app_id: appId, page_size: 9999 })
      this.resourceTypes = res['groups']
      this.resourceTypePerms = res['id2perms'][`${appId}`]
      this.currentResourceId = res['groups'][0] && res['groups'][0]['id']
      await this.loadResource()
    },
    async loadResource() {
      this.spinning = true
      const fil = this.roles.filter((role) => role.uid === this.user.uid)
      if (!fil[0]) {
        return
      }
      const res = await searchPermResourceByRoleId(fil[0].id, {
        resource_type_id: this.currentResourceId,
        app_id: this.currentAppId,
      })
      this.resources = res['resources']
      this.spinning = false
    },
    filterNameMethod({ option, row }) {
      return row.name.toLowerCase().includes(option.data.toLowerCase())
    },
    filterNameRecoverMethod({ option }) {
      option.data = ''
    },
  },
}
</script>
<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}

.fold {
  width: calc(100% - 216px);
  display: inline-block;
}

.operator {
  margin-bottom: 18px;
}
.action-btn {
  margin-bottom: 1rem;
}
.custom-filter-dropdown {
  padding: 8px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0;
}
</style>
