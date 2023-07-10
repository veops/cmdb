<template>
  <div class="user-wrapper">
    <div class="content-box">
      <!-- <document-link /> -->
      <span
        v-if="hasBackendPermission"
        @click="handleClick"
        class="action"
        style="width: 40px; display: flex; justify-content: center"
      >
        <a-icon type="setting" />
      </span>
      <a-popover
        trigger="click"
        :overlayStyle="{ width: '120px' }"
        placement="bottomRight"
        overlayClassName="custom-user"
      >
        <template slot="content">
          <router-link :to="{ name: 'setting_person' }" :style="{ color: '#000000a6' }">
            <div class="custom-user-item">
              <a-icon type="user" :style="{ marginRight: '10px' }" />
              <span>个人中心</span>
            </div>
          </router-link>
          <div @click="handleLogout" class="custom-user-item">
            <a-icon type="logout" :style="{ marginRight: '10px' }" />
            <span>退出登录</span>
          </div>
        </template>
        <span class="action ant-dropdown-link user-dropdown-menu">
          <a-avatar
            v-if="avatar()"
            class="avatar"
            size="small"
            :src="avatar().startsWith('https') ? avatar() : `/api/common-setting/v1/file/${avatar()}`"
          />
          <a-avatar v-else class="avatar" size="small" icon="user" />
          <span>{{ nickname() }}</span>
        </span>
      </a-popover>
    </div>
  </div>
</template>

<script>
import DocumentLink from './DocumentLink.vue'
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: 'UserMenu',
  components: {
    DocumentLink,
  },
  computed: {
    ...mapState(['user']),
    hasBackendPermission() {
      return this.user?.roles?.permissions.includes('acl_admin', 'backend_admin') || false
    },
  },
  methods: {
    ...mapActions(['Logout']),
    ...mapGetters(['nickname', 'avatar']),
    handleLogout() {
      const that = this

      this.$confirm({
        title: '提示',
        content: '真的要注销登录吗 ?',
        onOk() {
          // localStorage.removeItem('ops_cityps_currentId')
          localStorage.clear()
          return that.Logout()
        },
        onCancel() {},
      })
    },
    handleClick() {
      this.$router.push('/setting')
    },
  },
}
</script>
<style lang="less">
@import '~@/style/static.less';
.color {
  color: #custom_colors[color_1];
  background-color: #custom_colors[color_2];
}
.custom-user {
  .custom-user-item {
    cursor: pointer;
    padding: 5px 10px;
    &:hover {
      .color() !important;
    }
  }
  .ant-popover-inner-content {
    padding: 0;
    color: #000000a6;
  }
}
</style>
