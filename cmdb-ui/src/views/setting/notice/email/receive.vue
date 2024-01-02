<template>
  <div class="notice-email-wrapper" :style="{ height: `${windowHeight - 104}px` }">
    <a-form-model :model="settingData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>{{ $t('cs.duty.basicSetting') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.notice.connectProtocol')">
        <a-radio-group v-model="settingData.connectProtocol" :default-value="1" @change="changeConnectProtocol">
          <a-radio :value="1" :default-checked="true"> POP/IMAP/POPS/IMAPS </a-radio>
          <a-radio :value="2">{{ $t('cs.notice.ews') }}</a-radio>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.authType')">
        <a-select v-model="settingData.authentication">
          <a-select-option value="Base"> {{ $t('cs.notice.base') }} </a-select-option>
          <a-select-option value="OAuth"> {{ $t('cs.notice.oauth') }} </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.ip')" prop="IP">
        <a-input v-model="settingData.IP" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.username')">
        <a-input v-model="settingData.username" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.password')">
        <a-input v-model="settingData.password" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.email')">
        <a-input v-model="settingData.email" />
      </a-form-model-item>
      <template v-if="settingData.connectProtocol === 1">
        <a-form-model-item :label="$t('cs.notice.emailType')">
          <a-select v-model="settingData.emailType">
            <a-select-option value="POP"> POP </a-select-option>
            <a-select-option value="IMAP"> IMAP </a-select-option>
            <a-select-option value="POPS"> POPS </a-select-option>
            <a-select-option value="IMAPS"> IMAPS </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item :label="$t('cs.notice.port')">
          <a-input v-model="settingData.port" />
        </a-form-model-item>
      </template>
      <a-form-model-item :label="$t('cs.notice.oauth')">
        <a-button type="primary" ghost>{{ $t('cs.notice.testRecyclingBin') }}</a-button>
        <br />
        <span class="notice-email-error-tips">
          <ops-icon type="icon-shidi-quxiao" :style="{ color: '#D81E06' }" />
          {{ $t('cs.notice.receiveEmailFailed') }}
        </span>
        <br />
        <span
        >{{ $('cs.notice.emailServiceNotConfig') }} <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a>{{ $('cs.notice.troubleshooting') }}</a></span
        >
      </a-form-model-item>
      <SpanTitle>{{ $('cs.notice.emailConfig') }}</SpanTitle>
      <a-form-model-item :label="$('cs.notice.receiveEmailInterval')" :wrapperCol="{ span: 4 }">
        <a-input class="ant-input-after" v-model="settingData.getEmailTimeout" />
        <span :style="{ position: 'absolute', marginLeft: '8px' }">{{ $t('cs.duty.min') }}</span>
      </a-form-model-item>
      <a-row>
        <a-col :span="16" :offset="3">
          <a-checkbox :default-checked="false" disabled>{{ $('cs.notice.startProxyServer') }}</a-checkbox>
          <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px' }" />
          <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a @click="configProxySetting">{{ $('cs.notice.configProxyServer') }}</a>
          <br />
          <a-checkbox :default-checked="false">{{ $('cs.notice.startEmailTest') }}</a-checkbox>
          <br /><br />
          <a-checkbox :default-checked="false" @change="changeCreateReqByEmail">{{ $('cs.notice.disableCreationOfRequestsViaEmail') }}</a-checkbox>
          <br />
          <template v-if="settingData.banReqByEmail">
            <strong>{{ $('cs.notice.specifyAllowedEmails') }}</strong>
            <a-input type="textarea" :style="{ borderRadius: '8px', borderColor: '#2F54EB' }" />
            <p :style="{ fontSize: '12px' }">{{ $('cs.notice.specifyAllowedEmailsExample') }}</p>
            <p :style="{ fontSize: '12px' }">{{ $('cs.notice.specifyAllowedEmailsLimit') }}</p>
          </template>
        </a-col>
      </a-row>
      <SpanTitle>{{ $('cs.notice.messageConfig') }}</SpanTitle>
      <a-row>
        <a-col :span="16" :offset="3">
          <a-checkbox :default-checked="false">{{ $('cs.notice.moveWrongMessagesToFolder') }}</a-checkbox>
          <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px' }" />
          <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a href="#">{{ $('cs.notice.knowMore') }}</a>
        </a-col>
      </a-row>
      <br /><br />
      <a-row>
        <a-col :span="16" :offset="3">
          <a-form-model-item :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-button type="primary" @click="onSubmit"> {{ $('save') }} </a-button>
            <a-button ghost type="primary" style="margin-left: 28px;" @click="resetForm"> {{ $('reset') }}  </a-button>
          </a-form-model-item>
        </a-col>
      </a-row>
    </a-form-model>
    <a-modal dialogClass="ops-modal" width="500px" v-model="visible" :title="$('cs.notice.configProxySettings')">
      <a-form-model v-model="proxySetting" :label-col="{ span: 4 }" :wrapper-col="{ span: 19 }">
        <a-form-model-item :label="$('cs.notice.host')">
          <a-input v-model="proxySetting.host" />
        </a-form-model-item>
        <a-form-model-item :label="$('cs.notice.port')">
          <a-input v-model="proxySetting.port" />
        </a-form-model-item>
        <a-form-model-item :label="$('cs.notice.username')">
          <a-input v-model="proxySetting.username" />
        </a-form-model-item>
        <a-form-model-item :label="$('cs.notice.password')">
          <a-input v-model="proxySetting.password" />
        </a-form-model-item>
      </a-form-model>
    </a-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import SpanTitle from '../../components/spanTitle.vue'
export default {
  name: 'Receive',
  components: { SpanTitle },
  data() {
    return {
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      settingData: {
        connectProtocol: 1,
        authentication: 'Base',
        IP: '',
        username: '',
        password: '',
        email: '',
        emailType: '',
        port: '',

        getEmailTimeout: '',
        activeProxy: false,
        activeEmailDebug: false,
        banReqByEmail: false,

        transfromMessage: false,
      },
      visible: false,
      proxySetting: {
        host: '',
        post: '',
        username: '',
        password: '',
      },
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  methods: {
    changeConnectProtocol(e) {
      console.log(e.target.value)
    },
    changeCreateReqByEmail(e) {
      this.settingData.banReqByEmail = e.target.checked
    },
    configProxySetting() {
      this.visible = true
    },
    onSubmit() {
      console.log(this.settingData)
    },
    resetForm() {
      this.settingData = {
        connectProtocol: 1,
        authentication: '',
        IP: '',
        username: '',
        password: '',
        email: '',
        emailType: '',
        port: '',

        getEmailTimeout: '',
        activeProxy: false,
        activeEmailDebug: false,
        banReqByEmail: false,

        transfromMessage: false,
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import './index.less';
</style>
