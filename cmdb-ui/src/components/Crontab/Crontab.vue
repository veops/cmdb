<template>
  <div :style="{ width: '490px' }">
    <el-tabs type="card" class="ops-crontab">
      <el-tab-pane label="秒" v-if="shouldHide('second')">
        <CrontabSecond @update="updateContabValue" :check="checkNumber" ref="cronsecond" />
      </el-tab-pane>

      <el-tab-pane label="分钟" v-if="shouldHide('min')">
        <CrontabMin @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronmin" />
      </el-tab-pane>

      <el-tab-pane label="小时" v-if="shouldHide('hour')">
        <CrontabHour @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronhour" />
      </el-tab-pane>

      <el-tab-pane label="日" v-if="shouldHide('day')">
        <CrontabDay @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronday" />
      </el-tab-pane>

      <el-tab-pane label="月" v-if="shouldHide('mouth')">
        <CrontabMouth @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronmouth" />
      </el-tab-pane>

      <el-tab-pane label="周" v-if="shouldHide('week')">
        <CrontabWeek @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronweek" />
      </el-tab-pane>

      <el-tab-pane label="年" v-if="shouldHide('year')">
        <CrontabYear @update="updateContabValue" :check="checkNumber" :cron="contabValueObj" ref="cronyear" />
      </el-tab-pane>
    </el-tabs>

    <div class="popup-main">
      <div class="popup-result">
        <p class="title">时间表达式</p>
        <div style="padding: 12px;">
          <div></div>
          <table>
            <thead>
              <th v-for="item of displayTabTitles" width="40" :key="item.value">{{ item.label }}</th>
              <th>crontab完整表达式</th>
            </thead>
            <tbody>
              <td v-if="shouldHide('second')">
                <span class="square">{{ contabValueObj.second }}</span>
              </td>
              <td v-if="shouldHide('min')">
                <span class="square">{{ contabValueObj.min }}</span>
              </td>
              <td v-if="shouldHide('hour')">
                <span class="square">{{ contabValueObj.hour }}</span>
              </td>
              <td v-if="shouldHide('day')">
                <span class="square">{{ contabValueObj.day === '?' ? '*' : contabValueObj.day }}</span>
              </td>
              <td v-if="shouldHide('mouth')">
                <span class="square">{{ contabValueObj.mouth }}</span>
              </td>
              <td v-if="shouldHide('week')">
                <span class="square">{{ contabValueObj.week === '?' ? '*' : contabValueObj.week }}</span>
              </td>
              <td v-if="shouldHide('year')">
                <span class="square">{{ contabValueObj.year }}</span>
              </td>
              <td>
                <span class="rectangle">{{ displayContabValueString }}</span>
              </td>
            </tbody>
          </table>
        </div>
      </div>
      <!-- <CrontabResult :ex="contabValueString"></CrontabResult> -->
    </div>
    <div class="pop_btn" v-if="hasFooter">
      <a-space>
        <a-button size="small" type="primary" @click="submitFill">确定</a-button>
        <a-button size="small" type="warning" @click="clearCron">重置</a-button>
        <a-button size="small" @click="hidePopup">取消</a-button>
      </a-space>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import CrontabSecond from './Crontab-Second.vue'
import CrontabMin from './Crontab-Min.vue'
import CrontabHour from './Crontab-Hour.vue'
import CrontabDay from './Crontab-Day.vue'
import CrontabMouth from './Crontab-Mouth.vue'
import CrontabWeek from './Crontab-Week.vue'
import CrontabYear from './Crontab-Year.vue'
import CrontabResult from './Crontab-Result.vue'
import { cronValidate } from './utils/index'
// 对表达式进行特异化处理 不展示？ 但是计算的时候还是有？的
export default {
  data() {
    return {
      tabTitles: [
        { value: 'second', label: '秒' },
        { value: 'min', label: '分钟' },
        { value: 'hour', label: '小时' },
        { value: 'day', label: '日' },
        { value: 'month', label: '月' },
        { value: 'week', label: '周' },
        { value: 'year', label: '年' },
      ],
      tabActive: 0,
      myindex: 0,
      contabValueObj: {
        second: '*',
        min: '*',
        hour: '*',
        day: '*',
        mouth: '*',
        week: '?',
        year: '',
      },
    }
  },
  name: 'Vcrontab',
  props: ['expression', 'hideComponent', 'defaultExpression', 'hasFooter'],
  methods: {
    shouldHide(key) {
      if (this.hideComponent && this.hideComponent.includes(key)) return false
      return true
    },
    resolveExp(expression) {
      // 反解析 表达式
      if (expression) {
        const arr = expression.split(' ')
        if (arr.length >= 6) {
          // 6 位以上是合法表达式
          const obj = {
            second: arr[0],
            min: arr[1],
            hour: arr[2],
            day: arr[3],
            mouth: arr[4],
            week: arr[5],
            year: arr[6] ? arr[6] : '',
          }
          this.contabValueObj = {
            ...obj,
          }
          for (const i in obj) {
            if (obj[i]) this.changeRadio(i, obj[i])
          }
        }
      }
    },
    // tab切换值
    tabCheck(index) {
      this.tabActive = index
    },
    // 由子组件触发，更改表达式组成的字段值
    updateContabValue(name, value, from) {
      'updateContabValue', name, value, from
      this.$set(this.contabValueObj, name, value)
      if (from && from !== name) {
        // console.log(`来自组件 ${from} 改变了 ${name} ${value}`);
        this.changeRadio(name, value)
      }
    },
    // 赋值到组件
    changeRadio(name, value) {
      const arr = ['second', 'min', 'hour', 'mouth']
      const refName = 'cron' + name
      let insVlaue
      if (!this.$refs[refName]) return

      if (arr.includes(name)) {
        if (value === '*') {
          insVlaue = 1
        } else if (value.indexOf('-') > -1) {
          const indexArr = value.split('-')
          isNaN(indexArr[0]) ? (this.$refs[refName].cycle01 = 0) : (this.$refs[refName].cycle01 = indexArr[0])
          this.$refs[refName].cycle02 = indexArr[1]
          insVlaue = 2
        } else if (value.indexOf('/') > -1) {
          const indexArr = value.split('/')
          isNaN(indexArr[0]) ? (this.$refs[refName].average01 = 0) : (this.$refs[refName].average01 = indexArr[0])
          this.$refs[refName].average02 = indexArr[1]
          insVlaue = 3
        } else {
          insVlaue = 4
          this.$refs[refName].checkboxList = value.split(',').map((v) => Number(v))
        }
      } else if (name == 'day') {
        if (value === '*') {
          insVlaue = 1
        } else if (value == '?') {
          insVlaue = 2
        } else if (value.indexOf('-') > -1) {
          const indexArr = value.split('-')
          isNaN(indexArr[0]) ? (this.$refs[refName].cycle01 = 0) : (this.$refs[refName].cycle01 = indexArr[0])
          this.$refs[refName].cycle02 = indexArr[1]
          insVlaue = 3
        } else if (value.indexOf('/') > -1) {
          const indexArr = value.split('/')
          isNaN(indexArr[0]) ? (this.$refs[refName].average01 = 0) : (this.$refs[refName].average01 = indexArr[0])
          this.$refs[refName].average02 = indexArr[1]
          insVlaue = 4
        } else if (value.indexOf('W') > -1) {
          const indexArr = value.split('W')
          isNaN(indexArr[0]) ? (this.$refs[refName].workday = 0) : (this.$refs[refName].workday = indexArr[0])
          insVlaue = 5
        } else if (value === 'L') {
          insVlaue = 6
        } else {
          this.$refs[refName].checkboxList = value.split(',')
          insVlaue = 7
        }
      } else if (name == 'week') {
        if (value === '*') {
          insVlaue = 1
        } else if (value == '?') {
          insVlaue = 2
        } else if (value.indexOf('-') > -1) {
          const indexArr = value.split('-')
          isNaN(indexArr[0]) ? (this.$refs[refName].cycle01 = 0) : (this.$refs[refName].cycle01 = indexArr[0])
          this.$refs[refName].cycle02 = indexArr[1]
          insVlaue = 3
        } else if (value.indexOf('#') > -1) {
          const indexArr = value.split('#')
          isNaN(indexArr[0]) ? (this.$refs[refName].average01 = 1) : (this.$refs[refName].average01 = indexArr[0])
          this.$refs[refName].average02 = indexArr[1]
          insVlaue = 4
        } else if (value.indexOf('L') > -1) {
          const indexArr = value.split('L')
          isNaN(indexArr[0]) ? (this.$refs[refName].weekday = 1) : (this.$refs[refName].weekday = indexArr[0])
          insVlaue = 5
        } else {
          this.$refs[refName].checkboxList = value.split(',')
          insVlaue = 6
        }
      } else if (name == 'year') {
        if (value == '') {
          insVlaue = 1
        } else if (value == '*') {
          insVlaue = 2
        } else if (value.indexOf('-') > -1) {
          insVlaue = 3
        } else if (value.indexOf('/') > -1) {
          insVlaue = 4
        } else {
          this.$refs[refName].checkboxList = value.split(',')
          insVlaue = 5
        }
      }
      this.$refs[refName].radioValue = insVlaue
    },
    // 表单选项的子组件校验数字格式（通过-props传递）
    checkNumber(value, minLimit, maxLimit) {
      // 检查必须为整数
      value = Math.floor(value)
      if (value < minLimit) {
        value = minLimit
      } else if (value > maxLimit) {
        value = maxLimit
      }
      return value
    },
    // 隐藏弹窗
    hidePopup() {
      this.$emit('hide')
    },
    // 填充表达式
    submitFill() {
      const result = cronValidate(this.contabValueString)
      console.log(result)
      if (typeof result !== 'boolean') {
        this.$message.warning(result)
        return this.$emit('error', result)
      }
      this.$emit('fill', this.displayContabValueString)
      this.hidePopup()
    },
    clearCron() {
      // 还原选择项
      this.resolveExp(this.defaultExpression || '* * * * * ?')
    },
  },
  computed: {
    contabValueString: function() {
      const obj = this.contabValueObj
      const str =
        obj.second +
        ' ' +
        obj.min +
        ' ' +
        obj.hour +
        ' ' +
        obj.day +
        ' ' +
        obj.mouth +
        ' ' +
        obj.week +
        (obj.year == '' ? '' : ' ' + obj.year)
      return str
    },
    displayContabValueString() {
      //去掉第一位秒，？改成 * 仅作展示用
      const _temp = this.contabValueString.substring(2)
      const reg = /\?/g
      return _temp.replace(reg, '*')
    },
    displayTabTitles() {
      return this.tabTitles.filter((item) => !this.hideComponent.includes(item.value))
    },
  },
  components: {
    CrontabSecond,
    CrontabMin,
    CrontabHour,
    CrontabDay,
    CrontabMouth,
    CrontabWeek,
    CrontabYear,
    CrontabResult,
  },
  watch: {
    expression: {
      handler(val) {
        if (!val) {
          this.clearCron()
          return
        }
        this.resolveExp(val)
      },
      immediate: true,
    },
  },
  mounted() {
    // 初始化
    if (this.expression) {
      this.resolveExp(this.expression)
    } else {
      this.clearCron()
    }
  },
}
</script>
<style scoped>
.pop_btn {
  text-align: right;
  margin-top: 24px;
}
.popup-main {
  position: relative;
  margin: 16px auto;
  background: #fff;
  border-radius: 8px;
  font-size: 12px;
  overflow: hidden;
  box-shadow: 0px 8px 16px rgba(160, 181, 235, 0.25);
}
.popup-title {
  overflow: hidden;
  line-height: 34px;
  padding-top: 6px;
  background: #f2f2f2;
}
.popup-result {
  border-radius: 8px;
}
.popup-result .title {
  background: #fff;
  font-weight: 400;
  font-size: 14px;
  color: #2f54eb;
  background-color: #f0f5ff;
  margin: 0px;
  box-sizing: border-box;
  padding-left: 12px;
}
.popup-result table {
  text-align: center;
  width: 100%;
  margin: 0 auto;
}
.popup-result table span {
  display: block;
  width: 100%;
  font-family: arial;
  line-height: 26px;
  height: 26px;
  white-space: nowrap;
  overflow: hidden;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
}

.popup-result table span.square {
  width: 40px;
  box-sizing: border-box;
}

.popup-result table span.rectangle {
  width: 247px;
}
.popup-result-scroll {
  font-size: 12px;
  line-height: 24px;
  height: 10em;
  overflow-y: auto;
}
</style>
