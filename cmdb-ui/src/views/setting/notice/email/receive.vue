<template>
  <div class="notice-email-wrapper" :style="{ height: `${windowHeight - 104}px` }">
    <a-form-model :model="settingData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>基础设置</SpanTitle>
      <a-form-model-item label="连接协议">
        <a-radio-group v-model="settingData.connectProtocol" :default-value="1" @change="changeConnectProtocol">
          <a-radio :value="1" :default-checked="true"> POP/IMAP/POPS/IMAPS </a-radio>
          <a-radio :value="2"> EWS(Exchange Web服务) </a-radio>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item label="认证类型">
        <a-select v-model="settingData.authentication">
          <a-select-option value="Base"> 基本 </a-select-option>
          <a-select-option value="OAuth"> OAuth </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="服务器名/IP地址" prop="IP">
        <a-input v-model="settingData.IP" />
      </a-form-model-item>
      <a-form-model-item label="用户名">
        <a-input v-model="settingData.username" />
      </a-form-model-item>
      <a-form-model-item label="密码">
        <a-input v-model="settingData.password" />
      </a-form-model-item>
      <a-form-model-item label="邮件地址">
        <a-input v-model="settingData.email" />
      </a-form-model-item>
      <template v-if="settingData.connectProtocol === 1">
        <a-form-model-item label="邮件类型">
          <a-select v-model="settingData.emailType">
            <a-select-option value="POP"> POP </a-select-option>
            <a-select-option value="IMAP"> IMAP </a-select-option>
            <a-select-option value="POPS"> POPS </a-select-option>
            <a-select-option value="IMAPS"> IMAPS </a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="端口">
          <a-input v-model="settingData.port" />
        </a-form-model-item>
      </template>
      <a-form-model-item label="测试邮件设置">
        <a-button type="primary" ghost>测试回收箱</a-button>
        <br />
        <span class="notice-email-error-tips">
          <ops-icon type="icon-shidi-quxiao" :style="{ color: '#D81E06' }" />
          邮件接收失败
        </span>
        <br />
        <span
        >邮箱服务器未配置，请配置一个邮箱服务器 <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a>故障诊断</a></span
        >
      </a-form-model-item>
      <SpanTitle>邮件设置</SpanTitle>
      <a-form-model-item label="获取邮件间隔" :wrapperCol="{ span: 4 }">
        <a-input class="ant-input-after" v-model="settingData.getEmailTimeout" />
        <span :style="{ position: 'absolute', marginLeft: '8px' }">分</span>
      </a-form-model-item>
      <a-row>
        <a-col :span="16" :offset="3">
          <a-checkbox :default-checked="false" disabled>启动代理服务器</a-checkbox>
          <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px' }" />
          <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a @click="configProxySetting">配置代理设置</a>
          <br />
          <a-checkbox :default-checked="false">启动邮件测试</a-checkbox>
          <br /><br />
          <a-checkbox :default-checked="false" @change="changeCreateReqByEmail">禁用通过邮件创建请求</a-checkbox>
          <br />
          <template v-if="settingData.banReqByEmail">
            <strong>指定允许的邮件/域名,逗号分隔多个值</strong>
            <a-input type="textarea" :style="{ borderRadius: '8px', borderColor: '#2F54EB' }" />
            <p :style="{ fontSize: '12px' }">例如:user@domain.com,*@domain.com</p>
            <p :style="{ fontSize: '12px' }">限制不能适用于已在会话中的请求,它将聚集到它的上级工单中</p>
          </template>
        </a-col>
      </a-row>
      <SpanTitle>消息设置</SpanTitle>
      <a-row>
        <a-col :span="16" :offset="3">
          <a-checkbox :default-checked="false">将消息移动到错误的文件夹</a-checkbox>
          <a-icon type="info-circle" :style="{ color: '#FF9E58', fontSize: '16px' }" />
          <a-divider type="vertical" :style="{ backgroundColor: '#2F54EB' }" />
          <a href="#">了解更多</a>
        </a-col>
      </a-row>
      <br /><br />
      <a-row>
        <a-col :span="16" :offset="3">
          <a-form-model-item :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-button type="primary" @click="onSubmit"> 保存 </a-button>
            <a-button ghost type="primary" style="margin-left: 28px;" @click="resetForm"> 重置 </a-button>
          </a-form-model-item>
        </a-col>
      </a-row>
    </a-form-model>
    <a-modal dialogClass="ops-modal" width="500px" v-model="visible" title="配置代理设置">
      <a-form-model v-model="proxySetting" :label-col="{ span: 4 }" :wrapper-col="{ span: 19 }">
        <a-form-model-item label="主机">
          <a-input v-model="proxySetting.host" />
        </a-form-model-item>
        <a-form-model-item label="端口">
          <a-input v-model="proxySetting.port" />
        </a-form-model-item>
        <a-form-model-item label="用户名">
          <a-input v-model="proxySetting.username" />
        </a-form-model-item>
        <a-form-model-item label="密码">
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
