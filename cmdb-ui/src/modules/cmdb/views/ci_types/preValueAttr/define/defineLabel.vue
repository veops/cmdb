<template>
  <div>
    <a-popover
      :visible="popoverVisible"
      placement="bottom"
      trigger="focus"
      overlayClassName="pre-value-edit-popover"
      @visibleChange="handleVisibleChange"
    >
      <div @click="popoverVisible = true" ref="popoverLabelRef">
        <a-input
          v-show="!labelData.label || popoverVisible"
          type="text"
          :style="{ width: '210px' }"
          :value="labelData.label"
          @change="changeLabel"
        >
        </a-input>

        <div
          class="pre-value-tag"
          :style="labelData.style ? labelData.style : {}"
          v-show="!popoverVisible && labelData.label"
        >
          <span>
            <img
              v-if="labelData.icon.id && labelData.icon.url"
              :src="`/api/common-setting/v1/file/${labelData.icon.url}`"
              :style="{ maxHeight: '12px', maxWidth: '12px', marginRight: '5px' }"
            />
            <ops-icon
              v-else-if="labelData.icon.name"
              :type="labelData.icon.name"
              :style="{ marginRight: '5px', color: labelData.icon.color || '#595959' }"
            />
            <a-tooltip :title="labelData.label">
              <span class="pre-value-tag-text">{{ labelData.label }}</span>
            </a-tooltip>
          </span>
        </div>
      </div>

      <div ref="preValueEdit" slot="content">
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">{{ $t('icon') }}</a-divider>
        <CustomIconSelect
          :style="{ marginLeft: '10px' }"
          :value="labelData.icon"
          @change="changeIcon"
        />
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">{{ $t('cmdb.ciType.font') }}</a-divider>
        <div :style="{ display: 'flex', justifyContent: 'space-around' }">
          <div
            @click="changeFontStyle('fontWeight', 'bold')"
            :class="`attributes-font-icon ${labelData.style.fontWeight === 'bold' ? 'attributes-font-icon-selected' : ''}`"
          >
            <a-icon type="bold" />
          </div>
          <div
            @click="changeFontStyle('fontStyle', 'italic')"
            :class="`attributes-font-icon ${labelData.style.fontStyle === 'italic' ? 'attributes-font-icon-selected' : ''}`"
          >
            <a-icon type="italic" />
          </div>
          <div
            @click="changeFontStyle('textDecoration', 'underline')"
            :class="
              `attributes-font-icon ${labelData.style.textDecoration === 'underline' ? 'attributes-font-icon-selected' : ''}`
            "
          >
            <a-icon type="underline" />
          </div>
        </div>

        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">{{ $t('cmdb.ciType.color') }}</a-divider>
        <div :style="{ display: 'flex', justifyContent: 'space-around' }">
          <div class="attributes-font-color">
            <a-icon type="font-colors" />
            <el-color-picker
              size="mini"
              :value="labelData.style.color"
              @change="(v) => changeFontStyle('color', v)"
              :predefine="defaultBGColors"
            >
            </el-color-picker>
          </div>
          <div class="attributes-font-color">
            <a-icon type="bg-colors" />
            <el-color-picker
              size="mini"
              :value="labelData.style.backgroundColor"
              @change="(v) => changeFontStyle('backgroundColor', v)"
              :predefine="defaultBGColors"
            >
            </el-color-picker>
          </div>
        </div>
        <a-divider orientation="left" style="margin:8px 0;color:gray;font-size:10px;">{{ $t('operation') }}</a-divider>
        <div style="text-align:right;">
          <a-tooltip
            :title="$t('delete')"
          >
            <a>
              <a-icon
                @click="handleDelete"
                style="margin-right:10px;color:red;"
                type="delete"
              />
            </a>
          </a-tooltip>
          <a-tooltip
            :title="$t('confirm')"
          >
            <a>
              <a-icon @click="popoverVisible = false" style="margin-right:10px;color:green;" type="check"/>
            </a>
          </a-tooltip>
        </div>
      </div>
    </a-popover>
  </div>
</template>

<script>
import { ColorPicker } from 'element-ui'
import CustomIconSelect from '@/components/CustomIconSelect'
import { defautValueColor, defaultBGColors } from '@/modules/cmdb/utils/const.js'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
locale.use(lang)

export default {
  name: 'DefineLabel',
  components: { ElColorPicker: ColorPicker, CustomIconSelect },
  props: {
    labelData: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      defautValueColor,
      defaultBGColors,
      popoverVisible: false,
    }
  },
  mounted() {
    document.addEventListener('click', this.eventListener)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.eventListener)
  },
  methods: {
    eventListener(e) {
      if (this.popoverVisible) {
        const dom = this.$refs.preValueEdit
        const dom_label = this.$refs.popoverLabelRef
        const dom_icon = document.getElementById(`custom-icon-select-popover`)
        e.stopPropagation()
        e.preventDefault()
        if (dom) {
          const isSelf =
            dom.contains(e.target) || (dom_label && dom_label.contains(e.target)) || (dom_icon && dom_icon.contains(e.target))
          if (!isSelf) {
            this.popoverVisible = false
          }
        }
      }
    },

    handleDelete() {
      this.popoverVisible = false
      this.$emit('deleteData')
    },

    changeFontStyle(key, value) {
      const style = {
        ...(this.labelData.style || {}),
        [key]: this.labelData.style[key] === value ? 'initial' : value,
      }
      this.$emit('change', 'style', style)
    },

    changeLabel(e) {
      const value = e.target.value
      this.$emit('change', 'label', value)
    },

    changeIcon(value) {
      this.$emit('change', 'icon', value)
    },

    handleVisibleChange(v) {
      if (!v) {
        this.popoverVisible = false
      }
    }
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
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  position: relative;
  cursor: pointer;
  max-width: 100%;

  &-text {
    overflow: hidden;
    text-wrap: nowrap;
    text-overflow: ellipsis;
    max-width: 100%;
  }

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
