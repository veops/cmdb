<template>
  <div class="ci-detail-relation">
    <CiDetailRelationTopo ref="ciDetailRelationTopo"/>
  </div>
</template>

<script>
import CiDetailRelationTopo from './ciDetailRelationTopo/index.vue'
import Node from './ciDetailRelationTopo/node.js'

export default {
  name: 'CIDetailRelation',
  components: { CiDetailRelationTopo },
  props: {
    ciId: {
      type: Number,
      default: 0,
    },
    typeId: {
      type: Number,
      default: 0,
    },
    ci: {
      type: Object,
      default: () => {},
    },
    relationData: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      firstCIs: {},
      secondCIs: {},
      topoData: {
        nodes: {},
        edges: []
      },
    }
  },
  computed: {
    exsited_ci() {
      const _exsited_ci = [this.ciId]
      this.relationData.parentCITypeList.forEach((parent) => {
        if (this.firstCIs[parent.name]) {
          this.firstCIs[parent.name].forEach((parentCi) => {
            _exsited_ci.push(parentCi._id)
          })
        }
      })
      this.relationData.childCITypeList.forEach((child) => {
        if (this.secondCIs[child.name]) {
          this.secondCIs[child.name].forEach((childCi) => {
            _exsited_ci.push(childCi._id)
          })
        }
      })
      return _exsited_ci
    },
  },
  inject: {
    attrList: { from: 'attrList' },
    attributes: { from: 'attributes' },
    ci_types: { from: 'ci_types' },
    relationViewRefreshNumber: {
      from: 'relationViewRefreshNumber',
      default: () => null,
    },
  },

  watch: {
    relationData: {
      immediate: true,
      deep: true,
      handler(val) {
        this.init(val)
      }
    }
  },

  methods: {
    async init(relationData) {
      const ci_types_list = this.ci_types()
      const _findCiType = ci_types_list.find((item) => item.id === this.typeId)
      if (!_findCiType) {
        return
      }

      this.getFirstCIs(relationData.parentCIList)
      this.getSecondCIs(relationData.childCIList)

      this.handleTopoData()
      this.$nextTick(() => {
        if (this.$refs.ciDetailRelationTopo) {
          this.$refs.ciDetailRelationTopo.exsited_ci = this.exsited_ci
          this.$refs.ciDetailRelationTopo.setTopoData(this.topoData)
        }
      })
    },
    async getFirstCIs(parentCIList) {
      const firstCIs = {}
      parentCIList.forEach((item) => {
        if (item.ci_type in firstCIs) {
          firstCIs[item.ci_type].push(item)
        } else {
          firstCIs[item.ci_type] = [item]
        }
      })
      this.firstCIs = firstCIs
    },
    async getSecondCIs(childCIList) {
      const secondCIs = {}
      childCIList.forEach((item) => {
        if (item.ci_type in secondCIs) {
          secondCIs[item.ci_type].push(item)
        } else {
          secondCIs[item.ci_type] = [item]
        }
      })
      this.secondCIs = secondCIs
    },

    handleTopoData() {
      const ci_types_list = this.ci_types()
      if (!ci_types_list?.length) {
        this.$set(this, 'topoData', {
          nodes: {},
          edges: []
        })
        return
      }

      const _findCiType = ci_types_list.find((item) => item.id === this.typeId)
      const unique_id = _findCiType.show_id || _findCiType.unique_id
      const _findUnique = this.attrList().find((attr) => attr.id === unique_id)
      const unique_name = _findUnique?.name
      const unique_alias = _findUnique?.alias || _findUnique?.name || ''

      const nodes = {
        isRoot: true,
        id: `Root_${this.typeId}`,
        title: _findCiType.alias || _findCiType.name, // 中文名
        name: _findCiType.name, // 英文名
        Class: Node,
        unique_alias,
        unique_name,
        unique_value: this.ci[unique_name],
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
        children: [],
      }
      const edges = []
      this.relationData.parentCITypeList.forEach((parent) => {
        const _findCiType = ci_types_list.find((item) => item.id === parent.id)
        if (this.firstCIs[parent.name] && _findCiType) {
          const unique_id = _findCiType.show_id || _findCiType.unique_id
          const _findUnique = parent.attributes.find((attr) => attr.id === unique_id)
          const unique_name = _findUnique?.name
          const unique_alias = _findUnique?.alias || _findUnique?.name || ''
          this.firstCIs[parent.name].forEach((parentCi) => {
            nodes.children.push({
              id: `${parentCi._id}`,
              Class: Node,
              title: parent.alias || parent.name,
              name: parent.name,
              side: 'left',
              unique_alias,
              unique_name,
              unique_value: parentCi[unique_name],
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
            edges.push({
              id: `${parentCi._id}_Root`,
              source: 'right',
              target: 'left',
              sourceNode: `${parentCi._id}`,
              targetNode: `Root_${this.typeId}`,
              type: 'endpoint',
            })
          })
        }
      })
      this.relationData.childCITypeList.forEach((child) => {
        const _findCiType = ci_types_list.find((item) => item.id === child.id)
        if (this.secondCIs[child.name] && _findCiType) {
          const unique_id = _findCiType.show_id || _findCiType.unique_id
          const _findUnique = child.attributes.find((attr) => attr.id === unique_id)
          const unique_name = _findUnique?.name
          const unique_alias = _findUnique?.alias || _findUnique?.name || ''
          this.secondCIs[child.name].forEach((childCi) => {
            nodes.children.push({
              id: `${childCi._id}`,
              Class: Node,
              title: child.alias || child.name,
              name: child.name,
              side: 'right',
              unique_alias,
              unique_name,
              unique_value: childCi[unique_name],
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
            edges.push({
              id: `Root_${childCi._id}`,
              source: 'right',
              target: 'left',
              sourceNode: `Root_${this.typeId}`,
              targetNode: `${childCi._id}`,
              type: 'endpoint',
            })
          })
        }
      })
      this.$set(this, 'topoData', {
        nodes,
        edges
      })
    }
  },
}
</script>

<style lang="less" scoped>
.ci-detail-relation {
  height: 100%;
}
</style>
