<template>
  <div
    id="ci-detail-relation-topo"
    class="ci-detail-relation-topo"
    :style="{ width: '100%', marginTop: '20px', height: 'calc(100vh - 136px)' }"
  ></div>
</template>

<script>
import _ from 'lodash'
import { TreeCanvas } from 'butterfly-dag'
import { searchCIRelation } from '@/modules/cmdb/api/CIRelation'
import Node from './node.js'

import 'butterfly-dag/dist/index.css'
import './index.less'

export default {
  name: 'CiDetailRelationTopo',
  data() {
    return {
      topoData: {},
      exsited_ci: [],
    }
  },
  inject: ['ci_types'],
  mounted() {},
  methods: {
    init() {
      const root = document.getElementById('ci-detail-relation-topo')
      this.canvas = new TreeCanvas({
        root: root,
        disLinkable: false, // 可删除连线
        linkable: false, // 可连线
        draggable: true, // 可拖动
        zoomable: true, // 可放大
        moveable: true, // 可平移
        theme: {
          edge: {
            shapeType: 'AdvancedBezier',
            arrow: true,
            arrowPosition: 1,
          },
        },
        layout: {
          type: 'mindmap',
          options: {
            direction: 'H',
            getSide(d) {
              return d.data.side || 'right'
            },
            getHeight(d) {
              return 10
            },
            getWidth(d) {
              return 40
            },
            getHGap(d) {
              return 80
            },
            getVGap(d) {
              return 40
            },
          },
        },
      })
      this.canvas.setZoomable(true, true)
      this.canvas.on('events', ({ type, data }) => {
        const sourceNode = data?.id || null
        if (type === 'custom:clickLeft') {
          searchCIRelation(`root_id=${Number(sourceNode)}&&level=1&&reverse=1&&count=10000`).then((res) => {
            this.redrawData(res, sourceNode, 'left')
          })
        }
        if (type === 'custom:clickRight') {
          searchCIRelation(`root_id=${Number(sourceNode)}&&level=1&&reverse=0&&count=10000`).then((res) => {
            this.redrawData(res, sourceNode, 'right')
          })
        }
      })
    },
    setTopoData(data) {
      this.canvas = null
      this.init()
      this.topoData = _.cloneDeep(data)
      this.canvas.draw(data, {}, () => {
        this.canvas.focusCenterWithAnimate()
      })
    },
    redrawData(res, sourceNode, side) {
      const newNodes = []
      const newEdges = []
      if (!res.result.length) {
        this.$message.info('无层级关系！')
        return
      }
      const ci_types_list = this.ci_types()
      res.result.forEach((r) => {
        if (!this.exsited_ci.includes(r._id)) {
          const _findCiType = ci_types_list.find((item) => item.id === r._type)
          newNodes.push({
            id: `${r._id}`,
            Class: Node,
            title: r.ci_type_alias || r.ci_type,
            name: r.ci_type,
            side: side,
            unique_alias: r.unique_alias,
            unique_name: r.unique,
            unique_value: r[r.unique],
            children: [],
            icon: _findCiType?.icon || '',
            endpoints: [
              {
                id: 'left',
                orientation: [-1, 0],
                pos: [0, 0.5],
              },
              {
                id: 'right',
                orientation: [1, 0],
                pos: [0, 0.5],
              },
            ],
          })
        }
        newEdges.push({
          id: `${r._id}`,
          source: 'right',
          target: 'left',
          sourceNode: side === 'right' ? sourceNode : `${r._id}`,
          targetNode: side === 'right' ? `${r._id}` : sourceNode,
          type: 'endpoint',
        })
      })
      const { nodes, edges } = this.canvas.getDataMap()
      // 删除原节点和边
      this.canvas.removeNodes(nodes.map((node) => node.id))
      this.canvas.removeEdges(edges)

      const _topoData = _.cloneDeep(this.topoData)
      _topoData.edges.push(...newEdges)
      let result
      const getTreeItem = (data, id) => {
        for (let i = 0; i < data.length; i++) {
          if (data[i].id === id) {
            result = data[i] // 结果赋值
            result.edges = _topoData.edges
            break
          } else {
            if (data[i].children && data[i].children.length) {
              getTreeItem(data[i].children, id)
            }
          }
        }
      }

      getTreeItem(_topoData.nodes.children, sourceNode)
      result.children.push(...newNodes)

      this.topoData = _topoData
      this.canvas.draw(_topoData, {}, () => {})
      this.exsited_ci = [...new Set([...this.exsited_ci, ...res.result.map((r) => r._id)])]
    },
  },
}
</script>

<style></style>
