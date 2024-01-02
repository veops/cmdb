<template>
  <div class="notice-email-wrapper" :style="{ height: `${windowHeight - 104}px` }">
    <a-form-model ref="sendForm" :model="settingData" :label-col="labelCol" :rules="rules" :wrapper-col="wrapperCol">
      <SpanTitle>{{ $t('cs.duty.basicSetting') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.notice.isEncrypted')">
        <a-radio-group v-model="settingData.tls" :disabled="!isEditable">
          <a-radio :value="true">
            {{ $t('yes') }}
          </a-radio>
          <a-radio :value="false">
            {{ $t('no') }}
          </a-radio>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.port')" prop="port">
        <a-input v-model="settingData.port" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.host')" prop="host">
        <a-input v-model="settingData.host" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.username')" prop="account">
        <a-input v-model="settingData.account" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.password')" prop="password">
        <a-input-password v-model="settingData.password" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>{{ $t('cs.notice.emailTest') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.notice.testSendAddress')" prop="receive_address">
        <a-input v-model="settingData.receive_address" :disabled="!isEditable">
          <span
            v-if="isEditable"
            :style="{ cursor: 'pointer' }"
            @click="testSendEmail"
            slot="addonAfter"
          >{{ $t('cs.notice.testMailSend') }}</span
          >
        </a-input>
      </a-form-model-item>
      <a-row v-if="isEditable">
        <a-col :span="16" :offset="3">
          <a-form-model-item :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-button type="primary" @click="onSubmit"> {{ $t('save') }} </a-button>
            <a-button ghost type="primary" style="margin-left: 28px;" @click="resetForm"> {{ $t('reset') }} </a-button>
          </a-form-model-item>
        </a-col>
      </a-row>
    </a-form-model>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SpanTitle from '../../components/spanTitle.vue'
import {
  getNoticeConfigByPlatform,
  postNoticeConfigByPlatform,
  putNoticeConfigByPlatform,
  sendTestEmail,
} from '@/api/noticeSetting'
import { mixinPermissions } from '@/utils/mixin'
export default {
  name: 'Send',
  mixins: [mixinPermissions],
  components: { SpanTitle },
  data() {
    return {
      labelCol: { lg: 3, md: 5, sm: 8 },
      wrapperCol: { lg: 10, md: 12, sm: 12 },
      id: null,
      settingData: {
        tls: true,
        host: '',
        account: '',
        password: '',
        port: '',
        receive_address: '',
      }
    }
  },
  computed: {
    ...mapState({
      rules() {
        return {
          port: [{ required: true, message: this.$t('cs.notice.portPlaceholder'), trigger: 'blur' }],
        host: [{ required: true, whitespace: true, message: this.$t('cs.auth.ldap.serverAddressPlaceholder'), trigger: 'blur' }],
        account: [
          { required: true, whitespace: true, message: this.$t('cs.auth.ldap.userPlaceholder'), trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: this.$t('cs.companyStructure.emailFormatErr'),
            trigger: 'blur',
          },
        ],
        password: [{ required: false, whitespace: true, message: this.$t('cs.companyStructure.passwordPlaceholder'), trigger: 'blur' }],
        receive_address: [
          { required: false, whitespace: true, message: this.$t('cs.notice.testSendAddressPlaceholder'), trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: this.$t('cs.companyStructure.emailFormatErr'),
            trigger: 'blur',
          },
        ]
        }
      },
      windowHeight: (state) => state.windowHeight,
    }),
    isEditable() {
      return this.hasDetailPermission('backend', '通知设置', ['update'])
    },
  },
  watch: {
    'settingData.tls': {
      handler(newV, oldV) {
        if (newV === false) {
          this.settingData.port = 25
        }
        if (newV === true) {
          this.settingData.port = 465
        }
      },
      immediate: true,
    },
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      getNoticeConfigByPlatform({ platform: 'email' }).then((res) => {
        this.id = res?.id ?? null
        if (this.id) {
          this.settingData = res.info
        }
      })
    },
    async testSendEmail() {
      await sendTestEmail(this.settingData.receive_address, {
        info: { ...this.settingData, receive_address: undefined },
      })
      this.$message.success(this.$t('cs.notice.emailSendSuccess'))
    },
    onSubmit() {
      this.$refs.sendForm.validate(async (valid) => {
        if (valid) {
          if (this.id) {
            await putNoticeConfigByPlatform(this.id, { info: { ...this.settingData, label: this.$t('cs.companyInfo.email') } })
          } else {
            await postNoticeConfigByPlatform({ platform: 'email', info: { ...this.settingData, label: this.$t('cs.companyInfo.email') } })
          }
          this.$message.success(this.$t('saveSuccess'))
          this.getData()
        }
      })
    },
    resetForm() {
      this.settingData = {
        tls: true,
        host: '',
        account: '',
        password: '',
        port: 25,
        receive_address: '',
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import './index.less';
</style>
