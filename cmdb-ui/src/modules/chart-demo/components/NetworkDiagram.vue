<template>
  <div class="w-full">
    <div ref="diagramDiv" class="go-diagram"></div>
  </div>
</template>

<script>
import * as go from 'gojs'

export default {
  name: 'NetworkDiagram',
  props: {
    nodes: {
      type: Array,
      default: () => []
    },
    links: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return { diagram: null }
  },
  mounted() {
    this.initDiagram()
  },
  beforeDestroy() {
    if (this.diagram) this.diagram.div = null
  },
  watch: {
    nodes: {
      handler() {
        this.updateDiagram()
      },
      deep: true
    },
    links: {
      handler() {
        this.updateDiagram()
      },
      deep: true
    }
  },
  methods: {
    initDiagram() {
      const $ = go.GraphObject.make

      this.diagram = $(go.Diagram, this.$refs.diagramDiv, {
        initialContentAlignment: go.Spot.Center,
        'undoManager.isEnabled': true,
        layout: $(go.Layout)
      })

      // ❌ Tắt animation để tránh giật
      this.diagram.animationManager.isEnabled = false

      // ===== Helpers =====
      const LBL = (key = 'text', opts = {}) =>
        $(go.TextBlock, { margin: new go.Margin(8, 10, 4, 10), font: 'bold 12pt Segoe UI', stroke: '#202124', textAlign: 'center', ...opts }, new go.Binding('text', key))

      const SUB = (key = 'subtitle') =>
        $(go.TextBlock, { margin: new go.Margin(0, 10, 8, 10), font: '10pt Segoe UI', stroke: '#5f6368', textAlign: 'center' }, new go.Binding('text', key))

      // ===== Nodes =====
      this.diagram.nodeTemplateMap.add('default',
        $(go.Node, 'Auto',
          { locationSpot: go.Spot.Center },
          new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, 'RoundedRectangle', { fill: '#ffffff', stroke: '#5f6368', strokeWidth: 1.2, parameter1: 6 }, new go.Binding('fill', 'fill'), new go.Binding('stroke', 'stroke'), new go.Binding('desiredSize', 'size', go.Size.parse)),
          $(go.Panel, 'Vertical', { margin: 2 }, LBL('text'), SUB('subtitle'))
        )
      )

      this.diagram.nodeTemplateMap.add('security',
        $(go.Node, 'Auto',
          { locationSpot: go.Spot.Center },
          new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, 'RoundedRectangle', { fill: '#fee2e2', stroke: '#ef4444', strokeWidth: 1.4, parameter1: 8 }, new go.Binding('desiredSize', 'size', go.Size.parse)),
          $(go.Panel, 'Vertical', { margin: 2 }, LBL('text', { stroke: '#7f1d1d' }), SUB('subtitle'))
        )
      )

      this.diagram.nodeTemplateMap.add('net',
        $(go.Node, 'Auto',
          { locationSpot: go.Spot.Center },
          new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, 'RoundedRectangle', { fill: '#e0f2fe', stroke: '#0284c7', strokeWidth: 1.2, parameter1: 6 }, new go.Binding('desiredSize', 'size', go.Size.parse)),
          $(go.Panel, 'Vertical', { margin: 2 }, LBL('text', { stroke: '#0c4a6e' }), SUB('subtitle'))
        )
      )

      this.diagram.nodeTemplateMap.add('label',
        $(go.Node, 'Auto',
          { locationSpot: go.Spot.Center },
          new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
          $(go.Shape, 'RoundedRectangle', { fill: '#eef2ff', stroke: '#6366f1', strokeWidth: 1.2, parameter1: 12 }),
          LBL('text', { margin: new go.Margin(10, 16, 10, 16) })
        )
      )

      // ===== Groups =====
      this.diagram.groupTemplateMap.add('area',
        $(go.Group, 'Auto',
          {
            computesBoundsAfterDrag: true,
            locationSpot: go.Spot.Center,
            handlesDragDropForMembers: true,
            layout: $(go.Layout)
          },
          $(go.Shape, 'RoundedRectangle', { fill: 'rgba(237,242,247,0.7)', stroke: '#94a3b8', strokeWidth: 1.2 }),
          $(go.Panel, 'Table',
            $(go.Panel, 'Auto', { row: 0, margin: 6 }, $(go.Placeholder, { padding: 16 })),
            $(go.Panel, 'Auto', { row: 1 },
              $(go.Shape, 'Rectangle', { fill: '#fde68a', stroke: '#f59e0b' }),
              $(go.TextBlock, { margin: new go.Margin(4, 10), font: 'bold 12pt Segoe UI', stroke: '#92400e', textAlign: 'center' }, new go.Binding('text', 'text'))
            )
          )
        )
      )

      this.diagram.groupTemplateMap.add('band',
        $(go.Group, 'Auto', { selectable: false, locationSpot: go.Spot.Center },
          new go.Binding('location', 'loc', go.Point.parse),
          $(go.Shape, 'RoundedRectangle', { fill: '#d9f99d', stroke: '#65a30d', strokeWidth: 1.2, parameter1: 6 }, new go.Binding('desiredSize', 'size', go.Size.parse)),
          $(go.TextBlock, { margin: 6, font: 'bold 12pt Segoe UI', stroke: '#1b4332' }, new go.Binding('text', 'text'))
        )
      )

      // ===== Links =====
      this.diagram.linkTemplate = $(go.Link, { routing: go.Link.AvoidsNodes, corner: 8 },
        $(go.Shape, { strokeWidth: 1.6 }),
        $(go.Shape, { toArrow: 'Standard', scale: 1.1 })
      )

      // Grid
      this.diagram.grid = $(go.Panel, 'Grid',
        $(go.Shape, 'LineH', { stroke: 'rgba(0,0,0,0.08)', strokeWidth: 1 }),
        $(go.Shape, 'LineV', { stroke: 'rgba(0,0,0,0.08)', strokeWidth: 1 })
      )
      this.diagram.grid.visible = true
      this.diagram.toolManager.draggingTool.isGridSnapEnabled = true
      this.diagram.grid.gridCellSize = new go.Size(10, 10)

      // Load initial data
      this.updateDiagram()
    },
    updateDiagram() {
      if (this.diagram && this.nodes.length > 0) {
        this.diagram.model = new go.GraphLinksModel(this.nodes, this.links)
        // canh giữa ngay sau khi load model
        this.diagram.delayInitialization(() => {
          this.diagram.centerRect(this.diagram.documentBounds)
        })
      }
    }
  }
}
</script>

<style scoped>
.go-diagram {
  width: 100%;
  height: 720px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
}
</style>
