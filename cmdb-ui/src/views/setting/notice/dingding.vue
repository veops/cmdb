<template>
  <div class="notice-dingding-wrapper" :style="{ height: `${windowHeight - 64}px` }">
    <a-form-model ref="dingdingForm" :model="dingdingData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>{{ $t('cs.duty.basicSetting') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.notice.appKey')">
        <a-input v-model="dingdingData.appKey" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.appSecret')">
        <a-input v-model="dingdingData.appSecret" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.robotCode')">
        <a-input v-model="dingdingData.robotCode" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.robot')">
        <Bot
          ref="bot"
          :disabled="!isEditable"
          :columns="[
            {
              field: 'name',
              title: $t('cs.notice.title'),
              required: true,
            },
            {
              field: 'url',
              title: $t('cs.notice.webhookAddress'),
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
      <!-- <a-form-model-item :label="测试邮件设置">
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
                await putNoticeConfigByPlatform(this.id, { info: { ...this.dingdingData, bot, label: this.$t('cs.person.dingdingApp') } })
              } else {
                await postNoticeConfigByPlatform({
                  platform: 'dingdingApp',
                  info: { ...this.dingdingData, bot, label: this.$t('cs.person.dingdingApp') },
                })
              }
              this.$message.success(this.$t('saveSuccess'))
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
  border-radius: @border-radius-box;
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
