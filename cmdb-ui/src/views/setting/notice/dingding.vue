<template>
  <div class="notice-dingding-wrapper" :style="{ height: `${windowHeight - 64}px` }">
    <a-form-model ref="dingdingForm" :model="dingdingData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>基础设置</SpanTitle>
      <a-form-model-item label="应用Key">
        <a-input v-model="dingdingData.appKey" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="应用密码">
        <a-input v-model="dingdingData.appSecret" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="机器人码">
        <a-input v-model="dingdingData.robotCode" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="机器人">
        <Bot
          ref="bot"
          :disabled="!isEditable"
          :columns="[
            {
              field: 'name',
              title: '名称',
              required: true,
            },
            {
              field: 'url',
              title: 'Webhook地址',
              required: true,
            },
            {
              field: 'token',
              title: 'token',
              required: false,
            },
          ]"
        />
      </a-form-model-item>
      <!-- <a-form-model-item label="测试邮件设置">
        <a-button type="primary" ghost>测试回收箱</a-button>
        <br />
        <span
          class="notice-dingding-wrapper-tips"
        ><ops-icon type="icon-shidi-quxiao" :style="{ color: '#D81E06' }" /> 邮件接收失败</span
        >
        <br />
        <span>邮箱服务器未配置，请配置一个邮箱服务器 | <a>故障诊断</a></span>
      </a-form-model-item> -->
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
import SpanTitle from '../components/spanTitle.vue'
import { getNoticeConfigByPlatform, postNoticeConfigByPlatform, putNoticeConfigByPlatform } from '@/api/noticeSetting'
import { mixinPermissions } from '@/utils/mixin'
import Bot from './bot.vue'

export default {
  name: 'NoticeDingding',
  components: { SpanTitle, Bot },
  mixins: [mixinPermissions],
  data() {
    return {
      labelCol: { lg: 3, md: 5, sm: 8 },
      wrapperCol: { lg: 15, md: 19, sm: 16 },
      id: null,
      dingdingData: {
        appKey: '',
        appSecret: '',
        robotCode: '',
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
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      getNoticeConfigByPlatform({ platform: 'dingdingApp' }).then((res) => {
        this.id = res?.id ?? null
        if (this.id) {
          this.dingdingData = res.info
          this.$refs.bot.setData(res?.info?.bot)
        }
      })
    },
    onSubmit() {
      this.$refs.dingdingForm.validate(async (valid) => {
        if (valid) {
          this.$refs.bot.getData(async (flag, bot) => {
            if (flag) {
              if (this.id) {
                await putNoticeConfigByPlatform(this.id, { info: { ...this.dingdingData, bot, label: '钉钉' } })
              } else {
                await postNoticeConfigByPlatform({
                  platform: 'dingdingApp',
                  info: { ...this.dingdingData, bot, label: '钉钉' },
                })
              }
              this.$message.success('保存成功')
              this.getData()
            }
          })
        }
      })
    },
    resetForm() {
      this.dingdingData = {
        appKey: '',
        appSecret: '',
        robotCode: '',
      }
    },
  },
}
</script>

<style lang="less" scoped>
.notice-dingding-wrapper {
  background-color: #fff;
  padding-top: 15px;
  overflow: auto;
  margin-bottom: -24px;
  border-radius: 15px;
  .notice-dingding-wrapper-tips {
    display: inline-block;
    background-color: #ffdfdf;
    border-radius: 4px;
    padding: 0 12px;
    width: 300px;
    color: #000000;
    margin-top: 8px;
  }
}
</style>
