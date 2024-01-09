<template>
  <div class="top-menu" v-if="routes.length > 2">
    <!-- <a-menu v-model="current" mode="horizontal">
      <a-menu-item :key="route.name" v-for="route in routes.slice(0, routes.length - 1)">
        <router-link :to="{ name: route.name }">{{ route.meta.title }}</router-link>
      </a-menu-item>
    </a-menu>-->
    <span
      :class="current === route.name ? 'top-menu-selected' : ''"
      v-for="route in defaultShowRoutes"
      :key="route.name"
      @click="() => handleClick(route)"
    >
      {{ route.meta.title }}
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
import store from '@/store'
import { gridSvg, top_agent, top_acl } from '@/core/icons'
export default {
  name: 'TopMenu',
  components: { gridSvg, top_agent, top_acl },
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
  },
  methods: {
    handleClick(route) {
      this.visible = false
      if (route.name !== this.current) {
        this.$router.push(route.redirect)
        // this.current = route.name
      }
    },
  },
}
</script>

<style lang="less">
@import '../../style/static.less';
// .top-menu {
//   display: inline-block;
// }
// .ant-menu-horizontal {
//   border-bottom: 0 !important;
// }
// .ant-menu-horizontal > .ant-menu-item {
//   border-bottom: 0;
// }

.top-menu {
  display: inline-flex;
  align-items: center;
  > .top-menu-icon {
    width: 40px;
    height: @layout-header-icon-height;
    line-height: @layout-header-icon-height;
    border-radius: 4px !important;
    display: inline-flex;
    align-items: flex-end;
  }
  > span {
    cursor: pointer;
    padding: 4px 10px;
    margin: 0 5px;
    border-radius: 4px;
    color: @layout-header-font-color;
    height: @layout-header-height;
    display: inline-flex;
    align-items: center;
    &:hover {
      background: linear-gradient(0deg, rgba(0, 80, 201, 0.2) 0%, rgba(174, 207, 255, 0.06) 86.76%);
      color: @layout-header-font-selected-color;
      border-radius: 3px 3px 0px 0px;
    }
  }
  .top-menu-selected {
    background: linear-gradient(0deg, rgba(0, 80, 201, 0.2) 0%, rgba(174, 207, 255, 0.06) 86.76%);
    color: @layout-header-font-selected-color;
    border-radius: 3px 3px 0px 0px;
    border-bottom: 3px solid @layout-header-font-selected-color;
    &:hover {
      background: linear-gradient(0deg, rgba(0, 80, 201, 0.2) 0%, rgba(174, 207, 255, 0.06) 86.76%);
      color: @layout-header-font-selected-color;
      border-radius: 3px 3px 0px 0px;
    }
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
