<template>
  <div :style="{ marginBottom: '-24px' }">
    <div v-if="subscribeTreeViewCiTypesLoading" class="page-loading">
      <a-spin size="large" />
    </div>
    <div v-else-if="subscribeTreeViewCiTypes.length === 0">
      <a-alert banner>
        <template #message>
          <span>{{ $t('cmdb.preference.tips1') }}</span>
          <router-link to="/cmdb/preference">{{ $t('cmdb.preference.tips2') }}</router-link>
          <span>{{ $t('cmdb.preference.tips3') }}</span>
        </template>
      </a-alert>
    </div>
    <div class="tree-views" v-else>
      <SplitPane
        :min="200"
        :max="500"
        :paneLengthPixel.sync="paneLengthPixel"
        appName="cmdb-tree-views"
        :triggerLength="18"
        calcBasedParent
      >
        <template #one>
          <div class="tree-views-left" :style="{ height: `${windowHeight - 64}px` }">
            <draggable
              v-model="subscribeTreeViewCiTypes"
              :animation="300"
              @change="
                (e) => {
                  orderChange(e, subscribeTreeViewCiTypes)
                }
              "
            >
              <div v-for="ciType in subscribeTreeViewCiTypes" :key="ciType.type_id">
                <div
                  @click="handleChangeCi(ciType.type_id)"
                  :class="{
                    'custom-header': true,
                    'custom-header-selected': Number(ciType.type_id) === Number(typeId) && !treeKeys.length,
                  }"
                >
                  <OpsMoveIcon class="move-icon" />
                  <span class="tree-views-left-header-icon">
                    <template v-if="ciType.icon">
                      <img
                        v-if="ciType.icon.split('$$')[2]"
                        :src="`/api/common-setting/v1/file/${ciType.icon.split('$$')[3]}`"
                        :style="{ maxHeight: '14px', maxWidth: '14px' }"
                      />
                      <ops-icon
                        v-else
                        :style="{
                          color: ciType.icon.split('$$')[1],
                          fontSize: '14px',
                        }"
                        :type="ciType.icon.split('$$')[0]"
                      />
                    </template>
                    <span class="primary-color" v-else>{{ ciType.name[0].toUpperCase() }}</span>
                  </span>
                  <span class="tree-views-left-header-name">{{ ciType.alias || ciType.name }}</span>
                  <div class="actions">
                    <a-tooltip :title="$t('cmdb.preference.cancelSub')">
                      <div class="action" @click="(e) => cancelSubscribe(e, ciType)">
                        <a-icon type="star" />
                      </div>
                    </a-tooltip>
                    <a-tooltip :title="$t('cmdb.tree.subSettings')">
                      <div class="action" @click="(e) => subscribeSetting(e, ciType)">
                        <a-icon type="setting" />
                      </div>
                    </a-tooltip>
                  </div>
                </div>
                <a-tree
                  :selectedKeys="selectedKeys"
                  :tree-data="treeData"
                  :load-data="onLoadData"
                  :expandedKeys="expandedKeys"
                  v-if="Number(ciType.type_id) === Number(typeId)"
                >
                  <template #title="{ key: treeKey, title, isLeaf, childLength}">
                    <TreeViewsNode
                      :title="title"
                      :treeKey="treeKey"
                      :levels="levels"
                      :childLength="childLength"
                      :isLeaf="isLeaf"
                      @onNodeClick="onNodeClick"
                    />
                  </template>
                </a-tree>
              </div>
            </draggable>
          </div>
        </template>
        <template #two>
          <div class="tree-views-right" id="tree-views-right" :style="{ height: `${windowHeight - 64}px` }">
            <div class="cmdb-views-header">
              <span>
                <span class="cmdb-views-header-title">{{ currentCiTypeName }}</span>
                <span
                  @click="
                    () => {
                      $refs.metadataDrawer.open(typeId)
                    }
                  "
                  class="cmdb-views-header-metadata"
                ><a-icon type="info-circle" />
                  {{ $t('cmdb.ci.attributeDesc') }}
                </span>
              </span>
              <a-space>
                <a-button
                  type="primary"
                  class="ops-button-ghost"
                  ghost
                  @click="$refs.create.handleOpen(true, 'create')"
                ><ops-icon type="veops-increase" />
                  {{ $t('create') }}
                </a-button>
                <EditAttrsPopover :typeId="Number(typeId)" class="operation-icon" @refresh="refreshAfterEditAttrs">
                  <a-button
                    type="primary"
                    ghost
                    class="ops-button-ghost"
                  ><ops-icon type="veops-configuration_table" />{{ $t('cmdb.configTable') }}</a-button
                  >
                </EditAttrsPopover>
              </a-space>
            </div>
            <SearchForm
              ref="search"
              @refresh="reloadData"
              :preferenceAttrList="currentAttrList"
              :typeId="Number(typeId)"
              @copyExpression="copyExpression"
            >
              <PreferenceSearch
                v-show="!selectedRowKeys.length"
                ref="preferenceSearch"
                @getQAndSort="getQAndSort"
                @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
              />
              <div class="ops-list-batch-action">
                <template v-if="selectedRowKeys.length">
                  <span @click="$refs.create.handleOpen(true, 'update')">{{ $t('update') }}</span>
                  <a-divider type="vertical" />
                  <span @click="openBatchDownload">{{ $t('download') }}</span>
                  <a-divider type="vertical" />
                  <span @click="batchDelete">{{ $t('delete') }}</span>
                  <span>{{ $t('cmdb.ci.selectRows', { rows: selectedRowKeys.length }) }}</span>
                </template>
              </div>
            </SearchForm>

            <CITable
              ref="xTable"
              :id="`cmdb-tree-${typeId}`"
              :loading="loading"
              :attrList="currentAttrList"
              :columns="columns"
              :passwordValue="passwordValue"
              :data="instanceList"
              :height="`${windowHeight - 240}px`"
              :loadingTip="loadTip"
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
                :current="currentPage"
                size="small"
                :total="totalNumber"
                show-quick-jumper
                :page-size="pageSize"
                :page-size-options="pageSizeOptions"
                :show-total="
                  (total, range) =>
                    $t('pagination.total', {
                      range0: range[0],
                      range1: range[1],
                      total,
                    })
                "
                :style="{ alignSelf: 'flex-end' }"
                @showSizeChange="onShowSizeChange"
                @change="
                  (page) => {
                    currentPage = page
                    handleLoadInstance({ sortByTable })
                  }
                "
              >
                <template slot="buildOptionText" slot-scope="props">
                  <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
                  <span v-if="props.value === '100000'">{{ $t('all') }}</span>
                </template>
              </a-pagination>
            </div>
          </div>
        </template>
      </SplitPane>
    </div>
    <SubscribeSetting
      ref="subscribeSetting"
      @reload="
        () => {
          reload()
        }
      "
    />
    <CiDetailDrawer ref="detail" :typeId="Number(typeId)" :treeViewsLevels="treeViewsLevels" />
    <create-instance-form
      ref="create"
      :typeIdFromRelation="Number(typeId)"
      @reload="sumbitFromCreateInstance"
      @submit="batchUpdateFromCreateInstance"
    />
    <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
    <MetadataDrawer ref="metadataDrawer" />
  </div>
</template>

<script>
/* eslint-disable no-useless-escape */
import _ from 'lodash'
import Sortable from 'sortablejs'
import draggable from 'vuedraggable'
import {
  getSubscribeTreeView,
  getSubscribeAttributes,
  subscribeTreeView,
  preferenceCitypeOrder,
} from '@/modules/cmdb/api/preference'
import { searchCI, updateCI, deleteCI } from '@/modules/cmdb/api/ci'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITableColumns } from '../../utils/helper'
import SearchForm from '../../components/searchForm/SearchForm.vue'
import SubscribeSetting from '../../components/subscribeSetting/subscribeSetting'
import SplitPane from '@/components/SplitPane'
import TreeViewsNode from './modules/treeViewsNode.vue'
import EditAttrsPopover from '../ci/modules/editAttrsPopover.vue'
import CiDetailDrawer from '../ci/modules/ciDetailDrawer.vue'
import CreateInstanceForm from '../ci/modules/CreateInstanceForm'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import MetadataDrawer from '../ci/modules/MetadataDrawer.vue'
import { intersection } from '@/utils/functions/set'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { getAttrPassword } from '../../api/CITypeAttr'
import CITable from '@/modules/cmdb/components/ciTable/index.vue'

export default {
  name: 'TreeViews',
  components: {
    SearchForm,
    SubscribeSetting,
    SplitPane,
    TreeViewsNode,
    EditAttrsPopover,
    CiDetailDrawer,
    CreateInstanceForm,
    BatchDownload,
    PreferenceSearch,
    MetadataDrawer,
    OpsMoveIcon,
    draggable,
    CITable
  },
  data() {
    return {
      keySplit: '---',
      treeData: [],
      treeNode: null,
      treeKeys: [],
      subscribeTreeViewCiTypes: [],
      subscribeTreeViewCiTypesLoading: false,
      levels: [],
      typeId: null,
      instanceList: [],
      columns: [],
      loading: false,
      loadTip: '',
      pageSizeOptions: ['50', '100', '200', '100000'],
      pageSize: 50,
      currentPage: 1,
      totalNumber: 0,
      currentAttrList: [],
      trigger: false,
      newLoad: true,
      formatSearchFormData: '',
      sortByTable: undefined,
      paneLengthPixel: 205,
      expandedKeys: [],
      attrList: [],
      attributes: {},
      selectedRowKeys: [],
      // 对照是否编辑
      initialInstanceList: [],
      citypes: [],
      // 表格拖拽的参数
      tableDragClassName: [],
      // 已经设置过data的node
      isSetDataNodes: [],

      initialPasswordValue: {},
      passwordValue: {},
      lastEditCiId: null,
      isContinueCloseEdit: true,
    }
  },

  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    selectedKeys() {
      if (this.treeKeys.length <= 1) {
        return this.treeKeys.map((item) => `${this.keySplit}${item}`)
      }
      return [this.treeKeys.join(this.keySplit)]
    },
    treeViewsLevels() {
      // 当前订阅的树型视图的字段
      const _find = this.subscribeTreeViewCiTypes.find((item) => item.type_id === Number(this.typeId))
      return _find?.levels || []
    },
    treeViewId() {
      // 当前页面的id
      const _find = this.subscribeTreeViewCiTypes.find((item) => item.type_id === Number(this.typeId))
      return _find?.id
    },
    currentCiTypeName() {
      const _find = this.citypes.find((item) => Number(item.id) === Number(this.typeId))
      return _find?.alias || _find?.name || ''
    },
  },
  watch: {
    '$route.path': function(newPath, oldPath) {
      this.newLoad = true
      this.typeId = this.$route.params.typeId
      this.initPage()
    },
  },
  provide() {
    return {
      handleSearch: this.handleLoadInstance,
      setPreferenceSearchCurrent: this.setPreferenceSearchCurrent,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      },
      filterCompPreferenceSearch: () => {
        return { ptv_id: this.treeViewId }
      },
    }
  },
  inject: ['reload'],
  async created() {
    await this.getTreeViews()
  },
  mounted() {
    setTimeout(() => {
      this.columnDrop()
    }, 1000)
    getCITypes().then((res) => {
      this.citypes = res.ci_types
    })
  },
  beforeDestroy() {
    if (this.sortable) {
      this.sortable.destroy()
    }
  },
  methods: {
    async getAttributeList() {
      const res = await getCITypeAttributesById(Number(this.typeId))
      this.attrList = res.attributes
      this.attributes = res
    },
    async getTreeViews() {
      this.subscribeTreeViewCiTypesLoading = true
      const res = await getSubscribeTreeView()
      this.subscribeTreeViewCiTypesLoading = false
      this.subscribeTreeViewCiTypes = res
      if (this.subscribeTreeViewCiTypes.length) {
        this.typeId = this.$route.params.typeId || this.subscribeTreeViewCiTypes[0].type_id
        this.selectedRowKeys = []
        this.$refs.xTable.getVxetableRef().clearCheckboxRow()
        this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
        this.levels = res.find((item) => item.type_id.toString() === this.typeId.toString()).levels
        await this.initPage()
      }
    },

    async initPage() {
      this.treeNode = null
      this.treeKeys = []
      this.levels = []
      this.currentPage = 1
      this.totalNumber = 0
      this.instanceList = []
      this.selectedRowKeys = []
      this.expandedKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      await this.loadCurrentView()
      await this.getAttributeList()
      await this.loadAttrList()
      await this.handleLoadInstance()
    },

    async loadCurrentView() {
      if (this.subscribeTreeViewCiTypes.length) {
        this.typeId = this.$route.params.typeId || this.subscribeTreeViewCiTypes[0].type_id
        this.selectedRowKeys = []
        this.$refs.xTable.getVxetableRef().clearCheckboxRow()
        this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
        this.levels = this.subscribeTreeViewCiTypes.find(
          (item) => item.type_id.toString() === this.typeId.toString()
        ).levels
      }
    },

    async loadAttrList() {
      const res = await getSubscribeAttributes(this.typeId)
      this.currentAttrList = res.attributes
    },

    async handleLoadInstance(params = {}) {
      this.trigger = true
      this.loading = true
      let q = `_type:${this.typeId}`

      if (this.treeKeys.length > 0) {
        // 再增加垂直分类信息
        this.treeKeys.forEach((item, idx) => {
          q += `,${this.levels[idx].name}:${item}`
        })
      }
      if (this.formatSearchFormData) {
        q = `${q}${this.formatSearchFormData}`
      }

      const expression = this.$refs['search'] ? this.$refs['search'].expression || '' : ''

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const regSort = /(?<=sort=).+/g
      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      if (exp) {
        q = `${q},${exp}`
      }
      const fuzzySearch = this.$refs['search'].fuzzySearch
      if (fuzzySearch) {
        q = `${q},*${fuzzySearch}*`
      }
      const payload = { q }

      // 如果是表格点击的排序 以表格为准
      let sort
      const { sortByTable } = params
      if (sortByTable) {
        sort = sortByTable
      } else {
        sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
      }
      payload.sort = sort

      if (this.levels.length > this.treeKeys.length) {
        // 增加切面信息
        payload['facet'] = `${this.levels[this.treeKeys.length].name}`
      }
      payload['page'] = this.currentPage
      payload['count'] = this.pageSize

      try {
        const res = await searchCI(payload)
        this.totalNumber = res.numfound

        if (Object.values(res.facet).length) {
          this.wrapTreeData(res.facet)
        }

        const jsonAttrList = this.currentAttrList.filter((attr) => attr.value_type === '6')
        this.instanceList = res['result'].map((item) => {
          jsonAttrList.forEach(
            (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
          )
          return { ..._.cloneDeep(item) }
        })
        this.initialInstanceList = _.cloneDeep(this.instanceList)
        const treeViewsRight = document.getElementById('tree-views-right')
        if (treeViewsRight) {
          const width = treeViewsRight.clientWidth - 50
          this.columns = getCITableColumns(res.result, this.currentAttrList, width)
          this.columns.forEach((col) => {
            if (col.is_password) {
              this.initialPasswordValue[col.field] = ''
              this.passwordValue[col.field] = ''
            }
          })
        }
      } catch (e) {
        console.log(e)
        this.$message.error(e)
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.trigger = false
          if (this.$refs.xTable) {
            this.$refs.xTable.getVxetableRef().refreshColumn()
          }
        })
      }
      this.newLoad = false
    },

    wrapTreeData(facet) {
      // 切面
      const _treeData = Object.values(facet)[0].map((item) => {
        let title = item[0]
        const attr = this.attrList.find((attr) => attr.name === item[2])
        if (attr?.choice_value?.length) {
          const choice = attr.choice_value.find((choice) => item[0] === choice?.[0])
          if (choice?.[1]?.label) {
            title = choice[1].label
          }
        }

        return {
          title: title,
          childLength: item[1],
          key: this.treeKeys.join(this.keySplit) + this.keySplit + item[0],
          isLeaf: this.levels.length - 1 === this.treeKeys.length,
        }
      })
      if (this.treeNode === null && this.newLoad) {
        this.treeData = _treeData
        this.treeNode = { dataRef: {} }
      } else {
        if (!this.isSetDataNodes.includes(this.treeNode.dataRef.key)) {
          this.treeNode.dataRef.children = _treeData
          this.treeData = [...this.treeData]
          this.isSetDataNodes.push(this.treeNode.dataRef.key)
        }
      }
    },
    onLoadData(treeNode) {
      this.triggerSelect = false
      return new Promise((resolve) => {
        if (treeNode.dataRef.children) {
          resolve()
          return
        }
        this.treeKeys = treeNode.eventKey.split(this.keySplit).filter((item) => item !== '')
        this.treeNode = treeNode
        this.selectedRowKeys = []
        this.$refs.xTable.getVxetableRef().clearCheckboxRow()
        this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
        resolve()
      })
    },
    handleChangeCi(value) {
      if (value && Number(this.typeId) !== Number(value)) {
        this.treeData = []
        this.$router.history.push({
          name: 'cmdb_tree_views_item',
          params: { typeId: Number(value) },
        })
        this.typeId = Number(value)
      } else {
        this.typeId = null
        this.$nextTick(() => {
          this.typeId = Number(value)
          this.newLoad = true
          this.initPage()
        })
      }
      this.isSetDataNodes = []
    },
    async reloadData() {
      const queryParams = this.$refs['search'].queryParam || {}
      this.formatSearchFormData = this.mergeQ(queryParams)
      this.currentPage = 1
      this.sortByTable = undefined
      const xTable = this.$refs.xTable.getVxetableRef()
      xTable.clearSort().then(() => {
        this.handleLoadInstance()
      })
    },
    mergeQ(params) {
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
      return q
    },
    cancelSubscribe(e, ciType) {
      e.stopPropagation()
      e.preventDefault()
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: (h) => (
          <div>{that.$t('cmdb.preference.confirmcancelSub2', { name: ciType.alias || ciType.name })}</div>
        ),
        onOk() {
          subscribeTreeView(ciType.type_id, []).then(() => {
            that.$message.success(that.$t('cmdb.preference.cancelSubSuccess'))
            if (Number(that.$route.params.typeId) === Number(ciType.type_id)) {
              that.$router.history.push('/cmdb/treeviews')
              that.reload()
            } else {
              that.reload()
            }
          })
        },
      })
    },
    subscribeSetting(e, ciType) {
      e.stopPropagation()
      e.preventDefault()
      this.$refs.subscribeSetting.open(ciType)
    },
    columnDrop() {
      this.$nextTick(() => {
        const xTable = this.$refs?.xTable?.getVxetableRef?.()
        if (!xTable) {
          return
        }

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
    handleSortCol({ column, property, order, sortBy, sortList, $event }) {
      let sortByTable
      if (order === 'asc') {
        sortByTable = property
      } else if (order === 'desc') {
        sortByTable = `-${property}`
      }
      this.sortByTable = sortByTable
      this.currentPage = 1
      this.handleLoadInstance({ sortByTable })
    },
    onNodeClick(keys, type) {
      console.log(keys)
      if (keys) {
        const _tempKeys = keys.split(this.keySplit).filter((item) => item !== '')
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
      this.handleLoadInstance()
    },
    async refreshAfterEditAttrs() {
      await this.loadAttrList()
      await this.handleLoadInstance()
    },
    deleteCI(record) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.reload()
          })
        },
      })
    },
    onSelectChange(records) {
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
    },
    setSelectRows() {
      const cached = new Set(this.selectedRowKeys)
      const loaded = new Set(this.instanceList.map((i) => i.ci_id || i._id))

      const inter = Array.from(intersection(cached, loaded))

      if (inter.length === this.instanceList.length) {
        this.$refs['xTable'].getVxetableRef().setAllCheckboxRow(true)
      } else {
        const rows = []
        inter.forEach((rid) => {
          rows.push(this.$refs['xTable'].getVxetableRef().getRowById(rid))
        })
        this.$refs['xTable'].getVxetableRef().setCheckboxRow(rows, true)
      }
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
        updateCI(row._id, data)
          .then(() => {
            this.$message.success(this.$t('saveSuccess'))
            const arr1 = this.treeViewsLevels.map((item) => item.name)
            const arr2 = Object.keys(data)
            const arr3 = arr1.filter((item) => {
              return arr2.includes(item)
            })
            if (arr3.length) {
              this.reload()
              return
            }
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
      this.columns.forEach((col) => {
        if (col.is_password) {
          this.initialPasswordValue[col.field] = ''
          this.passwordValue[col.field] = ''
        }
      })
    },
    async openBatchDownload() {
      this.$refs.batchDownload.open({ preferenceAttrList: this.currentAttrList.filter((attr) => !attr?.is_reference), ciTypeName: this.currentCiTypeName })
    },
    batchDownload({ filename, type, checkedKeys }) {
      console.log(filename, type)
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.currentAttrList.find((attr) => attr.name === key)
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
          that.batchDeleteAsync()
        },
      })
    },
    async batchDeleteAsync() {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.batchDeleting')
      const floor = Math.ceil(this.selectedRowKeys.length / 6)
      for (let i = 0; i < floor; i++) {
        const itemList = this.selectedRowKeys.slice(6 * i, 6 * i + 6)
        const promises = itemList.map((x) => deleteCI(x, false))
        await Promise.allSettled(promises)
          .then((res) => {
            res.forEach((r) => {
              if (r.status === 'fulfilled') {
                successNum += 1
              } else {
                errorNum += 1
              }
            })
          })
          .finally(() => {
            this.loadTip = this.$t('cmdb.ci.batchDeleting2', {
              total: this.selectedRowKeys.length,
              successNum: successNum,
              errorNum: errorNum,
            })
          })
      }
      this.loading = false
      this.loadTip = ''
      this.reload()
    },
    sumbitFromCreateInstance({ ci_id }) {
      this.reload()
    },
    batchUpdateFromCreateInstance(values) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ci.batchUpdateConfirm'),
        onOk() {
          that.batchUpdateAsync(values)
        },
      })
    },
    async batchUpdateAsync(values) {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.batchUpdateInProgress')
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
      this.$refs.create.visible = false
      const key = 'updatable'
      let errorMsg = ''
      for (let i = 0; i < this.selectedRowKeys.length; i++) {
        await updateCI(this.selectedRowKeys[i], payload, false)
          .then(() => {
            successNum += 1
          })
          .catch((error) => {
            errorMsg = errorMsg + '\n' + `${this.selectedRowKeys[i]}:${error.response?.data?.message ?? ''}`
            this.$notification.warning({
              key,
              message: this.$t('warning'),
              description: errorMsg,
              duration: 0,
              style: { whiteSpace: 'break-spaces' },
            })
            errorNum += 1
          })
          .finally(() => {
            this.loadTip = this.$t('cmdb.ci.batchUpdateInProgress2', {
              total: this.selectedRowKeys.length,
              successNum: successNum,
              errorNum: errorNum,
            })
          })
      }
      this.loading = false
      this.loadTip = ''
      const arr1 = this.treeViewsLevels.map((item) => item.name)
      const arr2 = Object.keys(values)
      const arr3 = arr1.filter((item) => {
        return arr2.includes(item)
      })
      if (arr3.length) {
        this.reload()
        return
      }
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.handleLoadInstance()
    },
    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize
      this.currentPage = 1
      this.handleLoadInstance()
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
      this.currentPage = 1
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$nextTick(() => {
        this.handleLoadInstance()
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
      const text = `q=_type:${this.typeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },
    orderChange(e, subscribeTreeViewCiTypes) {
      preferenceCitypeOrder({ type_ids: subscribeTreeViewCiTypes.map((type) => type.type_id), is_tree: true }).catch(
        () => {
          this.getTreeViews()
        }
      )
    },
    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$refs.detail.create(id, activeTabKey, ciDetailRelationKey)
    }
  },
}
</script>

<style lang="less">
@import '../index.less';
.page-loading {
  text-align: center;
  padding-top: 150px;
}

.tree-views {
  width: 100%;
  height: calc(100% - 32px);
  .tree-views-left {
    float: left;
    position: relative;
    overflow: hidden;
    width: 100%;
    &:hover {
      overflow: auto;
    }
    .custom-header {
      width: 100%;
      display: inline-flex;
      flex-direction: row;
      flex-wrap: nowrap;
      justify-content: flex-start;
      align-items: center;
      padding: 8px 0 8px 12px;
      cursor: move;
      border-radius: 2px;
      position: relative;
      &:hover {
        background-color: @primary-color_3;
        > .actions,
        > .move-icon {
          display: inherit;
        }
      }
      .move-icon {
        width: 14px;
        height: 20px;
        cursor: move;
        position: absolute;
        display: none;
        left: 0;
      }
      .tree-views-left-header-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 2px;
        margin-right: 6px;
      }
      .tree-views-left-header-name {
        flex: 1;
        font-weight: bold;
        margin-left: 5px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: @text-color_1;
      }
      .actions {
        display: none;
        margin-left: auto;
        cursor: pointer;
      }
      .action {
        display: inline-block;
        width: 22px;
        text-align: center;
        border-radius: 5px;
        &:hover {
          background-color: #cacaca;
        }
      }
    }
    .custom-header-selected {
      background-color: @primary-color_3 !important;
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
    .ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected {
      background-color: @primary-color_3;
    }
  }
  .tree-views-right {
    background-color: #fff;
    display: flex;
    flex-direction: column;
    padding: 20px;
    overflow: auto;
    width: 100%;
    border-radius: @border-radius-box;
  }
}
</style>
