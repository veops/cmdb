<template>
  <a-card :bordered="false">
    <a-spin :tip="loadTip" :spinning="loading">
      <search-form ref="search" @refresh="refreshTable" :preferenceAttrList="preferenceAttrList" />

      <ci-detail ref="detail" :typeId="typeId" />

      <div class="table-operator">
        <a-button
          type="primary"
          icon="plus"
          @click="$refs.create.visible = true; $refs.create.action='create'"
        >新建</a-button>
        <a-dropdown v-action:edit v-if="selectedRowKeys.length > 0">
          <a-menu slot="overlay">
            <a-menu-item
              key="batchUpdate"
              @click="$refs.create.visible = true; $refs.create.action='update'"
            >
              <span @click="$refs.create.visible = true">
                <a-icon type="edit" />&nbsp;修改
              </span>
            </a-menu-item>
            <a-menu-item key="batchDownload" @click="batchDownload">
              <json-excel :fetch="batchDownload" name="cmdb.xls">
                <a-icon type="download" />&nbsp;下载
              </json-excel>
            </a-menu-item>
            <a-menu-item key="batchDelete" @click="batchDelete">
              <a-icon type="delete" />删除
            </a-menu-item>
          </a-menu>
          <a-button style="margin-left: 8px">
            批量操作
            <a-icon type="down" />
          </a-button>
        </a-dropdown>
      </div>
      <s-table
        bordered
        ref="table"
        size="middle"
        rowKey="ci_id"
        :columns="columns"
        :data="loadInstances"
        :alert="options.alert"
        :rowSelection="options.rowSelection"
        :scroll="{ x: scrollX, y: scrollY }"
        :pagination="{ showTotal: (total, range) => `${range[0]}-${range[1]} 共 ${total} 条记录`, pageSizeOptions: pageSizeOptions}"
        showPagination="auto"
        :pageSize="25"
      >
        <template :slot="col.dataIndex" slot-scope="text, record" v-for="col in columns">
          <editable-cell
            :key="'edit_' + col.dataIndex"
            :text="text"
            @change="onCellChange(record.key, col.dataIndex, $event, record[col.dataIndex])"
          />
        </template>

        <span slot="action" slot-scope="text, record">
          <template>
            <a
              @click="$refs.detail.visible = true; $refs.detail.ciId = record.key; $refs.detail.create()"
            >详情</a>

            <a-divider type="vertical" />
            <a @click="deleteCI(record)">删除</a>
          </template>
        </span>
      </s-table>

      <create-instance-form @refresh="refreshTable" ref="create" @submit="batchUpdate" />
    </a-spin>
  </a-card>
</template>

<script>
import { setTimeout } from 'timers'
import { STable } from '@/components'
import JsonExcel from 'vue-json-excel'

import SearchForm from './modules/SearchForm'
import CreateInstanceForm from './modules/CreateInstanceForm'
import EditableCell from './modules/EditableCell'
import CiDetail from './modules/CiDetail'
import { searchCI, updateCI, deleteCI } from '@/api/cmdb/ci'
import { getSubscribeAttributes } from '@/api/cmdb/preference'
import { notification } from 'ant-design-vue'

var valueTypeMap = {
  '0': 'int',
  '1': 'float',
  '2': 'text',
  '3': 'datetime',
  '4': 'date',
  '5': 'time',
  '6': 'json'
}

export default {
  name: 'InstanceList',
  components: {
    STable,
    EditableCell,
    JsonExcel,
    SearchForm,
    CreateInstanceForm,
    CiDetail
  },
  data () {
    return {
      loading: false,
      loadTip: '',
      pageSizeOptions: ['10', '25', '50', '100'],
      form: this.$form.createForm(this),
      valueTypeMap: valueTypeMap,
      mdl: {},
      typeId: this.$router.currentRoute.meta.typeId,

      scrollX: 0,
      scrollY: 0,

      preferenceAttrList: [],

      instanceList: [],
      // 表头
      columns: [],
      // 加载数据方法 必须为 Promise 对象
      loadInstances: parameter => {
        const params = Object.assign(parameter, this.$refs.search.queryParam)
        let q = `q=_type:${this.$router.currentRoute.meta.typeId}`
        Object.keys(params).forEach(key => {
          if (!['pageNo', 'pageSize', 'sortField', 'sortOrder'].includes(key) && params[key] + '' !== '') {
            if (typeof params[key] === 'object' && params[key] && params[key].length > 1) {
              q += `,${key}:(${params[key].join(';')})`
            } else if (params[key]) {
              q += `,${key}:*${params[key]}*`
            }
          }
        })
        q += `&page=${params['pageNo']}&count=${params['pageSize']}`
        if ('sortField' in params) {
          let order = ''
          if (params['sortOrder'] !== 'ascend') {
            order = '-'
          }
          q += `&sort=${order}${params['sortField']}`
        }

        return searchCI(q).then(res => {
          const result = {}
          result.pageNo = res.page
          result.pageSize = res.total
          result.totalCount = res.numfound
          result.totalPage = Math.ceil(res.numfound / params.pageSize)
          result.data = Object.assign([], res.result)
          result.data.forEach((item, index) => (item.key = item.ci_id))
          if (res.numfound) {
            setTimeout(() => {
              this.setColumnWidth()
            }, 200)
          }
          this.instanceList = result.data
          return result
        })
      },
      // custom table alert & rowSelection
      selectedRowKeys: [],
      selectedRows: [],
      options: {
        alert: {
          show: true,
          clear: () => {
            this.selectedRowKeys = []
          }
        },
        rowSelection: {
          selectedRowKeys: this.selectedRowKeys,
          onChange: this.onSelectChange,
          columnWidth: 62,
          fixed: true
        }
      },
      optionAlertShow: false,
      watch: {
        '$route.path': function (newPath, oldPath) {
          this.reload()
        }
      }
    }
  },

  created () {
    this.tableOption()
    this.loadColumns()
  },
  watch: {
    '$route.path': function (newPath, oldPath) {
      this.reload()
    }
  },
  inject: ['reload'],
  methods: {
    setColumnWidth () {
      let rows = []
      try {
        rows = document.querySelector('.ant-table-body').childNodes[0].childNodes[2].childNodes[0].childNodes
      } catch (e) {
        rows = document.querySelector('.ant-table-body').childNodes[0].childNodes[1].childNodes[0].childNodes
      }
      let scrollX = 0

      const columns = Object.assign([], this.columns)
      for (let i = 1; i < rows.length - 1; i++) {
        columns[i - 1].width = rows[i].offsetWidth < 100 ? 100 : rows[i].offsetWidth
        scrollX += columns[i - 1].width
      }
      this.columns = columns

      this.scrollX =
        scrollX +
        document.querySelector('.ant-table-fixed-left').offsetWidth +
        document.querySelector('.ant-table-fixed-right').offsetWidth
      this.scrollY = window.innerHeight - this.$refs.table.$el.offsetTop - 300
    },
    tableOption () {
      if (!this.optionAlertShow) {
        this.options = {
          alert: {
            show: true,
            clear: () => {
              this.selectedRowKeys = []
            }
          },
          rowSelection: {
            selectedRowKeys: this.selectedRowKeys,
            onChange: this.onSelectChange,
            getCheckboxProps: record => ({
              props: {
                disabled: record.no === 'No 2', // Column configuration not to be checked
                name: record.no
              }
            }),
            columnWidth: 62,
            fixed: true
          }
        }
        this.optionAlertShow = true
      } else {
        alert('no alert')
        this.options = {
          alert: false,
          rowSelection: null
        }
        this.optionAlertShow = false
      }
    },

    loadColumns () {
      getSubscribeAttributes(this.$router.currentRoute.meta.typeId).then(res => {
        const prefAttrList = res.attributes
        this.preferenceAttrList = prefAttrList

        const columns = []
        prefAttrList.forEach((item, index) => {
          const col = {}
          col.title = item.alias
          col.dataIndex = item.name
          col.value_type = item.value_type
          if (index !== prefAttrList.length - 1) {
            col.width = 100
          }
          if (item.is_sortable) {
            col.sorter = true
          }
          if (item.is_choice) {
            const filters = []
            item.choice_value.forEach(item => filters.push({ text: item, value: item }))
            col.filters = filters
          }
          col.scopedSlots = { customRender: item.name }
          columns.push(col)
        })

        columns.push({
          title: '操作',
          key: 'operation',
          width: 100,
          fixed: 'right',
          scopedSlots: { customRender: 'action' }
        })
        this.columns = columns
      })
    },

    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },

    refreshTable (bool = false) {
      this.$refs.table.refresh(bool)
    },

    onCellChange (key, dataIndex, event, oldValue) {
      const value = event[0]
      const payload = {}
      payload[dataIndex] = value
      updateCI(key, payload)
        .then(res => {
          event[1].x = false
        })
        .catch(err => {
          notification.error({
            message: err.response.data.message
          })
        })
    },
    async batchDownload () {
      this.loading = true
      this.loadTip = '正在下载 ...'
      const promises = this.selectedRowKeys.map(ciId => {
        return searchCI(`q=_id:${ciId}`).then(res => {
          const ciMap = {}
          Object.keys(res.result[0]).forEach(k => {
            if (!['ci_type', 'ci_id', 'ci_type_alias', 'type_id'].includes(k)) {
              ciMap[k] = res.result[0][k]
            }
          })
          return ciMap
        })
      })
      const results = await Promise.all(promises)
      this.loading = false
      this.$refs.table.clearSelected()

      return results
    },
    batchUpdate (values) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认要批量修改吗 ?',
        onOk () {
          that.loading = true
          that.loadTip = '正在批量修改 ...'
          const payload = {}
          Object.keys(values).forEach(key => {
            if (values[key] || values[key] === 0) {
              payload[key] = values[key]
            }
          })
          const promises = that.selectedRowKeys.map(ciId => {
            return updateCI(ciId, payload).then(res => {
              return 'ok'
            })
          })
          Promise.all(promises)
            .then(res => {
              that.loading = false
              notification.success({
                message: '批量修改成功'
              })
              that.$refs.create.visible = false

              that.$refs.table.clearSelected()
              setTimeout(() => {
                that.$refs.table.refresh(true)
              }, 1000)
              that.reload()
            })
            .catch(e => {
              console.log(e)
              that.loading = false
              notification.error({
                message: e.response.data.message
              })
              setTimeout(() => {
                that.$refs.table.refresh(true)
              }, 1000)
            })
        }
      })
    },
    batchDelete () {
      const that = this
      this.$confirm({
        title: '警告',
        content: '真的要删除吗 ?',
        onOk () {
          that.loading = true
          that.loadTip = '正在删除 ...'
          const promises = that.selectedRowKeys.map(ciId => {
            return deleteCI(ciId).then(res => {
              return 'ok'
            })
          })
          Promise.all(promises)
            .then(res => {
              that.loading = false
              notification.success({
                message: '删除成功'
              })
              that.$refs.table.clearSelected()
              setTimeout(() => {
                that.$refs.table.refresh(true)
              }, 1500)
            })
            .catch(e => {
              console.log(e)
              that.loading = false
              notification.error({
                message: e.response.data.message
              })
              setTimeout(() => {
                that.$refs.table.refresh(true)
              }, 1000)
            })
        }
      })
    },
    deleteCI (record) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '真的要删除吗 ?',
        onOk () {
          deleteCI(record.key)
            .then(res => {
              setTimeout(() => {
                that.$refs.table.refresh(true)
              }, 1000)
            })
            .catch(e => {
              console.log(e)
              notification.error({
                message: e.response.data.message
              })
            })
        }
      })
    }
  }
}
</script>

<style>
.ant-table-thead > tr > th,
.ant-table-tbody > tr > td {
  white-space: nowrap;
  overflow: hidden;
}
.spin-content {
  border: 1px solid #91d5ff;
  background-color: #e6f7ff;
  padding: 30px;
}
</style>
