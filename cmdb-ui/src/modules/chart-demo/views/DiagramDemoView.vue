<template>
  <div class="diagram-demo-view">
    <h2>Chart Demo Test</h2>

    <!-- Chart with map -->
    <div class="simple-chart">
      <div class="chart-container">
        <!-- Nodes -->
        <div
          v-for="node in chartData.nodeDataArray"
          :key="node.key"
          class="node"
          :class="getNodeClass(node)"
          :style="getNodeStyle(node)"
        >
          <div class="node-shape">
            <div class="node-text">{{ node.text }}</div>
          </div>
        </div>

        <!-- Links -->
        <svg class="links-svg">
          <line
            v-for="link in chartData.linkDataArray"
            :key="`${link.from}-${link.to}`"
            :x1="getLinkX1(link)"
            :y1="getLinkY1(link)"
            :x2="getLinkX2(link)"
            :y2="getLinkY2(link)"
            stroke="#dcb263"
            stroke-width="2"
            marker-end="url(#arrowhead)"
          />
          <!-- Link text labels -->
          <text
            v-for="link in chartData.linkDataArray"
            :key="`text-${link.from}-${link.to}`"
            v-if="link.text"
            :x="getLinkTextX(link)"
            :y="getLinkTextY(link)"
            class="link-text"
            text-anchor="middle"
            dominant-baseline="middle"
          >
            {{ link.text }}
          </text>
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#dcb263"/>
            </marker>
          </defs>
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiagramDemoView',
  data() {
    return {
      chartData: {
        'class': 'GraphLinksModel',
        'pointsDigits': 0,
        'nodeDataArray': [
          { 'key': -1, 'category': 'Start', 'loc': '-237 41', 'text': 'Start' },
          { 'key': -2, 'category': 'End', 'loc': '277 696', 'text': 'End' },
          { 'category': 'Conditional', 'text': 'Is data\ntree-like?', 'key': -14, 'loc': '40 165' },
          { 'text': 'Use a TreeModel', 'key': -5, 'loc': '-100 230' },
          { 'text': 'Use a GraphLinksModel', 'key': -6, 'loc': '180 230' },
          { 'category': 'Comment', 'text': 'GraphLinksModel\nalso allows Groups', 'key': -7, 'loc': '362 230' },
          { 'text': 'Create DIV for Diagram', 'key': -8, 'loc': '-64 41' },
          { 'text': 'Create new Diagram associated with DIV', 'key': -9, 'loc': '164 41' },
          { 'text': 'Style node templates', 'key': -10, 'loc': '40 617' },
          { 'text': 'Add data to node/linkDataArray', 'key': -12, 'loc': '180 320' },
          { 'text': 'Add data to nodeDataArray, including parent', 'key': -13, 'loc': '-100 320' },
          { 'text': 'Style link templates', 'key': -15, 'loc': '277 617' },
          { 'category': 'Conditional', 'text': 'Should nodes be auto-positioned?', 'key': -16, 'loc': '40 460' },
          { 'text': 'Choose a layout', 'key': -18, 'loc': '-100 525' },
          { 'text': 'Set location in node data and bind', 'key': -17, 'loc': '180 525' }
        ],
        'linkDataArray': [
          { 'from': -1, 'to': -8 },
          { 'from': -8, 'to': -9 },
          { 'from': -5, 'to': -13 },
          { 'from': -6, 'to': -12 },
          { 'from': -15, 'to': -2 },
          { 'from': -14, 'to': -5, 'text': 'Yes' },
          { 'from': -14, 'to': -6, 'text': 'No' },
          { 'from': -9, 'to': -14 },
          { 'from': -13, 'to': -16 },
          { 'from': -12, 'to': -16 },
          { 'from': -16, 'to': -18, 'text': 'Yes' },
          { 'from': -16, 'to': -17, 'text': 'No' },
          { 'from': -18, 'to': -10 },
          { 'from': -17, 'to': -10 },
          { 'from': -10, 'to': -15 }
        ]
      }
    }
  },
  methods: {

    getNodeClass(node) {
      if (node.category === 'Start') return 'start-node'
      if (node.category === 'End') return 'end-node'
      if (node.category === 'Conditional') return 'conditional-node'
      if (node.category === 'Comment') return 'comment-node'
      return 'process-node'
    },

    getNodeStyle(node) {
      const [x, y] = node.loc.split(' ').map(Number)
      return {
        left: `${x + 400}px`,
        top: `${y + 150}px`
      }
    },

    getLinkX1(link) {
      const fromNode = this.chartData.nodeDataArray.find(n => n.key === link.from)
      if (!fromNode) return 0
      const [x] = fromNode.loc.split(' ').map(Number)
      const nodeClass = this.getNodeClass(fromNode)
      let offset = 60
      if (nodeClass === 'start-node' || nodeClass === 'end-node') offset = 40
      if (nodeClass === 'conditional-node') offset = 50
      if (nodeClass === 'comment-node') offset = 70
      return x + 400 + offset
    },

    getLinkY1(link) {
      const fromNode = this.chartData.nodeDataArray.find(n => n.key === link.from)
      if (!fromNode) return 0
      const [, y] = fromNode.loc.split(' ').map(Number)
      const nodeClass = this.getNodeClass(fromNode)
      let offset = 25
      if (nodeClass === 'start-node' || nodeClass === 'end-node') offset = 20
      if (nodeClass === 'conditional-node') offset = 50
      if (nodeClass === 'comment-node') offset = 30
      return y + 150 + offset
    },

    getLinkX2(link) {
      const toNode = this.chartData.nodeDataArray.find(n => n.key === link.to)
      if (!toNode) return 0
      const [x] = toNode.loc.split(' ').map(Number)
      const nodeClass = this.getNodeClass(toNode)
      let offset = 60
      if (nodeClass === 'start-node' || nodeClass === 'end-node') offset = 40
      if (nodeClass === 'conditional-node') offset = 50
      if (nodeClass === 'comment-node') offset = 70
      return x + 400 + offset
    },

    getLinkY2(link) {
      const toNode = this.chartData.nodeDataArray.find(n => n.key === link.to)
      if (!toNode) return 0
      const [, y] = toNode.loc.split(' ').map(Number)
      const nodeClass = this.getNodeClass(toNode)
      let offset = 25
      if (nodeClass === 'start-node' || nodeClass === 'end-node') offset = 20
      if (nodeClass === 'conditional-node') offset = 50
      if (nodeClass === 'comment-node') offset = 30
      return y + 150 + offset
    },

    getLinkTextX(link) {
      const fromNode = this.chartData.nodeDataArray.find(n => n.key === link.from)
      if (!fromNode) return 0
      const [x] = fromNode.loc.split(' ').map(Number)
      const toNode = this.chartData.nodeDataArray.find(n => n.key === link.to)
      if (!toNode) return 0
      const [x2] = toNode.loc.split(' ').map(Number)
      return (x + x2) / 2 + 400
    },

    getLinkTextY(link) {
      const fromNode = this.chartData.nodeDataArray.find(n => n.key === link.from)
      if (!fromNode) return 0
      const [, y] = fromNode.loc.split(' ').map(Number)
      const toNode = this.chartData.nodeDataArray.find(n => n.key === link.to)
      if (!toNode) return 0
      const [, y2] = toNode.loc.split(' ').map(Number)
      return (y + y2) / 2 + 150
    }
  }
}
</script>

<style scoped>
.diagram-demo-view {
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.simple-chart {
  width: 100%;
  height: 1000px;
  border: 2px solid #ccc;
  background: #ede9e0;
  margin: 10px 0;
  position: relative;
  overflow: hidden;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.node {
  position: absolute;
  cursor: pointer;
  transition: transform 0.2s;
  z-index: 2;
}

.node:hover {
  transform: scale(1.05);
}

.node-shape {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  min-height: 40px;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 2px solid transparent;
}

.start-node .node-shape {
  background: #064e3b;
  border-radius: 20px;
  width: 80px;
  height: 40px;
  min-width: 80px;
  min-height: 40px;
  padding: 5px 6px;
}

.process-node .node-shape {
  background: #49939e;
  min-width: 120px;
  min-height: 40px;
  max-width: 160px;
}

.conditional-node .node-shape {
  background: #6a9a8a;
  width: 100px;
  height: 100px;
  min-width: 100px;
  min-height: 100px;
  transform: rotate(45deg);
  border-radius: 0;
  max-width: 160px;
}

.comment-node .node-shape {
  background: #ede9e0;
  border: 3px solid #a691cc;
  min-width: 140px;
  min-height: 60px;
  max-width: 200px;
  position: relative;
}

.comment-node .node-shape::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 0px solid transparent;
  border-top: 15px solid #a691cc;
}

.end-node .node-shape {
  background: #7f1d1d;
  border-radius: 20px;
  width: 80px;
  height: 40px;
  min-width: 80px;
  min-height: 40px;
  padding: 5px 6px;
}

.node-text {
  font-weight: bold;
  color: #fff;
  text-align: center;
  font-size: 11px;
  line-height: 1.2;
  white-space: pre-line;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
  font-family: 'Figtree, sans-serif';
}

.conditional-node .node-text {
  font-size: 10px;
  transform: rotate(-45deg);
  width: 80px;
  line-height: 1.1;
}

.comment-node .node-text {
  color: #000;
  font-size: 9px;
  text-shadow: none;
}

.links-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.link-text {
  font-size: 10px;
  font-weight: bold;
  fill: #000;
  text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}
</style>
