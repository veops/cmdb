<template>
  <div>
    <div :style="{ marginLeft: '10px'}">
      <FilterComp
        ref="filterComp"
        :canSearchPreferenceAttrList="canSearchPreferenceAttrList"
        :placement="placement"
        @setExpFromFilter="setExpFromFilter"
      >
        <div slot="popover_item" class="search-form-bar-filter">
          <a-icon :class="filterExp.length ? 'search-form-bar-filter-icon' : 'search-form-bar-filter-icon_selected'" type="filter"/>
          {{ $t('cs.components.conditionFilter') }}
          <a-icon :class="filterExp.length ? 'search-form-bar-filter-icon' : 'search-form-bar-filter-icon_selected'" type="down"/>
        </div>
      </FilterComp>
    </div>
  </div>
</template>

<script>
import FilterComp from './settingFilterComp'
export default {
name: 'SearchForm',
  components: {
    FilterComp,
  },
  props: {
      canSearchPreferenceAttrList: {
          type: Array,
          required: true,
          default: () => [],
      },
      placement: {
          type: String,
          default: 'bottomLeft'
      }
  },
  data() {
    return {
      filterExp: []
    }
  },
  methods: {
    setExpFromFilter(filterExp) {
      // const regSort = /(?<=sort=).+/g
      // const expSort = this.expression.match(regSort) ? this.expression.match(regSort)[0] : undefined
      // let expression = ''
      // if (filterExp) {
      //   expression = `q=${filterExp}`
      // }
      // if (expSort) {
      //   expression += `&sort=${expSort}`
      // }
      this.filterExp = filterExp
      this.emitRefresh(filterExp)
    },
    emitRefresh(filterExp) {
      this.$nextTick(() => {
        this.$emit('refresh', filterExp)
      })
    },
  },
}
</script>

<style lang="less" scoped>
  .search-form-bar-filter {
    background-color: rgb(240, 245, 255);
    .ops_display_wrapper();
    .search-form-bar-filter-icon {
      color: #custom_colors[color_1];
      font-size: 12px;
    }
    .search-form-bar-filter-icon_selected{
      color:#606266;
      font-size: 12px;
    }
  }
</style>
