<template>
  <CustomDrawer
    :title="drawerTitle"
    :visible="drawerVisible"
    width="80%"
    placement="left"
    @close="() => (drawerVisible = false)"
    :hasFooter="false"
  >
    <vxe-table :max-height="`${windowHeight - 150}px`" :data="resPerms" ref="rTable">
      <vxe-column
        field="name"
        title="角色名"
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
              placeholder="按回车确认筛选"
            />
          </template>
        </template>
      </vxe-column>
      <vxe-column field="users" title="下属用户" width="35%">
        <template #default="{row}">
          <a-tag color="green" v-for="user in row.users" :key="user.nickname">
            {{ user.nickname }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="perms" title="权限列表" width="35%">
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
      <vxe-column field="operate" title="批量操作">
        <template #default="{row}">
          <a-button size="small" type="danger" @click="handleClearAll(row)">
            清空
          </a-button>
        </template>
      </vxe-column>
    </vxe-table>
    <!-- <a-table
      :columns="columns"
      :dataSource="resPerms"
      :rowKey="record => record.name"
      :pagination="{ showTotal: (total, range) => `${range[0]}-${range[1]} 共 ${total} 条记录` }"
      showPagination="auto"
      ref="rTable"
      size="middle"
    >
      <div slot="perms" slot-scope="text">
        <a-tag closable color="cyan" v-for="perm in text" :key="perm.name" @close="deletePerm(perm.rid, perm.name)">
          {{ perm.name }}
        </a-tag>
      </div>
      <div slot="users" slot-scope="text">
        <a-tag color="green" v-for="user in text" :key="user.nickname">
          {{ user.nickname }}
        </a-tag>
      </div>
      <div slot="operate" slot-scope="text">
        <a-button size="small" type="danger" @click="handleClearAll(text)">
          清空
        </a-button>
      </div>
    </a-table> -->
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
      drawerTitle: '权限列表',
      drawerVisible: false,
      record: null,
      allPerms: [],
      resPerms: [],
      roleID: null,
      // columns: [
      //   {
      //     title: '角色名',
      //     dataIndex: 'name',
      //     sorter: false,
      //     width: 50,
      //   },
      //   {
      //     title: '下属用户',
      //     dataIndex: 'users',
      //     sorter: false,
      //     width: 150,
      //     scopedSlots: { customRender: 'users' },
      //   },
      //   {
      //     title: '权限列表',
      //     dataIndex: 'perms',
      //     sorter: false,
      //     width: 150,
      //     scopedSlots: { customRender: 'perms' },
      //   },
      //   {
      //     title: '批量操作',
      //     sorter: false,
      //     width: 50,
      //     scopedSlots: { customRender: 'operate' },
      //   },
      // ],
      childrenDrawer: false,
      allRoles: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
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
          this.$message.success('删除成功')
          this.$nextTick(() => {
            this.getResPerms(this.record.id)
          })
        })
      } else {
        deleteRoleResourcePerm(text.perms[0].rid, this.record.id, {
          perms: [],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success('删除成功')
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
          this.$message.success(`删除成功`)
        })
        // .catch(err => this.requestFailed(err))
      } else {
        deleteRoleResourceGroupPerm(roleID, this.record.id, {
          perms: [permName],
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.$message.success(`删除成功`)
        })
        // .catch(err => this.requestFailed(err))
      }
    },
    handleCancel(e) {
      this.drawerVisible = false
    },
    // requestFailed(err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
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
