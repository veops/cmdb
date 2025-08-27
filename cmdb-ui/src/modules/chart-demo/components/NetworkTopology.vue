<template>
  <div>
    <div ref="diagramDiv" style="width: 100%; height: 700px; border: 1px solid #ddd"></div>
  </div>
</template>

<script>
import * as go from 'gojs'

export default {
  name: 'NetworkTopology',
  props: {
    nodes: {
      type: Array,
      default: () => [],
    },
    links: {
      type: Array,
      default: () => [],
    },
    height: {
      type: String,
      default: '700px',
    },
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
      deep: true,
    },
    links: {
      handler() {
        this.updateDiagram()
      },
      deep: true,
    },
  },
  methods: {
    initDiagram() {
      const $ = go.GraphObject.make
      const diagramDiv = this.$refs.diagramDiv

      const diagram = $(go.Diagram, diagramDiv, {
        initialContentAlignment: go.Spot.TopCenter,
        'undoManager.isEnabled': true,
        layout: $(go.Layout),
      })

      // Add grid
      diagram.grid = $(
        go.Panel,
        'Grid',
        $(go.Shape, 'LineH', { stroke: 'rgba(0,0,0,0.1)', strokeWidth: 1 }),
        $(go.Shape, 'LineV', { stroke: 'rgba(0,0,0,0.1)', strokeWidth: 1 })
      )
      diagram.grid.visible = true

      // --- Node template: bind location từ nodeData.loc ---
      diagram.nodeTemplate = $(
        go.Node,
        'Auto',
        // location binding (expects "x y" string in nodeData.loc)
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        $(
          go.Shape,
          'RoundedRectangle',
          { stroke: '#444', strokeWidth: 1.5, minSize: new go.Size(100, 50) },
          new go.Binding('fill', 'color')
        ),
        $(
          go.Panel,
          'Vertical',
          { margin: 6 },
          $(go.TextBlock, { font: 'bold 11px sans-serif', textAlign: 'center' }, new go.Binding('text', 'label')),
          $(
            go.TextBlock,
            { font: '9px sans-serif', textAlign: 'center', stroke: '#666', maxLines: 2 },
            new go.Binding('text', 'subtitle')
          )
        )
      )

      // --- Group template (dashed box with heading) ---
      diagram.groupTemplate = $(
        go.Group,
        'Auto',
        {
          movable: false,
          copyable: false,
          deletable: false,
        },
        $(go.Shape, 'Rectangle', { fill: 'transparent', stroke: '#888', strokeDashArray: [6, 3], strokeWidth: 1.2 }),
        $(
          go.Panel,
          'Vertical',
          $(go.TextBlock, { margin: 6, font: 'bold 14px sans-serif' }, new go.Binding('text', 'key')),
          $(go.Placeholder, { padding: 8 })
        )
      )

      // --- Link template: label ở midpoint, offset lên trên, tránh chồng node ---
      diagram.linkTemplate = $(
        go.Link,
        {
          routing: go.Link.AvoidsNodes,
          curve: go.Link.JumpOver,
          adjusting: go.Link.Stretch,
          corner: 8,
          toShortLength: 6,
        },
        new go.Binding('stroke', 'isHighlighted', (h) => (h ? '#0066cc' : '#333')),
        $(go.Shape, { strokeWidth: 2 }),
        $(go.Shape, { toArrow: 'Standard', stroke: null, scale: 0.9 }),
        // label panel: đặt lên giữa segment 0 (đường thẳng chỉ có 1 segment)
        $(
          go.Panel,
          'Auto',
          {
            segmentIndex: 0,
            segmentFraction: 0.5, // midpoint
            segmentOffset: new go.Point(0, -15), // lên trên 15px để khỏi chạm node
          },
          $(go.Shape, 'RoundedRectangle', { fill: 'white', stroke: '#ccc', strokeWidth: 0.5 }),
          $(go.TextBlock, { margin: 3, font: '9px sans-serif' }, new go.Binding('text', 'label'))
        )
      )

      this.diagram = diagram
      this.updateDiagram()
    },
    updateDiagram() {
      if (this.diagram && this.nodes.length > 0) {
        const diagramDiv = this.$refs.diagramDiv
        const width = Math.max(diagramDiv.clientWidth || 1200, 1100)

        // Calculate positions for nodes with static layout
        const computedNodes = JSON.parse(JSON.stringify(this.nodes))
        const centerX = width / 2

        // Static positioning based on node keys for better control
        computedNodes.forEach((node) => {
          if (node.isGroup) {
            // Group positions
            const groupPositions = {
              SPINE: { x: centerX, y: 50 },
              LEAF: { x: centerX, y: 200 },
              APIC: { x: centerX, y: 350 },
              INTERNET: { x: centerX, y: 30 },
              EDGE: { x: centerX, y: 180 },
              ACCESS: { x: centerX, y: 280 },
            }
            const pos = groupPositions[node.key]
            if (pos) {
              node.loc = `${pos.x} ${pos.y}`
            }
          } else {
            // Individual node positions
            const nodePositions = {
              // Internet layer
              'INTERNET-CLOUD': { x: centerX, y: 80 },
              FPT: { x: centerX - 200, y: 120 },
              CMC: { x: centerX + 200, y: 120 },
              VIETTEL: { x: centerX - 400, y: 120 },
              'DDOS-01': { x: centerX - 200, y: 160 },
              'DDOS-02': { x: centerX + 200, y: 160 },

              // Edge layer
              'MX204-EDGE-01': { x: centerX - 150, y: 240 },
              'MX204-EDGE-02': { x: centerX + 150, y: 240 },

              // Access layer
              'C9300-01': { x: centerX - 300, y: 320 },
              'C9300-02': { x: centerX + 300, y: 320 },
              'MX-LEAF-01': { x: centerX - 200, y: 400 },
              'MX-LEAF-02': { x: centerX + 200, y: 400 },

              // ACI Fabric nodes
              'SPINE-01': { x: centerX - 100, y: 120 },
              'SPINE-02': { x: centerX + 100, y: 120 },
              'LEAF-01': { x: centerX - 300, y: 320 },
              'LEAF-02': { x: centerX - 200, y: 320 },
              'LEAF-03': { x: centerX - 100, y: 320 },
              'LEAF-04': { x: centerX, y: 320 },
              'LEAF-05': { x: centerX + 100, y: 320 },
              'LEAF-06': { x: centerX + 200, y: 320 },
              'LEAF-07': { x: centerX + 300, y: 320 },
              'LEAF-08': { x: centerX + 400, y: 320 },
              'LEAF-09': { x: centerX + 500, y: 320 },
              'LEAF-10': { x: centerX + 600, y: 320 },
              'APIC-01': { x: centerX - 100, y: 520 },
              'APIC-02': { x: centerX, y: 520 },
              'APIC-03': { x: centerX + 100, y: 520 },
            }

            const pos = nodePositions[node.key]
            if (pos) {
              node.loc = `${pos.x} ${pos.y}`
            } else {
              // Fallback positioning for unknown nodes
              const typeToY = {
                spine: 120,
                leaf: 320,
                apic: 520,
                internet: 80,
                isp: 120,
                ddos: 160,
                edge: 240,
                access: 320,
                mgmt: 400,
              }
              const y = typeToY[node.type] || 200
              const x = centerX + (Math.random() - 0.5) * 200
              node.loc = `${x} ${y}`
            }
          }
        })

        this.diagram.model = new go.GraphLinksModel(computedNodes, this.links)
        this.diagram.requestUpdate()
        setTimeout(() => this.diagram.commandHandler.zoomToFit(), 50)
      }
    },
  },
}
</script>
