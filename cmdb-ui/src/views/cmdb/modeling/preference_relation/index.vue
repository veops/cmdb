<template>
  <div>
    <a-card :bordered="true" title="关系视图定义面板">
      <a-card-meta description="方法1. 右键选择树节点(推荐)"></a-card-meta>
      <a-card-meta description="方法2. 先打开右上角的开关，再选择树的节点"></a-card-meta>
      <a-switch
        slot="extra"
        @change="toggleSelect"
        checkedChildren="on"
        unCheckedChildren="off"
      />
      <div
        id="visualization"
        style="height:400px"
        @mousedown="mouseDown"
        @mouseup="mouseUp"
        @mousemove="mouseMove">
      </div>
      <relation-view-form @refresh="reload" ref="relationViewForm"></relation-view-form>
    </a-card>

    <a-row :gutter="0">
      <a-col
        :xl="12"
        :lg="12"
        :md="12"
        :sm="24"
        :xs="24"
        :key="view"
        v-for="view in Object.keys(relationViews.views)">
        <a-card :bordered="true" :title="view">
          <a slot="extra"><a-icon type="close" @click="deleteView(view)"></a-icon></a>
          <div :id="&quot;view-&quot; + (relationViews.views[view].topo_flatten || []).join(&quot;&quot;)" style="height:200px"></div>
        </a-card>
      </a-col>
    </a-row>
  </div>

</template>

<script>
import { DataSet, Network } from 'vis-network'
import { getCITypeRelations } from '@/api/cmdb/CITypeRelation'
import { getRelationView, deleteRelationView } from '@/api/cmdb/preference'
import RelationViewForm from './modules/RelationViewForm'
import { notification } from 'ant-design-vue'

export default {
  components: {
    RelationViewForm
  },
  data () {
    return {
      relationViews: { views: {} },
      relations: [],
      network: null,
      options: {},
      viewData: {},
      container: null,
      nodes: null,
      edges: null,
      canvas: null,
      ctx: null,
      drag: false,
      canSelect: false,
      rect: {},
      drawingSurfaceImageData: null
    }
  },
  created () {
    this.create()
  },
  inject: ['reload'],
  methods: {
    create () {
      getRelationView().then(res => {
        this.relationViews = res
        this.createRelationViews()
      })
      getCITypeRelations().then(res => {
        // create an array with nodes
        this.relations = res
        const nodes = []
        const edges = []
        const nodeMap = {}
        res.forEach(item => {
          if (!(item.child.id in nodeMap)) {
            nodes.push({
              id: item.child.id,
              label: item.child.alias
            })
          }

          if (!(item.parent.id in nodeMap)) {
            nodes.push({
              id: item.parent.id,
              label: item.parent.alias
            })
          }

          nodeMap[item.child.id] = 1
          nodeMap[item.parent.id] = 1

          edges.push({
            from: item.parent.id,
            to: item.child.id,
            label: item.relation_type.name
          })
        })
        const _nodes = new DataSet(nodes)

        const _edges = new DataSet(edges)
        this.nodes = _nodes
        this.edges = _edges
        // create a network
        this.container = document.querySelector('#visualization')

        // provide the data in the vis format
        var data = {
          nodes: _nodes,
          edges: _edges
        }
        var options = {
          layout: { randomSeed: 2 },
          autoResize: true,
          nodes: {
            size: 30,
            font: {
              size: 14
            },
            borderWidth: 2
          },
          edges: {
            width: 2,
            smooth: {
              enabled: false
            },
            arrows: {
              to: {
                enabled: true,
                scaleFactor: 0.5
              }
            }
          },
          physics: {
            enabled: false
          },
          interaction: {
            hover: true,
            dragView: true,
            dragNodes: true,
            multiselect: true
          }
        }

        // initialize your network!
        this.container.oncontextmenu = () => { return false }
        this.options = options
        this.viewData = data
        this.network = new Network(this.container, data, options)
        this.canvas = this.network.canvas.frame.canvas
        this.ctx = this.canvas.getContext('2d')
      })
    },

    toggleSelect (checked) {
      if (checked) {
        this.canSelect = true
        this.options.autoResize = false
        this.options.interaction.hover = false
        this.options.interaction.dragView = false
        this.options.interaction.dragNodes = false
        this.network = new Network(this.container, this.viewData, this.options)
        this.canvas = this.network.canvas.frame.canvas
        this.ctx = this.canvas.getContext('2d')
      } else {
        this.canSelect = false
        this.options.autoResize = true
        this.options.interaction.hover = true
        this.options.interaction.dragView = true
        this.options.interaction.dragNodes = true
        this.network = new Network(this.container, this.viewData, this.options)
        this.canvas = this.network.canvas.frame.canvas
        this.ctx = this.canvas.getContext('2d')
      }
    },

    createRelationViews () {
      Object.keys(this.relationViews.views).forEach(viewName => {
        const nodes = []
        const edges = []
        const len = this.relationViews.views[viewName].topo_flatten.length
        this.relationViews.views[viewName].topo_flatten.slice(0, len - 1).forEach((fromId, idx) => {
          nodes.push({
            id: fromId,
            label: this.relationViews.id2type[fromId].alias
          })
          edges.push({
            from: fromId,
            to: this.relationViews.views[viewName].topo_flatten[idx + 1]
          })
        })
        nodes.push({
          id: this.relationViews.views[viewName].topo_flatten[len - 1],
          label: this.relationViews.id2type[this.relationViews.views[viewName].topo_flatten[len - 1]].alias
        })
        const _nodes = new DataSet(nodes)
        const _edges = new DataSet(edges)
        var data = {
          nodes: _nodes,
          edges: _edges
        }

        var options = {
          layout: { randomSeed: 2 },
          nodes: {
            size: 30,
            font: {
              size: 14
            },
            borderWidth: 2
          },
          edges: {
            width: 2,
            smooth: {
              enabled: false
            },
            arrows: {
              to: {
                enabled: true,
                scaleFactor: 0.5
              }
            }
          },
          physics: {
            enabled: false
          },
          interaction: {
            hover: true,
            dragView: false,
            dragNodes: false
          }
        }
        setTimeout(() => {
          const container = document.querySelector('#view-' + this.relationViews.views[viewName].topo_flatten.join(''))
          const n = new Network(container, data, options)
          console.log(n) // TODO
        }, 100)
      })
    },

    toggleCreate (nodeIds) {
      const crIds = []
      this.relations.forEach(item => {
        if (nodeIds.includes(item.parent_id) && nodeIds.includes(item.child_id)) {
          crIds.push({
            parent_id: item.parent_id,
            child_id: item.child_id
          })
        }
      })
      this.$refs.relationViewForm.handleCreate(crIds)
    },

    saveDrawingSurface () {
      this.drawingSurfaceImageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height)
    },

    restoreDrawingSurface () {
      this.ctx.putImageData(this.drawingSurfaceImageData, 0, 0)
    },

    selectNodesFromHighlight () {
      var nodesIdInDrawing = []
      var xRange = this.getStartToEnd(this.rect.startX, this.rect.w)
      var yRange = this.getStartToEnd(this.rect.startY, this.rect.h)

      var allNodes = this.nodes.get()
      for (var i = 0; i < allNodes.length; i++) {
        var curNode = allNodes[i]
        var nodePosition = this.network.getPositions([curNode.id])
        var nodeXY = this.network.canvasToDOM({ x: nodePosition[curNode.id].x, y: nodePosition[curNode.id].y })
        if (xRange.start <= nodeXY.x && nodeXY.x <= xRange.end && yRange.start <= nodeXY.y && nodeXY.y <= yRange.end) {
          nodesIdInDrawing.push(curNode.id)
        }
      }
      this.toggleCreate(nodesIdInDrawing)
      this.network.selectNodes(nodesIdInDrawing)
    },

    getStartToEnd (start, theLen) {
      return theLen > 0 ? { start: start, end: start + theLen } : { start: start + theLen, end: start }
    },

    mouseMove () {
      if (this.drag) {
        this.restoreDrawingSurface()
        this.rect.w = event.offsetX - this.rect.startX
        this.rect.h = event.offsetY - this.rect.startY

        this.ctx.setLineDash([5])
        this.ctx.strokeStyle = 'rgb(0, 102, 0)'
        this.ctx.strokeRect(this.rect.startX, this.rect.startY, this.rect.w, this.rect.h)
        this.ctx.setLineDash([])
        this.ctx.fillStyle = 'rgba(0, 255, 0, 0.2)'
        this.ctx.fillRect(this.rect.startX, this.rect.startY, this.rect.w, this.rect.h)
      }
    },

    mouseDown () {
      if ((event.button === 0 && this.canSelect) || event.button === 2) {
        this.saveDrawingSurface()
        this.rect.startX = event.offsetX
        this.rect.startY = event.offsetY
        this.drag = true
        this.container.style.cursor = 'crosshair'
      }
    },

    mouseUp () {
      if ((event.button === 0 && this.canSelect) || event.button === 2) {
        this.restoreDrawingSurface()
        this.drag = false

        this.container.style.cursor = 'default'
        this.selectNodesFromHighlight()
      }
    },

    deleteView (viewName) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认要删除吗 ?',
        onOk () {
          deleteRelationView(viewName).then(res => {
            that.create()
          }).catch(e => {
            notification.error({ message: e.reponse.data.message })
          })
        }
      })
    }
  }
}
</script>
