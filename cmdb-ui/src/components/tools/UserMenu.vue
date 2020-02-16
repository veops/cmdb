<template>
  <div class="user-wrapper">
    <div class="content-box">
      <a href="https://github.com/pycook/cmdb" target="_blank">
        <span class="action">
          {{ $t('tip.sourceCode') }} -> <a-icon type="github" style="font-size: 20px; color: #002140"></a-icon>
        </span>
      </a>
      <!-- <a href="https://pro.loacg.com/docs/getting-started" target="_blank">
        <span class="action">
          <a-icon type="question-circle-o"></a-icon>
        </span>
      </a>
      <notice-icon class="action"/> -->
      <a-dropdown>
        <span class="action ant-dropdown-link user-dropdown-menu">
          <a-avatar class="avatar" size="small" :src="avatar()"/>
          <span>{{ nickname() }}</span>
        </span>
        <a-menu slot="overlay" class="user-dropdown-menu-wrapper">
          <!-- <a-menu-item key="0">
            <router-link :to="{ name: 'center' }">
              <a-icon type="user"/>
              <span>个人中心</span>
            </router-link>
          </a-menu-item>
          <a-menu-item key="1">
            <router-link :to="{ name: 'settings' }">
              <a-icon type="setting"/>
              <span>账户设置</span>
            </router-link>
          </a-menu-item>
          <a-menu-divider/> -->
          <a-menu-item key="3">
            <a href="javascript:;" @click="handleLogout">
              <a-icon type="logout"/>
              <span>{{ $t('login.logout') }}</span>
            </a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
      <lang-select v-if="showLocale" />
    </div>
  </div>
</template>

<script>
import NoticeIcon from '@/components/NoticeIcon'
import { mapActions, mapGetters } from 'vuex'
import LangSelect from '@/components/tools/LangSelect'
import config from '@/config/defaultSettings'

export default {
  name: 'UserMenu',
  components: {
    NoticeIcon, LangSelect
  },
  data () {
    return {
      showLocale: config.showLocale
    }
  },
  methods: {
    ...mapActions(['Logout']),
    ...mapGetters(['nickname', 'avatar']),
    handleLogout () {
      const that = this

      this.$confirm({
        title: this.$t('tip.warning'),
        content: this.$t('login.confirmLogout'),
        onOk () {
          return that.Logout()
        },
        onCancel () {
        }
      })
    }
  }
}
</script>
