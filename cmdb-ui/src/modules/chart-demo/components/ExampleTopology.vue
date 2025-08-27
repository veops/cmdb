<template>
  <div>
    <div style="margin-bottom: 10px; padding: 10px; background: #f0f0f0;">
      <strong>Debug Info:</strong> Nodes: {{ topologyData.nodeDataArray.length }}, Links: {{ topologyData.linkDataArray.length }}
    </div>

    <!-- SVG Network Topology -->
    <div style="border: 1px solid #ccc; padding: 20px; margin-bottom: 20px;">
      <h3>SVG Network Topology</h3>
      <svg ref="svgContainer" width="100%" height="600" style="border: 1px solid #ddd; background: white;">
        <!-- Grid -->
        <defs>
          <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
            <path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(0,0,0,0.1)" stroke-width="1"/>
          </pattern>
        </defs>

        <!-- Background grid -->
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Groups -->
        <g v-for="group in groups" :key="group.key">
          <rect
            :x="group.x"
            :y="group.y"
            :width="group.width"
            :height="group.height"
            fill="rgba(0,0,0,0.05)"
            stroke="#333"
            stroke-dasharray="5,5"
            stroke-width="2"
            rx="5"
          />
          <text
            :x="group.x + 10"
            :y="group.y + 20"
            font-family="Arial"
            font-size="14"
            font-weight="bold"
            fill="#333"
          >
            {{ group.text }}
          </text>
        </g>

        <!-- Links -->
        <g v-for="link in links" :key="`link-${link.from}-${link.to}`">
          <line
            :x1="getNodePosition(link.from).x"
            :y1="getNodePosition(link.from).y"
            :x2="getNodePosition(link.to).x"
            :y2="getNodePosition(link.to).y"
            stroke="red"
            stroke-width="2"
          />
        </g>

        <!-- Nodes with SVG Icons -->
        <g v-for="node in nodes" :key="node.key">
          <!-- Background circle -->
          <circle
            :cx="getNodePosition(node.key).x"
            :cy="getNodePosition(node.key).y"
            r="30"
            :fill="getNodeColor(node.type)"
            stroke="#333"
            stroke-width="2"
            @mouseover="highlightNode(node.key)"
            @mouseout="unhighlightNode(node.key)"
            style="cursor: pointer;"
          />

          <!-- SVG Icon -->
          <image
            :x="getNodePosition(node.key).x - 20"
            :y="getNodePosition(node.key).y - 20"
            width="40"
            height="40"
            :href="getNodeIcon(node.type)"
            style="pointer-events: none;"
          />

          <!-- Node label -->
          <text
            :x="getNodePosition(node.key).x"
            :y="getNodePosition(node.key).y + 45"
            text-anchor="middle"
            font-family="Arial"
            font-size="10"
            font-weight="bold"
            fill="#333"
          >
            {{ node.text || node.type }}
          </text>
        </g>
      </svg>
    </div>
  </div>
</template>

<script>
// Import SVG icons
import cloudIcon from '@/assets/icons/cloud-svgrepo-com.svg'
import firewallIcon from '@/assets/icons/firewalld2-svgrepo-com.svg'
import pcIcon from '@/assets/icons/pc-svgrepo-com.svg'
import routerIcon from '@/assets/icons/router-svgrepo-com.svg'
import serverIcon from '@/assets/icons/server-svgrepo-com.svg'
import switchIcon from '@/assets/icons/switch-svgrepo-com.svg'

export default {
  name: 'ExampleTopology',
  data() {
    return {
      topologyData: {
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
      },
      // Icon mapping
      icons: {
        'Cloud': cloudIcon,
        'Firewall': firewallIcon,
        'Router': routerIcon,
        'Server': serverIcon,
        'Switch': switchIcon,
        'PC': pcIcon
      }
    }
  },
  computed: {
    nodes() {
      return this.topologyData.nodeDataArray.filter(node => !node.isGroup)
    },
    groups() {
      return this.topologyData.nodeDataArray.filter(node => node.isGroup).map(group => {
        const groupNodes = this.topologyData.nodeDataArray.filter(node => node.group === group.key)
        if (groupNodes.length === 0) return null

        const positions = groupNodes.map(node => this.parseLocation(node.loc))
        const minX = Math.min(...positions.map(p => p.x)) - 20
        const maxX = Math.max(...positions.map(p => p.x)) + 20
        const minY = Math.min(...positions.map(p => p.y)) - 20
        const maxY = Math.max(...positions.map(p => p.y)) + 20

        return {
          key: group.key,
          text: group.text,
          x: minX,
          y: minY - 30,
          width: maxX - minX,
          height: maxY - minY + 30
        }
      }).filter(Boolean)
    },
    links() {
      return this.topologyData.linkDataArray
    }
  },
  mounted() {
    console.log('SVG Topology mounted with data:', this.topologyData)
  },
  methods: {
    parseLocation(loc) {
      if (!loc) return { x: 0, y: 0 }
      const [x, y] = loc.split(' ').map(Number)
      return { x: x + 300, y: y + 100 } // Offset for better positioning
    },
    getNodePosition(key) {
      const node = this.topologyData.nodeDataArray.find(n => n.key === key)
      return this.parseLocation(node?.loc)
    },
    getNodeColor(type) {
      const colors = {
        'Cloud': '#e0f2fe',
        'Firewall': '#fee2e2',
        'Router': '#e0f2fe',
        'Server': '#d1fae5',
        'Switch': '#fef3c7',
        'PC': '#f3e8ff'
      }
      return colors[type] || '#f0f0f0'
    },
    getNodeIcon(type) {
      return this.icons[type] || pcIcon // Default to PC icon
    },
    highlightNode(key) {
      // Highlight connected links
      const connectedLinks = this.links.filter(link => link.from === key || link.to === key)
      console.log('Highlighting node:', key, 'Connected links:', connectedLinks)
    },
         unhighlightNode(key) {
       console.log('Unhighlighting node:', key)
     }
  }
}
</script>

<style scoped>
svg {
  font-family: Arial, sans-serif;
}

circle:hover {
  stroke-width: 3;
  stroke: #0066cc;
}

image {
  filter: brightness(0.8);
}

circle:hover + image {
  filter: brightness(1.2);
}
</style>
