<template>
  <div class="acl-apps">
    <a-row :gutter="[24, 24]">
      <a-col
        v-for="app in apps"
        :key="app.id"
        :xxl="4"
        :xl="6"
        :md="8"
        :sm="12"
        :xs="24">
        <a-card>
          <a-card-meta :title="app.name">
            <div slot="description" :title="app.description || ''">{{ app.description || '无' }}</div>
            <a-avatar style="background-color: #5dc2f1" slot="avatar">{{ app.name[0].toUpperCase() }}</a-avatar>
          </a-card-meta>
          <template slot="actions">
            <a-icon type="edit" @click="handleEditApp(app)" />
            <a-icon type="delete" @click="handleDeleteApp(app)" />
          </template>
        </a-card>
      </a-col>
      <a-col :xxl="4" :xl="6" :md="8" :sm="12" :xs="24">
        <div class="acl-apps-add" @click="handleCreateApp">
          <span class="acl-apps-add-icon">+</span>
        </div>
      </a-col>
    </a-row>
    <app-form ref="appForm" @refresh="loadApps"></app-form>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import { searchApp, deleteApp } from '@/modules/acl/api/app'
import AppForm from './module/appForm'

export default {
  name: 'AclApps',
  data() {
    return {
      apps: [],
      selected: null,
      modalVisible: false,
      allUsers: [],
      permissionRoles: [],
    }
  },
  computed: mapState({
    windowHeight: (state) => state.windowHeight,
  }),
  components: { AppForm },
  mounted() {
    this.loadApps()
  },
  methods: {
    loadApps() {
      searchApp().then((res) => {
        this.apps = res.apps
      })
    },
    handleCreateApp() {
      this.selected = null
      this.$refs.appForm.handleEdit()
    },
    handleDeleteApp(app) {
      const that = this
      this.$confirm({
        title: '危险操作',
        content: '确定要删除该App吗？',
        onOk() {
          deleteApp(app.id).then((res) => {
            that.$message.success(`删除成功：${app.name}`)
            that.loadApps()
          })
        },
      })
    },
    handleEditApp(app) {
      this.$nextTick(() => {
        this.$refs.appForm.handleEdit(app)
      })
    },
  },
}
</script>

<style lang="less">
.acl-apps {
  .ant-card-meta-description > div {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .acl-apps-add {
    width: 100%;
    height: 141px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border: 1px #e8e8e8 solid;
    background-color: #fff;
    .acl-apps-add-icon {
      font-size: 70px;
      display: block;
      text-align: center;
      color: #5dc2f1;
      cursor: pointer;
    }
  }
}
</style>
