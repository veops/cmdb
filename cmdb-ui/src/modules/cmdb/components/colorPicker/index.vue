<template>
  <div class="color-picker">
    <!-- 选中的颜色 -->
    <!-- <div class="color-button">
      <div class="back-ground">
        <div class="contain" :style="{ backgroundColor: realShowColor }" @click="isShowDropDown">
          <a-icon type="down" />
        </div>
      </div>
    </div> -->
    <!-- 颜色选择器 -->
    <div class="color-dropdown">
      <div class="color-dropdown-picker">
        <!-- 颜色面板 -->
        <div
          ref="colorPannel"
          class="color-pannel-box"
          @click="pannelMosueClick($event)"
          :style="{ backgroundColor: colorPannel.backgroundColor }"
        >
          <div
            :style="{ top: colorPannel.top + 'px', left: colorPannel.left + 'px' }"
            class="color-select-circle"
            @mousedown="pannelMosueHandler($event)"
          ></div>
        </div>
        <!-- 色相柱 -->
        <div ref="colorBar" class="color-slider-box">
          <div class="color-slider"></div>
          <div class="color-thumb" :style="{ top: colorBar.top + 'px' }" @mousedown="thumbMouseHandler($event)"></div>
        </div>
      </div>
      <!-- 透明条 -->
      <!-- <div v-if="showAlpha" ref="alphaBar" class="color-alpha">
        <div
          class="color-alpha-bar"
          :style="{
            background: `linear-gradient(to right, ${alphaColorBar.barColor}, ${rgbToRgba(alphaColorBar.barColor, 0)})`,
          }"
        ></div>
        <div
          class="color-alpha-thumb"
          :style="{ left: alphaColorBar.thumbLeft + 'px' }"
          @mousedown="alphaBarMouseHandler($event)"
        ></div>
      </div> -->
      <div class="color-input">
        <a-input
          size="small"
          v-model="realShowColor"
          class="color-input-box"
          type="text"
          style="width:130px"
          @pressEnter="changeInputColor"
        />
        <!-- <button @click="submitColor">确定</button> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ColorPicker',
  props: {
    // 是否开启透明度
    // showAlpha: {
    //   type: Boolean,
    //   default() {
    //     return true
    //   },
    // },
    // 初始化颜色，使用该组件时传入的默认颜色：支持hex、rgb格式
    initColor: {
      type: String,
      default() {
        return '#f00'
      },
    },
    // input中展示的颜色格式: hex、rgb
    colorFormat: {
      type: String,
      default() {
        return 'hex'
      },
    },
  },
  data() {
    return {
      colorConfig: {
        h: 360,
        s: 100,
        v: 100,
        alpha: 1,
        value: '',
        // 底色
        basicColor: '',
      },
      alphaColorBar: {
        barColor: 'rgb(255, 0, 0)',
        thumbLeft: 0,
        width: 0,
      },
      colorBar: {
        top: 0,
        height: 0,
      },
      colorPannel: {
        top: 0,
        left: 300,
        backgroundColor: '#f00',
        height: 0,
        width: 0,
      },
      // 默认红色
      realShowColor: '#f00',
      isShow: true,
      isApply: false,
    }
  },
  mounted() {
    this.initShowColor(this.initColor)
  },
  methods: {
    // 初始化
    initShowColor(color) {
      // 初始化hsv颜色、格式化的颜色值
      let hsvObj, initRgb
      if (color.indexOf('#') !== -1) {
        initRgb = this.hexToRGB(color)
        hsvObj = this.rgbToHSV(initRgb)
      } else if (color.indexOf('rgb') !== -1) {
        hsvObj = this.rgbToHSV(color)
      } else {
        throw new Error('初始化颜色格式错误，使用#fff或rgb格式')
        // this.$message.error('颜色格式错误，使用16进制格式')
      }
      if (hsvObj) {
        this.colorConfig.h = hsvObj.h
        this.colorConfig.s = hsvObj.s
        this.colorConfig.v = hsvObj.v
      }
      // 获取容器高宽
      this.colorBar.height = this.$refs.colorBar.getBoundingClientRect().height
      this.colorPannel.height = this.$refs.colorPannel.getBoundingClientRect().height
      this.colorPannel.width = this.$refs.colorPannel.getBoundingClientRect().width
      if (this.showAlpha) {
        this.alphaColorBar.width = this.$refs.alphaBar.getBoundingClientRect().width
        // 根据alpha获取滑块位置
        this.alphaToPosition(this.colorConfig.alpha, this.alphaColorBar.width)
        this.alphaColorBar.barColor = initRgb || color
      }
      // 根据hsv获取位置
      this.colorPannel.backgroundColor = this.hueToRGB(this.colorConfig.h)
      this.hsvToPosition(this.colorConfig.s, this.colorConfig.v, this.colorPannel.width, this.colorPannel.height)
      this.hueToPosition(this.colorConfig.h, this.colorBar.height)

      // 根据colorFormat和showAlpha格式化颜色
      this.colorForamtTransform()

      this.realShowColor = this.colorConfig.value || this.initColor
    },
    // isShowDropDown() {
    //   this.isShow = !this.isShow
    // },
    submitColor() {
      // 如果颜色为rgba形式将转换为rgb。
      let initColor
      if (this.realShowColor.indexOf('rgba') !== -1) {
        initColor = this.realShowColor.replace(/,\d{1,3}(?=\))/, '')
        // 获取输入的alpha
        this.colorConfig.alpha = parseFloat(this.realShowColor.split(',')[3].replace(')', ''))
        this.colorConfig.alpha = Math.max(0, this.colorConfig.alpha)
        this.colorConfig.alpha = Math.min(this.colorConfig.alpha, 1)
      } else {
        initColor = this.realShowColor
      }
      this.initShowColor(initColor)
      this.isShow = false
    },
    // 色相柱的拖拽事件
    thumbMouseHandler(e) {
      if (e.type === 'mousedown') {
        document.body.addEventListener('mousemove', this.thumbMouseHandler)
        document.body.addEventListener('mouseup', this.thumbMouseHandler)
      } else if (e.type === 'mousemove') {
        const elemInfo = this.$refs.colorBar.getBoundingClientRect()

        this.colorBar.top = e.clientY - elemInfo.top
        this.colorBar.top = Math.max(0, this.colorBar.top)
        this.colorBar.top = Math.min(this.colorBar.top, elemInfo.height)
        this.colorConfig.h = ((parseInt(this.colorBar.top) / elemInfo.height) * 360 * 100) / 100
        // 色相[0,360)
        if (this.colorConfig.h === 360) {
          this.colorConfig.h = 0
        }

        // 获取颜色面板背景色
        this.colorPannel.backgroundColor = this.hueToRGB(this.colorConfig.h)
        this.colorForamtTransform()
        this.alphaColorBar.barColor = this.colorConfig.basicColor
        this.realShowColor = this.colorConfig.value
      } else if (e.type === 'mouseup') {
        // 当释放鼠标键时，删除鼠标移动事件和删除鼠标释放事件
        document.body.removeEventListener('mousemove', this.thumbMouseHandler)
        document.body.removeEventListener('mouseup', this.thumbMouseHandler)
      }
      this.$emit('changColorPicker', this.realShowColor)
    },
    // 颜色面板点击事件
    pannelMosueClick(e) {
      const elemInfo = this.$refs.colorPannel.getBoundingClientRect()
      // 在颜色面板容器范围内移动
      this.colorPannel.top = e.clientY - elemInfo.top
      this.colorPannel.left = e.clientX - elemInfo.left
      // 使取色圈移动更加顺滑且不超过取色面板容器范围
      this.colorPannel.left = Math.max(0, this.colorPannel.left)
      this.colorPannel.left = Math.min(this.colorPannel.left, elemInfo.width)
      this.colorPannel.top = Math.max(0, this.colorPannel.top)
      this.colorPannel.top = Math.min(this.colorPannel.top, elemInfo.height)

      // 计算饱和度(0 -> 100)和亮度 (0 -> 100)
      this.colorConfig.s = (parseInt(this.colorPannel.left) / elemInfo.width) * 100
      this.colorConfig.v = (1 - parseInt(this.colorPannel.top) / elemInfo.height) * 100
      this.colorForamtTransform()
      // 将hsv转换为rgb
      this.alphaColorBar.barColor = this.colorConfig.basicColor
      this.realShowColor = this.colorConfig.value
      this.$emit('changColorPicker', this.realShowColor)
    },
    // 颜色面板的拖拽事件
    pannelMosueHandler(e) {
      if (e.type === 'mousedown') {
        document.body.addEventListener('mousemove', this.pannelMosueHandler)
        document.body.addEventListener('mouseup', this.pannelMosueHandler)
      } else if (e.type === 'mousemove') {
        const elemInfo = this.$refs.colorPannel.getBoundingClientRect()
        // 在颜色面板容器范围内移动
        this.colorPannel.top = e.clientY - elemInfo.top
        this.colorPannel.left = e.clientX - elemInfo.left
        // 使取色圈移动更加顺滑且不超过取色面板容器范围
        this.colorPannel.left = Math.max(0, this.colorPannel.left)
        this.colorPannel.left = Math.min(this.colorPannel.left, elemInfo.width)
        this.colorPannel.top = Math.max(0, this.colorPannel.top)
        this.colorPannel.top = Math.min(this.colorPannel.top, elemInfo.height)

        // 计算饱和度(0 -> 100)和亮度 (0 -> 100)
        this.colorConfig.s = (parseInt(this.colorPannel.left) / elemInfo.width) * 100
        this.colorConfig.v = (1 - parseInt(this.colorPannel.top) / elemInfo.height) * 100
        this.colorForamtTransform()
        // 将hsv转换为rgb
        this.alphaColorBar.barColor = this.colorConfig.basicColor
        this.realShowColor = this.colorConfig.value
      } else if (e.type === 'mouseup') {
        // 当释放鼠标键时，删除鼠标移动事件和删除鼠标释放事件
        document.body.removeEventListener('mousemove', this.pannelMosueHandler)
        document.body.removeEventListener('mouseup', this.pannelMosueHandler)
      }
      this.$emit('changColorPicker', this.realShowColor)
    },
    // 透明柱的拖拽事件
    // alphaBarMouseHandler(e) {
    //   if (e.type === 'mousedown') {
    //     document.body.addEventListener('mousemove', this.alphaBarMouseHandler)
    //     document.body.addEventListener('mouseup', this.alphaBarMouseHandler)
    //   } else if (e.type === 'mousemove') {
    //     const elemInfo = this.$refs.alphaBar.getBoundingClientRect()
    //     this.alphaColorBar.thumbLeft = e.clientX - elemInfo.left
    //     this.alphaColorBar.thumbLeft = Math.max(0, this.alphaColorBar.thumbLeft)
    //     this.alphaColorBar.thumbLeft = Math.min(this.alphaColorBar.thumbLeft, elemInfo.width)
    //     // 获取颜色透明度0 -> 1
    //     this.colorConfig.alpha = (1 - this.alphaColorBar.thumbLeft / elemInfo.width).toFixed(2)
    //     this.colorForamtTransform()
    //     this.realShowColor = this.colorConfig.value
    //   } else if (e.type === 'mouseup') {
    //     // 当释放鼠标键时，删除鼠标移动事件和删除鼠标释放事件
    //     document.body.removeEventListener('mousemove', this.alphaBarMouseHandler)
    //     document.body.removeEventListener('mouseup', this.alphaBarMouseHandler)
    //   }
    // },
    // 颜色格式
    colorForamtTransform() {
      if (this.showAlpha) {
        // 如果开启透明度，那么颜色一定为rgba格式
        this.colorConfig.basicColor = this.hsvToRGB(this.colorConfig.h, this.colorConfig.s, this.colorConfig.v)
        this.colorConfig.value = this.rgbToRgba(this.colorConfig.basicColor, this.colorConfig.alpha)
      } else {
        if (this.colorFormat === 'hex') {
          this.colorConfig.basicColor = this.hsvToRGB(this.colorConfig.h, this.colorConfig.s, this.colorConfig.v)
          this.colorConfig.value = this.rgbToHex(this.colorConfig.basicColor)
        }
        if (this.colorFormat === 'rgb') {
          this.colorConfig.basicColor = this.hsvToRGB(this.colorConfig.h, this.colorConfig.s, this.colorConfig.v)
          this.colorConfig.value = this.colorConfig.basicColor
        }
      }
    },
    // 从hue to rgb
    hueToRGB(h) {
      if (h === 360) {
        h = 0
      }
      const doHandle = (num) => {
        if (num > 255) {
          return 255
        } else if (num < 0) {
          return 0
        } else {
          return Math.round(num)
        }
      }

      const hueRGB = (h / 60) * 255
      const r = doHandle(Math.abs(hueRGB - 765) - 255)
      const g = doHandle(510 - Math.abs(hueRGB - 510))
      const b = doHandle(510 - Math.abs(hueRGB - 1020))
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },
    // 从HSV(色相、饱和度、亮度) to rgb
    hsvToRGB(h, s, v) {
      s = s / 100
      v = v / 100
      let r = 0
      let g = 0
      let b = 0
      const i = Math.floor(h / 60)
      const f = h / 60 - i
      const p = v * (1 - s)
      const q = v * (1 - f * s)
      const t = v * (1 - (1 - f) * s)
      switch (i) {
        case 0:
          r = v
          g = t
          b = p
          break
        case 1:
          r = q
          g = v
          b = p
          break
        case 2:
          r = p
          g = v
          b = t
          break
        case 3:
          r = p
          g = q
          b = v
          break
        case 4:
          r = t
          g = p
          b = v
          break
        case 5:
          r = v
          g = p
          b = q
          break
      }

      return `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`
    },
    // rgb to  hsv
    rgbToHSV(rgbStr) {
      let { r, g, b } = this.getRGB(rgbStr)
      r = parseFloat(parseFloat(r / 255).toFixed(4))
      g = parseFloat(parseFloat(g / 255).toFixed(4))
      b = parseFloat(parseFloat(b / 255).toFixed(4))
      const max = Math.max(r, g, b)
      const min = Math.min(r, g, b)
      let h
      const v = max

      const d = max - min
      const s = max === 0 ? 0 : d / max

      if (max === min) {
        h = 0 // achromatic
      } else {
        switch (max) {
          case r:
            h = (g - b) / d + (g < b ? 6 : 0)
            break
          case g:
            h = (b - r) / d + 2
            break
          case b:
            h = (r - g) / d + 4
            break
        }
        h /= 6
      }
      return { h: h * 360, s: s * 100, v: v * 100 }
    },
    // 根据hsv获取取色圈位置
    hsvToPosition(s, v, width, height) {
      this.colorPannel.top = height - (v * height) / 100
      this.colorPannel.left = (s * width) / 100
    },
    hueToPosition(h, height) {
      this.colorBar.top = (h * height) / 360
    },
    alphaToPosition(alpha, width) {
      this.alphaColorBar.thumbLeft = (1 - alpha) * width
    },
    // 拆解rgb为r,g,b
    getRGB(rgbStr) {
      const matchArr = rgbStr.match(/\(.+?\)/g)[0].match(/\w+/g)
      const r = parseInt(matchArr[0])
      const g = parseInt(matchArr[1])
      const b = parseInt(matchArr[2])
      return { r, g, b }
    },
    // rgb 转 16进制
    rgbToHex(rgbStr) {
      // 拆解rgb为[255,255,255]形式。
      const { r, g, b } = this.getRGB(rgbStr)
      return `#${this.zeroFill(r.toString(16))}${this.zeroFill(g.toString(16))}${this.zeroFill(b.toString(16))}`
    },
    rgbToRgba(rgbStr, alpha) {
      return rgbStr.replace(')', `,${alpha})`)
    },
    hexToRGB(hexStr) {
      if (hexStr.length === 4) {
        const hexArr = hexStr.match(/\w{1}/g)
        return `rgb(${parseInt(hexArr[0] + hexArr[0], 16)},${parseInt(hexArr[1] + hexArr[1], 16)},${parseInt(
          hexArr[2] + hexArr[2],
          16
        )})`
      }
      if (hexStr.length === 7) {
        const hexArr = hexStr.match(/\w{2}/g)
        return `rgb(${parseInt(hexArr[0], 16)},${parseInt(hexArr[1], 16)},${parseInt(hexArr[2], 16)})`
      }
    },
    // 补零
    zeroFill(val) {
      return val.length > 1 ? val : '0' + val
    },
    changeInputColor(e) {
      this.initShowColor(e.target.value)
      this.$emit('changColorPicker', e.target.value)
    },
  },
}
</script>

<style lang="less" scoped>
.color-picker {
  width: 150px;
  margin: auto;
  height: 100px;
  margin-top: 0px;
  position: relative;

  //   .color-button {
  //     height: 36px;
  //     width: 36px;
  //     border: 1px solid rgba(0, 0, 0, 0.15);
  //     border-radius: 4px;
  //     .back-ground {
  //       height: 26px;
  //       width: 26px;
  //       margin: 4px;
  //       background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAIAAADZF8uwAAAAGUlEQVQYV2M4gwH+YwCGIasIUwhT25BVBADtzYNYrHvv4gAAAABJRU5ErkJggg==);
  //       .contain {
  //         border: 1px solid rgba(0, 0, 0, 0.5);
  //         border-radius: 2px;
  //       }
  //     }
  //   }
  .color-dropdown {
    margin: auto;
    width: 140px;
    height: 92px;
    position: absolute;
    top: 0;
    left: 0;
    // background-color: rgba(0, 0, 0, 0.2);
    overflow: hidden;
    .color-dropdown-picker {
      display: flex;
      flex-direction: row;
      flex-wrap: nowrap;
      justify-content: space-around;
      .color-pannel-box {
        position: relative;
        width: 110px;
        height: 64px;
        background: linear-gradient(to top, #000, transparent), linear-gradient(to right, #fff, transparent);
        .color-select-circle {
          position: absolute;
          transform: translate(-4px, -4px);
          border: 1px solid #fff;
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }
      }
      .color-slider-box {
        cursor: pointer;
        width: 10px;

        position: relative;
        .color-slider {
          background: linear-gradient(180deg, #f00, #ff0 17%, #0f0 33%, #0ff 50%, #00f 67%, #f0f 83%, #f00);
          width: 10px;
          height: 64px;
        }
        .color-thumb {
          width: 10px;
          height: 7px;
          position: absolute;
          left: 0;
          transform: translate(0, -3px);
          border-radius: 2px;
          background-color: rgb(10, 10, 10);
          border: 3px solid #fff;
          margin-left: 0;
        }
      }
    }

    .color-alpha {
      position: relative;
      height: 12px;
      box-shadow: 2px 2px 2px 2px 2px rgba(0, 0, 0, 0.1);
      margin-left: 10px;
      width: 300px;
      background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAIAAADZF8uwAAAAGUlEQVQYV2M4gwH+YwCGIasIUwhT25BVBADtzYNYrHvv4gAAAABJRU5ErkJggg==);
      .color-alpha-bar {
        height: 100%;
        width: 100%;
      }
      .color-alpha-thumb {
        width: 7px;
        height: 18px;
        position: absolute;
        top: -3px;
        transform: translate(-3px, 0);
        border-radius: 2px;
        background-color: rgb(10, 10, 10);
        border: 3px solid #fff;
      }
    }
    .color-input {
      width: 100%;
      margin: auto;
      display: flex;
      padding: 3px 6px;
      justify-content: space-between;
      button {
        color: #000;
      }
      .color-input-box {
        color: #000;
        border: 1px solid rgba(0, 0, 0, 0.1);
      }
    }
  }
}
</style>
