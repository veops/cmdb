<template>
  <a-card :bordered="false">
    <a-menu v-model="current" mode="horizontal" v-if="ciTypes && ciTypes.length">
      <a-menu-item :key="ciType.id" v-for="ciType in ciTypes">
        <router-link
          :to="{name: 'cmdb_tree_views_item', params: {typeId: ciType.id}}"
        >{{ ciType.alias || ciTypes.name }}</router-link>
      </a-menu-item>
    </a-menu>
    <a-alert message="请先到 我的订阅 页面完成订阅!" banner v-else-if="ciTypes && !ciTypes.length"></a-alert>
    <div style="clear: both; margin-top: 20px"></div>
    <template>
      <a-row :gutter="8">
        <a-col :span="5">
          <a-tree showLine :loadData="onLoadData" @select="onSelect" :treeData="treeData"></a-tree>
        </a-col>
        <a-col :span="19">
          <search-form ref="search" @refresh="refreshTable" :preferenceAttrList="preferenceAttrList" />
          <s-table
            v-if="ciTypes && ciTypes.length"
            bordered
            ref="table"
            size="middle"
            rowKey="ci_id"
            :columns="columns"
            :data="loadInstances"
            :scroll="{ x: scrollX, y: scrollY }"
            :pagination="{ showTotal: (total, range) => `${range[0]}-${range[1]} 共 ${total} 条记录`, pageSizeOptions: pageSizeOptions}"
            :pageSize="25"
            showPagination="auto"
          ></s-table>
        </a-col>
      </a-row>
    </template>
  </a-card>
</template>

<script>
import { STable } from '@/components'

import { getSubscribeTreeView, getSubscribeAttributes } from '@/api/cmdb/preference'
import { searchCI } from '@/api/cmdb/ci'
import SearchForm from '@/views/cmdb/ci/modules/SearchForm'
export default {
  components: {
    STable,
    SearchForm
  },
  data () {
    return {
      treeData: [],
      triggerSelect: false,
      treeNode: null,
      ciTypes: null,
      levels: [],
      typeId: null,
      current: [],
      instanceList: [],
      treeKeys: [],
      columns: [],
      pageSizeOptions: ['10', '25', '50', '100'],
      loading: false,
      scrollX: 0,
      scrollY: 0,
      preferenceAttrList: [],

      loadInstances: parameter => {
        const params = Object.assign(parameter || {}, this.$refs.search.queryParam)
        let q = `q=_type:${this.typeId}`
        Object.keys(params).forEach(key => {
          if (!['pageNo', 'pageSize', 'sortField', 'sortOrder'].includes(key) && params[key] + '' !== '') {
            if (typeof params[key] === 'object' && params[key].length > 1) {
              q += `,${key}:(${params[key].join(';')})`
            } else if (params[key]) {
              q += `,${key}:${params[key]}`
            }

            if (typeof params[key] === 'string') {
              q += '*'
            }
          }
        })

        if (this.treeKeys.length > 0) {
          this.treeKeys.forEach((item, idx) => {
            q += `,${this.levels[idx].name}:${item}`
          })
        }

        if (this.levels.length > this.treeKeys.length) {
          q += `&facet=${this.levels[this.treeKeys.length].name}`
        }

        if ('pageNo' in params) {
          q += `&page=${params['pageNo']}&count=${params['pageSize']}`
        }

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
          result.totalPage = Math.ceil(res.numfound / (params.pageSize || 25))
          result.data = Object.assign([], res.result)
          result.data.forEach((item, index) => (item.key = item.ci_id))
          setTimeout(() => {
            this.setColumnWidth()
          }, 200)

          if (Object.values(res.facet).length) {
            this.wrapTreeData(res.facet)
          }

          return result
        })
      }
    }
  },

  created () {
    this.getCITypes()
  },

  inject: ['reload'],
  watch: {
    '$route.path': function (newPath, oldPath) {
      this.typeId = this.$route.params.typeId
      this.getCITypes()
      this.reload()
    }
  },

  methods: {
    refreshTable (bool = false) {
      this.$refs.table.refresh(bool)
    },

    onSelect (keys) {
      this.triggerSelect = true
      if (keys.length) {
        this.treeKeys = keys[0].split('-').filter(item => item !== '')
      }

      this.$refs.table.refresh(true)
    },
    wrapTreeData (facet) {
      if (this.triggerSelect) {
        return
      }
      const treeData = []
      Object.values(facet)[0].forEach(item => {
        treeData.push({
          title: `${item[0]} (${item[1]})`,
          key: this.treeKeys.join('-') + '-' + item[0],
          isLeaf: this.levels.length - 1 === this.treeKeys.length
        })
      })
      if (this.treeNode === null) {
        this.treeData = treeData
      } else {
        this.treeNode.dataRef.children = treeData
        this.treeData = [...this.treeData]
      }
    },
    setColumnWidth () {
      let rows = []
      try {
        rows = document.querySelector('.ant-table-body').childNodes[0].childNodes[2].childNodes[0].childNodes
      } catch (e) {
        rows = document.querySelector('.ant-table-body').childNodes[0].childNodes[1].childNodes[0].childNodes
      }
      let scrollX = 0

      const columns = Object.assign([], this.columns)
      for (let i = 0; i < rows.length; i++) {
        columns[i].width = rows[i].offsetWidth < 80 ? 80 : rows[i].offsetWidth
        scrollX += columns[i].width
      }
      this.columns = columns

      this.scrollX = scrollX
      this.scrollY = window.innerHeight - this.$refs.table.$el.offsetTop - 300
    },

    onLoadData (treeNode) {
      this.triggerSelect = false
      return new Promise(resolve => {
        if (treeNode.dataRef.children) {
          resolve()
          return
        }
        this.treeKeys = treeNode.eventKey.split('-').filter(item => item !== '')
        this.treeNode = treeNode
        this.$refs.table.refresh(true)
        resolve()
      })
    },

    getCITypes () {
      getSubscribeTreeView().then(res => {
        this.ciTypes = res
        if (this.ciTypes.length) {
          this.typeId = this.$route.params.typeId || this.ciTypes[0].id
          this.current = [this.typeId]
          this.loadColumns()
          this.levels = res.find(item => item.id === this.typeId).levels
          this.$refs.table && this.$refs.table.refresh(true)
        }
      })
    },
    loadColumns () {
      getSubscribeAttributes(this.typeId).then(res => {
        const prefAttrList = res.attributes
        this.preferenceAttrList = prefAttrList

        const columns = []
        prefAttrList.forEach((item, index) => {
          const col = {}
          col.title = item.alias
          col.dataIndex = item.name
          if (index !== prefAttrList.length - 1) {
            col.width = 80
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

        this.columns = columns
      })
    }
  }
}
</script>

<style scoped>
.ant-menu-horizontal {
  border-bottom: 1px solid #ebedf0 !important;
}
.ant-menu-horizontal {
  border-bottom: 1px solid #ebedf0 !important;
}
</style>
