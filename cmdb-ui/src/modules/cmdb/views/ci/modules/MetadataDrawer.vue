<template>
  <CustomDrawer
    :visible="visible"
    :hasFooter="false"
    @close="
      () => {
        visible = false
      }
    "
    :title="$t('cmdb.ci.attributeDesc')"
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
          :placeholder="$t('cmdb.ci.tips5')"
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
            index < 2
              ? null
              : index === 2
                ? valueTypeFilters
                : [
                  { label: $t('yes'), value: true },
                  { label: $t('no'), value: false },
                ]
          "
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
    return {
      visible: false,
      list: [],
      tableData: [],
      loading: false,
      valueTypeFilters: [],
      searchKey: '',
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    valueTypeMap() {
      return valueTypeMap()
    },
    columns() {
      return [
        {
          field: 'name',
          title: this.$t('name'),
          width: 150,
          align: 'left',
          help: null,
        },
        {
          field: 'alias',
          title: this.$t('alias'),
          width: 150,
          align: 'left',
          help: null,
        },
        {
          field: 'value_type',
          title: this.$t('type'),
          width: 100,
          align: 'left',
          help: null,
        },
        {
          field: 'is_index',
          title: this.$t('cmdb.ciType.isIndex'),
          width: 110,
          help: this.$t('cmdb.ci.tips6'),
        },
        {
          field: 'default_show',
          title: this.$t('cmdb.ciType.defaultShow'),
          width: 110,
          help: this.$t('cmdb.ciType.defaultShowTips'),
        },
        {
          field: 'is_unique',
          title: this.$t('cmdb.ciType.isUnique'),
          width: 110,
          help: null,
        },
        {
          field: 'is_choice',
          title: this.$t('cmdb.ciType.isChoice'),
          width: 110,
          help: this.$t('cmdb.ci.tips7'),
        },
        {
          field: 'is_list',
          title: this.$t('cmdb.ciType.list'),
          width: 110,
          help: this.$t('cmdb.ci.tips8'),
        },
        {
          field: 'is_sortable',
          title: this.$t('cmdb.ciType.isSortable'),
          width: 100,
          help: this.$t('cmdb.ci.tips9'),
        },
        {
          field: 'is_computed',
          title: this.$t('cmdb.ciType.computedAttribute'),
          width: 110,
          help: this.$t('cmdb.ci.tips10'),
        },
      ]
    },
  },
  created: function() {
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
      this.tableData = attributes.map((attr) => {
        if (attr.is_password) {
          attr.value_type = '7'
        }
        if (attr.is_link) {
          attr.value_type = '8'
        }
        return attr
      })
      this.loading = false
      this.searchAttributes()
    },
    searchAttributes() {
      const filterName = XEUtils.toValueString(this.searchKey)
        .trim()
        .toLowerCase()
      if (filterName) {
        const filterRE = new RegExp(filterName, 'gi')
        const searchProps = ['name', 'alias', 'value_type']
        const rest = this.tableData.filter((item) =>
          searchProps.some(
            (key) =>
              XEUtils.toValueString(item[key])
                .toLowerCase()
                .indexOf(filterName) > -1
          )
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
