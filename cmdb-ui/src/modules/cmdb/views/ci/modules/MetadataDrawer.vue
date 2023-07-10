<template>
  <CustomDrawer
    :visible="visible"
    :hasFooter="false"
    @close="
      () => {
        visible = false
      }
    "
    title="属性说明"
    width="72%"
    :bodyStyle="{ height: '100vh' }"
  >
    <vxe-toolbar>
      <template #buttons>
        <a-input
          v-model="searchKey"
          :style="{ display: 'inline-block', width: '244px' }"
          class="ops-input ops-input-radius"
          type="search"
          placeholder="搜索 名称 | 别名"
          @keyup="searchAttributes"
        >
          <a-icon type="search" slot="suffix" />
        </a-input>
      </template>
    </vxe-toolbar>

    <a-spin :spinning="loading">
      <vxe-table
        resizable
        border
        size="mini"
        :height="windowHeight - 160"
        :data="list"
        :scroll-x="{ enabled: true, gt: 0 }"
        show-overflow
        show-header-overflow
        align="center"
        highlight-hover-row
        class="ops-stripe-table"
      >
        <vxe-column
          v-for="(column, index) in columns"
          :field="column.field"
          :title="column.title"
          :min-width="column.width"
          :align="column.align"
          :key="column.field"
          :fixed="index < 3 ? 'left' : ''"
          :sortable="index < 3 ? true : false"
          :title-help="column.help !== null ? { message: column.help } : null"
          :filters="
            index < 2 ? null: index === 2
              ? valueTypeFilters: [{ label: '是', value: true }, { label: '否', value: false },]"
          type="html"
        >
          <template #default="{ row }">
            <span v-if="column.field !== 'name' && column.field !== 'alias' && column.field !== 'value_type'">
              <a-icon :style="{ color: '#1fb51f' }" type="check" v-if="row[column.field]" />
            </span>
            <span v-else-if="column.field === 'value_type'" v-html="valueTypeMap[row.value_type]"> </span>
            <span v-else v-html="row[column.field]"> </span>
          </template>
        </vxe-column>
      </vxe-table>
    </a-spin>
  </CustomDrawer>
</template>

<script>
import XEUtils from 'xe-utils'
import { getCITypeAttributesByName } from '@/modules/cmdb/api/CITypeAttr'
import { valueTypeMap } from '@/modules/cmdb/utils/const'
export default {
  name: 'MetadataDrawer',
  data() {
    const columns = [
      {
        field: 'name',
        title: '名称',
        width: 150,
        align: 'left',
        help: null,
      },
      {
        field: 'alias',
        title: '别名',
        width: 150,
        align: 'left',
        help: null,
      },
      {
        field: 'value_type',
        title: '类型',
        width: 100,
        align: 'left',
        help: null,
      },
      {
        field: 'is_index',
        title: '是否索引',
        width: 110,
        help: '加快检索, 可以全文搜索, 无需使用条件过滤\n\n json目前不支持建索引 \n\n文本字符长度超过190不能建索引',
      },
      {
        field: 'default_show',
        title: '默认显示',
        width: 110,
        help: '订阅CI，默认显示在table里的属性',
      },
      {
        field: 'is_unique',
        title: '是否唯一',
        width: 110,
        help: null,
      },
      {
        field: 'is_choice',
        title: '是否选择',
        width: 110,
        help: '表现形式是下拉框, 值必须在预定义值里',
      },
      {
        field: 'is_list',
        title: '是否列表',
        width: 110,
        help: '多值, 比如内网IP',
      },
      {
        field: 'is_sortable',
        title: '可排序',
        width: 100,
        help: '仅针对前端',
      },
      {
        field: 'is_password',
        title: '是否密码',
        width: 100,
        help: null,
      },
      {
        field: 'is_link',
        title: '是否链接',
        width: 110,
        help: null,
      },
      {
        field: 'is_computed',
        title: '计算属性',
        width: 110,
        help: '模型的其他属性通过表达式的方式计算出来\n\n一个代码片段计算返回的值',
      },
    ]
    return {
      columns,
      visible: false,
      list: [],
      tableData: [],
      loading: false,
      valueTypeMap,
      valueTypeFilters: [],
      searchKey: '',
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  created: function () {
    this.valueTypeFilters = Object.keys(this.valueTypeMap).map((key) => {
      return { label: this.valueTypeMap[key], value: key }
    })
  },
  methods: {
    open(typeId) {
      this.visible = true
      this.typeId = typeId
      this.getAttrs()
    },
    async getAttrs() {
      this.loading = true
      const { attributes = [] } = await getCITypeAttributesByName(this.typeId)
      this.tableData = attributes
      this.loading = false
      this.searchAttributes()
    },
    searchAttributes() {
      const filterName = XEUtils.toValueString(this.searchKey).trim().toLowerCase()
      if (filterName) {
        const filterRE = new RegExp(filterName, 'gi')
        const searchProps = ['name', 'alias', 'value_type']
        const rest = this.tableData.filter((item) =>
          searchProps.some((key) => XEUtils.toValueString(item[key]).toLowerCase().indexOf(filterName) > -1)
        )
        this.list = rest.map((row) => {
          const item = Object.assign({}, row)
          searchProps.forEach((key) => {
            item[key] = XEUtils.toValueString(item[key]).replace(
              filterRE,
              (match) => `<span style='background: yellow'>${match}</span>`
            )
          })
          return item
        })
      } else {
        this.list = this.tableData
      }
    },
  },
}
</script>

<style></style>
