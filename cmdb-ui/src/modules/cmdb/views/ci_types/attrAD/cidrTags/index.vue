<template>
  <a-form-item
    label="CIDR"
    :labelCol="labelCol"
    :wrapperCol="{ span: 6 }"
    :extra="$t('cmdb.ciType.snmpFormTip7')"
  >
    <div class="cidr-tag">
      <div
        v-for="(item) in list"
        :key="item.id"
        class="cidr-tag-item"
      >
        <a-tooltip :title="item.value">
          <span class="cidr-tag-text">{{ item.value }}</span>
        </a-tooltip>
        <a-icon
          class="cidrv-tag-close"
          type="close"
          @click.stop="clickClose(item.id)"
        />
      </div>
      <a-input
        v-if="showAddInput"
        class="cidr-tag-input"
        autofocus
        @blur="addPreValue"
        @pressEnter="showAddInput = false"
      ></a-input>
      <a v-else class="cidr-tag-add" @click="showAddInput = true">+ {{ $t('new') }}</a>
    </div>
  </a-form-item>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'CIDRTags',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      showAddInput: false,
    }
  },
  inject: ['provide_labelCol'],
  computed: {
    list: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit('change', newValue)
      }
    },
    labelCol() {
      return this.provide_labelCol()
    }
  },
  methods: {
    clickClose(id) {
      const list = _.cloneDeep(this.value)
      const index = list.findIndex((item) => item.id === id)
      if (index !== -1) {
        list.splice(index, 1)
        this.$emit('change', list)
      }
    },
    addPreValue(e) {
      this.showAddInput = false
      const val = e.target.value
      if (!val) {
        return
      }
      const list = _.cloneDeep(this.value)
      list.push({
        value: val,
        id: uuidv4()
      })
      this.$emit('change', list)
    }
  }
}
</script>

<style lang="less" scoped>
.cidr-tag {
  width: max-content;
  max-width: 100%;
  padding: 6px 9px;
  border-radius: 2px;
  border: 1px solid #E4E7ED;
  background: #FFF;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  &-item {
    padding: 3px 6px;
    background-color: #F0F5FF;
    display: flex;
    align-items: center;
  }

  &-text {
    font-size: 12px;
    font-weight: 400;
    color: #1D2129;
    line-height: 18px;
    text-overflow: ellipsis;
    word-break: break-all;
    white-space: nowrap;
    max-width: 100px;
    overflow: hidden;
  }

  &-close {
    font-size: 12px;
    color: #1D2129;
    margin-left: 4px;
    cursor: pointer;
  }

  &-input {
    max-width: 120px;
    height: 26px;
    line-height: 26px;
    padding: 3px 6px;
  }

  &-add {
    border: dashed 1px #e4e7ed;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 400;
    color: #1D2129;
    line-height: 18px;
    cursor: pointer;
  }
}
</style>
