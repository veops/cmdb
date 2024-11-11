<template>
  <div>
    <a-transfer
      :dataSource="dataSource"
      :showSearch="true"
      :listStyle="{
        width: '200px',
        height: `${height}px`,
      }"
      :titles="[$t('cmdb.components.unselectAttributes'), $t('cmdb.components.selectAttributes')]"
      :render="(item) => item.title"
      :targetKeys="targetKeys"
      @change="handleChange"
      @selectChange="selectChange"
      :selectedKeys="selectedKeys"
      :filterOption="filterOption"
      class="cmdb-transfer"
    >
      <span slot="notFoundContent">{{ $t('noData') }}</span>
      <template slot="children" slot-scope="{ props: { direction, filteredItems } }">
        <div class="ant-transfer-list-content" v-if="direction === 'right'">
          <draggable :value="targetKeys" animation="300" @end="dragEnd" :disabled="!isSortable">
            <div
              @dblclick="changeSingleItem(item)"
              v-for="item in filterDefaultAttr(filteredItems)"
              :key="item.key"
              :style="{ height: '38px' }"
            >
              <li
                :class="
                  `ant-transfer-list-content-item ${
                    selectedKeys.includes(item.key) ? 'ant-transfer-list-content-item-selected' : ''
                  }`
                "
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

          <div
            v-if="rightDefaultAttrList.length"
            class="default-attr"
          >
            <a-divider>
              <span class="default-attr-divider">
                {{ $t('cmdb.components.default') }}
              </span>
            </a-divider>

            <div
              v-for="(item) in rightDefaultAttrList"
              :key="item.key"
              :class="['default-attr-item', selectedKeys.includes(item.key) ? 'default-attr-item-selected' : '']"
              @click="setSelectedKeys(item)"
              @dblclick="changeSingleItem(item)"
            >
              <div
                class="default-attr-arrow"
                style="left: 17px"
                @click.stop="changeSingleItem(item)"
              >
                <a-icon type="left" />
              </div>
              <div class="default-attr-title">
                {{ $t(item.title) }}
              </div>
              <div class="default-attr-name">
                {{ item.name }}
              </div>
            </div>
          </div>
        </div>
        <div v-if="direction === 'left'" class="ant-transfer-list-content">
          <div
            @dblclick="changeSingleItem(item)"
            v-for="item in filterDefaultAttr(filteredItems)"
            :key="item.key"
            :style="{ height: '38px' }"
          >
            <li
              :class="
                `ant-transfer-list-content-item ${
                  selectedKeys.includes(item.key) ? 'ant-transfer-list-content-item-selected' : ''
                }`
              "
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

          <div
            v-if="leftDefaultAttrList.length"
            class="default-attr"
          >
            <a-divider>
              <span class="default-attr-divider">
                {{ $t('cmdb.components.default') }}
              </span>
            </a-divider>

            <div
              v-for="(item) in leftDefaultAttrList"
              :key="item.key"
              :class="['default-attr-item', selectedKeys.includes(item.key) ? 'default-attr-item-selected' : '']"
              @click="setSelectedKeys(item)"
              @dblclick="changeSingleItem(item)"
            >
              <div
                class="default-attr-arrow"
                style="left: 2px"
                @click.stop="changeSingleItem(item)"
              >
                <a-icon type="right" />
              </div>
              <div class="default-attr-title">
                {{ $t(item.title) }}
              </div>
              <div class="default-attr-name">
                {{ item.name }}
              </div>
            </div>
          </div>
        </div>
      </template>
    </a-transfer>
    <div v-if="hasFooter" :style="{ marginTop: '5px', height: '20px' }">
      <a-button :style="{ float: 'right' }" size="small" @click="handleSubmit" type="primary">{{ $t('confirm') }}</a-button>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { CI_DEFAULT_ATTR } from '@/modules/cmdb/utils/const.js'

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
      // Is the right side sortable?
      type: Boolean,
      default: true,
    },
    isFixable: {
      // Can the right side be fixed?
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
    showDefaultAttr: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      selectedKeys: [],
      defaultAttrList: [
        {
          title: 'cmdb.components.updater',
          name: 'updater',
          key: CI_DEFAULT_ATTR.UPDATE_USER
        },
        {
          title: 'cmdb.components.updateTime',
          name: 'update time',
          key: CI_DEFAULT_ATTR.UPDATE_TIME
        }
      ]
    }
  },
  computed: {
    rightDefaultAttrList() {
      if (!this.showDefaultAttr) {
        return []
      }
      return this.defaultAttrList.filter((item) => this.targetKeys.includes(item.key))
    },

    leftDefaultAttrList() {
      if (!this.showDefaultAttr) {
        return []
      }
      return this.defaultAttrList.filter((item) => !this.targetKeys.includes(item.key))
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

    filterDefaultAttr(list) {
      return this.showDefaultAttr ? list.filter((item) => ![CI_DEFAULT_ATTR.UPDATE_USER, CI_DEFAULT_ATTR.UPDATE_TIME].includes(item.key)) : list
    }
  },
}
</script>

<style lang="less">

.cmdb-transfer {
  .ant-transfer-list {
    background-color: #f9fbff;
    border-color: #e4e7ed;
    .ant-transfer-list-header {
      background-color: #f9fbff;
      border-bottom: none;
      .ant-transfer-list-header-title {
        color: @primary-color;
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
          color: @primary-color;
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
            color: @primary-color;
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
        background-color: @primary-color_5;
        border-color: @primary-color;
      }
    }
  }

  .default-attr {
    .ant-divider {
      margin: 7px 0;
      padding: 0 15px;

      .ant-divider-inner-text {
        padding: 0 6px;
      }
    }

    &-divider {
      font-size: 12px;
      color: #86909C;
    }

    &-title {
      font-size: 14px;
      line-height: 14px;
      font-weight: 400;
    }

    &-name {
      font-size: 11px;
      line-height: 12px;
      color: rgb(163, 163, 163);
    }

    &-arrow {
      position: absolute;
      top: 9px;
      display: none;
      cursor: pointer;
      font-size: 12px;
      background-color: #fff;
      color: @primary-color;
      border-radius: 4px;
      width: 12px;
    }

    &-item {
      padding-left: 34px;
      padding-top: 4px;
      padding-bottom: 4px;
      position: relative;
      border-left: solid 2px transparent;
      margin-bottom: 6px;

      &-selected {
        background-color: #f0f5ff;
        border-color: #2f54eb;
      }

      &:hover {
        background-color: #f0f5ff;

        .default-attr-arrow {
          display: inline;
        }
      }
    }
  }
}
</style>
