<template>
  <div>
    <a-form :colon="false">
      <a-row :gutter="24">
        <a-col
          :sm="24"
          :md="12"
          :lg="12"
          :xl="8"
          v-for="attr in attrList.slice(0,3)"
          :key="attr.name"
        >
          <a-form-item
            :label="attr.alias || attr.name "
            :labelCol="{span:4}"
            :wrapperCol="{span:20}"
            labelAlign="right"
          >
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
                :key="'Search_' + attr.name + index"
              >
                {{ Object.keys(choice)[0] }}
              </a-select-option>
            </a-select>
            <a-range-picker
              v-model="date"
              @change="onChange"
              :style="{width:'100%'}"
              format="YYYY-MM-DD HH:mm:ss"
              :placeholder="[$t('cmdb.history.startTime'), $t('cmdb.history.endTime')]"
              :show-time="{
                hideDisabledOptions: true,
                defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('23:59:59', 'HH:mm:ss')],
              }"
              v-else-if="valueTypeMap[attr.value_type] == 'date' || valueTypeMap[attr.value_type] == 'datetime'"
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
            <a-form-item
              :label="item.alias || item.name"
              :label-col="{ span: 4 }"
              :wrapper-col="{ span: 20 }"
              labelAlign="right"
            >
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
                format="YYYY-MM-DD HH:mm"
                :placeholder="[$t('cmdb.history.startTime'), $t('cmdb.history.endTime')]"
                v-else-if="valueTypeMap[item.value_type] == 'date' || valueTypeMap[item.value_type] == 'datetime'"
                :show-time="{
                  hideDisabledOptions: true,
                  defaultValue: [moment('00:00:00', 'HH:mm:ss'), moment('23:59:59', 'HH:mm:ss')],
                }"
              />
              <a-input v-model="queryParams[item.name]" style="width: 100%" allowClear v-else/>
            </a-form-item>
          </a-col>
        </template>
      </a-row>
      <a-row>
        <a-col :span="24" :style="{ textAlign: 'right' , marginBottom: '10px' }">
          <a-button type="primary" html-type="submit" @click="handleSearch">
            {{ $t('query') }}
          </a-button>
          <a-button :style="{ marginLeft: '8px' }" @click="handleReset">
            {{ $t('reset') }}
          </a-button>
          <a :style="{ marginLeft: '8px', fontSize: '12px' }" @click="toggle" v-if="attrList.length >= 4">
            {{ expand?$t('hide'):$t('expand') }} <a-icon :type="expand ? 'up' : 'down'" />
          </a>
        </a-col>
      </a-row>
    </a-form>
  </div>
</template>

<script>
import moment from 'moment'
import { valueTypeMap } from '../../../utils/const'
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
      date: undefined
    }
  },
  computed: {
    valueTypeMap() {
      return valueTypeMap()
    },
  },
  watch: {
    queryParams: {
      deep: true,
      handler: function (val) {
        this.preProcessData()
        this.$emit('searchFormChange', val)
      }
    },
  },
  methods: {
    moment,
    handleSearch() {
      this.queryParams.page = 1
      this.$emit('search', this.queryParams)
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

<style>

</style>
