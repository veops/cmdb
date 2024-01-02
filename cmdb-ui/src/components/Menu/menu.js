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
      resource_type: {}
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
    $route: function () {
      this.updateMenu()
    },
  },
  inject: ['reload'],
  methods: {
    // 取消订阅
    cancelAttributes(e, menu) {
      const that = this
      e.preventDefault()
      e.stopPropagation()
      this.$confirm({
        title: '警告',
        content: `确认取消订阅 ${menu.meta.title}?`,
        onOk() {
          const citypeId = menu.meta.typeId
          const unsubCIType = subscribeCIType(citypeId, '')
          const unsubTree = subscribeTreeView(citypeId, '')
          Promise.all([unsubCIType, unsubTree]).then(() => {
            that.$message.success('取消订阅成功')
            const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
            if (Number(citypeId) === Number(lastTypeId)) {
              localStorage.setItem('ops_ci_typeid', '')
            }
            // 删除路由
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
      // 在水平模式下时执行，并且不再执行后续
      if (this.mode === 'horizontal') {
        this.openKeys = openKeys
        return
      }
      // 非水平模式时
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
      return this.$t(`${title}`)
    },
    renderMenuItem(menu) {
      const isShowDot = menu.path.substr(0, 22) === '/cmdb/instances/types/'
      const isShowGrant = menu.path.substr(0, 20) === '/cmdb/relationviews/'
      const target = menu.meta.target || null
      const tag = target && 'a' || 'router-link'
      const props = { to: { name: menu.name } }
      const attrs = { href: menu.meta.targetHref || menu.path, target: menu.meta.target }

      if (menu.children && menu.hideChildrenInMenu) {
        // 把有子菜单的 并且 父菜单是要隐藏子菜单的
        // 都给子菜单增加一个 hidden 属性
        // 用来给刷新页面时， selectedKeys 做控制用
        menu.children.forEach(item => {
          item.meta = Object.assign(item.meta, { hidden: true })
        })
      }

      return (
        <Item {...{ key: menu.path }} disabled={menu.meta.disabled || false}>
          <tag {...{ props, attrs }}>
            {this.renderIcon({ icon: menu.meta.icon, customIcon: menu.meta.customIcon, name: menu.meta.name, typeId: menu.meta.typeId, routeName: menu.name, selectedIcon: menu.meta.selectedIcon, })}
            <span>
              <span class={this.renderI18n(menu.meta.title).length > 10 ? 'scroll' : ''}>{this.renderI18n(menu.meta.title)}</span>
              {isShowDot &&
                <a-popover
                  overlayClassName="custom-menu-extra-submenu"
                  placement="rightTop"
                  arrowPointAtCenter
                  autoAdjustOverflow={false}
                  getPopupContainer={(trigger) => trigger}
                  content={() =>
                    <div>
                      <div onClick={e => this.handlePerm(e, menu, 'CIType')} class="custom-menu-extra-submenu-item"><a-icon type="user-add" />授权</div>
                      <div onClick={e => this.cancelAttributes(e, menu)} class="custom-menu-extra-submenu-item"><a-icon type="star" />取消订阅</div>
                    </div>}
                >
                  <a-icon type="menu" ref="extraEllipsis" class="custom-menu-extra-ellipsis"></a-icon>
                </a-popover>
              }
              {isShowGrant && <a-icon class="custom-menu-extra-ellipsis" onClick={e => this.handlePerm(e, menu, 'RelationView')} type="user-add" />}
            </span>
          </tag>
          {isShowDot && <CMDBGrant ref="cmdbGrantCIType" resourceType="CIType" app_id="cmdb" />}
          {isShowGrant && <CMDBGrant ref="cmdbGrantRelationView" resourceType="RelationView" app_id="cmdb" />}
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
      } else if (icon.startsWith('ops-') || icon.startsWith('icon-xianxing') || icon.startsWith('icon-shidi')) {
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
          this.$message.error('权限不足！')
        }
      })
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
        {menuTree}
      </Menu>
    )
  }
}
