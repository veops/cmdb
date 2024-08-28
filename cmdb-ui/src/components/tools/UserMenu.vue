<template>
  <div class="user-wrapper">
    <div class="content-box">
      <!-- <document-link /> -->
      <span
        v-if="hasBackendPermission"
        @click="handleClick"
        class="common-settings-btn"
      >
        <ops-icon class="common-settings-btn-icon" type="veops-setting" />
        <span class="common-settings-btn-text">{{ $t('settings') }}</span>
      </span>
      <a-popover
        overlayClassName="lang-popover-wrap"
        placement="bottomRight"
        :getPopupContainer="(trigger) => trigger.parentNode"
      >
        <span class="locale">{{ languageList.find((lang) => lang.key === locale).title }}</span>
        <div class="lang-menu" slot="content">
          <a
            v-for="(lang) in languageList"
            :key="lang.key"
            :class="['lang-menu-item', lang.key === locale ? 'lang-menu-item_active' : '']"
            @click="changeLang(lang.key)"
          >
            {{ lang.title }}
          </a>
        </div>
      </a-popover>
      <a-popover
        :overlayStyle="{ width: '130px' }"
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
        <span class="action ant-dropdown-link user-dropdown-menu user-info-wrap">
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
  data() {
    return {
      languageList: [
        {
          title: '简中',
          key: 'zh'
        },
        {
          title: 'EN',
          key: 'en'
        },
      ]
    }
  },
  computed: {
    ...mapState(['user', 'locale']),
    hasBackendPermission() {
      const isAdmin = this?.user?.roles?.permissions?.includes('acl_admin')

      return isAdmin || this.user?.detailPermissions?.backend?.length
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
          return that.Logout()
        },
        onCancel() {},
      })
    },
    handleClick() {
      this.$router.push('/setting')
    },
    changeLang(lang) {
      this.SET_LOCALE(lang)
      this.$i18n.locale = lang
      this.$nextTick(() => {
        setDocumentTitle(`${this.$t(this.$route.meta.title)} - ${domTitle}`)
      })
    },
  },
}
</script>

<style lang="less">
.color {
  color: @primary-color;
  background-color: @primary-color_5;
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
  padding: 0 8px;

  &:hover {
    color: @primary-color;
  }
}

.lang-popover-wrap {
  width: 70px;
  padding: 0px;

  .ant-popover-inner-content {
    padding: 0px;
  }
}
</style>

<style lang="less" scoped>
.user-wrapper {
  .common-settings-btn {
    cursor: pointer;
    padding: 0px 18px;
    background-color: #F0F5FF;
    border-radius: 22px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 8px;

    &-icon {
      font-size: 12px;
      color: #2F54EB;
    }

    &-text {
      margin-left: 4px;
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;
    }

    &:hover {
      .commen-settings-btn-text {
        color: #2F54EB;
      }
    }
  }

  .lang-menu {
    width: 100%;
    display: flex;
    flex-direction: column;

    &-item {
      width: 100%;
      padding: 5px 10px;
      cursor: pointer;
      color: #4E5969;

      &_active {
        color: #2F54EB;
        background-color: #f0f5ff;
      }

      &:hover {
        color: #2F54EB;
      }
    }
  }

  .user-info-wrap {
    .avatar {
      transition: all 0.2s;
      border: solid 1px transparent;
    }

    &:hover {
      .avatar {
        border-color: #2F54EB;
      }
    }
  }
}
</style>
