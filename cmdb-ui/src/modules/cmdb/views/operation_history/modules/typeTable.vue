<template>
  <div>
    <search-form
      :attrList="typeTableAttrList"
      @expandChange="handleExpandChange"
      @search="handleSearch"
      @searchFormReset="searchFormReset"
    ></search-form>
    <vxe-table
      ref="xTable"
      :loading="loading"
      border
      resizable
      :data="tableData"
      :max-height="`${windowHeight - windowHeightMinus}px`"
      row-id="_XID"
      size="small"
      :row-config="{isHover: true}"
    >
      <vxe-column field="created_at" width="159px" title="操作时间"></vxe-column>
      <vxe-column field="user" width="116px" title="用户"></vxe-column>
      <vxe-column field="operate_type" width="135px" title="操作">
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-popover trigger="click" placement="bottom">
            <a-icon class="filter" type="filter" theme="filled" />
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
                  v-for="(choice, index) in typeTableAttrList[1].choice_value"
                >
                  {{ Object.keys(choice)[0] }}
                </a-select-option>
              </a-select>
              <a-button type="link" class="filterButton" @click="filterOperate">筛选</a-button>
              <a-button type="link" class="filterResetButton" @click="filterOperateReset">重置</a-button>
            </a>
          </a-popover>
        </template>
        <template #default="{ row }">
          <a-tag color="green" v-if="row.operate_type.includes('新增')">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="orange" v-else-if="row.operate_type.includes('修改')">
            {{ row.operate_type }}
          </a-tag>
          <a-tag color="red" v-else>
            {{ row.operate_type }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column field="type_id" title="模型" width="150px">
        <template #default="{ row }">
          {{ row.operate_type === '删除模型' ? row.change.alias : row.type_id}}
        </template>
      </vxe-column>
      <vxe-column field="changeDescription" title="描述">
        <template #default="{ row }">
          <p style="color:rgba(0, 0, 0, 0.65);" v-if="row.changeDescription === '没有修改'">
            {{ row.changeDescription }}
          </p>
          <template v-else-if="row.operate_type.includes('修改')">
            <p :key="index" style="color:#fa8c16;" v-for="(tag, index) in row.changeArr">
              {{ tag }}
            </p>
          </template>
          <p class="more-tag" style="color:#52c41a;" v-else-if="row.operate_type.includes('新增')">
            {{ row.changeDescription }}
          </p>
          <p style="color:#f5222d;" v-else-if="row.operate_type.includes('删除')">
            {{ row.changeDescription }}
          </p>
        </template>
      </vxe-column>
    </vxe-table>
    <a-row class="row" type="flex" justify="end">
      <a-col>
        <a-pagination
          size="small"
          v-model="current"
          :page-size-options="pageSizeOptions"
          :total="numfound"
          show-size-changer
          :page-size="pageSize"
          @change="onChange"
          @showSizeChange="onShowSizeChange"
          :show-total="(total) => `共 ${total} 条记录`"
        >
        </a-pagination>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import _ from 'lodash'
import SearchForm from './searchForm'
import { getCITypesTable, getUsers } from '@/modules/cmdb/api/history'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getRelationTypes } from '@/modules/cmdb/api/relationType'
export default {
  name: 'TypeTable',
  components: { SearchForm },
  data() {
    return {
      loading: true,
      relationTypeList: null,
      operateTypeMap: new Map([
        ['0', '新增模型'],
        ['1', '修改模型'],
        ['2', '删除模型'],
        ['3', '新增属性'],
        ['4', '修改属性'],
        ['5', '删除属性'],
        ['6', '新增触发器'],
        ['7', '修改触发器'],
        ['8', '删除触发器'],
        ['9', '新增联合唯一'],
        ['10', '修改联合唯一'],
        ['11', '删除联合唯一'],
        ['12', '新增关系'],
        ['13', '删除关系'],
      ]),
      typeList: null,
      userList: [],
      typeTableAttrList: [
        {
          alias: '模型',
          is_choice: true,
          name: 'type_id',
          value_type: '2',
          choice_value: [],
        },
        {
          alias: '操作',
          is_choice: true,
          name: 'operate_type',
          value_type: '2',
          choice_value: [
            { 新增模型: 0 },
            { 修改模型: 1 },
            { 删除模型: 2 },
            { 新增属性: 3 },
            { 修改属性: 4 },
            { 删除属性: 5 },
            { 新增触发器: 6 },
            { 修改触发器: 7 },
            { 删除触发器: 8 },
            { 新增联合唯一: 9 },
            { 修改联合唯一: 10 },
            { 删除联合唯一: 11 },
            { 新增关系: 12 },
            { 删除关系: 13 },
          ],
        },
      ],
      pageSizeOptions: ['50', '100', '200'],
      isExpand: false,
      current: 1,
      pageSize: 50,
      total: 0,
      numfound: 0,
      tableData: [],
      queryParams: {
        page: 1,
        page_size: 50,
        type_id: undefined,
        operate_type: undefined,
      },
    }
  },
  async created() {
    await Promise.all([
      this.getRelationTypes(),
      this.getTypes(),
      this.getUserList(),
    ])
    await this.getTable(this.queryParams)
  },
  updated() {
    this.$refs.xTable.$el.querySelector('.vxe-table--body-wrapper').scrollTop = 0
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowHeightMinus() {
      return this.isExpand ? 396 : 331
    },
  },
  watch: {
    current(val) {
      this.queryParams.page = val
    },
    pageSize(val) {
      this.queryParams.page_size = val
    },
  },
  methods: {
    // 获取表格数据
    async getTable(queryParams) {
      try {
        this.loading = true
        const res = await getCITypesTable(queryParams)
        res.result.forEach((item) => {
          this.handleChangeDescription(item, item.operate_type)
          item.operate_type = this.handleOperateType(item.operate_type)
          item.type_id = this.handleTypeId(item.type_id)
          item.uid = this.handleUID(item.uid)
        })
        this.tableData = res.result
        this.pageSize = res.page_size
        this.current = res.page
        this.numfound = res.numfound
        this.total = res.total
        console.log(this.tableData)
      } finally {
        this.loading = false
      }
    },
    // 获取模型
    async getTypes() {
      const res = await getCITypes()
      const typesArr = []
      const typesMap = new Map()
      res.ci_types.forEach((item) => {
        const tempObj = {}
        tempObj[item.alias] = item.id
        if (item.alias) {
          typesMap.set(item.id, item.alias)
          typesArr.push(tempObj)
        }
      })
      this.typeList = typesMap
      // 设置模型options选项
      this.typeTableAttrList[0].choice_value = typesArr
    },
    // 获取用户列表
    async getUserList() {
      const res = await getUsers()
      const userListMap = new Map()
      res.forEach((item) => {
        userListMap.set(item.uid, item.nickname)
      })
      this.userList = userListMap
    },
    // 获取关系
    async getRelationTypes() {
      const res = await getRelationTypes()
      const relationTypeMap = new Map()
      res.forEach((item) => {
        relationTypeMap.set(item.id, item.name)
      })
      this.relationTypeList = relationTypeMap
    },
    onChange(current) {
      this.current = current
      this.getTable(this.queryParams)
    },
    onShowSizeChange(current, size) {
      this.current = 1
      this.pageSize = size
      this.getTable(this.queryParams)
    },
    handleExpandChange(expand) {
      this.isExpand = expand
    },
    // 处理查询
    handleSearch(queryParams) {
      this.current = 1
      this.queryParams = queryParams
      this.getTable(this.queryParams)
    },
    // 重置表单
    searchFormReset() {
      this.queryParams = {
        page: 1,
        page_size: 50,
        type_id: undefined,
        operate_type: undefined,
      }
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
    // 转换uid
    handleUID(uid) {
      return this.userList.get(uid)
    },
    // 转换relation_type_id
    handleRelationType(relation_type_id) {
      return this.relationTypeList.get(relation_type_id)
    },
    // 处理改变描述
    handleChangeDescription(item, operate_type) {
      switch (operate_type) {
        // 新增模型
        case '0': {
          item.changeDescription = '新增模型：' + item.change.alias
          break
        }
        // 修改模型
        case '1': {
          item.changeArr = []
          for (const key in item.change.old) {
            const newVal = item.change.new[key]
            const oldVal = item.change.old[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at') {
              if (oldVal === null) {
                const str = ` [ ${key} : 改为 ${newVal || '""'} ] `
                item.changeDescription += str
                item.changeArr.push(str)
              } else {
                const str = ` [ ${key} : 由 ${oldVal || '""'} 改为 ${newVal || '""'} ] `
                item.changeDescription += ` [ ${key} : 由 ${oldVal || '""'} 改为 ${newVal || '""'} ] `
                item.changeArr.push(str)
              }
            }
          }
          if (!item.changeDescription) item.changeDescription = '没有修改'
          break
        }
        // 删除模型
        case '2': {
          item.changeDescription = `删除模型：${item.change.alias}`
          break
        }
        // 新增属性
        case '3': {
          item.changeDescription = `属性名：${item.change.alias}`
          break
        }
        // 修改属性
        case '4': {
          item.changeArr = []
          for (const key in item.change.old) {
            if (!_.isEqual(item.change.new[key], item.change.old[key]) && key !== 'updated_at') {
              let newStr = item.change.new[key]
              let oldStr = item.change.old[key]
              if (key === 'choice_value') {
                newStr = newStr ? newStr.map((item) => item[0]).join(',') : ''
                oldStr = oldStr ? oldStr.map((item) => item[0]).join(',') : ''
              }
              if (Object.prototype.toString.call(newStr) === '[object Object]') {
                newStr = JSON.stringify(newStr)
              }
              if (Object.prototype.toString.call(oldStr) === '[object Object]') {
                oldStr = JSON.stringify(oldStr)
              }
              const str = `${key} : ${oldStr ? `由 ${oldStr || '""'} ` : ''} 改为 ${newStr || '""'}`
              item.changeDescription += ` [ ${str} ] `
              item.changeArr.push(str)
            }
          }
          if (!item.changeDescription) item.changeDescription = '没有修改'
          break
        }
        // 删除属性
        case '5': {
          item.changeDescription = `删除：${item.change.alias}`
          break
        }
        // 新增触发器
        case '6': {
          item.changeDescription = `属性ID：${item.change.attr_id}，提前：${item.change.notify.before_days}天，主题：${item.change.notify.subject}\n内容：${item.change.notify.body}\n通知时间：${item.change.notify.notify_at}`
          break
        }
        // 修改触发器
        case '7': {
          item.changeArr = []
          for (const key in item.change.old.notify) {
            const newVal = item.change.new.notify[key]
            const oldVal = item.change.old.notify[key]
            if (!_.isEqual(newVal, oldVal) && key !== 'updated_at') {
              const str = ` [ ${key} : 由 ${oldVal} 改为 ${newVal} ] `
              item.changeDescription += str
              item.changeArr.push(str)
            }
          }
          if (!item.changeDescription) item.changeDescription = '没有修改'
          break
        }
        // 删除触发器
        case '8': {
          item.changeDescription = `属性ID：${item.change.attr_id}，提前：${item.change.notify.before_days}天，主题：${item.change.notify.subject}\n内容：${item.change.notify.body}\n通知时间：${item.change.notify.notify_at}`
          break
        }
        // 新增联合唯一
        case '9': {
          item.changeDescription = `属性id：[${item.change.attr_ids}]`
          break
        }
        // 修改联合唯一
        case '10': {
          item.changeArr = []
          const oldVal = item.change.old.attr_ids
          const newVal = item.change.new.attr_ids
          const str = `属性id：[${oldVal}] -> [${newVal}]`
          item.changeDescription = str
          item.changeArr.push(str)
          break
        }
        // 删除联合唯一
        case '11': {
          item.changeDescription = `属性id：[${item.change.attr_ids}]`
          break
        }
        // 新增关系
        case '12': {
          item.changeDescription = `新增：${item.change.parent.alias} -> ${this.handleRelationType(
            item.change.relation_type_id
          )} -> ${item.change.child.alias}`
          break
        }
        // 删除关系
        case '13': {
          item.changeDescription = `删除：${item.change.parent_id.alias} -> ${this.handleRelationType(
            item.change.relation_type_id
          )} -> ${item.change.child.alias}`
          break
        }
      }
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
      return option.componentOptions.children[0].text.indexOf(input) >= 0
    },
  },
}
</script>

<style lang="less" scoped>
.row {
  margin-top: 5px;
}
.filter {
  margin-left: 10px;
  color: #c0c4cc;
  cursor: pointer;
  &:hover {
    color: #606266;
  }
}
.more-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow:ellipsis;
}
p {
  margin-bottom: 0;
}
</style>
