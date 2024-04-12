<template>
  <div class="notice-feishu-wrapper" :style="{ height: `${windowHeight - 64}px` }">
    <a-form-model ref="feishuForm" :model="feishuData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>{{ $t('cs.duty.basicSetting') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.notice.appKey')">
        <a-input v-model="feishuData.id" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.notice.appSecret')">
        <a-input v-model="feishuData.password" :disabled="!isEditable" />
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
          ]"
        />
      </a-form-model-item>
      <a-row v-if="isEditable">
        <a-col :span="16" :offset="3">
          <a-form-model-item :label-col="labelCol" :wrapper-col="wrapperCol">
            <a-button type="primary" @click="onSubmit"> {{ $t('save') }} </a-button>
            <a-button ghost type="primary" style="margin-left: 28px;" @click="resetForm"> {{ $t('reset') }}  </a-button>
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
  name: 'NoticeFeishu',
  components: { SpanTitle, Bot },
  mixins: [mixinPermissions],
  data() {
    return {
      labelCol: { lg: 3, md: 5, sm: 8 },
      wrapperCol: { lg: 15, md: 19, sm: 16 },
      id: null,
      feishuData: {
        id: '',
        password: '',
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
      getNoticeConfigByPlatform({ platform: 'feishuApp' }).then((res) => {
        this.id = res?.id ?? null
        if (this.id) {
          this.feishuData = res.info
          this.$refs.bot.setData(res?.info?.bot)
        }
      })
    },
    onSubmit() {
      this.$refs.feishuForm.validate(async (valid) => {
        if (valid) {
          this.$refs.bot.getData(async (flag, bot) => {
            if (flag) {
              if (this.id) {
                await putNoticeConfigByPlatform(this.id, { info: { ...this.feishuData, bot, label: this.$t('cs.person.feishuApp') } })
              } else {
                await postNoticeConfigByPlatform({
                  platform: 'feishuApp',
                  info: { ...this.feishuData, bot, label: this.$t('cs.person.feishuApp') },
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
      this.feishuData = {
        id: '',
        password: '',
      }
    },
  },
}
</script>

<style lang="less" scoped>
.notice-feishu-wrapper {
  background-color: #fff;
  padding-top: 15px;
  overflow: auto;
  margin-bottom: -24px;
  border-radius: @border-radius-box;
  .notice-feishu-wrapper-tips {
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
