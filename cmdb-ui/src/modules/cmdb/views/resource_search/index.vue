<template>
  <div id="resource_search" :style="{ height: fromCronJob ? `${windowHeight - 48}px` : `${windowHeight - 90}px` }">
    <div class="cmdb-views-header">
      <span>
        <span class="cmdb-views-header-title">资源搜索</span>
      </span>
    </div>
    <div :style="{ backgroundColor: '#fff', padding: '12px', borderRadius: '15px' }">
      <SearchForm
        ref="search"
        type="resourceSearch"
        @refresh="handleSearch"
        :preferenceAttrList="allAttributesList"
        @updateAllAttributesList="updateAllAttributesList"
        @copyExpression="copyExpression"
      />
      <div
        v-if="!fromCronJob"
        :style="{
          display: 'flex',
          justifyContent: 'space-between',
          height: '32px',
          marginBottom: '5px',
          alignItems: 'center',
        }"
      >
        <a-button icon="download" type="primary" ghost size="small" @click="handleExport">导出</a-button>
        <PreferenceSearch
          ref="preferenceSearch"
          @getQAndSort="getQAndSort"
          @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
        />
      </div>
      <vxe-table
        :id="`cmdb-resource`"
        border
        keep-source
        show-overflow
        resizable
        ref="xTable"
        size="small"
        row-id="_id"
        :loading="loading"
        :height="fromCronJob ? windowHeight - 180 : windowHeight - 250"
        show-header-overflow
        highlight-hover-row
        :data="instanceList"
        :sort-config="{ remote: true, trigger: 'cell' }"
        @sort-change="handleSortCol"
        :row-key="true"
        :column-key="true"
        :cell-style="getCellStyle"
        :scroll-y="{ enabled: true, gt: 20 }"
        :scroll-x="{ enabled: true, gt: 0 }"
        :export-config="{
          isColgroup: true,
          type: 'xlsx',
          types: ['xlsx', 'csv', 'html', 'xml', 'txt'],
          mode: 'current',
          modes: ['current'],
          isFooter: false,
          isHeader: true,
          isColgroup: true,
        }"
        class="ops-unstripe-table"
        :style="{ margin: '0 -12px' }"
        :custom-config="{ storage: true }"
      >
        <vxe-column
          v-if="instanceList.length"
          title="模型"
          field="ci_type_alias"
          :width="100"
          fixed="left"
        ></vxe-column>
        <vxe-colgroup v-for="colGroup in columnsGroup" :key="colGroup.value" :title="colGroup.label">
          <template #header>
            <span :style="{ display: 'inline-flex', alignItems: 'center' }">
              {{ colGroup.label }}
              <EditAttrsPopover
                :style="{ borderLeft: 'none', width: '30px', height: '38px', cursor: 'pointer' }"
                v-if="colGroup.isCiType"
                :typeId="Number(colGroup.id.split('-')[1])"
                @refresh="loadInstance"
              />
            </span>
          </template>
          <vxe-column
            v-for="(col, index) in colGroup.children"
            :key="`${col.field}_${index}`"
            :title="col.title"
            :field="col.field"
            :width="col.width"
            :minWidth="100"
            :cell-type="col.value_type === '2' ? 'string' : 'auto'"
          >
            <template v-if="col.value_type === '6' || col.is_link || col.is_password || col.is_choice" #default="{row}">
              <span v-if="col.value_type === '6' && row[col.field]">{{ JSON.stringify(row[col.field]) }}</span>
              <a v-else-if="col.is_link" :href="`${row[col.field]}`" target="_blank">{{ row[col.field] }}</a>
              <PasswordField v-else-if="col.is_password && row[col.field]" :password="row[col.field]"></PasswordField>
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
                    }"
                  ><ops-icon
                    :style="{ color: getChoiceValueIcon(col, value).color }"
                    :type="getChoiceValueIcon(col, value).name"
                  />{{ value }}</span
                  >
                </template>
                <span
                  v-else
                  :style="{
                    borderRadius: '4px',
                    padding: '1px 5px',
                    margin: '2px 0',
                    ...getChoiceValueStyle(col, row[col.field]),
                  }"
                >
                  <ops-icon
                    :style="{ color: getChoiceValueIcon(col, row[col.field]).color }"
                    :type="getChoiceValueIcon(col, row[col.field]).name"
                  />
                  {{ row[col.field] }}</span
                >
              </template>
            </template>
          </vxe-column>
        </vxe-colgroup>

        <template #empty>
          <div v-if="loading" style="height: 200px; line-height: 200px">加载中...</div>
          <div v-else>
            <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
            <div>暂无数据</div>
          </div>
        </template>
      </vxe-table>
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
              loadInstance(sortByTable)
            }
          "
        >
          <template slot="buildOptionText" slot-scope="props">
            <span v-if="props.value !== '100000'">{{ props.value }}条/页</span>
            <span v-if="props.value === '100000'">全部</span>
          </template>
        </a-pagination>
      </div>
    </div>

    <BatchDownload
      :replaceFields="{ cildren: 'children', title: 'label', key: 'id' }"
      ref="batchDownload"
      @batchDownload="batchDownload"
      treeType="tree"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import SearchForm from '../../components/searchForm/SearchForm.vue'
import { searchCI } from '../../api/ci'
import { searchAttributes, getCITypeAttributesByTypeIds } from '../../api/CITypeAttr'
import { getCITypes } from '../../api/CIType'
import { getSubscribeAttributes } from '../../api/preference'
import { getCITableColumns } from '../../utils/helper'
import EditAttrsPopover from '../ci/modules/editAttrsPopover.vue'
import PasswordField from '../../components/passwordField/index.vue'
import BatchDownload from '../../components/batchDownload/batchDownload.vue'
import PreferenceSearch from '../../components/preferenceSearch/preferenceSearch.vue'

export default {
  name: 'ResourceSearch',
  components: { SearchForm, EditAttrsPopover, PasswordField, BatchDownload, PreferenceSearch },
  props: {
    fromCronJob: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ciTypes: [],
      allAttributesList: [], // 当前选择的模型的全部attributes  默认全部
      currentPage: 1,
      pageSizeOptions: ['50', '100', '200', '100000'],
      pageSize: 50,
      totalNumber: 0,
      instanceList: [],
      // columns: {},
      sortByTable: undefined,
      loading: false,
      columnsGroup: [],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  provide() {
    return {
      setPreferenceSearchCurrent: this.setPreferenceSearchCurrent,
      filterCompPreferenceSearch: () => {},
    }
  },
  mounted() {
    this.getAllAttr()
    this.getAllCiTypes()
  },
  methods: {
    getAllCiTypes() {
      getCITypes().then((res) => {
        this.ciTypes = res.ci_types
      })
    },
    getAllAttr() {
      searchAttributes({ page_size: 9999 }).then((res) => {
        this.allAttributesList = res.attributes
      })
    },
    updateAllAttributesList(value) {
      if (value && value.length) {
        getCITypeAttributesByTypeIds({ type_ids: value.join(',') }).then((res) => {
          this.allAttributesList = res.attributes
        })
      } else {
        this.getAllAttr()
      }
    },
    async loadInstance(sortByTable = undefined) {
      this.loading = true
      // 若模糊搜索可以 queryParam相关后期可删除
      // const queryParams = this.$refs['search'].queryParam || {}
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
      if (!sort) {
        sort = '_type'
      }
      let currenCiType = this.$refs['search'].currenCiType
      if (!currenCiType.length) {
        const _currenCiType = []
        this.$refs['search'].ciTypeGroup.forEach((item) => {
          _currenCiType.push(...item.ci_types.map((type) => type.id))
        })
        currenCiType = _currenCiType
      }
      searchCI({
        q: `${currenCiType && currenCiType.length ? `_type:(${currenCiType.join(';')})` : ''}${exp ? `,${exp}` : ''}${
          fuzzySearch ? `,*${fuzzySearch}*` : ''
        }`,
        count: this.pageSize,
        page: this.currentPage,
        sort,
      })
        .then(async (res) => {
          this.columnsGroup = []
          this.instanceList = []
          this.totalNumber = res['numfound']

          const oldData = res.result

          function allKeys(data) {
            const keys = {}
            const ignoreAttr = ['_id', '_type', 'ci_type', 'ci_type_alias', 'unique', 'unique_alias']
            data.forEach((item) => {
              Object.keys(item).forEach((key) => {
                if (!ignoreAttr.includes(key)) {
                  keys[key] = ''
                }
              })
            })
            return keys
          }

          function tidy(data) {
            const outputKeys = allKeys(data)
            const common = {}
            data.forEach((item) => {
              const tmp = {}
              Object.keys(outputKeys).forEach((j) => {
                if (j in item) {
                  tmp[j] = item[j]
                  // 提取common
                  {
                    const key = item['ci_type_alias']
                    if (j in common) {
                      common[j][[key]] = ''
                    } else {
                      common[j] = { [key]: '' }
                    }
                  }
                } else {
                  tmp[j] = null
                }
              })
            })
            const commonObject = {}
            const commonKeys = []
            // 整理common
            Object.keys(common).forEach((key) => {
              if (Object.keys(common[key]).length > 1) {
                commonKeys.push(key)
                const reverseKey = Object.keys(common[key]).join('&')
                if (!commonObject[reverseKey]) {
                  commonObject[reverseKey] = [key]
                } else {
                  commonObject[reverseKey].push(key)
                }
              }
            })
            return { commonObject, commonKeys }
          }

          const { commonObject, commonKeys } = tidy(oldData)
          const _commonColumnsGroup = Object.keys(commonObject).map((key) => {
            return {
              id: `parent-${key}`,
              value: key,
              label: key,
              children: this.getColumns(
                res.result,
                commonObject[key].map((item) => {
                  const _find = this.allAttributesList.find((attr) => attr.name === item)
                  return _find
                })
              ),
            }
          })

          const _columnsGroup = Object.keys(res.counter).map((key) => {
            const _find = this.ciTypes.find((item) => item.name === key)
            return {
              id: `parent-${_find.id}`,
              value: key,
              label: _find?.alias || _find?.name,
              isCiType: true,
            }
          })

          const promises = _columnsGroup.map((item) => {
            return getSubscribeAttributes(item.id.split('-')[1]).then((res1) => {
              item.children = this.getColumns(res.result, res1.attributes).filter(
                (col) => !commonKeys.includes(col.field)
              )
            })
          })
          await Promise.all(promises).then(() => {
            this.columnsGroup = [..._commonColumnsGroup, ..._columnsGroup]
            this.instanceList = res['result']
          })
        })
        .finally(() => {
          this.loading = false
        })
    },
    getColumns(data, attrList) {
      const width = document.getElementById('resource_search').clientWidth - 50
      return getCITableColumns(data, attrList, width).map((item) => {
        return { ...item, id: item.field, label: item.title }
      })
    },
    handleSearch() {
      this.currentPage = 1
      this.loadInstance()
    },
    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize
      this.currentPage = 1
      this.loadInstance()
    },
    handleSortCol() {},
    getCellStyle({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      const { property } = column
      const _find = this.allAttributesList.find((attr) => attr.name === property)
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
    handleExport() {
      // this.$refs.xTable.openExport()
      this.$refs.batchDownload.open({
        preferenceAttrList: [{ id: `ci_type_alias`, value: 'ci_type_alias', label: '模型' }, ...this.columnsGroup],
      })
    },
    batchDownload({ filename, type, checkedKeys }) {
      const jsonAttrList = []
      checkedKeys.forEach((key) => {
        const _find = this.allAttributesList.find((attr) => attr.name === key)
        if (_find && _find.value_type === '6') {
          jsonAttrList.push(key)
        }
      })
      const data = _.cloneDeep(this.instanceList)
      this.$refs.xTable.exportData({
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
        download: false,
      })
      this.selectedRowKeys = []
      this.$refs.xTable.clearCheckboxRow()
      this.$refs.xTable.clearCheckboxReserve()
    },
    getQAndSort() {
      const fuzzySearch = this.$refs['search'].fuzzySearch || ''
      const expression = this.$refs['search'].expression || ''
      const currenCiType = this.$refs['search'].currenCiType || undefined
      this.$refs.preferenceSearch.savePreference({ fuzzySearch, expression, currenCiType })
    },
    setParamsFromPreferenceSearch(item) {
      const { fuzzySearch, expression, currenCiType } = item.option
      this.$refs.search.fuzzySearch = fuzzySearch
      this.$refs.search.expression = expression
      this.$refs.search.currenCiType = currenCiType
      this.currentPage = 1
      this.$nextTick(() => {
        this.loadInstance()
      })
    },
    setPreferenceSearchCurrent(id = null) {
      if (this.$refs.preferenceSearch) {
        this.$refs.preferenceSearch.currentPreferenceSearch = id
      }
    },
    copyExpression() {
      const expression = this.$refs['search'].expression || ''
      const fuzzySearch = this.$refs['search'].fuzzySearch

      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g

      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null
      let currenCiType = this.$refs['search'].currenCiType
      if (!currenCiType.length) {
        const _currenCiType = []
        this.$refs['search'].ciTypeGroup.forEach((item) => {
          _currenCiType.push(...item.ci_types.map((type) => type.id))
        })
        currenCiType = _currenCiType
      }
      const text = `q=${currenCiType && currenCiType.length ? `_type:(${currenCiType.join(';')})` : ''}${
        exp ? `,${exp}` : ''
      }${fuzzySearch ? `,*${fuzzySearch}*` : ''}`
      this.$copyText(text)
        .then(() => {
          this.$message.success('复制成功！')
          this.$emit('copySuccess', text)
        })
        .catch(() => {
          this.$message.error('复制失败！')
        })
    },
  },
}
</script>
