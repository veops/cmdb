<template>
  <div :class="['search-input', classType ? 'search-input-' + classType : '', { 'column-search-mode': isColumnSearch }]">
    <div class="search-area">
      <div v-show="!isColumnSearch" class="input-wrapper">
        <a-input
          :value="searchValue"
          class="search-input-component"
          :placeholder="$t('cmdb.ciType.searchInputTip')"
          @change="handleChangeSearchValue"
          @pressEnter="saveCondition(true, 'normal')"
        />
        <a-icon
          class="search-icon"
          type="search"
          @click="saveCondition(true, 'normal')"
        />
      </div>

      <div v-show="isColumnSearch" class="textarea-wrapper">
        <div class="textarea-container">
          <a-textarea
            :value="searchValue"
            class="column-search-component"
            :rows="4"
            :placeholder="$t('cmdb.ciType.columnSearchInputTip')"
            @change="handleChangeColumnSearchValue"
            @pressEnter="handlePressEnter"
          />
          <a-icon
            class="search-icon"
            type="search"
            @click="saveCondition(true, 'column')"
          />
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

        <div class="column-search-btn" @click="toggleColumnSearch">
          <a-icon class="column-search-btn-icon" type="menu" />
          <span class="column-search-btn-title">
            {{ isColumnSearch ? $t('cmdb.ciType.rowSearchMode') : $t('cmdb.ciType.columnSearchMode') }}
          </span>
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
    isColumnSearch: {
      type: Boolean,
      default: false
    }
  },
  computed: {
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
        let processedValue = this.searchValue
        if (this.isColumnSearch) {
          const values = this.searchValue.split('\n').filter(v => v.trim())
          if (values.length) {
            processedValue = `(${values.join(';')})`
          }
        }
        textArray.push(`${!this.isColumnSearch ? '*' : ''}${processedValue}${!this.isColumnSearch ? '*' : ''}`)
      }

      return textArray.length ? `q=${textArray.join(',')}` : ''
    },
  },
  methods: {
    updateAllAttributesList(value) {
      this.$emit('updateAllAttributesList', value)
    },
    saveCondition(isSubmit, searchType = 'normal') {
      this.$emit('saveCondition', isSubmit, searchType)
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
      const copyText = `${ciTypeIds?.length ? `_type:(${ciTypeIds.join(';')})` : ''}${exp ? `,${exp}` : ''}${
        searchValue ? `,${!this.isColumnSearch ? '*' : ''}${searchValue}${!this.isColumnSearch ? '*' : ''}` : ''
      }`

      this.$copyText(copyText)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },

    toggleColumnSearch() {
      this.$emit('toggleSearchMode', !this.isColumnSearch)
      this.saveCondition(false, !this.isColumnSearch ? 'column' : 'normal')
    },

    handleChangeColumnSearchValue(e) {
      const value = e.target.value
      this.changeFilter({
        name: 'searchValue',
        value
      })
    },

    handlePressEnter(e) {
      if (this.isColumnSearch) {
        // 列搜索模式下，按下 Enter 键时阻止默认行为并插入换行符
        e.preventDefault()
        const value = this.searchValue || ''
        const cursorPosition = e.target.selectionStart
        const newValue = value.slice(0, cursorPosition) + '\n' + value.slice(cursorPosition)
        this.changeFilter({
          name: 'searchValue',
          value: newValue
        })
      } else {
        this.saveCondition(true, 'normal')
      }
    }
  }
}
</script>

<style lang="less" scoped>
.search-input {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;

  .search-area {
    display: flex;
    align-items: flex-start;
    min-height: 48px;
    width: 100%;
  }

  .input-wrapper {
    position: relative;
    flex-grow: 1;

    .search-input-component {
      height: 48px;
      width: 100%;
      background-color: #FFFFFF;
      border: 1px solid #d9d9d9;
      font-size: 14px;
      border-radius: 8px;

      /deep/ input {
        height: 100%;
        padding-right: 40px;
      }
    }

    .search-icon {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: #2F54EB;
      font-size: 14px;
      cursor: pointer;
    }
  }

  .textarea-wrapper {
    flex-grow: 1;

    .textarea-container {
      position: relative;
      width: 100%;
      max-height: 200px;

      .column-search-component {
        width: 100%;
        max-height: 200px;
        background-color: #FFFFFF;
        border: 1px solid #d9d9d9;
        font-size: 14px;
        border-radius: 8px;
        padding-right: 35px;
        resize: none;
        transition: all 0.3s;

        &:hover, &:focus {
          border-color: #40a9ff;
          box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
        }
      }

      .search-icon {
        position: absolute;
        right: 12px;
        top: 12px;
        color: #2F54EB;
        font-size: 14px;
        cursor: pointer;
      }
    }
  }

  .operation-area {
    display: flex;
    align-items: center;
    height: 48px;
    margin-left: 10px;
  }

  .column-search-btn {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    margin-left: 13px;
    cursor: pointer;

    &-icon {
      color: #2F54EB;
      font-size: 12px;
    }

    &-title {
      font-size: 14px;
      font-weight: 400;
      color: #2F54EB;
      margin-left: 3px;
    }
  }

  .expression-display {
    display: flex;
    align-items: center;
    margin-left: 20px;
    max-width: 30%;

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

  .search-input-component,
  .column-search-component {
    &:hover {
      border-color: #40a9ff;
    }

    &:focus {
      border-color: #40a9ff;
      box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
      outline: none;
    }
  }
}
</style>
