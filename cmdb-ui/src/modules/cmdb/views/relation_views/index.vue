<template>
  <div :style="{ marginBottom: '-24px', overflow: 'hidden' }">
    <div v-if="relationViews.name2id && relationViews.name2id.length" class="relation-views-wrapper">
      <SplitPane
        :min="200"
        :max="500"
        :paneLengthPixel.sync="paneLengthPixel"
        :appName="`cmdb-relation-views-${viewId}`"
        :triggerLength="18"
        calcBasedParent
      >
        <template #one>
          <div class="relation-views-left" :style="{ height: `${windowHeight - 64}px` }">
            <div class="relation-views-left-header">
              <div class="relation-views-left-header-icon">
                <ops-icon type="ops-cmdb-relation" />
              </div>

              <div class="relation-views-left-header-name relation-views-text-scroll">
                <span>
                  {{ viewName }}
                </span>
              </div>

              <a-dropdown
                overlayClassName="relation-views-left-header-dropdown"
              >
                <div class="relation-views-left-header-down">
                  <ops-icon type="veops-switch1" />
                </div>

                <a-menu
                  slot="overlay"
                  :selectedKeys="[viewId]"
                  class="relation-views-left-header-menu"
                >
                  <a-menu-item
                    v-for="(item) in relationViewMenu"
                    :key="item.id"
                    @click="clickRelationViewMenu(item.id)"
                  >
                    <a class="relation-views-left-header-menu-item">
                      <div class="relation-views-left-header-menu-name relation-views-text-scroll">
                        <span>{{ item.name }}</span>
                      </div>
                      <a-icon
                        class="relation-views-left-header-menu-grant"
                        type="user-add"
                        @click.stop="handlePerm(item.name)"
                      />
                    </a>
                  </a-menu-item>
                </a-menu>
              </a-dropdown>
            </div>
            <a-input
              :placeholder="$t('cmdb.serviceTree.searchTips')"
              class="relation-views-left-input"
              @pressEnter="handleSearchFull"
              v-model="fullSearchValue"
            >
              <a-icon slot="prefix" type="search" />
            </a-input>
            <div
              class="ops-list-batch-action"
              :style="{ marginBottom: '10px' }"
              v-if="showBatchLevel !== null && batchTreeKey && batchTreeKey.length"
            >
              <span
                @click="
                  () => {
                    $refs.grantModal.open('depart')
                  }
                "
              >{{ $t('grant') }}</span
              >
              <span
                @click="
                  () => {
                    $refs.revokeModal.open()
                  }
                "
              >{{ $t('revoke') }}</span
              >
              <template v-if="showBatchLevel > 0">
                <span @click="batchDeleteCIRelationFromTree">{{ $t('cmdb.serviceTree.remove') }}</span>
              </template>
              <span
                @click="
                  () => {
                    showBatchLevel = null
                    batchTreeKey = []
                  }
                "
              >{{ $t('cancel') }}</span
              >
              <span>{{ $t('selectRows', { rows: batchTreeKey.length }) }}</span>
            </div>
            <a-tree
              v-if="!isFullSearch"
              :selectedKeys="selectedKeys"
              :loadData="onLoadData"
              :treeData="treeData"
              draggable
              @dragenter="onDragEnter"
              @drop="onDrop"
              :expandedKeys="expandedKeys"
            >
              <template #title="treeNodeData">
                <ContextMenu
                  :treeNodeData="treeNodeData"
                  :levels="levels"
                  :currentViews="relationViews.views[viewName]"
                  :id2type="relationViews.id2type"
                  @onContextMenuClick="onContextMenuClick"
                  @onNodeClick="onNodeClick"
                  :ciTypeIcons="ciTypeIcons"
                  :showBatchLevel="showBatchLevel"
                  :batchTreeKey="batchTreeKey"
                  @clickCheckbox="clickCheckbox"
                  @updateTreeData="updateTreeData"
                />
              </template>
            </a-tree>
            <a-tree
              v-else
              :treeData="filterFullTreeData"
              defaultExpandAll
              :selectedKeys="selectedKeys"
              :expandedKeys="expandedKeys"
            >
              <template #title="treeNodeData">
                <ContextMenu
                  :treeNodeData="treeNodeData"
                  :levels="levels"
                  :currentViews="relationViews.views[viewName]"
                  :id2type="relationViews.id2type"
                  @onContextMenuClick="onContextMenuClick"
                  @onNodeClick="onNodeClick"
                  :ciTypeIcons="ciTypeIcons"
                  :showBatchLevel="showBatchLevel"
                  :batchTreeKey="batchTreeKey"
                  @clickCheckbox="clickCheckbox"
                  @updateTreeData="updateTreeData"
                  :fullSearchValue="fullSearchValue"
                />
              </template>
            </a-tree>
          </div>
        </template>
        <template #two>
          <div id="relation-views-right" class="relation-views-right" :style="{ height: `${windowHeight - 64}px` }">
            <a-tabs :activeKey="currentTypeId[0]" class="ops-tab" @change="changeCIType" size="small">
              <a-tab-pane v-for="item in showTypes" :key="item.id" :tab="item.alias || item.name"> </a-tab-pane>
              <a-space slot="tabBarExtraContent">
                <a-button
                  v-if="isLeaf"
                  type="primary"
                  class="ops-button-ghost"
                  ghost
                  @click="$refs.create.handleOpen(true, 'create')"
                ><ops-icon type="veops-increase" />{{ $t('create') }}</a-button
                >
                <a-button icon="user-add" type="primary" ghost @click="handlePerm" class="ops-button-ghost">{{
                  $t('grant')
                }}</a-button>
                <EditAttrsPopover
                  :typeId="Number(currentTypeId[0])"
                  class="operation-icon"
                  @refresh="refreshAfterEditAttrs"
                >
                  <a-button
                    type="primary"
                    ghost
                    class="ops-button-ghost"
                  ><ops-icon type="veops-configuration_table" />{{ $t('cmdb.configTable') }}</a-button
                  >
                </EditAttrsPopover>
              </a-space>
            </a-tabs>
            <SearchForm
              ref="search"
              @refresh="refreshTable"
              :preferenceAttrList="preferenceAttrList"
              :isShowExpression="!(isLeaf && isShowBatchIcon)"
              :typeId="Number(currentTypeId[0])"
              @copyExpression="copyExpression"
              type="relationView"
            >
              <PreferenceSearch
                v-if="!(isLeaf && isShowBatchIcon)"
                ref="preferenceSearch"
                @getQAndSort="getQAndSort"
                @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
              />
              <a-space slot="extraContent">
                <div class="ops-list-batch-action" v-if="isLeaf && isShowBatchIcon">
                  <template v-if="selectedRowKeys.length">
                    <span @click="$refs.create.handleOpen(true, 'update')">{{ $t('update') }}</span>
                    <span @click="openBatchDownload">{{ $t('download') }}</span>
                    <span @click="batchDelete">{{ $t('cmdb.ciType.deleteInstance') }}</span>
                    <span @click="batchDeleteCIRelation">{{ $t('cmdb.history.deleteRelation') }}</span>
                    <span>{{ $t('cmdb.ci.selectRows', { rows: selectedRowKeys.length }) }}</span>
                  </template>
                </div>
              </a-space>
            </SearchForm>

            <CITable
              ref="xTable"
              :id="`cmdb-relation-${viewId}-${currentTypeId}`"
              :loading="loading"
              :attrList="preferenceAttrList"
              :columns="columns"
              :passwordValue="passwordValue"
              :data="instanceList"
              :height="tableHeight"
              :showCheckbox="isLeaf"
              :showDelete="isLeaf"
              @onSelectChange="onSelectChange"
              @edit-closed="handleEditClose"
              @edit-actived="handleEditActived"
              @sort-change="handleSortCol"
              @openDetail="openDetail"
              @deleteCI="deleteCI"
            />

            <div :style="{ textAlign: 'right', marginTop: '4px' }">
              <a-pagination
                :showSizeChanger="true"
                v-model="pageNo"
                size="small"
                :total="numfound"
                show-quick-jumper
                :page-size="pageSize"
                :page-size-options="pageSizeOptions"
                @showSizeChange="onShowSizeChange"
                :show-total="
                  (total, range) =>
                    $t('pagination.total', {
                      range0: range[0],
                      range1: range[1],
                      total,
                    })
                "
              >
                <template slot="buildOptionText" slot-scope="props">
                  <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('cmdb.history.itemsPerPage') }}</span>
                  <span v-if="props.value === '100000'">{{ $t('cmdb.components.all') }}</span>
                </template>
              </a-pagination>
            </div>
          </div>
        </template>
      </SplitPane>
    </div>
    <a-alert
      :message="$t('noData')"
      banner
      v-else-if="relationViews.name2id && !relationViews.name2id.length"
    ></a-alert>
    <AddTableModal ref="addTableModal" @reload="reload" />
    <CMDBGrant ref="cmdbGrant" resourceType="RelationView" app_id="cmdb" />
    <GrantModal ref="grantModal" @handleOk="onRelationViewGrant" :customTitle="$t('cmdb.serviceTree.grantTitle')" />
    <CiDetailDrawer ref="detail" :typeId="Number(currentTypeId[0])" />
    <create-instance-form
      ref="create"
      :typeIdFromRelation="Number(currentTypeId[0])"
      @reload="sumbitFromCreateInstance"
      @submit="batchUpdateFromCreateInstance"
    />
    <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
    <ReadPermissionsModal ref="readPermissionsModal" />
    <RevokeModal ref="revokeModal" @handleRevoke="handleRevoke" />
  </div>
</template>

<script>
import _ from 'lodash'
import { Tree } from 'element-ui'
import Sortable from 'sortablejs'
import SearchForm from '../../components/searchForm/SearchForm.vue'
import { getCITableColumns } from '../../utils/helper'
import AddTableModal from './modules/AddTableModal'
import ContextMenu from './modules/ContextMenu.vue'
import { getRelationView, getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import {
  searchCIRelation,
  statisticsCIRelation,
  deleteCIRelationView,
  batchDeleteCIRelation,
  batchUpdateCIRelationChildren,
  addCIRelationView,
  searchCIRelationFull,
} from '@/modules/cmdb/api/CIRelation'

import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { searchCI2, updateCI, deleteCI } from '@/modules/cmdb/api/ci'
import { getCITypeIcons, grantCiType, revokeCiType } from '../../api/CIType'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import SplitPane from '@/components/SplitPane'
import EditAttrsPopover from '../ci/modules/editAttrsPopover.vue'
import CiDetailDrawer from '../ci/modules/ciDetailDrawer.vue'
import CreateInstanceForm from '../ci/modules/CreateInstanceForm'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import CMDBGrant from '../../components/cmdbGrant'
import GrantModal from '../../components/cmdbGrant/grantModal.vue'
import { getAttrPassword } from '../../api/CITypeAttr'
import ReadPermissionsModal from './modules/ReadPermissionsModal.vue'
import RevokeModal from '../../components/cmdbGrant/revokeModal.vue'
import CITable from '@/modules/cmdb/components/ciTable/index.vue'

const relationViewKeyStorage = 'cmdb_relation_view_menu_key'

export default {
  name: 'RelationViews',
  components: {
    SearchForm,
    AddTableModal,
    ContextMenu,
    CMDBGrant,
    GrantModal,
    SplitPane,
    ElTree: Tree,
    EditAttrsPopover,
    CiDetailDrawer,
    CreateInstanceForm,
    BatchDownload,
    PreferenceSearch,
    ReadPermissionsModal,
    RevokeModal,
    CITable
  },
  data() {
    return {
      treeData: [],
      triggerSelect: false,
      treeNode: null,
      ciTypeIcons: {},
      relationViews: {},
      levels: [],
      showTypeIds: [],
      origShowTypeIds: [],
      showTypes: [],
      origShowTypes: [],
      leaf2showTypes: {},
      node2ShowTypes: {},
      level2constraint: {},
      leaf: [],
      typeId: null,
      viewId: null,
      viewName: null,
      currentView: null,
      currentTypeId: [],
      instanceList: [],
      numfound: 0,
      pageNo: 1,
      pageSize: 50,
      pageSizeOptions: ['50', '100', '200', '100000'],
      treeKeys: [],
      expandedKeys: [],
      columns: [],
      loading: false,
      preferenceAttrList: [],
      selectedRowKeys: [],
      paneLengthPixel: 210,
      attrList: [],
      attributes: {},
      // 对照是否编辑
      initialInstanceList: [],
      sortByTable: undefined,
      // 表格拖拽的参数
      tableDragClassName: [],

      resource_type: {},

      initialPasswordValue: {},
      passwordValue: {},
      lastEditCiId: null,
      isContinueCloseEdit: true,

      contextMenuKey: null,
      showBatchLevel: null,
      batchTreeKey: [],

      statisticsObj: {},
      viewOption: {},
      loadRootStatisticsParams: {},
      fullSearchValue: '',
      isFullSearch: false,
      fullTreeData: [],
      filterFullTreeData: [],

      lastSelected: [], // checkbox range 记录
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      return this.windowHeight - 244
    },
    selectedKeys() {
      return [this.treeKeys.join('@^@')]
    },
    isLeaf() {
      return this.treeKeys.length === this.levels.length
    },
    isShowBatchIcon() {
      return !!this.selectedRowKeys.length
    },
    topo_flatten() {
      return this.relationViews?.views[this.viewName]?.topo_flatten ?? []
    },
    descendant_ids() {
      return this.topo_flatten.slice(this.treeKeys.length).join(',')
    },
    descendant_ids_for_statistics() {
      return this.topo_flatten.slice(this.treeKeys.length + 1).join(',')
    },
    root_parent_path() {
      return this.treeKeys
        .slice(0, this.treeKeys.length)
        .map((item) => item.split('%')[0])
        .join(',')
    },
    is_show_leaf_node() {
      return this.viewOption?.is_show_leaf_node ?? true
    },
    is_show_tree_node() {
      return this.viewOption?.is_show_tree_node ?? false
    },
    leaf_tree_sort() {
      return this.viewOption?.sort ?? 1
    },
    relationViewMenu() {
      const name2id = this?.relationViews?.name2id || []
      return name2id.map((item) => {
        return {
          id: item?.[1] || -1,
          name: item?.[0] || ''
        }
      })
    }
  },
  provide() {
    return {
      handleSearch: this.refreshTable,
      setPreferenceSearchCurrent: this.setPreferenceSearchCurrent,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      },
      relationViewRefreshNumber: this.relationViewRefreshNumber,
      filterCompPreferenceSearch: () => {
        return { prv_id: this.viewId }
      },
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  created() {
    this.getRelationViews()
    this.getCITypesList()
  },
  mounted() {
    setTimeout(() => {
      this.columnDrop()
    }, 1000)
  },
  beforeDestroy() {
    if (this.sortable) {
      this.sortable.destroy()
    }
  },
  inject: ['reload'],
  watch: {
    pageNo: function(newPage, oldPage) {
      this.loadData({ parameter: { pageNo: newPage }, refreshType: undefined, sortByTable: this.sortByTable })
    },
  },

  methods: {
    async getAttributeList() {
      await getCITypeAttributesById(Number(this.currentTypeId[0])).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },
    getCITypesList() {
      getCITypeIcons().then((res) => {
        this.ciTypeIcons = res
      })
    },
    refreshTable() {
      this.selectedRowKeys = []
      this.sortByTable = undefined
      const xTable = this.$refs.xTable.getVxetableRef()
      if (xTable) {
        xTable.clearCheckboxRow()
        xTable.clearCheckboxReserve()
        xTable.clearSort()
      }
      this.loadData()
    },

    async loadData({ parameter, refreshType = undefined, sortByTable = undefined } = {}) {
      // refreshType='refreshNumber' 树图只更新number
      const params = Object.assign(parameter || {}, (this.$refs.search || {}).queryParam)
      let q = ''
      Object.keys(params).forEach((key) => {
        if (!['pageNo', 'pageSize', 'sortField', 'sortOrder'].includes(key) && params[key] + '' !== '') {
          if (typeof params[key] === 'object' && params[key] && params[key].length > 1) {
            q += `,${key}:(${params[key].join(';')})`
          } else if (params[key]) {
            q += `,${key}:*${params[key]}*`
          }
        }
      })

      const expression = (this.$refs['search'] || {}).expression || ''
      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const regSort = /(?<=sort=).+/g

      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      if (exp) {
        q = `${q},${exp}`
      }

      let sort
      if (sortByTable) {
        sort = sortByTable
      } else {
        sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
      }
      if (sort) {
        q = `${q}&sort=${sort}`
      }
      if ('pageNo' in params) {
        q += `&page=${params['pageNo']}&count=${this.pageSize}`
      } else {
        q += `&page=1&count=${this.pageSize}`
      }

      if ('sortField' in params) {
        let order = ''
        if (params['sortOrder'] !== 'ascend') {
          order = '-'
        }
        q += `&sort=${order}${params['sortField']}`
      }
      if (q && q[0] === ',') {
        q = q.slice(1)
      }

      if (this.treeKeys.length === 0) {
        if (!refreshType && !this.isFullSearch) {
          await this.loadRoot()
        }
      } else {
        q += `&root_id=${this.treeKeys[this.treeKeys.length - 1].split('%')[0]}`

        if (
          Object.keys(this.level2constraint).some(
            (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
          )
        ) {
          q += `&ancestor_ids=${this.treeKeys
            .slice(0, this.treeKeys.length - 1)
            .map((item) => item.split('%')[0])
            .join(',')}`
        }

        await this.judgeCITypes()

        const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('%')[1])
        let level = []
        if (!this.leaf.includes(typeId)) {
          let startIdx = 0
          this.levels.forEach((item, idx) => {
            if (item.includes(typeId)) {
              startIdx = idx
            }
          })

          this.leaf.forEach((leafId) => {
            this.levels.forEach((item, levelIdx) => {
              if (item.includes(leafId) && levelIdx - startIdx + 1 > 0) {
                level.push(levelIdx - startIdx + 1)
              }
            })
          })
        } else {
          level = [1]
        }

        q += `&level=${this.topo_flatten.includes(this.currentTypeId[0]) ? 1 : level.join(',')}`
        if (!refreshType && !this.isFullSearch) {
          this.loadNoRoot(this.treeKeys[this.treeKeys.length - 1], level)
        }
        const fuzzySearch = (this.$refs['search'] || {}).fuzzySearch || ''
        if (fuzzySearch) {
          q = `q=_type:${this.currentTypeId[0]},*${fuzzySearch}*,` + q
        } else {
          q = `q=_type:${this.currentTypeId[0]},` + q
        }
        if (Object.values(this.level2constraint).includes('2')) {
          q = q + `&has_m2m=1`
        }
        if (this.root_parent_path) {
          q = q + `&root_parent_path=${this.root_parent_path}`
        }
        q = q + `&descendant_ids=${this.descendant_ids}`
        if (this.currentTypeId[0]) {
          const res = await searchCIRelation(q)

          const _data = Object.assign([], res.result)
          _data.forEach((item, index) => (item.key = item._id))
          this.numfound = res.numfound
          this.pageNo = res.page

          const jsonAttrList = this.preferenceAttrList.filter((attr) => attr.value_type === '6')
          this.instanceList = _data.map((item) => {
            jsonAttrList.forEach(
              (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
            )
            return { ..._.cloneDeep(item) }
          })
          this.initialInstanceList = _.cloneDeep(this.instanceList)

          this.calcColumns()
        }
        if (refreshType === 'refreshNumber') {
          this.treeKeys.map((key, index) => {
            let ancestor_ids
            if (
              Object.keys(this.level2constraint).some(
                (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
              )
            ) {
              ancestor_ids = `${this.treeKeys
                .slice(0, index)
                .map((item) => item.split('%')[0])
                .join(',')}`
            }
            statisticsCIRelation({
              ancestor_ids,
              root_ids: key.split('%')[0],
              level: this.treeKeys.length - index,
              type_ids: this.leaf2showTypes[this.leaf[0]].join(','),
              has_m2m: Number(Object.values(this.level2constraint).includes('2')),
              descendant_ids: this.descendant_ids_for_statistics,
            }).then((res) => {
              let result
              const getTreeItem = (data, id) => {
                for (let i = 0; i < data.length; i++) {
                  if (Number(data[i].id) === Number(id)) {
                    result = data[i] // 结果赋值
                    break
                  } else {
                    if (data[i].children && data[i].children.length) {
                      getTreeItem(data[i].children, id)
                    }
                  }
                }
              }
              getTreeItem(this.treeData, key.split('%')[0])

              const reg = /(?<=\()\S+(?=\))/g
              result.title = result.title.replace(reg, `${res[key.split('%')[0]]}`)
            })
          })
        }
      }
    },

    changeCIType(typeId) {
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.search.reset()
      this.selectedRowKeys = []
      this.currentTypeId = [typeId]
      this.loadColumns()
    },

    async judgeCITypes() {
      let _showTypeIds = []
      let _showTypes = []
      if (this.treeKeys.length) {
        if (this.is_show_leaf_node) {
          const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('%')[1])
          _showTypeIds = _.cloneDeep(this.origShowTypeIds)
          _showTypes = _.cloneDeep(this.node2ShowTypes[typeId])
        }
        if (this.is_show_tree_node) {
          const treeKeyTypeId = Number(this.treeKeys.slice(-1)[0].split('%')[1])
          const _idx = this.topo_flatten.findIndex((item) => item === treeKeyTypeId)
          if (_idx > -1 && _idx < this.topo_flatten.length - 1) {
            const _showTreeTypeId = this.topo_flatten[_idx + 1]
            const _showTreeTypes = this.relationViews.id2type[_showTreeTypeId]
            if (this.leaf_tree_sort === 1) {
              _showTypeIds.push(_showTreeTypeId)
              _showTypes.push(_showTreeTypes)
            } else {
              _showTypeIds.unshift(_showTreeTypeId)
              _showTypes.unshift(_showTreeTypes)
            }
          }
        }
        this.showTypeIds = _showTypeIds
        this.showTypes = _showTypes
      } else {
        this.showTypeIds = _.cloneDeep(this.origShowTypeIds)
        this.showTypes = JSON.parse(JSON.stringify(this.origShowTypes))
      }
      if (
        !this.currentTypeId.length ||
        (this.currentTypeId.length && !this.showTypeIds.includes(this.currentTypeId[0]))
      ) {
        this.currentTypeId = [this.showTypeIds[0]]
        await this.loadColumns()
      }
    },

    async loadRoot() {
      await searchCI2(`q=_type:(${this.levels[0].join(';')})&count=10000&use_id_filter=1`).then(async (res) => {
        const facet = []
        const ciIds = []
        res.result.forEach((item) => {
          const showName = this.relationViews.id2type[item._type]?.show_name ?? null
          facet.push({
            showName,
            showNameValue: item[showName] ?? null,
            uniqueValue: item[item.unique],
            number: 0,
            ciId: item._id,
            typeId: item._type,
            unique: item.unique,
          })
          ciIds.push(item._id)
        })

        const leafId = this.leaf[0]
        let level = 0
        this.levels.forEach((item, idx) => {
          if (item.includes(leafId)) {
            level = idx + 1
          }
        })
        const params = {
          level,
          root_ids: ciIds.join(','),
          has_m2m: Number(Object.values(this.level2constraint).includes('2')),
        }
        this.loadRootStatisticsParams = params
        await statisticsCIRelation({
          ...params,
          type_ids: this.leaf2showTypes[this.leaf[0]].join(','),
          descendant_ids: this.descendant_ids_for_statistics,
        }).then((num) => {
          facet.forEach((item, idx) => {
            item.number += num[ciIds[idx] + '']
          })
        })
        this.wrapTreeData(facet)
        // default select first node
        this.onNodeClick(this.treeData[0].key)
      })
    },

    async loadNoRoot(rootIdAndTypeId, level) {
      const rootId = rootIdAndTypeId.split('%')[0]
      const typeId = Number(rootIdAndTypeId.split('%')[1])
      const index = this.topo_flatten.findIndex((id) => id === typeId)
      const _type = this.topo_flatten[index + 1]
      if (_type) {
        let q = `q=_type:${_type}&root_id=${rootId}&level=1&count=10000`
        if (
          Object.keys(this.level2constraint).some(
            (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
          )
        ) {
          q += `&ancestor_ids=${this.treeKeys
            .slice(0, this.treeKeys.length - 1)
            .map((item) => item.split('%')[0])
            .join(',')}`
        }
        if (Object.values(this.level2constraint).includes('2')) {
          q = q + `&has_m2m=1`
        }
        if (this.root_parent_path) {
          q = q + `&root_parent_path=${this.root_parent_path}`
        }
        q = q + `&descendant_ids=${this.descendant_ids}`
        searchCIRelation(q).then(async (res) => {
          const facet = []
          const ciIds = []
          res.result.forEach((item) => {
            const showName = this.relationViews.id2type[item._type]?.show_name ?? null
            facet.push({
              showName,
              showNameValue: item[showName] ?? null,
              uniqueValue: item[item.unique],
              number: 0,
              ciId: item._id,
              typeId: item._type,
              unique: item.unique,
            })
            ciIds.push(item._id)
          })
          let ancestor_ids
          if (
            Object.keys(this.level2constraint).some(
              (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
            )
          ) {
            ancestor_ids = `${this.treeKeys.map((item) => item.split('%')[0]).join(',')}`
          }
          const promises = level.map((_level) => {
            if (_level > 1) {
              return statisticsCIRelation({
                ancestor_ids,
                root_ids: ciIds.join(','),
                level: _level - 1,
                type_ids: this.leaf2showTypes[this.leaf[0]].join(','),
                has_m2m: Number(Object.values(this.level2constraint).includes('2')),
                descendant_ids: this.descendant_ids_for_statistics,
              }).then((num) => {
                facet.forEach((item, idx) => {
                  item.number += num[ciIds[idx] + '']
                })
              })
            }
          })
          await Promise.all(promises)
          this.wrapTreeData(facet)
        })
      }
    },

    onNodeClick(keys, callback = undefined) {
      this.triggerSelect = true
      if (keys) {
        const _tempKeys = keys.split('@^@').filter((item) => item !== '')
        if (_tempKeys.length === this.levels.length) {
          this.$refs.xTable.getVxetableRef().clearCheckboxRow()
          this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
          this.selectedRowKeys = []
        }
        this.treeKeys = _tempKeys
      }
      const idx = this.expandedKeys.findIndex((item) => item === keys)
      if (idx > -1) {
        this.expandedKeys.splice(idx, 1)
      } else {
        this.expandedKeys.push(keys)
      }

      this.refreshTable()
      if (callback && typeof callback === 'function') {
        callback()
      }
    },
    wrapTreeData(facet) {
      if (this.triggerSelect) {
        return
      }
      const treeData = []
      facet.forEach((item) => {
        const _treeKeys = _.cloneDeep(this.treeKeys)
        _treeKeys.push(item.ciId + '%' + item.typeId + '%' + `{"${item.unique}":"${item.uniqueValue}"}`)
        treeData.push({
          title: item.showName ? item.showNameValue : item.uniqueValue,
          number: item.number,
          key: _treeKeys.join('@^@'),
          isLeaf: this.leaf.includes(item.typeId),
          id: item.ciId,
          showName: item.showName,
        })
      })
      if (this.treeNode === null) {
        this.treeData = treeData
      } else {
        this.treeNode.dataRef.children = treeData
        this.treeData = [...this.treeData]
      }
    },

    onLoadData(treeNode) {
      this.triggerSelect = false
      return new Promise((resolve) => {
        if (treeNode.dataRef.children) {
          resolve()
          return
        }
        this.treeKeys = treeNode.eventKey.split('@^@').filter((item) => item !== '')
        this.treeNode = treeNode
        resolve()
      })
    },

    getRelationViews() {
      getRelationView().then((res) => {
        if (JSON.stringify(res) === '{}') {
          this.relationViews = {
            id2type: {},
            name2id: [],
            views: {},
          }
        } else {
          this.relationViews = res
        }
        if ((Object.keys(this.relationViews.views) || []).length) {
          let viewId = parseInt(localStorage.getItem(relationViewKeyStorage)) || parseInt(this.$route.params.viewId) || this.relationViews.name2id[0][1]
          let viewName = null

          const currentView = this.relationViews.name2id.find((item) => item?.[1] === viewId)
          if (currentView) {
            viewName = currentView[0]
          } else {
            viewId = this.relationViews.name2id[0][1]
            viewName = this.relationViews.name2id[0][0]
          }

          localStorage.setItem(relationViewKeyStorage, viewId)
          this.viewId = viewId
          this.viewName = viewName
          this.refreshData()
        }
      })
    },

    refreshData() {
      this.levels = this.relationViews.views[this.viewName].topo
      this.origShowTypes = this.relationViews.views[this.viewName].show_types
      const showTypeIds = []
      this.origShowTypes.forEach((item) => {
        showTypeIds.push(item.id)
      })
      this.origShowTypeIds = showTypeIds
      this.leaf2showTypes = this.relationViews.views[this.viewName].leaf2show_types
      this.node2ShowTypes = this.relationViews.views[this.viewName].node2show_types
      this.level2constraint = this.relationViews.views[this.viewName].level2constraint
      this.leaf = this.relationViews.views[this.viewName].leaf
      this.currentView = `${this.viewId}`
      this.typeId = this.levels[0][0]
      this.viewOption = this.relationViews.views[this.viewName].option ?? {}

      this.$nextTick(() => {
        this.refreshTable()
      })
    },

    async loadColumns() {
      if (this.currentTypeId[0]) {
        this.getAttributeList()
        const res = await getSubscribeAttributes(this.currentTypeId[0])
        this.preferenceAttrList = res.attributes
        this.calcColumns()
      }
    },

    calcColumns() {
      const width = document.getElementById('relation-views-right').clientWidth
      this.columns = getCITableColumns(this.instanceList, this.preferenceAttrList, width)
      this.columns.forEach((col) => {
        if (col.is_password) {
          this.initialPasswordValue[col.field] = ''
          this.passwordValue[col.field] = ''
        }
      })
      this.$nextTick(() => {
        this.$refs.xTable.getVxetableRef().refreshColumn()
      })
    },
    calculateParamsFromTreeKey(treeKey, menuKey) {
      const splitTreeKey = treeKey.split('@^@')
      const _tempTree = splitTreeKey[splitTreeKey.length - 1].split('%')
      const firstCIObj = JSON.parse(_tempTree[2])
      const firstCIId = _tempTree[0]
      let ancestor_ids
      if (
        Object.keys(this.level2constraint).some(
          (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
        )
      ) {
        const ancestor = treeKey
          .split('@^@')
          .slice(0, menuKey === 'delete' ? treeKey.split('@^@').length - 2 : treeKey.split('@^@').length - 1)
        ancestor_ids = ancestor.map((item) => item.split('%')[0]).join(',')
      }
      return { splitTreeKey, firstCIObj, firstCIId, _tempTree, ancestor_ids }
    },
    onContextMenuClick(treeKey, menuKey) {
      if (treeKey) {
        if (!['batchGrant', 'batchRevoke', 'batchDelete', 'batchCancel'].includes(menuKey)) {
          this.contextMenuKey = treeKey
        }

        const { splitTreeKey, firstCIObj, firstCIId, _tempTree, ancestor_ids } = this.calculateParamsFromTreeKey(
          treeKey,
          menuKey
        )
        if (menuKey === 'delete') {
          const _tempTreeParent = splitTreeKey[splitTreeKey.length - 2].split('%')
          const that = this
          this.$confirm({
            title: that.$t('warning'),
            content: that.$t('confirmDelete2', { name: Object.values(firstCIObj)[0] }),
            onOk() {
              deleteCIRelationView(_tempTreeParent[0], _tempTree[0], { ancestor_ids }).then((res) => {
                that.$message.success(that.$t('deleteSuccess'))
                setTimeout(() => {
                  that.reload()
                }, 500)
              })
            },
          })
        } else if (menuKey === 'grant') {
          this.$refs.grantModal.open('depart')
        } else if (menuKey === 'revoke') {
          this.$refs.revokeModal.open()
        } else if (menuKey === 'view') {
          this.$refs.readPermissionsModal.open(treeKey)
        } else if (menuKey === 'batch') {
          this.showBatchLevel = splitTreeKey.filter((item) => !!item).length - 1
          this.batchTreeKey = []
        } else if (menuKey === 'batchGrant') {
          this.$refs.grantModal.open('depart')
        } else if (menuKey === 'batchRevoke') {
          this.$refs.revokeModal.open()
        } else if (menuKey === 'batchDelete') {
          this.batchDeleteCIRelationFromTree()
        } else if (menuKey === 'batchCancel') {
          this.showBatchLevel = null
          this.batchTreeKey = []
        } else {
          const childTypeId = menuKey

          let typeName = ''
          if (this?.relationViews?.id2type?.[childTypeId]) {
            typeName = this.relationViews.id2type[childTypeId]?.name || ''
          } else {
            const node2show_types = this?.relationViews?.views?.[this.viewName]?.node2show_types
            const typeId = _tempTree?.[1]
            if (node2show_types?.[typeId]?.length) {
              const findType = node2show_types[typeId].find((item) => item.id === childTypeId)
              typeName = findType?.name || ''
            }
          }
          this.$refs.addTableModal.openModal(
            firstCIObj,
            firstCIId,
            {
              id: childTypeId,
              name: typeName
            },
            'children',
            ancestor_ids
          )
        }
      }
    },
    onSelectChange(records) {
      this.selectedRowKeys = records
    },
    batchDeleteCIRelation() {
      const currentShowType = this.showTypes.find((item) => item.id === Number(this.currentTypeId[0]))
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: (h) => (
          <div>
            {that.$t('cmdb.serviceTree.deleteRelationConfirm', { name: currentShowType.alias || currentShowType.name })}
          </div>
        ),
        onOk() {
          const _tempTree = that.treeKeys[that.treeKeys.length - 1].split('%')
          const first_ci_id = Number(_tempTree[0])
          let ancestor_ids
          if (
            Object.keys(that.level2constraint).some(
              (le) => le < Object.keys(that.level2constraint).length && that.level2constraint[le] === '2'
            )
          ) {
            ancestor_ids = `${that.treeKeys
              .slice(0, that.treeKeys.length - 1)
              .map((item) => item.split('%')[0])
              .join(',')}`
          }
          batchDeleteCIRelation(
            that.selectedRowKeys.map((item) => item._id),
            [first_ci_id],
            ancestor_ids
          ).then((res) => {
            that.$refs.xTable.getVxetableRef().clearCheckboxRow()
            that.$refs.xTable.getVxetableRef().clearCheckboxReserve()
            that.selectedRowKeys = []
            that.loadData({ parameter: {}, refreshType: 'refreshNumber' })
          })
        },
      })
    },
    onDragEnter(info) {},
    onDrop(info) {
      const dragKey = info.dragNode.eventKey
      const targetKey = info.node.eventKey
      const _splitDragKey = dragKey.split('@^@')
      const _splitTargetKey = targetKey.split('@^@').filter((item) => item !== '')
      if (_splitDragKey.length - 1 === _splitTargetKey.length) {
        const dragId = _splitDragKey[_splitDragKey.length - 1].split('%')[0]
        const targetId = _splitTargetKey[_splitTargetKey.length - 1].split('%')[0]
        batchUpdateCIRelationChildren([dragId], [targetId]).then((res) => {
          this.reload()
        })
      }
    },
    handlePerm(resourceName) {
      const _resource_name = resourceName ?? this.viewName

      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'RelationView',
        perm: 'grant',
        resource_name: _resource_name,
      }).then((res) => {
        if (res.result) {
          searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
            this.resource_type = { groups: res.groups, id2perms: res.id2perms }
            this.$nextTick(() => {
              this.$refs.cmdbGrant.open({ name: _resource_name, cmdbGrantType: 'relation_view' })
            })
          })
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },
    handleSortCol({ column, property, order, sortBy, sortList, $event }) {
      let sortByTable
      if (order === 'asc') {
        sortByTable = property
      } else if (order === 'desc') {
        sortByTable = `-${property}`
      }
      this.sortByTable = sortByTable
      this.$nextTick(() => {
        if (this.pageNo === 1) {
          this.loadData({ parameter: {}, refreshType: undefined, sortByTable })
        } else {
          this.pageNo = 1
        }
      })
    },
    columnDrop() {
      this.$nextTick(() => {
        const xTable = this.$refs?.xTable?.getVxetableRef?.()
        this.sortable = Sortable.create(
          xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row'),
          {
            handle: '.vxe-handle',
            onChoose: () => {
              const header = xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row')
              const classNameList = []
              header.childNodes.forEach((item) => {
                classNameList.push(item.classList[1])
              })
              this.tableDragClassName = classNameList
            },
            onEnd: (params) => {
              // 由于开启了虚拟滚动，newIndex和oldIndex是虚拟的
              const { newIndex, oldIndex } = params
              // 从tableDragClassName拿到colid
              const fromColid = this.tableDragClassName[oldIndex]
              const toColid = this.tableDragClassName[newIndex]
              const fromColumn = xTable.getColumnById(fromColid)
              const toColumn = xTable.getColumnById(toColid)
              const fromIndex = xTable.getColumnIndex(fromColumn)
              const toIndex = xTable.getColumnIndex(toColumn)
              const tableColumn = xTable.getColumns()
              const currRow = tableColumn.splice(fromIndex, 1)[0]
              tableColumn.splice(toIndex, 0, currRow)
              xTable.loadColumn(tableColumn)
            },
          }
        )
      })
    },
    refreshAfterEditAttrs() {
      this.loadColumns()
    },
    handleEditActived() {
      const passwordCol = this.columns.filter((col) => col.is_password)
      this.$nextTick(() => {
        const editRecord = this.$refs.xTable.getVxetableRef().getEditRecord()
        const { row, column } = editRecord
        if (passwordCol.length && this.lastEditCiId !== row._id) {
          this.$nextTick(async () => {
            for (let i = 0; i < passwordCol.length; i++) {
              await getAttrPassword(row._id, passwordCol[i].attr_id).then((res) => {
                this.initialPasswordValue[passwordCol[i].field] = res.value
                this.passwordValue[passwordCol[i].field] = res.value
              })
            }
            this.isContinueCloseEdit = false
            await this.$refs.xTable.getVxetableRef().clearEdit()
            this.isContinueCloseEdit = true
            this.$nextTick(() => {
              this.$refs.xTable.getVxetableRef().setEditCell(row, column.field)
            })
          })
        }
        this.lastEditCiId = row._id
      })
    },
    handleEditClose({ row, rowIndex, column }) {
      if (!this.isContinueCloseEdit) {
        return
      }
      const $table = this.$refs['xTable'].getVxetableRef()
      const data = {}
      this.columns.forEach((item) => {
        if (
          !(item.field in this.initialPasswordValue) &&
          !_.isEqual(row[item.field], this.initialInstanceList[rowIndex][item.field])
        ) {
          data[item.field] = row[item.field] ?? null
        }
      })
      Object.keys(this.initialPasswordValue).forEach((key) => {
        if (this.initialPasswordValue[key] !== this.passwordValue[key]) {
          data[key] = this.passwordValue[key]
          row[key] = this.passwordValue[key]
        }
      })
      this.lastEditCiId = null
      if (JSON.stringify(data) !== '{}') {
        updateCI(row.ci_id || row._id, data)
          .then(() => {
            this.$message.success(this.$t('saveSuccess'))
            $table.reloadRow(row, null)
            const _initialInstanceList = _.cloneDeep(this.initialInstanceList)
            _initialInstanceList[rowIndex] = {
              ..._initialInstanceList[rowIndex],
              ...data,
            }
            this.initialInstanceList = _initialInstanceList
            this.$nextTick(() => {
              this.refreshTable()
            })
          })
          .catch((err) => {
            console.log(err)
            $table.revertData(row)
          })
      }
      this.columns.forEach((col) => {
        if (col.is_password) {
          this.initialPasswordValue[col.field] = ''
          this.passwordValue[col.field] = ''
        }
      })
    },
    deleteCI(record) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadData({ parameter: {}, refreshType: 'refreshNumber' })
          })
        },
      })
    },
    sumbitFromCreateInstance({ ci_id }) {
      const first_ci_id = this.treeKeys[this.treeKeys.length - 1].split('%')[0]
      let ancestor_ids
      if (
        Object.keys(this.level2constraint).some(
          (le) => le < Object.keys(this.level2constraint).length && this.level2constraint[le] === '2'
        )
      ) {
        ancestor_ids = `${this.treeKeys
          .slice(0, this.treeKeys.length - 1)
          .map((item) => item.split('%')[0])
          .join(',')}`
      }
      addCIRelationView(first_ci_id, ci_id, { ancestor_ids }).then((res) => {
        setTimeout(() => {
          this.loadData({ parameter: {}, refreshType: 'refreshNumber' })
        }, 500)
      })
    },
    batchUpdateFromCreateInstance(values) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ci.batchUpdateConfirm'),
        onOk() {
          that.loading = true
          const payload = {}
          Object.keys(values).forEach((key) => {
            if (values[key] || values[key] === 0) {
              payload[key] = values[key]
            }
            // 字段值支持置空
            // 目前存在字段值不支持置空，由后端返回
            if (values[key] === undefined || values[key] === null) {
              payload[key] = null
            }
          })
          const promises = that.selectedRowKeys.map((row) => {
            return updateCI(row._id, payload).then((res) => {
              return 'ok'
            })
          })
          Promise.all(promises)
            .then((res) => {
              that.$message.success(that.$t('updateSuccess'))
              that.$refs.create.visible = false
            })
            .catch((e) => {
              console.log(e)
            })
            .finally(() => {
              that.loading = false
              setTimeout(() => {
                that.loadData({ parameter: {} })
              }, 800)
            })
        },
      })
    },
    async openBatchDownload() {
      this.$refs.batchDownload.open({
        preferenceAttrList: this.preferenceAttrList.filter((attr) => !attr?.is_reference),
        ciTypeName: this.viewName,
      })
    },
    batchDownload({ filename, type, checkedKeys }) {
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.preferenceAttrList.find((attr) => attr.name === key)
        if (_find && _find.value_type === '6') jsonAttrList.push(key)
      })
      const data = _.cloneDeep([
      ...this.$refs.xTable.getVxetableRef().getCheckboxReserveRecords(),
      ...this.$refs.xTable.getVxetableRef().getCheckboxRecords(true),
      ])
      this.$refs.xTable.getVxetableRef().exportData({
        filename,
        type,
        columnFilterMethod({ column }) {
          return checkedKeys.includes(column.property)
        },
        data: [
          ...data.map((item) => {
            jsonAttrList.forEach((jsonAttr) => (item[jsonAttr] = item[jsonAttr] ? JSON.stringify(item[jsonAttr]) : ''))
            return { ...item }
          }),
        ],
      })
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
    },
    batchDelete() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          that.loading = true
          const promises = that.selectedRowKeys.map((c) => {
            return deleteCI(c._id).then((res) => {
              return 'ok'
            })
          })
          Promise.all(promises)
            .then((res) => {
              that.$message.success(that.$t('deleteSuccess'))
            })
            .catch((e) => {
              console.log(e)
            })
            .finally(() => {
              that.loading = false
              that.selectedRowKeys = []
              that.$refs.xTable.getVxetableRef().clearCheckboxRow()
              that.$refs.xTable.getVxetableRef().clearCheckboxReserve()
              that.loadData({ parameter: {}, refreshType: 'refreshNumber' })
            })
        },
      })
    },
    relationViewRefreshNumber() {
      this.loadData({ parameter: {}, refreshType: 'refreshNumber' })
    },
    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize
      this.pageNo = 1
      this.loadData()
    },
    getQAndSort() {
      const fuzzySearch = this.$refs['search'].fuzzySearch || ''
      const expression = this.$refs['search'].expression || ''
      this.$refs.preferenceSearch.savePreference({ fuzzySearch, expression })
    },
    setParamsFromPreferenceSearch(item) {
      const { fuzzySearch, expression } = item.option
      this.$refs.search.fuzzySearch = fuzzySearch
      this.$refs.search.expression = expression
      this.pageNo = 1
      this.$nextTick(() => {
        this.loadData()
      })
    },
    setPreferenceSearchCurrent(id = null) {
      this.$nextTick(() => {
        this.$refs.preferenceSearch.currentPreferenceSearch = id
      })
    },
    copyExpression() {
      const expression = this.$refs['search'].expression || ''
      const fuzzySearch = this.$refs['search'].fuzzySearch

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      const text = `q=_type:${this.currentTypeId[0]}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.serviceTreecopyFailed'))
        })
    },
    async onRelationViewGrant({ department, user }, type) {
      const result = []
      if (this.showBatchLevel !== null && this.batchTreeKey && this.batchTreeKey.length) {
        for (let i = 0; i < this.batchTreeKey.length; i++) {
          await this.relationViewGrant({ department, user }, this.batchTreeKey[i], (_result) => {
            result.push(..._result)
          })
        }
        this.showBatchLevel = null
        this.batchTreeKey = []
      } else {
        await this.relationViewGrant({ department, user }, this.contextMenuKey, (_result) => {
          result.push(..._result)
        })
      }
      if (result.every((r) => r.status === 'fulfilled')) {
        this.$message.success(this.$t('operateSuccess'))
      }
    },
    async relationViewGrant({ department, user }, nodeKey, callback) {
      const needGrantNodes = nodeKey
        .split('@^@')
        .filter((item) => !!item)
        .reverse()

      const needGrantRids = [...department, ...user]
      const floor = Math.ceil(needGrantRids.length / 6)
      const result = []
      for (let i = 0; i < needGrantNodes.length; i++) {
        const grantNode = needGrantNodes[i]
        const _grantNode = grantNode.split('%')
        const ciId = _grantNode[0]
        const typeId = _grantNode[1]
        const uniqueValue = Object.entries(JSON.parse(_grantNode[2]))[0][1]
        const parent_path = needGrantNodes
          .slice(i + 1)
          .map((item) => {
            return Number(item.split('%')[0])
          })
          .reverse()
          .join(',')
        for (let j = 0; j < floor; j++) {
          const itemList = needGrantRids.slice(6 * j, 6 * j + 6)
          const promises = itemList.map((rid) =>
            grantCiType(typeId, rid, {
              id_filter: { [ciId]: { name: uniqueValue, parent_path } },
              is_recursive: Number(i > 0),
            })
          )
          const _result = await Promise.allSettled(promises)
          result.push(..._result)
        }
      }
      callback(result)
    },
    clickCheckbox(treeKey) {
      const _idx = this.batchTreeKey.findIndex((item) => item === treeKey)
      if (_idx > -1) {
        this.batchTreeKey.splice(_idx, 1)
      } else {
        this.batchTreeKey.push(treeKey)
      }
    },
    batchDeleteCIRelationFromTree() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: (h) => <div>{that.$t('confirmDelete')}</div>,
        async onOk() {
          for (let i = 0; i < that.batchTreeKey.length; i++) {
            const { splitTreeKey, _tempTree, ancestor_ids } = that.calculateParamsFromTreeKey(
              that.batchTreeKey[i],
              'delete'
            )
            const _tempTreeParent = splitTreeKey[splitTreeKey.length - 2].split('%')
            await deleteCIRelationView(_tempTreeParent[0], _tempTree[0], { ancestor_ids }).then((res) => {})
          }
          that.$message.success(that.$t('deleteSuccess'))
          that.showBatchLevel = null
          that.batchTreeKey = []
          setTimeout(() => {
            that.reload()
          }, 500)
        },
      })
    },
    async handleSingleRevoke({ users = [], roles = [] }, treeKey, callback) {
      const rids = [...users.map((item) => Number(item.split('-')[1])), ...roles]
      const treeKeyPath = treeKey.split('@^@').filter((item) => !!item)
      const _treeKey = treeKeyPath.pop(-1).split('%')
      const id_filter = {}
      const typeId = _treeKey[1]
      const ciId = _treeKey[0]
      const uniqueValue = Object.entries(JSON.parse(_treeKey[2]))[0][1]

      const parent_path = treeKeyPath
        .map((item) => {
          return Number(item.split('%')[0])
        })
        .join(',')
      id_filter[ciId] = { name: uniqueValue, parent_path }
      const floor = Math.ceil(rids.length / 6)
      const result = []
      for (let j = 0; j < floor; j++) {
        const itemList = rids.slice(6 * j, 6 * j + 6)
        const promises = itemList.map((rid) => revokeCiType(typeId, rid, { id_filter, perms: ['read'], parent_path }))
        const _result = await Promise.allSettled(promises)
        result.push(..._result)
      }
      callback(result)
    },
    async handleRevoke({ users = [], roles = [] }) {
      const result = []
      if (this.showBatchLevel !== null && this.batchTreeKey && this.batchTreeKey.length) {
        for (let i = 0; i < this.batchTreeKey.length; i++) {
          const treeKey = this.batchTreeKey[i]
          await this.handleSingleRevoke({ users, roles }, treeKey, (_result) => {
            result.push(..._result)
          })
        }
      } else {
        await this.handleSingleRevoke({ users, roles }, this.contextMenuKey, (_result) => {
          result.push(..._result)
        })
      }
      if (result.every((r) => r.status === 'fulfilled')) {
        this.$message.success(this.$t('operateSuccess'))
      }
      this.showBatchLevel = null
      this.batchTreeKey = []
    },
    findNode(node, target) {
      for (let i = 0; i < node.length; i++) {
        if (node[i].id === target) {
          return node[i]
        }
        if (node[i].children && node[i].children.length) {
          const found = this.findNode(node[i].children, target)
          if (found) {
            return found
          }
        }
      }
      return null
    },
    updateTreeData(ciId, value) {
      const _find = this.findNode(this.treeData, ciId)
      if (_find) {
        this.$set(_find, 'title', value)
      }
      this.refreshTable()
    },
    handleSearchFull(e) {
      const value = e.target.value
      this.treeKeys = []
      this.expandedKeys = []
      if (!value) {
        this.reload()
        return
      }
      if (this.isFullSearch) {
        this.calcFilterFullTreeData()
        return
      }
      searchCIRelationFull({
        ...this.loadRootStatisticsParams,
        type_ids: this.topo_flatten.join(','),
      }).then((res) => {
        this.isFullSearch = true
        this.fullTreeData = this.formatTreeData(res)
        this.calcFilterFullTreeData()
      })
    },
    calcFilterFullTreeData() {
      const _expandedKeys = []
      const predicateCiIds = []
      const filterTree = (node, predicate) => {
        if (predicate(node)) {
          predicateCiIds.push(node.id)
          return true
        }
        if (node.children) {
          node.children = node.children.filter((child) => {
            if (
              predicateCiIds.some(
                (id) =>
                  child.key
                    .split('@^@')
                    .map((item) => Number(item.split('%')[0]))
                    .indexOf(id) > -1
              )
            ) {
              return true
            }
            return filterTree(child, predicate)
          })
          if (
            node.children.length &&
            !predicateCiIds.some(
              (id) =>
                node.key
                  .split('@^@')
                  .map((item) => Number(item.split('%')[0]))
                  .indexOf(id) > -1
            )
          ) {
            _expandedKeys.push(node.key)
          }
          return node.children.length > 0
        }
        return false
      }
      const predicate = (node) =>
        String(node.title)
          .toLowerCase()
          .includes(this.fullSearchValue.toLowerCase())
      const _fullTreeData = _.cloneDeep(this.fullTreeData)
      this.filterFullTreeData = _fullTreeData.filter((item) => filterTree(item, predicate))
      if (this.filterFullTreeData && this.filterFullTreeData.length) {
        this.onNodeClick(this.filterFullTreeData[0].key, () => {
          this.expandedKeys = _expandedKeys
        })
      } else {
        this.treeKeys = []
        this.instanceList = []
      }
    },
    formatTreeData(array, parentKey = '') {
      array.forEach((item) => {
        const showName = this.relationViews.id2type[item.type_id]?.show_name ?? null
        const uniqueName = this.relationViews.id2type[item.type_id]?.unique_name ?? null
        const keyList = parentKey.split('@^@').filter((item) => !!item)
        keyList.push(item.id + '%' + item.type_id + '%' + `{"${uniqueName}":"${item.uniqueValue}"}`)
        const key = keyList.join('@^@')
        item.key = key
        item.showName = showName
        if (!item.isLeaf && item.children && item.children.length) {
          item.children = this.formatTreeData(item.children, key)
        }
      })
      return array
    },

    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$refs.detail.create(id, activeTabKey, ciDetailRelationKey)
    },

    clickRelationViewMenu(id) {
      if (id) {
        localStorage.setItem(relationViewKeyStorage, id)
        this.reload()
      }
    }
  },
}
</script>

<style lang="less">
@import '../index.less';

.relation-views-wrapper {
  width: 100%;
  .relation-views-left {
    width: 100%;
    float: left;
    position: relative;
    overflow: hidden;
    padding: 12px 8px;
    background-color: #f7f8fa;
    border-right: 1px solid #e8eaed;
    &:hover {
      overflow: auto;
    }
    .relation-views-left-header {
      display: flex;
      align-items: center;
      max-width: 100%;
      overflow: hidden;
      padding-bottom: 12px;
      border-bottom: @border-color-base;
      margin-bottom: 14px;

      &-icon {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 22px;
        background-color: @primary-color;

        i {
          font-size: 12px;
          color: #FFFFFF;
        }
      }

      &-name {
        margin-left: 9px;

        span {
          font-size: 17px;
          font-weight: 700;
          color: @primary-color;
        }
      }

      &-down {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 1px;
        background-color: @primary-color_3;
        cursor: pointer;
        margin-left: auto;

        i {
          font-size: 18px;
          color: @primary-color;
        }

        &:hover {
          background-color: @primary-color_4;
        }
      }
    }
    .ant-tree li {
      padding: 2px 0;
    }
    .ant-tree-switcher {
      display: none;
    }
    .ant-tree-node-content-wrapper {
      width: 100%;
      padding: 6px 8px;
      display: inline-block;
      height: 100%;
      border-radius: 6px;
      transition: all 0.2s ease;

      &:hover {
        background-color: @primary-color_7;
        transform: translateX(2px);
      }

      &.ant-tree-node-selected {
        background-color: @primary-color_6;

        .ant-tree-title {
          color: @primary-color;
          font-weight: 600;
        }
      }
      .ant-tree-title {
        display: inline-block;
        width: 100%;
        padding: 0 4px;
      }
    }
    .relation-views-left-input {
      margin-bottom: 12px;

      .ant-input {
        background-color: #fff;
        border-radius: 6px;
        border: 1px solid #e8eaed;
        transition: all 0.2s ease;

        &:hover {
          border-color: #c3cdd7;
        }

        &:focus {
          border-color: @primary-color;
          box-shadow: 0 0 0 2px fade(@primary-color, 10%);
        }
      }

      .ant-input-prefix {
        color: @text-color_3;
      }
    }
  }
  .relation-views-right {
    width: 100%;
    overflow: auto;
    background-color: #fff;
    padding: 20px;
    border-radius: @border-radius-box;

    .ant-tabs-tab {
      padding-top: 0px;
    }
  }
}

.relation-views-left-header-dropdown {
  background-color: #FFFFFF;

  .relation-views-left-header-menu {
    box-shadow: none;
    max-height: 400px;
    min-height: 150px;
    overflow-y: auto;
    overflow-x: hidden;

    &-item {
      width: 150px;
      overflow: hidden;
      display: flex !important;
      align-items: center;

      &:hover {
        .relation-views-left-header-menu-grant {
          display: inline-block;
        }
      }
    }

    &-name {
      margin-right: 8px;
    }

    &-grant {
      margin-left: 8px;
      flex-shrink: 0;
      font-size: 12px;
      display: none;
      margin-left: auto;
      color: @text-color_4;

      &:hover {
        color: @primary-color;
      }
    }
  }
}

.relation-views-text-scroll {
  max-width: 100%;
  overflow: hidden;

  & > span {
    display: block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
  }

  &:hover {
    & > span {
      overflow: visible;
      animation: scroll-left 3s linear infinite;
    }
  }

  @keyframes scroll-left {
    0% {
      transform: translateX(0);
    }
    100% {
      transform: translateX(-100%);
    }
  }
}
</style>
