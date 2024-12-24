<template>
  <div :class="['search-input', classType ? 'search-input-' + classType : '']">
    <div class="search-area">
      <a-input
        v-show="searchMode === SEARCH_MODE.NORMAL"
        :value="searchValue"
        class="search-input-component"
        :placeholder="$t('cmdb.ciType.searchInputTip')"
        @change="handleChangeSearchValue"
        @pressEnter="saveCondition(true)"
      >
        <a-icon
          class="search-icon"
          slot="prefix"
          type="search"
          @click="saveCondition(true)"
        />
      </a-input>

      <div
        v-show="searchMode === SEARCH_MODE.COLUMN"
        class="search-textarea-component"
      >
        <a-textarea
          :value="searchValue"
          :autosize="{
            minRows: 3,
            maxRows: 3,
          }"
          :placeholder="$t('cmdb.ciType.columnSearchInputTip')"
          @change="handleChangeSearchValue"
        />
        <div class="search-textarea-icon-wrap">
          <a-icon
            class="search-icon"
            type="search"
            @click="saveCondition(true)"
          />

          <a-tooltip :title="$t('cmdb.ciType.columnSearchTip')">
            <a-icon
              type="info-circle"
              class="search-icon"
            />
          </a-tooltip>
        </div>
      </div>

      <div class="operation-area">
        <FilterPopover
          ref="filterPpoverRef"
          :CITypeGroup="CITypeGroup"
          :allAttributesList="allAttributesList"
          :expression="expression"
          :selectCITypeIds="selectCITypeIds"
          @changeFilter="changeFilter"
          @updateAllAttributesList="updateAllAttributesList"
          @saveCondition="saveCondition"
        />

        <div class="search-mode-switch">
          <span
            v-for="(item) in searchModeList"
            :key="item.value"
            :class="['search-mode-switch-item', searchMode === item.value ? 'search-mode-switch-item-active' : '']"
            :style="{
              width: isZh ? '40px' : '65px'
            }"
            @click="updateSearchMode(item.value)"
          >
            {{ $t(item.label) }}
          </span>

          <span
            class="search-mode-switch-slide"
            :style="{
              left: searchMode === SEARCH_MODE.COLUMN ? (isZh ? '44px' : '69px') : '4px',
              width: isZh ? '40px' : '65px'
            }"
          ></span>
        </div>
      </div>
    </div>

    <div v-if="copyText" class="expression-display">
      <span class="expression-display-text">{{ copyText }}</span>
      <a-icon
        slot="suffix"
        type="check-circle"
        class="expression-display-icon"
        @click="handleCopyExpression"
      />
    </div>
  </div>
</template>

<script>
import { SEARCH_MODE } from '../constants.js'
import FilterPopover from './filterPopover.vue'

export default {
  name: 'SearchInput',
  components: {
    FilterPopover
  },
  props: {
    searchValue: {
      type: String,
      default: ''
    },
    expression: {
      type: String,
      default: ''
    },
    selectCITypeIds: {
      type: Array,
      default: () => []
    },
    CITypeGroup: {
      type: Array,
      default: () => []
    },
    allAttributesList: {
      type: Array,
      default: () => []
    },
    classType: {
      type: String,
      default: ''
    },
    searchMode: {
      type: String,
      default: SEARCH_MODE.NORMAL
    }
  },
  data() {
    return {
      SEARCH_MODE,
      searchModeList: [
        {
          value: SEARCH_MODE.NORMAL,
          label: 'cmdb.ciType.rowSearchMode'
        },
        {
          value: SEARCH_MODE.COLUMN,
          label: 'cmdb.ciType.columnSearchMode'
        },
      ]
    }
  },
  computed: {
    isZh() {
      return this.$i18n.locale === 'zh'
    },

    // 复制文字展示，与实际文本复制内容区别在于，未选择模型时不展示所有模型拼接数据
    copyText() {
      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const exp = this.expression.match(regQ) ? this.expression.match(regQ)[0] : null

      const textArray = []
      if (this.selectCITypeIds?.length) {
        textArray.push(`_type:(${this.selectCITypeIds.join(';')})`)
      }
      if (exp) {
        textArray.push(exp)
      }
      if (this.searchValue) {
        if (
          this.searchMode === SEARCH_MODE.COLUMN &&
          this.searchValue.includes('\n')
        ) {
          const values = this.searchValue.split('\n').filter(v => v.trim())
          textArray.push(`(${values.join(';')})`)
        } else {
          textArray.push(`*${this.searchValue}*`)
        }
      }

      return textArray.length ? `q=${textArray.join(',')}` : ''
    },
  },
  methods: {
    updateAllAttributesList(value) {
      this.$emit('updateAllAttributesList', value)
    },
    saveCondition(isSubmit) {
      this.$emit('saveCondition', isSubmit)
    },
    handleChangeSearchValue(e) {
      const value = e.target.value
      this.changeFilter({
        name: 'searchValue',
        value
      })
    },

    changeFilter(data) {
      this.$emit('changeFilter', data)
    },

    handleCopyExpression() {
      const { selectCITypeIds, expression, searchValue } = this
      const regQ = /(?<=q=).+(?=&)|(?<=q=).+$/g
      const exp = expression.match(regQ) ? expression.match(regQ)[0] : null

      const ciTypeIds = [...selectCITypeIds]
      if (!ciTypeIds.length) {
        this.CITypeGroup.forEach((item) => {
          const ids = item.ci_types.map((ci_type) => ci_type.id)
          ciTypeIds.push(...ids)
        })
      }

      let copySearchValue = ''
      if (searchValue) {
        if (
          this.searchMode === SEARCH_MODE.COLUMN &&
          this.searchValue.includes('\n')
        ) {
          const values = searchValue.split('\n').filter(v => v.trim())
          copySearchValue = `,(${values.join(';')})`
        } else {
          copySearchValue = `,*${searchValue}*`
        }
      }

      const copyText = `${ciTypeIds?.length ? `_type:(${ciTypeIds.join(';')})` : ''}${exp ? `,${exp}` : ''}${copySearchValue}`

      this.$copyText(copyText)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },

    updateSearchMode(mode) {
      this.$emit('updateSearchMode', mode)
    }
  }
}
</script>

<style lang="less" scoped>
.search-input {
  width: 100%;
  margin-bottom: 16px;

  .search-area {
    width: 100%;
    position: relative;

    .search-input-component {
      height: 48px;
      line-height: 48px;
      border-radius: 48px;
      width: 100%;
      background-color: #FFFFFF;
      font-size: 14px;

      &:hover {
        /deep/ .ant-input {
          background-color: @primary-color_5;
        }
      }

      /deep/ .ant-input {
        border: none;
        height: 48px;
        line-height: 48px;
        border-radius: 48px;

        &:focus {
          border: solid 1px @primary-color;
          background-color: #FFFFFF !important;
        }
      }
    }

    .search-textarea-component {
      position: relative;

      .search-textarea-icon-wrap {
        position: absolute;
        top: 10px;
        left: 12px;
        display: flex;
        flex-direction: column;
        row-gap: 6px;
      }

      &:hover {
        /deep/ .ant-input {
          background-color: @primary-color_5;
        }
      }

      /deep/ .ant-input {
        border: none;
        padding-left: 36px;
        resize: none;

        &:focus {
          border: solid 1px @primary-color;
          background-color: #FFFFFF !important;
        }
      }
    }

    .search-icon {
      color: @primary-color;
      font-size: 14px;
      cursor: pointer;
    }
  }

  .operation-area {
    position: absolute;
    display: flex;
    align-items: center;
    right: 0px;
    top: 0px;
    height: 48px;
    transform: translateX(100%);

    .search-mode-switch {
      display: flex;
      align-items: center;
      height: 32px;
      background-color: @primary-color_3;
      border-radius: 32px;
      position: relative;
      padding: 0 4px;
      margin-left: 14px;
      cursor: pointer;

      &-item {
        height: 24px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 400;
        color: @text-color_2;
        z-index: 1;
        position: relative;

        &-active {
          color: @primary-color;
        }
      }

      &-slide {
        position: absolute;
        transition: left 0.2s;
        border-radius: 24px;
        background-color: #FFFFFF;
        height: 24px;
        top: 4px;
        width: 40px;
        z-index: 0;
      }
    }
  }

  .expression-display {
    display: flex;
    align-items: center;
    max-width: 100%;
    width: fit-content;
    margin-top: 8px;

    &-text {
      width: 100%;
      text-overflow: ellipsis;
      overflow: hidden;
      text-wrap: nowrap;
    }

    &-icon {
      margin-left: 8px;
      color: #00b42a;
      cursor: pointer;
    }
  }

  &-after {
    .search-area {
      max-width: 420px;
    }
  }
}
</style>
