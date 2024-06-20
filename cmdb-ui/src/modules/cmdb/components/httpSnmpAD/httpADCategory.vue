<template>
  <div class="http-ad-category">
    <div class="http-ad-category-preview" v-if="currentCate">
      <div class="category-side">
        <div
          v-for="category in categories"
          :key="category.category"
          class="category-side-item"
        >
          <div class="category-side-title">{{ category.category }}</div>
          <div class="category-side-children">
            <div
              v-for="item in category.items"
              :key="item"
              :class="['category-side-children-item', item === currentCate ? 'category-side-children-item_active' : '']"
              @click="clickCategory(item)"
            >
              {{ item }}
            </div>
          </div>
        </div>
      </div>
      <div class="category-table">
        <ADPreviewTable
          :tableData="tableData"
        />
      </div>
    </div>

    <template v-else>
      <a-input-search
        class="category-search"
        :placeholder="$t('cmdb.ad.httpSearchPlaceHolder')"
        @search="onSearchHttp"
      />
      <div class="category-main">
        <div
          v-for="category in filterCategories"
          :key="category.category"
          class="category-item"
        >
          <div class="category-title">{{ category.category }}</div>
          <div class="category-children">
            <div
              v-for="item in category.items"
              :key="item"
              :class="['category-children-item', item === currentCate ? 'category-children-item_active' : '']"
              @click="clickCategory(item)"
            >
              {{ item }}
            </div>
          </div>
        </div>
      </div>
      <div class="corporate-tip">
        {{ $t('cmdb.ad.corporateTip') }} <a href="mailto:bd@veops.cn">bd@veops.cn</a>
      </div>
    </template>
  </div>
</template>

<script>
import _ from 'lodash'
import ADPreviewTable from './adPreviewTable.vue'

export default {
  name: 'HttpADCategory',
  components: {
    ADPreviewTable
  },
  props: {
    categories: {
      type: Array,
      default: () => {},
    },
    currentCate: {
      type: String,
      default: ''
    },
    tableData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      searchValue: ''
    }
  },
  computed: {
    filterCategories() {
      const categories = _.cloneDeep(this.categories)
      const filterCategories = categories.filter((category) => {
        category.items = category.items.filter((item) => {
          return item?.indexOf(this.searchValue) !== -1
        })
        return category?.items?.length > 0
      })
      return filterCategories
    }
  },
  methods: {
    onSearchHttp(v) {
      this.searchValue = v
    },
    clickCategory(item) {
      this.$emit('clickCategory', item)
    }
  }
}
</script>

<style lang="less" scoped>
.http-ad-category {
  &-preview {
    display: flex;
    width: 100%;
    height: calc(100vh - 156px);
    justify-content: space-between;
  }

  .category-side {
    flex-shrink: 0;
    width: 150px;
    height: 100%;
    border-right: solid 1px @border-color-base;
    padding-right: 10px;

    &-item {
      &:not(:first-child) {
        margin-top: 24px;
      }

      .category-side-title {
        font-size: 12px;
        font-weight: 400;
        color: @text-color_4;
      }

      .category-side-children {
        margin-top: 5px;

        &-item {
          padding: 7px 10px;
          background-color: @layout-content-background;
          border-radius: @border-radius-base;

          color: @text-color_2;
          font-size: 12px;
          font-weight: 400;

          cursor: pointer;

          &:hover {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }

          &_active {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }
        }
      }
    }
  }

  .category-table {
    width: calc(100% - 150px - 10px - 16px);
    flex-shrink: 0;
    height: 100%;
  }

  .category-search {
    width: 254px;
  }

  .category-main {
    .category-item {
      margin-top: 24px;

      .category-title {
        font-size: 14px;
        font-weight: 700;
      }

      .category-children {
        margin-top: 8px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 19px;

        &-item {
          padding: 18px 19px;
          background-color: @layout-content-background;
          border-radius: @border-radius-base;

          color: @text-color_2;
          font-size: 14px;
          font-weight: 400;

          cursor: pointer;

          &:hover {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }

          &_active {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }
        }
      }
    }

    .corporate-tip {
      margin-top: 20px;
    }
  }
}
</style>
