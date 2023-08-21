<template>
  <div :style="{ marginBottom: '-24px', overflow: 'hidden' }">
    <div v-if="relationViews.name2id && relationViews.name2id.length" class="relation-views-wrapper">
      <div class="cmdb-views-header">
        <span class="cmdb-views-header-title">{{ $route.meta.name }}</span>
        <a-button size="small" icon="user-add" type="primary" ghost @click="handlePerm">授权</a-button>
      </div>
      <SplitPane
        :min="200"
        :max="500"
        :paneLengthPixel.sync="paneLengthPixel"
        appName="cmdb-relation-views"
        triggerColor="#F0F5FF"
        :triggerLength="18"
      >
        <template #one>
          <div class="relation-views-left" :style="{ height: `${windowHeight - 115}px` }">
            <a-tree
              :selectedKeys="selectedKeys"
              :loadData="onLoadData"
              :treeData="treeData"
              draggable
              @dragenter="onDragEnter"
              @drop="onDrop"
              :expandedKeys="expandedKeys"
            >
              <a-icon slot="switcherIcon" type="down" />
              <template #title="{ key: treeKey, title, isLeaf }">
                <ContextMenu
                  :title="title"
                  :treeKey="treeKey"
                  :levels="levels"
                  :isLeaf="isLeaf"
                  :currentViews="relationViews.views[viewName]"
                  :id2type="relationViews.id2type"
                  @onContextMenuClick="onContextMenuClick"
                  @onNodeClick="onNodeClick"
                  :ciTypes="ciTypes"
                />
              </template>
            </a-tree>
          </div>
        </template>
        <template #two>
          <div id="relation-views-right" class="relation-views-right" :style="{ height: `${windowHeight - 115}px` }">
            <a-tabs :activeKey="String(currentTypeId[0])" type="card" @change="changeCIType" class="ops-tab">
              <a-tab-pane v-for="item in showTypes" :key="`${item.id}`" :tab="item.alias || item.name"> </a-tab-pane>
            </a-tabs>
            <SearchForm
              ref="search"
              @refresh="refreshTable"
              :preferenceAttrList="preferenceAttrList"
              :isShowExpression="true"
              :typeId="Number(currentTypeId[0])"
              @copyExpression="copyExpression"
              type="relationView"
              :style="{ padding: '0 12px', marginTop: '16px' }"
            />
            <div class="relation-views-right-bar">
              <a-space>
                <a-button
                  v-if="isLeaf"
                  type="primary"
                  size="small"
                  @click="$refs.create.handleOpen(true, 'create')"
                >新建</a-button
                >

                <div class="ops-list-batch-action" v-if="isLeaf && isShowBatchIcon">
                  <template v-if="selectedRowKeys.length">
                    <span @click="$refs.create.handleOpen(true, 'update')">修改</span>
                    <a-divider type="vertical" />
                    <span @click="openBatchDownload">下载</span>
                    <a-divider type="vertical" />
                    <span @click="batchDelete">删除实例</span>
                    <a-divider type="vertical" />
                    <span @click="batchDeleteCIRelation">删除关系</span>
                    <span>选取：{{ selectedRowKeys.length }} 项</span>
                  </template>
                </div>
                <PreferenceSearch
                  ref="preferenceSearch"
                  @getQAndSort="getQAndSort"
                  @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
                />
              </a-space>
            </div>
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
                <template v-if="col.is_choice" #edit="{ row }">
                  <a-select
                    :getPopupContainer="(trigger) => trigger.parentElement"
                    :style="{ width: '100%', height: '32px' }"
                    v-model="row[col.field]"
                    placeholder="请选择"
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
                      <span :style="choice[1] ? choice[1].style || {} : {}">
                        <ops-icon
                          :style="{ color: choice[1].icon.color }"
                          v-if="choice[1] && choice[1].icon && choice[1].icon.name"
                          :type="choice[1].icon.name"
                        />
                        {{ choice[0] }}
                      </span>
                    </a-select-option>
                  </a-select>
                </template>
                <template
                  v-if="col.value_type === '6' || col.is_link || col.is_password || col.is_choice"
                  #default="{ row }"
                >
                  <span v-if="col.value_type === '6' && row[col.field]">{{ row[col.field] }}</span>
                  <a v-else-if="col.is_link" :href="`${row[col.field]}`" target="_blank">{{ row[col.field] }}</a>
                  <PasswordField
                    v-else-if="col.is_password && row[col.field]"
                    :password="row[col.field]"
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
                        }"
                      ><ops-icon
                        :style="{ color: getChoiceValueIcon(col, value).color }"
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
                      }"
                    >
                      <ops-icon
                        :style="{ color: getChoiceValueIcon(col, row[col.field]).color }"
                        :type="getChoiceValueIcon(col, row[col.field]).name"
                      />{{ row[col.field] }}</span
                    >
                  </template>
                </template>
              </vxe-table-column>
              <vxe-column align="left" field="operate" fixed="right" width="80">
                <template #header>
                  <span>操作</span>
                  <EditAttrsPopover
                    :typeId="Number(currentTypeId[0])"
                    class="operation-icon"
                    @refresh="refreshAfterEditAttrs"
                  />
                </template>
                <template #default="{ row }">
                  <a @click="$refs.detail.create(row.ci_id || row._id)">
                    <a-icon type="unordered-list" />
                  </a>
                  <template v-if="isLeaf">
                    <a-divider type="vertical" />
                    <a-tooltip title="删除实例">
                      <a @click="deleteCI(row)" :style="{ color: 'red' }">
                        <a-icon type="delete" />
                      </a>
                    </a-tooltip>
                  </template>
                </template>
              </vxe-column>
              <template #empty>
                <div v-if="loading" style="height: 200px; line-height: 200px">加载中...</div>
                <div v-else>
                  <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
                  <div>暂无数据</div>
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
                :show-total="(total, range) => `当前${range[0]}-${range[1]} 共 ${total}条记录`"
                :style="{ alignSelf: 'flex-end', marginRight: '12px' }"
              >
                <template slot="buildOptionText" slot-scope="props">
                  <span v-if="props.value !== '100000'">{{ props.value }}条/页</span>
                  <span v-if="props.value === '100000'">全部</span>
                </template>
              </a-pagination>
            </div>
          </div>
        </template>
      </SplitPane>
    </div>
    <a-alert
      message="管理员 还未配置业务关系, 或者你无权限访问!"
      banner
      v-else-if="relationViews.name2id && !relationViews.name2id.length"
    ></a-alert>
    <AddTableModal ref="addTableModal" @reload="reload" />
    <CMDBGrant ref="cmdbGrant" resourceType="RelationView" app_id="cmdb" />

    <ci-detail ref="detail" :typeId="Number(currentTypeId[0])" />
    <create-instance-form
      ref="create"
      :typeIdFromRelation="Number(currentTypeId[0])"
      @reload="sumbitFromCreateInstance"
      @submit="batchUpdateFromCreateInstance"
    />
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
    <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
  </div>
</template>

<script>
/* eslint-disable no-useless-escape */
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
import { getCITypes } from '../../api/CIType'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import SplitPane from '@/components/SplitPane'
import EditAttrsPopover from '../ci/modules/editAttrsPopover.vue'
import CiDetail from '../ci/modules/CiDetail'
import CreateInstanceForm from '../ci/modules/CreateInstanceForm'
import JsonEditor from '../../components/JsonEditor/jsonEditor.vue'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PasswordField from '../../components/passwordField/index.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import CMDBGrant from '../../components/cmdbGrant'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'

export default {
  name: 'RelationViews',
  components: {
    SearchForm,
    AddTableModal,
    ContextMenu,
    CMDBGrant,
    SplitPane,
    ElTree: Tree,
    EditAttrsPopover,
    CiDetail,
    CreateInstanceForm,
    JsonEditor,
    BatchDownload,
    PasswordField,
    PreferenceSearch,
    OpsMoveIcon,
  },
  data() {
    return {
      treeData: [],
      triggerSelect: false,
      treeNode: null,
      ciTypes: [],
      relationViews: {},
      levels: [],
      showTypeIds: [],
      origShowTypeIds: [],
      showTypes: [],
      origShowTypes: [],
      leaf2showTypes: {},
      node2ShowTypes: {},
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
    }
  },

  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      return this.windowHeight - 295
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
    '$route.path': function (newPath, oldPath) {
      this.viewId = this.$route.params.viewId
      this.reload()
    },
    pageNo: function (newPage, oldPage) {
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
      getCITypes().then((res) => {
        this.ciTypes = res.ci_types
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
        if (!refreshType) {
          this.loadRoot()
        }

        await this.judgeCITypes(q)
        const fuzzySearch = (this.$refs['search'] || {}).fuzzySearch || ''
        if (fuzzySearch) {
          q = `q=_type:${this.currentTypeId[0]},*${fuzzySearch}*,` + q
        } else {
          q = `q=_type:${this.currentTypeId[0]},` + q
        }
        const res = await searchCI2(q)
        this.pageNo = res.page
        this.numfound = res.numfound
        res.result.forEach((item, index) => (item.key = item._id))
        const jsonAttrList = this.preferenceAttrList.filter((attr) => attr.value_type === '6')
        console.log(jsonAttrList)
        this.instanceList = res['result'].map((item) => {
          jsonAttrList.forEach(
            (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
          )
          return { ..._.cloneDeep(item) }
        })
        this.initialInstanceList = _.cloneDeep(this.instanceList)
        this.calcColumns()
      } else {
        q += `&root_id=${this.treeKeys[this.treeKeys.length - 1].split('%')[0]}`
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
        q += `&level=${level.join(',')}`
        if (!refreshType) {
          this.loadNoRoot(this.treeKeys[this.treeKeys.length - 1], level)
        }
        await this.judgeCITypes(q)
        const fuzzySearch = (this.$refs['search'] || {}).fuzzySearch || ''
        if (fuzzySearch) {
          q = `q=_type:${this.currentTypeId[0]},*${fuzzySearch}*,` + q
        } else {
          q = `q=_type:${this.currentTypeId[0]},` + q
        }
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
        if (refreshType === 'refreshNumber') {
          this.treeKeys.map((key, index) => {
            statisticsCIRelation({
              root_ids: key.split('%')[0],
              level: this.treeKeys.length - index,
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
      this.$nextTick(() => {
        this.refreshTable()
      })
    },

    async judgeCITypes(q) {
      const showTypeIds = []
      let _showTypes = []
      let _showTypeIds = []

      if (this.treeKeys.length) {
        const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('%')[1])

        _showTypes = this.node2ShowTypes[typeId + '']
        _showTypes.forEach((item) => {
          _showTypeIds.push(item.id)
        })
      } else {
        _showTypeIds = JSON.parse(JSON.stringify(this.origShowTypeIds))
        _showTypes = JSON.parse(JSON.stringify(this.origShowTypes))
      }
      const promises = _showTypeIds.map((typeId) => {
        const _q = (`q=_type:${typeId},` + q).replace(/count=\d*/, 'count=1')
        if (this.treeKeys.length === 0) {
          return searchCI2(_q).then((res) => {
            if (res.numfound !== 0) {
              showTypeIds.push(typeId)
            }
          })
        } else {
          return searchCIRelation(_q).then((res) => {
            if (res.numfound !== 0) {
              showTypeIds.push(typeId)
            }
          })
        }
      })
      await Promise.all(promises).then(async () => {
        if (showTypeIds.length && showTypeIds.sort().join(',') !== this.showTypeIds.sort().join(',')) {
          const showTypes = []
          _showTypes.forEach((item) => {
            if (showTypeIds.includes(item.id)) {
              showTypes.push(item)
            }
          })
          this.showTypes = showTypes
          this.showTypeIds = showTypeIds
          if (
            !this.currentTypeId.length ||
            (this.currentTypeId.length && !this.showTypeIds.includes(this.currentTypeId[0]))
          ) {
            this.currentTypeId = [this.showTypeIds[0]]
            await this.loadColumns()
          }
        }
      })
    },

    async loadRoot() {
      searchCI2(`q=_type:(${this.levels[0].join(';')})&count=10000`).then(async (res) => {
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
          return statisticsCIRelation({ root_ids: ciIds.join(','), level: level }).then((num) => {
            facet.forEach((item, idx) => {
              item[1] += num[ciIds[idx] + '']
            })
          })
        })
        await Promise.all(promises)
        this.wrapTreeData(facet, 'loadRoot')
      })
    },

    async loadNoRoot(rootIdAndTypeId, level) {
      const rootId = rootIdAndTypeId.split('%')[0]
      searchCIRelation(`root_id=${rootId}&level=1&count=10000`).then(async (res) => {
        const facet = []
        const ciIds = []
        res.result.forEach((item) => {
          facet.push([item[item.unique], 0, item._id, item._type, item.unique])
          ciIds.push(item._id)
        })
        const promises = level.map((_level) => {
          if (_level > 1) {
            return statisticsCIRelation({ root_ids: ciIds.join(','), level: _level - 1 }).then((num) => {
              facet.forEach((item, idx) => {
                item[1] += num[ciIds[idx] + '']
              })
            })
          }
        })
        await Promise.all(promises)
        this.wrapTreeData(facet, 'loadNoRoot')
      })
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
          title: `${item[0]} (${item[1]})`,
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
          this.leaf = this.relationViews.views[this.viewName].leaf
          this.currentView = `${this.viewId}`
          this.typeId = this.levels[0][0]
          this.refreshTable()
        }
      })
    },

    async loadColumns() {
      this.getAttributeList()
      const res = await getSubscribeAttributes(this.currentTypeId[0])
      this.preferenceAttrList = res.attributes
      this.calcColumns()
    },

    calcColumns() {
      const width = document.getElementById('relation-views-right').clientWidth
      this.columns = getCITableColumns(this.instanceList, this.preferenceAttrList, width)
      this.$nextTick(() => {
        this.$refs.xTable.refreshColumn()
      })
    },
    onContextMenuClick(treeKey, menuKey) {
      if (treeKey) {
        const splitTreeKey = treeKey.split('@^@')
        const _tempTree = splitTreeKey[splitTreeKey.length - 1].split('%')
        const firstCIObj = JSON.parse(_tempTree[2])
        const firstCIId = _tempTree[0]
        if (menuKey === 'delete') {
          const _tempTreeParent = splitTreeKey[splitTreeKey.length - 2].split('%')
          const that = this

          this.$confirm({
            title: '警告',
            content: (h) => (
              <div>
                确认删除 <strong>{Object.values(firstCIObj)[0]}</strong>？
              </div>
            ),
            onOk() {
              deleteCIRelationView(_tempTreeParent[0], _tempTree[0]).then((res) => {
                that.$message.success('删除成功！')
                that.reload()
              })
            },
          })
        } else {
          const childTypeId = menuKey
          console.log(menuKey)
          this.$refs.addTableModal.openModal(firstCIObj, firstCIId, childTypeId, 'children')
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
        title: '警告',
        content: (h) => (
          <div>
            确认将选中的 <strong>{currentShowType.alias || currentShowType.name}</strong> 从当前关系中删除？
          </div>
        ),
        onOk() {
          const _tempTree = that.treeKeys[that.treeKeys.length - 1].split('%')
          const firstCIObj = JSON.parse(_tempTree[2])
          batchDeleteCIRelation(
            that.selectedRowKeys.map((item) => item._id),
            firstCIObj
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
        const targetId = _splitTargetKey[_splitTargetKey.length - 1].split('%')[0]
        console.log(_splitDragKey)
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
          this.$message.error('权限不足！')
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
    handleEditActived() {},
    handleEditClose({ row, rowIndex, column }) {
      const $table = this.$refs['xTable']
      const data = {}
      this.columns.forEach((item) => {
        if (!_.isEqual(row[item.field], this.initialInstanceList[rowIndex][item.field])) {
          data[item.field] = row[item.field] || null
        }
      })
      if (JSON.stringify(data) !== '{}') {
        updateCI(row.ci_id || row._id, data)
          .then(() => {
            this.$message.success('保存成功！')
            $table.reloadRow(row, null)
            const _initialInstanceList = _.cloneDeep(this.initialInstanceList)
            _initialInstanceList[rowIndex] = {
              ..._initialInstanceList[rowIndex],
              ...data,
            }
            this.initialInstanceList = _initialInstanceList
          })
          .catch((err) => {
            console.log(err)
            $table.revertData(row)
          })
      }
    },
    deleteCI(record) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认删除？',
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            that.$message.success('删除成功！')
            that.loadData({}, 'refreshNumber')
          })
        },
      })
    },
    sumbitFromCreateInstance({ ci_id }) {
      const first_ci_id = this.treeKeys[this.treeKeys.length - 1].split('%')[0]
      addCIRelationView(first_ci_id, ci_id).then((res) => {
        setTimeout(() => {
          this.loadData({}, 'refreshNumber')
        }, 500)
      })
    },
    batchUpdateFromCreateInstance(values) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认要批量修改吗 ?',
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
              that.$message.success('批量修改成功')
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
      this.$refs.batchDownload.open({ preferenceAttrList: this.preferenceAttrList })
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
        title: '警告',
        content: '确认删除？',
        onOk() {
          that.loading = true
          const promises = that.selectedRowKeys.map((c) => {
            return deleteCI(c._id).then((res) => {
              return 'ok'
            })
          })
          Promise.all(promises)
            .then((res) => {
              that.$message.success({
                message: '删除成功',
              })
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
          this.$message.success('复制成功！')
        })
        .catch(() => {
          this.$message.error('复制失败！')
        })
    },
  },
}
</script>

<style lang="less">
@import '../index.less';
@import '~@/style/static.less';

.relation-views-wrapper {
  width: 100%;
  .relation-views-left {
    width: 100%;
    float: left;
    position: relative;
    // transition: all 0.3s;
    background-color: #fff;
    overflow: hidden;
    padding: 12px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    &:hover {
      overflow: auto;
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
    .relation-views-right-bar {
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 5px;
      height: 32px;
      padding: 0 12px;
    }
  }
}
</style>
