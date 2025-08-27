<template>
  <div class="top-menu" v-if="routes.length > 2">
    <span
      :class="current === route.name ? 'top-menu-selected' : ''"
      v-for="route in defaultShowRoutes"
      :key="route.name"
      @click="() => handleClick(route)"
    >
      {{ route.meta.title }}
    </span>
    <span
      :class="current === 'chart-demo' ? 'top-menu-selected' : ''"
      @click="() => handleClick({ name: 'chart-demo' })"
    >
      Topology
    </span>
    <!-- <a-popover v-model="visible" placement="bottom" trigger="click" overlayClassName="top-menu-dropdown">
      <template slot="content">
        <div class="title">
          更多应用
        </div>
        <a-divider style="margin:10px 0;" />
        <div
          @click="
            () => {
              handleClick(route)
            }
          "
          :class="`more ${current == route.name ? 'more-selected' : ''}`"
          v-for="route in defaultUnShowRoutes"
          :key="route.name"
        >
          <div class="more-icon-block">
            <components :is="`top_${route.name}`" style="width:40px;height:40px;" />
          </div>
          {{ route.meta.title }}
        </div>
      </template>
      <span class="top-menu-icon"><gridSvg /></span>
    </a-popover> -->
  </div>
</template>

<script>
import { gridSvg, top_acl, top_agent, topChartDemo } from '@/core/icons'
import { getPreference } from '@/modules/cmdb/api/preference'
import store from '@/store'
export default {
  name: 'TopMenu',
  components: { gridSvg, top_agent, top_acl, topChartDemo },
  data() {
    return {
      defaultShowRouteName: ['cmdb', 'acl'],
      defaultUnShowRouteName: [],
      routes: store.getters.appRoutes.filter((i) => !(i.meta || {}).hiddenInTopMenu),
      current: store.getters.appRoutes[0].name,
      visible: false,
    }
  },
  computed: {
    defaultShowRoutes() {
      return this.routes.filter((item) => this.defaultShowRouteName.includes(item.name))
    },
    defaultUnShowRoutes() {
      return this.routes.filter((item) => this.defaultUnShowRouteName.includes(item.name))
    },
  },
  watch: {
    $route: {
      immediate: true,
      deep: true,
      handler(newVal) {
        if (newVal) {
          this.current = newVal.matched[0].name
        }
      },
    },
  },
  mounted() {
    this.current = this.$route.matched[0].name
    console.log('TopMenu routes:', this.routes)
    console.log('TopMenu defaultShowRoutes:', this.defaultShowRoutes)
    console.log('TopMenu appRoutes:', store.getters.appRoutes)
  },
  methods: {
    async handleClick(route) {
      this.visible = false
      if (route.name !== this.current) {
        if (route.name === 'cmdb') {
          const preference = await getPreference()
          const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
          if (lastTypeId && preference.type_ids.some((item) => item === Number(lastTypeId))) {
            this.$router.push(`/cmdb/instances/types/${lastTypeId}`)
          } else {
            this.$router.push('/cmdb/dashboard')
          }
        } else if (route.name === 'chart-demo') {
          this.$router.push('/chart-demo/gds')
        } else if (route.name === 'xyz') {
          this.$router.push('/xyz')
        } else {
          this.$router.push(route.redirect)
        }
        // this.current = route.name
      }
    },
  },
}
</script>

<style lang="less">
@import '../../style/static.less';

.top-menu {
  display: inline-flex;
  align-items: center;
  > .top-menu-icon {
    width: 40px;
    height: @layout-header-icon-height;
    line-height: @layout-header-icon-height;
    border-radius: 4px !important;
    display: inline-flex;
    align-items: center;
  }
  > span {
    cursor: pointer;
    padding: 4px 10px;
    margin: 0 5px;
    color: @layout-header-font-color;
    height: @layout-header-height;
    line-height: @layout-header-line-height;
    display: inline-block;
  }
  > span:hover {
    background-color: #f0f2f5;
  }
  .top-menu-selected {
    font-weight: bold;
    color: @layout-header-font-selected-color;
  }
  > span::before {
    display: block;
    content: attr(title);
    font-weight: bold;
    height: 0;
    overflow: hidden;
    visibility: hidden;
  }
}

.top-menu-dropdown.ant-popover-placement-bottom .ant-popover-content {
  margin-top: -8px;
}

.top-menu-dropdown {
  min-width: 500px;
  .ant-popover-arrow {
    display: none;
  }
  .title {
    font-weight: 700;
  }
  .more {
    display: inline-block;
    padding: 8px 16px;
    margin: 0px 30px 0 10px;
    border-radius: 4px;
    background: linear-gradient(0deg, #eeeeee 55%, white);
    color: @layout-header-font-color;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    .more-icon-block {
      width: 40px;
      height: 40px;
    }
    &:hover {
      background: linear-gradient(0deg, rgba(0, 80, 201, 0.2) 0%, rgba(174, 207, 255, 0.06) 86.76%);
      color: @layout-header-font-selected-color;
    }
  }
  .more-selected {
    background-color: #001428;
    color: @layout-header-font-color;
  }
}
</style>
