<template>
  <div id="ciIndex" class="cmdb-ci">
    <div class="cmdb-views-header">
      <span>
        <span class="cmdb-views-header-title">{{ $route.meta.title || $route.meta.name }}</span>
        <span
          @click="
            () => {
              $refs.metadataDrawer.open(typeId)
            }
          "
          class="cmdb-views-header-metadata"
        >
          <a-icon type="info-circle" />属性说明
        </span>
      </span>
      <a-space>
        <a-button size="small" icon="plus" type="primary" @click="$refs.create.handleOpen(true, 'create')">
          新建
        </a-button>
        <a-button size="small" icon="user-add" type="primary" ghost @click="handlePerm">授权</a-button>
        <a-popconfirm
          :title="`确认取消订阅 ${this.$route.meta.title || this.$route.meta.name} 吗？`"
          ok-text="确认"
          cancel-text="取消"
          @confirm="unsubscribe"
          placement="bottomRight"
        >
          <a-button size="small" icon="star" type="primary" ghost>取消订阅</a-button>
        </a-popconfirm>
      </a-space>
    </div>
    <div class="cmdb-ci-main">
      <a-spin :tip="loadTip" :spinning="loading">
        <SearchForm
          ref="search"
          @refresh="handleSearch"
          :preferenceAttrList="preferenceAttrList"
          :typeId="typeId"
          :selectedRowKeys="selectedRowKeys"
          @copyExpression="copyExpression"
        >
          <PreferenceSearch
            ref="preferenceSearch"
            v-show="!selectedRowKeys.length"
            @getQAndSort="getQAndSort"
            @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
          />
          <div class="ops-list-batch-action" v-show="!!selectedRowKeys.length">
            <span @click="$refs.create.handleOpen(true, 'update')">修改</span>
            <a-divider type="vertical" />
            <span @click="openBatchDownload">下载</span>
            <a-divider type="vertical" />
            <span @click="batchDelete">删除</span>
            <span>选取：{{ selectedRowKeys.length }} 项</span>
          </div>
        </SearchForm>
        <CiDetail ref="detail" :typeId="typeId" />
        <ops-table
          :id="`cmdb-ci-${typeId}`"
          border
          keep-source
          show-overflow
          resizable
          ref="xTable"
          size="small"
          :row-config="{ useKey: true, keyField: '_id' }"
          :height="tableHeight"
          show-header-overflow
          highlight-hover-row
          :data="instanceList"
          @checkbox-change="onSelectChange"
          @checkbox-all="onSelectChange"
          @checkbox-range-end="onSelectRangeEnd"
          :checkbox-config="{ reserve: true, highlight: true, range: true }"
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
            <!-- <template #edit="{row}"><a-input v-model="row[col.field]"></a-input></template> -->
            <template #header>
              <span class="vxe-handle">
                <OpsMoveIcon
                  style="width: 17px; height: 17px; display: none; position: absolute; left: -3px; top: 12px"
                />
                <span>{{ col.title }}</span>
              </span>
            </template>
            <template v-if="col.is_choice || col.is_password" #edit="{ row }">
              <vxe-input v-if="col.is_password" v-model="passwordValue[col.field]" />
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
              #default="{ row }"
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
                    />{{ value }}
                  </span>
                </template>
                <span
                  v-else
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
                  />
                  {{ row[col.field] }}
                </span>
              </template>
            </template>
          </vxe-table-column>
          <vxe-column align="left" field="operate" fixed="right" width="80">
            <template #header>
              <span>操作</span>
              <EditAttrsPopover :typeId="typeId" class="operation-icon" @refresh="refreshAfterEditAttrs" />
              <!-- <a-icon class="operation-icon" type="control" /> -->
            </template>
            <template #default="{ row }">
              <a-space>
                <a @click="$refs.detail.create(row.ci_id || row._id)">
                  <a-icon type="unordered-list" />
                </a>
                <a-tooltip title="添加关系">
                  <a @click="$refs.detail.create(row.ci_id || row._id, 'tab_2', '2')">
                    <a-icon type="retweet" />
                  </a>
                </a-tooltip>
                <a @click="deleteCI(row)" :style="{ color: 'red' }">
                  <a-icon type="delete" />
                </a>
              </a-space>
            </template>
          </vxe-column>
          <template #empty>
            <div v-if="loading" style="height: 200px; line-height: 200px">加载中...</div>
            <div v-else>
              <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
              <div>暂无数据</div>
            </div>
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
            @showSizeChange="onShowSizeChange"
            :show-total="(total, range) => `当前${range[0]}-${range[1]} 共 ${total}条记录`"
            @change="
              (page) => {
                currentPage = page
              }
            "
          >
            <template slot="buildOptionText" slot-scope="props">
              <span v-if="props.value !== '100000'">{{ props.value }}条/页</span>
              <span v-if="props.value === '100000'">全部</span>
            </template>
          </a-pagination>
        </div>
        <create-instance-form ref="create" @reload="reloadData" @submit="batchUpdate" />
        <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
        <BatchDownload ref="batchDownload" @batchDownload="batchDownload" />
        <MetadataDrawer ref="metadataDrawer" />
        <CMDBGrant ref="cmdbGrant" resourceTypeName="CIType" app_id="cmdb" />
      </a-spin>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import Sortable from 'sortablejs'
import store from '@/store'
import router, { resetRouter } from '@/router'

import SearchForm from '../../components/searchForm/SearchForm.vue'
import CreateInstanceForm from './modules/CreateInstanceForm'
import CiDetail from './modules/CiDetail'
import EditAttrsPopover from './modules/editAttrsPopover'
import JsonEditor from '../../components/JsonEditor/jsonEditor.vue'
import { searchCI, updateCI, deleteCI } from '@/modules/cmdb/api/ci'
import { getSubscribeAttributes, subscribeCIType, subscribeTreeView } from '@/modules/cmdb/api/preference'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import { getCITableColumns } from '../../utils/helper'
import { intersection } from '@/utils/functions/set'
import PasswordField from '../../components/passwordField/index.vue'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'
import MetadataDrawer from './modules/MetadataDrawer.vue'
import CMDBGrant from '../../components/cmdbGrant'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { getAttrPassword } from '../../api/CITypeAttr'

export default {
  name: 'InstanceList',
  components: {
    SearchForm,
    CreateInstanceForm,
    CiDetail,
    JsonEditor,
    PasswordField,
    EditAttrsPopover,
    BatchDownload,
    PreferenceSearch,
    MetadataDrawer,
    CMDBGrant,
    OpsMoveIcon,
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    isCheckboxFixed() {
      const idx = this.columns.findIndex((item) => item.is_fixed)
      return idx > -1
    },
    tableHeight() {
      // if (this.selectedRowKeys && this.selectedRowKeys.length) {
      //   return this.windowHeight - 246
      // }
      return this.windowHeight - 210
    },
  },
  data() {
    return {
      tableData: [],
      loading: false,
      currentPage: 1,
      pageSizeOptions: ['50', '100', '200', '100000'],
      pageSize: 50,
      totalNumber: 0,
      loadTip: '',
      form: this.$form.createForm(this),
      typeId: this.$router.currentRoute.meta.typeId,
      preferenceAttrList: [],

      instanceList: [],
      // 表头
      columns: [],
      // custom table alert & rowSelection
      selectedRowKeys: [],
      // 对照是否编辑
      initialInstanceList: [],
      sortByTable: undefined,
      isEditActive: false,
      attrList: [],
      attributes: {},
      // 表格拖拽的参数
      tableDragClassName: [],

      resource_type: {},

      initialPasswordValue: {},
      passwordValue: {},
      lastEditCiId: null,
      isContinueCloseEdit: true,
    }
  },
  watch: {
    '$route.path': function(newPath, oldPath) {
      this.reloadBoard()
    },
    currentPage: function(newVal, oldVal) {
      this.loadTableData(this.sortByTable)
    },
  },
  async created() {
    await this.getAttributeList()
    await this.loadPreferenceAttrList()
    await this.loadTableData()
    localStorage.setItem('ops_ci_typeid', this.typeId)
  },

  provide() {
    return {
      handleSearch: this.handleSearch,
      setPreferenceSearchCurrent: this.setPreferenceSearchCurrent,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      },
      filterCompPreferenceSearch: () => {
        return { type_id: this.typeId }
      },
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  inject: ['reloadBoard'],
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
  methods: {
    async getAttributeList() {
      await getCITypeAttributesById(this.typeId).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },
    handleSearch() {
      this.$refs.xTable.getVxetableRef().clearSort()
      this.sortByTable = undefined
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.reloadData()
        } else {
          this.currentPage = 1
        }
      })
    },
    async loadTableData(sortByTable = undefined) {
      try {
        this.loading = true
        // 若模糊搜索可以 queryParam相关后期可删除
        const fuzzySearch = this.$refs['search'].fuzzySearch
        const expression = this.$refs['search'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
        const regSort = /(?<=sort=).+/g

        const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
        // 如果是表格点击的排序 以表格为准
        let sort
        if (sortByTable) {
          sort = sortByTable
        } else {
          sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
        }
        const res = await searchCI({
          q: `_type:${this.typeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
          // q: `${this.mergeQ(queryParams)}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
          count: this.pageSize,
          page: this.currentPage,
          sort,
        })
        this.totalNumber = res['numfound']
        this.columns = this.getColumns(res.result, this.preferenceAttrList)
        this.columns.forEach((col) => {
          if (col.is_password) {
            this.initialPasswordValue[col.field] = ''
            this.passwordValue[col.field] = ''
          }
        })
        const jsonAttrList = this.attrList.filter((attr) => attr.value_type === '6')
        this.instanceList = res['result'].map((item) => {
          jsonAttrList.forEach(
            (jsonAttr) => (item[jsonAttr.name] = item[jsonAttr.name] ? JSON.stringify(item[jsonAttr.name]) : '')
          )
          return { ..._.cloneDeep(item) }
        })
        this.initialInstanceList = _.cloneDeep(this.instanceList)
        this.$nextTick(() => {
          // this.setSelectRows()
          this.$refs.xTable.getVxetableRef().refreshColumn()
        })
      } finally {
        this.loading = false
      }
    },
    getColumns(data, attrList) {
      const width = document.getElementById('ciIndex').clientWidth - 50
      return getCITableColumns(data, attrList, width)
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
    async loadPreferenceAttrList() {
      const subscribed = await getSubscribeAttributes(this.typeId)
      this.preferenceAttrList = subscribed.attributes // 已经订阅的全部列
    },

    onSelectChange() {
      const xTable = this.$refs.xTable.getVxetableRef()
      const records = [...xTable.getCheckboxRecords(), ...xTable.getCheckboxReserveRecords()]
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
    },
    onSelectRangeEnd({ records }) {
      this.selectedRowKeys = records.map((i) => i.ci_id || i._id)
    },
    reloadData() {
      this.loadTableData()
    },

    handleEditClose({ row, rowIndex, column }) {
      if (!this.isContinueCloseEdit) {
        return
      }
      const $table = this.$refs['xTable'].getVxetableRef()
      const data = {}
      this.columns.forEach((item) => {
        if (!(item.field in this.initialPasswordValue) && !_.isEqual(row[item.field], this.initialInstanceList[rowIndex][item.field])) {
          data[item.field] = row[item.field] ?? null
        }
      })
      Object.keys(this.initialPasswordValue).forEach((key) => {
        if (this.initialPasswordValue[key] !== this.passwordValue[key]) {
          data[key] = this.passwordValue[key]
        }
      })
      this.isEditActive = false
      this.lastEditCiId = null
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
      this.columns.forEach((col) => {
        if (col.is_password) {
          this.initialPasswordValue[col.field] = ''
          this.passwordValue[col.field] = ''
        }
      })
    },

    async openBatchDownload() {
      this.$refs.batchDownload.open({ preferenceAttrList: this.preferenceAttrList })
    },
    batchDownload({ filename, type, checkedKeys }) {
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.attrList.find((attr) => attr.name === key)
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
    batchUpdate(values) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认要批量修改吗？',
        async onOk() {
          that.batchUpdateAsync(values)
        },
      })
    },
    async batchUpdateAsync(values) {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = `正在批量修改...`
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
            this.loadTip = `正在批量修改，共${this.selectedRowKeys.length}个，成功${successNum}个，失败${errorNum}个`
          })
      }
      this.loading = false
      this.loadTip = ''
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.reloadData()
    },
    batchDelete() {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认删除？',
        onOk() {
          that.batchDeleteAsync()
        },
      })
    },
    async batchDeleteAsync() {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = `正在删除...`
      for (let i = 0; i < this.selectedRowKeys.length; i++) {
        await deleteCI(this.selectedRowKeys[i], false)
          .then(() => {
            successNum += 1
          })
          .catch(() => {
            errorNum += 1
          })
          .finally(() => {
            this.loadTip = `正在删除，共${this.selectedRowKeys.length}个，成功${successNum}个，失败${errorNum}个`
          })
      }
      this.loading = false
      this.loadTip = ''
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData()
        } else {
          this.currentPage = 1
        }
      })
    },
    deleteCI(record) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认删除？',
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            // that.$refs.table.refresh(true)
            that.$message.success('删除成功！')
            that.reloadData()
          })
        },
      })
    },
    async refreshAfterEditAttrs() {
      await this.loadPreferenceAttrList()
      await this.loadTableData()
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
    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize
      if (this.currentPage === 1) {
        this.reloadData()
      } else {
        this.currentPage = 1
      }
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
        if (this.currentPage === 1) {
          this.loadTableData(sortByTable)
        } else {
          this.currentPage = 1
        }
      })
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
              const { newIndex, oldIndex, from, to } = params
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
    handleEditActived() {
      this.isEditActive = true
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
    getQAndSort() {
      const fuzzySearch = this.$refs['search'].fuzzySearch || ''
      const expression = this.$refs['search'].expression || ''
      this.$refs.preferenceSearch.savePreference({ fuzzySearch, expression })
    },
    setParamsFromPreferenceSearch(item) {
      const { fuzzySearch, expression } = item.option
      this.$refs.search.fuzzySearch = fuzzySearch
      this.$refs.search.expression = expression
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.$refs.xTable.getVxetableRef().clearSort()
      this.sortByTable = undefined
      this.$nextTick(() => {
        if (this.currentPage === 1) {
          this.loadTableData()
        } else {
          this.currentPage = 1
        }
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
          this.$message.success('复制成功！')
        })
        .catch(() => {
          this.$message.error('复制失败！')
        })
    },
    unsubscribe(ciType, type = 'all') {
      const promises = [subscribeCIType(this.typeId, ''), subscribeTreeView(this.typeId, '')]
      Promise.all(promises).then(() => {
        this.$message.success('取消订阅成功')
        this.resetRoute()
        this.$router.push('/cmdb/preference')
      })
    },
    resetRoute() {
      resetRouter()
      const roles = store.getters.roles
      store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
        router.addRoutes(store.getters.appRoutes)
      })
    },
    handlePerm() {
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'CIType',
        perm: 'grant',
        resource_name: this.$route.meta.name,
      }).then((res) => {
        if (res.result) {
          searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
            this.resource_type = { groups: res.groups, id2perms: res.id2perms }
            this.$nextTick(() => {
              this.$refs.cmdbGrant.open({
                name: this.$route.meta.name,
                cmdbGrantType: 'ci',
                CITypeId: this.typeId,
              })
            })
          })
        } else {
          this.$message.error('权限不足！')
        }
      })
    },
  },
}
</script>

<style lang="less">
@import '../index.less';
</style>

<style lang="less" scoped>
@import '~@/style/static.less';
.cmdb-ci {
  margin-bottom: -24px;
  .cmdb-ci-main {
    background-color: #fff;
    border-radius: 15px;
    padding: 12px;
  }
}
</style>
