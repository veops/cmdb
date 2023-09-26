<template>
  <div>
    <search-form
      ref="child"
      :attrList="ciTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
      @searchFormChange="searchFormChange"
    ></search-form>
    <vxe-table
      ref="xTable"
      row-id="_XID"
      :loading="loading"
      border
      size="small"
      show-overflow="tooltip"
      show-header-overflow="tooltip"
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightMinus}px`"
      :span-method="mergeRowMethod"
      :scroll-y="{enabled: false}"
      class="ops-unstripe-table"
    >
      <vxe-column field="created_at" width="159px" title="操作时间"></vxe-column>
      <vxe-column field="user" width="100px" title="用户">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon class="filter" type="filter" theme="filled"/>
            <a slot="content">
              <a-input placeholder="输入筛选用户名" size="small" v-model="queryParams.username" style="width: 200px" allowClear/>
              <a-button type="link" class="filterButton" @click="filterUser">筛选</a-button>
              <a-button type="link" class="filterResetButton" @click="filterUserReset">重置</a-button>
            </a>
          </a-popover>
        </template>
      </vxe-column>
      <vxe-column field="type_id" width="100px" title="模型"></vxe-column>
      <vxe-column field="operate_type" width="89px" title="操作">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon class="filter" type="filter" theme="filled"/>
            <a slot="content">
              <a-select
                v-model="queryParams.operate_type"
                placeholder="选择筛选操作"
                show-search
                style="width: 200px"
                :filter-option="filterOption"
                allowClear
              >
                <a-select-option
                  :value="Object.values(choice)[0]"
                  :key="index"
                  v-for="(choice, index) in ciTableAttrList[4].choice_value"
                >
                  {{ Object.keys(choice)[0] }}
                </a-select-option
                >
              </a-select>
              <a-button type="link" class="filterButton" @click="filterOperate">筛选</a-button>
              <a-button type="link" class="filterResetButton" @click="filterOperateReset">重置</a-button>
            </a>
          </a-popover>
        </template>
        <template #default="{ row }">
          <a-tag color="green" v-if="row.operate_type === '新增' ">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="orange" v-else-if="row.operate_type === '修改' ">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="red" v-else>
            {{ row.operate_type }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="attr_alias" title="属性"></vxe-column>
      <vxe-column field="old" title="旧"></vxe-column>
      <vxe-column field="new" title="新"></vxe-column>
    </vxe-table>
    <pager
      :current-page.sync="queryParams.page"
      :page-size.sync="queryParams.page_size"
      :page-sizes="[50,100,200]"
      :total="total"
      :isLoading="loading"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
    ></pager>
  </div>
</template>
<script>
import Pager from './pager.vue'
import SearchForm from './searchForm.vue'
import { getCIHistoryTable, getUsers } from '@/modules/cmdb/api/history'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
export default {
  name: 'CiTable',
  components: { SearchForm, Pager },
  data() {
    return {
      typeId: undefined,
      operateTypeMap: new Map([
        ['0', '新增'],
        ['1', '删除'],
        ['2', '修改'],
      ]),
      loading: true,
      typeList: null,
      userList: [],
      tableData: [],
      total: 0,
      isExpand: false,
      queryParams: {
        page: 1,
        page_size: 50,
      },
      ciTableAttrList: [
        {
          alias: '日期',
          is_choice: false,
          name: 'datetime',
          value_type: '3'
        },
        {
          alias: '用户',
          is_choice: true,
          name: 'username',
          value_type: '2',
          choice_value: []
        },
        {
          alias: '模型',
          is_choice: true,
          name: 'type_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: '属性',
          is_choice: true,
          name: 'attr_id',
          value_type: '2',
          choice_value: []
        },
        {
          alias: '操作',
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { '新增': 0 },
            { '删除': 1 },
            { '修改': 2 },
          ]
        },
        {
          alias: 'CI_ID',
          is_choice: false,
          name: 'ci_id',
          value_type: '2'
        }
      ],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowHeightMinus() {
      return this.isExpand ? 396 : 331
    }
  },
  async created() {
    this.$watch(
      function () {
        return this.ciTableAttrList[3].choice_value
      },
      function () {
        delete this.$refs.child.queryParams.attr_id
      }
    )
    await Promise.all([
      this.getUserList(),
      this.getTypes()
    ])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  methods: {
    // 获取表格数据
    async getTable(queryParams) {
      try {
        this.loading = true
        const res = await getCIHistoryTable(queryParams)
        const tempArr = []
        res.records.forEach(item => {
          item[0].type_id = this.handleTypeId(item[0].type_id)
          item[1].forEach((subItem) => {
            subItem.operate_type = this.handleOperateType(subItem.operate_type)
            const tempObj = Object.assign(subItem, item[0])
            tempArr.push(tempObj)
          })
        })
        this.tableData = tempArr
        this.total = res.total
      } finally {
        this.loading = false
      }
    },
    // 获取用户列表
    async getUserList() {
      const res = await getUsers()
      this.userList = res.map(x => {
        const username = x.nickname
        const obj = {
          [username]: username
        }
        return obj
      })
      this.ciTableAttrList[1].choice_value = this.userList
    },
    // 获取模型
    async getTypes() {
      const res = await getCITypes()
      const typesArr = []
      const typesMap = new Map()
      res.ci_types.forEach(item => {
        const tempObj = {}
        tempObj[item.alias] = item.id
        if (item.alias) {
          typesArr.push(tempObj)
          typesMap.set(item.id, item.alias)
        }
      })
      this.typeList = typesMap
      this.ciTableAttrList[2].choice_value = typesArr
    },
    // 获取模型对应属性
    async getAttrs(type_id) {
      if (!type_id) {
        this.ciTableAttrList[3].choice_value = []
        return
      }
      const res = await getCITypeAttributesById(type_id)
      const attrsArr = []
      res.attributes.forEach(item => {
        const tempObj = {}
        tempObj[item.alias] = item.id
        if (item.alias) {
          attrsArr.push(tempObj)
        }
      })
      this.ciTableAttrList[3].choice_value = attrsArr
    },
    onShowSizeChange(size) {
      this.queryParams.page_size = size
      this.queryParams.page = 1
      this.getTable(this.queryParams)
    },
    onChange(pageNum) {
      this.queryParams.page = pageNum
      this.getTable(this.queryParams)
    },
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    // 处理查询
    handleSearch(queryParams) {
      this.queryParams = queryParams
      this.getTable(this.queryParams)
    },
    // 重置表单
    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: 50,
        start: '',
        end: '',
        username: '',
        ci_id: undefined,
        attr_id: undefined,
        operate_type: undefined
      }
      // 将属性options重置
      this.ciTableAttrList[3].choice_value = []
      this.getTable(this.queryParams)
    },
    // 转换operate_type
    handleOperateType(operate_type) {
      return this.operateTypeMap.get(operate_type)
    },
    // 转换type_id
    handleTypeId(type_id) {
      return this.typeList.get(type_id) ? this.typeList.get(type_id) : type_id
    },
    // 表单改变，重新获取属性列表
    searchFormChange(queryParams) {
      if (this.typeId !== queryParams.type_id) {
        this.typeId = queryParams.type_id
        this.getAttrs(queryParams.type_id)
      }
      if (queryParams.type_id === undefined) {
        this.typeId = undefined
        this.$refs.child.queryParams.attr_id = undefined
      }
    },
    // 合并表格
    mergeRowMethod ({ row, _rowIndex, column, visibleData }) {
      const fields = ['created_at', 'user', 'type_id']
      // 单元格值 = 行[列.属性] 确定一格
      const cellValue = row[column.property]
      const created_at = row['created_at']
      // 如果单元格值不为空且作用域包含当前列
      if (column.property === 'created_at') {
        if (cellValue && fields.includes(column.property)) {
          // 前一行
          const prevRow = visibleData[_rowIndex - 1]
          // 下一行
          let nextRow = visibleData[_rowIndex + 1]
          // 如果前一行不为空且前一行单元格的值与cellValue相同
          if (prevRow && prevRow[column.property] === cellValue) {
            return { rowspan: 0, colspan: 0 }
          } else {
            let countRowspan = 1
            while (nextRow && nextRow[column.property] === cellValue) {
              nextRow = visibleData[++countRowspan + _rowIndex]
            }
            if (countRowspan > 1) {
              return { rowspan: countRowspan, colspan: 1 }
            }
          }
        }
      } else if (column.property === 'user') {
        if (cellValue && fields.includes(column.property)) {
          // 前一行
          const prevRow = visibleData[_rowIndex - 1]
          // 下一行
          let nextRow = visibleData[_rowIndex + 1]
          // 如果前一行不为空且前一行单元格的值与cellValue相同
          if (prevRow && prevRow[column.property] === cellValue && prevRow['created_at'] === created_at) {
            return { rowspan: 0, colspan: 0 }
          } else {
            let countRowspan = 1
            while (nextRow && nextRow[column.property] === cellValue && nextRow['created_at'] === created_at) {
              nextRow = visibleData[++countRowspan + _rowIndex]
            }
            if (countRowspan > 1) {
              return { rowspan: countRowspan, colspan: 1 }
            }
          }
        }
      } else if (column.property === 'type_id') {
        if (cellValue && fields.includes(column.property)) {
          // 前一行
          const prevRow = visibleData[_rowIndex - 1]
          // 下一行
          let nextRow = visibleData[_rowIndex + 1]
          // 如果前一行不为空且前一行单元格的值与cellValue相同
          if (prevRow && prevRow[column.property] === cellValue && prevRow['created_at'] === created_at) {
            return { rowspan: 0, colspan: 0 }
          } else {
            let countRowspan = 1
            while (nextRow && nextRow[column.property] === cellValue && nextRow['created_at'] === created_at) {
              nextRow = visibleData[++countRowspan + _rowIndex]
            }
            if (countRowspan > 1) {
              return { rowspan: countRowspan, colspan: 1 }
            }
          }
        }
      }
    },
    filterUser() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.getTable(this.queryParams)
    },
    filterUserReset() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.queryParams.username = ''
      this.getTable(this.queryParams)
    },
    filterOperate() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.getTable(this.queryParams)
    },
    filterOperateReset() {
      this.queryParams.page = 1
      this.queryParams.page_size = 50
      this.queryParams.operate_type = undefined
      this.getTable(this.queryParams)
    },
    filterOption(input, option) {
      return (
        option.componentOptions.children[0].text.indexOf(input) >= 0
      )
    }
  }
}
</script>

<style lang="less" scoped>
.filter{
  margin-left: 10px;
  color: #c0c4cc;
  cursor: pointer;
  &:hover{
    color: #606266;
  }
}
</style>
