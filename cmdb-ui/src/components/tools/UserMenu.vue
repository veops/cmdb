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
      <span class="locale" @click="changeLang">{{ locale === 'zh' ? 'English' : '中文' }}</span>
      <a-popover
        trigger="click"
        :overlayStyle="{ width: '150px' }"
        placement="bottomRight"
        overlayClassName="custom-user"
      >
        <template slot="content">
          <router-link :to="{ name: 'setting_person' }" :style="{ color: '#000000a6' }">
            <div class="custom-user-item">
              <a-icon type="user" :style="{ marginRight: '10px' }" />
              <span>{{ $t('topMenu.personalCenter') }}</span>
            </div>
          </router-link>
          <div @click="handleLogout" class="custom-user-item">
            <a-icon type="logout" :style="{ marginRight: '10px' }" />
            <span>{{ $t('topMenu.logout') }}</span>
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
import { mapState, mapActions, mapGetters, mapMutations } from 'vuex'
import DocumentLink from './DocumentLink.vue'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'

export default {
  name: 'UserMenu',
  components: {
    DocumentLink,
  },
  computed: {
    ...mapState(['user', 'locale']),
    hasBackendPermission() {
      return this.user?.detailPermissions?.backend?.length
    },
  },
  methods: {
    ...mapActions(['Logout']),
    ...mapGetters(['nickname', 'avatar']),
    ...mapMutations(['SET_LOCALE']),
    handleLogout() {
      const that = this

      this.$confirm({
        title: this.$t('tip'),
        content: this.$t('topMenu.confirmLogout'),
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
    changeLang() {
      if (this.locale === 'zh') {
        this.SET_LOCALE('en')
        this.$i18n.locale = 'en'
      } else {
        this.SET_LOCALE('zh')
        this.$i18n.locale = 'zh'
      }
      this.$nextTick(() => {
        setDocumentTitle(`${this.$t(this.$route.meta.title)} - ${domTitle}`)
      })
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

.locale {
  cursor: pointer;
  &:hover {
    color: #custom_colors[color_1];
  }
}
</style>
