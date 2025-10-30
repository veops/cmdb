<template>
  <div class="search-form-wrapper">
    <a-form
      class="search-form"
      :colon="false"
      :labelCol="{ span: 4 }"
      :wrapperCol="{ span: 20 }"
      labelAlign="left"
    >
      <a-row :gutter="24">
        <a-col
          :sm="24"
          :md="12"
          :lg="12"
          :xl="8"
          v-for="attr in attrList.slice(0,3)"
          :key="attr.name"
        >
          <a-form-item :label="attr.alias || attr.name">
            <a-select
              v-model="queryParams[attr.name]"
              :placeholder="$t('cmdb.history.pleaseSelect')"
              v-if="attr.is_choice"
              show-search
              :filter-option="filterOption"
              allowClear
            >
              <a-select-option
                :value="Object.values(choice)[0]"
                v-for="(choice, index) in attr.choice_value"
                :key="'Search_' + attr.name + Object.values(choice)[0] + index"
              >
                {{ Object.keys(choice)[0] }}
              </a-select-option>
            </a-select>
            <a-range-picker
              v-model="date"
              @change="onChange"
              :style="{width:'100%'}"
              :format="DATE_FORMAT"
              :placeholder="[$t('cmdb.history.startTime'), $t('cmdb.history.endTime')]"
              :show-time="timeConfig"
              v-else-if="attr.value_type === '3'"
            />
            <a-input v-model="queryParams[attr.name]" style="width: 100%" allowClear v-else />
          </a-form-item>
        </a-col>

        <template v-if="expand && attrList.length >= 4">
          <a-col
            :sm="24"
            :md="12"
            :lg="8"
            :xl="8"
            :key="'expand_' + item.name"
            v-for="item in attrList.slice(3)"
          >
            <a-form-item :label="item.alias || item.name">
              <a-select
                v-model="queryParams[item.name]"
                :placeholder="$t('cmdb.history.pleaseSelect')"
                v-if="item.is_choice"
                show-search
                :filter-option="filterOption"
                allowClear
              >
                <a-select-option
                  :value="Object.values(choice)[0]"
                  :key="'Search_' + item.name + index"
                  v-for="(choice, index) in item.choice_value"
                >
                  {{ Object.keys(choice)[0] }}
                </a-select-option
                >
              </a-select>
              <a-range-picker
                :style="{width:'100%'}"
                @change="onChange"
                :format="DATE_FORMAT"
                :placeholder="[$t('cmdb.history.startTime'), $t('cmdb.history.endTime')]"
                v-else-if="item.value_type === '3'"
                :show-time="timeConfig"
              />
              <a-input v-model="queryParams[item.name]" style="width: 100%" allowClear v-else/>
            </a-form-item>
          </a-col>
        </template>
      </a-row>
      <a-row>
        <a-col :span="24" class="search-form-actions">
          <a-space :size="8">
            <a-button type="primary" html-type="submit" @click="handleSearch" icon="search">
              {{ $t('query') }}
            </a-button>
            <a-button @click="handleExport" icon="download">
              {{ $t('export') }}
            </a-button>
            <a-button @click="handleReset" icon="redo">
              {{ $t('reset') }}
            </a-button>
            <a v-if="attrList.length >= 4" @click="toggle" class="expand-link">
              {{ expand ? $t('hide') : $t('expand') }}
              <a-icon :type="expand ? 'up' : 'down'" />
            </a>
          </a-space>
        </a-col>
      </a-row>
    </a-form>
  </div>
</template>

<script>
import moment from 'moment'
import { debounce } from 'lodash'
import { valueTypeMap } from '../../../utils/const'
import { DATE_FORMAT, TIME_DEFAULT_VALUE } from '../constants'

export default {
  name: 'SearchForm',
  props: {
    attrList: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      expand: false,
      queryParams: {
        page: 1,
        page_size: 50
      },
      date: undefined,
      DATE_FORMAT,
      searchDebounced: null
    }
  },
  computed: {
    valueTypeMap() {
      return valueTypeMap()
    },
    timeConfig() {
      return {
        hideDisabledOptions: TIME_DEFAULT_VALUE.hideDisabledOptions,
        defaultValue: [
          moment(TIME_DEFAULT_VALUE.defaultValue[0], 'HH:mm:ss'),
          moment(TIME_DEFAULT_VALUE.defaultValue[1], 'HH:mm:ss')
        ]
      }
    }
  },
  watch: {
    queryParams: {
      deep: true,
      handler: function (val) {
        if (this.searchDebounced) {
          this.searchDebounced(val)
        }
      }
    },
  },
  created() {
    this.searchDebounced = debounce((val) => {
      this.preProcessData()
      this.$emit('searchFormChange', val)
    }, 300)
  },
  beforeDestroy() {
    if (this.searchDebounced) {
      this.searchDebounced.cancel()
    }
  },
  methods: {
    moment,
    handleSearch() {
      this.queryParams.page = 1
      this.$emit('search', this.queryParams)
    },

    handleExport() {
      const queryParams = {
        ...this.queryParams
      }
      this.$emit('export', queryParams)
    },

    handleReset() {
      this.queryParams = {
        page: 1,
        page_size: 50
      }
      this.date = undefined
      this.$emit('searchFormReset')
    },

    toggle() {
      this.expand = !this.expand
      this.$emit('expandChange', this.expand)
    },

    onChange(date, dateString) {
      this.queryParams.start = dateString[0]
      this.queryParams.end = dateString[1]
    },

    filterOption(input, option) {
      return (
        option.componentOptions.children[0].text.indexOf(input) >= 0
      )
    },

    preProcessData() {
      Object.keys(this.queryParams).forEach(item => {
        if (this.queryParams[item] === '' || this.queryParams[item] === undefined) {
          delete this.queryParams[item]
        }
      })
      return this.queryParams
    },
  },
}
</script>

<style lang="less" scoped>
.search-form-wrapper {
  background: #fafafa;
  border: 1px solid #e8e8e8;
  border-radius: 2px;
  padding: 16px;
  margin-bottom: 16px;
}

.search-form {
  :deep(.ant-form-item) {
    margin-bottom: 16px;
  }

  :deep(.ant-form-item-label) {
    line-height: 32px;

    > label {
      color: rgba(0, 0, 0, 0.85);
      font-weight: 500;
    }
  }

  :deep(.ant-input),
  :deep(.ant-select-selection),
  :deep(.ant-calendar-picker-input) {
    border-radius: 2px;

    &:hover {
      border-color: @primary-color;
    }

    &:focus,
    &.ant-select-focused .ant-select-selection {
      border-color: @primary-color;
      box-shadow: 0 0 0 2px fade(@primary-color, 20%);
    }
  }
}

.search-form-actions {
  text-align: right;
  padding-top: 16px;
  border-top: 1px solid #e8e8e8;

  :deep(.ant-space) {
    margin-top: 16px;
  }

  :deep(.ant-btn) {
    border-radius: 2px;
    font-weight: 400;
    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.015);

    &.ant-btn-primary {
      &:hover {
        background-color: @primary-color;
        border-color: @primary-color;
      }
    }

    &:not(.ant-btn-primary) {
      &:hover {
        color: @primary-color;
        border-color: @primary-color;
      }
    }
  }

  .expand-link {
    font-size: 12px;
    color: @primary-color;
    cursor: pointer;
    transition: color 0.3s;
    user-select: none;

    &:hover {
      color: @primary-color;
    }

    .anticon {
      margin-left: 4px;
      font-size: 12px;
      transition: transform 0.3s;
    }
  }
}
</style>
