<template>
  <div class="ci-detail-relation">
    <a-radio-group v-model="activeKey" size="small" @change="handleChangeActiveKey">
      <a-radio-button value="1">
        拓扑
      </a-radio-button>
      <a-radio-button value="2">
        表格
      </a-radio-button>
    </a-radio-group>
    <CiDetailRelationTopo ref="ciDetailRelationTopo" v-if="activeKey === '1'" />
    <template v-if="activeKey === '2'">
      <template v-for="parent in parentCITypes">
        <div :key="'ctr_' + parent.ctr_id">
          <div class="ci-detail-relation-table-title">
            {{ parent.alias || parent.name }}
            <a
              @click="
                () => {
                  $refs.addTableModal.openModal({ [`${ci.unique}`]: ci[ci.unique] }, ci._id, parent.id, 'parents')
                }
              "
            ><a-icon
              type="plus-square"
            /></a>
          </div>
          <vxe-grid
            v-if="firstCIs[parent.name]"
            bordered
            size="mini"
            :columns="firstCIColumns[parent.id]"
            :data="firstCIs[parent.name]"
            overflow
            showOverflow="tooltip"
            showHeaderOverflow="tooltip"
            resizable
            class="ops-stripe-table"
          >
            <template #operation_default="{ row }">
              <a-popconfirm arrowPointAtCenter title="确认删除关系？" @confirm="deleteRelation(row._id, ciId)">
                <a :style="{ color: 'red' }"><a-icon type="delete"/></a>
              </a-popconfirm>
            </template>
          </vxe-grid>
        </div>
      </template>
      <a-divider />
      <template v-for="child in childCITypes">
        <div :key="'ctr_' + child.ctr_id">
          <div class="ci-detail-relation-table-title">
            {{ child.alias || child.name }}
            <a
              @click="
                () => {
                  $refs.addTableModal.openModal({ [`${ci.unique}`]: ci[ci.unique] }, ci._id, child.id, 'children')
                }
              "
            ><a-icon
              type="plus-square"
            /></a>
          </div>
          <vxe-grid
            v-if="secondCIs[child.name]"
            bordered
            size="mini"
            :columns="secondCIColumns[child.id]"
            :data="secondCIs[child.name]"
            showOverflow="tooltip"
            showHeaderOverflow="tooltip"
            resizable
            class="ops-stripe-table"
          >
            <template #operation_default="{ row }">
              <a-popconfirm arrowPointAtCenter title="确认删除关系？" @confirm="deleteRelation(ciId, row._id)">
                <a :style="{ color: 'red' }"><a-icon type="delete"/></a>
              </a-popconfirm>
            </template>
          </vxe-grid>
        </div>
      </template>
    </template>
    <AddTableModal ref="addTableModal" @reload="reload" />
  </div>
</template>

<script>
import _ from 'lodash'
import { getCITypeChildren, getCITypeParent } from '@/modules/cmdb/api/CITypeRelation'
import { searchCIRelation, deleteCIRelationView } from '@/modules/cmdb/api/CIRelation'
import CiDetailRelationTopo from './ciDetailRelationTopo/index.vue'
import Node from './ciDetailRelationTopo/node.js'
import AddTableModal from '../../relation_views/modules/AddTableModal.vue'
export default {
  name: 'CiDetailRelation',
  components: { CiDetailRelationTopo, AddTableModal },
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
  },
  data() {
    return {
      activeKey: '1',
      parentCITypes: [],
      childCITypes: [],
      firstCIs: {},
      firstCIColumns: {},
      secondCIs: {},
      secondCIColumns: {},
      firstCIJsonAttr: {},
      secondCIJsonAttr: {},
    }
  },
  computed: {
    topoData() {
      const ci_types_list = this.ci_types()
      const unique_id = this.attributes().unique_id
      const unique_name = this.attributes().unique
      const _findUnique = this.attrList().find((attr) => attr.id === unique_id)
      const unique_alias = _findUnique?.alias || _findUnique?.name || ''
      const _findCiType = ci_types_list.find((item) => item.id === this.typeId)
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
      this.parentCITypes.forEach((parent) => {
        const _findCiType = ci_types_list.find((item) => item.id === parent.id)
        if (this.firstCIs[parent.name]) {
          this.firstCIs[parent.name].forEach((parentCi) => {
            nodes.children.push({
              id: `${parentCi._id}`,
              Class: Node,
              title: parent.alias || parent.name,
              name: parent.name,
              side: 'left',
              unique_alias: parentCi.unique_alias,
              unique_name: parentCi.unique,
              unique_value: parentCi[parentCi.unique],
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
      this.childCITypes.forEach((child) => {
        const _findCiType = ci_types_list.find((item) => item.id === child.id)
        if (this.secondCIs[child.name]) {
          this.secondCIs[child.name].forEach((childCi) => {
            nodes.children.push({
              id: `${childCi._id}`,
              Class: Node,
              title: child.alias || child.name,
              name: child.name,
              side: 'right',
              unique_alias: childCi.unique_alias,
              unique_name: childCi.unique,
              unique_value: childCi[childCi.unique],
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
      return { nodes, edges }
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
  mounted() {
    this.init(true)
  },
  methods: {
    async init(isFirst) {
      await Promise.all([this.getParentCITypes(), this.getChildCITypes()])
      Promise.all([this.getFirstCIs(), this.getSecondCIs()]).then(() => {
        if (isFirst && this.$refs.ciDetailRelationTopo) {
          this.$refs.ciDetailRelationTopo.setTopoData(this.topoData)
        }
      })
    },
    async getFirstCIs() {
      await searchCIRelation(`root_id=${Number(this.ciId)}&&level=1&&reverse=1&&count=10000`)
        .then((res) => {
          const firstCIs = {}
          res.result.forEach((item) => {
            this.firstCIJsonAttr[item._type].forEach((attr) => {
              item[`${attr}`] = item[`${attr}`] ? JSON.stringify(item[`${attr}`]) : ''
            })
            if (item.ci_type in firstCIs) {
              firstCIs[item.ci_type].push(item)
            } else {
              firstCIs[item.ci_type] = [item]
            }
          })
          this.firstCIs = firstCIs
        })
        .catch((e) => {})
    },
    async getSecondCIs() {
      await searchCIRelation(`root_id=${Number(this.ciId)}&&level=1&&reverse=0&&count=10000`)
        .then((res) => {
          const secondCIs = {}
          res.result.forEach((item) => {
            this.secondCIJsonAttr[item._type].forEach((attr) => {
              item[`${attr}`] = item[`${attr}`] ? JSON.stringify(item[`${attr}`]) : ''
            })
            if (item.ci_type in secondCIs) {
              secondCIs[item.ci_type].push(item)
            } else {
              secondCIs[item.ci_type] = [item]
            }
          })
          console.log(_.cloneDeep(secondCIs))
          this.secondCIs = secondCIs
        })
        .catch((e) => {})
    },
    async getParentCITypes() {
      await getCITypeParent(this.typeId)
        .then((res) => {
          this.parentCITypes = res.parents

          const firstCIColumns = {}
          const firstCIJsonAttr = {}
          res.parents.forEach((item) => {
            const columns = []
            const jsonAttr = []
            item.attributes.forEach((attr) => {
              columns.push({ key: 'p_' + attr.id, field: attr.name, title: attr.alias, minWidth: '100px' })
              if (attr.value_type === '6') {
                jsonAttr.push(attr.name)
              }
            })
            firstCIJsonAttr[item.id] = jsonAttr
            firstCIColumns[item.id] = columns
            firstCIColumns[item.id].push({
              key: 'p_operation',
              field: 'operation',
              title: '操作',
              width: '60px',
              fixed: 'right',
              slots: {
                default: 'operation_default',
              },
              align: 'center',
            })
          })

          this.firstCIColumns = firstCIColumns
          this.firstCIJsonAttr = firstCIJsonAttr
        })
        .catch((e) => {})
    },
    async getChildCITypes() {
      await getCITypeChildren(this.typeId)
        .then((res) => {
          this.childCITypes = res.children

          const secondCIColumns = {}
          const secondCIJsonAttr = {}
          res.children.forEach((item) => {
            const columns = []
            const jsonAttr = []
            item.attributes.forEach((attr) => {
              columns.push({ key: 'c_' + attr.id, field: attr.name, title: attr.alias, minWidth: '100px' })
              if (attr.value_type === '6') {
                jsonAttr.push(attr.name)
              }
            })
            secondCIJsonAttr[item.id] = jsonAttr
            secondCIColumns[item.id] = columns
            secondCIColumns[item.id].push({
              key: 'c_operation',
              field: 'operation',
              title: '操作',
              width: '60px',
              fixed: 'right',
              slots: {
                default: 'operation_default',
              },
              align: 'center',
            })
          })

          this.secondCIColumns = secondCIColumns
          this.secondCIJsonAttr = secondCIJsonAttr
        })
        .catch((e) => {})
    },
    reload() {
      this.init()
    },
    deleteRelation(first_ci_id, second_ci_id) {
      deleteCIRelationView(first_ci_id, second_ci_id).then((res) => {
        this.init()
        if (this.relationViewRefreshNumber) {
          this.relationViewRefreshNumber()
        }
      })
    },
    handleChangeActiveKey(e) {
      if (e.target.value === '1') {
        this.$nextTick(() => {
          this.$refs.ciDetailRelationTopo.setTopoData(this.topoData)
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.ci-detail-relation {
  .ci-detail-relation-table-title {
    font-size: 16px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 5px;
    color: #303133;
  }
}
</style>
