<template>
  <CustomDrawer
    wrapClassName="trigger-form"
    :width="910"
    :title="title"
    :visible="visible"
    @close="handleCancel"
    @ok="handleOk"
    destroyOnClose
  >
    <div class="custom-drawer-bottom-action">
      <a-button type="primary" ghost @click="handleCancel">{{ $t('cancel') }}</a-button>
      <a-button v-if="triggerId" type="danger" @click="handleDetele">{{ $t('delete') }}</a-button>
      <a-button @click="handleOk" type="primary">{{ $t('confirm') }}</a-button>
    </div>
    <a-form-model ref="triggerForm" :model="form" :rules="rules" :label-col="{ span: 3 }" :wrapper-col="{ span: 18 }">
      <p>
        <strong>{{ $t('cmdb.ciType.basicInfo') }}</strong>
      </p>
      <a-form-model-item :label="$t('name')" prop="name">
        <a-input v-model="form.name" :placeholder="$t('cmdb.ciType.nameInputTips')" />
      </a-form-model-item>
      <a-form-model-item :label="$t('type')">
        <a-radio-group v-model="category">
          <a-radio-button :value="1">
            {{ $t('cmdb.ciType.triggerDataChange') }}
          </a-radio-button>
          <a-radio-button :value="2">
            {{ $t('cmdb.ciType.triggerDate') }}
          </a-radio-button>
        </a-radio-group>
      </a-form-model-item>
      <a-form-model-item :label="$t('desc')" prop="description">
        <a-input v-model="form.description" :placeholder="$t('cmdb.ciType.descInput')" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.ciType.triggerEnable')" prop="enable">
        <a-switch v-model="form.enable" />
      </a-form-model-item>
      <template v-if="category === 1">
        <p>
          <strong>{{ $t('cmdb.ciType.triggerCondition') }}</strong>
        </p>
        <a-form-model-item :label="$t('cmdb.ciType.event')" prop="action">
          <a-radio-group v-model="form.action">
            <a-radio value="0">
              {{ $t('cmdb.ciType.addInstance') }}
            </a-radio>
            <a-radio value="1">
              {{ $t('cmdb.ciType.deleteInstance') }}
            </a-radio>
            <a-radio value="2">
              {{ $t('cmdb.ciType.changeInstance') }}
            </a-radio>
          </a-radio-group>
        </a-form-model-item>
        <a-form-model-item v-if="form.action === '2'" :label="$t('cmdb.ciType.attributes')" prop="attr_ids">
          <a-select
            v-model="form.attr_ids"
            show-search
            mode="multiple"
            :placeholder="$t('cmdb.ciType.selectMutipleAttributes')"
          >
            <a-select-option v-for="attr in attrList" :key="attr.id" :value="attr.id">{{
              attr.alias || attr.name
            }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item :label="$t('cmdb.ciType.filter')" class="trigger-form-filter">
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
      <p>
        <strong>{{ $t('cmdb.ciType.triggerCondition') }}</strong>
      </p>
      <a-form-model
        ref="dateForm"
        :model="dateForm"
        :rules="dateFormRules"
        :label-col="{ span: 3 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-model-item :label="$t('cmdb.ciType.attributes')" prop="attr_id">
          <a-select v-model="dateForm.attr_id" :placeholder="$t('cmdb.ciType.selectSingleAttribute')">
            <a-select-option v-for="attr in canAddTriggerAttr" :key="attr.id" :value="attr.id">{{
              attr.alias || attr.name
            }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item :label="$t('cmdb.ciType.filter')" class="trigger-form-filter">
          <FilterComp
            ref="filterComp"
            :isDropdown="false"
            :canSearchPreferenceAttrList="attrList"
            @setExpFromFilter="setExpFromFilter"
            :expression="filterExp ? `q=${filterExp}` : ''"
          />
        </a-form-model-item>
        <a-form-model-item :label="$t('cmdb.ciType.beforeDays')" prop="before_days">
          <a-input-number v-model="dateForm.before_days" :min="0" />
          {{ $t('cmdb.ciType.days') }}
        </a-form-model-item>
        <a-form-model-item :label="$t('cmdb.ciType.notifyAt')" prop="notify_at">
          <a-time-picker v-model="dateForm.notify_at" format="HH:mm" valueFormat="HH:mm" />
        </a-form-model-item>
      </a-form-model>
    </template>
    <p>
      <strong>{{ $t('cmdb.ciType.triggerAction') }}</strong>
    </p>
    <a-radio-group
      v-model="triggerAction"
      :style="{ width: '100%', display: 'flex', justifyContent: 'space-around', marginBottom: '10px' }"
    >
      <a-radio value="1">
        {{ $t('cmdb.ciType.notify') }}
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
      <a-form-model-item :label="$t('cmdb.ciType.receivers')" prop="employee_ids" class="trigger-form-employee">
        <EmployeeTreeSelect multiple v-model="notifies.employee_ids" />
        <div class="trigger-form-custom-email">
          <a-textarea
            v-if="showCustomEmail"
            v-model="notifies.custom_email"
            :placeholder="$t('cmdb.ciType.emailTips')"
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
          >{{ `${showCustomEmail ? $t('delete') : $t('add')}` }}{{ $t('cmdb.ciType.customEmail') }}</a-button
          >
        </div>
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.ciType.notifySubject')" prop="subject">
        <a-input v-model="notifies.subject" :placeholder="$t('cmdb.ciType.notifySubjectTips')" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.ciType.notifyContent')" prop="body" :wrapper-col="{ span: 21 }">
        <NoticeContent :needOld="category === 1 && form.action === '2'" :attrList="attrList" ref="noticeContent" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.ciType.notifyMethod')" prop="method">
        <a-checkbox-group v-model="notifies.method">
          <a-row :style="{ marginTop: '4px' }" :gutter="[0, 12]">
            <a-col :span="6">
              <a-checkbox value="email">
                <ops-icon type="email" style="margin-right:5px" />{{ $t('email') }}
              </a-checkbox>
            </a-col>
            <a-col :span="6">
              <a-checkbox value="wechatApp">
                <ops-icon type="wechatApp" style="margin-right:5px" />{{ $t('wechat') }}
              </a-checkbox>
            </a-col>
            <a-col :span="6">
              <a-checkbox value="dingdingApp">
                <ops-icon type="dingdingApp" style="margin-right:5px" />{{ $t('dingding') }}
              </a-checkbox>
            </a-col>
            <a-col :span="6">
              <a-checkbox value="feishuApp">
                <ops-icon type="feishuApp" style="margin-right:5px" />{{ $t('feishu') }}
              </a-checkbox>
            </a-col>
            <a-col :span="4" :style="{ lineHeight: '32px' }">
              <ops-icon type="robot" style="margin-right:5px" />{{ $t('bot') }}：
            </a-col>
            <a-col :span="18">
              <treeselect
                :disable-branch-nodes="true"
                :class="{
                  'custom-treeselect': true,
                  'custom-treeselect-bgcAndBorder': true,
                }"
                :style="{
                  '--custom-height': '32px',
                  lineHeight: '32px',
                  '--custom-bg-color': '#fff',
                  '--custom-border': '1px solid #d9d9d9',
                  '--custom-multiple-lineHeight': '14px',
                }"
                v-model="selectedBot"
                :multiple="true"
                :clearable="true"
                searchable
                :options="appBot"
                value-consists-of="LEAF_PRIORITY"
                :placeholder="$t('cmdb.ciType.botSelect')"
                :normalizer="
                  (node) => {
                    return {
                      id: node.name,
                      label: node.label || node.name,
                      children: node.bot,
                    }
                  }
                "
                appendToBody
                :zIndex="1050"
                :noChildrenText="$t('noData')"
              >
                <div
                  :title="node.label"
                  slot="option-label"
                  slot-scope="{ node }"
                  :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
                >
                  <ops-icon :type="node.id" v-if="node.children" />{{ node.label }}
                </div>
                <div slot="value-label" slot-scope="{ node }">
                  <ops-icon :type="node.parentNode.id" />{{ node.label }}
                </div>
              </treeselect>
            </a-col>
          </a-row>
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
    <span v-if="triggerAction === '2'" class="trigger-tips">{{ webhookTips }}</span>
    <Webhook ref="webhook" style="margin-top:10px" v-if="triggerAction === '2'" />
  </CustomDrawer>
</template>

<script>
import _ from 'lodash'
import { addTrigger, updateTrigger, deleteTrigger } from '../../api/CIType'
import FilterComp from '@/components/CMDBFilterComp'
import EmployeeTreeSelect from '@/views/setting/components/employeeTreeSelect.vue'
import Webhook from '../../components/webhook'
import NoticeContent from '../../components/noticeContent'
import { getNoticeByEmployeeIds } from '@/api/employee'
import { getNoticeConfigAppBot } from '@/api/noticeSetting'

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
      visible: false,
      category: 1,
      form: _.cloneDeep(defaultForm),
      rules: {
        name: [{ required: true, message: this.$t('cmdb.ciType.nameInputTips') }],
      },
      dateForm: _.cloneDeep(defaultDateForm),
      dateFormRules: {
        attr_id: [{ required: true, message: this.$t('cmdb.ciType.selectAttributes') }],
      },
      notifies: _.cloneDeep(defaultNotify),
      notifiesRules: {},
      WxUsers: [],
      filterValue: '',
      triggerId: null,
      title: this.$t('cmdb.ciType.newTrigger'),
      attrList: [],
      filterExp: '',
      triggerAction: '1',
      searchValue: '',
      dags: [],
      isShow: false,
      dag_id: null,
      showCustomEmail: false,
      appBot: [],
      selectedBot: undefined,
    }
  },
  computed: {
    canAddTriggerAttr() {
      return this.attrList.filter((attr) => attr.value_type === '3' || attr.value_type === '4')
    },
    filterList() {
      if (this.searchValue) {
        return this.dags.filter((item) => item.label.toLowerCase().includes(this.searchValue.toLowerCase()))
      }
      return this.dags
    },
    tips() {
      return this.$t('cmdb.ciType.refAttributeTips')
    },
    webhookTips() {
      return this.$t('cmdb.ciType.webhookRefAttributeTips')
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
    async getNoticeConfigAppBot() {
      await getNoticeConfigAppBot().then((res) => {
        this.appBot = res
      })
    },
    createFromTriggerTable(attrList) {
      this.visible = true
      this.getNoticeConfigAppBot()
      this.attrList = attrList
      this.triggerId = null
      this.title = this.$t('cmdb.ciType.newTrigger')
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
      await this.getNoticeConfigAppBot()
      this.attrList = attrList
      if (property.has_trigger) {
        this.triggerId = property.trigger.id
        this.title = this.$t('cmdb.ciType.editTriggerTitle', { name: `${property.alias || property.name}` })
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
              .filter((t) => !t.employee_id && t.email)
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
          const _method = method.filter((item) => ['email', 'wechatApp', 'dingdingApp', 'feishuApp'].includes(item))
          const _flatAppBot = []
          this.appBot.forEach((item) => {
            _flatAppBot.push(...item.bot.map((b) => b.name))
          })
          const selectedBot = method.filter(
            (item) => !['email', 'wechatApp', 'dingdingApp', 'feishuApp'].includes(item) && _flatAppBot.includes(item)
          )
          this.selectedBot = selectedBot
          this.notifies = { employee_ids, custom_email, subject, method: _method }
        }
      } else {
        this.title = this.$t('cmdb.ciType.newTriggerTitle', { name: `${property.alias || property.name}` })
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
      this.selectedBot = undefined
      this.visible = false
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
              if (this.selectedBot && this.selectedBot.length) {
                this.selectedBot.forEach((bot) => {
                  tos.push({ [`${bot}`]: bot })
                })
              }
              if (this.category === 2) {
                const { before_days, notify_at } = this.dateForm
                params.option.notifies = {
                  tos,
                  subject,
                  body,
                  body_html,
                  method: [...method, ...(this.selectedBot ?? [])],
                  before_days,
                  notify_at,
                }
              } else {
                params.option.notifies = {
                  tos,
                  subject,
                  body,
                  body_html,
                  method: [...method, ...(this.selectedBot ?? [])],
                }
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
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteTrigger'),
        onOk() {
          deleteTrigger(that.CITypeId, that.triggerId).then(() => {
            that.$message.success(that.$t('deleteSuccess'))
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
