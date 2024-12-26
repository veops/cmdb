import router, { resetRouter } from '@/router'
import Menu from 'ant-design-vue/es/menu'
import Icon from 'ant-design-vue/es/icon'
import store from '@/store'
import {
  subscribeCIType,
  subscribeTreeView,
} from '@/modules/cmdb/api/preference'
import { searchResourceType } from '@/modules/acl/api/resource'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import CMDBGrant from '@/modules/cmdb/components/cmdbGrant'
import styles from './index.module.less'
import { mapActions } from 'vuex'

const { Item, SubMenu } = Menu

export default {
  name: 'SMenu',
  props: {
    menu: {
      type: Array,
      required: true
    },
    theme: {
      type: String,
      required: false,
      default: 'dark'
    },
    mode: {
      type: String,
      required: false,
      default: 'inline'
    },
    collapsed: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      openKeys: [],
      selectedKeys: [],
      cachedOpenKeys: [],
      resource_type: {},
      currentAppRoute: ''
    }
  },
  computed: {
    rootSubmenuKeys: vm => {
      const keys = []
      vm.menu.forEach(item => keys.push(item.path))
      return keys
    },
  },
  provide() {
    return {
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  created() {

  },
  mounted() {
    searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then(res => {
      this.resource_type = { groups: res.groups, id2perms: res.id2perms }
    })
    this.currentAppRoute = this.$route?.matched?.[0]?.name || ''
    this.updateMenu()
  },
  watch: {
    collapsed(val) {
      if (val) {
        this.cachedOpenKeys = this.openKeys.concat()
        this.openKeys = []
      } else {
        this.openKeys = this.cachedOpenKeys
      }
    },
    $route: function (route) {
      this.currentAppRoute = route?.matched?.[0]?.name
      this.updateMenu()
    },
  },
  inject: ['reload'],
  methods: {
    ...mapActions(['UpdateCMDBSEarchValue']),
    cancelAttributes(e, menu) {
      const that = this
      e.preventDefault()
      e.stopPropagation()
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.preference.confirmcancelSub2', { name: menu.meta.title }),
        onOk() {
          const citypeId = menu.meta.typeId
          const unsubCIType = subscribeCIType(citypeId, '')
          const unsubTree = subscribeTreeView(citypeId, '')
          Promise.all([unsubCIType, unsubTree]).then(() => {
            that.$message.success(that.$t('cmdb.preference.cancelSubSuccess'))
            const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
            if (Number(citypeId) === Number(lastTypeId)) {
              localStorage.setItem('ops_ci_typeid', '')
            }
            const href = window.location.href
            const hrefSplit = href.split('/')
            if (Number(hrefSplit[hrefSplit.length - 1]) === Number(citypeId)) {
              that.$router.push('/cmdb/preference')
            }
            const roles = store.getters.roles
            resetRouter()
            store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
              router.addRoutes(store.getters.appRoutes)
            })
            if (hrefSplit[hrefSplit.length - 1] === 'preference') {
              that.reload()
            }
          })
        },
      })
    },
    // select menu item
    onOpenChange(openKeys) {
      if (this.mode === 'horizontal') {
        this.openKeys = openKeys
        return
      }
      const latestOpenKey = openKeys.find(key => !this.openKeys.includes(key))
      if (!this.rootSubmenuKeys.includes(latestOpenKey)) {
        this.openKeys = openKeys
      } else {
        this.openKeys = latestOpenKey ? [latestOpenKey] : []
      }
    },
    updateMenu() {
      const routes = this.$route.matched.concat()

      const { hidden } = this.$route.meta
      if (routes.length >= 3 && hidden) {
        routes.pop()
        this.selectedKeys = [routes[routes.length - 1].path]
      } else {
        this.selectedKeys = [routes.pop().path]
      }
      const openKeys = []
      if (this.mode === 'inline') {
        routes.forEach(item => {
          openKeys.push(item.path)
        })
      }

      this.collapsed ? (this.cachedOpenKeys = openKeys) : (this.openKeys = openKeys)
    },
    // render
    renderItem(menu) {
      if (this.collapsed && menu.meta.disabled) {
        return null
      }
      if (!menu.hidden) {
        return menu.children && !menu.hideChildrenInMenu ? this.renderSubMenu(menu) : this.renderMenuItem(menu)
      }
      return null
    },
    renderI18n(title) {
      if (Object.prototype.toString.call(this.$t(`${title}`)) === '[object Object]') {
        return title
      }
      return this.$t(`${title}`)
    },
    renderMenuItem(menu) {
      const isShowDot = menu.path.substr(0, 22) === '/cmdb/instances/types/'
      const target = menu.meta.target || null
      const tag = target && 'a' || 'router-link'
      const props = { to: { name: menu.name } }
      const attrs = { href: menu.meta.targetHref || menu.path, target: menu.meta.target }

      if (menu.children && menu.hideChildrenInMenu) {
        menu.children.forEach(item => {
          item.meta = Object.assign(item.meta, { hidden: true })
        })
      }

      return (
        <Item {...{ key: menu.path }} disabled={menu.meta.disabled || false}>
          <tag {...{ props, attrs }}>
            {this.renderIcon({ icon: menu.meta.icon, customIcon: menu.meta.customIcon, name: menu.meta.name, typeId: menu.meta.typeId, routeName: menu.name, selectedIcon: menu.meta.selectedIcon, })}
            <span>
              <span style={menu.meta.style} class={this.renderI18n(menu.meta.title).length > 10 ? 'scroll' : ''}>{this.renderI18n(menu.meta.title)}</span>
              {isShowDot && !menu.meta.disabled &&
                <a-popover
                  overlayClassName="custom-menu-extra-submenu"
                  placement="rightTop"
                  arrowPointAtCenter
                  autoAdjustOverflow={false}
                  getPopupContainer={(trigger) => trigger}
                  content={() =>
                    <div>
                      <div onClick={e => this.handlePerm(e, menu, 'CIType')} class="custom-menu-extra-submenu-item"><a-icon type="user-add" />{ this.renderI18n('grant') }</div>
                      <div onClick={e => this.cancelAttributes(e, menu)} class="custom-menu-extra-submenu-item"><a-icon type="star" />{ this.renderI18n('cmdb.preference.cancelSub') }</div>
                    </div>}
                >
                  <a-icon type="menu" ref="extraEllipsis" class="custom-menu-extra-ellipsis"></a-icon>
                </a-popover>
              }
            </span>
          </tag>
          {isShowDot && <CMDBGrant ref="cmdbGrantCIType" resourceType="CIType" app_id="cmdb" />}
        </Item>
      )
    },
    renderSubMenu(menu) {
      const itemArr = []
      if (!menu.hideChildrenInMenu) {
        menu.children.forEach(item => itemArr.push(this.renderItem(item)))
      }
      return (
        <SubMenu {...{ key: menu.path }}>
          <span slot="title">
            {this.renderIcon({ icon: menu.meta.icon, selectedIcon: menu.meta.selectedIcon, routeName: menu.name })}
            <span>{this.renderI18n(menu.meta.title)}</span>
          </span>
          {itemArr}
        </SubMenu>
      )
    },
    renderIcon({ icon, selectedIcon, customIcon = undefined, name = undefined, typeId = undefined, routeName }) {
      if (typeId) {
        if (customIcon) {
          if (customIcon.split('$$')[2]) {
            return <img style={{ maxHeight: '14px', maxWidth: '14px', marginRight: '10px' }} src={`/api/common-setting/v1/file/${customIcon.split('$$')[3]}`}></img >
          }
          return <ops-icon
            style={{
              color: customIcon.split('$$')[1],
            }}
            type={customIcon.split('$$')[0]}
          />
        }
        return <span
          style={{
            display: 'inline-block',
            width: '14px',
            height: '14px',
            borderRadius: '50%',
            backgroundColor: '#d3d3d3',
            color: '#fff',
            textAlign: 'center',
            lineHeight: '14px',
            fontSize: '10px',
            marginRight: '10px'
          }}
        >{name[0].toUpperCase()}</span>
      }

      if (icon === 'none' || icon === undefined) {
        return null
      }
      const props = {}
      if (this.$route.name === routeName && selectedIcon) {
        return <ops-icon type={selectedIcon}></ops-icon>
      } else if (icon.startsWith('ops-') || icon.startsWith('icon-xianxing') || icon.startsWith('icon-shidi') || icon.startsWith('veops-')) {
        return <ops-icon type={icon}></ops-icon>
      } else {
        typeof (icon) === 'object' ? props.component = icon : props.type = icon
        return (
          <Icon {... { props }} />
        )
      }
    },
    handlePerm(e, menu, resource_type_name) {
      e.stopPropagation()
      e.preventDefault()
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name,
        perm: 'grant',
        resource_name: menu.meta.name,
      }).then(res => {
        if (res.result) {
          console.log(menu)
          if (resource_type_name === 'CIType') {
            this.$refs.cmdbGrantCIType.open({ name: menu.meta.name, cmdbGrantType: 'ci', CITypeId: menu.meta?.typeId })
          } else {
            this.$refs.cmdbGrantRelationView.open({ name: menu.meta.name, cmdbGrantType: 'relation_view' })
          }
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },

    jumpCMDBSearch(value) {
      this.UpdateCMDBSEarchValue(value)

      if (this.$route.name !== 'cmdb_resource_search') {
        this.$router.push({
          name: 'cmdb_resource_search',
        })
      }
    },

    renderCMDBSearch() {
      if (this.currentAppRoute !== 'cmdb' || this.collapsed) {
        return null
      }

      return (
        <Item class={styles['cmdb-side-menu-search']}>
          <a-input
            ref="cmdbSideMenuSearchInputRef"
            class={`ops-input ${this.$route.name === 'cmdb_resource_search' ? 'cmdb-side-menu-search-focused' : ''}`}
            placeholder={this.$t('cmdbSearch')}
            onPressEnter={(e) => {
              this.jumpCMDBSearch(e.target.value)
            }}
          >
            <ops-icon
              slot="suffix"
              type="veops-search1"
              onClick={() => {
                const value = this.$refs?.cmdbSideMenuSearchInputRef?.$refs?.input?.value || ''
                this.jumpCMDBSearch(value)
              }}
            />
          </a-input>
        </Item>
      )
    }
  },

  render() {
    const { mode, theme, menu } = this
    const props = {
      mode: mode,
      theme: theme,
      openKeys: this.openKeys
    }
    const on = {
      select: obj => {
        // this.selectedKeys = obj.selectedKeys
        this.$emit('select', obj)
      },
      openChange: this.onOpenChange
    }

    const menuTree = menu.map(item => {
      if (item.hidden) {
        return null
      }
      return this.renderItem(item)
    })
    // {...{ props, on: on }}
    return (
      <Menu class="ops-side-bar" selectedKeys={this.selectedKeys} {...{ props, on: on }}>
        {this.renderCMDBSearch()}
        {menuTree}
      </Menu>
    )
  }
}
