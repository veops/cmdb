<template>
  <div class="http-ad-category">
    <div class="http-ad-category-preview" v-if="currentCate && isPreviewDetail">
      <div class="category-side">
        <div
          v-for="(category, categoryIndex) in categories"
          :key="category.category"
          class="category-side-item"
        >
          <div class="category-side-title">
            <div class="category-side-title">
              <a-icon
                v-if="categoryIndex === 0"
                type="left"
                @click="clickBack"
              />
              {{ category.category }}
            </div>
          </div>
          <div class="category-side-children">
            <div
              v-for="(item, itemIndex) in category.items"
              :key="item"
              :class="['category-side-children-item', item === currentCate ? 'category-side-children-item_active' : '']"
              @click="clickCategory(item)"
            >
              {{ item }}
              <span
                class="category-side-children-item-corporate"
                v-if="ruleType === 'private_cloud' || (ruleType === 'http' && (categoryIndex !== 0 || itemIndex !== 0))"
              >
                企
              </span>
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
          v-for="(category, categoryIndex) in filterCategories"
          :key="category.category"
          class="category-item"
        >
          <div class="category-title">{{ category.category }}</div>
          <div class="category-children">
            <div
              v-for="(item, itemIndex) in category.items"
              :key="item"
              :class="['category-children-item', item === currentCate ? 'category-children-item_active' : '']"
              @click="clickCategory(item)"
            >
              {{ item }}
              <div
                class="corporate-flag"
                v-if="ruleType === 'private_cloud' || (ruleType === 'http' && (categoryIndex !== 0 || itemIndex !== 0))"
              >
                <span class="corporate-flag-text">企</span>
              </div>
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
    ruleType: {
      type: String,
      default: 'http',
    },
  },
  data() {
    return {
      searchValue: '',
      isPreviewDetail: false,
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
      this.isPreviewDetail = true
    },
    clickBack() {
      this.isPreviewDetail = false
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
      &:not(:last-child) {
        margin-bottom: 24px;
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
          position: relative;
          margin-top: 5px;

          display: flex;
          align-items: center;
          justify-content: space-between;

          &:hover {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }

          &_active {
            background-color: @layout-sidebar-selected-color;
            color: @layout-header-font-selected-color;
          }

          &-corporate {
            flex-shrink: 0;
            width: 18px;
            height: 18px;
            background-color: #E1EFFF;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;

            color: #2F54EB;
            font-size: 12px;
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
          position: relative;
          min-width: 100px;
          text-align: center;

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

  .corporate-tip {
    margin-top: 20px;
  }

  .corporate-flag {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 4;

    width: 38px;
    height: 28px;
    border-left: 38px solid transparent;
    border-top: 28px solid @primary-color_4;

    &-text {
      width: 37px;
      position: absolute;
      top: -28px;
      right: 3px;
      text-align: right;

      color: @primary-color;
      font-size: 10px;
      font-weight: 400;
    }
  }
}
</style>
