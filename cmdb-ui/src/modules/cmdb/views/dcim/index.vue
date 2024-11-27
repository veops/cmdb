<template>
  <TwoColumnLayout
    class="dcim"
    appName="cmdb-dcim"
    calcBasedParent
  >
    <template #one>
      <DCIMTree
        :treeData="treeData"
        :treeKey="treeKey"
        @getAttrList="getAttrList"
        @updateTreeKey="updateTreeKey"
        @openForm="openForm"
      />

      <DCIMForm
        ref="dcimFormRef"
        :allAttrList="allAttrList"
        @ok="handleDCIMFormOk"
      />
    </template>

    <template #two>
      <DCIMMain
        v-if="!initLoading && rackCITYpe.id"
        ref="dcimMainRef"
        :roomId="treeKey"
        :attrObj="allAttrList[DCIM_TYPE.RACK]"
        :rackCITYpe="rackCITYpe"
        :preferenceAttrList="rackPreferenceAttrList"
        @openForm="openForm"
        @refreshTreeData="getTreeData"
      />
    </template>
  </TwoColumnLayout>
</template>

<script>
import { getDCIMTreeView } from '@/modules/cmdb/api/dcim.js'
import { DCIM_CITYPE_NAME, DCIM_TYPE, DCIM_TYPE_NAME_MAP } from './constants.js'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCIType } from '@/modules/cmdb/api/CIType.js'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'

import TwoColumnLayout from '@/components/TwoColumnLayout'
import DCIMTree from './components/dcimTree.vue'
import DCIMForm from './components/dcimForm.vue'
import DCIMMain from './components/dcimMain/index.vue'

const TREE_STORAGE_KEY = 'ops_dcim_tree_active'

export default {
  name: 'DCIM',
  components: {
    TwoColumnLayout,
    DCIMTree,
    DCIMForm,
    DCIMMain
  },
  data() {
    return {
      DCIM_TYPE,
      treeKey: localStorage.getItem(TREE_STORAGE_KEY) || '',
      treeData: [],
      allAttrList: {
        [DCIM_TYPE.REGION]: {},
        [DCIM_TYPE.IDC]: {},
        [DCIM_TYPE.SERVER_ROOM]: {},
        [DCIM_TYPE.RACK]: {}
      },

      initLoading: true,
      rackCITYpe: {},
      rackPreferenceAttrList: []
    }
  },
  async mounted() {
    this.initLoading = true

    try {
      await this.getTreeData()
      await this.getRackData()
    } catch (error) {
      console.log('initData fail', error)
    }

    this.initLoading = false
  },
  provide() {
    return {
      getTreeData: this.getTreeData
    }
  },
  methods: {
    async getTreeData() {
      const res = await getDCIMTreeView()
      let treeData = []

      if (res?.result?.length) {
        treeData = res.result.map((data) => {
          return this.handleTreeData(data, res.type2name)
        })
      }

      const currentNode = this.findNodeById(treeData, this.treeKey)
      if (!currentNode) {
        this.updateTreeKey('')
      }

      const flatRreeData = []
      treeData.forEach((item) => {
        flatRreeData.push({
          ...item,
          class: 'ipam-tree-node_hide_expand',
          children: []
        })
        if (item.children.length) {
          flatRreeData.push(...item.children)
        }
      })

      this.treeData = flatRreeData
    },

    handleTreeData(data, type2name, parentId = '') {
      const title = data?.[type2name?.[data?._type]] || ''
      const dcimType = DCIM_TYPE_NAME_MAP[data.ci_type]
      let icon = ''
      let iconColor = '#A5A9BC'
      let addType = ''

      const key = String(data._id)

      switch (data.ci_type) {
        case DCIM_CITYPE_NAME.REGION:
          icon = 'veops-region'
          iconColor = '#2F54EB'
          addType = DCIM_TYPE.IDC
          break
        case DCIM_CITYPE_NAME.IDC:
          icon = 'veops-IDC'
          addType = DCIM_TYPE.SERVER_ROOM
          break
        case DCIM_CITYPE_NAME.SERVER_ROOM:
          icon = 'a-veops-room1'
          break
        default:
          break
      }

      if (!data?.children?.length) {
        return {
          ...data,
          key,
          title,
          icon,
          iconColor,
          parentId,
          addType,
          dcimType,
          count: data?.rack_count || 0
        }
      }

      const children = data.children.map((item) => {
        return this.handleTreeData(item, type2name, key)
      })

      return {
        ...data,
        key,
        title,
        icon,
        iconColor,
        addType,
        parentId,
        children,
        dcimType,
        count: children.reduce((acc, item) => {
          return acc + item.count
        }, 0)
      }
    },

    findNodeById(nodes, id) {
      for (const node of nodes) {
        if (node.key === id) {
          return node
        }
        if (node.children) {
          const foundNode = this.findNodeById(node.children, id)
          if (foundNode) {
            return foundNode
          }
        }
      }
      return null
    },

    async getRackData() {
      await this.getAttrList(DCIM_CITYPE_NAME.RACK, DCIM_TYPE.RACK)

      const CITypeRes = await getCIType(DCIM_CITYPE_NAME.RACK)
      this.rackCITYpe = CITypeRes?.ci_types?.[0] || {}

      if (this.rackCITYpe.id) {
        const subscribed = await getSubscribeAttributes(this.rackCITYpe.id)
        this.rackPreferenceAttrList = subscribed.attributes
      }
    },

    async getAttrList(id, type, cb) {
      if (Object.keys(this?.allAttrList?.[type] || {})?.length === 0) {
        const res = await getCITypeAttributesById(id)
        this.$set(this.allAttrList, type, res || {})
      }

      if (cb) {
        cb(this.allAttrList)
      }
    },

    async openForm(data) {
      await this.getAttrList(DCIM_TYPE_NAME_MAP[data.dcimType], data.dcimType)

      this.$nextTick(() => {
        this.$refs.dcimFormRef.open(data)
      })
    },

    updateTreeKey(key) {
      this.treeKey = key
      localStorage.setItem(TREE_STORAGE_KEY, key)
    },

    handleDCIMFormOk({
      dcimType,
      editType
    }) {
      switch (dcimType) {
        case DCIM_TYPE.REGION:
        case DCIM_TYPE.IDC:
        case DCIM_TYPE.SERVER_ROOM:
          this.getTreeData()
          break
        case DCIM_TYPE.RACK:
          this.getRackList()
          if (editType === 'create') {
            this.getTreeData()
          }
          break
        default:
          break
      }
    },

    getRackList() {
      if (this.$refs.dcimMainRef) {
        this.$refs.dcimMainRef.getRackList()
      }
    }
  }
}
</script>

<style lang="less" scoped>
</style>
