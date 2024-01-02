<template>
  <div class="setting-person">
    <div class="setting-person-left">
      <div
        @click="
          () => {
            $refs.personForm.clearValidate()
            $nextTick(() => {
              current = '1'
            })
          }
        "
        :class="{ 'setting-person-left-item': true, 'setting-person-left-item-selected': current === '1' }"
      >
        <ops-icon type="icon-shidi-yonghu" />{{ $t('cs.person.spanTitle') }}
      </div>
      <div
        @click="
          () => {
            $refs.personForm.clearValidate()
            $nextTick(() => {
              current = '2'
            })
          }
        "
        :class="{ 'setting-person-left-item': true, 'setting-person-left-item-selected': current === '2' }"
      >
        <a-icon type="unlock" theme="filled" />{{ $t('cs.person.accountAndPassword') }}
      </div>
    </div>
    <div class="setting-person-right">
      <a-form-model
        ref="personForm"
        :model="form"
        :rules="current === '1' ? rules1 : rules2"
        :colon="false"
        labelAlign="left"
        :labelCol="{ span: 4 }"
        :wrapperCol="{ span: 10 }"
      >
        <div v-show="current === '1'">
          <a-form-model-item :label="$t('cs.person.avatar')" :style="{ display: 'flex', alignItems: 'center' }">
            <a-space>
              <a-avatar v-if="form.avatar" :src="`/api/common-setting/v1/file/${form.avatar}`" :size="64"> </a-avatar>
              <a-avatar v-else style="backgroundColor:#F0F5FF" :size="64">
                <ops-icon type="icon-shidi-yonghu" :style="{ color: '#2F54EB' }" />
              </a-avatar>
              <a-upload
                name="avatar"
                :show-upload-list="false"
                :customRequest="customRequest"
                :before-upload="beforeUpload"
                :style="{ width: '310px', height: '100px' }"
                accept=".svg,.png,.jpg,.jpeg"
              >
                <a-button type="primary" ghost size="small">{{ $t('cs.person.changeAvatar') }}</a-button>
              </a-upload>
            </a-space>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.nickname')" prop="nickname">
            <a-input v-model="form.nickname" />
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.username')">
            <div class="setting-person-right-disabled">{{ form.username }}</div>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.email')">
            <div class="setting-person-right-disabled">{{ form.email }}</div>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.supervisor')">
            <div class="setting-person-right-disabled">
              {{ getDirectorName(allFlatEmployees, form.direct_supervisor_id) }}
            </div>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.sex')">
            <a-select v-model="form.sex">
              <a-select-option value="男">{{ $t('cs.companyStructure.male') }}</a-select-option>
              <a-select-option value="女">{{ $t('cs.companyStructure.female') }}</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.mobile')" prop="mobile">
            <a-input v-model="form.mobile" />
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.departmentName')">
            <div class="setting-person-right-disabled">
              {{ getDepartmentName(allFlatDepartments, form.department_id) }}
            </div>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.companyStructure.positionName')">
            <div class="setting-person-right-disabled">{{ form.position_name }}</div>
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.person.bindInfo')">
            <a-space>
              <a-tooltip :title="$t('cs.person.wechatApp')">
                <div
                  @click="handleBind('wechatApp', form.notice_info && form.notice_info.wechatApp)"
                  :class="{
                    'setting-person-bind': true,
                    'setting-person-bind-existed': form.notice_info && form.notice_info.wechatApp,
                  }"
                >
                  <ops-icon type="ops-setting-notice-wx" />
                </div>
              </a-tooltip>
              <a-tooltip :title="$t('cs.person.feishuApp')">
                <div
                  @click="handleBind('feishuApp', form.notice_info && form.notice_info.feishuApp)"
                  :class="{
                    'setting-person-bind': true,
                    'setting-person-bind-existed': form.notice_info && form.notice_info.feishuApp,
                  }"
                >
                  <ops-icon type="ops-setting-notice-feishu" />
                </div>
              </a-tooltip>
              <a-tooltip :title="$t('cs.person.dingdingApp')">
                <div
                  @click="handleBind('dingdingApp', form.notice_info && form.notice_info.dingdingApp)"
                  :class="{
                    'setting-person-bind': true,
                    'setting-person-bind-existed': form.notice_info && form.notice_info.dingdingApp,
                  }"
                >
                  <ops-icon type="ops-setting-notice-dingding" />
                </div>
              </a-tooltip>
            </a-space>
          </a-form-model-item>
        </div>
        <div v-show="current === '2'">
          <a-form-model-item :label="$t('cs.person.newPassword')" prop="password1">
            <a-input v-model="form.password1" />
          </a-form-model-item>
          <a-form-model-item :label="$t('cs.person.confirmPassword')" prop="password2">
            <a-input v-model="form.password2" />
          </a-form-model-item>
        </div>
        <div style="margin-right: 120px">
          <a-form-model-item label=" ">
            <a-button type="primary" @click="handleSave" :style="{ width: '100%' }">{{ $t('save') }}</a-button>
          </a-form-model-item>
        </div>
      </a-form-model>
    </div>
    <EditImage
      v-if="showEditImage"
      :show="showEditImage"
      :image="editImage"
      :title="eidtImageOption.title"
      :preview-width="eidtImageOption.previewWidth"
      :preview-height="eidtImageOption.previewHeight"
      preview-radius="0"
      width="550px"
      :save-button-title="$t('confirm')"
      @save="submitImage"
      @close="showEditImage = false"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { getAllDepartmentList } from '@/api/company'
import { postImageFile } from '@/api/file'
import {
  getEmployeeList,
  getEmployeeByUid,
  updateEmployeeByUid,
  updatePasswordByUid,
  bindPlatformByUid,
  unbindPlatformByUid,
} from '@/api/employee'
import { getDepartmentName, getDirectorName } from '@/utils/util'
import EditImage from '../components/EditImage.vue'
export default {
  name: 'Person',
  components: { EditImage },
  data() {
    return {
      current: '1',
      form: {},
      allFlatEmployees: [],
      allFlatDepartments: [],
      showEditImage: false,
      editImage: null,
    }
  },
  computed: {
    ...mapGetters(['uid']),
    rules1() {
      return {
        nickname: [
          {
            required: true,
            whitespace: true,
            message: this.$t('cs.companyStructure.nicknamePlaceholder'),
            trigger: 'blur',
          },
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
    },
    rules2() {
      const validatePassword = (rule, value, callback) => {
        if (!value) {
          callback(new Error(this.$t('cs.person.pleaseConfirmNewPasswordSecondTime')))
        }
        if (value !== this.form.password1) {
          callback(new Error(this.$t('cs.person.thePasswordEnteredTwiceIsInconsistent')))
        }
        callback()
      }
      return {
        password1: [
          { required: true, message: this.$t('cs.person.pleaseConfirmNewPasswordSecondTime'), trigger: 'blur' },
        ],
        password2: [
          {
            required: true,
            message: this.$t('cs.person.thePasswordEnteredTwiceIsInconsistent'),
            trigger: 'blur',
            validator: validatePassword,
          },
        ],
      }
    },
    eidtImageOption() {
      return {
        type: 'avatar',
        fixedNumber: [4, 4],
        title: this.$t('cs.components.editAvatar'),
        previewWidth: '60px',
        previewHeight: '60px',
      }
    },
  },
  mounted() {
    this.getAllFlatEmployees()
    this.getAllFlatDepartment()
    this.getEmployeeByUid()
  },
  methods: {
    ...mapActions(['GetInfo']),
    getDepartmentName,
    getDirectorName,
    getEmployeeByUid() {
      getEmployeeByUid(this.uid).then((res) => {
        this.form = { ...res }
      })
    },
    getAllFlatEmployees() {
      getEmployeeList({ block_status: 0, page_size: 99999 }).then((res) => {
        this.allFlatEmployees = res.data_list
      })
    },
    getAllFlatDepartment() {
      getAllDepartmentList({ is_tree: 0 }).then((res) => {
        this.allFlatDepartments = res
      })
    },
    async handleSave() {
      await this.$refs.personForm.validate(async (valid) => {
        if (valid) {
          const { nickname, mobile, sex, avatar, password1 } = this.form
          const params = { nickname, mobile, sex, avatar }
          if (this.current === '1') {
            await updateEmployeeByUid(this.uid, params).then((res) => {
              this.$message.success(this.$t('saveSuccess'))
              this.getEmployeeByUid()
              this.GetInfo()
            })
          } else {
            await updatePasswordByUid(this.uid, { password: password1 }).then((res) => {
              this.$message.success(this.$t('saveSuccess'))
            })
          }
        }
      })
    },
    customRequest(file) {
      const reader = new FileReader()
      var self = this
      reader.onload = function(e) {
        let result
        if (typeof e.target.result === 'object') {
          // 把Array Buffer转化为blob 如果是base64不需要
          result = window.URL.createObjectURL(new Blob([e.target.result]))
        } else {
          result = e.target.result
        }

        self.editImage = result
        self.showEditImage = true
      }
      reader.readAsDataURL(file.file)
    },
    beforeUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error(this.$t('cs.companyInfo.imageSizeLimit2MB'))
      }
      return isLt2M
    },
    submitImage(file) {
      postImageFile(file).then((res) => {
        if (res.file_name) {
          this.form.avatar = res.file_name
        }
      })
    },
    async handleBind(platform, isBind) {
      if (isBind) {
        const that = this
        this.$confirm({
          title: this.$t('warning'),
          content: this.$t('cs.person.confirmUnbind'),
          onOk() {
            unbindPlatformByUid(platform, that.uid)
              .then(() => {
                that.$message.success(this.$t('cs.person.unbindSuccess'))
              })
              .finally(() => {
                that.getEmployeeByUid()
                that.GetInfo()
              })
          },
        })
      } else {
        await this.$refs.personForm.validate(async (valid) => {
          if (valid) {
            const { nickname, mobile, sex, avatar } = this.form
            const params = { nickname, mobile, sex, avatar }
            await updateEmployeeByUid(this.uid, params)
            bindPlatformByUid(platform, this.uid)
              .then(() => {
                this.$message.success(this.$t('cs.person.bindSuccess'))
              })
              .finally(() => {
                this.getEmployeeByUid()
                this.GetInfo()
              })
          }
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.setting-person {
  display: flex;
  flex-direction: row;
  .setting-person-left {
    width: 200px;
    height: 400px;
    margin-right: 24px;
    background-color: #fff;
    border-radius: 15px;
    padding-top: 15px;
    .setting-person-left-item {
      cursor: pointer;
      padding: 10px 20px;
      color: #a5a9bc;
      border-left: 4px solid #fff;
      margin-bottom: 5px;
      &:hover {
        .ops_popover_item_selected();
        border-color: #custom_colors[color_1];
      }
      > i {
        margin-right: 10px;
      }
    }
    .setting-person-left-item-selected {
      .ops_popover_item_selected();
      border-color: #custom_colors[color_1];
    }
  }
  .setting-person-right {
    width: 800px;
    height: 700px;
    background-color: #fff;
    border-radius: 15px;
    padding: 24px 48px;
    .setting-person-right-disabled {
      background-color: #custom_colors[color_2];
      border-radius: 4px;
      height: 30px;
      line-height: 30px;
      margin-top: 4px;
      padding: 0 10px;
      color: #a5a9bc;
    }
    .setting-person-bind {
      width: 40px;
      height: 40px;
      background: #a5a9bc;
      border-radius: 4px;
      color: #fff;
      font-size: 30px;
      text-align: center;
      cursor: pointer;
    }
    .setting-person-bind-existed {
      background: #008cee;
    }
  }
}
</style>
<style lang="less">
.setting-person-right .ant-form-item {
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
