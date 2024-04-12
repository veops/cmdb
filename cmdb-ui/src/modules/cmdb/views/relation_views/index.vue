<template>
  <div :style="{ marginBottom: '-24px', overflow: 'hidden' }">
    <div v-if="relationViews.name2id && relationViews.name2id.length" class="relation-views-wrapper">
      <SplitPane
        :min="200"
        :max="500"
        :paneLengthPixel.sync="paneLengthPixel"
        :appName="`cmdb-relation-views-${viewId}`"
        :triggerLength="18"
      >
        <template #one>
          <div class="relation-views-left" :style="{ height: `${windowHeight - 115}px` }">
            <div class="relation-views-left-header" :title="$route.meta.name">{{ $route.meta.name }}</div>
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
              :selectedKeys="selectedKeys"
              :loadData="onLoadData"
              :treeData="treeData"
              draggable
              @dragenter="onDragEnter"
              @drop="onDrop"
              :expandedKeys="expandedKeys"
            >
              <template #title="{ key: treeKey, title,number, isLeaf }">
                <ContextMenu
                  :title="title"
                  :number="number"
                  :treeKey="treeKey"
                  :levels="levels"
                  :isLeaf="isLeaf"
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
            <vxe-table
              :id="`cmdb-relation-${viewId}-${currentTypeId}`"
              border
              keep-source
              show-overflow
              resizable
              ref="xTable"
              size="small"
              row-id="_id"
              :height="tableHeight"
              :loading="loading"
              show-header-overflow
              highlight-hover-row
              :data="instanceList"
              @checkbox-change="onSelectChange"
              @checkbox-all="onSelectChange"
              :checkbox-config="{ reserve: true, trigger: 'cell' }"
              @edit-closed="handleEditClose"
              @edit-actived="handleEditActived"
              :edit-config="{ trigger: 'dblclick', mode: 'row', showIcon: false }"
              :sort-config="{ remote: true, trigger: 'cell' }"
              @sort-change="handleSortCol"
              :row-key="true"
              :column-key="true"
              :cell-style="getCellStyle"
              :scroll-y="{ enabled: true, gt: 20 }"
              :scroll-x="{ enabled: true, gt: 0 }"
              class="ops-unstripe-table"
              :custom-config="{ storage: true }"
            >
              <vxe-column v-if="isLeaf" align="center" type="checkbox" width="50" fixed="left"></vxe-column>
              <vxe-table-column
                v-for="(col, index) in columns"
                :key="`${col.field}_${index}`"
                :title="col.title"
                :field="col.field"
                :width="col.width"
                :sortable="col.sortable"
                :edit-render="getColumnsEditRender(col)"
                :cell-type="col.value_type === '2' ? 'string' : 'auto'"
                :fixed="col.is_fixed ? 'left' : ''"
              >
                <template #header>
                  <span class="vxe-handle">
                    <OpsMoveIcon
                      style="width: 17px; height: 17px; display: none; position: absolute; left: -3px; top: 12px"
                    />
                    {{ col.title }}</span
                  >
                </template>
                <template v-if="col.is_choice || col.is_password" #edit="{ row }">
                  <vxe-input v-if="col.is_password" v-model="passwordValue[col.field]" />
                  <a-select
                    :getPopupContainer="(trigger) => trigger.parentElement"
                    :style="{ width: '100%', height: '32px' }"
                    v-model="row[col.field]"
                    :placeholder="$t('placeholder2')"
                    v-if="col.is_choice"
                    :showArrow="false"
                    :mode="col.is_list ? 'multiple' : 'default'"
                    class="ci-table-edit-select"
                    allowClear
                  >
                    <a-select-option
                      :value="choice[0]"
                      :key="'edit_' + col.field + idx"
                      v-for="(choice, idx) in col.filters"
                    >
                      <span
                        :style="{ ...(choice[1] ? choice[1].style : {}), display: 'inline-flex', alignItems: 'center' }"
                      >
                        <template v-if="choice[1] && choice[1].icon && choice[1].icon.name">
                          <img
                            v-if="choice[1].icon.id && choice[1].icon.url"
                            :src="`/api/common-setting/v1/file/${choice[1].icon.url}`"
                            :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
                          />
                          <ops-icon
                            v-else
                            :style="{ color: choice[1].icon.color, marginRight: '5px' }"
                            :type="choice[1].icon.name"
                          />
                        </template>
                        {{ choice[0] }}
                      </span>
                    </a-select-option>
                  </a-select>
                </template>
                <template
                  v-if="col.value_type === '6' || col.is_link || col.is_password || col.is_choice"
                  #default="{row}"
                >
                  <span v-if="col.value_type === '6' && row[col.field]">{{ row[col.field] }}</span>
                  <a
                    v-else-if="col.is_link && row[col.field]"
                    :href="
                      row[col.field].startsWith('http') || row[col.field].startsWith('https')
                        ? `${row[col.field]}`
                        : `http://${row[col.field]}`
                    "
                    target="_blank"
                  >{{ row[col.field] }}</a
                  >
                  <PasswordField
                    v-else-if="col.is_password && row[col.field]"
                    :ci_id="row._id"
                    :attr_id="col.attr_id"
                  ></PasswordField>
                  <template v-else-if="col.is_choice">
                    <template v-if="col.is_list">
                      <span
                        v-for="value in row[col.field]"
                        :key="value"
                        :style="{
                          borderRadius: '4px',
                          padding: '1px 5px',
                          margin: '2px',
                          ...getChoiceValueStyle(col, value),
                          display: 'inline-flex',
                          alignItems: 'center',
                        }"
                      >
                        <img
                          v-if="getChoiceValueIcon(col, value).id && getChoiceValueIcon(col, value).url"
                          :src="`/api/common-setting/v1/file/${getChoiceValueIcon(col, value).url}`"
                          :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
                        />
                        <ops-icon
                          v-else
                          :style="{ color: getChoiceValueIcon(col, value).color, marginRight: '5px' }"
                          :type="getChoiceValueIcon(col, value).name"
                        />{{ value }}</span
                      >
                    </template>
                    <span
                      v-else-if="row[col.field]"
                      :style="{
                        borderRadius: '4px',
                        padding: '1px 5px',
                        margin: '2px 0',
                        ...getChoiceValueStyle(col, row[col.field]),
                        display: 'inline-flex',
                        alignItems: 'center',
                      }"
                    >
                      <img
                        v-if="getChoiceValueIcon(col, row[col.field]).id && getChoiceValueIcon(col, row[col.field]).url"
                        :src="`/api/common-setting/v1/file/${getChoiceValueIcon(col, row[col.field]).url}`"
                        :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
                      />
                      <ops-icon
                        v-else
                        :style="{ color: getChoiceValueIcon(col, row[col.field]).color, marginRight: '5px' }"
                        :type="getChoiceValueIcon(col, row[col.field]).name"
                      />{{ row[col.field] }}</span
                    >
                  </template>
                </template>
              </vxe-table-column>
              <vxe-column align="left" field="operate" fixed="right" width="80">
                <template #header>
                  <span>{{ $t('operation') }}</span>
                </template>
                <template #default="{ row }">
                  <a-space>
                    <a @click="$refs.detail.create(row.ci_id || row._id)">
                      <a-icon type="unordered-list" />
                    </a>
                    <a-tooltip :title="$t('cmdb.ci.addRelation')">
                      <a @click="$refs.detail.create(row.ci_id || row._id, 'tab_2', '2')">
                        <a-icon type="retweet" />
                      </a>
                    </a-tooltip>
                    <template v-if="isLeaf">
                      <a-tooltip :title="$t('cmdb.ciType.deleteInstance')">
                        <a @click="deleteCI(row)" :style="{ color: 'red' }">
                          <a-icon type="delete" />
                        </a>
                      </a-tooltip>
                    </template>
                  </a-space>
                </template>
              </vxe-column>
              <template #empty>
                <div v-if="loading" style="height: 200px; line-height: 200px">{{ $t('loading') }}</div>
                <div v-else>
                  <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
                  <div>{{ $t('noData') }}</div>
                </div>
              </template>
            </vxe-table>
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
                :style="{ alignSelf: 'flex-end', marginRight: '12px' }"
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
      :message="$t('cmdb.serviceTreealert1')"
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
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
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
import JsonEditor from '../../components/JsonEditor/jsonEditor.vue'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PasswordField from '../../components/passwordField/index.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import CMDBGrant from '../../components/cmdbGrant'
import GrantModal from '../../components/cmdbGrant/grantModal.vue'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { getAttrPassword } from '../../api/CITypeAttr'
import ReadPermissionsModal from './modules/ReadPermissionsModal.vue'
import RevokeModal from '../../components/cmdbGrant/revokeModal.vue'

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
    JsonEditor,
    BatchDownload,
    PasswordField,
    PreferenceSearch,
    OpsMoveIcon,
    ReadPermissionsModal,
    RevokeModal,
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
      if (this.treeKeys.length <= 1) {
        return this.treeKeys.map((item) => `@^@${item}`)
      }
      return [this.treeKeys.join('@^@')]
    },
    isLeaf() {
      return this.treeKeys.length === this.levels.length
    },
    isShowBatchIcon() {
      return !!this.selectedRowKeys.length
    },
    topo_flatten() {
      return this.relationViews?.views[this.$route.meta.name]?.topo_flatten ?? []
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
    '$route.path': function(newPath, oldPath) {
      this.viewId = this.$route.params.viewId
      this.reload()
    },
    pageNo: function(newPage, oldPage) {
      this.loadData({ pageNo: newPage }, undefined, this.sortByTable)
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
      const xTable = this.$refs.xTable
      if (xTable) {
        xTable.clearCheckboxRow()
        xTable.clearCheckboxReserve()
        xTable.clearSort()
      }
      this.loadData()
    },

    async loadData(parameter, refreshType = undefined, sortByTable = undefined) {
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
        // exp = exp.replace(/(\:)/g, '$1*')
        // exp = exp.replace(/(\,)/g, '*$1')
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
        // await this.judgeCITypes(q)
        if (!refreshType) {
          await this.loadRoot()
        }

        // const fuzzySearch = (this.$refs['search'] || {}).fuzzySearch || ''
        // if (fuzzySearch) {
        //   q = `q=_type:${this.currentTypeId[0]},*${fuzzySearch}*,` + q
        // } else {
        //   q = `q=_type:${this.currentTypeId[0]},` + q
        // }
        // if (this.currentTypeId[0] && this.treeData && this.treeData.length) {
        //   // default select first node
        //   this.onNodeClick(this.treeData[0].key)
        //   const res = await searchCI2(q)
        //   const root_id = this.treeData.map((item) => item.id).join(',')
        //   q += `&root_id=${root_id}`

        //   this.pageNo = res.page
        //   this.numfound = res.numfound
        //   res.result.forEach((item, index) => (item.key = item._id))
        //   const jsonAttrList = this.preferenceAttrList.filter((attr) => attr.value_type === '6')
        //   console.log(jsonAttrList)
        //   this.instanceList = res['result'].map((item) => {
        //     jsonAttrList.forEach(
        //       (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
        //     )
        //     return { ..._.cloneDeep(item) }
        //   })
        //   this.initialInstanceList = _.cloneDeep(this.instanceList)
        //   this.calcColumns()
        // }
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
        if (!refreshType) {
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
          const promises = this.treeKeys.map((key, index) => {
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
      this.$refs.xTable.clearCheckboxRow()
      this.$refs.xTable.clearCheckboxReserve()
      this.$refs.search.reset()
      this.selectedRowKeys = []
      this.currentTypeId = [typeId]
      this.loadColumns()
      // this.$nextTick(() => {
      //   this.refreshTable()
      // })
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
      // const showTypeIds = []
      // let _showTypes = []
      // let _showTypeIds = []

      // if (this.treeKeys.length) {
      //   const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('%')[1])

      //   _showTypes = this.node2ShowTypes[typeId + '']
      //   _showTypes.forEach((item) => {
      //     _showTypeIds.push(item.id)
      //   })
      // } else {
      //   _showTypeIds = JSON.parse(JSON.stringify(this.origShowTypeIds))
      //   _showTypes = JSON.parse(JSON.stringify(this.origShowTypes))
      // }
      // const promises = _showTypeIds.map((typeId) => {
      //   let _q = (`q=_type:${typeId},` + q).replace(/count=\d*/, 'count=1')
      //   if (Object.values(this.level2constraint).includes('2')) {
      //     _q = _q + `&has_m2m=1`
      //   }
      //   if (this.root_parent_path) {
      //     _q = _q + `&root_parent_path=${this.root_parent_path}`
      //   }
      //   // if (this.treeKeys.length === 0) {
      //   //   return searchCI2(_q).then((res) => {
      //   //     if (res.numfound !== 0) {
      //   //       showTypeIds.push(typeId)
      //   //     }
      //   //   })
      //   // } else {
      //   _q = _q + `&descendant_ids=${this.descendant_ids}`
      //   return searchCIRelation(_q).then((res) => {
      //     if (res.numfound !== 0) {
      //       showTypeIds.push(typeId)
      //     }
      //   })
      //   // }
      // })
      // await Promise.all(promises).then(async () => {
      //   if (showTypeIds.length && showTypeIds.sort().join(',') !== this.showTypeIds.sort().join(',')) {
      //     const showTypes = []
      //     _showTypes.forEach((item) => {
      //       if (showTypeIds.includes(item.id)) {
      //         showTypes.push(item)
      //       }
      //     })
      //     console.log(showTypes)
      //     this.showTypes = showTypes
      //     this.showTypeIds = showTypeIds
      //     if (
      //       !this.currentTypeId.length ||
      //       (this.currentTypeId.length && !this.showTypeIds.includes(this.currentTypeId[0]))
      //     ) {
      //       this.currentTypeId = [this.showTypeIds[0]]
      //       await this.loadColumns()
      //     }
      //   }
      // })
    },

    async loadRoot() {
      await searchCI2(`q=_type:(${this.levels[0].join(';')})&count=10000&use_id_filter=1`).then(async (res) => {
        const facet = []
        const ciIds = []
        res.result.forEach((item) => {
          facet.push([item[item.unique], 0, item._id, item._type, item.unique])
          ciIds.push(item._id)
        })
        const promises = this.leaf.map((leafId) => {
          let level = 0
          this.levels.forEach((item, idx) => {
            if (item.includes(leafId)) {
              level = idx + 1
            }
          })
          return statisticsCIRelation({
            root_ids: ciIds.join(','),
            level: level,
            type_ids: this.leaf2showTypes[this.leaf[0]].join(','),
            has_m2m: Number(Object.values(this.level2constraint).includes('2')),
            descendant_ids: this.descendant_ids_for_statistics,
          }).then((num) => {
            facet.forEach((item, idx) => {
              item[1] += num[ciIds[idx] + '']
            })
          })
        })
        await Promise.all(promises)
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
            facet.push([item[item.unique], 0, item._id, item._type, item.unique])
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
                  item[1] += num[ciIds[idx] + '']
                })
              })
            }
          })
          await Promise.all(promises)
          this.wrapTreeData(facet)
        })
      }
    },

    onNodeClick(keys) {
      this.triggerSelect = true
      if (keys) {
        const _tempKeys = keys.split('@^@').filter((item) => item !== '')
        if (_tempKeys.length === this.levels.length) {
          this.$refs.xTable.clearCheckboxRow()
          this.$refs.xTable.clearCheckboxReserve()
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
    },
    wrapTreeData(facet) {
      if (this.triggerSelect) {
        return
      }
      const treeData = []
      facet.forEach((item) => {
        treeData.push({
          title: item[0],
          number: item[1],
          key: this.treeKeys.join('@^@') + '@^@' + item[2] + '%' + item[3] + '%' + `{"${item[4]}":"${item[0]}"}`,
          isLeaf: this.leaf.includes(item[3]),
          id: item[2],
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
        // this.refreshTable()
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
          this.viewId =
            parseInt(this.$route.path.split('/')[this.$route.path.split('/').length - 1]) ||
            this.relationViews.name2id[0][1]
          this.relationViews.name2id.forEach((item) => {
            if (item[1] === this.viewId) {
              this.viewName = item[0]
            }
          })
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
          this.refreshTable()
        }
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
        this.$refs.xTable.refreshColumn()
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
            content: (h) => <div>{that.$t('confirmDelete2', { name: Object.values(firstCIObj)[0] })}</div>,
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
          this.$refs.addTableModal.openModal(firstCIObj, firstCIId, childTypeId, 'children', ancestor_ids)
        }
      }
    },
    onSelectChange({ records, reserves }) {
      this.selectedRowKeys = [...records, ...reserves]
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
            that.$refs.xTable.clearCheckboxRow()
            that.$refs.xTable.clearCheckboxReserve()
            that.selectedRowKeys = []
            that.loadData({}, 'refreshNumber')
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
        // const targetObj = JSON.parse(_splitTargetKey[_splitTargetKey.length - 1].split('%')[2])
        const targetId = _splitTargetKey[_splitTargetKey.length - 1].split('%')[0]
        // TODO 拖拽这里不造咋弄 等等再说吧
        batchUpdateCIRelationChildren([dragId], [targetId]).then((res) => {
          this.reload()
        })
      }
    },
    handlePerm() {
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'RelationView',
        perm: 'grant',
        resource_name: this.$route.meta.title,
      }).then((res) => {
        if (res.result) {
          searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
            this.resource_type = { groups: res.groups, id2perms: res.id2perms }
            this.$nextTick(() => {
              this.$refs.cmdbGrant.open({ name: this.$route.meta.title, cmdbGrantType: 'relation_view' })
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
          this.loadData({}, undefined, sortByTable)
        } else {
          this.pageNo = 1
        }
      })
    },
    columnDrop() {
      this.$nextTick(() => {
        const xTable = this.$refs.xTable
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
    getChoiceValueStyle(col, colValue) {
      const _find = col.filters.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.style || {}
      }
      return {}
    },
    getChoiceValueIcon(col, colValue) {
      const _find = col.filters.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.icon || {}
      }
      return {}
    },
    getCellStyle({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      const { property } = column
      const _find = this.preferenceAttrList.find((attr) => attr.name === property)
      if (
        _find &&
        _find.option &&
        _find.option.fontOptions &&
        row[`${property}`] !== undefined &&
        row[`${property}`] !== null
      ) {
        return { ..._find.option.fontOptions }
      }
    },
    refreshAfterEditAttrs() {
      this.loadColumns()
    },
    getColumnsEditRender(col) {
      const _editRender = {
        ...col.editRender,
      }
      if (col.value_type === '6') {
        _editRender.events = { focus: this.handleFocusJson }
      }
      return _editRender
    },
    handleEditActived() {
      const passwordCol = this.columns.filter((col) => col.is_password)
      this.$nextTick(() => {
        const editRecord = this.$refs.xTable.getEditRecord()
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
            await this.$refs.xTable.clearEdit()
            this.isContinueCloseEdit = true
            this.$nextTick(() => {
              this.$refs.xTable.setEditCell(row, column.field)
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
      const $table = this.$refs['xTable']
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
            that.loadData({}, 'refreshNumber')
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
          this.loadData({}, 'refreshNumber')
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
                that.loadData({})
              }, 800)
            })
        },
      })
    },
    async openBatchDownload() {
      this.$refs.batchDownload.open({
        preferenceAttrList: this.preferenceAttrList,
        ciTypeName: this.$route.meta.name,
      })
    },
    batchDownload({ filename, type, checkedKeys }) {
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.preferenceAttrList.find((attr) => attr.name === key)
        if (_find && _find.value_type === '6') jsonAttrList.push(key)
      })
      const data = _.cloneDeep([
        ...this.$refs.xTable.getCheckboxReserveRecords(),
        ...this.$refs.xTable.getCheckboxRecords(true),
      ])
      this.$refs.xTable.exportData({
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
      this.$refs.xTable.clearCheckboxRow()
      this.$refs.xTable.clearCheckboxReserve()
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
              that.$refs.xTable.clearCheckboxRow()
              that.$refs.xTable.clearCheckboxReserve()
              that.loadData({}, 'refreshNumber')
            })
        },
      })
    },
    handleFocusJson({ column, row }) {
      this.$refs.jsonEditor.open(column, row)
    },
    jsonEditorOk(row, column, jsonData) {
      // 后端写数据有快慢，不拉接口直接修改table的数据
      // this.reloadData()
      this.instanceList.forEach((item) => {
        if (item._id === row._id) {
          item[column.property] = JSON.stringify(jsonData)
        }
      })
      this.$refs.xTable.refreshColumn()
    },
    relationViewRefreshNumber() {
      this.loadData({}, 'refreshNumber')
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
      this.$refs.preferenceSearch.currentPreferenceSearch = id
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
            const { splitTreeKey, firstCIObj, firstCIId, _tempTree, ancestor_ids } = that.calculateParamsFromTreeKey(
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
          for (let i = 0; i < node[i].children.length; i++) {
            const found = this.findNode(node[i].children, target)
            if (found) {
              return found
            }
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
    padding: 0;
    &:hover {
      overflow: auto;
    }
    .relation-views-left-header {
      border-left: 4px solid @primary-color;
      height: 32px;
      line-height: 32px;
      padding-left: 12px;
      margin-bottom: 12px;
      color: @text-color_1;
      font-weight: bold;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: default;
    }
    .ant-tree li {
      padding: 2px 0;
    }
    .ant-tree-switcher {
      display: none;
    }
    .ant-tree-node-content-wrapper {
      width: 100%;
      padding: 4px 0;
      display: inline-block;
      height: 100%;
      .ant-tree-title {
        display: inline-block;
        width: 100%;
        padding: 0 6px;
      }
    }
  }
  .relation-views-right {
    width: 100%;
    overflow: auto;
    background-color: #fff;
    padding: 20px;
    border-radius: @border-radius-box;
  }
}
</style>
