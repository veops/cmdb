<template>
  <div style="display:inline;position:relative">
    <a-popover v-if="inputVisible" :visible="true" placement="bottom" overlayClassName="pre-value-edit-popover">
      <a-input
        ref="input"
        type="text"
        size="small"
        :style="{ width: '150px', marginBottom: type === 'add' ? '10px' : '5px' }"
        v-model="inputValue"
        class="pre-value-tag-input"
      >
      </a-input>
      <div ref="preValueEdit" slot="content">
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">图标</a-divider>
        <IconArea ref="iconArea" />
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">字体</a-divider>
        <div :style="{ display: 'flex', justifyContent: 'space-around' }">
          <div
            @click="changeFontStyle('fontWeight', 'bold')"
            :class="`attributes-font-icon ${style.fontWeight === 'bold' ? 'attributes-font-icon-selected' : ''}`"
          >
            <a-icon type="bold" />
          </div>
          <div
            @click="changeFontStyle('fontStyle', 'italic')"
            :class="`attributes-font-icon ${style.fontStyle === 'italic' ? 'attributes-font-icon-selected' : ''}`"
          >
            <a-icon type="italic" />
          </div>
          <div
            @click="changeFontStyle('textDecoration', 'underline')"
            :class="
              `attributes-font-icon ${style.textDecoration === 'underline' ? 'attributes-font-icon-selected' : ''}`
            "
          >
            <a-icon type="underline" />
          </div>
        </div>

        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">颜色</a-divider>
        <div :style="{ display: 'flex', justifyContent: 'space-around' }">
          <div class="attributes-font-color">
            <a-icon type="font-colors" /><el-color-picker
              size="mini"
              v-model="style.color"
              :predefine="defaultBGColors"
            >
            </el-color-picker>
          </div>
          <div class="attributes-font-color">
            <a-icon type="bg-colors" /><el-color-picker
              size="mini"
              v-model="style.backgroundColor"
              :predefine="defaultBGColors"
            >
            </el-color-picker>
          </div>
        </div>
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">操作</a-divider>
        <div style="text-align:right;">
          <a-tooltip
            v-if="type !== 'add'"
            title="删除"
          ><a
          ><a-icon
            @click="handleDelete"
            v-if="type !== 'add'"
            style="margin-right:10px;color:red;"
            type="delete"/></a
            ></a-tooltip>
          <a-tooltip
            title="确定"
          ><a><a-icon @click="handleEditOk" style="margin-right:10px;color:green;" type="check"/></a
          ></a-tooltip>
          <a-tooltip
            title="取消"
          ><a
          ><a-icon
            @click="
              () => {
                inputVisible = false
              }
            "
            style="color:gray;"
            type="close"/></a
            ></a-tooltip>
        </div>
      </div>
    </a-popover>
    <div
      ref="valueTag"
      :class="`handle ${type === 'edit' ? 'pre-value-tag' : ''}`"
      v-else
      :style="type === 'edit' && item[1] && item[1].style ? item[1].style : {}"
      @click="
        (e) => {
          if (!disabled) {
            e.preventDefault()
            handleEdit()
          }
        }
      "
    >
      <span :style="{ cursor: disabled ? 'default' : 'move' }">
        <img
          v-if="icon.id && icon.url"
          :src="`/api/common-setting/v1/file/${icon.url}`"
          :style="{ maxHeight: '12px', maxWidth: '12px', marginRight: '5px' }"
        />
        <ops-icon
          v-else-if="icon.name"
          :type="icon.name"
          :style="{ marginRight: '5px', color: icon.color || '#595959' }"
        />
        <span>{{ item[0] }}</span>
      </span>
      <a
        class="pre-value-tag-dropdown"
        @click="
          (e) => {
            if (!disabled) {
              e.preventDefault()
              handleEdit()
            }
          }
        "
      >
        <a-icon class="pre-value-tag-dropdown-icon" v-if="type === 'edit' && !disabled" type="down" />
        <slot v-else></slot>
      </a>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { ColorPicker } from 'element-ui'
import { defautValueColor, defaultBGColors } from '../../utils/const'
import IconArea from './iconArea.vue'
export default {
  name: 'PreValueTag',
  components: { ElColorPicker: ColorPicker, IconArea },
  props: {
    item: {
      type: Array,
      default: () => [],
    },
    type: {
      type: String,
      default: 'edit',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      defautValueColor,
      defaultBGColors,
      inputVisible: false,
      inputValue: '',
      style: {},
      icon: {},
    }
  },
  mounted() {
    document.addEventListener('click', this.eventListener)
    this.style = _.cloneDeep(this.item[1]?.style || {})
    this.icon = _.cloneDeep(this.item[1]?.icon || {})
  },
  beforeDestroy() {
    document.removeEventListener('click', this.eventListener)
  },
  methods: {
    eventListener(e) {
      if (this.inputVisible) {
        const dom = this.$refs.preValueEdit
        const dom_input = this.$refs.input.$el
        const dom_icon = document.getElementById(`custom-icon-select-popover`)
        e.stopPropagation()
        e.preventDefault()
        if (dom) {
          const isSelf =
            dom.contains(e.target) || dom_input.contains(e.target) || (dom_icon && dom_icon.contains(e.target))
          if (!isSelf) {
            this.inputVisible = false
          }
        }
      }
    },
    handleDelete() {
      this.$emit('deleteValue', this.item)
      this.inputVisible = false
    },
    handleEdit() {
      this.style = _.cloneDeep(this.item[1]?.style || {})
      this.icon = _.cloneDeep(this.item[1]?.icon || {})
      setTimeout(() => {
        this.inputVisible = true
        this.inputValue = this.item[0]

        this.$nextTick(() => {
          this.$refs.input.focus()
          this.$nextTick(() => {
            this.$refs.iconArea.setIcon(this.icon)
          })
        })
      }, 100)
    },
    handleEditOk() {
      const icon = this.$refs.iconArea.getIcon()
      if (this.type === 'edit') {
        this.icon = { ...icon, color: icon && icon.name && icon.name.startsWith('icon-') ? icon.color || '' : '' }
        this.$emit('editValue', this.item, this.inputValue, this.style, this.icon)
      } else {
        this.$emit('add', this.inputValue, this.style, icon)
      }
      this.inputVisible = false
    },
    changeFontStyle(key, value) {
      this.style = {
        ..._.cloneDeep(this.style),
        [key]: this.style[key] === value ? 'initial' : value,
      }
    },
  },
}
</script>

<style lang="less" scoped>
.pre-value-edit-color {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  .pre-value-edit-color-item {
    cursor: pointer;
    display: inline-block;
    width: 25px;
    height: 20px;
    margin: 5px;
  }
}
.pre-value-tag {
  display: inline-block;
  margin: 5px 15px 5px 0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  position: relative;
  > span {
    display: flex;
    align-items: center;
  }
  &:hover .pre-value-tag-dropdown-icon {
    display: inline !important;
  }

  .pre-value-tag-dropdown {
    font-size: 10px;
    color: #999999;
    &:hover {
      color: #2f54eb;
    }
    .pre-value-tag-dropdown-icon {
      display: none;
      position: absolute;
      right: -10px;
      top: 8px;
    }
  }
}
</style>
<style lang="less">
.pre-value-tag-input {
  border: none;
  border-bottom: 1px solid #d9d9d9;
  font-size: 12px;
  &:focus {
    box-shadow: none;
  }
}
.pre-value-edit-popover.ant-popover-placement-top .ant-popover-content {
  margin-bottom: -10px;
}
.pre-value-edit-popover.ant-popover-placement-bottom .ant-popover-content {
  margin-top: -10px;
}
.pre-value-edit-popover {
  .ant-popover-content {
    width: 150px;
    .ant-popover-arrow {
      display: none;
    }
    .ant-popover-inner-content {
      padding: 3px 4px;
    }
  }
  .attributes-font-icon {
    cursor: pointer;
    display: inline-block;
    width: 30px;
    height: 30px;
    position: relative;
    border: 1px solid #fff;
    &:hover {
      background-color: #eeeeee;
      border-color: #606266;
    }
    > i {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }
  }
  .attributes-font-icon-selected {
    background-color: #eeeeee;
  }
  .attributes-font-color {
    display: inline-flex;
    align-items: center;
    width: 50%;
    justify-content: center;
  }
}
</style>
