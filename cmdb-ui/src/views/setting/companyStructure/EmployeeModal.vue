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
      <a-form-model-item ref="email" :label="$t('cs.companyStructure.email')" prop="email" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='email')!==-1">
        <a-input v-model="employeeFormData.email" :placeholder="$t('cs.companyStructure.emailPlaceholder')"/>
      </a-form-model-item>
      <a-form-model-item ref="username" :label="$t('cs.companyStructure.username')" prop="username" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='username')!==-1">
        <a-input v-model="employeeFormData.username" :placeholder="$t('cs.companyStructure.usernamePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item
        v-if="type === 'add'"
        ref="password"
        :label="$t('cs.companyStructure.password')"
        prop="password"
        :style="formModalItemStyle"
      >
        <a-input-password v-model="employeeFormData.password" :placeholder="$t('cs.companyStructure.passwordPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="nickname" :label="$t('cs.companyStructure.nickname')" prop="nickname" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='nickname')!==-1">
        <a-input v-model="employeeFormData.nickname" :placeholder="$t('cs.companyStructure.nicknamePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyStructure.sex')" prop="sex" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='sex')!==-1">
        <a-select v-model="employeeFormData.sex" :placeholder="$t('cs.companyStructure.sexPlaceholder')">
          <a-select-option value="男"> {{ $t('cs.companyStructure.male') }} </a-select-option>
          <a-select-option value="女"> {{ $t('cs.companyStructure.female') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="mobile" :label="$t('cs.companyStructure.mobile')" prop="mobile" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='mobile')!==-1">
        <a-input v-model="employeeFormData.mobile" :placeholder="$t('cs.companyStructure.mobilePlaceholder')" />
      </a-form-model-item>
      <div :style="{ width: '361px', display: 'inline-block', margin: '0 7px' }" v-if="attributes.findIndex(v=>v=='department_id')!==-1">
        <div :style="{ height: '41px', lineHeight: '40px' }">{{ $t('cs.companyStructure.departmentName') }}</div>
        <DepartmentTreeSelect v-model="employeeFormData.department_id" />
      </div>
      <a-form-model-item ref="position_name" :label="$t('cs.companyStructure.positionName')" prop="position_name" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='position_name')!==-1">
        <a-input v-model="employeeFormData.position_name" :placeholder="$t('cs.companyStructure.positionNamePlaceholder')" />
      </a-form-model-item>
      <div :style="{ width: '361px', display: 'inline-block', margin: '0 7px' }" v-if="attributes.findIndex(v=>v=='direct_supervisor_id')!==-1">
        <div :style="{ height: '41px', lineHeight: '40px' }">{{ $t('cs.companyStructure.selectDirectSupervisor') }}</div>
        <EmployeeTreeSelect v-model="employeeFormData.direct_supervisor_id" />
      </div>
      <!-- <a-form-model-item :label="角色" prop="role" :style="formModalItemStyle">
        <a-select mode="multiple" v-model="employeeFormData.role" :placeholder="请选择角色">
          <a-select-option value="PM"> PM </a-select-option>
          <a-select-option value="Test"> Test </a-select-option>
          <a-select-option value="Tevelop"> Develop </a-select-option>
        </a-select>
      </a-form-model-item> -->
      <a-form-model-item ref="annual_leave" :label="$t('cs.companyStructure.annualLeave')" prop="annual_leave" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='annual_leave')!==-1">
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.annual_leave"
          :placeholder="$t('cs.companyStructure.annualLeavePlaceholder')"
          :formatter="(value) => `${value} $t('cs.companyStructure.day')`"
        />
      </a-form-model-item>
      <a-form-model-item ref="virtual_annual_leave" :label="$t('cs.companyStructure.virtualAnnualLeave')" prop="virtual_annual_leave" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='virtual_annual_leave')!==-1">
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.virtual_annual_leave"
          :placeholder="$t('cs.companyStructure.virtualAnnualLeavePlaceholder')"
          :formatter="(value) => `${value} $t('cs.companyStructure.day')`"
        />
      </a-form-model-item>
      <a-form-model-item ref="parenting_leave" :label="$t('cs.companyStructure.parentingLeave')" prop="parenting_leave" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='parenting_leave')!==-1">
        <a-input-number
          :min="0"
          :step="1"
          :style="{ width: '100%' }"
          v-model="employeeFormData.parenting_leave"
          :placeholder="$t('cs.companyStructure.parentingLeavePlaceholder')"
          :formatter="(value) => `${value} $t('cs.companyStructure.day')`"
        />
      </a-form-model-item>
      <a-form-model-item v-if="attributes.findIndex(v=>v=='current_company')!==-1" ref="current_company" :label="$t('cs.companyStructure.currentCompany')" prop="current_company" :style="formModalItemStyle">
        <a-input v-model="employeeFormData.current_company" :placeholder="$t('cs.companyStructure.currentCompanyPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item v-if="attributes.findIndex(v=>v=='dfc_entry_date')!==-1" ref="dfc_entry_date" :label="$t('cs.companyStructure.dfcEntryDate')" prop="dfc_entry_date" :style="formModalItemStyle">
        <a-date-picker :placeholder="$t('cs.companyStructure.dfcEntryDatePlaceholder')" v-model="employeeFormData.dfc_entry_date" :style="{ width: '100%'}" @change="onChange($event, 'dfc_entry_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item ref="entry_date" :label="$t('cs.companyStructure.entryDate')" prop="entry_date" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='entry_date')!==-1">
        <a-date-picker :placeholder="$t('cs.companyStructure.entryDatePlaceholder')" v-model="employeeFormData.entry_date" :style="{ width: '100%'}" @change="onChange($event, 'entry_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item ref="is_internship" :label="$t('cs.companyStructure.isInternship')" prop="is_internship" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='is_internship')!==-1">
        <a-select v-model="employeeFormData.is_internship" :placeholder="$t('cs.companyStructure.isInternshipPlaceholder')">
          <a-select-option :value="0"> {{ $t('cs.companyStructure.fullTime') }} </a-select-option>
          <a-select-option :value="1"> {{ $t('cs.companyStructure.internship') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="leave_date" :label="$t('cs.companyStructure.leaveDate')" prop="leave_date" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='leave_date')!==-1">
        <a-date-picker v-model="employeeFormData.leave_date" :placeholder="$t('cs.companyStructure.leaveDatePlaceholder')" :style="{ width: '100%'}" @change="onChange($event, 'leave_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item ref="id_card" :label="$t('cs.companyStructure.idCard')" prop="id_card" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='id_card')!==-1">
        <a-input v-model="employeeFormData.id_card" :placeholder="$t('cs.companyStructure.idCardPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="nation" :label="$t('cs.companyStructure.nation')" prop="nation" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='nation')!==-1">
        <a-input v-model="employeeFormData.nation" :placeholder="$t('cs.companyStructure.nationPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="id_place" :label="$t('cs.companyStructure.idPlace')" prop="id_place" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='id_place')!==-1">
        <a-input v-model="employeeFormData.id_place" :placeholder="$t('cs.companyStructure.idPlacePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="party" :label="$t('cs.companyStructure.party')" prop="party" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='party')!==-1">
        <a-select v-model="employeeFormData.party" :placeholder="$t('cs.companyStructure.')">
          <a-select-option value="党员"> {{ $t('cs.companyStructure.partyMember') }} </a-select-option>
          <a-select-option value="团员"> {{ $t('cs.companyStructure.member') }} </a-select-option>
          <a-select-option value="群众"> {{ $t('cs.companyStructure.masses') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="household_registration_type" :label="$t('cs.companyStructure.householdRegistrationType')" prop="household_registration_type" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='household_registration_type')!==-1">
        <a-select v-model="employeeFormData.household_registration_type" :placeholder="$t('cs.companyStructure.')">
          <a-select-option value="城镇"> {{ $t('cs.companyStructure.town') }} </a-select-option>
          <a-select-option value="农业"> {{ $t('cs.companyStructure.agriculture') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="hometown" :label="$t('cs.companyStructure.hometown')" prop="hometown" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='hometown')!==-1">
        <a-input v-model="employeeFormData.hometown" :placeholder="$t('cs.companyStructure.hometownPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="marry" :label="$t('cs.companyStructure.marry')" prop="marry" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='marry')!==-1">
        <a-select v-model="employeeFormData.marry" :placeholder="$t('cs.companyStructure.')">
          <a-select-option value="未婚"> {{ $t('cs.companyStructure.unmarried') }}</a-select-option>
          <a-select-option value="已婚"> {{ $t('cs.companyStructure.married') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="max_degree" :label="$t('cs.companyStructure.maxDegree')" prop="max_degree" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='max_degree')!==-1">
        <a-select v-model="employeeFormData.max_degree" :placeholder="$t('cs.companyStructure.maxDegreePlaceholder')">
          <a-select-option value="博士"> {{ $t('cs.companyStructure.phd') }} </a-select-option>
          <a-select-option value="硕士"> {{ $t('cs.companyStructure.master') }} </a-select-option>
          <a-select-option value="本科"> {{ $t('cs.companyStructure.undergraduate') }} </a-select-option>
          <a-select-option value="专科"> {{ $t('cs.companyStructure.specialist') }} </a-select-option>
          <a-select-option value="高中"> {{ $t('cs.companyStructure.highSchool') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item ref="emergency_person" :label="$t('cs.companyStructure.emergencyPerson')" prop="emergency_person" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='emergency_person')!==-1">
        <a-input v-model="employeeFormData.emergency_person" :placeholder="$t('cs.companyStructure.emergencyPersonPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="emergency_phone" :label="$t('cs.companyStructure.emergencyPhone')" prop="emergency_phone" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='emergency_phone')!==-1">
        <a-input v-model="employeeFormData.emergency_phone" :placeholder="$t('cs.companyStructure.emergencyPhonePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="birth_date" :label="$t('cs.companyStructure.birthDate')" prop="birth_date" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='birth_date')!==-1">
        <a-date-picker v-model="employeeFormData.birth_date" :placeholder="$t('cs.companyStructure.birthDatePlaceholder')" :style="{ width: '100%'}" @change="onChange($event, 'birth_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item ref="birth_place" :label="$t('cs.companyStructure.birthPlace')" prop="birth_place" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='birth_place')!==-1">
        <a-input v-model="employeeFormData.birth_place" :placeholder="$t('cs.companyStructure.birthPlacePlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="nationality_region" :label="$t('cs.companyStructure.nationalityRegion')" prop="nationality_region" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='nationality_region')!==-1">
        <a-input v-model="employeeFormData.nationality_region" :placeholder="$t('cs.companyStructure.nationalityRegionPlaceholder')" />
      </a-form-model-item>
      <a-form-model-item ref="first_entry_date" :label="$t('cs.companyStructure.firstEntryDate')" prop="first_entry_date" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='first_entry_date')!==-1">
        <a-date-picker v-model="employeeFormData.first_entry_date" :placeholder="$t('cs.companyStructure.firstEntryDatePlaceholder')" :style="{ width: '100%'}" @change="onChange($event, 'first_entry_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item ref="estimated_departure_date" :label="$t('cs.companyStructure.estimatedDepartureDate')" prop="estimated_departure_date" :style="formModalItemStyle" v-if="attributes.findIndex(v=>v=='estimated_departure_date')!==-1">
        <a-date-picker v-model="employeeFormData.estimated_departure_date" :placeholder="$t('cs.companyStructure.estimatedDepartureDatePlaceholder')" :style="{ width: '100%'}" @change="onChange($event, 'estimated_departure_date')"></a-date-picker>
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyStructure.educationalExperience')" prop="employeeFormData" :style="{ display: 'inline-block', width: '100%', margin: '0 7px'}" v-if="attributes.findIndex(v=>v=='educational_experience')!==-1">
        <a-row
          :gutter="[8,{xs:8}]"
          v-for="(item) in educational_experience"
          :key="item.id"
        >
          <a-col :span="5">
            <a-input v-model="item.school" :placeholder="$t('cs.companyStructure.school')" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-input v-model="item.major" :placeholder="$t('cs.companyStructure.major')" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-select v-model="item.education" :placeholder="$t('cs.companyStructure.education')" allowClear>
              <a-select-option value="小学"> {{ $t('cs.companyStructure.primarySchool') }} </a-select-option>
              <a-select-option value="初中"> {{ $t('cs.companyStructure.juniorHighSchool') }} </a-select-option>
              <a-select-option value="中专/高中"> {{ $t('cs.companyStructure.technicalSecondaryOrHighSchool') }} </a-select-option>
              <a-select-option value="专科"> {{ $t('cs.companyStructure.specialist') }} </a-select-option>
              <a-select-option value="本科"> {{ $t('cs.companyStructure.undergraduate') }} </a-select-option>
              <a-select-option value="硕士"> {{ $t('cs.companyStructure.master') }} </a-select-option>
              <a-select-option value="博士"> {{ $t('cs.companyStructure.phd') }} </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="5">
            <a-month-picker v-model="item.graduation_year" :placeholder="$t('cs.companyStructure.graduationYearPlaceholder')"  @change="onChange($event, 'graduation_year',item.id)" ></a-month-picker>
          </a-col>
          <a-col :span="1">
            <a
              @click="addEducation"
            >
              <a-icon type="plus-circle" />
            </a>
          </a-col>
          <a-col :span="1" v-if="educational_experience.length > 1">
            <a
              @click="() => removeEducation(item.id)"
              :style="{ color: 'red' }"
            >
              <a-icon type="delete" />
            </a>
          </a-col>
        </a-row>
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyStructure.childrenInformation')" prop="employeeFormData" :style="{ display: 'inline-block', width: '100%', margin: '0 7px'}" v-if="attributes.findIndex(v=>v=='children_information')!==-1">
        <!-- <a-space
          v-for="(item,index) in educational_experience"
          :key="index"
          align="baseline"
          > -->
        <a-row
          :gutter="[8,{xs:8}]"
          v-for="(item) in children_information"
          :key="item.id"
        >
          <a-col :span="5">
            <a-input v-model="item.name" :placeholder="$t('cs.companyStructure.childrenName')" allowClear></a-input>
          </a-col>
          <a-col :span="5">
            <a-select v-model="item.gender" :placeholder="$t('cs.companyStructure.sex')"  allowClear>
              <a-select-option value="男"> {{ $t('cs.companyStructure.male') }} </a-select-option>
              <a-select-option value="女"> {{ $t('cs.companyStructure.female') }} </a-select-option>
            </a-select>
          </a-col>
          <a-col :span="5">
            <a-date-picker v-model="item.birthday" :placeholder="$t('cs.companyStructure.birthDatePlaceholder')" @change="onChange($event, 'birthday',item.id)"></a-date-picker>
          </a-col>
          <a-col :span="5">
            <a-input-number
              :min="0"
              :step="1"
              :style="{ width: '100%' }"
              v-model="item.parental_leave_left"
              :placeholder="$t('cs.companyStructure.')"
              :formatter="(value) => `${value} $t('cs.companyStructure.day')`"
            />
          </a-col>
          <a-col :span="1">
            <a
              @click="addChildren"
            >
              <a-icon type="plus-circle" />
            </a>
          </a-col>
          <a-col :span="1" v-if="children_information.length > 1">
            <a
              @click="() => removeChildren(item.id)"
              :style="{ color: 'red' }"
            >
              <a-icon type="delete" />
            </a>
          </a-col>
        </a-row>
      </a-form-model-item>
      <a-form-model-item
        :label="$t('cs.companyStructure.bankCardInfo')"
        prop="bank_card"
        :style="{display: 'inline-block', width: '98%', margin: '0 7px 24px'}"
        v-if="attributes.findIndex(v=>v=='bank_card_number')!==-1 || attributes.findIndex(v=>v=='bank_card_name')!==-1 || attributes.findIndex(v=>v=='opening_bank')!==-1 || attributes.findIndex(v=>v=='account_opening_location')!==-1"
      >
        <a-row :gutter="[8,{xs:8}]">
          <a-col :span="6" v-if="attributes.findIndex(v=>v=='bank_card_number')!==-1">
            <a-input v-model="employeeFormData.bank_card_number" :placeholder="$t('cs.companyStructure.bankCardNumberPlaceholder')" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex(v=>v=='bank_card_name')!==-1">
            <a-input v-model="employeeFormData.bank_card_name" :placeholder="$t('cs.companyStructure.bankCardNamePlaceholder')" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex(v=>v=='opening_bank')!==-1">
            <a-input v-model="employeeFormData.opening_bank" :placeholder="$t('cs.companyStructure.openingBankPlaceholder')" allowClear></a-input>
          </a-col>
          <a-col :span="6" v-if="attributes.findIndex(v=>v=='account_opening_location')!==-1">
            <a-input v-model="employeeFormData.account_opening_location" :placeholder="$t('cs.companyStructure.accountOpeningLocationPlaceholder')" allowClear></a-input>
          </a-col>
        </a-row>
      </a-form-model-item>
    </a-form-model>
    <template slot="footer">
      <a-button key="back" @click="close"> {{ $t('cancel') }} </a-button>
      <a-button type="primary" @click="employeeModalHandleOk"> {{ $t('confirm') }} </a-button>
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
      type: 'add',
      educational_experience: [],
      children_information: [],
      file_is_show: true,
      attributes: []
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
        return this.$t('cs.companyStructure.createEmployee')
      }
      return this.$t('cs.companyStructure.editEmployee')
    },
    rules() {
      return {
        email: [
          { required: true, whitespace: true, message: this.$t('cs.companyStructure.emailPlaceholder'), trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: this.$t('cs.companyStructure.emailFormatErr'),
            trigger: 'blur',
          },
          { max: 50, message: this.$t('cs.person.inputStrCountLimit', { limit: 50 }) },
        ],
        username: [
          { required: true, whitespace: true, message: '请输入用户名', trigger: 'blur' },
          { max: 20, message: this.$t('cs.person.inputStrCountLimit', { limit: 20 }) },
        ],
        password: [{ required: true, whitespace: true, message: '请输入密码', trigger: 'blur' }],
        nickname: [
          { required: true, whitespace: true, message: '请输入姓名', trigger: 'blur' },
          { max: 20, message: this.$t('cs.person.inputStrCountLimit', { limit: 20 }) },
        ],
        mobile: [
          {
            pattern: /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/,
            message: this.$t('cs.companyStructure.mobileFormatErr'),
            trigger: 'blur',
          },
        ],
      }
    }
  },
  beforeDestroy() {
    Bus.$off('getAttributes')
  },
  methods: {
    async open(getData, type) {
      // 提交时去掉school, major, education, graduation_year, name, gender, birthday, parental_leave_left
      const { school, major, education, graduation_year, name, gender, birthday, parental_leave_left, ...newGetData } = getData
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
      this.children_information = this.formatChildrenInformationList() || [{
        id: uuidv4(),
        name: '',
        gender: undefined,
        birthday: null,
        parental_leave_left: 0
      }]
      this.educational_experience = this.formatEducationalExperienceList() || [{
        id: uuidv4(),
        school: '',
        major: '',
        education: undefined,
        graduation_year: null
      }]

      this.type = type
      this.visible = true
    },
    close() {
      this.$refs.employeeFormData.resetFields()
      this.educational_experience = [{
        school: '',
        major: '',
        education: undefined,
        graduation_year: null
      }]
      this.children_information = [{
        id: uuidv4(),
        name: '',
        gender: undefined,
        birthday: null,
        parental_leave_left: 0
      }]
      this.visible = false
    },
    formatChildrenInformationList() {
      let arr = []
      arr = this.employeeFormData.children_information ? this.employeeFormData.children_information : undefined
      if (arr && arr.length) {
        arr.forEach(item => {
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
        arr.forEach(item => {
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
        graduation_year: null
      }
      this.educational_experience.push(newEducational_experience)
    },
    removeEducation(removeId) {
      const _idx = this.educational_experience.findIndex(item => item.id === removeId)
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
        parental_leave_left: 0
      }
      this.children_information.push(newChildrenInfo)
    },
    removeChildren(removeId) {
      const _idx = this.children_information.findIndex(item => item.id === removeId)
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
          const _idx = this.educational_experience.findIndex(item => item.id === id)
          this.educational_experience[_idx].graduation_year = moment(date).format('YYYY-MM')
        } else if (param === 'birthday') {
          const _idx = this.children_information.findIndex(item => item.id === id)
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
          this.$message.success(this.$t('cs.companyStructure.opSuccess'))
          this.$emit('refresh')
          Bus.$emit('updataAllIncludeEmployees')
          this.close()
        } else {
          this.$message.warning(this.$t('cs.companyInfo.checkInputCorrect'))
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
