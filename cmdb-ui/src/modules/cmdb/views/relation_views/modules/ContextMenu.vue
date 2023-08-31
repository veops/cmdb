<template>
  <a-dropdown :trigger="['contextmenu']">
    <a-menu slot="overlay" @click="({ key: menuKey }) => this.onContextMenuClick(this.treeKey, menuKey)">
      <a-menu-item v-for="item in menuList" :key="item.id">新增{{ item.alias }}</a-menu-item>
      <a-menu-item v-if="showDelete" key="delete">删除节点</a-menu-item>
    </a-menu>
    <div
      :style="{
        width: '100%',
        display: 'inline-flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }"
      @click="clickNode"
    >
      <span
        :style="{
          display: 'flex',
          overflow: 'hidden',
          width: '100%',
          textOverflow: 'ellipsis',
          whiteSpace: 'nowrap',
          alignItems: 'center',
        }"
      >
        <template v-if="icon">
          <img
            v-if="icon.split('$$')[2]"
            :src="`/api/common-setting/v1/file/${icon.split('$$')[3]}`"
            :style="{ maxHeight: '14px', maxWidth: '14px' }"
          />
          <ops-icon
            v-else
            :style="{
              color: icon.split('$$')[1],
              fontSize: '14px',
            }"
            :type="icon.split('$$')[0]"
          />
        </template>
        <span
          :style="{
            display: 'inline-block',
            width: '16px',
            height: '16px',
            borderRadius: '50%',
            backgroundColor: '#d3d3d3',
            color: '#fff',
            textAlign: 'center',
            lineHeight: '16px',
            fontSize: '12px',
          }"
          v-else
        >{{ ciTypeName ? ciTypeName[0].toUpperCase() : 'i' }}</span
        >
        <span :style="{ marginLeft: '5px' }">{{ this.title }}</span>
      </span>
      <a-icon :style="{ fontSize: '10px' }" v-if="childLength && !isLeaf" :type="switchIcon"></a-icon>
    </div>
  </a-dropdown>
</template>

<script>
export default {
  name: 'ContextMenu',
  props: {
    title: {
      type: String,
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
    currentViews: {
      type: Object,
      default: () => {},
    },
    id2type: {
      type: Object,
      default: () => {},
    },
    isLeaf: {
      type: Boolean,
      default: () => false,
    },
    ciTypes: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      switchIcon: 'down',
    }
  },
  computed: {
    childLength() {
      const reg = /(?<=\()\S+(?=\))/g
      return Number(this.title.match(reg)[0])
    },
    splitTreeKey() {
      return this.treeKey.split('@^@')
    },
    _tempTree() {
      return this.splitTreeKey[this.splitTreeKey.length - 1].split('%')
    },
    _typeIdIdx() {
      return this.levels.findIndex((level) => level[0] === Number(this._tempTree[1])) // 当前节点在levels中的index
    },
    showDelete() {
      if (this._typeIdIdx === 0) {
        // 如果是第一层节点，则不能删除
        return false
      }
      return true
    },
    menuList() {
      let _menuList = []
      if (this._typeIdIdx > -1 && this._typeIdIdx < this.levels.length - 1) {
        // 不是叶子节点
        const id = Number(this.levels[this._typeIdIdx + 1])
        _menuList = [
          {
            id,
            alias: this.id2type[id].alias || this.id2type[id].name,
          },
        ]
      } else {
        // 叶子节点
        _menuList = this.currentViews.node2show_types[this._tempTree[1]].map((item) => {
          return { id: item.id, alias: item.alias || item.name }
        })
      }
      return _menuList
    },
    icon() {
      const _split = this.treeKey.split('@^@')
      const currentNodeTypeId = _split[_split.length - 1].split('%')[1]
      const _find = this.ciTypes.find((type) => type.id === Number(currentNodeTypeId))
      return _find?.icon || null
    },
    ciTypeName() {
      const _split = this.treeKey.split('@^@')
      const currentNodeTypeId = _split[_split.length - 1].split('%')[1]
      const _find = this.ciTypes.find((type) => type.id === Number(currentNodeTypeId))
      return _find?.name || ''
    },
  },
  methods: {
    onContextMenuClick(treeKey, menuKey) {
      this.$emit('onContextMenuClick', treeKey, menuKey)
    },
    clickNode() {
      this.$emit('onNodeClick', this.treeKey)
      this.switchIcon = this.switchIcon === 'down' ? 'up' : 'down'
    },
  },
}
</script>

<style></style>
