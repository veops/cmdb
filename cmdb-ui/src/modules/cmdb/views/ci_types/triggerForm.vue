<template>
  <a-modal :title="title" :visible="visible" @cancel="handleCancel" @ok="handleOk">
    <a-space slot="footer">
      <a-button type="primary" ghost @click="handleCancel">取消</a-button>
      <a-button v-if="triggerId" type="danger" @click="handleDetele">删除</a-button>
      <a-button @click="handleOk" type="primary">确定</a-button>
    </a-space>
    <a-form-model ref="triggerForm" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
      <a-form-model-item label="属性" prop="attr_id" :hidden="!isCreateFromTriggerTable || triggerId">
        <a-select v-model="form.attr_id">
          <a-select-option v-for="attr in canAddTriggerAttr" :key="attr.id" :value="attr.id">{{
            attr.alias || attr.name
          }}</a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="主题" prop="subject">
        <a-input v-model="form.subject" />
      </a-form-model-item>
      <a-form-model-item label="内容" prop="body">
        <a-textarea v-model="form.body" :rows="3" />
      </a-form-model-item>
      <a-form-model-item label="微信通知" prop="wx_to">
        <a-select
          mode="tags"
          v-model="form.wx_to"
          placeholder="选择微信通知人"
          showSearch
          :filter-option="false"
          @search="filterChange"
        >
          <a-select-option v-for="item in filterWxUsers" :value="item['wx_id']" :key="item.id">
            <span>{{ item['nickname'] }}</span>
            <a-divider type="vertical" />
            <span>{{ item['wx_id'].length > 12 ? item['wx_id'].slice(0, 10) + '...' : item['wx_id'] }}</span>
          </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item label="邮箱通知" prop="mail_to">
        <a-textarea v-model="form.mail_to" :rows="3" placeholder="多个邮箱用逗号分隔" />
      </a-form-model-item>
      <a-form-model-item label="提前" prop="before_days">
        <a-input-number v-model="form.before_days" :min="0" />
        天
      </a-form-model-item>
      <a-form-model-item label="发送时间" prop="notify_at">
        <a-time-picker v-model="form.notify_at" format="HH:mm" valueFormat="HH:mm" />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { getWX } from '../../api/perm'
import { addTrigger, updateTrigger, deleteTrigger } from '../../api/CIType'
export default {
  name: 'TriggerForm',
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      visible: false,
      form: { attr_id: '', subject: '', body: '', wx_to: [], mail_to: '', before_days: 0, notify_at: '08:00' },
      rules: {
        attr_id: [{ required: true, message: '请选择属性' }],
        subject: [{ required: true, message: '请填写主题' }],
        body: [{ required: true, message: '请填写内容' }],
      },
      WxUsers: [],
      filterValue: '',
      triggerId: null,
      attr_id: null,
      canAddTriggerAttr: [],
      isCreateFromTriggerTable: false,
      title: '新增触发器',
    }
  },
  computed: {
    filterWxUsers() {
      if (!this.filterValue) {
        return this.WxUsers
      }
      return this.WxUsers.filter(
        (user) =>
          user.nickname.toLowerCase().indexOf(this.filterValue.toLowerCase()) >= 0 ||
          user.username.toLowerCase().indexOf(this.filterValue.toLowerCase()) >= 0
      )
    },
  },
  inject: ['refresh'],
  methods: {
    createFromTriggerTable(canAddTriggerAttr) {
      this.visible = true
      this.getWxList()
      this.canAddTriggerAttr = canAddTriggerAttr
      this.triggerId = null
      this.isCreateFromTriggerTable = true
      this.title = '新增触发器'
      this.form = {
        attr_id: '',
        subject: '',
        body: '',
        wx_to: [],
        mail_to: '',
        before_days: 0,
        notify_at: '08:00',
      }
    },
    open(property) {
      this.visible = true
      this.getWxList()
      if (property.has_trigger) {
        this.triggerId = property.trigger.id
        this.title = `编辑触发器 ${property.alias || property.name}`
        this.form = {
          ...property.trigger.notify,
          attr_id: property.id,
          mail_to: property.trigger.notify.mail_to ? property.trigger.notify.mail_to.join(',') : '',
        }
      } else {
        this.title = `新增触发器 ${property.alias || property.name}`
        this.triggerId = null
        this.form = {
          attr_id: property.id,
          subject: '',
          body: '',
          wx_to: [],
          mail_to: '',
          before_days: 0,
          notify_at: '08:00',
        }
      }
    },
    handleCancel() {
      this.$refs.triggerForm.clearValidate()
      this.$refs.triggerForm.resetFields()
      this.filterValue = ''
      this.visible = false
    },
    getWxList() {
      getWX().then((res) => {
        this.WxUsers = res.filter((item) => item.wx_id)
      })
    },
    filterChange(value) {
      this.filterValue = value
    },
    handleOk() {
      this.$refs.triggerForm.validate(async (valid) => {
        if (valid) {
          const { mail_to, attr_id } = this.form
          const params = {
            attr_id,
            notify: { ...this.form, mail_to: mail_to ? mail_to.split(',') : undefined },
          }
          delete params.notify.attr_id
          if (this.triggerId) {
            await updateTrigger(this.CITypeId, this.triggerId, params)
          } else {
            await addTrigger(this.CITypeId, params)
          }
          this.handleCancel()
          this.refresh()
        }
      })
    },
    handleDetele() {
      const that = this
      this.$confirm({
        title: '警告',
        content: '确认删除该触发器吗?',
        onOk() {
          deleteTrigger(that.CITypeId, that.triggerId).then(() => {
            that.$message.success('删除成功！')
            that.handleCancel()
            that.refresh()
          })
        },
      })
    },
  },
}
</script>

<style></style>
