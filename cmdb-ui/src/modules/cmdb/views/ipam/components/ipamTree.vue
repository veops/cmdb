<template>
  <div class="ipam-tree">
    <a-input
      v-model="searchValue"
      class="ipam-tree-search"
      :placeholder="$t('placeholder1')"
    />

    <div class="ipam-tree-main">
      <a-tree
        v-if="treeData.length"
        autoExpandParent
        :treeData="filterTreeData"
        :selectedKeys="treeKey ? [treeKey] : []"
        :defaultExpandedKeys="treeKey ? [treeKey] : []"
      >
        <template #title="treeNodeData">
          <div
            class="ipam-tree-node"
            @click="clickTreeNode(treeNodeData)"
          >
            <ops-icon
              :type="treeNodeData.icon"
              class="ipam-tree-node-icon"
              :style="{ color: treeNodeData.iconColor }"
            />
            <a-tooltip :title="treeNodeData.title">
              <span
                :class="['ipam-tree-node-title', treeKey === treeNodeData.key ? 'primary-color' : '']"
              >
                {{ treeNodeData.title }}
              </span>
            </a-tooltip>
            <div class="ipam-tree-node-right">
              <span
                v-if="(treeNodeData.key === 'all' && treeNodeData.count) || (treeNodeData.key !== 'all' && treeNodeData.children && treeNodeData.children.length && treeNodeData.count)"
                class="ipam-tree-node-count"
              >
                {{ treeNodeData.count }}
              </span>

              <a-dropdown :getPopupContainer="(trigger) => trigger">
                <a class="ipam-tree-node-action">
                  <ops-icon type="veops-more" />
                </a>
                <a-menu slot="overlay">
                  <a-menu-item
                    v-if="treeNodeData.showCatalogBtn"
                    @click="openCatalogForm(treeNodeData, 'create')"
                  >
                    <ops-icon type="veops-catalog" />
                    {{ $t('cmdb.ipam.addCatalog') }}
                  </a-menu-item>
                  <a-menu-item
                    v-if="treeNodeData.showSubnetBtn"
                    @click="openSubnetForm(treeNodeData, 'create')"
                  >
                    <ops-icon type="veops-increase" />
                    {{ $t('cmdb.ipam.addSubnet') }}
                  </a-menu-item>

                  <template v-if="treeNodeData.key !== 'all'">
                    <a-menu-item
                      v-if="!treeNodeData.isSubnet"
                      @click="openCatalogForm(treeNodeData, 'edit')"
                    >
                      <ops-icon type="veops-edit" />
                      {{ $t('cmdb.ipam.editName') }}
                    </a-menu-item>
                    <a-menu-item
                      v-if="treeNodeData.isSubnet"
                      @click="openSubnetForm(treeNodeData, 'edit')"
                    >
                      <ops-icon type="veops-edit" />
                      {{ $t('cmdb.ipam.editNode') }}
                    </a-menu-item>
                    <a-menu-item @click="deleteNode(treeNodeData)">
                      <ops-icon type="veops-delete" />
                      {{ $t('cmdb.ipam.deleteNode') }}
                    </a-menu-item>
                  </template>
                </a-menu>
              </a-dropdown>
            </div>
          </div>
        </template>
      </a-tree>
    </div>

    <SubnetForm
      ref="subnetFormRef"
      :subnetCIType="subnetCIType"
      @ok="refreshData"
    />

    <CatalogForm
      ref="catalogFormRef"
      @ok="refreshData"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { deleteIPAMSubnet, deleteIPAMScope } from '@/modules/cmdb/api/ipam.js'

import SubnetForm from './subnetForm.vue'
import CatalogForm from './catalogForm.vue'

export default {
  name: 'IPAMTree',
  components: {
    SubnetForm,
    CatalogForm
  },
  props: {
    treeData: {
      type: Array,
      default: () => []
    },
    treeKey: {
      type: [String, Number],
      default: () => ''
    },
    subnetCIType: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      searchValue: ''
    }
  },
  computed: {
    filterTreeData() {
      if (this.searchValue) {
        let treeData = _.cloneDeep(this.treeData)
        treeData = treeData.filter((data) => {
          return this.handleTreeDataBySearch(data)
        })
        return treeData
      }

      return this.treeData
    }
  },
  methods: {
    handleTreeDataBySearch(data) {
      const isMatch = data?.title?.indexOf?.(this.searchValue) !== -1
      if (!data?.children?.length) {
        return isMatch ? data : null
      }

      data.children = data.children.filter((data) => {
        return this.handleTreeDataBySearch(data)
      })
      return isMatch || data.children.length ? data : null
    },

    openCatalogForm(node, type) {
      const nodeId = node?.key && node?.key !== 'all' ? node.key : null
      const name = type === 'edit' ? (node?.title || '') : ''

      this.$refs.catalogFormRef.open({
        nodeId,
        type,
        name
      })
    },

    openSubnetForm(node, type) {
      const nodeId = node?.key && node?.key !== 'all' ? node.key : null
      const parentId = node?.parentId || null

      this.$refs.subnetFormRef.open(nodeId, type, parentId)
    },

    deleteNode(node) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('confirmDelete'),
        onOk: async () => {
          if (node.isSubnet) {
            await deleteIPAMSubnet(node.key)
          } else {
            await deleteIPAMScope(node.key)
          }

          if (node.key === this.treeKey) {
            this.$emit('updateTreeKey', 'all')
          }
          this.$nextTick(() => {
            this.refreshData()
          })
        },
      })
    },

    refreshData() {
      this.$emit('refreshData')
    },

    clickTreeNode(node) {
      this.$emit('updateTreeKey', node.key)
    }
  }
}
</script>

<style lang="less" scoped>
.ipam-tree {
  width: 100%;

  &-search {
    width: 100%;
    height: 26px;
    line-height: 26px;
  }

  &-main {
    width: 100%;
    height: 100%;

    /deep/ .ant-tree {
      .ant-tree-node-content-wrapper {
        width: calc(100% - 24px);
        padding: 0px;
        display: inline-block;
        height: fit-content;

        .ant-tree-title {
          display: inline-block;
          width: 100%;
          padding: 0 6px;
        }
      }

      .ipam-tree-node-all {
        .ant-tree-switcher {
          display: none;
        }

        .ant-tree-node-content-wrapper {
          width: 100%;
        }
      }

      .ant-tree-switcher-icon {
        color: #CACDD9;
      }
    }
  }

  &-node {
    display: flex;
    align-items: center;
    height: 32px;
    cursor: pointer;

    &-icon {
      font-size: 12px;
      flex-shrink: 0;
    }

    &-title {
      margin-left: 6px;
      font-size: 14px;
      font-weight: 400;

      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
    }

    &-right {
      margin-left: auto;
      display: flex;
      align-items: center;
      flex-shrink: 0;
    }

    &-count {
      font-size: 10px;
      font-weight: 400;
      color: #A5A9BC;
    }

    &-action {
      display: none;
      margin-left: 3px;
      font-size: 12px;

      &:hover {
        color: #2F54EB;
      }

      /deep/ .ant-dropdown-menu {
        padding: 4px 0;
      }

      /deep/ .ant-dropdown-menu-item {
        padding: 5px 12px;
      }
    }

    &:hover {
      .ipam-tree-node-action {
        display: inline-block;
      }
    }
  }
}
</style>
