<template>
  <div>
    <div
      :class="{
        'sidebar-list-item': true,
        'sidebar-list-item-dotline': dotLine,
        'sidebar-list-item-selected': selected[`${value}`] === item[`${value}`],
      }"
      v-for="item in list"
      :key="item[`${value}`]"
      @click="
        () => {
          selected = item
          $emit('clickItem', item)
        }
      "
    >
      <div class="sidebar-list-label" :title="item[`${label}`]">
        <slot name="icon" :item="item"></slot>
        <slot name="label" :item="item">{{ item[`${label}`] }}</slot>
      </div>
      <a-space class="sidebar-list-action"><slot name="action"> </slot></a-space>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SidebarList',
  props: {
    list: {
      type: Array,
      default: () => {},
    },
    value: {
      type: String,
      default: 'id',
    },
    label: {
      type: String,
      default: 'name',
    },
    dotLine: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      selected: {},
    }
  },
  mounted() {},
  methods: {
    setSelected(item) {
      this.selected = item
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.sidebar-list-item {
  .ops_popover_item();
  margin: 2px 0;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .sidebar-list-label {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .sidebar-list-action {
    margin-left: auto;
    display: none;
  }
  &:hover {
    .sidebar-list-action {
      display: inline-flex;
    }
    .sidebar-list-label {
      width: calc(100% - 36px);
    }
  }
}

.sidebar-list-item-selected {
  .ops_popover_item_selected();
  background-color: transparent;
}
.sidebar-list-item.sidebar-list-item-selected::before {
  background-color: #custom_colors[color_1];
}
.sidebar-list-item-dotline {
  padding-left: 20px;
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 10px;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #cacaca;
    z-index: 2;
  }
}

.sidebar-list-item-dotline:not(:last-child)::after {
  content: '';
  width: 1px;
  height: 31px;
  position: absolute;
  left: 12px;
  background-color: #cacaca;
  top: 15px;
  z-index: 1;
}
</style>
