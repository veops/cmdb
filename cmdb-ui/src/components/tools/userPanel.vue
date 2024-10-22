<template>
  <div class="user-panel">
    <a-avatar
      class="user-panel-avatar"
      size="small"
      icon="user"
      :src="avatarSrc"
    />
    <div class="user-panel-nickname">
      {{ userInfo.nickname }}
    </div>
    <div class="user-panel-info">
      <ops-icon
        type="veops-company"
        class="user-panel-info-icon"
      />
      <div class="user-panel-info-text">
        {{ companyName }}
      </div>
    </div>
    <div class="user-panel-info">
      <ops-icon
        type="veops-emails"
        class="user-panel-info-icon"
      />
      <div class="user-panel-info-text">
        {{ email }}
      </div>
    </div>

    <div class="user-panel-btn">
      <div
        v-for="(item) in userBtnGroup"
        :key="item.type"
        class="user-panel-btn-item"
        @click="clickBtnGroup(item.type)"
      >
        <ops-icon
          :type="item.icon"
          class="user-panel-btn-icon"
        />
        <span class="user-panel-btn-title">
          {{ $t(item.title) }}
        </span>
      </div>
    </div>

    <div class="user-panel-row">
      <div class="user-panel-row-label">
        {{ $t('userPanel.switchLanguage') }}
      </div>

      <div class="user-panel-lang">
        <div
          v-for="(lang, index) in languageList"
          :key="index"
          :class="['user-panel-lang-item', lang.key === locale ? 'user-panel-lang-item_active' : '']"
          @click="changeLang(lang.key)"
        >
          {{ lang.title }}
        </div>
      </div>
    </div>

    <div class="user-panel-row">
      <div class="user-panel-row-label">
        {{ $t('userPanel.bindAccount') }}
      </div>

      <div class="user-panel-bind">
        <a-tooltip
          v-for="(item) in bindList"
          :key="item.type"
          :title="$t(item.title)"
        >
          <ops-icon
            class="user-panel-bind-item"
            :type="userInfo.notice_info && userInfo.notice_info[item.type] ? item.existedIcon : item.icon"
            @click="handleBindInfo(item.type)"
          />
        </a-tooltip>
      </div>
    </div>

    <div class="user-panel-account">
      <div
        v-for="(item, index) in accountActions"
        :key="index"
        class="user-panel-account-item"
        @click="handleLogout"
      >
        <ops-icon class="user-panel-account-icon" :type="item.icon" />
        <span class="user-panel-account-title">
          {{ $t(item.title) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex'
import { setDocumentTitle, domTitle } from '@/utils/domUtil'
import {
  bindPlatformByUid,
  unbindPlatformByUid,
} from '@/api/employee'
import { getCompanyInfo } from '@/api/company'

export default {
  name: 'UserPanel',
  data() {
    return {
      userBtnGroup: [
        {
          icon: 'veops-personal',
          title: 'userPanel.myProfile',
          type: 'myProfile'
        },
        {
          icon: 'a-veops-account1',
          title: 'userPanel.accountPassword',
          type: 'accountPassword'
        }
      ],
      languageList: [
        {
          title: '简中',
          key: 'zh'
        },
        {
          title: 'EN',
          key: 'en'
        },
      ],
      bindList: [
        {
          type: 'wechatApp',
          icon: 'qiyeweixin',
          existedIcon: 'wechatApp',
          title: 'wechat'
        },
        {
          type: 'feishuApp',
          icon: 'ops-setting-notice-feishu-selected',
          existedIcon: 'feishuApp',
          title: 'feishu'
        },
        {
          type: 'dingdingApp',
          icon: 'ops-setting-notice-dingding-selected',
          existedIcon: 'dingdingApp',
          title: 'dingding'
        },
      ],
      accountActions: [
        {
          icon: 'veops-switch',
          title: 'userPanel.switchAccount'
        },
        {
          icon: 'veops-sign_out',
          title: 'userPanel.logout'
        },
      ],
      hoverBindAccountList: []
    }
  },
  computed: {
    ...mapState({
      email: (state) => state.user.email,
      locale: (state) => state.locale,
      userInfo: (state) => state.user,
      companyName: (state) => state.company.name
    }),
    avatarSrc() {
      const avatar = this.userInfo.avatar
      if (!avatar) {
        return null
      }

      return avatar.startsWith('https') ? avatar : `/api/common-setting/v1/file/${avatar}`
    }
  },
  mounted() {
    if (this.companyName === undefined) {
      this.getCompanyInfo()
    }
  },
  methods: {
    ...mapActions(['Logout', 'GetInfo']),
    ...mapMutations(['SET_LOCALE', 'SET_COMPANY_NAME']),
    async getCompanyInfo() {
      const res = await getCompanyInfo()
      const name = res?.info?.name || ''
      this.SET_COMPANY_NAME(name)
    },

    changeLang(lang) {
      this.SET_LOCALE(lang)
      this.$i18n.locale = lang
      this.$nextTick(() => {
        setDocumentTitle(`${this.$t(this.$route.meta.title)} - ${domTitle}`)
      })
    },
    handleBindInfo(platform) {
      const isBind = this?.userInfo?.notice_info?.[platform]
      const uid = this?.userInfo?.uid

      if (isBind) {
        this.$confirm({
          title: this.$t('warning'),
          content: this.$t('cs.person.confirmUnbind'),
          onOk: () => {
            unbindPlatformByUid(platform, uid)
              .then(() => {
                this.$message.success(this.$t('cs.person.unbindSuccess'))
              })
              .finally(() => {
                this.GetInfo()
              })
          },
        })
      } else {
        bindPlatformByUid(platform, uid)
          .then(() => {
            this.$message.success(this.$t('cs.person.bindSuccess'))
          })
          .finally(() => {
            this.GetInfo()
          })
      }
    },

    handleLogout() {
      this.$confirm({
        title: this.$t('tip'),
        content: this.$t('topMenu.confirmLogout'),
        onOk: () => {
          this.Logout()
        },
        onCancel() {},
      })
    },

    clickBtnGroup(type) {
      switch (type) {
        case 'myProfile':
          if (this.$route.name === 'setting_person') {
            this.$bus.$emit('changeSettingPersonCurrent', '1')
          } else {
            this.$router.push({
              name: 'setting_person',
              query: {
                current: '1'
              }
            })
          }
          break
        case 'accountPassword':
          if (this.$route.name === 'setting_person') {
            this.$bus.$emit('changeSettingPersonCurrent', '2')
          } else {
            this.$router.push({
              name: 'setting_person',
              query: {
                current: '2'
              }
            })
          }
          break
        default:
          break
      }
    },

    handleBindAccountMouse(type, isHover) {
      const index = this.hoverBindAccountList.findIndex((item) => item === type)
      if (isHover && index === -1) {
        this.hoverBindAccountList.push(type)
      } else if (!isHover && index !== -1) {
        this.hoverBindAccountList.splice(index, 1)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.user-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 350px;
  padding: 0 20px;

  &-avatar {
    width: 62px;
    height: 62px;
    border-radius: 62px;
    margin-top: 13px;

    display: flex;
    align-items: center;
    justify-content: center;
    color: #000000;
    background-color: #FFFFFF;
    font-size: 48px !important;
  }

  &-nickname {
    color: #1D2129;
    font-size: 15px;
    font-weight: 700;

    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
    margin-top: 8px;
  }

  &-info {
    display: flex;
    align-items: center;
    column-gap: 6px;
    margin-top: 6px;
    max-width: 100%;

    &-icon {
      flex-shrink: 0;
      font-size: 12px;
    }

    &-text {
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;

      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
    }
  }

  &-btn {
    width: 100%;
    height: 72px;
    display: flex;
    align-items: center;
    margin-top: 11px;

    &-icon {
      font-size: 22px;
      color: #CACDD9;
    }

    &-title {
      font-size: 14px;
      font-weight: 400;
      color: #1D2129;
      margin-top: 8px;
    }

    &-item {
      flex: 1;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-color: #F7F8FA;
      cursor: pointer;

      &:hover {
        background-color: #EBEFF8;

        .user-panel-btn-icon {
          color: #2F54EB;
        }

        .user-panel-btn-title {
          color: #2F54EB;
        }
      }
    }
  }

  &-row {
    width: 100%;
    margin-top: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    &-label {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
    }
  }

  &-lang {
    display: flex;
    align-items: center;
    height: 28px;
    width: 108px;
    border-radius: 28px;
    overflow: hidden;

    &-item {
      flex: 1;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #F7F8FA;
      cursor: pointer;

      &:first-child {
        border-right: solid 1px #E4E7ED;
      }

      &_active {
        background-color: #EBEFF8;
        color: #2F54EB;
      }

      &:hover {
        color: #2F54EB;
      }
    }
  }

  &-bind {
    display: flex;
    align-items: center;
    column-gap: 22px;

    &-item {
      cursor: pointer;
      font-size: 16px;
    }
  }

  &-account {
    margin-top: 22px;
    padding-top: 13px;
    padding-bottom: 20px;
    border-top: solid 1px #F0F1F5;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    width: 100%;

    &-icon {
      font-size: 14px;
      color: #CACDD9;
    }

    &-title {
      font-size: 14px;
      color: #86909C;
      margin-left: 5px;
    }

    &-item {
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
      cursor: pointer;

      &:hover {
        .user-panel-account-icon {
          color: #2F54EB;
        }

        .user-panel-account-title {
          color: #2F54EB;
        }
      }
    }
  }
}
</style>
