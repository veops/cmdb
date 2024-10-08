<template>
  <div
    class="resource-search"
    id="resource_search"
    :style="{ height: fromCronJob ? `${windowHeight - 48}px` : `${windowHeight - 64}px` }"
  >
    <div class="cmdb-views-header">
      <span>
        <span class="cmdb-views-header-title">{{ $t('cmdb.menu.ciSearch') }}</span>
      </span>
      <a-button
        v-if="!fromCronJob"
        icon="download"
        type="primary"
        class="ops-button-ghost"
        ghost
        @click="handleExport"
      >{{ $t('download') }}</a-button
      >
    </div>
    <div v-if="fromCronJob" class="resource-search-tip">
      <div class="resource-search-tip-item">{{ $t('cmdb.ciType.resourceSearchTip1') }}</div>
      <div class="resource-search-tip-item">{{ $t('cmdb.ciType.resourceSearchTip2') }}</div>
      <div class="resource-search-tip-item">{{ $t('cmdb.ciType.resourceSearchTip3') }}</div>
    </div>
    <SearchForm
      ref="search"
      :type="type"
      :typeId="typeId"
      @refresh="handleSearch"
      :preferenceAttrList="allAttributesList"
      @updateAllAttributesList="updateAllAttributesList"
      @copyExpression="copyExpression"
    >
      <PreferenceSearch
        v-if="!fromCronJob"
        ref="preferenceSearch"
        @getQAndSort="getQAndSort"
        @setParamsFromPreferenceSearch="setParamsFromPreferenceSearch"
      />
    </SearchForm>
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
      :height="fromCronJob ? windowHeight - 280 : windowHeight - 240"
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
      :custom-config="{ storage: true }"
    >
      <vxe-column
        v-if="instanceList.length"
        :title="$t('cmdb.ciType.ciType')"
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
          <template v-if="col.value_type === '6' || col.is_link || col.is_password || col.is_choice || col.is_reference" #default="{row}">
            <template v-if="col.is_reference && row[col.field]" >
              <a
                v-for="(ciId) in (col.is_list ? row[col.field] : [row[col.field]])"
                :key="ciId"
                :href="`/cmdb/cidetail/${col.reference_type_id}/${ciId}`"
                target="_blank"
              >
                {{ getReferenceAttrValue(ciId, col) }}
              </a>
            </template>
            <span v-else-if="col.value_type === '6' && row[col.field]">{{ JSON.stringify(row[col.field]) }}</span>
            <template v-else-if="col.is_link && row[col.field]">
              <a
                v-for="(item, linkIndex) in (col.is_list ? row[col.field] : [row[col.field]])"
                :key="linkIndex"
                :href="
                  item.startsWith('http') || item.startsWith('https')
                    ? `${item}`
                    : `http://${item}`
                "
                target="_blank"
              >
                {{ getChoiceValueLabel(col, item) || item }}
              </a>
            </template>
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
                  }"
                >
                  <ops-icon
                    :style="{ color: getChoiceValueIcon(col, value).color }"
                    :type="getChoiceValueIcon(col, value).name"
                  />
                  {{ getChoiceValueLabel(col, value) || value }}
                </span>
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
                {{ getChoiceValueLabel(col, row[col.field]) || row[col.field] }}
              </span>
            </template>
          </template>
        </vxe-column>
      </vxe-colgroup>

      <template #empty>
        <div>
          <img :style="{ width: '140px' }" :src="require('@/assets/data_empty.png')" />
          <div>{{ $t('noData') }}</div>
        </div>
      </template>
      <template #loading>
        <div style="height: 200px; line-height: 200px">{{ $t('loading') }}</div>
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
            loadInstance(sortByTable)
          }
        "
      >
        <template slot="buildOptionText" slot-scope="props">
          <span v-if="props.value !== '100000'">{{ props.value }}{{ $t('itemsPerPage') }}</span>
          <span v-if="props.value === '100000'">{{ $t('all') }}</span>
        </template>
      </a-pagination>
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
import { searchAttributes, getCITypeAttributesByTypeIds, getCITypeAttributesById } from '../../api/CITypeAttr'
import { getCITypes, getCIType } from '../../api/CIType'
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
    typeId: {
      type: Number,
      default: null
    },
    type: {
      type: String,
      default: 'resourceSearch'
    }
  },
  data() {
    return {
      ciTypes: [],
      originAllAttributesList: [],
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
      referenceShowAttrNameMap: {},
      referenceCIIdMap: {},
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
    if (this.typeId) {
      this.getCIType(this.typeId)
      this.getAttrsByType(this.typeId)
      this.loadInstance()
    } else {
      this.getAllAttr()
      this.getAllCiTypes()
    }
  },
  methods: {
    getAllCiTypes() {
      getCITypes().then((res) => {
        this.ciTypes = res.ci_types
      })
    },
    async getCIType(typeId) {
      await getCIType(typeId).then((res) => {
        this.ciTypes = res.ci_types
      })
    },
    async getAttrsByType(typeId) {
      await getCITypeAttributesById(typeId).then((res) => {
        this.allAttributesList = res.attributes
        this.originAllAttributesList = res.attributes
      })
    },
    async getAllAttr() {
      await searchAttributes({ page_size: 9999 }).then((res) => {
        this.allAttributesList = res.attributes
        this.originAllAttributesList = res.attributes
      })
    },
    async updateAllAttributesList(value) {
      if (value && value.length) {
        await getCITypeAttributesByTypeIds({ type_ids: value.join(',') }).then((res) => {
          this.allAttributesList = res.attributes
        })
      } else {
        this.allAttributesList = this.originAllAttributesList
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
      // if (exp) {
      //   exp = exp.replace(/(\:)/g, '$1*')
      //   exp = exp.replace(/(\,)/g, '*$1')
      // }
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
          if (!res['numfound']) {
            return
          }
          const { attributes: resAllAttributes } = await getCITypeAttributesByTypeIds({
            type_ids: Object.keys(res.counter).join(','),
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
          const ciTypeAttribute = {}
          const promises = _columnsGroup.map((item) => {
            return getCITypeAttributesById(item.id.split('-')[1]).then((res) => {
              ciTypeAttribute[item.label] = res.attributes
            })
          })
          await Promise.all(promises)

          const outputKeys = {}
          resAllAttributes.forEach((attr) => {
            outputKeys[attr.name] = ''
          })

          const common = {}
          Object.keys(outputKeys).forEach((key) => {
            Object.entries(ciTypeAttribute).forEach(([type, attrs]) => {
              if (attrs.find((a) => a.name === key)) {
                if (key in common) {
                  common[key][type] = ''
                } else {
                  common[key] = { [type]: '' }
                }
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

          const promises1 = _columnsGroup.map((item) => {
            return getSubscribeAttributes(item.id.split('-')[1]).then((res1) => {
              item.children = this.getColumns(res.result, res1.attributes).filter(
                (col) => !commonKeys.includes(col.field)
              )
            })
          })
          await Promise.all(promises1).then(() => {
            this.columnsGroup = [..._commonColumnsGroup, ..._columnsGroup]
            this.instanceList = res['result']
            this.handlePerference()
          })
        })
        .finally(() => {
          this.loading = false
        })
    },

    handlePerference() {
      let needRequiredCIType = []
      this.columnsGroup.forEach((group) => {
        group.children.forEach((col) => {
          if (col?.is_reference && col?.reference_type_id) {
            needRequiredCIType.push(col)
          }
        })
      })
      needRequiredCIType = _.uniq(needRequiredCIType)

      if (!needRequiredCIType.length) {
        this.referenceShowAttrNameMap = {}
        this.referenceCIIdMap = {}
        return
      }

      this.handleReferenceShowAttrName(needRequiredCIType)
      this.handleReferenceCIIdMap(needRequiredCIType)
    },

    async handleReferenceShowAttrName(needRequiredCIType) {
      const res = await getCITypes({
        type_ids: needRequiredCIType.map((col) => col.reference_type_id).join(',')
      })

      const map = {}
      res.ci_types.forEach((ciType) => {
        map[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      this.referenceShowAttrNameMap = map
    },

    async handleReferenceCIIdMap(needRequiredCIType) {
      const map = {}
      this.instanceList.forEach((row) => {
        needRequiredCIType.forEach((col) => {
          const ids = Array.isArray(row[col.field]) ? row[col.field] : row[col.field] ? [row[col.field]] : []
          if (ids.length) {
            if (!map?.[col.reference_type_id]) {
              map[col.reference_type_id] = {}
            }
            ids.forEach((id) => {
              map[col.reference_type_id][id] = {}
            })
          }
        })
      })

      if (!Object.keys(map).length) {
        this.referenceCIIdMap = {}
        return
      }

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (map?.[item._type]?.[item._id]) {
            map[item._type][item._id] = item
          }
        })
      })

      this.referenceCIIdMap = map
    },

    getReferenceAttrValue(id, col) {
      const ci = this?.referenceCIIdMap?.[col?.reference_type_id]?.[id]
      if (!ci) {
        return id
      }

      const attrName = this.referenceShowAttrNameMap?.[col.reference_type_id]
      return ci?.[attrName] || id
    },

    getColumns(data, attrList) {
      const width = document.getElementById('resource_search').clientWidth - 50
      return getCITableColumns(data, attrList, width).map((item) => {
        return { ...item, id: item.field, label: item.title }
      })
    },
    async handleSearch() {
      this.currentPage = 1
      // await this.updateAllAttributesList()
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
    getChoiceValueLabel(col, colValue) {
      const _find = col?.filters?.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.label || ''
      }
      return ''
    },
    handleExport() {
      const preferenceAttrList = [
        { id: `ci_type_alias`, value: 'ci_type_alias', label: this.$t('cmdb.ciType.ciType') },
        ...this.columnsGroup,
      ]

      preferenceAttrList.forEach((attr) => {
        if (Array.isArray(attr?.children) && attr?.children?.length) {
          attr.children = attr.children.filter((child) => {
            return !child?.is_reference
          })
        }
      })

      this.$refs.batchDownload.open({
        preferenceAttrList,
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
        original: true,
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
          this.$message.success(this.$t('copySuccess'))
          this.$emit('copySuccess', text)
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },
  },
}
</script>

<style lang="less" scoped>

.resource-search {
  margin-bottom: -24px;
  background-color: #fff;
  padding: 20px;
  border-radius: @border-radius-box;

  &-tip {
    margin-bottom: 16px;

    &-item {
      font-size: 12px;
      color: @text-color_4
    }
  }
}
</style>
