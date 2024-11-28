<template>
  <div class="dcim-tree">
    <div class="dcim-tree-header">
      <a-input
        v-model="searchValue"
        class="dcim-tree-header-search"
        :placeholder="$t('placeholder1')"
      />
      <a-dropdown>
        <a-button class="dcim-tree-header-more">
          <ops-icon type="veops-more" />
        </a-button>
        <a-menu slot="overlay">
          <a-menu-item
            v-for="(type) in rootAction"
            :key="type"
            @click="openForm({
              dcimType: type
            })"
          >
            <a>
              <a-icon
                type="plus-circle"
                class="dcim-tree-header-menu-icon"
              />
              {{ $t(addActionTitle[type]) }}
            </a>
          </a-menu-item>

          <a-menu-item
            class="dcim-tree-header-calc"
            @click="calcUnitFreeCount"
          >
            <a>
              <ops-icon
                type="veops-refresh"
                class="dcim-tree-header-menu-icon"
              />
              {{ $t('cmdb.dcim.calcUnitFreeCount') }}
            </a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
    </div>

    <div class="dcim-tree-main">
      <a-tree
        v-if="treeData.length"
        autoExpandParent
        :treeData="filterTreeData"
        :selectedKeys="treeKey ? [treeKey] : []"
        :defaultExpandedKeys="treeKey ? [treeKey] : []"
      >
        <template #title="treeNodeData">
          <div
            class="dcim-tree-node"
            @click="clickTreeNode(treeNodeData)"
          >
            <ops-icon
              :type="treeNodeData.icon"
              class="dcim-tree-node-icon"
              :style="{ color: treeNodeData.iconColor }"
            />
            <a-tooltip :title="treeNodeData.title">
              <span
                class="dcim-tree-node-title"
                :style="{
                  color: treeKey === treeNodeData.key ? '#2F54EB' : ''
                }"
              >
                {{ treeNodeData.title }}
              </span>
            </a-tooltip>

            <div class="dcim-tree-node-right">
              <span
                v-if="treeNodeData.count"
                class="dcim-tree-node-count"
              >
                {{ treeNodeData.count }}
              </span>

              <a-dropdown>
                <a class="dcim-tree-node-action">
                  <ops-icon type="veops-more" />
                </a>

                <a-menu slot="overlay">
                  <a-menu-item
                    v-if="treeNodeData.addType"
                    @click="openForm({
                      dcimType: treeNodeData.addType,
                      parentId: treeNodeData._id
                    })"
                  >
                    <a-icon type="plus-circle" />
                    {{ $t(addActionTitle[treeNodeData.addType]) }}
                  </a-menu-item>
                  <a-menu-item
                    @click="openDetail(treeNodeData)"
                  >
                    <a-icon type="unordered-list" />
                    {{ $t('cmdb.dcim.viewDetail') }}
                  </a-menu-item>
                  <a-menu-item
                    @click="openForm({
                      dcimType: treeNodeData.dcimType,
                      parentId: treeNodeData.parentId,
                      nodeId: treeNodeData._id
                    })"
                  >
                    <ops-icon type="veops-edit" />
                    {{ $t('cmdb.dcim.editNode') }}
                  </a-menu-item>
                  <a-menu-item @click="deleteNode(treeNodeData)">
                    <ops-icon type="veops-delete" />
                    {{ $t('cmdb.dcim.deleteNode') }}
                  </a-menu-item>
                </a-menu>
              </a-dropdown>
            </div>
          </div>
        </template>
      </a-tree>
    </div>

    <CIDetailDrawer
      ref="CIdetailRef"
      :typeId="viewDetailCITypeId"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { DCIM_TYPE, DCIM_TYPE_NAME_MAP } from '../constants.js'
import { deleteDCIM, calcUnitFreeCount } from '@/modules/cmdb/api/dcim.js'
import CIDetailDrawer from '@/modules/cmdb/views/ci/modules/ciDetailDrawer.vue'

export default {
  name: 'DCIMTree',
  components: {
    CIDetailDrawer
  },
  props: {
    treeData: {
      type: Array,
      default: () => []
    },
    treeKey: {
      type: [String, Number],
      default: ''
    }
  },
  data() {
    return {
      searchValue: '',
      addActionTitle: {
        [DCIM_TYPE.REGION]: 'cmdb.dcim.addRegion',
        [DCIM_TYPE.IDC]: 'cmdb.dcim.addIDC',
        [DCIM_TYPE.SERVER_ROOM]: 'cmdb.dcim.addServerRoom',
      },
      rootAction: [
        DCIM_TYPE.REGION,
        DCIM_TYPE.IDC
      ],

      viewDetailCITypeId: 0,
      viewDetailAttrObj: {},

      calculatedFreeUnitCount: false,
    }
  },
  computed: {
    filterTreeData() {
      if (this.searchValue) {
        const treeData = _.cloneDeep(this.treeData)

        // 过滤筛选
        const filterTreeData = treeData.filter((data) => {
          return this.handleTreeDataBySearch(data)
        })

        // 处理同级父节点
        const newTreeData = []
        treeData.forEach((item) => {
          const filterNodeData = filterTreeData.find((data) => data.key === item.key)
          if (filterNodeData) {
            newTreeData.push(filterNodeData)
          } else if (
            filterTreeData.some((data) => data.parentId === item.key)
          ) {
            newTreeData.push(item)
          }
        })

        return newTreeData
      }

      return this.treeData
    }
  },
  inject: ['getTreeData'],
  provide() {
    return {
      handleSearch: this.refreshTreeData,
      attrList: () => {
        return this.viewDetailAttrObj?.attributes || []
      },
      attributes: () => {
        return this.viewDetailAttrObj
      }
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

    openForm({
      dcimType,
      nodeId = undefined,
      parentId = ''
    }) {
      this.$emit('openForm', {
        dcimType,
        nodeId,
        parentId
      })
    },

    deleteNode(node) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('confirmDelete'),
        onOk: async () => {
          await deleteDCIM(node.dcimType, node._id)

          if (node.key === this.treeKey) {
            this.$emit('updateTreeKey', '')
          }

          this.$nextTick(() => {
            this.refreshTreeData()
          })
        },
      })
    },

    refreshTreeData() {
      this.getTreeData()
    },

    clickTreeNode(node) {
      if (node.dcimType === DCIM_TYPE.SERVER_ROOM) {
        this.$emit('updateTreeKey', node.key)
      }
    },

    async openDetail(node) {
      this.$emit('getAttrList', DCIM_TYPE_NAME_MAP[node.dcimType], node.dcimType, (allAttrList) => {
        this.viewDetailCITypeId = node._type
        this.viewDetailAttrObj = allAttrList[node.dcimType]

        this.$nextTick(() => {
          this.$refs.CIdetailRef.create(node._id)
        })
      })
    },

    calcUnitFreeCount() {
      if (this.calculatedFreeUnitCount) {
        this.$message.info(this.$t('cmdb.dcim.calcUnitFreeCountTip'))
      } else {
        this.$confirm({
          title: this.$t('tip'),
          content: this.$t('cmdb.dcim.calcUnitFreeCountTip2'),
          onOk: () => {
            calcUnitFreeCount().then(() => {
              this.calculatedFreeUnitCount = true
              this.$message.success(this.$t('cmdb.dcim.calcUnitFreeCountTip1'))
            })
          }
        })
      }
    }
  }
}
</script>

<style lang="less" scoped>
.dcim-tree {
  &-header {
    display: flex;
    align-items: center;
    column-gap: 14px;

    &-search {
      width: 100%;
    }

    &-more {
      flex-shrink: 0;
      width: 32px;
      padding: 0px;
    }

    &-calc {
      border-top: dashed 1px #e8e8e8;
    }

    &-menu-icon {
      margin-right: 6px;
    }
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

      .ipam-tree-node_hide_expand {
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
      .dcim-tree-node-action {
        display: inline-block;
      }
    }
  }
}
</style>
