<template>
  <div @click="clickNode" class="tree-views-node">
    <a-icon v-if="childLength && !isLeaf" :type="switchIcon"></a-icon>
    <div v-else></div>
    <div class="tree-views-node-content">
      <span>{{ this.title }}</span>
      <span>{{ childLength }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TreeViewsNode',
  props: {
    title: {
      type: [String, Number],
      default: '',
    },
    treeKey: {
      type: String,
      default: '',
    },
    levels: {
      type: Array,
      default: () => [],
    },
    isLeaf: {
      type: Boolean,
      default: () => false,
    },
    childLength: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      switchIcon: 'caret-right',
    }
  },
  computed: {},
  methods: {
    clickNode() {
      this.$emit('onNodeClick', this.treeKey)
      this.switchIcon = this.switchIcon === 'caret-right' ? 'caret-down' : 'caret-right'
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.tree-views-node {
  width: 100%;
  display: inline-flex;
  justify-content: space-between;
  align-items: center;
  > div:first-child {
    width: 10px;
  }
  i {
    font-size: 10px;
    color: @text-color_5;
  }
  .tree-views-node-content {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    margin-left: 5px;
    width: calc(100% - 10px);
    > span:first-child {
      width: calc(100% - 30px);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      color: @text-color_1;
    }
    > span:last-child {
      color: @text-color_4;
    }
  }
}
</style>
