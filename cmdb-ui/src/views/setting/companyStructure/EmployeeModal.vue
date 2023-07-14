<template>
  <a-modal
    dialogClass="ops-modal"
    destroyOnClose
    width="810px"
    v-model="visible"
    :title="title"
    layout="inline"
    @cancel="close"
    :body-style="{ height: `${windowHeight - 320}px`, overflow: 'hidden', overflowY: 'scroll' }"
  >
    <a-form-model ref="employeeFormData" :model="employeeFormData" :rules="rules" :colon="false">
      <a-form-model-item
        ref="email"
        label="邮箱"
        prop="email"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'email') !== -1"
      >
        <a-input v-model="employeeFormData.email" placeholder="请输入邮箱" />
      </a-form-model-item>
      <a-form-model-item
        ref="username"
        label="用户名"
        prop="username"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'username') !== -1"
      >
        <a-input v-model="employeeFormData.username" placeholder="请输入用户名" />
      </a-form-model-item>
      <a-form-model-item
        v-if="type === 'add'"
        ref="password"
        label="登录密码"
        prop="password"
        :style="formModalItemStyle"
      >
        <a-input-password v-model="employeeFormData.password" placeholder="请输入登录密码" />
      </a-form-model-item>
      <a-form-model-item
        ref="nickname"
        label="姓名"
        prop="nickname"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'nickname') !== -1"
      >
        <a-input v-model="employeeFormData.nickname" placeholder="请输入姓名" />
      </a-form-model-item>
      <a-form-model-item
        label="性别"
        prop="sex"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'sex') !== -1"
      >
        <a-select v-model="employeeFormData.sex" placeholder="请选择性别">
          <a-select-option value="男"> 男 </a-select-option>
          <a-select-option value="女"> 女 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="mobile"
        label="手机号"
        prop="mobile"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'mobile') !== -1"
      >
        <a-input v-model="employeeFormData.mobile" placeholder="请输入手机号" />
      </a-form-model-item>
      <div
        :style="{ width: '361px', display: 'inline-block', margin: '0 7px' }"
        v-if="attributes.findIndex((v) => v == 'department_id') !== -1"
      >
        <div :style="{ height: '41px', lineHeight: '40px' }">部门</div>
        <DepartmentTreeSelect v-model="employeeFormData.department_id" />
      </div>
      <a-form-model-item
        ref="position_name"
        label="岗位"
        prop="position_name"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'position_name') !== -1"
      >
        <a-input v-model="employeeFormData.position_name" placeholder="请输入岗位" />
      </a-form-model-item>
      <div
        :style="{ width: '361px', display: 'inline-block', margin: '0 7px' }"
        v-if="attributes.findIndex((v) => v == 'direct_supervisor_id') !== -1"
      >
        <div :style="{ height: '41px', lineHeight: '40px' }">上级</div>
        <EmployeeTreeSelect v-model="employeeFormData.direct_supervisor_id" />
      </div>
      <a-form-model-item
        ref="annual_leave"
        label="年假"
        prop="annual_leave"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'annual_leave') !== -1"
      >
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.annual_leave"
          placeholder="请输入年假"
          :formatter="(value) => `${value} 天`"
        />
      </a-form-model-item>
      <a-form-model-item
        ref="virtual_annual_leave"
        label="虚拟年假"
        prop="virtual_annual_leave"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'virtual_annual_leave') !== -1"
      >
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.virtual_annual_leave"
          placeholder="请输入虚拟年假"
          :formatter="(value) => `${value} 天`"
        />
      </a-form-model-item>
      <a-form-model-item
        ref="parenting_leave"
        label="育儿假"
        prop="parenting_leave"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'parenting_leave') !== -1"
      >
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.parenting_leave"
          placeholder="请输入育儿假"
          :formatter="(value) => `${value} 天`"
        />
      </a-form-model-item>
      <a-form-model-item
        ref="entry_date"
        label="目前主体入职日期"
        prop="entry_date"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'entry_date') !== -1"
      >
        <a-date-picker
          placeholder="请选择目前主体入职日期"
          v-model="employeeFormData.entry_date"
          :style="{ width: '100%' }"
          @change="onChange($event, 'entry_date')"
        ></a-date-picker>
      </a-form-model-item>
      <a-form-model-item
        ref="is_internship"
        label="正式/实习生"
        prop="is_internship"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'is_internship') !== -1"
      >
        <a-select v-model="employeeFormData.is_internship" placeholder="请选择是否正式/实习生">
          <a-select-option :value="0"> 正式 </a-select-option>
          <a-select-option :value="1"> 实习生 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="leave_date"
        label="离职日期"
        prop="leave_date"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'leave_date') !== -1"
      >
        <a-date-picker
          v-model="employeeFormData.leave_date"
          placeholder="请选择离职日期"
          :style="{ width: '100%' }"
          @change="onChange($event, 'leave_date')"
        ></a-date-picker>
      </a-form-model-item>
      <a-form-model-item
        ref="id_card"
        label="身份证号码"
        prop="id_card"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'id_card') !== -1"
      >
        <a-input v-model="employeeFormData.id_card" placeholder="请输入身份证号码" />
      </a-form-model-item>
      <a-form-model-item
        ref="nation"
        label="民族"
        prop="nation"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'nation') !== -1"
      >
        <a-input v-model="employeeFormData.nation" placeholder="请输入民族" />
      </a-form-model-item>
      <a-form-model-item
        ref="id_place"
        label="籍贯"
        prop="id_place"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'id_place') !== -1"
      >
        <a-input v-model="employeeFormData.id_place" placeholder="请输入籍贯" />
      </a-form-model-item>
      <a-form-model-item
        ref="party"
        label="组织关系"
        prop="party"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'party') !== -1"
      >
        <a-select v-model="employeeFormData.party" placeholder="请选择组织关系">
          <a-select-option value="党员"> 党员 </a-select-option>
          <a-select-option value="团员"> 团员 </a-select-option>
          <a-select-option value="群众"> 群众 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="household_registration_type"
        label="户籍类型"
        prop="household_registration_type"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'household_registration_type') !== -1"
      >
        <a-select v-model="employeeFormData.household_registration_type" placeholder="请选择户籍类型">
          <a-select-option value="城镇"> 城镇 </a-select-option>
          <a-select-option value="农业"> 农业 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="hometown"
        label="户口所在地"
        prop="hometown"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'hometown') !== -1"
      >
        <a-input v-model="employeeFormData.hometown" placeholder="请输入户口所在地" />
      </a-form-model-item>
      <a-form-model-item
        ref="marry"
        label="婚姻情况"
        prop="marry"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'marry') !== -1"
      >
        <a-select v-model="employeeFormData.marry" placeholder="请选择婚姻情况">
          <a-select-option value="未婚"> 未婚 </a-select-option>
          <a-select-option value="已婚"> 已婚 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="max_degree"
        label="最高学历"
        prop="max_degree"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'max_degree') !== -1"
      >
        <a-select v-model="employeeFormData.max_degree" placeholder="请选择最高学历">
          <a-select-option value="博士"> 博士 </a-select-option>
          <a-select-option value="硕士"> 硕士 </a-select-option>
          <a-select-option value="本科"> 本科 </a-select-option>
          <a-select-option value="专科"> 专科 </a-select-option>
          <a-select-option value="高中"> 高中 </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item
        ref="emergency_person"
        label="紧急联系人"
        prop="emergency_person"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'emergency_person') !== -1"
      >
        <a-input v-model="employeeFormData.emergency_person" placeholder="请输入紧急联系人" />
      </a-form-model-item>
      <a-form-model-item
        ref="emergency_phone"
        label="紧急联系电话"
        prop="emergency_phone"
        :style="formModalItemStyle"
        v-if="attributes.findIndex((v) => v == 'emergency_phone') !== -1"
      >
        <a-input v-model="employeeFormData.emergency_phone" placeholder="请输入紧急联系电话" />
      </a-form-model-item>
      <a-form-model-item
        label="教育经历"
        prop="employeeFormData"
        :style="{ display: 'inline-block', width: '100%', margin: '0 7px' }"
        v-if="attributes.findIndex((v) => v == 'educational_experience') !== -1"
      >
        <a-row :gutter="[8, { xs: 8 }]" v-for="item in educational_experience" :key="item.id">
          <a-col :span="5">
            <a-input v-model="item.school" placeholder="学校" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-input v-model="item.major" placeholder="专业" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-select v-model="item.education" placeholder="学历" allowClear>
              <a-select-option value="小学"> 小学 </a-select-option>
              <a-select-option value="初中"> 初中 </a-select-option>
              <a-select-option value="中专/高中"> 中专/高中 </a-select-option>
              <a-select-option value="专科"> 专科 </a-select-option>
              <a-select-option value="本科"> 本科 </a-select-option>
              <a-select-option value="硕士"> 硕士 </a-select-option>
              <a-select-option value="博士"> 博士 </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="5">
            <a-month-picker
              v-model="item.graduation_year"
              placeholder="毕业年份"
              @change="onChange($event, 'graduation_year', item.id)"
            ></a-month-picker>
          </a-col>
          <a-col :span="1">
            <a @click="addEducation">
              <a-icon type="plus-circle" />
            </a>
          </a-col>
          <a-col :span="1" v-if="educational_experience.length > 1">
            <a @click="() => removeEducation(item.id)" :style="{ color: 'red' }">
              <a-icon type="delete" />
            </a>
          </a-col>
        </a-row>
      </a-form-model-item>
      <a-form-model-item
        label="子女信息"
        prop="employeeFormData"
        :style="{ display: 'inline-block', width: '100%', margin: '0 7px' }"
        v-if="attributes.findIndex((v) => v == 'children_information') !== -1"
      >
        <!-- <a-space
          v-for="(item,index) in educational_experience"
          :key="index"
          align="baseline"
          > -->
        <a-row :gutter="[8, { xs: 8 }]" v-for="item in children_information" :key="item.id">
          <a-col :span="5">
            <a-input v-model="item.name" placeholder="姓名" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-select v-model="item.gender" placeholder="请选择性别" allowClear>
              <a-select-option value="男"> 男 </a-select-option>
              <a-select-option value="女"> 女 </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="5">
            <a-date-picker
              v-model="item.birthday"
              placeholder="出生日期"
              @change="onChange($event, 'birth_date', item.id)"
            ></a-date-picker>
          </a-col>
          <a-col :span="5">
            <a-input-number
              :min="0"
              :step="1"
              :style="{ width: '100%' }"
              v-model="item.parental_leave_left"
              placeholder="请输入剩余育儿假"
              :formatter="(value) => `${value} 天`"
            />
          </a-col>
          <a-col :span="1">
            <a @click="addChildren">
              <a-icon type="plus-circle" />
            </a>
          </a-col>
          <a-col :span="1" v-if="children_information.length > 1">
            <a @click="() => removeChildren(item.id)" :style="{ color: 'red' }">
              <a-icon type="delete" />
            </a>
          </a-col>
        </a-row>
      </a-form-model-item>
      <a-form-model-item
        label="银行卡"
        prop="bank_card"
        :style="{ display: 'inline-block', width: '98%', margin: '0 7px 24px' }"
        v-if="
          attributes.findIndex((v) => v == 'bank_card_number') !== -1 ||
          attributes.findIndex((v) => v == 'bank_card_name') !== -1 ||
          attributes.findIndex((v) => v == 'opening_bank') !== -1 ||
          attributes.findIndex((v) => v == 'account_opening_location') !== -1
        "
      >
        <a-row :gutter="[8, { xs: 8 }]">
          <a-col :span="6" v-if="attributes.findIndex((v) => v == 'bank_card_number') !== -1">
            <a-input v-model="employeeFormData.bank_card_number" placeholder="卡号" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex((v) => v == 'bank_card_name') !== -1">
            <a-input v-model="employeeFormData.bank_card_name" placeholder="银行" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex((v) => v == 'opening_bank') !== -1">
            <a-input v-model="employeeFormData.opening_bank" placeholder="开户行" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex((v) => v == 'account_opening_location') !== -1">
            <a-input v-model="employeeFormData.account_opening_location" placeholder="开户地" allowClear></a-input>
          </a-col>
        </a-row>
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button key="back" @click="close"> 取消 </a-button>
      <a-button type="primary" @click="employeeModalHandleOk"> 确定 </a-button>
    </template>
  </a-modal>
</template>
<script>
import { mapState } from 'vuex'
import _ from 'lodash'
import { postEmployee, putEmployee } from '@/api/employee'
import Bus from './eventBus/bus'
import EmployeeTreeSelect from '../components/employeeTreeSelect.vue'
import DepartmentTreeSelect from '../components/departmentTreeSelect.vue'
import moment from 'moment'
import { v4 as uuidv4 } from 'uuid'
export default {
  components: { EmployeeTreeSelect, DepartmentTreeSelect },
  data() {
    return {
      visible: false,
      employeeFormData: {},
      formModalItemStyle: { display: 'inline-block', width: '48%', margin: '0 7px 24px', overflow: 'hidden' },
      rules: {
        email: [
          { required: true, whitespace: true, message: '请输入邮箱', trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: '邮箱格式错误',
            trigger: 'blur',
          },
          { max: 50, message: '字符数须小于50' },
        ],
        username: [
          { required: true, whitespace: true, message: '请输入用户名', trigger: 'blur' },
          { max: 20, message: '字符数须小于20' },
        ],
        password: [{ required: true, whitespace: true, message: '请输入密码', trigger: 'blur' }],
        nickname: [
          { required: true, whitespace: true, message: '请输入姓名', trigger: 'blur' },
          { max: 20, message: '字符数须小于20' },
        ],
        mobile: [
          {
            pattern: /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/,
            message: '请输入正确的手机号',
            trigger: 'blur',
          },
        ],
      },
      type: 'add',
      educational_experience: [],
      children_information: [],
      file_is_show: true,
      attributes: [],
    }
  },
  created() {
    Bus.$on('getAttributes', (attributes) => {
      this.attributes = attributes
    })
  },
  inject: ['provide_allTreeDepartment', 'provide_allFlatEmployees'],
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    departemntTreeSelectOption() {
      return this.provide_allTreeDepartment()
    },
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    },
    title() {
      if (this.type === 'add') {
        return '新建员工'
      }
      return '编辑员工'
    },
  },
  beforeDestroy() {
    Bus.$off('getAttributes')
  },
  methods: {
    async open(getData, type) {
      // 提交时去掉school, major, education, graduation_year, name, gender, birthday, parental_leave_left
      const { school, major, education, graduation_year, name, gender, birthday, parental_leave_left, ...newGetData } =
        getData
      const _getData = _.cloneDeep(newGetData)
      const { direct_supervisor_id } = newGetData
      if (direct_supervisor_id) {
        const _find = this.allFlatEmployees.find((item) => item.employee_id === direct_supervisor_id)
        _getData.direct_supervisor_id = `${_find.department_id}-${direct_supervisor_id}`
      } else {
        _getData.direct_supervisor_id = undefined
      }
      this.employeeFormData = _.cloneDeep(_getData)
      // if (type !== 'add' && this.employeeFormData.educational_experience.length !== 0) {
      //   this.educational_experience = this.employeeFormData.educational_experience
      // }
      this.children_information = this.formatChildrenInformationList() || [
        {
          id: uuidv4(),
          name: '',
          gender: undefined,
          birthday: null,
          parental_leave_left: 0,
        },
      ]
      this.educational_experience = this.formatEducationalExperienceList() || [
        {
          id: uuidv4(),
          school: '',
          major: '',
          education: undefined,
          graduation_year: null,
        },
      ]

      this.type = type
      this.visible = true
    },
    close() {
      this.$refs.employeeFormData.resetFields()
      this.educational_experience = [
        {
          school: '',
          major: '',
          education: undefined,
          graduation_year: null,
        },
      ]
      this.children_information = [
        {
          id: uuidv4(),
          name: '',
          gender: undefined,
          birthday: null,
          parental_leave_left: 0,
        },
      ]
      this.visible = false
    },
    formatChildrenInformationList() {
      let arr = []
      arr = this.employeeFormData.children_information ? this.employeeFormData.children_information : undefined
      if (arr && arr.length) {
        arr.forEach((item) => {
          item.id = uuidv4()
        })
        return arr
      }
      return null
    },
    formatEducationalExperienceList() {
      let arr = []
      arr = this.employeeFormData.educational_experience ? this.employeeFormData.educational_experience : undefined
      if (arr && arr.length) {
        arr.forEach((item) => {
          item.id = uuidv4()
        })
        return arr
      }
      return null
    },
    addEducation() {
      const newEducational_experience = {
        id: uuidv4(),
        school: '',
        major: '',
        education: undefined,
        graduation_year: null,
      }
      this.educational_experience.push(newEducational_experience)
    },
    removeEducation(removeId) {
      const _idx = this.educational_experience.findIndex((item) => item.id === removeId)
      if (_idx !== -1) {
        this.educational_experience.splice(_idx, 1)
      }
    },
    addChildren() {
      const newChildrenInfo = {
        id: uuidv4(),
        name: '',
        gender: undefined,
        birthday: null,
        parental_leave_left: 0,
      }
      this.children_information.push(newChildrenInfo)
    },
    removeChildren(removeId) {
      const _idx = this.children_information.findIndex((item) => item.id === removeId)
      if (_idx !== -1) {
        this.children_information.splice(_idx, 1)
      }
    },
    onChange(date, param, id) {
      // if (param === 'graduation_year') {
      //   if (date === null) {
      //     this.educational_experience[index].graduation_year = null
      //   } else {
      //     this.educational_experience[index].graduation_year = moment(date).format('YYYY-MM-DD')
      //   }
      // } else {
      //   if (date === null) {
      //     this.employeeFormData[param] = null
      //   } else {
      //     this.employeeFormData[param] = moment(date).format('YYYY-MM-DD')
      //   }
      // }
      if (date !== null) {
        if (param === 'graduation_year') {
          const _idx = this.educational_experience.findIndex((item) => item.id === id)
          this.educational_experience[_idx].graduation_year = moment(date).format('YYYY-MM')
        } else if (param === 'birth_date') {
          const _idx = this.children_information.findIndex((item) => item.id === id)
          this.children_information[_idx].birthday = moment(date).format('YYYY-MM-DD')
        } else {
          this.employeeFormData[param] = moment(date).format('YYYY-MM-DD')
        }
      }
    },
    async employeeModalHandleOk() {
      if (this.attributes.includes('educational_experience')) {
        this.employeeFormData.educational_experience = this.educational_experience
      }
      if (this.attributes.includes('children_information')) {
        this.employeeFormData.children_information = this.children_information
      }
      // if (!this.employeeFormData.annual_leave) {
      //   this.employeeFormData.annual_leave = 0
      // }
      const getFormData = this.employeeFormData
      getFormData.direct_supervisor_id = getFormData.direct_supervisor_id
        ? (getFormData.direct_supervisor_id + '').includes('-')
          ? +getFormData.direct_supervisor_id.split('-')[1]
          : +getFormData.direct_supervisor_id
        : 0
      this.$refs.employeeFormData.validate(async (valid) => {
        if (valid) {
          if (this.type === 'add') {
            await postEmployee(getFormData)
          }
          if (this.type === 'edit') {
            await putEmployee(getFormData.employee_id, getFormData)
          }
          this.$message.success('操作成功')
          this.$emit('refresh')
          Bus.$emit('updataAllIncludeEmployees')
          this.close()
        } else {
          this.$message.warning('检查您的输入是否正确!')
          return false
        }
      })
    },
  },
}
</script>
<style lang="less" scoped>
.el-date-picker {
  width: 100%;
  height: 36px;
}
</style>
