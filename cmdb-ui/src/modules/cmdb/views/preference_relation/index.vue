<template>
  <div class="preference-relation-wrapper">
    <div class="ci-type-relation">
      <div class="ci-type-relation-header">
        <a-space>
          <a-button
            v-if="!isEdit"
            type="primary"
            size="small"
            @click="
              () => {
                isEdit = true
              }
            "
          >{{ $t('cmdb.preference_relation.newServiceTree') }}</a-button
          >
          <template v-else>
            <a-button type="primary" size="small" @click="openServiceTreeModal({}, 'add')">{{ $t('save') }}</a-button>
            <a-button
              type="primary"
              size="small"
              ghost
              @click="
                () => {
                  isEdit = false
                  checkedNodes = []
                }
              "
            >{{ $t('cancel') }}</a-button
            >
          </template>
          <a-button size="small" @click="handleSave">{{ $t('cmdb.preference_relation.saveLayout') }}</a-button>
          <span>{{ $t('cmdb.preference_relation.tips5') }}</span>
        </a-space>
      </div>
      <SeeksRelationGraph v-if="isPullConfig" ref="ciTypeRelationGraph" :options="graphOptions">
        <div slot="node" slot-scope="{ node }">
          <a-checkbox
            v-if="isEdit"
            :checked="checkedNodes.includes(node.id)"
            @change="(e) => checked(e, node)"
          ></a-checkbox>
          <span :style="{ marginLeft: '5px' }">{{ node.text }}</span>
        </div>
      </SeeksRelationGraph>
    </div>
    <template v-if="relationViews.views && !loading">
      <a-row :gutter="4">
        <a-col
          :xl="12"
          :lg="12"
          :md="12"
          :sm="24"
          :xs="24"
          :key="`${view}`"
          v-for="view in Object.keys(relationViews.views)"
        >
          <div class="relation-views">
            <h3 :style="{ padding: '10px 0 0 20px' }">{{ view }}</h3>
            <a
              class="relation-views-edit"
              @click="openServiceTreeModal({ name: view }, 'edit')"
            ><ops-icon
              type="icon-xianxing-edit"
            /></a>
            <a-popconfirm :title="$t('cmdb.ciType.confirmDelete', { name: `${view}` })" @confirm="confirmDelete(view)">
              <a class="relation-views-close"><a-icon type="close"/></a>
            </a-popconfirm>
            <div :style="{ height: '250px' }">
              <SeeksRelationGraph ref="relationViewsGraph" :options="relationViewOptions"></SeeksRelationGraph>
            </div>
          </div>
        </a-col>
      </a-row>
    </template>
    <ServiceTreeModal ref="serviceTreeModal" @submitServiceTree="submitServiceTree" />
  </div>
</template>

<script>
import _ from 'lodash'
import router, { resetRouter } from '@/router'
import store from '@/store'
import SeeksRelationGraph from '@/modules/cmdb/3rd/relation-graph'
import { getCITypeRelations } from '@/modules/cmdb/api/CITypeRelation'
import {
  getRelationView,
  deleteRelationView,
  subscribeRelationView,
  putRelationView,
} from '@/modules/cmdb/api/preference'
import { getSystemConfig, saveSystemConfig } from '../../api/system_config'
import ServiceTreeModal from './serviceTreeModal.vue'
export default {
  name: 'PreferenceRelation',
  components: { SeeksRelationGraph, ServiceTreeModal },
  data() {
    const defaultOptions = {
      allowShowMiniToolBar: false,
      allowShowMiniNameFilter: false,
      defaultFocusRootNode: false,
      defaultNodeColor: 'rgba(230, 247, 255, 1)',
      defaultNodeFontColor: 'rgba(33, 32, 32, 1)',
    }
    const graphOptions = {
      ...defaultOptions,
      layouts: [
        {
          layoutName: 'center',
          distance_coefficient: 1,
          layoutClassName: 'seeks-layout-center',
        },
      ],
    }
    const relationViewOptions = {
      ...defaultOptions,
      disableZoom: true,
      layouts: [
        {
          layoutName: 'tree',
          from: 'left',
          layoutClassName: 'seeks-layout-center',
        },
      ],
    }
    return {
      graphOptions,
      relationViewOptions,
      isEdit: false,
      relationViews: {},
      graphJsonData: {},
      checkedNodes: [],
      isPullConfig: false,
      loading: false,
    }
  },
  async created() {
    await getSystemConfig({ name: 'ci_type_relation_layout' }).then((res) => {
      this.config = res || {}
      if (this.config && this.config.option) {
        const _graphOptions = _.cloneDeep(this.graphOptions)
        _graphOptions.layouts[0].layoutName = 'fixed'
        this.graphOptions = _graphOptions
      }
      this.isPullConfig = true
    })
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.getMainData()
      this.getViewsData()
    },
    async getMainData() {
      const { relations: ciTypeRelations } = await getCITypeRelations()
      const nodes = []
      const links = []
      ciTypeRelations.forEach((item) => {
        links.push({
          from: `${item.parent_id}`,
          to: `${item.child_id}`,
          text: item.relation_type.name,
          disableDefaultClickEffect: true,
        })
        if (nodes.findIndex((node) => String(node.id) === String(item.child_id)) < 0) {
          const _find =
            this.config && this.config.option ? this.config.option.find((n) => n.id === `${item.child_id}`) : undefined
          nodes.push({
            id: `${item.child_id}`,
            name: item.child.alias || item.child.name,
            nodeShape: 1,
            borderWidth: -1,
            disableDefaultClickEffect: true,
            x: _find?.x ?? 500,
            y: _find?.y ?? 500,
          })
        }
        if (nodes.findIndex((node) => String(node.id) === String(item.parent_id)) < 0) {
          const _find =
            this.config && this.config.option ? this.config.option.find((n) => n.id === `${item.parent_id}`) : undefined
          nodes.push({
            id: `${item.parent_id}`,
            name: item.parent.alias || item.parent.name,
            nodeShape: 1,
            borderWidth: -1,
            disableDefaultClickEffect: true,
            x: _find?.x ?? 500,
            y: _find?.y ?? 500,
          })
        }
      })
      const _from = links.map((item) => item.from)
      const _to = links.map((item) => item.to)
      const rootId = this.findMost([..._from, _to])
      const _graphJsonData = {
        rootId,
        nodes,
        links,
      }
      console.log(_.cloneDeep(_graphJsonData))
      this.graphJsonData = _graphJsonData
      this.$nextTick(() => {
        this.$refs.ciTypeRelationGraph.setJsonData(_graphJsonData, (res) => {
          console.log(this.$refs.ciTypeRelationGraph.getNodes())
        })
      })
    },
    findMost(arr) {
      const hash = {}
      let maxNum = 0
      let maxEle = null
      for (var i = 0; i < arr.length; i++) {
        hash[arr[i]] === undefined ? (hash[arr[i]] = 1) : hash[arr[i]]++
        if (hash[arr[i]] > maxNum) {
          maxEle = arr[i]
          maxNum = hash[arr[i]]
        }
      }
      return maxEle
    },
    async getViewsData() {
      this.loading = true
      const data = await getRelationView()
      this.relationViews = data
      const { views } = data
      Object.keys(views).forEach((item, index) => {
        const nodes = []
        const links = []
        views[`${item}`].topo_flatten.forEach((nodeId, idx) => {
          nodes.push({
            id: `${nodeId}`,
            name: data.id2type[nodeId].alias,
            nodeShape: 1,
            borderWidth: -1,
            disableDefaultClickEffect: true,
          })
          if (idx !== views[`${item}`].topo_flatten.length - 1) {
            links.push({
              from: `${nodeId}`,
              to: `${views[`${item}`].topo_flatten[idx + 1]}`,
            })
          }
        })
        const _graphJsonData = {
          rootId: `${views[`${item}`].topo_flatten[0]}`,
          nodes,
          links,
        }

        this.$nextTick(() => {
          this.$refs.relationViewsGraph[index].setJsonData(_graphJsonData)
        })
        this.loading = false
      })
    },
    checked(e, node) {
      if (e.target.checked) {
        const graph = this.$refs.ciTypeRelationGraph
        if (!graph.getNodeById(node.id).targetTo.length) {
          this.$message.warning(`${node.text} ` + this.$t('cmdb.preference_relation.childNodesNotFound'))
          return
        }
        if (!this.checkedNodes.length) {
          this.checkedNodes.push(node.id)
        } else if (this.checkedNodes.length === 1) {
          const currentCheckedNode = graph.getNodeById(this.checkedNodes[0])
          this.pushNodeId(currentCheckedNode, currentCheckedNode, node)
        } else if (this.checkedNodes.length >= 2) {
          const startNode = graph.getNodeById(this.checkedNodes[0])
          const endNode = graph.getNodeById(this.checkedNodes[this.checkedNodes.length - 1])
          this.pushNodeId(startNode, endNode, node)
        }
      } else {
        const idx = this.checkedNodes.findIndex((item) => item === node.id)
        if (idx > -1) {
          if (this.checkedNodes.slice(0, idx).length >= 2) {
            this.checkedNodes = this.checkedNodes.slice(0, idx)
            return
          }
          if (this.checkedNodes.slice(idx + 1, this.checkedNodes.length).length >= 2) {
            this.checkedNodes = this.checkedNodes.slice(idx + 1, this.checkedNodes.length)
            return
          }
          this.checkedNodes = []
        }
      }
    },
    pushNodeId(startNode, endNode, node) {
      const idFrom = startNode.targetFrom.findIndex((item) => item.id === node.id)
      const idTo = endNode.targetTo.findIndex((item) => item.id === node.id)
      if (idFrom <= -1 && idTo <= -1) {
        this.$message.warning(`${node.text} ` + this.$t('cmdb.preference_relation.tips1'))
        return
      }
      if (idFrom > -1) {
        this.checkedNodes.unshift(node.id)
      }
      if (idTo > -1) {
        this.checkedNodes.push(node.id)
      }
    },
    openServiceTreeModal(treeData, type) {
      if (type === 'add' && this.checkedNodes.length < 2) {
        this.$message.warning(this.$t('cmdb.preference_relation.tips3'))
        return
      }
      let _treeData = { ...treeData }
      if (type === 'edit') {
        const { name } = _treeData
        _treeData = {
          ...treeData,
          ...(this.relationViews?.views[name]?.option ?? {}),
          is_public: this.relationViews?.views[name]?.is_public ?? true,
        }
      }
      this.$refs.serviceTreeModal.open(_treeData, type)
    },
    async submitServiceTree(treeData, type, originName) {
      const { name, is_public, is_show_leaf_node, is_show_tree_node, sort } = treeData
      if (type === 'add') {
        const cr_ids = []
        this.checkedNodes.forEach((item, idx) => {
          if (idx !== this.checkedNodes.length - 1) {
            cr_ids.push({ parent_id: Number(item), child_id: Number(this.checkedNodes[idx + 1]) })
          }
        })
        await subscribeRelationView({
          cr_ids,
          name,
          is_public,
          option: { is_show_leaf_node, is_show_tree_node, sort, is_public },
        })
      } else {
        const _name = name === originName ? name : originName
        const topo_flatten = this.relationViews?.views[_name]?.topo_flatten ?? []
        const name2id = this.relationViews?.name2id.find((item) => item[0] === _name)
        const cr_ids = []
        topo_flatten.forEach((item, idx) => {
          if (idx !== topo_flatten.length - 1) {
            cr_ids.push({ parent_id: Number(item), child_id: Number(topo_flatten[idx + 1]) })
          }
        })
        console.log(originName, name, cr_ids, name2id)
        await putRelationView(name2id[1], {
          cr_ids,
          name,
          is_public,
          option: { is_show_leaf_node, is_show_tree_node, sort, is_public },
        })
      }
      this.resetRoute()
      this.getViewsData()
      this.isEdit = false
      this.checkedNodes = []
    },
    async confirmDelete(viewName) {
      await deleteRelationView(viewName)
      this.getViewsData()
      this.resetRoute()
    },
    resetRoute() {
      resetRouter()
      const roles = store.getters.roles
      store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
        router.addRoutes(store.getters.appRoutes)
      })
    },
    handleSave() {
      console.log(this.$refs.ciTypeRelationGraph.getNodes())
      const nodes = this.$refs.ciTypeRelationGraph.getNodes()
      if (nodes && nodes.length) {
        saveSystemConfig({
          name: 'ci_type_relation_layout',
          option: nodes.map((item) => {
            return {
              id: item.id,
              x: item.x,
              y: item.y,
            }
          }),
        }).then((res) => {
          this.$message.success(this.$t('saveSuccess'))
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.preference-relation-wrapper {
  overflow: hidden;
  .ci-type-relation {
    background-color: #fff;
    position: relative;
    height: 600px;
    width: 100%;
    .ci-type-relation-header {
      position: absolute;
      top: 20px;
      left: 20px;
      z-index: 10;
    }
  }
  .relation-views {
    background-color: #fff;
    margin-top: 5px;
    position: relative;
    .relation-views-edit,
    .relation-views-close {
      position: absolute;
      z-index: 10;
      right: 60px;
      top: 10px;
    }
    .relation-views-edit {
      right: 46px;
    }
    .relation-views-close {
      right: 20px;
    }
  }
}
</style>
