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
        <div :class="`${currentIconType === '4' ? 'selected' : ''}`" @click="handleChangeIconType('4')">
          {{ this.$t('customIconSelect.custom') }}
        </div>
        <a-upload
          slot="description"
          name="avatar"
          :before-upload="beforeUpload"
          :show-upload-list="false"
          accept=".svg,.png,.jpg,.jpeg"
          v-if="currentIconType === '4'"
        >
          <a-button icon="plus" size="small" type="primary">{{ $t('add') }}</a-button>
        </a-upload>
      </div>
      <div class="custom-icon-select-popover-content">
        <template v-if="iconList && iconList.length">
          <template v-if="currentIconType !== '4'">
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
          </template>
          <div class="custom-icon-select-popover-content-wrapper" :style="{ marginTop: '10px' }" v-else>
            <div
              v-for="icon in iconList"
              :key="icon.id"
              :class="`custom-icon-select-popover-item ${value.id === icon.id ? 'selected' : ''}`"
              @click="clickCustomIcon(icon)"
            >
              <div class="custom-icon-select-popover-content-img-box">
                <img v-if="icon.data && icon.data.url" :src="`/api/common-setting/v1/file/${icon.data.url}`" />
                <a-popconfirm
                  overlayClassName="custom-icon-select-confirm-popover"
                  :getPopupContainer="(trigger) => trigger.parentNode"
                  :title="$t('confirmDelete')"
                  @confirm="(e) => deleteIcon(e, icon)"
                  @cancel="
                    (e) => {
                      e.stopPropagation()
                      e.preventDefault()
                    }
                  "
                >
                  <a-icon
                    type="close"
                    @click="
                      (e) => {
                        e.stopPropagation()
                        e.preventDefault()
                      }
                    "
                  />
                </a-popconfirm>
              </div>
              <span class="custom-icon-select-popover-item-label" :title="icon.data.name">{{ icon.data.name }}</span>
            </div>
          </div>
        </template>
        <a-empty v-else :style="{ marginTop: '15%' }">
          <img slot="image" :src="require('@/assets/data_empty.png')" />
          <a-upload
            slot="description"
            name="avatar"
            :before-upload="beforeUpload"
            :show-upload-list="false"
            accept=".svg,.png,.jpg,.jpeg"
          >
            <a> 暂无自定义图标，点击此处上传 </a>
          </a-upload>
        </a-empty>
      </div>
      <template v-if="!['0', '3', '4'].includes(currentIconType)">
        <a-divider :style="{ margin: '5px 0' }" />
        <el-color-picker size="mini" v-model="value.color"> </el-color-picker>
      </template>
      <a-form class="custom-icon-select-form" :form="form" v-show="currentIconType === '4' && formVisible">
        <a-form-item
          :label="$t('name')"
          :labelCol="{ span: 4 }"
          :wrapperCol="{ span: 16 }"
        ><a-input
          v-decorator="['name', { rules: [{ required: true, message: $t('placeholder1') }] }]"
        /></a-form-item>
        <a-form-item :label="$t('customIconSelect.preview')" :labelCol="{ span: 4 }">
          <div class="custom-icon-select-form-img">
            <img :src="formImg" />
          </div>
        </a-form-item>
        <a-form-item label=" " :colon="false" :labelCol="{ span: 16 }">
          <a-space>
            <a-button size="small" @click="handleCancel">{{ $t('cancel') }}</a-button>
            <a-button size="small" type="primary" @click="handleOk">{{ $t('confirm') }}</a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </div>

    <div class="custom-icon-select-block" :id="`custom-icon-select-block-${uuid}`" @click="showSelect">
      <img v-if="value.id && value.url" :src="`/api/common-setting/v1/file/${value.url}`" />
      <ops-icon
        v-else
        :type="value.name"
        :style="{ color: value.name && value.name.startsWith('icon-') ? value.color || '' : '' }"
      />
    </div>
  </a-popover>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import { ColorPicker } from 'element-ui'
import {
  iconTypeList,
  commonIconList,
  linearIconList,
  fillIconList,
  multicolorIconList,
} from './constants'
import { postImageFile, getFileData, addFileData, deleteFileData } from '@/api/file'

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
      form: this.$form.createForm(this),
      commonIconList,
      linearIconList,
      fillIconList,
      multicolorIconList,
      visible: false,
      currentIconType: '3',
      customIconList: [],
      formVisible: false,
      formImg: null,
      file: null,
      uuid: uuidv4(),
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
        case '4': // 自定义
          return this.customIconList
        default:
          return this.linearIconList
      }
    },
    fileName() {
      const splitFileName = this.file.name.split('.')
      return splitFileName.splice(0, splitFileName.length - 1).join('')
    },
    iconTypeList() {
      return iconTypeList()
    },
  },
  mounted() {
    document.addEventListener('click', this.eventListener)
    this.getFileData()
  },
  beforeDestroy() {
    document.removeEventListener('click', this.eventListener)
  },
  methods: {
    getFileData() {
      getFileData('ops-custom-icon').then((res) => {
        this.customIconList = res
      })
    },
    eventListener(e) {
      if (this.visible) {
        const dom = document.getElementById(`custom-icon-select-popover`)
        const dom_icon = document.getElementById(`custom-icon-select-block-${this.uuid}`)
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
    clickCustomIcon(icon) {
      if (icon.id === this.value.id) {
        this.$emit('change', {
          name: '',
          color: '',
        })
      } else {
        this.$emit('change', { name: icon.data.name, id: icon.id, url: icon?.data?.url })
      }
    },
    showSelect() {
      this.visible = true
      if (!this.value.name) {
        this.currentIconType = '3'
        return
      }
      // changyong已废弃
      if (this.value.name.startsWith('changyong-')) {
        this.currentIconType = '0'
      } else if (this.value.name.startsWith('icon-xianxing')) {
        this.currentIconType = '1'
      } else if (this.value.name.startsWith('icon-shidi')) {
        this.currentIconType = '2'
      } else if (this.value.name.startsWith('caise')) {
        this.currentIconType = '3'
      } else {
        this.currentIconType = '4'
      }
    },
    handleChangeIconType(value) {
      this.currentIconType = value
    },
    beforeUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error(this.$t('customIconSelect.sizeLimit'))
        return false
      }

      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        this.formVisible = true
        this.$nextTick(() => {
          this.file = file
          this.formImg = reader.result
          this.form.setFieldsValue({ name: this.fileName })
        })
      }
      return false
    },
    handleCancel() {
      this.formVisible = false
      this.form.setFieldsValue({ name: '' })
      this.formImg = null
    },
    handleOk() {
      const fm = new FormData()
      fm.append('file', this.file)
      postImageFile(fm).then((res) => {
        this.form.validateFields((err, values) => {
          if (!err) {
            addFileData('ops-custom-icon', { data: { name: values.name, url: res.file_name } }).then(() => {
              this.$message.success(this.$t('uploadSuccess'))
              this.handleCancel()
              this.getFileData()
            })
          }
        })
      })
    },
    deleteIcon(e, icon) {
      e.stopPropagation()
      e.preventDefault()
      deleteFileData('ops-custom-icon', icon.id).then(() => {
        this.$message.success(this.$t('deleteSuccess'))
        this.handleCancel()
        this.getFileData()
      })
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
    height: 400px;
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
        position: relative;
        .custom-icon-select-popover-item-label {
          margin-top: 6px;
          font-size: 11px;
          width: 100%;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          text-align: center;
        }
        &:hover {
          background-color: #eeeeee;
          .custom-icon-select-popover-content-img-box > i {
            display: inline;
          }
        }
        .custom-icon-select-popover-content-img-box {
          width: 26px;
          height: 26px;
          display: flex;
          align-items: center;
          justify-content: center;
          > img {
            max-width: 26px;
            max-height: 26px;
          }

          > i {
            display: none;
            position: absolute;
            top: 2px;
            right: 2px;
            font-size: 12px;
            &:hover {
              color: #2f54eb;
            }
          }
        }
      }
      .selected {
        background-color: #eeeeee;
      }
    }
  }
  .custom-icon-select-popover-icon-type {
    display: inline-block;
    width: 100%;
    position: relative;
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
    .ant-btn {
      position: absolute;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
    }
  }

  .custom-icon-select-confirm-popover .ant-popover-inner-content {
    width: 150px;
  }
}
</style>

<style lang="less" scoped>
.custom-icon-select-block {
  position: relative;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  display: inline-block;
  cursor: pointer;
  > i,
  > img {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  > img {
    max-width: 26px;
    max-height: 26px;
  }
  > i {
    font-size: 18px;
  }
}
.custom-icon-select-form {
  .custom-icon-select-form-img {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    display: inline-flex;
    margin-top: 5px;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    img {
      max-width: 26px;
      max-height: 26px;
    }
  }
}
</style>
