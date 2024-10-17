<template>
  <div :class="['search-input', classType ? 'search-input-' + classType : '']">
    <a-input
      :value="searchValue"
      class="search-input-component"
      :placeholder="$t('cmdb.ciType.searchInputTip')"
      @change="handleChangeSearchValue"
      @pressEnter="saveCondition(true)"
    >
      <a-icon
        class="search-input-component-icon"
        slot="prefix"
        type="search"
        @click="saveCondition(true)"
      />
    </a-input>
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
    }
  },
  data() {
    return {}
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
        textArray.push(`*${this.searchValue}*`)
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
      const copyText = `${ciTypeIds?.length ? `_type:(${ciTypeIds.join(';')})` : ''}${exp ? `,${exp}` : ''}${searchValue ? `,*${searchValue}*` : ''}`

      this.$copyText(copyText)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    }
  }
}
</script>

<style lang="less" scoped>
.search-input {
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;

  &-component {
    height: 100%;
    flex-grow: 1;
    background-color: #FFFFFF;
    border: none;
    font-size: 14px;
    border-radius: 48px;
    overflow: hidden;

    &-icon {
      color: #2F54EB;
      font-size: 14px;
    }

    /deep/ & > input {
      height: 100%;
      margin-left: 10px;
      border: none;
      box-shadow: none;
    }
  }

  &-after {
    height: 38px;
    justify-content: flex-start;

    .search-input-component {
      max-width: 524px;
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
}
</style>
