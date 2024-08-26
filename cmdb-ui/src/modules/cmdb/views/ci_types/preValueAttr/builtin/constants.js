export const BUILT_IN_TYPE = {
  DEPARTMENT: 'department', // 部门
  USER: 'user', // 用户
  USER_GROUP: 'userGroup' // 用户组
}

export const DISPLAY_VALUE_SELECT = [
  { label: 'cs.companyStructure.nickname', value: 'nickname' },
  { label: 'cs.companyStructure.email', value: 'email' },
  { label: 'cs.companyStructure.mobile', value: 'mobile' },
]

export const USER_FILTER_SELECT = [
  { label: 'cs.companyStructure.nickname', value: 'nickname' },
  { label: 'cs.companyStructure.username', value: 'username' },
  { label: 'cs.companyStructure.email', value: 'email' },
  {
    label: 'cs.companyStructure.sex',
    value: 'sex',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.male', value: '男' },
      { label: 'cs.companyStructure.female', value: '女' },
    ],
  },
  { label: 'cs.companyStructure.mobile', value: 'mobile' },
  { label: 'cs.companyStructure.departmentName', value: 'department_name' },
  { label: 'cs.companyStructure.positionName', value: 'position_name' },
  { label: 'cs.companyStructure.supervisor', value: 'direct_supervisor_id' },
  { label: 'cs.companyStructure.annualLeave', value: 'annual_leave' },
  { label: 'cs.companyStructure.currentCompany', value: 'current_company' },
  { label: 'cs.companyStructure.dfcEntryDate', value: 'dfc_entry_date' },
  { label: 'cs.companyStructure.entryDate', value: 'entry_date' },
  {
    label: 'cs.companyStructure.isInternship',
    value: 'is_internship',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.fullTime', value: 0 },
      { label: 'cs.companyStructure.internship', value: 1 },
    ],
  },
  { label: 'cs.companyStructure.leaveDate', value: 'leave_date' },
  { label: 'cs.companyStructure.idCard', value: 'id_card' },
  { label: 'cs.companyStructure.nation', value: 'nation' },
  { label: 'cs.companyStructure.idPlace', value: 'id_place' },
  {
    label: 'cs.companyStructure.party',
    value: 'party',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.partyMember', value: '党员' },
      { label: 'cs.companyStructure.member', value: '团员' },
      { label: 'cs.companyStructure.masses', value: '群众' },
    ],
  },
  {
    label: 'cs.companyStructure.householdRegistrationType',
    value: 'household_registration_type',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.town', value: '城镇' },
      { label: 'cs.companyStructure.agriculture', value: '农业' },
    ],
  },
  { label: 'cs.companyStructure.hometown', value: 'hometown' },
  {
    label: 'cs.companyStructure.marry',
    value: 'marry',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.unmarried', value: '未婚' },
      { label: 'cs.companyStructure.married', value: '已婚' },
    ],
  },
  {
    label: 'cs.companyStructure.maxDegree',
    value: 'max_degree',
    is_choice: true,
    choice_value: [
      { label: 'cs.companyStructure.phd', value: '博士' },
      { label: 'cs.companyStructure.master', value: '硕士' },
      {
        label: 'cs.companyStructure.undergraduate',
        value: '本科',
      },
      { label: 'cs.companyStructure.specialist', value: '专科' },
      { label: 'cs.companyStructure.highSchool', value: '高中' },
    ],
  },
  { label: 'cs.companyStructure.emergencyPerson', value: 'emergency_person' },
  { label: 'cs.companyStructure.emergencyPhone', value: 'emergency_phone' },
  { label: 'cs.companyStructure.bankCardNumber', value: 'bank_card_number' },
  { label: 'cs.companyStructure.bankCardName', value: 'bank_card_name' },
  { label: 'cs.companyStructure.openingBank', value: 'opening_bank' },
  { label: 'cs.companyStructure.accountOpeningLocation', value: 'account_opening_location' },
  { label: 'cs.companyStructure.birthDate', value: 'birth_date' },
  { label: 'cs.companyStructure.nationalityRegion', value: 'nationality_region' },
  { label: 'cs.companyStructure.birthPlace', value: 'birth_place' },
  { label: 'cs.companyStructure.firstEntryDate', value: 'first_entry_date' },
  { label: 'cs.companyStructure.estimatedDepartureDate', value: 'estimated_departure_date' },
  // { label: '角色', value: 'roles' },
  { label: 'cs.companyStructure.lastLogin', value: 'last_login' },
]
