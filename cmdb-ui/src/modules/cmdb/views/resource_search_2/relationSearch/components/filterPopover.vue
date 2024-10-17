<template>
  <a-popover
    v-model="visible"
    trigger="click"
    placement="bottomRight"
    @visibleChange="handleVisibleChange"
  >
    <div class="search-condition-filter">
      <a-icon class="search-condition-filter-icon" type="filter" />

      <div
        v-if="expression"
        class="search-condition-filter-flag"
      >
      </div>
    </div>
    <template slot="content">
      <div class="search-condition-content">
        <div class="search-condition-content-title">
          {{ $t('cmdb.relationSearch.conditionFilter') }}:
        </div>

        <ConditionFilter
          ref="conditionFilterRef"
          :canSearchPreferenceAttrList="allAttributesList"
          :expression="expression"
          :CITypeIds="selectCITypeIds"
          :isDropdown="false"
          @setExpFromFilter="setExpFromFilter"
        />

        <div class="search-condition-filter-submit">
          <a-button
            type="primary"
            size="small"
            @click="clickSubmit()"
          >
            {{ $t('confirm') }}
          </a-button>
        </div>
      </div>
    </template>
  </a-popover>
</template>

<script>
import ConditionFilter from '@/modules/cmdb/components/conditionFilter/index.vue'

export default {
  name: 'FilterPopover',
  components: {
    ConditionFilter
  },
  props: {
    allAttributesList: {
      type: Array,
      default: () => []
    },
    selectCITypeIds: {
      type: Array,
      default: () => []
    },
    expression: {
      type: String,
      default: ''
    },
  },
  data() {
    return {
      visible: false
    }
  },
  methods: {
    handleVisibleChange(open) {
      if (open) {
        this.$nextTick(() => {
          this.$refs.conditionFilterRef.init(true, false)
        })
      }
    },
    clickSubmit() {
      this.$refs.conditionFilterRef.handleSubmit()
      this.visible = false
    },
    setExpFromFilter(filterExp) {
      const regSort = /(?<=sort=).+/g
      const expSort = this.expression.match(regSort) ? this.expression.match(regSort)[0] : undefined
      let expression = ''
      if (filterExp) {
        expression = `q=${filterExp}`
      }
      if (expSort) {
        expression += `&sort=${expSort}`
      }

      this.$emit('changeExpression', expression)
    }
  }
}
</script>

<style lang="less" scoped>
.search-condition-filter {
  height: 32px;
  width: 32px;
  background-color: #FFFFFF;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;

  &-flag {
    position: absolute;
    right: -5px;
    bottom: -5px;
    width: 10px;
    height: 10px;
    border-radius: 10px;
    background-color: #00B42A22;
    display: flex;
    align-items: center;
    justify-content: center;

    &::after {
      content: '';
      width: 5px;
      height: 5px;
      border-radius: 5px;
      background-color: #00B42A;
    }
  }

  &-icon {
    font-size: 12px;
    color: #A5A9BC;
  }

  &:hover {
    .search-condition-filter-icon {
      color: #2F54EB;
    }
  }
}

.search-condition-content {
  min-width: 500px;

  &-title {
    font-size: 14px;
    font-weight: 400;
    color: #4E5969;
  }
}

.search-condition-filter-submit {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}
</style>
