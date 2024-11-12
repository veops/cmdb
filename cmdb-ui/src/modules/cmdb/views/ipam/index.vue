<template>
  <TwoColumnLayout
    class="ipam"
    appName="cmdb-ipam"
    calcBasedParent
  >
    <template #one>
      <IPAMTree
        v-if="subnetCIType"
        :treeData="treeData"
        :treeKey="treeKey"
        :subnetCIType="subnetCIType"
        @refreshData="refreshData"
        @updateTreeKey="updateTreeKey"
      />
    </template>

    <template #two>
      <a-tabs
        :activeKey="tabKey"
        @change="handleTabChange"
      >
        <a-tab-pane
          v-for="(item) in tabs"
          :key="item.key"
          :tab="$t(item.title)"
        >
        </a-tab-pane>
      </a-tabs>

      <Overview
        v-if="tabKey === 'overview'"
        ref="overviewRef"
        :nodeId="treeKey"
      />
      <template v-if="addressCIType">
        <Address
          v-if="tabKey === 'address'"
          :nodeData="nodeData"
          :addressCIType="addressCIType"
        />
        <IPSearch
          v-if="tabKey === 'ipSearch'"
          :addressCIType="addressCIType"
        />
      </template>
      <template v-if="subnetCIType">
        <SubnetList
          v-if="tabKey === 'subnet'"
          ref="subnetListRef"
          :subnetCIType="subnetCIType"
          @delete="getTreeData"
        />
      </template>
      <HistoryLog
        v-if="tabKey === 'history'"
        ref="historyRef"
      />
    </template>
  </TwoColumnLayout>
</template>

<script>
import { getIPAMSubnet } from '@/modules/cmdb/api/ipam.js'
import { getCIType } from '@/modules/cmdb/api/CIType.js'
import { SUB_NET_CITYPE_NAME, ADDRESS_CITYPE_NAME, SCOPE_CITYPE_NAME } from './constants.js'

import TwoColumnLayout from '@/components/TwoColumnLayout'
import IPAMTree from './components/ipamTree.vue'
import Overview from './modules/overview/index.vue'
import Address from './modules/address/index.vue'
import IPSearch from './modules/ipSearch/index.vue'
import SubnetList from './modules/subnetList/index.vue'
import HistoryLog from './modules/history/index.vue'

const TAB_STORAGE_KEY = 'ops_ipam_tab_active'
const TREE_STORAGE_KEY = 'ops_ipam_tree_active'

export default {
  name: 'IPAM',
  components: {
    TwoColumnLayout,
    IPAMTree,
    IPSearch,
    SubnetList,
    Address,
    HistoryLog,
    Overview
  },
  data() {
    return {
      tabKey: localStorage.getItem(TAB_STORAGE_KEY) || 'overview',
      treeKey: localStorage.getItem(TREE_STORAGE_KEY) || 'all',

      tabs: [
        {
          key: 'overview',
          title: 'cmdb.ipam.overview'
        },
        {
          key: 'address',
          title: 'cmdb.ipam.addressAssign'
        },
        {
          key: 'ipSearch',
          title: 'cmdb.ipam.ipSearch'
        },
        {
          key: 'subnet',
          title: 'cmdb.ipam.subnetList'
        },
        {
          key: 'history',
          title: 'cmdb.ipam.history'
        }
      ],
      treeData: [],
      subnetCIType: null,
      addressCIType: null,
    }
  },
  computed: {
    nodeData() {
      return this.findNodeById(this.treeData, this.treeKey)
    }
  },
  watch: {
    tabKey: {
      deep: true,
      immediate: true,
      handler(key) {
        switch (key) {
          case 'subnet':
            if (!this.subnetCITYpe) {
              this.getSubnetCIType()
            }
            break
          case 'address':
          case 'ipSearch':
            if (!this.addressCIType) {
              this.getAddressCIType()
            }
            break
          default:
            break
        }
      }
    }
  },
  mounted() {
    this.getSubnetCIType()
    this.getTreeData()
  },
  methods: {
    async getSubnetCIType() {
      const res = await getCIType(SUB_NET_CITYPE_NAME)
      this.subnetCIType = res?.ci_types?.[0] || {}
    },

    async getAddressCIType() {
      const res = await getCIType(ADDRESS_CITYPE_NAME)
      this.addressCIType = res?.ci_types?.[0] || {}
    },

    async getTreeData() {
      const res = await getIPAMSubnet()
      let treeData = []

      if (res?.result?.length) {
        treeData = res.result.map((data) => {
          return this.handleTreeData(data, res.type2name)
        })
      }

      const allCount = treeData.reduce((acc, cur) => acc + cur.count, 0)
      const rootShowSubnetBtn = treeData.every((item) => item.ci_type === SUB_NET_CITYPE_NAME)
      const rootShowCatalogBtn = treeData.every((item) => item.ci_type === SCOPE_CITYPE_NAME)

      treeData.unshift({
        key: 'all',
        title: this.$t('all'),
        count: allCount,
        icon: 'veops-entire_network_',
        iconColor: '#2F54EB',
        showCatalogBtn: rootShowCatalogBtn,
        showSubnetBtn: rootShowSubnetBtn,
        parentId: '',
        class: 'ipam-tree-node-all'
      })

      this.treeData = treeData
    },

    handleTreeData(data, type2name, parentId = '') {
      const title = data?.[type2name?.[data?._type]] || ''
      const isSubnet = data?.ci_type === SUB_NET_CITYPE_NAME
      const icon = isSubnet ? 'veops-subnet' : 'veops-folder'
      const iconColor = isSubnet ? '#CACDD9' : ''
      const key = String(data._id)

      if (!data?.children?.length) {
        return {
          key,
          title,
          count: isSubnet ? 1 : 0,
          icon,
          iconColor,
          showCatalogBtn: !isSubnet,
          showSubnetBtn: true,
          isSubnet,
          parentId,
          ...data
        }
      }

      const children = data.children.map((item) => {
        return this.handleTreeData(item, type2name, key)
      })

      const showSubnetBtn = children.every((item) => item.ci_type === SUB_NET_CITYPE_NAME)
      return {
        key,
        title,
        icon,
        iconColor,
        showCatalogBtn: !isSubnet && !showSubnetBtn,
        showSubnetBtn: showSubnetBtn,
        isSubnet,
        parentId,
        ...data,
        children,
        count: children.reduce((acc, item) => {
          return acc + item.count
        }, 0)
      }
    },

    handleTabChange(key) {
      if (key !== this.tabKey) {
        this.tabKey = key
        localStorage.setItem(TAB_STORAGE_KEY, key)
      }
    },

    updateTreeKey(key) {
      this.treeKey = key
      localStorage.setItem(TREE_STORAGE_KEY, key)
    },

    findNodeById(nodes, key) {
      for (const node of nodes) {
        if (node.key === key) {
          return node
        }
        if (node.children) {
          const foundNode = this.findNodeById(node.children, key)
          if (foundNode) {
            return foundNode
          }
        }
      }
      return null
    },

    refreshData() {
      this.getTreeData()
      switch (this.tabKey) {
        case 'overview':
          if (this.$refs.overviewRef) {
            this.$refs.overviewRef.initData()
          }
          break
        case 'subnet':
          if (this.$refs.subnetListRef) {
            this.$refs.subnetListRef.getTableData()
          }
          break
        case 'history':
          if (this.$refs.historyRef) {
            this.$refs.historyRef.refreshData()
          }
          break
        default:
          break
      }
    }
  }
}
</script>

<style lang="less" scoped>
.ipam {
  /deep/ .ant-tabs {
    display: inline-block;
  }
}
</style>
