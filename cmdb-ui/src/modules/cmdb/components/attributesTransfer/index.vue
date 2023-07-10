<template>
  <div>
    <a-transfer
      :dataSource="dataSource"
      :showSearch="true"
      :listStyle="{
        width: '200px',
        height: `${height}px`,
      }"
      :titles="['未选属性', '已选属性']"
      :render="(item) => item.title"
      :targetKeys="targetKeys"
      @change="handleChange"
      @selectChange="selectChange"
      :selectedKeys="selectedKeys"
      :filterOption="filterOption"
      class="cmdb-transfer"
    >
      <span slot="notFoundContent">暂无数据</span>
      <template slot="children" slot-scope="{ props: { direction, filteredItems } }">
        <div class="ant-transfer-list-content" v-if="direction === 'right'">
          <draggable :value="targetKeys" animation="300" @end="dragEnd" :disabled="!isSortable">
            <div
              @dblclick="changeSingleItem(item)"
              v-for="item in filteredItems"
              :key="item.key"
              :style="{ height: '38px' }"
            >
              <li
                :class="{
                  'ant-transfer-list-content-item': true,
                  'ant-transfer-list-content-item-selected': selectedKeys.includes(item.key),
                }"
                @click="setSelectedKeys(item)"
              >
                <OpsMoveIcon class="move-icon" />
                <div :class="`ant-transfer-list-content-item-text`" style="display: inline">
                  {{ item.title }}
                  <span
                    :style="{ position: 'absolute', top: '15px', left: '34px', fontSize: '11px', color: '#a3a3a3' }"
                  >{{ item.name }}</span
                  >
                </div>
                <div v-if="isFixable" @click="(e) => changeFixed(e, item)" class="ant-transfer-list-lock-icon">
                  <a-icon
                    :type="fixedList.includes(item.key) ? 'lock' : 'unlock'"
                    :theme="fixedList.includes(item.key) ? 'filled' : 'outlined'"
                  />
                </div>
                <div class="ant-transfer-list-icon" :style="{ left: '17px' }" @click="changeSingleItem(item)">
                  <a-icon type="left" />
                </div>
              </li>
            </div>
          </draggable>
        </div>
        <div v-if="direction === 'left'" class="ant-transfer-list-content">
          <div
            @dblclick="changeSingleItem(item)"
            v-for="item in filteredItems"
            :key="item.key"
            :style="{ height: '38px' }"
          >
            <li
              :class="`ant-transfer-list-content-item ${
                selectedKeys.includes(item.key) ? 'ant-transfer-list-content-item-selected' : ''
              }`"
              @click="setSelectedKeys(item)"
            >
              <div class="ant-transfer-list-content-item-text" style="display: inline">
                {{ item.title }}
                <span
                  :style="{ position: 'absolute', top: '15px', left: '34px', fontSize: '11px', color: '#a3a3a3' }"
                >{{ item.name }}</span
                >
              </div>
              <div @click="changeSingleItem(item)" :style="{ left: '4px' }" class="ant-transfer-list-icon">
                <a-icon type="right" />
              </div>
            </li>
          </div>
        </div>
      </template>
    </a-transfer>
    <div v-if="hasFooter" :style="{ marginTop: '5px', height: '20px' }">
      <a-button :style="{ float: 'right' }" size="small" @click="handleSubmit" type="primary">确定</a-button>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'

export default {
  name: 'AttributesTransfer',
  components: { draggable, OpsMoveIcon },
  props: {
    dataSource: {
      type: Array,
      default: () => [],
    },
    targetKeys: {
      type: Array,
      default: () => [],
    },
    hasFooter: {
      type: Boolean,
      default: true,
    },
    isSortable: {
      // 右侧是否可排序
      type: Boolean,
      default: true,
    },
    isFixable: {
      // 右侧是否可固定
      type: Boolean,
      default: true,
    },
    fixedList: {
      type: Array,
      default: () => [],
    },
    height: {
      type: Number,
      default: 400,
    },
  },
  data() {
    return {
      selectedKeys: [],
    }
  },
  methods: {
    selectChange(sourceSelectedKeys, targetSelectedKeys) {
      const _selectedKeys = _.cloneDeep(this.selectedKeys)
      const list = [
        { data: sourceSelectedKeys, name: 'source' },
        { data: targetSelectedKeys, name: 'target' },
      ]
      list.forEach((item) => {
        if (!item.data.__ob__) {
          if (item.data.length) {
            item.data.forEach((key) => {
              const idx = _selectedKeys.findIndex((selected) => selected === key)
              if (idx > -1) {
              } else {
                _selectedKeys.push(key)
              }
            })
            this.selectedKeys = _.cloneDeep(_selectedKeys)
          } else {
            let _list = []
            if (item.name === 'source') {
              _list = _selectedKeys.filter((key) => this.targetKeys.includes(key))
            } else {
              _list = _selectedKeys.filter((key) => !this.targetKeys.includes(key))
            }
            this.selectedKeys = _list
          }
        }
      })
    },
    setSelectedKeys(item) {
      const idx = this.selectedKeys.findIndex((key) => key === item.key)
      if (idx > -1) {
        this.selectedKeys.splice(idx, 1)
      } else {
        this.selectedKeys.push(item.key)
      }
    },
    handleChange(targetKeys, direction, moveKeys) {
      const _selectedKeys = _.cloneDeep(this.selectedKeys)
      moveKeys.forEach((key) => {
        const idx = _selectedKeys.findIndex((selected) => selected === key)
        if (idx > -1) {
          _selectedKeys.splice(idx, 1)
        }
      })
      this.selectedKeys = _.cloneDeep(_selectedKeys)
      this.$emit('setTargetKeys', targetKeys)
    },
    handleSubmit() {
      this.$emit('handleSubmit')
    },
    changeSingleItem(item) {
      this.$emit('changeSingleItem', item)
    },
    dragEnd(e) {
      const { newIndex, oldIndex } = e
      const _targetKeys = _.cloneDeep(this.targetKeys)
      const _item = _targetKeys.splice(oldIndex, 1)[0]
      _targetKeys.splice(newIndex, 0, _item)
      this.$emit('setTargetKeys', _targetKeys)
    },
    filterOption(inputValue, option) {
      return (
        option.title.toLowerCase().includes(inputValue.toLowerCase()) ||
        option.name.toLowerCase().includes(inputValue.toLowerCase())
      )
    },
    changeFixed(e, item) {
      e.stopPropagation()
      e.preventDefault()
      const _fixedList = _.cloneDeep(this.fixedList)
      const idx = _fixedList.findIndex((key) => key === item.key)
      if (idx > -1) {
        _fixedList.splice(idx, 1)
      } else {
        _fixedList.push(item.key)
      }
      this.$emit('setFixedList', _fixedList)
    },
  },
}
</script>

<style lang="less">
@import '~@/style/static.less';

.cmdb-transfer {
  .ant-transfer-list {
    background-color: #f9fbff;
    border-color: #e4e7ed;
    .ant-transfer-list-header {
      background-color: #f9fbff;
      border-bottom: none;
      .ant-transfer-list-header-title {
        color: #custom_colors[color_1];
        font-weight: 400;
        font-size: 14px;
      }
    }
    .ant-transfer-list-body-search-wrapper {
      padding-top: 0;
      padding-bottom: 5px;
      .ant-transfer-list-search-action {
        top: 0;
      }
    }
    .ant-transfer-list-body-customize-wrapper {
      padding: 0 !important;
      height: 100%;
      max-height: calc(100% - 44px);
      .ant-transfer-list-content-item {
        transition: all 0.3s;
        border-left: 2px solid #f9fbff;
        padding: 0 12px 8px 25px;
        position: relative;
        .ant-transfer-list-icon {
          position: absolute;
          top: 6px;
          display: none;
          cursor: pointer;
          font-size: 12px;
          background-color: #fff;
          color: #custom_colors[color_1];
          border-radius: 4px;
          width: 12px;
        }
        .ant-transfer-list-lock-icon {
          position: absolute;
          top: 6px;
          right: 4px;
          display: inline;
          cursor: pointer;
          font-size: 12px;
          color: #cacdd9;
          &:hover {
            color: #custom_colors[color_1];
          }
        }
        .move-icon {
          position: absolute;
          left: 0;
          top: 6px;
          display: none;
          width: 14px;
          height: 20px;
        }
        &:hover .ant-transfer-list-icon {
          display: inline;
        }
        &:hover .move-icon {
          display: inline !important;
          cursor: move;
        }
      }
      .ant-transfer-list-content-item-selected {
        background-color: #custom_colors[color_2];
        border-color: #custom_colors[color_1];
      }
    }
  }
}
</style>
