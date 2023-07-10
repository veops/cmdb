<template>
  <div ref="splitPane" class="split-pane" :class="direction + ' ' + appName" :style="{ flexDirection: direction }">
    <div class="pane pane-one" ref="one" :style="lengthType + ':' + paneLengthValue1">
      <slot name="one"></slot>
    </div>

    <div class="spliter-wrap">
      <a-button
        v-show="collapsable"
        :icon="isExpanded ? 'left' : 'right'"
        class="collapse-btn"
        @click="handleExpand"
      ></a-button>
      <div
        class="pane-trigger"
        @mousedown="handleMouseDown"
        :style="{ backgroundColor: triggerColor, width: `${triggerLength}px` }"
      ></div>
    </div>

    <div class="pane pane-two" ref="two" :style="lengthType + ':' + paneLengthValue2">
      <slot name="two"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SplitPane',
  props: {
    direction: {
      type: String,
      default: 'row',
    },

    min: {
      type: Number,
      default: 10,
    },

    max: {
      type: Number,
      default: 90,
    },

    paneLengthPixel: {
      type: Number,
      default: 220,
    },

    triggerLength: {
      type: Number,
      default: 8,
    },

    appName: {
      type: String,
      default: 'viewer',
    },

    collapsable: {
      type: Boolean,
      default: false,
    },
    triggerColor: {
      type: String,
      default: '#f0f2f5',
    },
  },
  data() {
    return {
      triggerLeftOffset: 0, // 鼠标距滑动器左(顶)侧偏移量
      isExpanded: localStorage.getItem(`${this.appName}-isExpanded`)
        ? JSON.parse(localStorage.getItem(`${this.appName}-isExpanded`))
        : false,
      parentContainer: null,
    }
  },
  computed: {
    lengthType() {
      return this.direction === 'row' ? 'width' : 'height'
    },

    minLengthType() {
      return this.direction === 'row' ? 'minWidth' : 'minHeight'
    },

    paneLengthValue1() {
      return `calc(${this.paneLengthPercent}% - ${this.triggerLength / 2 + 'px'})`
    },

    paneLengthValue2() {
      const rest = 100 - this.paneLengthPercent
      return `calc(${rest}% - ${this.triggerLength / 2 + 'px'})`
    },

    paneLengthPercent() {
      const clientRectWidth = this.parentContainer
        ? this.parentContainer.clientWidth
        : document.documentElement.getBoundingClientRect().width
      return (this.paneLengthPixel / clientRectWidth) * 100
    },
  },

  watch: {
    isExpanded(newValue) {
      if (newValue) {
        document.querySelector(`.${this.appName} .pane-two`).style.display = 'none'
      } else {
        document.querySelector(`.${this.appName} .pane-two`).style.display = ''
      }
    },
  },

  mounted() {
    this.parentContainer = document.querySelector(`.${this.appName}`)
    if (this.isExpanded) {
      document.querySelector(`.${this.appName} .pane-two`).style.display = 'none'
    } else {
      document.querySelector(`.${this.appName} .pane-two`).style.display = ''
    }
  },

  methods: {
    // 按下滑动器
    handleMouseDown(e) {
      document.addEventListener('mousemove', this.handleMouseMove)
      document.addEventListener('mouseup', this.handleMouseUp)
      if (this.direction === 'row') {
        this.triggerLeftOffset = e.pageX - e.srcElement.getBoundingClientRect().left
      } else {
        this.triggerLeftOffset = e.pageY - e.srcElement.getBoundingClientRect().top
      }
    },

    // 按下滑动器后移动鼠标
    handleMouseMove(e) {
      this.isExpanded = false
      this.$emit('expand', this.isExpanded)
      const clientRect = this.$refs.splitPane.getBoundingClientRect()
      let paneLengthPixel = 0

      if (this.direction === 'row') {
        const offset = e.pageX - clientRect.left - this.triggerLeftOffset + this.triggerLength / 2
        paneLengthPixel = offset
      } else {
        const offset = e.pageY - clientRect.top - this.triggerLeftOffset + this.triggerLength / 2
        paneLengthPixel = offset
      }

      if (paneLengthPixel < this.min) {
        paneLengthPixel = this.min
      }
      if (paneLengthPixel > this.max) {
        paneLengthPixel = this.max
      }

      this.$emit('update:paneLengthPixel', paneLengthPixel)

      localStorage.setItem(`${this.appName}-paneLengthPixel`, paneLengthPixel)
    },

    // 松开滑动器
    handleMouseUp() {
      document.removeEventListener('mousemove', this.handleMouseMove)
    },

    handleExpand() {
      this.isExpanded = !this.isExpanded
      this.$emit('expand', this.isExpanded)
      localStorage.setItem(`${this.appName}-isExpanded`, this.isExpanded)
    },
  },
}
</script>

<style scoped lang="less">
@import './index.less';
</style>
