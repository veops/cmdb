<template>
  <div class="network-diagram-view">
    <h2>Network Diagram Demo</h2>

    <!-- GoJS Network Diagram -->
    <div class="network-chart">
      <div id="myDiagramDiv" class="diagram"></div>
    </div>
  </div>
</template>

<script>
import go from 'gojs'

export default {
  name: 'NetworkDiagramView',
  data() {
    return {
      myDiagram: null,
      networkData: {
        'class': 'go.GraphLinksModel',
        'nodeDataArray': [
          { 'key': 0, 'type': 'Cloud', 'loc': '0 0', 'text': 'Internet' },
          { 'key': 1, 'type': 'Firewall', 'loc': '100 0' },
          { 'key': 2, 'type': 'Router', 'loc': '200 0' },
          { 'key': 3, 'type': 'Server', 'loc': '300 0' },
          { 'key': 4, 'type': 'Switch', 'loc': '200 100' },
          { 'key': 5, 'type': 'Firewall', 'loc': '25 100' },
          { 'key': 6, 'type': 'Router', 'loc': '25 200' },
          { 'key': 7, 'type': 'Switch', 'loc': '400 100' },

          { 'key': 10, 'isGroup': true, 'text': 'Intranet 1' },
          { 'key': 11, 'type': 'PC', 'loc': '150 220', 'group': 10 },
          { 'key': 12, 'type': 'PC', 'loc': '250 220', 'group': 10 },
          { 'key': 13, 'type': 'PC', 'loc': '150 270', 'group': 10 },
          { 'key': 14, 'type': 'PC', 'loc': '250 270', 'group': 10 },

          { 'key': 20, 'isGroup': true, 'text': 'Intranet 2' },
          { 'key': 21, 'type': 'PC', 'loc': '350 220', 'group': 20 },
          { 'key': 22, 'type': 'PC', 'loc': '450 220', 'group': 20 },
          { 'key': 23, 'type': 'PC', 'loc': '350 270', 'group': 20 },
          { 'key': 24, 'type': 'PC', 'loc': '450 270', 'group': 20 },

          { 'key': 30, 'isGroup': true, 'text': 'Isolation test' },
          { 'key': 31, 'type': 'PC', 'loc': '-100 172', 'group': 30 },
          { 'key': 32, 'type': 'PC', 'loc': '-100 242', 'group': 30 }
        ],
        'linkDataArray': [
          { 'from': 0, 'to': 1 },
          { 'from': 1, 'to': 2 },
          { 'from': 2, 'to': 3 },
          { 'from': 2, 'to': 4 },
          { 'from': 5, 'to': 4 },
          { 'from': 5, 'to': 6 },
          { 'from': 4, 'to': 7 },
          { 'from': 4, 'to': 10 },
          { 'from': 7, 'to': 20 },
          { 'from': 6, 'to': 30 }
        ]
      }
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      const $ = go.GraphObject.make

      this.myDiagram = new go.Diagram('myDiagramDiv', {
        'commandHandler.archetypeGroupData': { isGroup: true, text: 'Subnet' },
        'undoManager.isEnabled': true
      })

      this.myDiagram.nodeTemplate = $(go.Node, 'Spot', {
        locationSpot: go.Spot.Center,
        locationObjectName: 'BODY',
        selectionObjectName: 'BODY'
      }, new go.Binding('location', 'loc', go.Point.parse, go.Point.stringify),
        $(go.Picture, {
          name: 'BODY',
          width: 50,
          height: 50,
          portId: '',
          fromLinkable: true,
          toLinkable: true,
          cursor: 'pointer'
        }, new go.Binding('source', 'type', (t) => this.getNetworkIcon(t))),
        $(go.Shape, {
          width: 25,
          height: 25,
          fill: 'transparent',
          strokeWidth: 0
        })
      )

      this.myDiagram.groupTemplate = $(go.Group, 'Vertical', {
        locationSpot: go.Spot.Center,
        padding: 5
      },
        $(go.TextBlock, {
          alignment: go.Spot.Left,
          font: '12px georgia',
          editable: true
        }, new go.Binding('text')),
        $(go.Panel, 'Auto',
          $(go.Shape, 'RoundedRectangle', {
            strokeDashArray: [2, 6],
            stroke: '#333',
            fill: 'rgba(0,0,0,0)'
          }),
          $(go.Placeholder, { padding: 5 })
        )
      )

      this.myDiagram.linkTemplate = $(go.Link, {
        routing: go.Routing.Orthogonal,
        fromSpot: go.Spot.AllSides,
        toSpot: go.Spot.AllSides,
        relinkableFrom: true,
        relinkableTo: true
      },
        $(go.Shape, { strokeWidth: 1.5, stroke: 'red' }),
        $(go.Shape, { strokeWidth: 0, fill: 'red', scale: 0.7, fromArrow: 'circle' }),
        $(go.Shape, { strokeWidth: 0, fill: 'red', scale: 0.7, toArrow: 'circle' })
      )

      this.load()
    },

    getNetworkIcon(type) {
      // Use SVG files from src/assets/icons
      const iconMap = {
        'Cloud': require('@/assets/icons/cloud-svgrepo-com.svg'),
        'Firewall': require('@/assets/icons/firewalld2-svgrepo-com.svg'),
        'Switch': require('@/assets/icons/switch-svgrepo-com.svg'),
        'Server': require('@/assets/icons/server-svgrepo-com.svg'),
        'Router': require('@/assets/icons/router-svgrepo-com.svg'),
        'PC': require('@/assets/icons/pc-svgrepo-com.svg')
      }

      return iconMap[type] || iconMap['PC']
    },

    load() {
      this.myDiagram.model = go.Model.fromJson(JSON.stringify(this.networkData))
    }
  }
}
</script>

<style scoped>
.network-diagram-view {
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.network-chart {
  width: 100%;
  height: 1000px;
  border: 2px solid #ccc;
  background: #f5f5f5;
  margin: 10px 0;
  position: relative;
  overflow: hidden;
}

.diagram {
  width: 100%;
  height: 100%;
  background: white;
}
</style>
