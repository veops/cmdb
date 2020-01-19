<template>
  <div class="table-page-search-wrapper">
    <a-form layout="inline">
      <a-row :gutter="48">
        <a-col
          :lg="6"
          :md="8"
          :sm="24"
          :key="prefAttr.name"
          v-for="prefAttr in preferenceAttrList.slice(0, 4)"
        >
          <a-form-item :label="prefAttr.alias || prefAttr.name">
            <a-select
              v-model="queryParam[prefAttr.name]"
              placeholder="请选择"
              v-if="prefAttr.is_choice"
            >
              <a-select-option
                :value="choice"
                :key="'Search_' + prefAttr.name + index"
                v-for="(choice, index) in prefAttr.choice_value"
              >{{ choice }}</a-select-option>
            </a-select>
            <a-input-number
              v-model="queryParam[prefAttr.name]"
              style="width: 100%"
              v-else-if="valueTypeMap[prefAttr.value_type] == 'int' || valueTypeMap[prefAttr.value_type] == 'float'"
            />
            <a-date-picker
              v-model="queryParam[prefAttr.name]"
              style="width: 100%"
              :format="valueTypeMap[prefAttr.value_type] == 'date' ? 'YYYY-MM-DD': 'YYYY-MM-DD HH:mm:ss'"
              v-else-if="valueTypeMap[prefAttr.value_type] == 'date' || valueTypeMap[prefAttr.value_type] == 'datetime'"
            />
            <a-input v-model="queryParam[prefAttr.name]" style="width: 100%" v-else />
          </a-form-item>
        </a-col>

        <template v-if="advanced && preferenceAttrList.length > 4">
          <a-col
            :lg="6"
            :md="8"
            :sm="24"
            :key="'advanced_' + item.name"
            v-for="item in preferenceAttrList.slice(4)"
          >
            <a-form-item :label="item.alias || item.name">
              <a-select v-model="queryParam[item.name]" placeholder="请选择" v-if="item.is_choice">
                <a-select-option
                  :value="choice"
                  :key="'advanced_' + item.name + index"
                  v-for="(choice, index) in item.choice_value"
                >{{ choice }}</a-select-option>
              </a-select>
              <a-input-number
                v-model="queryParam[item.name]"
                style="width: 100%"
                v-else-if="valueTypeMap[item.value_type] == 'int' || valueTypeMap[item.value_type] == 'float'"
              />
              <a-date-picker
                v-model="queryParam[item.name]"
                style="width: 100%"
                :format="valueTypeMap[item.value_type] == 'date' ? 'YYYY-MM-DD': 'YYYY-MM-DD HH:mm:ss'"
                v-else-if="valueTypeMap[item.value_type] == 'date' || valueTypeMap[item.value_type] == 'datetime'"
              />
              <a-input v-model="queryParam[item.name]" style="width: 100%" v-else />
            </a-form-item>
          </a-col>
        </template>

        <a-col :lg="!advanced && 6 || 24" :md="!advanced && 8 || 24" :sm="24" style="float: right; padding-left: 0">
          <span
            class="table-page-search-submitButtons"
            :style="advanced && { float: 'right', overflow: 'hidden' } || {} "
          >
            <a-button type="primary" @click="$emit('refresh', true)" v-if="preferenceAttrList.length">查询</a-button>
            <a-button style="margin-left: 8px" @click="() => queryParam = {}" v-if="preferenceAttrList.length">重置</a-button>
            <a
              @click="toggleAdvanced"
              style="margin-left: 8px"
              v-if="preferenceAttrList.length > 4"
            >
              {{ advanced ? '收起' : '展开' }}
              <a-icon :type="advanced ? 'up' : 'down'" />
            </a>
          </span>
        </a-col>
      </a-row>
    </a-form>
  </div>
</template>

<script>
var valueTypeMap = {
  '0': 'int',
  '1': 'float',
  '2': 'text',
  '3': 'datetime',
  '4': 'date',
  '5': 'time',
  '6': 'json'
}

export default {
  data () {
    return {
      // 高级搜索 展开/关闭
      advanced: false,
      queryParam: {},
      valueTypeMap: valueTypeMap
    }
  },
  props: {
    preferenceAttrList: {
      type: Array,
      required: true
    }
  },

  watch: {
    '$route.path': function (oldValue, newValue) {
      this.queryParam = {}
    }
  },

  methods: {
    toggleAdvanced () {
      this.advanced = !this.advanced
    }
  }
}
</script>
