<template>
  <div
    :class="{
      'relation-views-node': true,
      'relation-views-node-checkbox': showCheckbox,
    }"
    @click="clickNode"
  >
    <span class="relation-views-node-switch">
      <a-icon v-if="childLength && !isLeaf" :type="switchIcon"></a-icon>
    </span>
    <span class="relation-views-node-content">
      <a-checkbox @click.stop="clickCheckbox" class="relation-views-node-checkbox" v-if="showCheckbox" />
      <template v-if="icon">
        <img
          v-if="icon.includes('$$') && icon.split('$$')[2]"
          :src="`/api/common-setting/v1/file/${icon.split('$$')[3]}`"
          :style="{ maxHeight: '14px', maxWidth: '14px' }"
        />
        <ops-icon
          v-else-if="icon.includes('$$') && icon.split('$$')[0]"
          :style="{
            color: icon.split('$$')[1],
            fontSize: '14px',
          }"
          :type="icon.split('$$')[0]"
        />
        <span class="relation-views-node-icon" v-else>{{ icon ? icon[0].toUpperCase() : 'i' }}</span>
      </template>
      <span class="relation-views-node-title" v-if="!isEditNodeName" :title="title">{{ title }}</span>
      <a-input
        ref="input"
        @blur="changeNodeName"
        @pressEnter="
          () => {
            $refs.input.blur()
          }
        "
        size="small"
        v-else
        v-model="editNodeName"
        :style="{ marginLeft: '5px' }"
      />
      <span class="relation-views-node-number">{{ number }}</span>
      <a-dropdown overlayClassName="relation-views-node-dropdown" :overlayStyle="{ width: '200px' }">
        <a-menu slot="overlay" @click="({ key: menuKey }) => onContextMenuClick(this.treeKey, menuKey)">
          <template v-if="showBatchLevel === null">
            <a-divider orientation="left">{{ $t('cmdb.relation') }}</a-divider>
            <a-menu-item
              v-for="item in menuList"
              :key="item.id"
            ><a-icon type="plus-circle" />{{ $t('add') }} {{ item.alias }}</a-menu-item
            >
            <a-menu-item
              v-if="showDelete"
              key="delete"
            ><ops-icon type="icon-xianxing-delete" />{{
              $t('cmdb.serviceTree.deleteNode', { name: title })
            }}</a-menu-item
            >
            <a-divider orientation="left">{{ $t('cmdb.components.perm') }}</a-divider>
            <a-menu-item key="grant"><a-icon type="user-add" />{{ $t('grant') }}</a-menu-item>
            <a-menu-item key="revoke"><a-icon type="user-delete" />{{ $t('revoke') }}</a-menu-item>
            <a-menu-item key="view"><a-icon type="eye" />{{ $t('cmdb.serviceTree.view') }}</a-menu-item>
            <a-menu-divider />
            <a-menu-item
              key="editNodeName"
            ><ops-icon type="icon-xianxing-edit" />{{ $t('cmdb.serviceTree.editNodeName') }}</a-menu-item
            >
            <a-menu-item
              key="batch"
            ><ops-icon type="veops-copy" />{{ $t('cmdb.serviceTree.batch') }}</a-menu-item
            >
          </template>
          <template v-else>
            <a-menu-item
              :disabled="!batchTreeKey || !batchTreeKey.length"
              key="batchGrant"
            ><a-icon type="user-add" />{{ $t('grant') }}</a-menu-item
            >
            <a-menu-item
              :disabled="!batchTreeKey || !batchTreeKey.length"
              key="batchRevoke"
            ><a-icon type="user-delete" />{{ $t('revoke') }}</a-menu-item
            >
            <a-menu-divider />
            <template v-if="showBatchLevel > 0">
              <a-menu-item
                :disabled="!batchTreeKey || !batchTreeKey.length"
                key="batchDelete"
              ><ops-icon type="icon-xianxing-delete" />{{ $t('cmdb.serviceTree.remove') }}</a-menu-item
              >
              <a-menu-divider />
            </template>
            <a-menu-item key="batchCancel"><a-icon type="close-circle" />{{ $t('cancel') }}</a-menu-item>
          </template>
        </a-menu>
        <a-icon class="relation-views-node-operation" type="ellipsis" />
      </a-dropdown>
    </span>
  </div>
</template>

<script>
import { updateCI } from '../../../api/ci.js'
export default {
  name: 'ContextMenu',
  props: {
    title: {
      type: String,
      default: '',
    },
    number: {
      type: Number,
      default: 0,
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
    ciTypeIcons: {
      type: Object,
      default: () => {},
    },
    showBatchLevel: {
      type: Number,
      default: null,
    },
    batchTreeKey: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      switchIcon: 'caret-right',
      isEditNodeName: false,
      editNodeName: '',
    }
  },
  computed: {
    childLength() {
      return this.number
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
      return this.ciTypeIcons[Number(currentNodeTypeId)] ?? null
    },
    showCheckbox() {
      return this.showBatchLevel === this.treeKey.split('@^@').filter((item) => !!item).length - 1
    },
  },
  methods: {
    onContextMenuClick(treeKey, menuKey) {
      if (menuKey === 'editNodeName') {
        this.isEditNodeName = true
        this.editNodeName = this.title
        this.$nextTick(() => {
          this.$refs.input.focus()
        })
        return
      }
      this.$emit('onContextMenuClick', treeKey, menuKey)
    },
    clickNode() {
      this.$emit('onNodeClick', this.treeKey)
      this.switchIcon = this.switchIcon === 'caret-right' ? 'caret-down' : 'caret-right'
    },
    clickCheckbox() {
      this.$emit('clickCheckbox', this.treeKey)
    },
    changeNodeName(e) {
      const value = e.target.value
      if (value !== this.title) {
        const ci = this.treeKey
          .split('@^@')
          .slice(-1)[0]
          .split('%')
        const unique = Object.keys(JSON.parse(ci[2]))[0]
        const ciId = Number(ci[0])

        updateCI(ciId, { [unique]: value }).then((res) => {
          this.$message.success(this.$t('updateSuccess'))
          this.$emit('updateTreeData', ciId, value)
        })
      }
      this.isEditNodeName = false
      this.editNodeName = ''
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';

.relation-views-node {
  width: 100%;
  display: inline-flex;
  justify-content: space-between;
  align-items: center;
  .relation-views-node-switch {
    display: inline-block;
    width: 15px;
    color: @text-color_5;
    i {
      opacity: 0;
      font-size: 10px;
    }
  }
  .relation-views-node-content {
    display: flex;
    overflow: hidden;
    align-items: center;
    width: 100%;
    .relation-views-node-icon {
      display: inline-block;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background-color: #d3d3d3;
      color: #fff;
      text-align: center;
      line-height: 16px;
      font-size: 12px;
    }
    .relation-views-node-title {
      padding-left: 5px;
      text-overflow: ellipsis;
      white-space: nowrap;
      overflow: hidden;
      flex: 1;
      color: @text-color_1;
    }
    .relation-views-node-number {
      color: @text-color_4;
      font-size: 12px;
      margin: 0 5px;
    }
    .relation-views-node-operation {
      opacity: 0;
      width: 15px;
    }
  }
}
.relation-views-node-checkbox {
  > span {
    .relation-views-node-checkbox {
      margin-right: 10px;
    }
    .relation-views-node-title {
      width: calc(100% - 42px);
    }
  }
}

.relation-views-left .ant-tree:hover {
  .relation-views-node .relation-views-node-switch i {
    opacity: 1;
  }
}
</style>

<style lang="less">
@import '~@/style/static.less';
.relation-views-left {
  ul:has(.relation-views-node-checkbox) > li > ul {
    margin-left: 26px;
  }
  ul:has(.relation-views-node-checkbox) {
    margin-left: 0 !important;
  }
  .ant-tree-node-content-wrapper:hover {
    .relation-views-node-operation {
      opacity: 1;
    }
  }
  .ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected,
  .ant-tree li .ant-tree-node-content-wrapper:hover {
    background-color: @primary-color_3;
  }
}

.relation-views-node-dropdown {
  .ant-divider {
    margin: 0;
    .ant-divider-inner-text {
      font-size: 12px;
      color: @text-color_3;
    }
  }
  .ant-dropdown-menu-item {
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>
