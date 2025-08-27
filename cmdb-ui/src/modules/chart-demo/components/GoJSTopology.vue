<template>
  <div class="gojs-topology">
    <div ref="diagramDiv" class="diagram-container"></div>
  </div>
</template>

<script>
import * as go from 'gojs'

export default {
  name: 'GoJSTopology',
  props: {
    modelData: {
      type: Object,
      default: () => ({
        nodeDataArray: [],
        linkDataArray: []
      })
    },
    width: {
      type: Number,
      default: 1200
    },
    height: {
      type: Number,
      default: 700
    }
  },
  data() {
    return {
      diagram: null
    }
  },
  mounted() {
    this.initDiagram()
  },
  beforeDestroy() {
    if (this.diagram) {
      this.diagram.div = null
    }
  },
  watch: {
    modelData: {
      handler() {
        this.loadModel()
      },
      deep: true
    }
  },
  methods: {
    initDiagram() {
      const $ = go.GraphObject.make

      this.diagram = new go.Diagram(this.$refs.diagramDiv, {
        'commandHandler.archetypeGroupData': { isGroup: true, text: 'Subnet' },
        'undoManager.isEnabled': false,
        initialContentAlignment: go.Spot.Center,
        layout: $(go.Layout),
        allowMove: false,
        allowSelect: false,
        allowLink: false,
        allowRelink: false,
        allowClipboard: false,
        allowCopy: false,
        allowDelete: false,
        allowGroup: false,
        allowUngroup: false,
        allowUndo: false,
        allowRedo: false,
        toolManager: null,
        maxSelectionCount: 0,
        contentAlignment: go.Spot.Center,
        scrollMode: go.Diagram.None,
        panMode: go.Diagram.None
      })

      // Node template with pictures
      this.diagram.nodeTemplate = new go.Node('Spot', {
        locationSpot: go.Spot.Center,
        locationObjectName: 'BODY',
        selectionObjectName: 'BODY',
        selectable: false,
        movable: false
      })
        .bindTwoWay('location', 'loc', go.Point.parse, go.Point.stringify)
        .add(
          new go.Picture({
            name: 'BODY',
            width: 50,
            height: 50,
            portId: '',
            fromLinkable: false,
            toLinkable: false,
            cursor: 'default'
          }).bind('source', 'type', (t) => `images/network/${t.toLowerCase()}.svg`),
          new go.Shape({
            width: 25,
            height: 25,
            fill: 'transparent',
            strokeWidth: 0
          })
        )

      // Group template
      this.diagram.groupTemplate = new go.Group('Vertical', {
        locationSpot: go.Spot.Center,
        padding: 5,
        selectable: false,
        movable: false
      })
        .add(
          new go.TextBlock({
            alignment: go.Spot.Left,
            font: '12px georgia',
            editable: false
          }).bindTwoWay('text'),
          new go.Panel('Auto')
            .add(
              new go.Shape('RoundedRectangle', {
                strokeDashArray: [2, 6],
                stroke: '#333',
                fill: 'rgba(0,0,0,0)'
              }),
              new go.Placeholder({ padding: 5 })
            )
        )

      // Link template
      this.diagram.linkTemplate = new go.Link({
        routing: go.Link.Orthogonal,
        fromSpot: go.Spot.AllSides,
        toSpot: go.Spot.AllSides,
        relinkableFrom: false,
        relinkableTo: false,
        selectable: false
      })
        .add(new go.Shape({ strokeWidth: 1.5, stroke: 'red' }))
        .add(new go.Shape({ strokeWidth: 0, fill: 'red', scale: 0.7, fromArrow: 'circle' }))
        .add(new go.Shape({ strokeWidth: 0, fill: 'red', scale: 0.7, toArrow: 'circle' }))

      // Load initial model
      this.loadModel()
    },
    loadModel() {
      if (this.diagram && this.modelData) {
        const model = new go.GraphLinksModel(
          this.modelData.nodeDataArray || [],
          this.modelData.linkDataArray || []
        )
        this.diagram.model = model
      }
    },
    save() {
      if (this.diagram) {
        const json = this.diagram.model.toJson()
        this.$emit('save', json)
        return json
      }
    }
  }
}
</script>

<style scoped>
.gojs-topology {
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  overflow: hidden;
}

.diagram-container {
  width: 100%;
  height: 100%;
  min-height: 600px;
}
</style>
