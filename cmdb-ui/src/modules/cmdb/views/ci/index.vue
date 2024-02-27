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
          <a-icon type="info-circle" />{{ $t('cmdb.ci.attributeDesc') }}
        </span>
      </span>
      <a-space>
        <a-button size="small" icon="plus" type="primary" @click="$refs.create.handleOpen(true, 'create')">
          {{ $t('create') }}
        </a-button>
        <a-button size="small" icon="user-add" type="primary" ghost @click="handlePerm">{{ $t('grant') }}</a-button>
        <a-popconfirm
          :title="
            $t('cmdb.preference.confirmcancelSub2', { name: `${this.$route.meta.title || this.$route.meta.name}` })
          "
          :ok-text="$t('confirm')"
          :cancel-text="$t('cancel')"
          @confirm="unsubscribe"
          placement="bottomRight"
        >
          <a-button size="small" icon="star" type="primary" ghost>{{ $t('cmdb.preference.cancelSub') }}</a-button>
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
            <span @click="$refs.create.handleOpen(true, 'update')">{{ $t('update') }}</span>
            <a-divider type="vertical" />
            <span @click="openBatchDownload">{{ $t('download') }}</span>
            <a-divider type="vertical" />
            <span @click="batchDelete">{{ $t('delete') }}</span>
            <span>{{ $t('cmdb.ci.selectRows', { rows: selectedRowKeys.length }) }}</span>
          </div>
        </SearchForm>
        <CiDetailDrawer ref="detail" :typeId="typeId" />
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
                :v-bind="$t('placeholder2')"
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
          <vxe-column align="left" field="operate" fixed="right" width="120">
            <template #header>
              <span>{{ $t('operation') }}</span>
              <EditAttrsPopover :typeId="typeId" class="operation-icon" @refresh="refreshAfterEditAttrs" />
              <!-- <a-icon class="operation-icon" type="control" /> -->
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
                <a @click="deleteCI(row)" :style="{ color: 'red' }">
                  <a-icon type="delete" />
                </a>
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
            :show-total="
              (total, range) =>
                $t('pagination.total', {
                  range0: range[0],
                  range1: range[1],
                  total,
                })
            "
            @change="
              (page) => {
                currentPage = page
              }
            "
          >
            <template slot="buildOptionText" slot-scope="props">
              <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
              <span v-if="props.value === '100000'">{{ $t('cmdb.ci.all') }}</span>
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
import CiDetailDrawer from './modules/ciDetailDrawer.vue'
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
    CiDetailDrawer,
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
      columns: [],
      // custom table alert & rowSelection
      selectedRowKeys: [],
      // Check whether to edit
      initialInstanceList: [],
      sortByTable: undefined,
      isEditActive: false,
      attrList: [],
      attributes: {},
      // Table drag parameters
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
    // window.onkeypress = (e) => {
    //   this.handleKeyPress(e)
    // }
    setTimeout(() => {
      this.columnDrop()
    }, 1000)
  },
  beforeDestroy() {
    // window.onkeypress = null
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
        // If fuzzy search is possible, queryParam can be deleted later.
        // const queryParams = this.$refs['search'].queryParam || {}
        const fuzzySearch = this.$refs['search'].fuzzySearch
        const expression = this.$refs['search'].expression || ''
        const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
        const regSort = /(?<=sort=).+/g

        const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
        let sort
        if (sortByTable) {
          sort = sortByTable
        } else {
          sort = expression.match(regSort) ? expression.match(regSort)[0] : undefined
        }
        const res = await searchCI({
          q: `_type:${this.typeId}${exp ? `,${exp}` : ''}${fuzzySearch ? `,*${fuzzySearch}*` : ''}`,
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
      this.preferenceAttrList = subscribed.attributes // All columns that have been subscribed
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
      this.isEditActive = false
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
          })
          .catch((err) => {
            console.log(err)
            this.loadTableData()
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
      this.$refs.batchDownload.open({
        preferenceAttrList: this.preferenceAttrList,
        ciTypeName: this.$route.meta.title || this.$route.meta.name,
      })
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
        title: that.$t('warning'),
        content: that.$t('cmdb.ci.batchUpdateConfirm'),
        async onOk() {
          that.batchUpdateAsync(values)
        },
      })
    },
    async batchUpdateAsync(values) {
      let successNum = 0
      let errorNum = 0
      this.loading = true
      this.loadTip = this.$t('cmdb.ci.batchUpdateInProgress') + '...'
      const payload = {}
      Object.keys(values).forEach((key) => {
        if (values[key] || values[key] === 0) {
          payload[key] = values[key]
        }
        // Field values support blanking
        // There are currently field values that do not support blanking and will be returned by the backend.
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
      this.selectedRowKeys = []
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
      this.reloadData()
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
        title: that.$t('warning'),
        content: that.$t('confirmDelete'),
        onOk() {
          deleteCI(record.ci_id || record._id).then((res) => {
            // that.$refs.table.refresh(true)
            that.$message.success(that.$t('deleteSuccess'))
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
      // The backend writes data at different speeds. You can modify the table data directly without pulling the interface.
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
      setTimeout(() => {
        // this.setSelectRows()
      }, 500)
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
    // tableFilterChangeEvent({ column, property, values, datas, filterList, $event }) {
    //   console.log(111)
    // },
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
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },
    unsubscribe(ciType, type = 'all') {
      const promises = [subscribeCIType(this.typeId, ''), subscribeTreeView(this.typeId, '')]
      Promise.all(promises).then(() => {
        const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
        if (Number(ciType) === Number(lastTypeId)) {
          localStorage.setItem('ops_ci_typeid', '')
        }
        this.$message.success(this.$t('cmdb.preference.cancelSubSuccess'))
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
          this.$message.error(this.$t('noPermission'))
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
