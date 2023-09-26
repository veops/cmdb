<template>
  <CustomDrawer
    wrapClassName="trigger-form"
    :width="700"
    :title="title"
    :visible="visible"
    @close="handleCancel"
    @ok="handleOk"
  >
    <div class="custom-drawer-bottom-action">
      <a-button type="primary" ghost @click="handleCancel">取消</a-button>
      <a-button v-if="triggerId" type="danger" @click="handleDetele">删除</a-button>
      <a-button @click="handleOk" type="primary">确定</a-button>
    </div>
    <a-form-model ref="triggerForm" :model="form" :rules="rules" :label-col="{ span: 3 }" :wrapper-col="{ span: 18 }">
      <p><strong>基本信息</strong></p>
      <a-form-model-item label="名称" prop="name">
        <a-input v-model="form.name" placeholder="请输入名称" />
      </a-form-model-item>
      <a-form-model-item label="类型">
        <a-radio-group v-model="category">
          <a-radio-button :value="1">
            数据变更
          </a-radio-button>
          <a-radio-button :value="2">
            日期属性
          </a-radio-button>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item label="备注" prop="description">
        <a-input v-model="form.description" placeholder="请输入备注" />
      </a-form-model-item>
      <a-form-model-item label="开启" prop="enable">
        <a-switch v-model="form.enable" />
      </a-form-model-item>
      <template v-if="category === 1">
        <p><strong>触发条件</strong></p>
        <a-form-model-item label="事件" prop="action">
          <a-radio-group v-model="form.action">
            <a-radio value="0">
              新增实例
            </a-radio>
            <a-radio value="1">
              删除实例
            </a-radio>
            <a-radio value="2">
              实例变更
            </a-radio>
          </a-radio-group>
        </a-form-model-item>
        <a-form-model-item v-if="form.action === '2'" label="属性" prop="attr_ids">
          <a-select v-model="form.attr_ids" show-search mode="multiple" placeholder="请选择属性（多选）">
            <a-select-option v-for="attr in attrList" :key="attr.id" :value="attr.id">{{
              attr.alias || attr.name
            }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="筛选" class="trigger-form-filter">
          <FilterComp
            ref="filterComp"
            :isDropdown="false"
            :canSearchPreferenceAttrList="attrList"
            @setExpFromFilter="setExpFromFilter"
            :expression="filterExp ? `q=${filterExp}` : ''"
          />
        </a-form-model-item>
      </template>
    </a-form-model>
    <template v-if="category === 2">
      <p><strong>触发条件</strong></p>
      <a-form-model
        ref="dateForm"
        :model="dateForm"
        :rules="dateFormRules"
        :label-col="{ span: 3 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-model-item label="属性" prop="attr_id">
          <a-select v-model="dateForm.attr_id" placeholder="请选择属性（单选）">
            <a-select-option v-for="attr in canAddTriggerAttr" :key="attr.id" :value="attr.id">{{
              attr.alias || attr.name
            }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="筛选" class="trigger-form-filter">
          <FilterComp
            ref="filterComp"
            :isDropdown="false"
            :canSearchPreferenceAttrList="attrList"
            @setExpFromFilter="setExpFromFilter"
            :expression="filterExp ? `q=${filterExp}` : ''"
          />
        </a-form-model-item>
        <a-form-model-item label="提前" prop="before_days">
          <a-input-number v-model="dateForm.before_days" :min="0" />
          天
        </a-form-model-item>
        <a-form-model-item label="发送时间" prop="notify_at">
          <a-time-picker v-model="dateForm.notify_at" format="HH:mm" valueFormat="HH:mm" />
        </a-form-model-item>
      </a-form-model>
    </template>
    <p><strong>触发动作</strong></p>
    <a-radio-group
      v-model="triggerAction"
      :style="{ width: '100%', display: 'flex', justifyContent: 'space-around', marginBottom: '10px' }"
    >
      <a-radio value="1">
        通知
      </a-radio>
      <a-radio value="2">
        Webhook
      </a-radio>
      <!-- <a-radio value="3">
        DAG
      </a-radio> -->
    </a-radio-group>
    <a-form-model
      ref="notifiesForm"
      :model="notifies"
      :rules="notifiesRules"
      :label-col="{ span: 3 }"
      :wrapper-col="{ span: 18 }"
      v-if="triggerAction === '1'"
    >
      <a-form-model-item label=" " :colon="false">
        <span class="trigger-tips">{{ tips }}</span>
      </a-form-model-item>
      <a-form-model-item label="收件人" prop="employee_ids" class="trigger-form-employee">
        <EmployeeTreeSelect multiple v-model="notifies.employee_ids" />
        <div class="trigger-form-custom-email">
          <a-textarea
            v-if="showCustomEmail"
            v-model="notifies.custom_email"
            placeholder="请输入邮箱，多个邮箱用;分隔"
            :rows="1"
          />
          <a-button
            @click="
              () => {
                showCustomEmail = !showCustomEmail
              }
            "
            type="primary"
            size="small"
            class="ops-button-primary"
          >{{ `${showCustomEmail ? '删除' : '添加'}自定义收件人` }}</a-button
          >
        </div>
      </a-form-model-item>
      <a-form-model-item label="通知标题" prop="subject">
        <a-input v-model="notifies.subject" placeholder="请输入通知标题" />
      </a-form-model-item>
      <a-form-model-item label="内容" prop="body" :wrapper-col="{ span: 21 }">
        <NoticeContent :needOld="category === 1 && form.action === '2'" :attrList="attrList" ref="noticeContent" />
      </a-form-model-item>
      <a-form-model-item label="通知方式" prop="method">
        <a-checkbox-group v-model="notifies.method">
          <a-checkbox value="wechatApp">
            微信
          </a-checkbox>
          <a-checkbox value="email">
            邮件
          </a-checkbox>
        </a-checkbox-group>
      </a-form-model-item>
    </a-form-model>
    <div class="auto-complete-wrapper" v-if="triggerAction === '3'">
      <a-input
        id="auto-complete-wrapper-input"
        ref="input"
        v-model="searchValue"
        @focus="focusOnInput"
        @blur="handleBlurInput"
        allowClear
      >
      </a-input>
      <div id="auto-complete-wrapper-popover" class="auto-complete-wrapper-popover" v-if="isShow">
        <div
          class="auto-complete-wrapper-popover-item"
          @click="handleClickSelect(item)"
          v-for="item in filterList"
          :key="item.id"
          :title="item.label"
        >
          {{ item.label }}
        </div>
      </div>
    </div>
    <Webhook ref="webhook" style="margin-top:10px" v-if="triggerAction === '2'" />
  </CustomDrawer>
</template>

<script>
import _ from 'lodash'
import { getWX } from '../../api/perm'
import { addTrigger, updateTrigger, deleteTrigger, getAllDagsName } from '../../api/CIType'
import FilterComp from '@/components/CMDBFilterComp'
import EmployeeTreeSelect from '@/views/setting/components/employeeTreeSelect.vue'
import Webhook from '../../components/webhook'
import NoticeContent from '../../components/noticeContent'
import { getNoticeByEmployeeIds } from '@/api/employee'

export default {
  name: 'TriggerForm',
  components: { FilterComp, Webhook, EmployeeTreeSelect, NoticeContent },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    const defaultForm = {
      name: '',
      description: '',
      enable: true,
      action: '0',
      attr_ids: [],
    }
    const defaultDateForm = {
      attr_id: undefined,
      before_days: 0,
      notify_at: '08:00',
    }
    const defaultNotify = {
      employee_ids: undefined,
      custom_email: '',
      subject: '',
      body: '',
      method: ['wechatApp'],
    }
    return {
      defaultForm,
      defaultDateForm,
      defaultNotify,
      tips: '标题、内容可以引用该模型的属性值，引用方法为: {{ attr_name }}',
      visible: false,
      category: 1,
      form: _.cloneDeep(defaultForm),
      rules: {
        name: [{ required: true, message: '请填写名称' }],
      },
      dateForm: _.cloneDeep(defaultDateForm),
      dateFormRules: {
        attr_id: [{ required: true, message: '请选择属性' }],
      },
      notifies: _.cloneDeep(defaultNotify),
      notifiesRules: {},
      WxUsers: [],
      filterValue: '',
      triggerId: null,
      title: '新增触发器',
      attrList: [],
      filterExp: '',
      triggerAction: '1',
      searchValue: '',
      dags: [],
      isShow: false,
      dag_id: null,
      showCustomEmail: false,
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
    canAddTriggerAttr() {
      return this.attrList.filter((attr) => attr.value_type === '3' || attr.value_type === '4')
    },
    filterList() {
      if (this.searchValue) {
        return this.dags.filter((item) => item.label.toLowerCase().includes(this.searchValue.toLowerCase()))
      }
      return this.dags
    },
  },
  inject: {
    refresh: {
      from: 'refresh',
      default: null,
    },
  },
  mounted() {},
  methods: {
    async getDags() {
      await getAllDagsName().then((res) => {
        this.dags = res.map((dag) => ({ id: dag[1], label: dag[0] }))
      })
    },
    createFromTriggerTable(attrList) {
      this.visible = true
      this.getWxList()
      // this.getDags()
      this.attrList = attrList
      this.triggerId = null
      this.title = '新增触发器'
      this.form = _.cloneDeep(this.defaultForm)
      this.dateForm = _.cloneDeep(this.defaultDateForm)
      this.notifies = _.cloneDeep(this.defaultNotify)
      this.category = 1
      this.triggerAction = '1'
      this.filterExp = ''
      this.$nextTick(() => {
        this.$refs.filterComp.visibleChange(true, false)
        setTimeout(() => {
          this.$refs.noticeContent.setContent('')
        }, 100)
      })
    },
    async open(property, attrList) {
      this.visible = true
      this.getWxList()
      // await this.getDags()
      this.attrList = attrList
      if (property.has_trigger) {
        this.triggerId = property.trigger.id
        this.title = `编辑触发器 ${property.alias || property.name}`
        const { name, description, enable, action = '0', attr_ids, filter = '' } = property?.trigger?.option ?? {}
        this.filterExp = filter
        this.$nextTick(() => {
          this.$refs.filterComp.visibleChange(true, false)
        })
        this.form = { name, description, enable, action, attr_ids }
        const { attr_id } = property?.trigger ?? {}
        if (attr_id) {
          this.category = 2
          const { before_days, notify_at } = property?.trigger?.option?.notifies ?? {}
          this.dateForm = {
            attr_id,
            before_days,
            notify_at,
          }
        } else {
          this.category = 1
        }
        const { notifies = undefined, webhooks = undefined, dag_id = undefined } = property?.trigger?.option ?? {}
        if (webhooks) {
          this.triggerAction = '2'
          this.$nextTick(() => {
            this.$refs.webhook.setParams(webhooks)
          })
        } else if (dag_id) {
          this.triggerAction = '3'
          this.dag_id = dag_id
          const _find = this.dags.find((item) => item.id === dag_id)
          this.searchValue = _find?.label
        } else if (notifies) {
          this.triggerAction = '1'
          const { tos = [], subject = '', body_html = '', method = ['wechatApp'] } =
            property?.trigger?.option?.notifies ?? {}
          const employee_ids = property?.trigger?.option?.employee_ids ?? undefined
          const custom_email =
            tos
              .filter((t) => !t.employee_id)
              .map((t) => t.email)
              .join(';') ?? ''

          if (custom_email) {
            this.showCustomEmail = true
          }
          if (body_html) {
            setTimeout(() => {
              this.$refs.noticeContent.setContent(body_html)
            }, 100)
          }
          this.notifies = { employee_ids, custom_email, subject, method }
        }
      } else {
        this.title = `新增触发器 ${property.alias || property.name}`
        this.triggerId = null
        this.form = _.cloneDeep(this.defaultForm)
      }
    },
    handleCancel() {
      this.$refs.triggerForm.clearValidate()
      this.$refs.triggerForm.resetFields()
      this.filterValue = ''
      this.form = _.cloneDeep(this.defaultForm)
      this.dateForm = _.cloneDeep(this.defaultDateForm)
      this.notifies = _.cloneDeep(this.defaultNotify)
      this.category = 1
      this.triggerAction = '1'
      this.filterExp = ''
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
          this.$refs.filterComp.handleSubmit()
          const { name, description, enable, action, attr_ids } = this.form
          const params = {
            attr_id: '',
            option: {
              filter: this.filterExp,
              name,
              description,
              enable,
            },
          }
          switch (this.triggerAction) {
            case '1':
              const { employee_ids, custom_email, subject, method } = this.notifies
              const { body, body_html } = this.$refs.noticeContent.getContent()
              let tos = []
              if (employee_ids && employee_ids.length) {
                await getNoticeByEmployeeIds({ employee_ids: employee_ids.map((item) => item.split('-')[1]) }).then(
                  (res) => {
                    tos = tos.concat(res)
                  }
                )
                params.option.employee_ids = employee_ids
              }
              if (this.showCustomEmail) {
                custom_email.split(';').forEach((email) => {
                  tos.push({ email })
                })
              }
              if (this.category === 2) {
                const { before_days, notify_at } = this.dateForm
                params.option.notifies = { tos, subject, body, body_html, method, before_days, notify_at }
              } else {
                params.option.notifies = { tos, subject, body, body_html, method }
              }
              break
            case '2':
              const webhooks = this.$refs.webhook.getParams()
              params.option.webhooks = webhooks
              break
            case '3':
              params.option.dag_id = this.dag_id
              break
          }
          if (this.category === 1) {
            params.option.action = action
            if (action === '2') {
              params.option.attr_ids = attr_ids
            }
          }
          if (this.category === 2) {
            this.$refs.dateForm.validate((valid) => {
              if (valid) {
                const { attr_id, before_days, notify_at } = this.dateForm
                params.attr_id = attr_id
                params.option.notifies = { ..._.cloneDeep(params.option.notifies), before_days, notify_at }
              } else {
                throw Error()
              }
            })
          }
          if (this.triggerId) {
            await updateTrigger(this.CITypeId, this.triggerId, params)
          } else {
            await addTrigger(this.CITypeId, params)
          }
          this.handleCancel()
          if (this.refresh) {
            this.refresh()
          }
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
            if (that.refresh) {
              that.refresh()
            }
          })
        },
      })
    },
    setExpFromFilter(filterExp) {
      if (filterExp) {
        this.filterExp = `${filterExp}`
      } else {
        this.filterExp = ''
      }
    },
    handleBlurInput() {
      setTimeout(() => {
        this.isShow = false
      }, 100)
    },
    focusOnInput() {
      this.isShow = true
    },
    handleClickSelect(item) {
      this.searchValue = item.label
      this.dag_id = item.id
    },
  },
}
</script>

<style lang="less">
.trigger-form {
  .ant-form-item {
    margin-bottom: 5px;
  }
  .trigger-form-employee,
  .trigger-form-filter {
    .ant-form-item-control {
      line-height: 24px;
    }
  }
  .trigger-form-filter {
    .table-filter-add {
      line-height: 40px;
    }
  }
}
</style>

<style lang="less" scoped>
@import '~@/style/static.less';

.auto-complete-wrapper {
  position: relative;
  margin-left: 25px;
  width: 250px;
  margin-top: 20px;
  .auto-complete-wrapper-popover {
    position: fixed;
    width: 250px;
    max-height: 200px;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: #fff;
    z-index: 10;
    box-shadow: 0 2px 8px #00000026;
    .auto-complete-wrapper-popover-item {
      .ops_popover_item();
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}

.trigger-form-custom-email {
  margin-top: 10px;
  text-align: right;
}

.trigger-tips {
  border: 1px solid #d4380d;
  background-color: #fff2e8;
  padding: 2px 10px;
  border-radius: 4px;
  color: #d4380d;
  line-height: 1.5;
}
</style>
