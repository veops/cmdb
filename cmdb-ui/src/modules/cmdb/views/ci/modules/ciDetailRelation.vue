<template>
  <div class="ci-detail-relation">
    <a-radio-group v-model="activeKey" size="small" @change="handleChangeActiveKey">
      <a-radio-button value="1">
        {{ $t('cmdb.ci.topo') }}
      </a-radio-button>
      <a-radio-button value="2">
        {{ $t('cmdb.ci.table') }}
      </a-radio-button>
    </a-radio-group>
    <CiDetailRelationTopo ref="ciDetailRelationTopo" v-if="activeKey === '1'" />
    <template v-if="activeKey === '2'">
      <template v-for="parent in parentCITypes">
        <div :key="'ctr_' + parent.ctr_id">
          <div class="ci-detail-relation-table-title">
            {{ parent.alias || parent.name }}
            <a
              :disabled="!canEdit[parent.id]"
              @click="
                () => {
                  $refs.addTableModal.openModal({ [`${ci.unique}`]: ci[ci.unique] }, ci._id, parent, 'parents')
                }
              "
            ><a-icon
              type="plus-square"
            /></a>
            <span v-if="!canEdit[parent.id]">（{{ $t('cmdb.ci.m2mTips') }}）</span>
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
            <template #reference_default="{ row, column }">
              <a
                v-for="(id) in (column.params.attr.is_list ? row[column.field] : [row[column.field]])"
                :key="id"
                :href="`/cmdb/cidetail/${column.params.attr.reference_type_id}/${id}`"
                target="_blank"
              >
                {{ getReferenceName(id, column) }}
              </a>
            </template>
            <template #operation_default="{ row }">
              <a-popconfirm
                arrowPointAtCenter
                :title="$t('cmdb.ci.confirmDeleteRelation')"
                @confirm="deleteRelation(row._id, ciId)"
              >
                <a
                  :disabled="!canEdit[parent.id]"
                  :style="{
                    color: !canEdit[parent.id] ? 'rgba(0, 0, 0, 0.25)' : 'red',
                  }"
                ><a-icon
                  type="delete"
                /></a>
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
              :disabled="!canEdit[child.id]"
              @click="
                () => {
                  $refs.addTableModal.openModal({ [`${ci.unique}`]: ci[ci.unique] }, ci._id, child, 'children')
                }
              "
            ><a-icon
              type="plus-square"
            /></a>
            <span v-if="!canEdit[child.id]">（{{ $t('cmdb.ci.m2mTips') }}）</span>
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
            <template #reference_default="{ row, column }">
              <a
                v-for="(id) in (column.params.attr.is_list ? row[column.field] : [row[column.field]])"
                :key="id"
                :href="`/cmdb/cidetail/${column.params.attr.reference_type_id}/${id}`"
                target="_blank"
              >
                {{ getReferenceName(id, column) }}
              </a>
            </template>
            <template #operation_default="{ row }">
              <a-popconfirm
                arrowPointAtCenter
                :title="$t('cmdb.ci.confirmDeleteRelation')"
                @confirm="deleteRelation(ciId, row._id)"
              >
                <a
                  :disabled="!canEdit[child.id]"
                  :style="{
                    color: !canEdit[child.id] ? 'rgba(0, 0, 0, 0.25)' : 'red',
                  }"
                ><a-icon
                  type="delete"
                /></a>
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
import { getCITypeChildren, getCITypeParent, getCanEditByParentIdChildId } from '@/modules/cmdb/api/CITypeRelation'
import { searchCIRelation, deleteCIRelationView } from '@/modules/cmdb/api/CIRelation'
import { searchCI } from '@/modules/cmdb/api/ci'
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
    initQueryLoading: {
      type: Boolean,
      default: false,
    }
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
      canEdit: {},
      topoData: {
        nodes: {},
        edges: []
      },
      referenceCINameMap: {}
    }
  },
  computed: {
    exsited_ci() {
      const _exsited_ci = [this.ciId]
      this.parentCITypes.forEach((parent) => {
        if (this.firstCIs[parent.name]) {
          this.firstCIs[parent.name].forEach((parentCi) => {
            _exsited_ci.push(parentCi._id)
          })
        }
      })
      this.childCITypes.forEach((child) => {
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
  mounted() {
    if (!this.initQueryLoading) {
      this.init(true)
    }
  },
  methods: {
    async init(isFirst) {
      const ci_types_list = this.ci_types()
      const _findCiType = ci_types_list.find((item) => item.id === this.typeId)
      if (!_findCiType) {
        return
      }

      await Promise.all([this.getParentCITypes(), this.getChildCITypes()])
      Promise.all([this.getFirstCIs(), this.getSecondCIs()]).then(() => {
        this.handleTopoData()
        if (
          isFirst &&
          this.$refs.ciDetailRelationTopo &&
          ci_types_list.length
        ) {
          this.$refs.ciDetailRelationTopo.exsited_ci = this.exsited_ci
          this.$refs.ciDetailRelationTopo.setTopoData(this.topoData)
        }

        this.handleReferenceCINameMap()
      })
    },
    async getFirstCIs() {
      await searchCIRelation(`root_id=${Number(this.ciId)}&level=1&reverse=1&count=10000`)
        .then((res) => {
          const firstCIs = {}
          res.result.forEach((item) => {
            this.firstCIJsonAttr[item._type].forEach((attr) => {
              item[`${attr}`] = item[`${attr}`] ? JSON.stringify(item[`${attr}`]) : ''
            })
            this.formatCI(item, this.firstCIColumns)
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
      await searchCIRelation(`root_id=${Number(this.ciId)}&level=1&reverse=0&count=10000`)
        .then((res) => {
          const secondCIs = {}
          res.result.forEach((item) => {
            this.secondCIJsonAttr[item._type].forEach((attr) => {
              item[`${attr}`] = item[`${attr}`] ? JSON.stringify(item[`${attr}`]) : ''
            })
            this.formatCI(item, this.secondCIColumns)
            if (item.ci_type in secondCIs) {
              secondCIs[item.ci_type].push(item)
            } else {
              secondCIs[item.ci_type] = [item]
            }
          })
          this.secondCIs = secondCIs
        })
        .catch((e) => {})
    },

    formatCI(ci, columns) {
      Object.keys(ci).forEach((key) => {
        const attr = columns?.[ci?._type]?.find((item) => item?.params?.attr?.name === key)?.params?.attr
        if (attr?.is_choice && attr?.choice_value?.length) {
          if (attr?.is_list) {
            ci[key] = ci[key].map((value) => {
              const label = attr?.choice_value?.find((choice) => choice?.[0] === value)?.[1]?.label
              return label || ci[key]
            })
          } else {
            const label = attr?.choice_value?.find((choice) => choice?.[0] === ci[key])?.[1]?.label
            ci[key] = label || ci[key]
          }
        }
      })

      return ci
    },

    async getParentCITypes() {
      const res = await getCITypeParent(this.typeId)
      this.parentCITypes = res.parents
      for (let i = 0; i < res.parents.length; i++) {
        await getCanEditByParentIdChildId(res.parents[i].id, this.typeId).then((p_res) => {
          this.canEdit = {
            ..._.cloneDeep(this.canEdit),
            [res.parents[i].id]: p_res.result,
          }
        })
      }
      const firstCIColumns = {}
      const firstCIJsonAttr = {}
      res.parents.forEach((item) => {
        const columns = []
        const jsonAttr = []
        item.attributes.forEach((attr) => {
          const column = {
            key: 'p_' + attr.id,
            field: attr.name,
            title: attr.alias,
            minWidth: '100px',
            params: {
              attr
            },
          }
          if (attr.is_reference) {
            column.slots = {
              default: 'reference_default'
            }
          }
          columns.push(column)

          if (attr.value_type === '6') {
            jsonAttr.push(attr.name)
          }
        })
        firstCIJsonAttr[item.id] = jsonAttr
        firstCIColumns[item.id] = columns
        firstCIColumns[item.id].push({
          key: 'p_operation',
          field: 'operation',
          title: this.$t('operation'),
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
    },
    async getChildCITypes() {
      const res = await getCITypeChildren(this.typeId)

      this.childCITypes = res.children
      for (let i = 0; i < res.children.length; i++) {
        await getCanEditByParentIdChildId(this.typeId, res.children[i].id).then((c_res) => {
          this.canEdit = {
            ..._.cloneDeep(this.canEdit),
            [res.children[i].id]: c_res.result,
          }
        })
      }
      const secondCIColumns = {}
      const secondCIJsonAttr = {}
      res.children.forEach((item) => {
        const columns = []
        const jsonAttr = []
        item.attributes.forEach((attr) => {
          const column = {
            key: 'c_' + attr.id,
            field: attr.name,
            title: attr.alias,
            minWidth: '100px',
            params: {
              attr
            },
          }
          if (attr.is_reference) {
            column.slots = {
              default: 'reference_default'
            }
          }
          columns.push(column)

          if (attr.value_type === '6') {
            jsonAttr.push(attr.name)
          }
        })
        secondCIJsonAttr[item.id] = jsonAttr
        secondCIColumns[item.id] = columns
        secondCIColumns[item.id].push({
          key: 'c_operation',
          field: 'operation',
          title: this.$t('operation'),
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
    },

    async handleReferenceCINameMap() {
      const CITypes = _.unionBy(
        [
          ...this.parentCITypes,
          ...this.childCITypes
        ],
        'id'
      )
      const CIList = _.unionBy(
        _.flatten(
          [
            ...Object.values(this.firstCIs),
            ...Object.values(this.secondCIs)
          ]
        ),
        '_id'
      )

      const CIMap = {}
      CIList.forEach((ci) => {
        if (!CIMap[ci._type]) {
          CIMap[ci._type] = []
        }
        CIMap[ci._type].push(ci)
      })

      const referenceCINameMap = {}
      CITypes.forEach((CIType) => {
        CIType.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            const currentCIList = CIMap[CIType.id]
            if (currentCIList?.length) {
              currentCIList.forEach((ci) => {
                const ids = Array.isArray(ci[attr.name]) ? ci[attr.name] : ci[attr.name] ? [ci[attr.name]] : []

                if (ids.length) {
                  if (!referenceCINameMap?.[attr.reference_type_id]) {
                    referenceCINameMap[attr.reference_type_id] = {}
                  }
                  ids.forEach((id) => {
                    referenceCINameMap[attr.reference_type_id][id] = ''
                  })
                }
              })
            }
          }
        })
      })

      if (!Object.keys(referenceCINameMap).length) {
        return
      }

      const allRes = await Promise.all(
        Object.keys(referenceCINameMap).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(referenceCINameMap[key]).join(';')})`,
            count: 9999
          })
        })
      )
      const CITypeList = this.ci_types()
      const showNameMap = {}

      Object.keys(referenceCINameMap).forEach((id) => {
        const CIType = CITypeList.find((CIType) => Number(CIType.id) === Number(id))

        showNameMap[id] = {
          show_name: CIType?.show_name,
          unique_key: CIType?.unique_key
        }
      })

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (referenceCINameMap?.[item._type]?.[item._id] === '') {
            const showName = showNameMap?.[item._type]

            referenceCINameMap[item._type][item._id] = item?.[showName?.show_name] ?? item?.[showName?.unique_key] ?? ''
          }
        })
      })

      this.referenceCINameMap = referenceCINameMap
    },

    getReferenceName(id, column) {
      const typeId = column?.params?.attr?.reference_type_id
      return this.referenceCINameMap?.[typeId]?.[id] || id
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
          this.$refs.ciDetailRelationTopo.exsited_ci = this.exsited_ci
          this.$refs.ciDetailRelationTopo.setTopoData(this.topoData)
        })
      }
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
      const unique_id = _findCiType.show_id || this.attributes().unique_id
      const unique_name = _findCiType.show_name || this.attributes().unique
      const _findUnique = this.attrList().find((attr) => attr.id === unique_id)
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
      this.parentCITypes.forEach((parent) => {
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
      this.childCITypes.forEach((child) => {
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
  .ci-detail-relation-table-title {
    font-size: 16px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 5px;
    color: #303133;
  }
}
</style>
