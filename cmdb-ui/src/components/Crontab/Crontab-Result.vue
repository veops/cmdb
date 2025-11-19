<template>
  <div class="popup-result">
    <p class="title">最近5次运行时间</p>
    <ul class="popup-result-scroll">
      <template v-if="isShow">
        <li v-for="item in resultList" :key="item">{{ item }}</li>
      </template>
      <li v-else>计算结果中...</li>
    </ul>
  </div>
</template>

<script>
/* eslint-disable */
export default {
  data() {
    return {
      dayRule: '',
      dayRuleSup: '',
      dateArr: [],
      resultList: [],
      isShow: false,
    }
  },
  name: 'CrontabResult',
  methods: {
    // When expression value changes, start calculating results
    expressionChange() {
      // Start calculation - hide results
      this.isShow = false
      // Get rule array [0:second, 1:minute, 2:hour, 3:day, 4:month, 5:week, 6:year]
      const ruleArr = this.$options.propsData.ex.split(' ')
      // Used to record the number of times entering the loop
      let nums = 0
      // Array for temporarily storing time rule results
      const resultArr = []
      // Get current time accurate to [year, month, day, hour, minute, second]
      const nTime = new Date()
      const nYear = nTime.getFullYear()
      let nMouth = nTime.getMonth() + 1
      let nDay = nTime.getDate()
      let nHour = nTime.getHours()
      let nMin = nTime.getMinutes()
      let nSecond = nTime.getSeconds()
      // Get arrays for years, months, etc. within the next 100 years based on rules
      this.getSecondArr(ruleArr[0])
      this.getMinArr(ruleArr[1])
      this.getHourArr(ruleArr[2])
      this.getDayArr(ruleArr[3])
      this.getMouthArr(ruleArr[4])
      this.getWeekArr(ruleArr[5])
      this.getYearArr(ruleArr[6], nYear)
      // Assign the obtained arrays - for easy use
      const sDate = this.dateArr[0]
      const mDate = this.dateArr[1]
      const hDate = this.dateArr[2]
      const DDate = this.dateArr[3]
      const MDate = this.dateArr[4]
      const YDate = this.dateArr[5]
      // Get the index of current time in the array
      let sIdx = this.getIndex(sDate, nSecond)
      let mIdx = this.getIndex(mDate, nMin)
      let hIdx = this.getIndex(hDate, nHour)
      let DIdx = this.getIndex(DDate, nDay)
      let MIdx = this.getIndex(MDate, nMouth)
      const YIdx = this.getIndex(YDate, nYear)
      // Functions to reset month, day, hour, minute, second (used frequently later)
      const resetSecond = function() {
        sIdx = 0
        nSecond = sDate[sIdx]
      }
      const resetMin = function() {
        mIdx = 0
        nMin = mDate[mIdx]
        resetSecond()
      }
      const resetHour = function() {
        hIdx = 0
        nHour = hDate[hIdx]
        resetMin()
      }
      const resetDay = function() {
        DIdx = 0
        nDay = DDate[DIdx]
        resetHour()
      }
      const resetMouth = function() {
        MIdx = 0
        nMouth = MDate[MIdx]
        resetDay()
      }
      // If current year is not the current value in array
      if (nYear !== YDate[YIdx]) {
        resetMouth()
      }
      // If current month is not the current value in array
      if (nMouth !== MDate[MIdx]) {
        resetDay()
      }
      // If current "day" is not the current value in array
      if (nDay !== DDate[DIdx]) {
        resetHour()
      }
      // If current "hour" is not the current value in array
      if (nHour !== hDate[hIdx]) {
        resetMin()
      }
      // If current "minute" is not the current value in array
      if (nMin !== mDate[mIdx]) {
        resetSecond()
      }

      // Loop through year array
      goYear: for (let Yi = YIdx; Yi < YDate.length; Yi++) {
        const YY = YDate[Yi]
        // When reaching maximum value
        if (nMouth > MDate[MDate.length - 1]) {
          resetMouth()
          continue
        }
        // Loop through month array
        goMouth: for (let Mi = MIdx; Mi < MDate.length; Mi++) {
          // Assign value, for easier calculation later
          let MM = MDate[Mi]
          MM = MM < 10 ? '0' + MM : MM
          // When reaching maximum value
          if (nDay > DDate[DDate.length - 1]) {
            resetDay()
            if (Mi == MDate.length - 1) {
              resetMouth()
              continue goYear
            }
            continue
          }
          // Loop through day array
          goDay: for (let Di = DIdx; Di < DDate.length; Di++) {
            // Assign value, for easier calculation later
            let DD = DDate[Di]
            let thisDD = DD < 10 ? '0' + DD : DD

            // When reaching maximum value
            if (nHour > hDate[hDate.length - 1]) {
              resetHour()
              if (Di == DDate.length - 1) {
                resetDay()
                if (Mi == MDate.length - 1) {
                  resetMouth()
                  continue goYear
                }
                continue goMouth
              }
              continue
            }

            // Check the validity of the date, if invalid, break out of current loop
            if (
              this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true &&
              this.dayRule !== 'workDay' &&
              this.dayRule !== 'lastWeek' &&
              this.dayRule !== 'lastDay'
            ) {
              resetDay()
              continue goMouth
            }
            // When there is a value in the day rule
            if (this.dayRule == 'lastDay') {
              // If not a valid date, adjust the date to a valid date, i.e., the last day of the month

              if (this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                while (DD > 0 && this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                  DD--

                  thisDD = DD < 10 ? '0' + DD : DD
                }
              }
            } else if (this.dayRule == 'workDay') {
              // Validate and adjust if a date like February 30th is passed in, adjust to normal month end
              if (this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                while (DD > 0 && this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                  DD--
                  thisDD = DD < 10 ? '0' + DD : DD
                }
              }
              // Get the day of week for the date that meets the condition
              const thisWeek = this.formatDate(new Date(YY + '-' + MM + '-' + thisDD + ' 00:00:00'), 'week')
              // When it's Sunday
              if (thisWeek == 0) {
                // First find the next day and check if it's the end of month
                DD++
                thisDD = DD < 10 ? '0' + DD : DD
                // Check if the next day is not a valid date
                if (this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                  DD -= 3
                }
              } else if (thisWeek == 6) {
                // When it's Saturday, only need to check it's not the 1st to proceed
                if (this.dayRuleSup !== 1) {
                  DD--
                } else {
                  DD += 2
                }
              }
            } else if (this.dayRule == 'weekDay') {
              // If a specific day of week is specified
              // Get which day of week the current date is
              const thisWeek = this.formatDate(new Date(YY + '-' + MM + '-' + DD + ' 00:00:00'), 'week')
              // Verify if current weekday is in the weekday pool (dayRuleSup)
              if (!this.dayRuleSup.includes(thisWeek)) {
                // When reaching maximum value
                if (Di == DDate.length - 1) {
                  resetDay()
                  if (Mi == MDate.length - 1) {
                    resetMouth()
                    continue goYear
                  }
                  continue goMouth
                }
                continue
              }
            } else if (this.dayRule == 'assWeek') {
              // If specified as which day of which week
              // Get which day of week the 1st of the month is
              const thisWeek = this.formatDate(new Date(YY + '-' + MM + '-' + DD + ' 00:00:00'), 'week')
              if (this.dayRuleSup[1] >= thisWeek) {
                DD = (this.dayRuleSup[0] - 1) * 7 + this.dayRuleSup[1] - thisWeek + 1
              } else {
                DD = this.dayRuleSup[0] * 7 + this.dayRuleSup[1] - thisWeek + 1
              }
            } else if (this.dayRule == 'lastWeek') {
              // If specified as the last specific weekday of the month
              // Validate and adjust if a date like February 30th is passed in, adjust to normal month end
              if (this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                while (DD > 0 && this.checkDate(YY + '-' + MM + '-' + thisDD + ' 00:00:00') !== true) {
                  DD--
                  thisDD = DD < 10 ? '0' + DD : DD
                }
              }
              // Get which day of week the last day of the month is
              const thisWeek = this.formatDate(new Date(YY + '-' + MM + '-' + thisDD + ' 00:00:00'), 'week')
              // Find the closest matching weekday in requirements
              if (this.dayRuleSup < thisWeek) {
                DD -= thisWeek - this.dayRuleSup
              } else if (this.dayRuleSup > thisWeek) {
                DD -= 7 - (this.dayRuleSup - thisWeek)
              }
            }
            // Check if time value is less than 10, format as "05"
            DD = DD < 10 ? '0' + DD : DD

            // Loop through "hour" array
            goHour: for (let hi = hIdx; hi < hDate.length; hi++) {
              const hh = hDate[hi] < 10 ? '0' + hDate[hi] : hDate[hi]

              // When reaching maximum value
              if (nMin > mDate[mDate.length - 1]) {
                resetMin()
                if (hi == hDate.length - 1) {
                  resetHour()
                  if (Di == DDate.length - 1) {
                    resetDay()
                    if (Mi == MDate.length - 1) {
                      resetMouth()
                      continue goYear
                    }
                    continue goMouth
                  }
                  continue goDay
                }
                continue
              }
              // Loop through "minute" array
              goMin: for (let mi = mIdx; mi < mDate.length; mi++) {
                const mm = mDate[mi] < 10 ? '0' + mDate[mi] : mDate[mi]

                // When reaching maximum value
                if (nSecond > sDate[sDate.length - 1]) {
                  resetSecond()
                  if (mi == mDate.length - 1) {
                    resetMin()
                    if (hi == hDate.length - 1) {
                      resetHour()
                      if (Di == DDate.length - 1) {
                        resetDay()
                        if (Mi == MDate.length - 1) {
                          resetMouth()
                          continue goYear
                        }
                        continue goMouth
                      }
                      continue goDay
                    }
                    continue goHour
                  }
                  continue
                }
                // Loop through "second" array
                goSecond: for (let si = sIdx; si <= sDate.length - 1; si++) {
                  const ss = sDate[si] < 10 ? '0' + sDate[si] : sDate[si]
                  // Add current time (time validity already checked in date loop)
                  if (MM !== '00' && DD !== '00') {
                    resultArr.push(YY + '-' + MM + '-' + DD + ' ' + hh + ':' + mm + ':' + ss)
                    nums++
                  }
                  // If count is full, exit the loop
                  if (nums == 5) break goYear
                  // When reaching maximum value
                  if (si == sDate.length - 1) {
                    resetSecond()
                    if (mi == mDate.length - 1) {
                      resetMin()
                      if (hi == hDate.length - 1) {
                        resetHour()
                        if (Di == DDate.length - 1) {
                          resetDay()
                          if (Mi == MDate.length - 1) {
                            resetMouth()
                            continue goYear
                          }
                          continue goMouth
                        }
                        continue goDay
                      }
                      continue goHour
                    }
                    continue goMin
                  }
                } // goSecond
              } // goMin
            } // goHour
          } // goDay
        } // goMouth
      }
      // Check the number of results within 100 years
      if (resultArr.length == 0) {
        this.resultList = ['No results match the conditions!']
      } else {
        this.resultList = resultArr
        if (resultArr.length !== 5) {
          this.resultList.push('Only ' + resultArr.length + ' results within the next 100 years!')
        }
      }
      // Calculation complete - show results
      this.isShow = true
    },
    // Used to calculate the index of a certain digit in the array
    getIndex(arr, value) {
      if (value <= arr[0] || value > arr[arr.length - 1]) {
        return 0
      } else {
        for (let i = 0; i < arr.length - 1; i++) {
          if (value > arr[i] && value <= arr[i + 1]) {
            return i + 1
          }
        }
      }
    },
    // Get "year" array
    getYearArr(rule, year) {
      this.dateArr[5] = this.getOrderArr(year, year + 100)
      if (rule !== undefined) {
        if (rule.indexOf('-') >= 0) {
          this.dateArr[5] = this.getCycleArr(rule, year + 100, false)
        } else if (rule.indexOf('/') >= 0) {
          this.dateArr[5] = this.getAverageArr(rule, year + 100)
        } else if (rule !== '*') {
          this.dateArr[5] = this.getAssignArr(rule)
        }
      }
    },
    // Get "month" array
    getMouthArr(rule) {
      this.dateArr[4] = this.getOrderArr(1, 12)
      if (rule.indexOf('-') >= 0) {
        this.dateArr[4] = this.getCycleArr(rule, 12, false)
      } else if (rule.indexOf('/') >= 0) {
        this.dateArr[4] = this.getAverageArr(rule, 12)
      } else if (rule !== '*') {
        this.dateArr[4] = this.getAssignArr(rule)
      }
    },
    // Get "day" array - mainly for date rules
    getWeekArr(rule) {
      // Only when both date rule values are "" does it indicate there are date options
      if (this.dayRule == '' && this.dayRuleSup == '') {
        if (rule.indexOf('-') >= 0) {
          this.dayRule = 'weekDay'
          this.dayRuleSup = this.getCycleArr(rule, 7, false)
        } else if (rule.indexOf('#') >= 0) {
          this.dayRule = 'assWeek'
          const matchRule = rule.match(/[0-9]{1}/g)
          this.dayRuleSup = [Number(matchRule[0]), Number(matchRule[1])]
          this.dateArr[3] = [1]
          if (this.dayRuleSup[1] == 7) {
            this.dayRuleSup[1] = 0
          }
        } else if (rule.indexOf('L') >= 0) {
          this.dayRule = 'lastWeek'
          this.dayRuleSup = Number(rule.match(/[0-9]{1,2}/g)[0])
          this.dateArr[3] = [31]
          if (this.dayRuleSup == 7) {
            this.dayRuleSup = 0
          }
        } else if (rule !== '*' && rule !== '?') {
          this.dayRule = 'weekDay'
          this.dayRuleSup = this.getAssignArr(rule)
        }
        // If weekDay, adjust 7 to 0 [week value 0 is Sunday]
        if (this.dayRule == 'weekDay') {
          for (let i = 0; i < this.dayRuleSup.length; i++) {
            if (this.dayRuleSup[i] == 7) {
              this.dayRuleSup[i] = 0
            }
          }
        }
      }
    },
    // Get "day" array - few are date rules
    getDayArr(rule) {
      this.dateArr[3] = this.getOrderArr(1, 31)
      this.dayRule = ''
      this.dayRuleSup = ''
      if (rule.indexOf('-') >= 0) {
        this.dateArr[3] = this.getCycleArr(rule, 31, false)
        this.dayRuleSup = 'null'
      } else if (rule.indexOf('/') >= 0) {
        this.dateArr[3] = this.getAverageArr(rule, 31)
        this.dayRuleSup = 'null'
      } else if (rule.indexOf('W') >= 0) {
        this.dayRule = 'workDay'
        this.dayRuleSup = Number(rule.match(/[0-9]{1,2}/g)[0])
        this.dateArr[3] = [this.dayRuleSup]
      } else if (rule.indexOf('L') >= 0) {
        this.dayRule = 'lastDay'
        this.dayRuleSup = 'null'
        this.dateArr[3] = [31]
      } else if (rule !== '*' && rule !== '?') {
        this.dateArr[3] = this.getAssignArr(rule)
        this.dayRuleSup = 'null'
      } else if (rule == '*') {
        this.dayRuleSup = 'null'
      }
    },
    // Get "hour" array
    getHourArr(rule) {
      this.dateArr[2] = this.getOrderArr(0, 23)
      if (rule.indexOf('-') >= 0) {
        this.dateArr[2] = this.getCycleArr(rule, 24, true)
      } else if (rule.indexOf('/') >= 0) {
        this.dateArr[2] = this.getAverageArr(rule, 23)
      } else if (rule !== '*') {
        this.dateArr[2] = this.getAssignArr(rule)
      }
    },
    // Get "minute" array
    getMinArr(rule) {
      this.dateArr[1] = this.getOrderArr(0, 59)
      if (rule.indexOf('-') >= 0) {
        this.dateArr[1] = this.getCycleArr(rule, 60, true)
      } else if (rule.indexOf('/') >= 0) {
        this.dateArr[1] = this.getAverageArr(rule, 59)
      } else if (rule !== '*') {
        this.dateArr[1] = this.getAssignArr(rule)
      }
    },
    // Get "second" array
    getSecondArr(rule) {
      this.dateArr[0] = this.getOrderArr(0, 59)
      if (rule.indexOf('-') >= 0) {
        this.dateArr[0] = this.getCycleArr(rule, 60, true)
      } else if (rule.indexOf('/') >= 0) {
        this.dateArr[0] = this.getAverageArr(rule, 59)
      } else if (rule !== '*') {
        this.dateArr[0] = this.getAssignArr(rule)
      }
    },
    // Return a sequential array based on the passed min-max
    getOrderArr(min, max) {
      const arr = []
      for (let i = min; i <= max; i++) {
        arr.push(i)
      }
      return arr
    },
    // Return an array based on scattered values specified in the rule
    getAssignArr(rule) {
      const arr = []
      const assiginArr = rule.split(',')
      for (let i = 0; i < assiginArr.length; i++) {
        arr[i] = Number(assiginArr[i])
      }
      arr.sort(this.compare)
      return arr
    },
    // Calculate and return an array based on certain arithmetic rules
    getAverageArr(rule, limit) {
      const arr = []
      const agArr = rule.split('/')
      let min = Number(agArr[0])
      const step = Number(agArr[1])
      while (min <= limit) {
        arr.push(min)
        min += step
      }
      return arr
    },
    // Return a periodic array based on the rule
    getCycleArr(rule, limit, status) {
      // status--indicates whether to start from 0 (or start from 1)
      const arr = []
      const cycleArr = rule.split('-')
      const min = Number(cycleArr[0])
      let max = Number(cycleArr[1])
      if (min > max) {
        max += limit
      }
      for (let i = min; i <= max; i++) {
        let add = 0
        if (status == false && i % limit == 0) {
          add = limit
        }
        arr.push(Math.round((i % limit) + add))
      }
      arr.sort(this.compare)
      return arr
    },
    // Compare number sizes (for Array.sort)
    compare(value1, value2) {
      if (value2 - value1 > 0) {
        return -1
      } else {
        return 1
      }
    },
    // Format date as: 2017-9-19 18:04:33
    formatDate(value, type) {
      // Calculate date-related values
      const time = typeof value === 'number' ? new Date(value) : value
      const Y = time.getFullYear()
      const M = time.getMonth() + 1
      const D = time.getDate()
      const h = time.getHours()
      const m = time.getMinutes()
      const s = time.getSeconds()
      const week = time.getDay()
      // If type was passed
      if (type == undefined) {
        return (
          Y +
          '-' +
          (M < 10 ? '0' + M : M) +
          '-' +
          (D < 10 ? '0' + D : D) +
          ' ' +
          (h < 10 ? '0' + h : h) +
          ':' +
          (m < 10 ? '0' + m : m) +
          ':' +
          (s < 10 ? '0' + s : s)
        )
      } else if (type == 'week') {
        return week
      }
    },
    // Check if date exists
    checkDate(value) {
      const time = new Date(value)
      const format = this.formatDate(time)
      return value == format
    },
  },
  watch: {
    ex: 'expressionChange',
  },
  props: ['ex'],
  mounted: function() {
    // Initialize, get results once
    this.expressionChange()
  },
}
</script>
