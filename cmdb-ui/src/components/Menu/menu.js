import { Menu, Icon } from 'ant-design-vue'

const menuProps = {
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
  },
  i18nRender: {
    type: Function,
    required: false
  }
}

const defaultI18nRender = (key) => `${key}`

// render
const renderItem = (h, menu, i18nRender) => {
  if (!menu.hidden) {
    // const localeKey = `menu.${menu.name}`
    // const localeKey = menu.meta && menu.meta.title
    // i18nRender(localeKey)
    return menu.children && !menu.hideChildrenInMenu ? renderSubMenu(h, menu, i18nRender) : renderMenuItem(h, menu, i18nRender)
  }
  return null
}

const renderMenuItem = (h, menu, i18nRender) => {
  const target = menu.meta.target || null
  const CustomTag = target && 'a' || 'router-link'
  const props = { to: { name: menu.name } }
  const attrs = { href: menu.path, target: menu.meta.target }

  if (menu.children && menu.hideChildrenInMenu) {
    // 把有子菜单的 并且 父菜单是要隐藏子菜单的
    // 都给子菜单增加一个 hidden 属性
    // 用来给刷新页面时， selectedKeys 做控制用
    menu.children.forEach(item => {
      item.meta = Object.assign(item.meta, { hidden: true })
    })
  }

  return (
    <Menu.Item {...{ key: menu.path }}>
      <CustomTag {...{ props, attrs }}>
        {renderIcon(h, menu.meta.icon)}
        <span>{i18nRender(menu.meta.title)}</span>
      </CustomTag>
    </Menu.Item>
  )
}

const renderSubMenu = (h, menu, i18nRender) => {
  const itemArr = []
  if (!menu.hideChildrenInMenu) {
    menu.children.forEach(item => itemArr.push(renderItem(h, item, i18nRender)))
  }
  return (
    <Menu.SubMenu {...{ key: menu.path }}>
      <span slot="title">
        {renderIcon(h, menu.meta.icon)}
        <span>{i18nRender(menu.meta.title)}</span>
      </span>
      {itemArr}
    </Menu.SubMenu>
  )
}

const renderIcon = (h, icon) => {
  if (icon === 'none' || icon === undefined) {
    return null
  }
  const props = {}
  typeof (icon) === 'object' ? props.component = icon : props.type = icon
  return (
    <Icon {...{ props }}/>
  )
}

const SMenu = {
  name: 'SMenu',
  props: menuProps,
  data () {
    return {
      openKeys: [],
      selectedKeys: [],
      cachedOpenKeys: []
    }
  },
  computed: {
    rootSubmenuKeys: vm => {
      const keys = []
      vm.menu.forEach(item => keys.push(item.path))
      return keys
    }
  },
  created () {
    this.$watch('collapsed', collapsed => {
      if (collapsed) {
        this.cachedOpenKeys = this.openKeys.concat()
        this.openKeys = []
      } else {
        this.openKeys = this.cachedOpenKeys
      }
    })
    this.$watch('$route', () => {
      this.updateMenu()
    })
  },
  mounted () {
    this.updateMenu()
  },
  methods: {
    // select menu item
    onOpenChange (openKeys) {
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
    updateMenu () {
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
    }
  },
  render (h) {
    const { mode, theme, menu, i18nRender = defaultI18nRender } = this
    const props = {
      mode: mode,
      theme: theme,
      openKeys: this.openKeys
    }
    const on = {
      select: obj => {
        this.selectedKeys = obj.selectedKeys
        this.$emit('select', obj)
      },
      openChange: this.onOpenChange
    }

    const menuTree = menu.map(item => {
      if (item.hidden) {
        return null
      }
      return renderItem(h, item, i18nRender)
    })
    // {...{ props, on: on }}
    return (
      <Menu vModel={this.selectedKeys} {...{ props, on: on }}>
        {menuTree}
      </Menu>
    )
  }
}

export default SMenu
