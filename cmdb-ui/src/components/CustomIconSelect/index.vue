<template>
  <a-popover
    :visible="visible"
    overlayClassName="custom-icon-select-popover"
    :destroyTooltipOnHide="true"
    placement="bottom"
  >
    <div id="custom-icon-select-popover" slot="content">
      <div class="custom-icon-select-popover-icon-type">
        <div
          :class="`${currentIconType === item.value ? 'selected' : ''}`"
          v-for="item in iconTypeList"
          :key="item.value"
          @click="handleChangeIconType(item.value)"
        >
          {{ item.label }}
        </div>
      </div>
      <div class="custom-icon-select-popover-content">
        <div v-for="category in iconList" :key="category.value">
          <h4 class="category">{{ category.label }}</h4>
          <div class="custom-icon-select-popover-content-wrapper">
            <div
              v-for="name in category.list"
              :key="name.value"
              :class="`custom-icon-select-popover-item ${value.name === name.value ? 'selected' : ''}`"
              @click="clickIcon(name.value)"
            >
              <ops-icon :type="name.value" />
              <span class="custom-icon-select-popover-item-label">{{ name.label }}</span>
            </div>
          </div>
        </div>
      </div>
      <template v-if="currentIconType !== '0' && currentIconType !== '3'">
        <a-divider :style="{ margin: '5px 0' }" />
        <el-color-picker size="mini" v-model="value.color"> </el-color-picker>
      </template>
    </div>

    <div class="custom-icon-select-block" id="custom-icon-select-block" @click="showSelect">
      <ops-icon
        :type="value.name"
        :style="{ color: value.name && value.name.startsWith('icon-') ? value.color || '' : '' }"
      />
    </div>
  </a-popover>
</template>

<script>
import { ColorPicker } from 'element-ui'
import {
  iconTypeList,
  commonIconList,
  linearIconList,
  fillIconList,
  multicolorIconList,
} from './constants'
export default {
  name: 'CustomIconSelect',
  components: { ElColorPicker: ColorPicker },
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Object,
      default: () => {
        return { name: '', color: '' }
      },
    },
    iconType: {
      type: String,
      default: 'cmdb',
    },
  },
  data() {
    return {
      iconTypeList,
      commonIconList,
      linearIconList,
      fillIconList,
      multicolorIconList,
      visible: false,
      currentIconType: '1',
    }
  },
  computed: {
    iconList() {
      switch (this.currentIconType) {
        case '0': // 常用
          return this.commonIconList
        case '1': // 线性
          return this.linearIconList
        case '2': // 实底
          return this.fillIconList
        case '3': // 多色
          return this.multicolorIconList
        default:
          return this.linearIconList
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.eventListener)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.eventListener)
  },
  methods: {
    eventListener(e) {
      if (this.visible) {
        const dom = document.getElementById(`custom-icon-select-popover`)
        const dom_icon = document.getElementById(`custom-icon-select-block`)
        e.stopPropagation()
        e.preventDefault()
        if (dom) {
          const isSelf = dom.contains(e.target) || dom_icon.contains(e.target)
          if (!isSelf) {
            this.visible = false
          }
        }
      }
    },
    clickIcon(name) {
      // 当name一样时，取消选择
      if (name === this.value.name) {
        this.$emit('change', {
          name: '',
          color: '',
        })
      } else {
        this.$emit('change', {
          name,
          color: this.value.name && this.value.name.startsWith('icon-') ? this.value.color || '' : '',
        })
      }
    },
    showSelect() {
      this.visible = true
      if (!this.value.name) {
        this.currentIconType = '1'
        return
      }
      if (this.value.name.startsWith('changyong-')) {
        this.currentIconType = '0'
      } else if (this.value.name.startsWith('icon-xianxing')) {
        this.currentIconType = '1'
      } else if (this.value.name.startsWith('icon-shidi')) {
        this.currentIconType = '2'
      } else {
        this.currentIconType = '3'
      }
    },
    handleChangeIconType(value) {
      this.currentIconType = value
    },
  },
}
</script>

<style lang="less">
.custom-icon-select-popover.ant-popover-placement-top .ant-popover-content {
  margin-bottom: -10px;
}
.custom-icon-select-popover {
  width: 650px;
  overflow: auto;
  padding-top: 0;
  box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.1);
  .ant-popover-arrow {
    display: none;
  }
  .ant-popover-inner-content {
    padding: 4px 6px;
  }
  .custom-icon-select-popover-content {
    max-height: 400px;
    overflow: auto;
    .category {
      font-size: 14px;
    }
    .custom-icon-select-popover-content-wrapper {
      font-size: 24px;
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      margin-left: 10px;
      .custom-icon-select-popover-item {
        width: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        padding: 5px 5px 2px 5px;
        margin: 0 2px 6px;
        color: #666;
        .custom-icon-select-popover-item-label {
          margin-top: 6px;
          font-size: 11px;
        }
        &:hover {
          background-color: #eeeeee;
        }
      }
      .selected {
        background-color: #eeeeee;
      }
    }
  }
  .custom-icon-select-popover-icon-type {
    display: inline-block;
    > div {
      cursor: pointer;
      display: inline-block;
      padding: 2px 8px;
      border: 1px solid #eeeeee;
      &:hover {
        color: #2f54eb;
      }
    }
    .selected {
      border-color: #2f54eb;
    }
  }
}
</style>

<style lang="less" scoped>
.custom-icon-select-block {
  position: relative;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: 1px solid #eeeeee;
  display: inline-block;
  cursor: pointer;
  > i {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 18px;
  }
}
</style>
