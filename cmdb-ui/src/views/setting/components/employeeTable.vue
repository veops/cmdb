<template>
  <vxe-table
    ref="employeeTable"
    border="none"
    stripe
    :data="tableData"
    show-overflow
    show-header-overflow
    highlight-hover-row
    size="small"
    class="ops-stripe-table"
    :height="tableHeight"
    :loading="loading"
    :sort-config="{ remote: true, trigger: 'cell', multiple: true }"
    @sort-change="sortChangeEvent"
    :column-config="{ resizable: true }"
    @checkbox-change="onSelectChange"
    @checkbox-all="onSelectChange"
    :filter-config="{ remote: true }"
    @filter-change="filterChangeEvent"
    :tooltip-config="{ contentMethod: contentMethod }"
    :column-key="true"
    :row-key="true"
  >
    <vxe-column type="checkbox" width="60px" v-if="isEditable && attributes.length" fixed="left"></vxe-column>
    <vxe-column
      field="nickname"
      min-width="100px"
      title="姓名"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'nickname') !== -1 && attributes.findIndex((v) => v == 'nickname') !== -1"
      key="nickname"
      fixed="left"
    >
      <template #default="{ row }">
        <div
          :style="{
            display: 'inline-block',
            width: '6px',
            marginBottom: '1px',
            height: '6px',
            borderRadius: '50%',
            backgroundColor: row.block ? '#ff6767' : '#49cc90',
            marginRight: '8px',
          }"
        ></div>
        <div :style="{ display: 'inline-block' }">{{ row.nickname }}</div>
      </template>
    </vxe-column>
    <vxe-column
      field="username"
      title="用户名"
      min-width="120px"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'username') !== -1 && attributes.findIndex((v) => v == 'username') !== -1"
      key="username"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>用户名</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="email"
      title="邮箱"
      min-width="140px"
      sortable
      v-if="checkedCols.findIndex((v) => v == 'email') !== -1 && attributes.findIndex((v) => v == 'email') !== -1"
      key="email"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>邮箱</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="sex"
      title="性别"
      width="70px"
      sortable
      align="center"
      v-if="checkedCols.findIndex((v) => v == 'sex') !== -1 && attributes.findIndex((v) => v == 'sex') !== -1"
      key="sex"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>性别</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="mobile"
      title="手机号"
      min-width="100px"
      v-if="checkedCols.findIndex((v) => v == 'mobile') !== -1 && attributes.findIndex((v) => v == 'mobile') !== -1"
      sortable
      key="mobile"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>手机号</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="department_name"
      title="部门"
      min-width="90px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'department_name') !== -1 &&
          attributes.findIndex((v) => v == 'department_name') !== -1
      "
      key="department_name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>部门</span>
        </span>
      </template>
      <template #default="{ row }">
        <!-- {{ getDepartmentName(allFlatDepartments, row.department_id) }} -->
        {{ row.department_name }}
      </template>
    </vxe-column>
    <vxe-column
      field="position_name"
      title="岗位"
      min-width="120px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'position_name') !== -1 &&
          attributes.findIndex((v) => v == 'position_name') !== -1
      "
      key="position_name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>岗位</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="direct_supervisor_id"
      title="直接上级"
      min-width="120px"
      sortable
      v-if="
        checkedCols.findIndex((v) => v == 'direct_supervisor_id') !== -1 &&
          attributes.findIndex((v) => v == 'direct_supervisor_id') !== -1
      "
      key="direct_supervisor_id"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>直接上级</span>
        </span>
      </template>
      <template #default="{ row }">
        <span v-if="row.direct_supervisor_id !== 0">{{
          getDirectorName(allFlatEmployees, row.direct_supervisor_id)
        }}</span>
      </template>
    </vxe-column>
    <vxe-column
      field="annual_leave"
      title="年假"
      sortable
      min-width="80"
      v-if="
        checkedCols.findIndex((v) => v == 'annual_leave') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'annual_leave') !== -1
      "
      key="annual_leave"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>年假</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="virtual_annual_leave"
      title="虚拟年假"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'virtual_annual_leave') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'virtual_annual_leave') !== -1
      "
      key="virtual_annual_leave"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>虚拟年假</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="parenting_leave"
      title="育儿假"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'parenting_leave') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'parenting_leave') !== -1
      "
      key="parenting_leave"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>育儿假</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="current_company"
      title="目前所属主体"
      sortable
      min-width="120"
      v-if="
        useDFC &&
          checkedCols.findIndex((v) => v == 'current_company') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'current_company') !== -1
      "
      key="current_company"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>目前所属主体</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="dfc_entry_date"
      title="初始入职日期"
      sortable
      min-width="120"
      v-if="
        useDFC &&
          checkedCols.findIndex((v) => v == 'dfc_entry_date') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'dfc_entry_date') !== -1
      "
      key="dfc_entry_date"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>初始入职日期</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="entry_date"
      title="目前主体入职日期"
      sortable
      min-width="150"
      v-if="
        checkedCols.findIndex((v) => v == 'entry_date') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'entry_date') !== -1
      "
      key="entry_date"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>目前主体入职日期</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="is_internship"
      title="正式/实习生"
      sortable
      min-width="140"
      v-bind="tableType === 'structure' ? { filters: internOptions, 'filter-multiple': false } : {}"
      v-if="
        checkedCols.findIndex((v) => v == 'is_internship') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'is_internship') !== -1
      "
      key="is_internship"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>正式/实习生</span>
        </span>
      </template>
      <template #default="{ row }">
        {{ getIsInterInship(row.is_internship) }}
      </template> </vxe-column
    >I
    <vxe-column
      field="leave_date"
      title="离职日期"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'leave_date') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'leave_date') !== -1
      "
      key="leave_date"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>离职日期</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="id_card"
      title="身份证号码"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'id_card') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'id_card') !== -1
      "
      key="id_card"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>身份证号码</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="nation"
      title="民族"
      sortable
      min-width="80"
      v-if="
        checkedCols.findIndex((v) => v == 'nation') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'nation') !== -1
      "
      key="nation"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>民族</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="id_place"
      title="籍贯"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'id_place') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'id_place') !== -1
      "
      key="id_place"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>籍贯</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="party"
      title="组织关系"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'party') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'party') !== -1
      "
      key="party"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>组织关系</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="household_registration_type"
      title="户籍类型"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'household_registration_type') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'household_registration_type') !== -1
      "
      key="household_registration_type"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>户籍类型</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="hometown"
      title="户口所在地"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'hometown') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'hometown') !== -1
      "
      key="hometown"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>户口所在地</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="marry"
      title="婚姻情况"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'marry') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'marry') !== -1
      "
      key="marry"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>婚姻情况</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="max_degree"
      title="最高学历"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'max_degree') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'max_degree') !== -1
      "
      key="max_degree"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>最高学历</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="emergency_person"
      title="紧急联系人"
      sortable
      min-width="110"
      v-if="
        checkedCols.findIndex((v) => v == 'emergency_person') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'emergency_person') !== -1
      "
      key="emergency_person"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>紧急联系人</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="emergency_phone"
      title="紧急联系电话"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'emergency_phone') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'emergency_phone') !== -1
      "
      key="emergency_phone"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>紧急联系电话</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="bank_card_number"
      title="卡号"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'bank_card_number') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'bank_card_number') !== -1
      "
      key="bank_card_number"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>卡号</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="bank_card_name"
      title="银行"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'bank_card_name') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'bank_card_name') !== -1
      "
      key="bank_card_name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>银行</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="opening_bank"
      title="开户行"
      sortable
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'opening_bank') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'opening_bank') !== -1
      "
      key="opening_bank"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>开户行</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="account_opening_location"
      title="开户地"
      sortable
      min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'account_opening_location') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'account_opening_location') !== -1
      "
      key="account_opening_location"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>开户地</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="school"
      title="学校"
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'school') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'school') !== -1
      "
      key="school"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>学校</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="major"
      title="专业"
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'major') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'major') !== -1
      "
      key="major"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>专业</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="education"
      title="学历"
      min-width="80"
      v-if="
        checkedCols.findIndex((v) => v == 'education') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'education') !== -1
      "
      key="education"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>学历</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="graduation_year"
      title="毕业年份"
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'graduation_year') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'graduation_year') !== -1
      "
      key="graduation_year"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>毕业年份</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="name"
      title="子女姓名"
      min-width="80"
      v-if="
        checkedCols.findIndex((v) => v == 'name') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'name') !== -1
      "
      key="name"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>子女姓名</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="gender"
      title="子女性别"
      min-width="80"
      v-if="
        checkedCols.findIndex((v) => v == 'gender') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'gender') !== -1
      "
      key="gender"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>子女性别</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="birthday"
      title="子女出生日期"
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'birthday') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'birthday') !== -1
      "
      key="birthday"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>子女出生日期</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="parental_leave_left"
      title="剩余育儿假"
      min-width="100"
      v-if="
        checkedCols.findIndex((v) => v == 'parental_leave_left') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'parental_leave_left') !== -1
      "
      key="parental_leave_left"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>剩余育儿假</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="roles"
      title="角色"
      v-bind="tableType === 'structure' ? { filters: [], 'filter-multiple': true } : {}"
      :min-width="120"
      v-if="
        checkedCols.findIndex((v) => v == 'roles') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'roles') !== -1
      "
      key="role"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>角色</span>
        </span>
      </template>
      <template #default="{ row }">
        <a-popover v-if="row.roles.length">
          <template slot="content">
            <a-tag v-for="item in row.roles" color="blue" :key="item.role_id" :style="{ marginBottom: '2px' }">
              {{ item.role_name }}
            </a-tag>
          </template>
          <span>
            <a-tag v-for="item in row.roles" color="blue" :key="item.role_id" :style="{ marginBottom: '2px' }">
              {{ item.role_name }}
            </a-tag>
          </span>
        </a-popover>
      </template>
    </vxe-column>
    <vxe-column
      field="last_login"
      title="上次登录时间"
      min-width="140px"
      sortable
      :formatter="formatDate"
      v-if="
        checkedCols.findIndex((v) => v == 'last_login') !== -1 &&
          tableType == 'structure' &&
          attributes.findIndex((v) => v == 'last_login') !== -1
      "
      key="last_login"
    >
      <template #header>
        <span class="vxe-handle">
          <OpsMoveIcon class="move-icon" />
          <span>上次登录时间</span>
        </span>
      </template>
    </vxe-column>
    <vxe-column
      field="control"
      width="100px"
      align="center"
      v-if="isEditable && attributes.length"
      fixed="right"
      key="control"
    >
      <template #header>
        <span>操作</span>
        <template>
          <a-popover
            title="请选择需要展示的列"
            placement="bottom"
            v-model="visible"
            trigger="click"
            v-if="tableType == 'structure'"
            @visibleChange="visibleChange"
            destroyTooltipOnHide
          >
            <template slot="content">
              <div :style="{ maxHeight: `${windowHeight - 320}px`, overflowY: 'auto', width: '160px' }">
                <a-checkbox-group v-model="unsbmitCheckedCols" :options="options" style="display: grid;">
                </a-checkbox-group>
              </div>
              <div
                :style="{
                  marginTop: '5px',
                  height: '20px',
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'flex-end',
                }"
              >
                <a-button :style="{ marginRight: '10px' }" size="small" @click="handleCancel">取消</a-button>
                <a-button size="small" @click="handleSubmit" type="primary">确定</a-button>
              </div>
            </template>
            <a-icon type="control" style="cursor: pointer;" />
          </a-popover>
        </template>
      </template>
      <template #default="{ row }">
        <a-space v-if="tableType === 'structure'">
          <a><a-icon type="edit" @click="openEmployeeModal(row, 'edit')"/></a>
          <a-tooltip>
            <template slot="title">
              重置密码
            </template>
            <a><a-icon type="reload" @click="openBatchModal('password', row)"/></a>
          </a-tooltip>
          <a-tooltip v-if="!row.block">
            <template slot="title">
              禁用
            </template>
            <a :style="{ color: 'red' }" @click="openBatchModal('block', row, 1)">
              <ops-icon type="icon-xianxing-weilianjie" />
            </a>
          </a-tooltip>
          <a-tooltip v-else>
            <template slot="title">
              恢复
            </template>
            <a @click="openBatchModal('block', row, 0)">
              <ops-icon type="icon-xianxing-yilianjie" />
            </a>
          </a-tooltip>
        </a-space>
        <a-tooltip v-else>
          <template slot="title">
            移除
          </template>
          <a :style="{ color: 'red' }" @click="removeEmployee(row)">
            <ops-icon type="icon-xianxing-shanchuyonghu" />
          </a>
        </a-tooltip>
      </template>
    </vxe-column>
    <template #empty>
      <div>
        <img :style="{ width: '200px' }" :src="require('@/assets/data_empty.png')" />
        <div>暂无数据</div>
      </div>
    </template>
  </vxe-table>
</template>

<script>
import { mapState } from 'vuex'
import { getRoleList } from '@/api/role'
import { getDepartmentName, getDirectorName } from '@/utils/util'
import Bus from '../companyStructure/eventBus/bus'
import appConfig from '@/config/app'
import Sortable from 'sortablejs'
import XEUtils from 'xe-utils'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'

export default {
  name: 'EmployeeTable',
  components: { OpsMoveIcon },
  props: {
    tableData: {
      type: Array,
      default: () => [],
    },
    tableHeight: {
      type: Number,
      default: 0,
    },
    tableType: {
      type: String,
      default: 'structure',
    },
    isEditable: {
      type: Boolean,
      default: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    const options = [
      { label: '姓名', value: 'nickname' },
      { label: '用户名', value: 'username' },
      { label: '邮箱', value: 'email' },
      { label: '性别', value: 'sex' },
      { label: '手机号', value: 'mobile' },
      { label: '部门', value: 'department_name' },
      { label: '岗位', value: 'position_name' },
      { label: '直接上级', value: 'direct_supervisor_id' },
      { label: '年假', value: 'annual_leave' },
      { label: '虚拟年假', value: 'virtual_annual_leave' },
      { label: '育儿假', value: 'parenting_leave' },
      { label: '目前所属主体', value: 'current_company' },
      { label: '初始入职日期', value: 'dfc_entry_date' },
      { label: '目前主体入职日期', value: 'entry_date' },
      { label: '正式/实习生', value: 'is_internship' },
      { label: '离职日期', value: 'leave_date' },
      { label: '身份证号码', value: 'id_card' },
      { label: '民族', value: 'nation' },
      { label: '籍贯', value: 'id_place' },
      { label: '组织关系', value: 'party' },
      { label: '户籍类型', value: 'household_registration_type' },
      { label: '户口所在地', value: 'hometown' },
      { label: '婚姻情况', value: 'marry' },
      { label: '最高学历', value: 'max_degree' },
      { label: '紧急联系人', value: 'emergency_person' },
      { label: '紧急联系电话', value: 'emergency_phone' },
      { label: '卡号', value: 'bank_card_number' },
      { label: '银行', value: 'bank_card_name' },
      { label: '开户行', value: 'opening_bank' },
      { label: '开户地', value: 'account_opening_location' },
      { label: '学校', value: 'school' },
      { label: '专业', value: 'major' },
      { label: '学历', value: 'education' },
      { label: '毕业年份', value: 'graduation_year' },
      { label: '子女姓名', value: 'name' },
      { label: '子女性别', value: 'gender' },
      { label: '子女出生日期', value: 'birthday' },
      { label: '剩余育儿假', value: 'parental_leave_left' },
      { label: '角色', value: 'roles' },
      { label: '上次登录时间', value: 'last_login' },
    ]
    const checkedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols')) || [
      'nickname',
      'username',
      'email',
      'sex',
      'mobile',
      'department_name',
      'position_name',
      'direct_supervisor_id',
      'annual_leave',
      'virtual_annual_leave',
      'parenting_leave',
      'roles',
      'last_login',
      'current_company',
      'dfc_entry_date',
      'is_internship',
      'entry_date',
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
      'name',
      'gender',
      'birthday',
      'parental_leave_left',
    ]
    return {
      filterRoleList: [],
      options,
      checkedCols,
      unsbmitCheckedCols: [],
      visible: false,
      useDFC: appConfig.useDFC,
      tableDragClassName: [], // 表格拖拽的参数
      attributes: [],
      internMap: [
        {
          id: 0,
          label: '正式',
        },
        {
          id: 1,
          label: '实习生',
        },
      ],
      internOptions: [
        { label: '正式', value: 0 },
        { label: '实习生', value: 1 },
      ],
    }
  },
  inject: ['provide_allFlatEmployees', 'provide_allFlatDepartments'],
  computed: {
    allFlatEmployees() {
      return this.provide_allFlatEmployees()
    },
    allFlatDepartments() {
      return this.provide_allFlatDepartments()
    },
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  created() {
    Bus.$on('reqExportSelectEvent', () => {
      this.exportExcel()
    })
    if (!this.useDFC) {
      this.options = this.options
        .filter((item) => item.label !== '目前所属主体')
        .filter((item) => item.label !== '初始入职日期')
    }
    this.unsbmitCheckedCols = this.checkedCols
  },
  beforeDestroy() {
    Bus.$off('reqExportSelectEvent')
  },
  mounted() {
    // 无编辑权限移除字段的缓存
    if (!this.isEditable && localStorage.getItem('setting-table-CheckedCols')) {
      localStorage.removeItem('setting-table-CheckedCols')
    }
    setTimeout(() => {
      // 获取并设置角色过滤项
      this.setRoleFilter()
      // table拖拽
      this.columnDrop()
    }, 1000)
  },
  watch: {
    tableData(newVal, oldVal) {
      newVal && this.initAttributes()
    },
  },
  methods: {
    getDepartmentName,
    getDirectorName,
    getVxetableRef() {
      return this.$refs.employeeTable
    },
    setRoleFilter() {
      // 获取并设置角色过滤项
      this.$nextTick(() => {
        if (this.tableType === 'structure') {
          getRoleList('all').then((res) => {
            const _filterRoleList = []
            Object.keys(res).forEach((key) => {
              _filterRoleList.push(
                ...res[key].role_list.map((role) => {
                  return {
                    label: role.role_name,
                    value: role.role_id,
                  }
                })
              )
            })
            this.filterRoleList = _filterRoleList
            const $table = this.$refs.employeeTable
            if ($table) {
              const nameColumn = $table.getColumnByField('role')
              if (nameColumn) {
                $table.setFilter(nameColumn, this.filterRoleList)
              }
            }
          })
        }
      })
    },
    initAttributes() {
      // 过滤用户没有权限的字段
      if (this.tableData.length) {
        const attributes = Object.keys(this.tableData[0]) // 获取用户有查看权限的所有字段
        // attributes = attributes.filter(v => v !== 'nickname')
        this.options.forEach((item) => {
          if (!attributes.includes(item.value)) {
            if (!attributes.includes('educational_experience') && !attributes.includes('children_information')) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('educational_experience') &&
              (item.value !== 'school' ||
                item.value !== 'major' ||
                item.value !== 'education' ||
                item.value !== 'graduation_year') &&
              !attributes.includes('children_information')
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('children_information') &&
              (item.value !== 'name' ||
                item.value !== 'gender' ||
                item.value !== 'birthday' ||
                item.value !== 'parental_leave_left') &&
              !attributes.includes('educational_experience')
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            } else if (
              attributes.includes('educational_experience') &&
              attributes.includes('children_information') &&
              ![
                'school',
                'major',
                'education',
                'graduation_year',
                'name',
                'gender',
                'birthday',
                'parental_leave_left',
              ].includes(item.value)
            ) {
              this.options = this.options.filter((v) => v.value !== item.value)
            }
          }
        })
        this.attributes = attributes
        localStorage.setItem('setting-table-attributes', JSON.stringify(this.attributes))
      } else {
        if (localStorage.getItem('setting-table-attributes')) {
          this.attributes = JSON.parse(localStorage.getItem('setting-table-attributes'))
        } else {
          this.attributes = []
          this.options = []
        }
      }
      Bus.$emit('getAttributes', this.attributes)
      this.$emit('tranferAttributes', this.attributes)
    },
    getIsInterInship(is_internship) {
      return this.internMap.filter((item) => item.id === is_internship)[0]['label']
    },
    sortChangeEvent(data) {
      this.$emit('sortChangeEvent', data)
    },
    filterChangeEvent(data) {
      this.$emit('filterChangeEvent', data)
    },
    onSelectChange(data) {
      this.$emit('onSelectChange', data)
    },
    openEmployeeModal(row, type) {
      this.$emit('openEmployeeModal', row, type)
    },
    openBatchModal(type, row, state) {
      this.$emit('openBatchModal', type, row, state)
    },
    removeEmployee(row) {
      const that = this
      this.$confirm({
        title: '提示',
        content: '确认移除该员工?',
        onOk() {
          that.$emit('removeEmployee', row)
        },
      })
    },
    contentMethod({ column }) {
      if (column.property === 'role') {
        return ''
      }
      return null
    },
    // table中上次登录时间如果后端返回None则显示为空
    formatDate(row) {
      if (row.cellValue === 'None') {
        return ''
      } else {
        return XEUtils.toDateString(row.cellValue, 'yyyy-MM-dd HH:mm:ss')
      }
    },
    // onChange(checkedValues) {
    //   localStorage.setItem('setting-table-CheckedCols', JSON.stringify(checkedValues))
    // },
    visibleChange(changeValue) {
      // 避免用户勾选字段时popover自动关闭
      if (!changeValue) {
        this.visible = true
      }
    },
    handleCancel() {
      if (JSON.parse(localStorage.getItem('setting-table-CheckedCols'))) {
        this.unsbmitCheckedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols'))
      } else {
        this.unsbmitCheckedCols = this.checkedCols
      }
      this.visible = false
    },
    handleSubmit() {
      this.visible = false
      // 如果用户选择了角色列，获取角色list
      if (!this.checkedCols.includes('roles') && this.unsbmitCheckedCols.includes('roles')) {
        this.setRoleFilter()
      }
      localStorage.setItem('setting-table-CheckedCols', JSON.stringify(this.unsbmitCheckedCols))
      this.$nextTick(() => {
        this.checkedCols = JSON.parse(localStorage.getItem('setting-table-CheckedCols'))
      })
    },
    // 导出excel
    exportExcel() {
      const now = new Date()
      const year = now.getFullYear() // 获取完整的年份(4位,1970-????)
      const month = now.getMonth() + 1 // 获取当前月份(0-11,0代表1月)
      const today = now.getDate() // 获取当前日(1-31)
      const hour = now.getHours() // 获取当前小时数(0-23)
      const minute = now.getMinutes() // 获取当前分钟数(0-59)
      const second = now.getSeconds() // 获取当前秒数(0-59)
      const now_time =
        year +
        this.fillZero(month) +
        this.fillZero(today) +
        this.fillZero(hour) +
        this.fillZero(minute) +
        this.fillZero(second)
      this.$refs.employeeTable.exportData({
        data: this.$refs.employeeTable.getCheckboxRecords().map((item) => {
          return {
            ...item,
            is_internship: item.is_internship ? '实习生' : '正式',
            direct_supervisor_id: getDirectorName(this.allFlatEmployees, item.direct_supervisor_id),
            roles: this.getRoleName(item.roles)
          }
        }),
        filename: 'employee-' + now_time,
        sheetName: 'Sheet1',
        type: 'xlsx',
        types: ['xlsx', 'csv', 'html', 'xml', 'txt'],
        useStyle: true, // 是否导出样式
        isFooter: false, // 是否导出表尾（比如合计）
        // 过滤那个字段导出
        columnFilterMethod: function(column, $columnIndex) {
          return !(column.$columnIndex === 0)
          // 0是复选框 不导出
        },
      })
      this.$refs.employeeTable.clearCheckboxRow()
      this.$refs.employeeTable.clearCheckboxReserve()
      this.$refs.employeeTable.clearSort()
      this.tableSortData = undefined
      Bus.$emit('changeSelectedRowKeys', [])
    },
    fillZero(str) {
      let realNum
      if (str < 10) {
        realNum = '0' + str
      } else {
        realNum = str
      }
      return realNum
    },
    getRoleName(roles) {
      let roles_str = ''
      roles.forEach(role => {
        roles_str += `${role.role_name}` + '，'
      })
      roles_str = roles_str.substring(0, roles_str.length - 1)
      return roles_str
    },
    columnDrop() {
      this.$nextTick(() => {
        if (this.$refs.employeeTable) {
          const xTable = this.$refs.employeeTable
          this.sortable = Sortable.create(
            xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row'),
            {
              handle: '.vxe-handle',
              onChoose: () => {
                const header = xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row')
                const classNameList = []
                header.childNodes.forEach((item) => {
                  classNameList.push(item.classList[1])
                })
                this.tableDragClassName = classNameList
              },
              onEnd: (params) => {
                // 由于开启了虚拟滚动，newIndex和oldIndex是虚拟的
                const { newIndex, oldIndex, from, to } = params
                // 从tableDragClassName拿到colid
                const fromColid = this.tableDragClassName[oldIndex]
                const toColid = this.tableDragClassName[newIndex]
                const fromColumn = xTable.getColumnById(fromColid)
                const toColumn = xTable.getColumnById(toColid)
                const fromIndex = xTable.getColumnIndex(fromColumn)
                const toIndex = xTable.getColumnIndex(toColumn)
                const tableColumn = xTable.getColumns()
                const currRow = tableColumn.splice(fromIndex, 1)[0]
                tableColumn.splice(toIndex, 0, currRow)
                xTable.reloadColumn(tableColumn)
              },
            }
          )
        }
      })
    },
  },
}
</script>
<style lang="less" scoped>
.vxe-handle {
  cursor: move;
  .move-icon {
    display: none;
    width: 17px;
    height: 17px;
    display: none;
    position: absolute;
    left: -3px;
    top: 12px;
  }
  &:hover > .move-icon {
    display: inline !important;
  }
}
</style>
