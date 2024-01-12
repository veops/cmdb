<template>
    <a-popover
      trigger="click"
      placement="bottom"
      ref="regexSelect"
      overlayClassName="regex-select-wrapper"
      :overlayStyle="{ '--overlay-width': `${width}px` }"
      @visibleChange="visibleChange"
    >
      <div class="regex-select" slot="content">
        <div class="regex-select-left">
          <div class="regex-select-left-header">{{ $t('regexSelect.limitedFormat') }}</div>
          <div
            @click="
              () => {
                current = reg
                testInput = ''
                showMessage = false
              }
            "
            :class="{
              'regex-select-left-reg': true,
              'regex-select-left-reg-selected': current && current.label === reg.label,
            }"
            v-for="(reg, index) in regList"
            :key="reg.label"
          >
            <a-divider :style="{ margin: '2px -12px', width: 'calc(100% + 24px)' }" v-if="index === regList.length - 1" />
            {{ reg.label }}
          </div>
        </div>
        <div class="regex-select-right">
          <template v-if="current">
            <div class="regex-select-right-header">{{ $t('regexSelect.regExp') }}</div>
            <div
              v-if="current.label !== $t('regexSelect.custom')"
              :style="{ color: '#000', fontSize: '12px', margin: '12px 0' }"
            >
              {{ current.value }}
            </div>
            <a-input
              :style="{ margin: '12px 0' }"
              size="small"
              v-else
              v-model="current.value"
              @change="
                () => {
                  this.$emit('change', current)
                }
              "
            />
            <template v-if="isShowErrorMsg">
              <div class="regex-select-right-header">{{ $t('regexSelect.errMsg') }}</div>
              <a-input :style="{ margin: '12px 0' }" size="small" v-model="current.message" />
            </template>
            <div class="regex-select-right-header">{{ $t('regexSelect.test') }}</div>
            <a-input v-model="testInput" :style="{ margin: '12px 0 4px' }" size="small" @change="validate" />
            <span :style="{ color: 'red', fontSize: '12px' }" v-if="showMessage">{{
              locale === 'zh' ? current.message || '错误' : $t('regexSelect.error')
            }}</span>
          </template>
        </div>
      </div>
      <a-input ref="regInput" :placeholder="$t('regexSelect.placeholder')" :value="current.label" @change="changeLabel">
      </a-input>
    </a-popover>
  </template>
  
  <script>
  import { mapState } from 'vuex'
  import { regList } from './constants'
  export default {
    name: 'RegexSelect',
    model: {
      prop: 'value',
      event: 'change',
    },
    props: {
      value: {
        type: Object,
        default: () => {},
      },
      isShowErrorMsg: {
        type: Boolean,
        default: true,
      },
      limitedFormat: {
        type: Array,
        default: () => [],
      },
    },
    data() {
      return {
        showMessage: false,
        width: 370,
        testInput: '',
      }
    },
    computed: {
      ...mapState(['locale']),
      regList() {
        if (this.limitedFormat.length) {
          return regList().filter((item) => this.limitedFormat.includes(item.id))
        }
        return regList()
      },
      current: {
        get() {
          if (this.value?.value && !this.value?.label) {
            const _find = this.regList.find((reg) => reg.value === this.value?.value)
            return { ...this.value, label: _find?.label ?? this.$t('regexSelect.custom') }
          }
          return this.value ?? {}
        },
        set(val) {
          this.showMessage = false
          this.$emit('change', val)
          return val
        },
      },
    },
    mounted() {
      this.$nextTick(() => {
        const regInput = this.$refs.regInput.$refs.input
        this.width = regInput.offsetWidth || 370
      })
    },
    methods: {
      validate(e) {
        const reg = RegExp(this.current.value, 'g')
        this.showMessage = !reg.test(e.target.value)
      },
      changeLabel(e) {
        this.current = {}
      },
      visibleChange(visible) {
        if (visible) {
          this.$nextTick(() => {
            this.testInput = ''
            this.showMessage = false
          })
        }
      },
    },
  }
  </script>
  
  <style lang="less" scoped>
  @import '~@/style/static.less';
  .regex-select {
    width: 100%;
    height: 300px;
    display: flex;
    .regex-select-left {
      width: 40%;
      height: 100%;
      border: 1px solid #cacdd9;
      border-radius: 4px;
      padding: 12px;
      &-reg {
        padding-left: 2px;
        cursor: pointer;
        &-selected,
        &:hover {
          color: #custom_colors[color_1];
        }
      }
    }
    &-right {
      flex: 1;
      height: 100%;
      border: 1px solid #cacdd9;
      border-radius: 4px;
      margin-left: 8px;
      padding: 12px;
    }
    &-left,
    &-right {
      &-header {
        font-weight: 400;
        font-size: 14px;
        color: #000000;
        border-left: 2px solid #custom_colors[color_1];
        padding-left: 6px;
        margin-left: -6px;
      }
    }
  }
  </style>
  
  <style lang="less">
  .regex-select-wrapper {
    .ant-popover-arrow {
      display: none;
    }
    .ant-popover-inner-content {
      padding: 0;
      min-width: 370px;
      width: var(--overlay-width);
    }
  }
  .regex-select-wrapper.ant-popover-placement-bottom .ant-popover-content {
    margin-top: -8px;
  }
  .regex-select-wrapper.ant-popover-placement-top .ant-popover-content {
    margin-bottom: -8px;
  }
  </style>  