<template>
  <a-modal
    :visible="visible"
    :title="$t('cs.companyStructure.batchImport')"
    dialogClass="ops-modal setting-structure-upload"
    :width="800"
    @cancel="close"
  >
    <div class="setting-structure-upload-steps">
      <div
        :class="{ 'setting-structure-upload-step': true, selected: index + 1 <= currentStep }"
        v-for="(step, index) in stepList"
        :key="step.value"
      >
        <div :class="{ 'setting-structure-upload-step-icon': true }">
          <ops-icon :type="step.icon" />
        </div>
        <span>{{ step.label }}</span>
      </div>
    </div>
    <template v-if="currentStep === 1">
      <a-upload :multiple="false" :customRequest="customRequest" accept=".xlsx" :showUploadList="false">
        <a-button :style="{ marginBottom: '20px' }" type="primary"> <a-icon type="upload" />{{ $t('cs.companyStructure.selectFile') }}</a-button>
      </a-upload>
      <p><a @click="download">{{ $t('cs.companyStructure.clickDownloadImportTemplate') }}</a></p>
    </template>
    <div
      :style="{
        height: '60px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        whiteSpace: 'pre-wrap',
      }"
      v-if="currentStep === 3"
    >
      {{ $t('cs.companyStructure.importSuccess', { allCount: allCount })
      }}<span :style="{ color: '#2362FB' }"> {{ allCount - errorCount }} </span>{{ $t('cs.companyStructure.count') }},
      {{ $t('cs.companyStructure.importFailed') }}<span :style="{ color: '#D81E06' }"> {{ errorCount }} </span
      >{{ $t('cs.companyStructure.count') }}
    </div>
    <vxe-table
      v-if="currentStep === 2 || has_error"
      ref="employeeTable"
      stripe
      :data="importData"
      show-overflow
      show-header-overflow
      highlight-hover-row
      size="small"
      class="ops-stripe-table"
      :max-height="400"
      :column-config="{ resizable: true }"
    >
      <vxe-column field="email" :title="$t('cs.companyStructure.email')" min-width="120" fixed="left"></vxe-column>
      <vxe-column field="username" :title="$t('cs.companyStructure.username')" min-width="80" ></vxe-column>
      <vxe-column field="nickname" :title="$t('cs.companyStructure.nickname')" min-width="80"></vxe-column>
      <vxe-column field="password" :title="$t('cs.companyStructure.password')" min-width="80"></vxe-column>
      <vxe-column field="sex" :title="$t('cs.companyStructure.sex')" min-width="60"></vxe-column>
      <vxe-column field="mobile" :title="$t('cs.companyStructure.mobile')" min-width="80"></vxe-column>
      <vxe-column field="position_name" :title="$t('cs.companyStructure.positionName')" min-width="80"></vxe-column>
      <vxe-column field="department_name" :title="$t('cs.companyStructure.departmentName')" min-width="80"></vxe-column>
      <vxe-column field="current_company" v-if="useDFC" :title="$t('cs.companyStructure.currentCompany')" min-width="120"></vxe-column>
      <vxe-column field="dfc_entry_date" v-if="useDFC" :title="$t('cs.companyStructure.dfcEntryDate')" min-width="120"></vxe-column>
      <vxe-column field="entry_date" :title="$t('cs.companyStructure.entryDate')" min-width="120"></vxe-column>
      <vxe-column field="is_internship" :title="$t('cs.companyStructure.isInternship')" min-width="120"></vxe-column>
      <vxe-column field="leave_date" :title="$t('cs.companyStructure.leaveDate')" min-width="120"></vxe-column>
      <vxe-column field="id_card" :title="$t('cs.companyStructure.idCard')" min-width="120"></vxe-column>
      <vxe-column field="nation" :title="$t('cs.companyStructure.nation')" min-width="80"></vxe-column>
      <vxe-column field="id_place" :title="$t('cs.companyStructure.idPlace')" min-width="80"></vxe-column>
      <vxe-column field="party" :title="$t('cs.companyStructure.party')" min-width="80"></vxe-column>
      <vxe-column field="household_registration_type" :title="$t('cs.companyStructure.householdRegistrationType')" min-width="80"></vxe-column>
      <vxe-column field="hometown" :title="$t('cs.companyStructure.homewtown')" min-width="80"></vxe-column>
      <vxe-column field="marry" :title="$t('cs.companyStructure.marry')" min-width="80"></vxe-column>
      <vxe-column field="max_degree" :title="$t('cs.companyStructure.maxDegree')" min-width="80"></vxe-column>
      <vxe-column field="emergency_person" :title="$t('cs.companyStructure.emergencyPerson')" min-width="120"></vxe-column>
      <vxe-column field="emergency_phone" :title="$t('cs.companyStructure.emergencyPhone')" min-width="120"></vxe-column>
      <vxe-column field="bank_card_number" :title="$t('cs.companyStructure.bankCardNumber')" min-width="120"></vxe-column>
      <vxe-column field="bank_card_name" :title="$t('cs.companyStructure.bankCardName')" min-width="80"></vxe-column>
      <vxe-column field="opening_bank" :title="$t('cs.companyStructure.openingBank')" min-width="80"></vxe-column>
      <vxe-column field="account_opening_location" :title="$t('cs.companyStructure.accountOpeningLocation')" min-width="120"></vxe-column>
      <vxe-column field="school" :title="$t('cs.companyStructure.school')" min-width="80"></vxe-column>
      <vxe-column field="major" :title="$t('cs.companyStructure.major')" min-width="80"></vxe-column>
      <vxe-column field="education" :title="$t('cs.companyStructure.education')" min-width="80"></vxe-column>
      <vxe-column field="graduation_year" :title="$t('cs.companyStructure.graduationYear')" min-width="120"></vxe-column>
      <vxe-column field="birth_date" :title="$t('cs.companyStructure.birthDate')" min-width="120"></vxe-column>
      <vxe-column field="birth_place" :title="$t('cs.companyStructure.birthPlace')" min-width="120"></vxe-column>
      <vxe-column field="nationality_region" :title="$t('cs.companyStructure.nationalityRegion')" min-width="120"></vxe-column>
      <vxe-column field="first_entry_date" :title="$t('cs.companyStructure.firstEntryDate')" min-width="120"></vxe-column>
      <vxe-column field="estimated_departure_date" :title="$t('cs.companyStructure.estimatedDepartureDate')" min-width="120"></vxe-column>
      <vxe-column v-if="has_error" field="err" :title="$t('cs.companyStructure.importFailedReason')" min-width="120" fixed="right">
        <template #default="{ row }">
          <span :style="{ color: '#D81E06' }">{{ row.err }}</span>
        </template>
      </vxe-column>
    </vxe-table>
    <a-space slot="footer">
      <a-button size="small" type="primary" ghost @click="close">{{ $t('cancel') }}</a-button>
      <a-button v-if="currentStep !== 1" size="small" type="primary" ghost @click="goPre">{{ $t('cs.companyStructure.prevStep') }}</a-button>
      <a-button v-if="currentStep !== 3" size="small" type="primary" @click="goNext">{{ $t('cs.companyStructure.nextStep') }}</a-button>
      <a-button v-else size="small" type="primary" @click="close">{{ $t('cs.companyStructure.done') }}</a-button>
    </a-space>
  </a-modal>
</template>

<script>
import { downloadExcel, excel2Array } from '@/utils/download'
import { importEmployee } from '@/api/employee'
export default {
  name: 'BatchUpload',
  data() {
    const stepList = [
      {
        value: 1,
        label: this.$t('cs.companyStructure.uploadFile'),
        icon: 'icon-shidi-tianjia',
      },
      {
        value: 2,
        label: this.$t('cs.companyStructure.confirmData'),
        icon: 'icon-shidi-yunshangchuan',
      },
      {
        value: 3,
        label: this.$t('cs.companyStructure.uploadDone'),
        icon: 'icon-shidi-queren',
      },
    ]
    const common_importParamsList = [
      'email',
      'username',
      'nickname',
      'password',
      'sex',
      'mobile',
      'position_name',
      'department_name',
      'entry_date',
      'is_internship',
      'leave_date',
      'id_card',
      'nation',
      'id_place',
      'party',
      'household_registration_type',
      'hometown',
      'marry',
      'max_degree',
      'emergency_person',
      'emergency_phone',
      'bank_card_number',
      'bank_card_name',
      'opening_bank',
      'account_opening_location',
      'school',
      'major',
      'education',
      'graduation_year',
    ]
    return {
      stepList,
      common_importParamsList,
      visible: false,
      currentStep: 1,
      importData: [],
      has_error: false,
      allCount: 0,
      errorCount: 0,
    }
  },
  methods: {
    open() {
      this.importData = []
      this.has_error = false
      this.errorCount = 0
      this.visible = true
    },
    close() {
      this.currentStep = 1
      this.visible = false
    },
    async goNext() {
      if (this.currentStep === 2) {
        // 此处调用后端接口
        this.allCount = this.importData.length
        const importData = this.importData.map((item) => {
          const { _X_ROW_KEY, ...rest } = item
          const keyArr = Object.keys(rest)
          keyArr.forEach((key) => {
            if (rest[key]) {
              rest[key] = rest[key] + ''
            }
          })
          rest.educational_experience = [
            {
              school: rest.school,
              major: rest.major,
              education: rest.education,
              graduation_year: rest.graduation_year,
            },
          ]
          delete rest.school
          delete rest.major
          delete rest.education
          delete rest.graduation_year
          return rest
        })
        const res = await importEmployee({ employee_list: importData })
        if (res.length) {
          const errData = res.filter((item) => {
            return item.err.length
          })
          console.log('err', errData)
          this.has_error = true
          this.errorCount = errData.length
          this.currentStep += 1
          this.importData = errData
          this.$message.error(this.$t('cs.companyStructure.dataErr'))
        } else {
          this.currentStep += 1
          this.$message.success(this.$t('cs.companyStructure.opSuccess'))
        }
        this.$emit('refresh')
      }
    },
    goPre() {
      this.has_error = false
      this.errorCount = 0
      this.currentStep -= 1
    },
    download() {
      const data = [
        [
          {
            v: '1、表头标“*”的红色字体为必填项\n2、邮箱、用户名不允许重复\n3、登录密码：密码由6-20位字母、数字组成\n4、部门：上下级部门间用"/"隔开，且从最上级部门开始，例如“深圳分公司/IT部/IT二部”。如出现相同的部门，则默认导入组织架构中顺序靠前的部门',
            t: 's',
            s: {
              alignment: {
                wrapText: true,
                vertical: 'center',
              },
            },
          },
        ],
        [
          {
            v: '*邮箱',
            t: 's',
            s: {
              font: {
                color: {
                  rgb: 'FF0000',
                },
              },
            },
          },
          {
            v: '*用户名',
            t: 's',
            s: {
              font: {
                color: {
                  rgb: 'FF0000',
                },
              },
            },
          },
          {
            v: '*姓名',
            t: 's',
            s: {
              font: {
                color: {
                  rgb: 'FF0000',
                },
              },
            },
          },
          {
            v: '*密码',
            t: 's',
            s: {
              font: {
                color: {
                  rgb: 'FF0000',
                },
              },
            },
          },
          {
            v: '性别',
            t: 's',
          },
          {
            v: '手机号',
            t: 's',
          },
          {
            v: '岗位',
            t: 's',
          },
          {
            v: '部门',
            t: 's',
          },
          {
            v: '目前所属主体',
            t: 's',
          },
          {
            v: '初始入职日期',
            t: 's',
          },
          {
            v: '目前主体入职日期',
            t: 's',
          },
          {
            v: '正式/实习生',
            t: 's',
          },
          {
            v: '离职日期',
            t: 's',
          },
          {
            v: '身份证号码',
            t: 's',
          },
          {
            v: '民族',
            t: 's',
          },
          {
            v: '籍贯',
            t: 's',
          },
          {
            v: '组织关系',
            t: 's',
          },
          {
            v: '户籍类型',
            t: 's',
          },
          {
            v: '户口所在地',
            t: 's',
          },
          {
            v: '婚姻情况',
            t: 's',
          },
          {
            v: '最高学历',
            t: 's',
          },
          {
            v: '紧急联系人',
            t: 's',
          },
          {
            v: '紧急联系电话',
            t: 's',
          },
          {
            v: '卡号',
            t: 's',
          },
          {
            v: '银行',
            t: 's',
          },
          {
            v: '开户行',
            t: 's',
          },
          {
            v: '开户地',
            t: 's',
          },
          {
            v: '学校',
            t: 's',
          },
          {
            v: '专业',
            t: 's',
          },
          {
            v: '学历',
            t: 's',
          },
          {
            v: '毕业年份',
            t: 's',
          },
        ],
      ]
      data[1] = data[1].filter((item) => item['v'] !== '目前所属主体')
      data[1] = data[1].filter((item) => item['v'] !== '初始入职日期')
      downloadExcel(data, '员工导入模板')
    },
    customRequest(data) {
      this.fileList = [data.file]
      excel2Array(data.file).then((res) => {
        res = res.filter((item) => item.length)
        this.importData = res.slice(2).map((item) => {
          const obj = {}
          // 格式化日期字段
          item[8] = this.formatDate(item[8]) // 目前主体入职日期
          item[10] = this.formatDate(item[10]) // 离职日期
          item[28] = this.formatDate(item[28]) // 毕业年份
          item.forEach((ele, index) => {
            obj[this.common_importParamsList[index]] = ele
          })
          return obj
        })
        this.currentStep = 2
      })
    },
    formatDate(numb) {
      if (numb) {
        const time = new Date((numb - 1) * 24 * 3600000 + 1)
        time.setYear(time.getFullYear() - 70)
        time.setMonth(time.getMonth())
        time.setHours(time.getHours() - 8)
        time.setMinutes(time.getMinutes())
        time.setMilliseconds(time.getMilliseconds())
        // return time.valueOf()
        // 日期格式
        const format = 'Y-m-d'
        const year = time.getFullYear()
        // 由于 getMonth 返回值会比正常月份小 1
        let month = time.getMonth() + 1
        let day = time.getDate()
        month = month > 9 ? month : `0${month}`
        day = day > 9 ? day : `0${day}`
        const hash = {
          Y: year,
          m: month,
          d: day,
        }
        return format.replace(/\w/g, (o) => {
          return hash[o]
        })
      } else {
        return null
      }
    },
  },
}
</script>

<style lang="less">
.setting-structure-upload {
  .ant-modal-body {
    padding: 24px 48px;
  }
  .setting-structure-upload-steps {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 20px;
    .setting-structure-upload-step {
      display: inline-block;
      text-align: center;
      position: relative;
      .setting-structure-upload-step-icon {
        width: 86px;
        height: 86px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-image: url('../../../assets/icon-bg.png');
        margin-bottom: 20px;
        > i {
          font-size: 40px;
          color: #fff;
        }
      }
      > span {
        font-size: 16px;
        font-weight: 600;
        color: rgba(0, 0, 0, 0.5);
      }
    }
    .setting-structure-upload-step:not(:first-child)::before {
      content: '';
      height: 2px;
      width: 223px;
      position: absolute;
      background-color: #e7ecf3;
      left: -223px;
      top: 43px;
      z-index: 0;
    }
    .selected.setting-structure-upload-step {
      &:not(:first-child)::before {
        background-color: #7eb0ff;
      }
    }
    .selected {
      .setting-structure-upload-step-icon {
        background-image: url('../../../assets/icon-bg-selected.png');
      }
      > span {
        color: rgba(0, 0, 0, 0.8);
      }
    }
  }
}
</style>
