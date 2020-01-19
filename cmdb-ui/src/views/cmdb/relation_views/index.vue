<template>
  <a-card :bordered="false" class="relation-card">
    <a-menu v-model="currentView" mode="horizontal" v-if="relationViews.name2id && relationViews.name2id.length">
      <a-menu-item :key="item[1]" v-for="item in relationViews.name2id">
        <router-link
          :to="{name: 'cmdb_relation_views_item', params: { viewId: item[1]} }"
        >{{ item[0] }}</router-link>
      </a-menu-item>
    </a-menu>
    <a-alert message="管理员 还未配置关系视图, 或者你无权限访问!" banner v-else-if="relationViews.name2id && !relationViews.name2id.length"></a-alert>
    <div style="clear: both; margin-top: 20px"></div>
    <template>
      <a-row :gutter="8">
        <a-col :span="5">
          <a-tree showLine :loadData="onLoadData" @select="onSelect" :treeData="treeData"></a-tree>
        </a-col>
        <a-col :span="19">
          <a-menu v-model="currentTypeId" mode="horizontal" v-if="showTypeIds && showTypeIds.length > 1">
            <a-menu-item :key="item.id" v-for="item in showTypes">
              <a @click="changeCIType(item.id)">{{ item.alias || item.name }}</a>
            </a-menu-item>
          </a-menu>
          <search-form style="margin-top: 10px" ref="search" @refresh="refreshTable" :preferenceAttrList="preferenceAttrList" />
          <s-table
            v-if="levels.length"
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

import { getRelationView, getSubscribeAttributes } from '@/api/cmdb/preference'
import { searchCIRelation, statisticsCIRelation } from '@/api/cmdb/CIRelation'
import { searchCI } from '@/api/cmdb/ci'
import SearchForm from '@/views/cmdb/ci/modules/SearchForm'
export default {
  components: {
    STable,
    SearchForm
  },
  data () {
    return {
      parameter: {},
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
      currentView: [],
      currentTypeId: [],
      instanceList: [],
      treeKeys: [],
      columns: [],
      pageSizeOptions: ['10', '25', '50', '100'],
      loading: false,
      scrollX: 0,
      scrollY: 0,
      preferenceAttrList: [],

      loadInstances: async parameter => {
        console.log(parameter, 'load instances')
        this.parameter = parameter
        const params = Object.assign(parameter || {}, this.$refs.search.queryParam)
        let q = ''
        Object.keys(params).forEach(key => {
          if (!['pageNo', 'pageSize', 'sortField', 'sortOrder'].includes(key) && params[key] + '' !== '') {
            if (typeof params[key] === 'object' && params[key] && params[key].length > 1) {
              q += `,${key}:(${params[key].join(';')})`
            } else if (params[key]) {
              q += `,${key}:*${params[key]}*`
            }
          }
        })
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
        if (q && q[0] === ',') {
          q = q.slice(1)
        }
        if (this.treeKeys.length === 0) {
          await this.judgeCITypes(q)
          q = `q=_type:${this.currentTypeId[0]},` + q
          return searchCI(q).then(res => {
            const result = {}
            result.pageNo = res.page
            result.pageSize = res.total
            result.totalCount = res.numfound
            result.totalPage = Math.ceil(res.numfound / (params.pageSize || 25))
            result.data = Object.assign([], res.result)
            result.data.forEach((item, index) => (item.key = item.ci_id))
            if (res.numfound !== 0) {
              setTimeout(() => {
                this.setColumnWidth()
                console.log('set column')
              }, 200)
            }
            this.loadRoot()
            return result
          })
        }

        q += `&root_id=${this.treeKeys[this.treeKeys.length - 1].split('_')[0]}`
        const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('_')[1])

        let level = []
        if (!this.leaf.includes(typeId)) {
          let startIdx = 0
          this.levels.forEach((item, idx) => {
            if (item.includes(typeId)) {
              startIdx = idx
            }
          })

          this.leaf.forEach(leafId => {
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
        await this.judgeCITypes(q)
        q = `q=_type:${this.currentTypeId[0]},` + q
        return searchCIRelation(q).then(res => {
          const result = {}
          result.pageNo = res.page
          result.pageSize = res.total
          result.totalCount = res.numfound
          result.totalPage = Math.ceil(res.numfound / (params.pageSize || 25))
          result.data = Object.assign([], res.result)
          result.data.forEach((item, index) => (item.key = item.ci_id))
          if (res.numfound !== 0) {
            setTimeout(() => {
              this.setColumnWidth()
              console.log('set column')
            }, 200)
          }
          this.loadNoRoot(this.treeKeys[this.treeKeys.length - 1], level)
          return result
        })
      }
    }
  },

  created () {
    this.getRelationViews()
  },

  inject: ['reload'],
  watch: {
    '$route.path': function (newPath, oldPath) {
      this.viewId = this.$route.params.viewId
      this.getRelationViews()
      this.reload()
    }
  },

  methods: {
    refreshTable (bool = false) {
      this.$refs.table.refresh(bool)
    },

    changeCIType (typeId) {
      this.currentTypeId = [typeId]
      this.loadColumns(typeId)
      this.$refs.table.renderClear()
      setTimeout(() => {
        this.refreshTable(true)
      }, 200)
    },

    async judgeCITypes (q) {
      const showTypeIds = []
      let _showTypes = []
      let _showTypeIds = []

      if (this.treeKeys.length) {
        const typeId = parseInt(this.treeKeys[this.treeKeys.length - 1].split('_')[1])

        _showTypes = this.node2ShowTypes[typeId + '']
        _showTypes.forEach(item => {
          _showTypeIds.push(item.id)
        })
      } else {
        _showTypeIds = JSON.parse(JSON.stringify(this.origShowTypeIds))
        _showTypes = JSON.parse(JSON.stringify(this.origShowTypes))
      }

      const promises = _showTypeIds.map(typeId => {
        const _q = (`q=_type:${typeId},` + q).replace(/count=\d*/, 'count=1')
        if (this.treeKeys.length === 0) {
          return searchCI(_q).then(res => {
            if (res.numfound !== 0) {
              showTypeIds.push(typeId)
            }
          })
        } else {
          return searchCIRelation(_q).then(res => {
            if (res.numfound !== 0) {
              showTypeIds.push(typeId)
            }
          })
        }
      })
      await Promise.all(promises)
      if (showTypeIds.length && showTypeIds.sort().join(',') !== this.showTypeIds.sort().join(',')) {
        const showTypes = []
        _showTypes.forEach(item => {
          if (showTypeIds.includes(item.id)) {
            showTypes.push(item)
          }
        })
        this.showTypes = showTypes
        this.showTypeIds = showTypeIds
        if (!this.currentTypeId.length || (this.currentTypeId.length && !this.showTypeIds.includes(this.currentTypeId[0]))) {
          this.currentTypeId = [this.showTypeIds[0]]
          this.loadColumns()
        }
      }
    },

    async loadRoot () {
      searchCI(`q=_type:(${this.levels[0].join(';')})&count=10000`).then(async res => {
        const facet = []
        const ciIds = []
        res.result.forEach(item => {
          facet.push([item[item.unique], 0, item.ci_id, item.type_id])
          ciIds.push(item.ci_id)
        })
        const promises = this.leaf.map(leafId => {
          let level = 0
          this.levels.forEach((item, idx) => {
            if (item.includes(leafId)) {
              level = idx + 1
            }
          })
          return statisticsCIRelation({ root_ids: ciIds.join(','), level: level }).then(num => {
            facet.forEach((item, idx) => {
              item[1] += num[ciIds[idx] + '']
            })
          })
        })
        await Promise.all(promises)
        this.wrapTreeData(facet)
      })
    },

    async loadNoRoot (rootIdAndTypeId, level) {
      const rootId = rootIdAndTypeId.split('_')[0]
      searchCIRelation(`root_id=${rootId}&level=1&count=10000`).then(async res => {
        const facet = []
        const ciIds = []
        res.result.forEach(item => {
          facet.push([item[item.unique], 0, item.ci_id, item.type_id])
          ciIds.push(item.ci_id)
        })

        const promises = level.map(_level => {
          if (_level > 1) {
            return statisticsCIRelation({ root_ids: ciIds.join(','), level: _level - 1 }).then(num => {
              facet.forEach((item, idx) => {
                item[1] += num[ciIds[idx] + '']
              })
            })
          }
        })
        await Promise.all(promises)
        this.wrapTreeData(facet)
      })
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
      facet.forEach(item => {
        treeData.push({
          title: `${item[0]} (${item[1]})`,
          key: this.treeKeys.join('-') + '-' + item[2] + '_' + item[3],
          isLeaf: this.leaf.includes(item[3])
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

    getRelationViews () {
      getRelationView().then(res => {
        this.relationViews = res

        if ((Object.keys(this.relationViews.views) || []).length) {
          this.viewId = parseInt(this.$route.params.viewId) || this.relationViews.name2id[0][1]
          this.relationViews.name2id.forEach(item => {
            if (item[1] === this.viewId) {
              this.viewName = item[0]
            }
          })
          this.levels = this.relationViews.views[this.viewName].topo
          this.origShowTypes = this.relationViews.views[this.viewName].show_types
          const showTypeIds = []
          this.origShowTypes.forEach(item => {
            showTypeIds.push(item.id)
          })
          this.origShowTypeIds = showTypeIds
          this.leaf2showTypes = this.relationViews.views[this.viewName].leaf2show_types
          this.node2ShowTypes = this.relationViews.views[this.viewName].node2show_types
          this.leaf = this.relationViews.views[this.viewName].leaf
          this.currentView = [this.viewId]
          this.typeId = this.levels[0][0]
          this.$refs.table && this.$refs.table.refresh(true)
        }
      })
    },
    loadColumns () {
      getSubscribeAttributes(this.currentTypeId[0]).then(res => {
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

<style lang='less'>
.ant-menu-horizontal {
  border-bottom: 1px solid #ebedf0 !important;
}
.ant-menu-horizontal {
  border-bottom: 1px solid #ebedf0 !important;
}
.relation-card > .ant-card-body {
  padding-top: 0 !important;
}
</style>
