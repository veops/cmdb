<template>
  <div>
    <a-card title="应用管理" class="acl-app-wrapper" :style="{ '--ant-body-height': `${windowHeight - 150}px` }">
      <a-row :guttr="24">
        <a-col v-for="app in apps" :key="app.id" :span="8">
          <div style="margin: 15px">
            <a-card class="acl-app-single-card">
              <a-card-meta :title="app.name">
                <div slot="description" :title="app.description || ''">{{ app.description || '无' }}</div>
                <a-avatar style="background-color: #5dc2f1" slot="avatar">{{ app.name[0].toUpperCase() }}</a-avatar>
              </a-card-meta>
              <template class="ant-card-actions" slot="actions">
                <a-icon type="edit" @click="handleEditApp(app)" />
                <a-icon type="delete" @click="handleDeleteApp(app)" />
              </template>
            </a-card>
          </div>
        </a-col>
        <a-col :span="8">
          <div class="acl-app-add" @click="handleCreateApp">
            <span class="acl-app-add-icon" style="">+</span>
          </div>
        </a-col>
      </a-row>
    </a-card>
    <app-form ref="appForm" @refresh="loadApps"></app-form>
  </div>
</template>
<script>
/* eslint-disable */
import { mapState } from 'vuex'
import { searchApp, addApp, updateApp, deleteApp } from '@/modules/acl/api/app'
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
.acl-app-wrapper {
  > .ant-card-body {
    overflow-y: auto;
    height: var(--ant-body-height);
    cursor: default;
  }
  .acl-app-single-card {
    .ant-card-meta-description > div {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    &:hover {
      box-shadow: 0 2px 8px #0000004d;
    }
  }
  .acl-app-add {
    height: 141px;
    margin: 15px;
    border: 1px #e8e8e8 solid;
    transition: all 0.3s;
    &:hover {
      box-shadow: 0 2px 8px #0000004d;
    }
    .acl-app-add-icon {
      font-size: 70px;
      display: block;
      text-align: center;
      color: #5dc2f1;
      cursor: pointer;
    }
  }
}
</style>
