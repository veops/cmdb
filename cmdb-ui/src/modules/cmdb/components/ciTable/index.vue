<template>
  <div class="ci-table-wrap">
    <ops-table
      :id="id"
      border
      keep-source
      show-overflow
      resizable
      ref="xTable"
      size="small"
      :data="data"
      :loading="loading"
      :row-config="{ useKey: true, keyField: '_id' }"
      show-header-overflow
      highlight-hover-row
      :checkbox-config="{ reserve: true, highlight: true, range: true }"
      :edit-config="{ trigger: 'dblclick', mode: 'row', showIcon: false }"
      :sort-config="sortConfig"
      :row-key="true"
      :column-key="true"
      :cell-style="getCellStyle"
      :scroll-y="{ enabled: true, gt: 20 }"
      :scroll-x="{ enabled: true, gt: 20 }"
      class="ops-unstripe-table checkbox-hover-table"
      :custom-config="{ storage: true }"
      @checkbox-change="onSelectChange"
      @checkbox-all="onSelectChange"
      @checkbox-range-end="onSelectRangeEnd"
      v-bind="$attrs"
      v-on="$listeners"
    >
      <vxe-column
        align="center"
        type="checkbox"
        width="60"
        :fixed="isCheckboxFixed ? 'left' : ''"
        v-if="showCheckbox"
      >
        <template #default="{row}">
          {{ getRowSeq(row) }}
        </template>
      </vxe-column>
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
            <OpsMoveIcon class="header-move-icon" />
            <span>{{ col.title }}</span>
          </span>
        </template>
        <template v-if="col.is_choice || col.is_password || col.is_bool || col.is_reference" #edit="{ row }">
          <CIReferenceAttr
            v-if="col.is_reference"
            :referenceTypeId="col.reference_type_id"
            :isList="col.is_list"
            :referenceShowAttrName="referenceShowAttrNameMap[col.reference_type_id] || ''"
            :initSelectOption="getInitReferenceSelectOption(row[col.field], col)"
            v-model="row[col.field]"
          />
          <a-switch
            v-else-if="col.is_bool"
            v-model="row[col.field]"
          />
          <vxe-input v-else-if="col.is_password" v-model="passwordValue[col.field]" />
          <a-select
            v-if="col.is_choice"
            v-model="row[col.field]"
            :getPopupContainer="(trigger) => trigger.parentElement"
            :style="{ width: '100%', height: '32px' }"
            :placeholder="$t('placeholder2')"
            :showArrow="false"
            :mode="col.is_list ? 'multiple' : 'default'"
            class="ci-table-edit-select"
            allowClear
            showSearch
          >
            <a-select-option
              v-for="(choice, idx) in col.filters"
              :value="choice[0]"
              :key="'edit_' + col.field + idx"
            >
              <span
                :style="{
                  ...(choice[1] ? choice[1].style : {}),
                  display: 'inline-flex',
                  alignItems: 'center'
                }"
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
                <a-tooltip placement="topLeft" :title="choice[1] ? choice[1].label || choice[0] : choice[0]">
                  <span>{{ choice[1] ? choice[1].label || choice[0] : choice[0] }}</span>
                </a-tooltip>
              </span>
            </a-select-option>
          </a-select>
        </template>
        <template
          v-if="col.value_type === '6' || col.is_link || col.is_password || col.is_choice || col.is_reference"
          #default="{ row }"
        >
          <template v-if="col.is_reference" >
            <a
              v-for="(ciId) in (col.is_list ? row[col.field] : [row[col.field]])"
              :key="ciId"
              :href="`/cmdb/cidetail/${col.reference_type_id}/${ciId}`"
              target="_blank"
            >
              {{ getReferenceAttrValue(ciId, col) }}
            </a>
          </template>
          <span v-else-if="col.value_type === '6' && row[col.field]">{{ row[col.field] }}</span>
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
            <span
              v-for="value in (col.is_list ? row[col.field] : [row[col.field]])"
              :key="value"
              :style="getChoiceValueStyle(col, value)"
              class="column-default-choice"
            >
              <img
                v-if="getChoiceValueIcon(col, value).id && getChoiceValueIcon(col, value).url"
                :src="`/api/common-setting/v1/file/${getChoiceValueIcon(col, value).url}`"
                :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
              />
              <ops-icon
                v-else-if="getChoiceValueIcon(col, value).name"
                :style="{ color: getChoiceValueIcon(col, value).color, marginRight: '5px' }"
                :type="getChoiceValueIcon(col, value).name"
              />
              {{ getChoiceValueLabel(col, value) || value }}
            </span>
          </template>
        </template>
      </vxe-table-column>
      <vxe-column v-if="showOperation" align="left" field="operate" fixed="right" width="80">
        <template #header>
          <span>{{ $t('operation') }}</span>
        </template>
        <template #default="{ row }">
          <a-space>
            <a @click="openDetail(row.ci_id || row._id)">
              <a-icon type="unordered-list" />
            </a>
            <a-tooltip :title="$t('cmdb.ci.viewRelation')">
              <a @click="openDetail(row.ci_id || row._id, 'tab_2', '2')">
                <a-icon type="retweet" />
              </a>
            </a-tooltip>
            <a v-if="showDelete" @click="deleteCI(row)" :style="{ color: 'red' }">
              <a-icon type="delete" />
            </a>
          </a-space>
        </template>
      </vxe-column>
      <template #empty>
        <div
          v-if="loading"
          class="ci-table-loading"
        >
          {{ loadingTip || $t('loading') }}
        </div>
        <div v-else>
          <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
          <div>{{ $t('noData') }}</div>
        </div>
      </template>
      <template #loading>
        <div class="ci-table-loading">{{ loadingTip || $t('loading') }}</div>
      </template>
    </ops-table>

    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
  </div>
</template>

<script>
import _ from 'lodash'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'
import JsonEditor from '../JsonEditor/jsonEditor.vue'
import PasswordField from '../passwordField/index.vue'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'CITable',
  components: {
    JsonEditor,
    PasswordField,
    OpsMoveIcon,
    CIReferenceAttr
  },
  props: {
    // table ID
    id: {
      type: String,
      default: ''
    },
    // table Loading
    loading: {
      type: Boolean,
      default: false,
    },
    // ci 属性列表
    attrList: {
      type: Array,
      default: () => []
    },
    // table column
    columns: {
      type: Array,
      default: () => []
    },
    passwordValue: {
      type: Object,
      default: () => {}
    },
    // 加载提示
    loadingTip: {
      type: String,
      default: ''
    },
    // 是否展示复选框
    showCheckbox: {
      type: Boolean,
      default: true
    },
    // 是否展示删除按钮
    showDelete: {
      type: Boolean,
      default: true
    },
    // 表格数据
    data: {
      type: Array,
      default: () => []
    },
    sortConfig: {
      type: Object,
      default: () => ({
        remote: true,
        trigger: 'cell'
      })
    },
    // 是否展示操作列
    showOperation: {
      type: Boolean,
      default: true
    }
  },

  data() {
    return {
      referenceShowAttrNameMap: {},
      referenceCIIdMap: {},
    }
  },

  computed: {
    isCheckboxFixed() {
      const idx = this.columns.findIndex((item) => item.is_fixed)
      return idx > -1
    },
    tableDataWatch() {
      return {
        data: this.data,
        columns: this.columns
      }
    },
    referenceCIIdWatch() {
      const referenceTypeCol = this.columns?.filter((col) => col?.is_reference && col?.reference_type_id) || []
      if (!this.data?.length || !referenceTypeCol?.length) {
        return []
      }

      const ids = []
      this.data.forEach((row) => {
        referenceTypeCol.forEach((col) => {
          if (row[col.field]) {
            ids.push(...(Array.isArray(row[col.field]) ? row[col.field] : [row[col.field]]))
          }
        })
      })

      return _.uniq(ids)
    }
  },

  watch: {
    columns: {
      immediate: true,
      deep: true,
      handler(newVal) {
        this.handleReferenceShowAttrName(newVal)
      }
    },
    referenceCIIdWatch: {
      immediate: true,
      deep: true,
      handler() {
        this.handleReferenceCIIdMap()
      }
    }
  },

  methods: {
    getVxetableRef() {
      return this?.$refs?.['xTable']?.getVxetableRef?.() || null
    },

    onSelectChange() {
      const xTable = this.getVxetableRef()
      const records = [...xTable.getCheckboxRecords(), ...xTable.getCheckboxReserveRecords()]
      this.$emit('onSelectChange', records)
    },

    onSelectRangeEnd({ records }) {
      this.$emit('onSelectChange', records)
    },

    getCellStyle({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      const { property } = column
      const _find = this.attrList.find((attr) => attr.name === property)
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
      this.data.forEach((item) => {
        if (item._id === row._id) {
          item[column.property] = JSON.stringify(jsonData)
        }
      })
      this.getVxetableRef().refreshColumn()
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

    /**
     * 开启当前 ci 详情弹窗
     */
    openDetail(id, activeTabKey, ciDetailRelationKey) {
      this.$emit('openDetail', id, activeTabKey, ciDetailRelationKey)
    },

    deleteCI(row) {
      this.$emit('deleteCI', row)
    },

    getRowSeq(row) {
      return this.getVxetableRef().getRowSeq(row)
    },

    async handleReferenceShowAttrName(columns) {
      const needRequiredCITypeIds = columns?.filter((col) => col?.is_reference && col?.reference_type_id).map((col) => col.reference_type_id) || []
      if (!needRequiredCITypeIds.length) {
        this.referenceShowAttrNameMap = {}
        return
      }

      const res = await getCITypes({
        type_ids: needRequiredCITypeIds.join(',')
      })

      const map = {}
      res.ci_types.forEach((ciType) => {
        map[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      this.referenceShowAttrNameMap = map
    },

    async handleReferenceCIIdMap() {
      const referenceTypeCol = this.columns.filter((col) => col?.is_reference && col?.reference_type_id) || []
      if (!this.data?.length || !referenceTypeCol?.length) {
        this.referenceCIIdMap = {}
        return
      }

      const map = {}
      this.data.forEach((row) => {
        referenceTypeCol.forEach((col) => {
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

    getInitReferenceSelectOption(value, col) {
      const ids = Array.isArray(value) ? value : value ? [value] : []
      if (!ids.length) {
        return []
      }

      const map = this?.referenceCIIdMap?.[col?.reference_type_id]
      const attrName = this.referenceShowAttrNameMap?.[col?.reference_type_id]

      const option = (Array.isArray(value) ? value : [value]).map((id) => {
        return {
          key: id,
          title: map?.[id]?.[attrName] || id
        }
      })

      return option
    }
  }
}
</script>

<style lang="less" scoped>
.ci-table-wrap {
  .ci-table-loading {
    width: 100%;
    line-height: 200px;
  }

  .header-move-icon {
    width: 17px;
    height: 17px;
    display: none;
    position: absolute;
    left: -3px;
    top: 12px;
  }

  .column-default-choice {
    border-radius: 4px;
    padding: 1px 5px;
    margin: 2px;
    vertical-align: bottom;
    display: inline-flex;
    align-items: center;
  }
}

.checkbox-hover-table {
  /deep/ .vxe-table--body-wrapper {
    .vxe-checkbox--label {
      display: inline;
      padding-left: 0px !important;
      color: #bfbfbf;
    }

    .vxe-icon-checkbox-unchecked {
      display: none;
    }

    .vxe-icon-checkbox-checked ~ .vxe-checkbox--label {
      display: none;
    }

    .vxe-cell--checkbox {
      &:hover {
        .vxe-icon-checkbox-unchecked {
          display: inline;
        }

        .vxe-checkbox--label {
          display: none;
        }
      }
    }
  }
}
</style>
