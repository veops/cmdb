<template>
  <CustomDrawer
    :title="drawerTitle"
    :visible="drawerVisible"
    width="80%"
    placement="left"
    @close="() => (drawerVisible = false)"
    :hasFooter="false"
  >
    <vxe-table
      stripe
      size="mini"
      class="ops-stripe-table"
      :max-height="`${windowHeight - 150}px`"
      :data="resPerms"
      ref="rTable"
    >
      <vxe-column
        field="name"
        :title="$t('acl.role')"
        width="20%"
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
      <vxe-column field="users" :title="$t('acl.subordinateUsers')" width="35%">
        <template #default="{row}">
          <a-tag color="green" v-for="user in row.users" :key="user.nickname">
            {{ user.nickname }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="perms" :title="$t('acl.permissionList')" width="35%">
        <template #default="{row}">
          <a-tag
            closable
            color="cyan"
            v-for="perm in row.perms"
            :key="perm.name"
            @close="deletePerm(perm.rid, perm.name)"
          >
            {{ perm.name }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="operate" :title="$t('acl.batchOperate')">
        <template #default="{row}">
          <a-button size="small" type="danger" @click="handleClearAll(row)">
            {{ $t('clear') }}
          </a-button>
        </template>
      </vxe-column>
      <template slot="empty">
        <img :src="require(`@/assets/data_empty.png`)" />
        <p style="font-size: 14px; line-height: 17px; color: rgba(0, 0, 0, 0.6)">{{ $t('noData') }}</p>
      </template>
    </vxe-table>
  </CustomDrawer>
</template>
<script>
import { mapState } from 'vuex'
import {
  getResourceTypePerms,
  getResourcePerms,
  deleteRoleResourcePerm,
  getResourceGroupPerms,
  deleteRoleResourceGroupPerm,
  deleteRoleResourceGroupPerm2,
} from '@/modules/acl/api/permission'

export default {
  name: 'ResourceForm',
  data() {
    return {
      isGroup: false,
      drawerVisible: false,
      record: null,
      allPerms: [],
      resPerms: [],
      roleID: null,
      childrenDrawer: false,
      allRoles: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    drawerTitle() {
      return this.$t('acl.permissionList')
    }
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handlePerm(record, isGroup) {
      this.isGroup = isGroup
      this.drawerVisible = true
      this.record = record
      this.getResPerms(record.id)

      this.$nextTick(() => {
        this.getAllPerms(record.resource_type_id)
      })
    },
    handleClearAll(text) {
      if (this.isGroup) {
        deleteRoleResourceGroupPerm2(text.perms[0].rid, this.record.id, {
          perms: [],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success(this.$t('deleteSuccess'))
          this.$nextTick(() => {
            this.getResPerms(this.record.id)
          })
        })
      } else {
        deleteRoleResourcePerm(text.perms[0].rid, this.record.id, {
          perms: [],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success(this.$t('deleteSuccess'))
          // for (let i = 0; i < this.resPerms.length; i++) {
          //   if (this.resPerms[i].name === text.name) {
          //     this.resPerms[i].perms = []
          //   }
          // }
          this.$nextTick(() => {
            this.getResPerms(this.record.id)
          })
        })
      }
    },
    getResPerms(resId) {
      if (!this.isGroup) {
        getResourcePerms(resId).then((res) => {
          const perms = []
          for (const key in res) {
            perms.push({ name: key, perms: res[key].perms, users: res[key].users })
          }
          this.resPerms = perms
        })
      } else {
        getResourceGroupPerms(resId).then((res) => {
          const perms = []
          for (const key in res) {
            perms.push({ name: key, perms: res[key].perms, users: res[key].users })
          }
          this.resPerms = perms
        })
      }
    },
    getAllPerms(resTypeId) {
      getResourceTypePerms(resTypeId).then((res) => {
        this.allPerms = res
      })
    },
    deletePerm(roleID, permName) {
      if (!this.isGroup) {
        deleteRoleResourcePerm(roleID, this.record.id, {
          perms: [permName],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success(this.$t('deleteSuccess'))
        })
        // .catch(err => this.requestFailed(err))
      } else {
        deleteRoleResourceGroupPerm(roleID, this.record.id, {
          perms: [permName],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success(this.$t('deleteSuccess'))
        })
      }
    },
    handleCancel(e) {
      this.drawerVisible = false
    },
    filterNameMethod({ option, row }) {
      return row.name.toLowerCase().includes(option.data.toLowerCase())
    },
    filterNameRecoverMethod({ option }) {
      option.data = ''
    },
  },
  watch: {},
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

@media screen and (max-width: 900px) {
  .fold {
    width: 100%;
  }
}
</style>
