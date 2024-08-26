<template>
  <div class="define-wrap">
    <a-button
      v-if="!defineList.length"
      type="primary"
      ghost
      :disabled="disabled"
      size="small"
      class="add-btn"
      @click="addData"
    >
      <a-icon type="plus" />
      {{ $t('add') }}
    </a-button>

    <vxe-table
      v-else
      ref="xTable"
      :data="defineList"
      size="mini"
      show-header-overflow
      :row-config="{ height: 46 }"
      :min-height="75"
      border="outer"
      class="define-wrap-table"
    >
      <vxe-column field="value" width="230" :title="$t('cmdb.ciType.enumValue')">
        <template #header="{ column }">
          <span class="table-header-required">*</span>
          {{ column.title }}
        </template>
        <template #default="{ row, rowIndex }">
          <a-input
            v-if="enumValueType === ENUM_VALUE_TYPE.INPUT"
            :value="row.value"
            :placeholder="$t('cmdb.ciType.valueInputTip')"
            @change="(e) => changeValue(rowIndex, e.target.value)"
          ></a-input>
          <a-input-number
            v-else-if="enumValueType === ENUM_VALUE_TYPE.NUMBER"
            :value="row.value"
            @change="(v) => changeValue(rowIndex, v)"
          >
          </a-input-number>
          <a-date-picker
            v-else
            style="width: 100%"
            :value="row.value"
            :format="enumValueType === ENUM_VALUE_TYPE.DATE ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
            :showTime="enumValueType === ENUM_VALUE_TYPE.DATE ? false : { format: 'HH:mm:ss' }"
            @change="(e) => changeDate(rowIndex, e)"
          />
        </template>
      </vxe-column>
      <vxe-column width="230" :title="$t('cmdb.ciType.label')">
        <template #default="{ row, rowIndex }">
          <DefineLabel
            :labelData="row"
            @change="(key, value) => changeStyle(rowIndex, key, value)"
            @deleteData="handleClear(rowIndex)"
          />
        </template>
      </vxe-column>
    </vxe-table>
    <div class="define-wrap-action">
      <div
        v-for="(item, index) in defineList"
        :key="item.id"
        class="define-wrap-action-item"
      >
        <a-icon
          type="plus-circle"
          class="define-wrap-action-item-icon"
          @click="addData(index)"
        />
        <a-icon
          type="minus-circle"
          class="define-wrap-action-item-icon"
          @click="deleteData(index)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import _ from 'lodash'
import DefineLabel from './defineLabel.vue'
import { ENUM_VALUE_TYPE } from '../constants.js'

export default {
  name: 'PreValueDefine',
  components: {
    DefineLabel
  },
  props: {
    value: {
      type: Array,
      default: () => []
    },
    disabled: {
      type: Boolean,
      default: false
    },
    // 枚举值控件类型
    enumValueType: {
      type: String,
      default: ENUM_VALUE_TYPE.INPUT
    }
  },
  model: {
    prop: 'value',
    event: 'change',
  },
  data() {
    return {
      ENUM_VALUE_TYPE
    }
  },
  computed: {
    defineList: {
      get() {
        return this.value.map((item) => {
          return {
            value: item?.[0] ?? '',
            ...(item?.[1] ?? {}),
            id: uuidv4()
          }
        })
      },
      set(val) {
        this.$emit('change', val.map((item) => {
          return [
            item?.value ?? '',
            {
              style: item?.style ?? {},
              icon: item?.icon ?? {},
              label: item?.label ?? '',
            }
          ]
        }))
        return val
      },
    },
  },
  methods: {
    addData(index) {
      const list = _.cloneDeep(this.value)
      list.splice(index + 1, 0, [
        '',
        {
          style: {},
          icon: {},
          label: ''
        }
      ])
      this.$emit('change', list)
    },
    deleteData(index) {
      if (this.value.length <= 1) {
        this.$message.error(this.$t('cmdb.ad.deleteTip'))
        return
      }
      const list = _.cloneDeep(this.value)
      list.splice(index, 1)
      this.$emit('change', list)
    },

    changeValue(rowIndex, value) {
      const list = _.cloneDeep(this.value)
      list[rowIndex][0] = value
      this.$emit('change', list)
    },

    changeDate(rowIndex, e) {
      const format = this.enumValueType === ENUM_VALUE_TYPE.DATE ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'
      const value = e.format(format)
      const list = _.cloneDeep(this.value)
      list[rowIndex][0] = value
      this.$emit('change', list)
    },

    changeStyle(rowIndex, key, value) {
      const list = _.cloneDeep(this.value)
      list[rowIndex][1] = {
        ...list[rowIndex][1],
        [key]: value
      }
      this.$emit('change', list)
    },

    handleClear(rowIndex) {
      const list = _.cloneDeep(this.value)
      list[rowIndex][1] = {
        style: {},
        icon: {},
        label: ''
      }
      this.$emit('change', list)
    }
  }
}
</script>

<style lang="less" scoped>
.define-wrap {
  display: flex;

  .add-btn {
    font-size: 12px;
    padding: 1px 7px;
  }

  &-table {
    flex-shrink: 0;

    .table-header-required {
      color: #FD4C6A;
    }

    /deep/ .ant-input-number {
      width: 100%;
    }
  }

  &-action {
    flex-shrink: 0;
    margin-left: 11px;
    padding-top: 36px;

    &-item {
      display: flex;
      align-items: center;
      height: 46px;
      gap: 12px;

      &-icon {
        cursor: pointer;
        color: #2F54EB;
      }
    }
  }
}
</style>
