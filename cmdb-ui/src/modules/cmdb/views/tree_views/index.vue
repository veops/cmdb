<template>
  <div :style="{ marginBottom: '-24px' }">
    <div v-if="!subscribeTreeViewCiTypesLoading && subscribeTreeViewCiTypes.length === 0">
      <a-alert :message="$t('cmdb.tree.tips1')" banner></a-alert>
    </div>
    <div class="tree-views" v-else>
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
            {{ $t('cmdb.components.attributeDesc') }}
          </span>
        </span>
        <a-button size="small" icon="plus" type="primary" @click="$refs.create.handleOpen(true, 'create')">{{
          $t('create')
        }}</a-button>
      </div>
      <SplitPane
        :min="200"
        :max="500"
        :paneLengthPixel.sync="paneLengthPixel"
        appName="cmdb-tree-views"
        triggerColor="#F0F5FF"
        :triggerLength="18"
      >
        <template #one>
          <div class="tree-views-left" :style="{ height: `${windowHeight - 115}px` }">
            <a-collapse
              :activeKey="current"
              accordion
              @change="handleChangeCi"
              :bordered="false"
              :destroyInactivePanel="true"
            >
              <a-collapse-panel
                v-for="ciType in subscribeTreeViewCiTypes"
                :key="String(ciType.type_id)"
                :showArrow="false"
                :style="{
                  borderRadius: '4px',
                  marginBottom: '5px',
                  border: 0,
                  overflow: 'hidden',
                  width: '100%',
                }"
              >
                <div
                  slot="header"
                  :class="{
                    'custom-header': true,
                    'custom-header-selected': Number(ciType.type_id) === Number(typeId),
                  }"
                >
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
                    <span :style="{ color: '#2f54eb' }" v-else>{{ ciType.name[0].toUpperCase() }}</span>
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
                >
                  <a-icon slot="switcherIcon" type="down" />
                  <template #title="{ key: treeKey, title, isLeaf }">
                    <TreeViewsNode
                      :title="title"
                      :treeKey="treeKey"
                      :levels="levels"
                      :isLeaf="isLeaf"
                      @onNodeClick="onNodeClick"
                    />
                  </template>
                </a-tree>
              </a-collapse-panel>
            </a-collapse>
          </div>
        </template>
        <template #two>
          <div class="tree-views-right" id="tree-views-right" :style="{ height: `${windowHeight - 115}px` }">
            <SearchForm
              ref="search"
              @refresh="reloadData"
              :preferenceAttrList="currentAttrList"
              :typeId="Number(typeId)"
              @copyExpression="copyExpression"
            />
            <div class="tree-views-right-bar">
              <PreferenceSearch
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
            </div>
            <ops-table
              :id="`cmdb-tree-${typeId}`"
              border
              ref="xTable"
              size="small"
              keep-source
              :loading="loading"
              :data="instanceList"
              highlight-hover-row
              show-overflow
              show-header-overflow
              row-id="_id"
              resizable
              :row-key="true"
              :column-key="true"
              :sort-config="{ remote: true, trigger: 'cell' }"
              @sort-change="handleSortCol"
              :cell-style="getCellStyle"
              :scroll-y="{ enabled: true, gt: 20 }"
              :scroll-x="{ enabled: true, gt: 0 }"
              :height="`${windowHeight - 252}px`"
              @checkbox-change="onSelectChange"
              @checkbox-all="onSelectChange"
              @checkbox-range-end="onSelectRangeEnd"
              :checkbox-config="{ reserve: true, highlight: true, range: true }"
              @edit-closed="handleEditClose"
              @edit-actived="handleEditActived"
              :edit-config="{ trigger: 'dblclick', mode: 'row', showIcon: false }"
              class="ops-unstripe-table"
              :style="{ margin: '0 -12px' }"
              :custom-config="{ storage: true }"
            >
              <vxe-column align="center" type="checkbox" width="60" :fixed="isCheckboxFixed ? 'left' : ''"></vxe-column>
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
                <template v-if="col.is_choice || col.is_password || col.is_list" #edit="{ row }">
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
                  <a-select
                    :getPopupContainer="(trigger) => trigger.parentElement"
                    :style="{ width: '100%', height: '32px' }"
                    v-model="row[col.field]"
                    :placeholder="$t('placeholder2')"
                    v-else-if="col.is_list"
                    :showArrow="false"
                    mode="tags"
                    class="ci-table-edit-select"
                    allowClear
                  >
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
              <vxe-table-column align="left" field="operate" fixed="right" width="120">
                <template #header>
                  <span>{{ $t('operation') }}</span>
                  <EditAttrsPopover :typeId="Number(typeId)" class="operation-icon" @refresh="refreshAfterEditAttrs" />
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
                    <template>
                      <a-tooltip :title="$t('cmdb.ciType.deleteInstance')">
                        <a @click="deleteCI(row)" :style="{ color: 'red' }">
                          <a-icon type="delete" />
                        </a>
                      </a-tooltip>
                    </template>
                  </a-space>
                </template>
              </vxe-table-column>
              <template #empty>
                <div v-if="loading" style="height: 200px; line-height: 200px">{{ $t('loading') }}</div>
                <div v-else>
                  <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
                  <div>{{ $t('noData') }}</div>
                </div>
              </template>
              <template #loading>
                <div style="height: 200px; line-height: 200px">{{ loadTip || $t('loading') }}</div>
              </template>
            </ops-table>
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
    <ci-detail ref="detail" :typeId="Number(typeId)" :treeViewsLevels="treeViewsLevels" />
    <create-instance-form
      ref="create"
      :typeIdFromRelation="Number(typeId)"
      @reload="sumbitFromCreateInstance"
      @submit="batchUpdateFromCreateInstance"
    />
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
    <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
    <MetadataDrawer ref="metadataDrawer" />
  </div>
</template>

<script>
/* eslint-disable no-useless-escape */
import _ from 'lodash'
import Sortable from 'sortablejs'
import { getSubscribeTreeView, getSubscribeAttributes, subscribeTreeView } from '@/modules/cmdb/api/preference'
import { searchCI, updateCI, deleteCI } from '@/modules/cmdb/api/ci'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITableColumns } from '../../utils/helper'
import SearchForm from '../../components/searchForm/SearchForm.vue'
import SubscribeSetting from '../../components/subscribeSetting/subscribeSetting'
import PasswordField from '../../components/passwordField/index.vue'
import SplitPane from '@/components/SplitPane'
import TreeViewsNode from './modules/treeViewsNode.vue'
import EditAttrsPopover from '../ci/modules/editAttrsPopover.vue'
import CiDetail from '../ci/modules/CiDetail'
import CreateInstanceForm from '../ci/modules/CreateInstanceForm'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import JsonEditor from '../../components/JsonEditor/jsonEditor.vue'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import MetadataDrawer from '../ci/modules/MetadataDrawer.vue'
import { intersection } from '@/utils/functions/set'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { getAttrPassword } from '../../api/CITypeAttr'

export default {
  name: 'TreeViews',
  components: {
    SearchForm,
    SubscribeSetting,
    PasswordField,
    SplitPane,
    TreeViewsNode,
    EditAttrsPopover,
    CiDetail,
    CreateInstanceForm,
    JsonEditor,
    BatchDownload,
    PreferenceSearch,
    MetadataDrawer,
    OpsMoveIcon,
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
      current: '', // 当前页面的type_id
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
    isCheckboxFixed() {
      const idx = this.columns.findIndex((item) => item.is_fixed)
      return idx > -1
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
      await getCITypeAttributesById(Number(this.typeId)).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },
    async getTreeViews() {
      this.subscribeTreeViewCiTypesLoading = true
      const res = await getSubscribeTreeView()
      this.subscribeTreeViewCiTypesLoading = false
      this.subscribeTreeViewCiTypes = res
      if (this.subscribeTreeViewCiTypes.length) {
        this.typeId = this.$route.params.typeId || this.subscribeTreeViewCiTypes[0].type_id
        this.current = `${this.typeId}`
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
        this.current = String(this.typeId)
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
      console.log('facet', facet)
      const _treeData = Object.values(facet)[0].map((item) => {
        return {
          title: `${item[0]} (${item[1]})`,
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
      } else {
        this.newLoad = true
        this.initPage()
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
        const xTable = this.$refs.xTable.getVxetableRef()
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
      const _find = this.currentAttrList.find((attr) => attr.name === property)
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
    onSelectChange(e) {
      const xTable = this.$refs.xTable.getVxetableRef()
      const records = [...xTable.getCheckboxRecords(), ...xTable.getCheckboxReserveRecords()]
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
    onSelectRangeEnd({ records }) {
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
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
    jsonEditorOk(row, column, jsonData) {
      // 后端写数据有快慢，不拉接口直接修改table的数据
      // this.reloadData()
      this.instanceList.forEach((item) => {
        if (item._id === row._id) {
          item[column.property] = JSON.stringify(jsonData)
        }
      })
      this.$refs.xTable.getVxetableRef().refreshColumn()
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
    handleFocusJson({ column, row }) {
      this.$refs.jsonEditor.open(column, row)
    },
    async openBatchDownload() {
      this.$refs.batchDownload.open({ preferenceAttrList: this.currentAttrList, ciTypeName: this.currentCiTypeName })
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
      for (let i = 0; i < this.selectedRowKeys.length; i++) {
        await updateCI(this.selectedRowKeys[i], payload, false)
          .then(() => {
            successNum += 1
          })
          .catch(() => {
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
  },
}
</script>

<style lang="less">
@import '../index.less';
.tree-views {
  width: 100%;
  height: calc(100% - 32px);
  .tree-views-left {
    float: left;
    position: relative;
    background-color: #fff;
    overflow: hidden;
    width: 100%;
    padding: 12px;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    &:hover {
      overflow: auto;
    }
    .ant-collapse-borderless {
      background-color: #fff;
    }
    .ant-collapse-item:has(.custom-header-selected):not(:has(.ant-tree-treenode-selected)) > .ant-collapse-header,
    .ant-collapse-item-active:not(:has(.ant-tree-treenode-selected)) > .ant-collapse-header {
      background-color: #d6e4ff;
    }
    .ant-collapse-header {
      padding: 8px 12px 4px;
      &:hover {
        background-color: #f0f5ff;
      }
      &:hover > .custom-header > .actions {
        display: inherit;
      }
      .custom-header {
        width: 100%;
        display: inline-flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: flex-start;
        align-items: center;
        .tree-views-left-header-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 20px;
          height: 20px;
          border-radius: 2px;
          box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
          margin-right: 6px;
          background-color: #fff;
        }
        .tree-views-left-header-name {
          flex: 1;
          font-weight: bold;
          margin-left: 5px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .actions {
          display: none;
          margin-left: auto;
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
    }

    .ant-collapse > .ant-collapse-item > .ant-collapse-header {
      white-space: nowrap;
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
  .tree-views-right {
    background-color: #fff;
    display: flex;
    flex-direction: column;
    padding: 12px;
    overflow: auto;
    width: 100%;
    border-radius: 15px;
    .tree-views-right-bar {
      display: inline-flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 10px;
      height: 36px;
    }
  }
}
</style>
