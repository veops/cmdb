<template>
  <div class="notice-email-wrapper" :style="{ height: `${windowHeight - 104}px` }">
    <a-form-model ref="sendForm" :model="settingData" :label-col="labelCol" :rules="rules" :wrapper-col="wrapperCol">
      <SpanTitle>基础设置</SpanTitle>
      <a-form-model-item label="是否加密">
        <a-radio-group v-model="settingData.tls" :disabled="!isEditable">
          <a-radio :value="true">
            是
          </a-radio>
          <a-radio :value="false">
            否
          </a-radio>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item label="端口" prop="port">
        <a-input v-model="settingData.port" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="邮件服务器" prop="host">
        <a-input v-model="settingData.host" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="用户名" prop="account">
        <a-input v-model="settingData.account" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="密码" prop="password">
        <a-input-password v-model="settingData.password" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>邮件测试</SpanTitle>
      <a-form-model-item label="测试发送邮件地址" prop="receive_address">
        <a-input v-model="settingData.receive_address" :disabled="!isEditable">
          <span
            v-if="isEditable"
            :style="{ cursor: 'pointer' }"
            @click="testSendEmail"
            slot="addonAfter"
          >测试邮件发送</span
          >
        </a-input>
      </a-form-model-item>
      <a-row v-if="isEditable">
        <a-col :span="16" :offset="3">
          <a-form-model-item :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-button type="primary" @click="onSubmit"> 保存 </a-button>
            <a-button ghost type="primary" style="margin-left: 28px;" @click="resetForm"> 重置 </a-button>
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
      },
      rules: {
        port: [{ required: true, message: '请输入端口', trigger: 'blur' }],
        host: [{ required: true, whitespace: true, message: '请输入服务器', trigger: 'blur' }],
        account: [
          { required: true, whitespace: true, message: '请输入用户名', trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: '邮箱格式错误',
            trigger: 'blur',
          },
        ],
        password: [{ required: false, whitespace: true, message: '请输入密码', trigger: 'blur' }],
        receive_address: [
          { required: false, whitespace: true, message: '请输入测试发送邮件地址', trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/,
            message: '邮箱格式错误',
            trigger: 'blur',
          },
        ],
      },
    }
  },
  computed: {
    ...mapState({
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
      this.$message.success('已发送邮件，请查收')
    },
    onSubmit() {
      this.$refs.sendForm.validate(async (valid) => {
        if (valid) {
          if (this.id) {
            await putNoticeConfigByPlatform(this.id, { info: { ...this.settingData, label: '邮箱' } })
          } else {
            await postNoticeConfigByPlatform({ platform: 'email', info: { ...this.settingData, label: '邮箱' } })
          }
          this.$message.success('保存成功')
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
