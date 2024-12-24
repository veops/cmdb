<template>
  <div
    class="search-condition"
    :style="{
      '--label-width': this.$i18n.locale === 'en' ? '90px' : '60px'
    }"
  >
    <div class="search-condition-row">
      <div class="search-condition-label">
        {{ $t('cmdb.relationSearch.sourceCIType') }}
      </div>

      <div class="search-condition-control">
        <treeselect
          :value="sourceCIType"
          class="custom-treeselect custom-treeselect-white filter-content-ciTypes"
          :style="{
            width: '100%',
            zIndex: '1000',
            '--custom-height': '32px',
            '--custom-multiple-lineHeight': '32px',
          }"
          :multiple="false"
          :clearable="true"
          searchable
          :options="CITypeGroup"
          :limit="1"
          :limitText="(count) => `+ ${count}`"
          :disableBranchNodes="true"
          :placeholder="$t('cmdb.relationSearch.sourceCITypeTip')"
          :normalizer="
            (node) => {
              return {
                id: node.id || -1,
                label: node.alias || node.name || $t('other'),
                title: node.alias || node.name || $t('other'),
                children: node.ci_types,
              }
            }
          "
          @input="updateSourceCIType"
          @open="handleSourceCITypeOpen"
        >
          <div
            :title="node.label"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            {{ node.label }}
          </div>
        </treeselect>

        <a-input-search
          class="search-condition-input"
          :placeholder="$t('cmdb.relationSearch.sourceCITYpeInput')"
          :value="sourceCITypeSearchValue"
          @change="handleSourceCITypeSearchValueChange"
        />
      </div>

      <FilterPopover
        :allAttributesList="sourceAllAttributesList"
        :selectCITypeIds="sourceCIType ? [sourceCIType] : []"
        :expression="sourceExpression"
        @changeExpression="changeSourceExpression"
      />
    </div>

    <div class="search-condition-row">
      <div class="search-condition-label">
        {{ $t('cmdb.relationSearch.targetCIType') }}
      </div>

      <div class="search-condition-control">
        <a-select
          :value="targetCITypes"
          show-search
          optionFilterProp="children"
          mode="multiple"
          :placeholder="$t('cmdb.relationSearch.targetCITypeTip')"
          class="search-condition-select"
          @change="handleTargetCITypeChange"
        >
          <a-select-opt-group
            v-for="(key, index) in Object.keys(targetCITypeGroup)"
            :key="key"
            :label="$t('cmdb.relationSearch.level') + `${index + 1}`"
          >
            <a-select-option
              v-for="citype in targetCITypeGroup[key]"
              :key="citype.id"
              :value="citype.id"
            >
              {{ citype.alias || citype.name }}
            </a-select-option>
          </a-select-opt-group>
        </a-select>
      </div>

      <FilterPopover
        :allAttributesList="targetAllAttributesList"
        :selectCITypeIds="targetCITypes"
        :expression="targetExpression"
        @changeExpression="changeTargetExpression"
      />
    </div>

    <div class="search-condition-row">
      <div class="search-condition-label">
        {{ $t('cmdb.relationSearch.pathSelect') }}
      </div>

      <div class="search-condition-control">
        <a-dropdown
          v-model="pathSelectVisible"
          :trigger="['click']"
          :getPopupContainer="(trigger) => trigger.parentElement"
        >
          <a-input
            :value="pathDisplay"
            readOnly
            :placeholder="$t('cmdb.relationSearch.pathSelectTip')"
            class="search-condition-input"
            @click="e => e.preventDefault()"
          >
            <a-icon
              slot="suffix"
              type="caret-down"
              class="search-condition-input-suffix"
            />
          </a-input>
          <div @click="clickPathSelectDropdown" slot="overlay">
            <template v-if="allPath.length" >
              <a-checkbox-group
                :value="selectedPath"
                class="search-condition-checkbox"
                @change="handlePathChange"
              >
                <a-checkbox
                  v-for="(path) in allPath"
                  :key="path.value"
                  :value="path.value"
                  class="search-condition-checkbox-item"
                >
                  <a-tooltip :title="path.pathNames">
                    <span class="search-condition-checkbox-item-name">
                      {{ path.pathNames }}
                    </span>
                  </a-tooltip>
                </a-checkbox>
              </a-checkbox-group>

              <div class="search-condition-path-divider"></div>

              <div class="search-condition-path-switch">
                <span>{{ $t('cmdb.relationSearch.returnPath') }}</span>
                <a-switch
                  :checked="returnPath"
                  @change="handleReturnPathChange"
                />
              </div>
            </template>

            <div
              v-else
              class="search-condition-path-null"
            >
              <img
                :src="require('@/assets/data_empty.png')"
                class="search-condition-path-null-img"
              />
              <div class="search-condition-path-null-text">{{ $t('noData') }}</div>
            </div>
          </div>
        </a-dropdown>
      </div>

      <div
        :class="['search-condition-submit', isSearchLoading ? 'search-condition-submit-loading' : '']"
        @click="clickSubmit"
      >
        <a-icon
          :type="isSearchLoading ? 'loading' : 'search'"
          class="search-condition-submit-icon"
        />
      </div>
    </div>
    <div class="search-condition-favor">
      <div class="search-condition-favor-list">
        <div
          v-for="(item) in favorList"
          :key="item.id"
          class="search-condition-favor-item"
          @click="clickFavor(item)"
        >
          <div class="search-condition-favor-name">
            {{ item.option.name }}
          </div>
          <a-icon
            @click.stop="deleteFavor(item.id)"
            type="close"
            class="search-condition-favor-close"
          />
        </div>
      </div>
      <div class="search-condition-favor-right">
        <a
          class="search-condition-save"
          @click="saveCondition"
        >
          <ops-icon
            type="veops-save"
            class="search-condition-save-icon"
          />
          <span class="search-condition-save-text">
            {{ $t('cmdb.relationSearch.saveCondition') }}
          </span>
        </a>

        <div
          v-if="isSearch"
          class="search-condition-hide"
          @click="hideSearchCondition"
        >
          <a-icon
            type="up"
            class="search-condition-hide-icon"
          />
        </div>
      </div>
    </div>

    <SaveConditionModal
      :visible="saveConditionVisible"
      @ok="handleSaveConditionOk"
      @cancel="saveConditionVisible = false"
    />
  </div>
</template>

<script>
import { getPreferenceSearch, savePreferenceSearch, deletePreferenceSearch } from '@/modules/cmdb/api/preference'

import FilterPopover from './filterPopover.vue'
import SaveConditionModal from './saveConditionModal.vue'

export default {
  name: 'SearchCondition',
  components: {
    FilterPopover,
    SaveConditionModal
  },
  props: {
    CITypeGroup: {
      type: Array,
      default: () => []
    },
    sourceCIType: {
      type: [Number, undefined],
      default: undefined
    },
    sourceCITypeSearchValue: {
      type: String,
      default: ''
    },
    sourceAllAttributesList: {
      type: Array,
      default: () => []
    },
    sourceExpression: {
      type: String,
      default: ''
    },
    targetCITypes: {
      type: Array,
      default: () => []
    },
    targetCITypeGroup: {
      type: Object,
      default: () => {}
    },
    targetAllAttributesList: {
      type: Array,
      default: () => []
    },
    targetExpression: {
      type: String,
      default: ''
    },
    returnPath: {
      type: Boolean,
      default: false
    },
    allPath: {
      type: Array,
      default: () => []
    },
    selectedPath: {
      type: Array,
      default: () => []
    },
    isSearch: {
      type: Boolean,
      default: false,
    },
    isSearchLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      oldsourceCIType: undefined,
      saveConditionVisible: false,
      pathSelectVisible: false,

      favorList: [],
      relationSearchFavorKey: '__relation_favor__'
    }
  },
  computed: {
    pathDisplay() {
      return this.allPath?.filter((path) => this?.selectedPath?.includes?.(path?.value))?.map((path) => path?.pathNames)?.join(', ') || ''
    }
  },
  mounted() {
    this.getFavorList()
  },
  methods: {
    async getFavorList() {
      const favorList = await getPreferenceSearch({
        name: this.relationSearchFavorKey
      })
      favorList.sort((a, b) => b.id - a.id)
      this.favorList = favorList
    },

    updateSourceCIType(value) {
      this.$emit('changeData', {
        name: 'sourceCIType',
        value
      })
    },

    handleSourceCITypeSearchValueChange(e) {
      const value = e.target.value
      this.$emit('changeData', {
        name: 'sourceCITypeSearchValue',
        value
      })
    },

    changeSourceExpression(expression) {
      this.$emit('changeData', {
        name: 'sourceExpression',
        value: expression
      })
    },

    handleTargetCITypeChange(value) {
      this.$emit('changeData', {
        name: 'targetCITypes',
        value
      })
    },

    changeTargetExpression(expression) {
      this.$emit('changeData', {
        name: 'targetExpression',
        value: expression
      })
    },

    handlePathChange(value) {
      this.$emit('changeData', {
        name: 'selectedPath',
        value
      })
    },

    handleReturnPathChange(checked) {
      this.$emit('changeData', {
        name: 'returnPath',
        value: checked
      })
    },

    clickSubmit() {
      if (this.isSearchLoading) {
        return
      }

      if (this.validateControl()) {
        return
      }

      this.$emit('search')
    },

    validateControl() {
      if (!this.sourceCIType) {
        this.$message.warning(`${this.$t('placeholder2')} ${this.$t('cmdb.relationSearch.sourceCIType')}`)
        return true
      }

      if (!this.targetCITypes.length) {
        this.$message.warning(`${this.$t('placeholder2')} ${this.$t('cmdb.relationSearch.targetCIType')}`)
        return true
      }

      if (!this.selectedPath.length) {
        this.$message.warning(`${this.$t('placeholder2')} ${this.$t('cmdb.relationSearch.path')}`)
        return true
      }

      return false
    },

    saveCondition() {
      if (this.validateControl()) {
        return
      }

      this.saveConditionVisible = true
    },

    async handleSaveConditionOk({ name }) {
      if (this?.favorList?.length >= 10) {
        const deletePromises = this.favorList.slice(9).map((item) => {
          return deletePreferenceSearch(item.id)
        })
        await Promise.all(deletePromises)
      }

      const option = {
        name,
        sourceCIType: this.sourceCIType,
        searchValue: this.sourceCITypeSearchValue,
        sourceExpression: this.sourceExpression,
        targetCITypes: this.targetCITypes,
        targetExpression: this.targetExpression,
        selectedPath: this.selectedPath,
      }

      savePreferenceSearch({
        option: {
          ...option
        },
        name: this.relationSearchFavorKey
      }).then(() => {
        this.$message.success(this.$t('saveSuccess'))
        this.getFavorList()
      })
    },

    deleteFavor(id) {
      deletePreferenceSearch(id).then(() => {
        this.$message.success(this.$t('deleteSuccess'))
        this.getFavorList()
      })
    },

    hideSearchCondition() {
      this.$emit('hideSearchCondition')
    },

    clickPathSelectDropdown(e) {
      if (e.key === '3') {
        this.pathSelectVisible = false
      }
    },

    clickFavor(data) {
      if (data?.option) {
        this.$emit('clickFavor', data.option)
      }
    },

    handleSourceCITypeOpen() {
      this.pathSelectVisible = false
    }
  }
}
</script>

<style lang="less" scoped>
.search-condition {
  &-row {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
    column-gap: 15px;
  }

  &-label {
    font-size: 14px;
    font-weight: 400;
    color: #000000;
    width: var(--label-width);
  }

  &-control {
    display: flex;
    align-items: center;
    column-gap: 12px;
    width: 500px;

    /deep/ .ant-dropdown-content {
      background-color: #FFFFFF;
      padding: 14px 18px;
      width: 500px;
    }

    /deep/ .filter-content-ciTypes {
      &:not(.vue-treeselect--disabled):not(.vue-treeselect--focused) {
        .vue-treeselect__control {
          border: solid 1px transparent;

          &:hover {
            border-color: @primary-color;
          }
        }
      }
    }
  }

  &-input {
    width: 100%;

    /deep/ .ant-input {
      border: solid 1px transparent;
      box-shadow: none;
      cursor: pointer;

      &:hover {
        border-color: @primary-color;
      }
    }

    &-suffix {
      color: #CACDD9;
    }
  }

  &-select {
    width: 100%;

    /deep/ .ant-select-selection {
      border: solid 1px transparent;
      box-shadow: none;

      &:hover {
        border-color: @primary-color;
      }
    }
  }

  &-path {
    &-divider {
      width: 100%;
      margin: 20px 0;
      height: 1px;
      background-color: #E4E7ED;
    }

    &-switch {
      display: flex;
      align-items: center;
      column-gap: 16px;
    }
  }

  &-checkbox {
    display: flex;
    flex-direction: column;
    max-height: 300px;
    overflow-y: auto;
    overflow-x: hidden;

    &-item {
      margin: 0px;
      display: flex;
      align-items: center;

      /deep/ & > span:first-child {
        flex-shrink: 0;
      }

      /deep/ & > span:last-child {
        width: 100%;
      }

      &-name {
        overflow: hidden;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        display: inline-block;
        max-width: 100%;
      }

      &:not(:last-child) {
        margin-bottom: 16px;
      }
    }
  }

  &-path-null {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    &-img {
      width: 100px;
    }

    &-text {
      margin-top: 12px;
      color: #A5A9BC;
    }
  }

  &-submit {
    width: 32px;
    height: 32px;
    cursor: pointer;
    border-radius: 2px;
    background-color: #2F54EB;
    display: flex;
    align-items: center;
    justify-content: center;

    &-icon {
      font-size: 12px;
      color: #FFFFFF;
    }

    &-loading {
      background-color: #2F54EB90;
    }

    &:hover {
      background-color: #2F54EB90;
    }
  }

  &-favor {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 24px;
    column-gap: 15px;

    &-list {
      max-width: 500px;
      display: flex;
      align-items: center;
      column-gap: 14px;
      overflow-x: auto;
      overflow-y: hidden;
      padding-bottom: 4px;
    }

    &-name {
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
    }

    &-close {
      font-size: 12px;
      color: #4E5969;
      flex-shrink: 0;

      &:hover {
        color: #4E596980;
      }
    }

    &-right {
      display: flex;
      align-items: center;
      flex-shrink: 0;
    }

    &-item {
      display: flex;
      align-items: center;
      max-width: 150px;
      background-color: #EBEFF8;
      border-radius: 28px;
      padding: 2px 12px;
      column-gap: 3px;
      cursor: pointer;

      &:hover {
        background-color: @primary-color_4;

        .search-condition-favor-name {
          color: @primary-color;
        }

        .search-condition-favor-close {
          color: @primary-color;
        }
      }
    }
  }

  &-save {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    font-size: 12px;
    column-gap: 7px;
  }

  &-hide {
    width: 18px;
    height: 18px;
    background-color: #EBEFF8;
    border-radius: 1px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-left: 22px;

    &-icon {
      font-size: 12px;
      color: #86909C;
    }

    &:hover {
      background-color: @primary-color_4;

      .search-condition-hide-icon {
        color: @primary-color_4;
      }
    }
  }
}
</style>
