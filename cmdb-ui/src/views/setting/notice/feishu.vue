<template>
  <div class="notice-feishu-wrapper" :style="{ height: `${windowHeight - 64}px` }">
    <a-form-model ref="feishuForm" :model="feishuData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <SpanTitle>基础设置</SpanTitle>
      <a-form-model-item label="应用ID">
        <a-input v-model="feishuData.id" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="应用密码">
        <a-input v-model="feishuData.password" :disabled="!isEditable" />
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
          ]"
        />
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
                await putNoticeConfigByPlatform(this.id, { info: { ...this.feishuData, bot, label: '飞书' } })
              } else {
                await postNoticeConfigByPlatform({
                  platform: 'feishuApp',
                  info: { ...this.feishuData, bot, label: '飞书' },
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
  border-radius: 15px;
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
