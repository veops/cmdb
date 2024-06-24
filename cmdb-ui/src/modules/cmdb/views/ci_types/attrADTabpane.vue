<template>
  <div class="attr-ad-tab-pane" :style="{ height: `${windowHeight - 254}px` }">
    <a
      v-if="!adrIsInner"
      :style="{ position: 'absolute', right: 0, top: 0 }"
      @click="
        () => {
          $emit('openEditDrawer', currentAdr, 'edit', 'plugin')
        }
      "
    >
      <a-space>
        <ops-icon type="icon-xianxing-edit" />
        <span>{{ $t('edit') }}</span>
      </a-space>
    </a>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.attributeMap') }}</div>
    <div class="attr-ad-attributemap-main">
      <AttrMapTable
        v-if="adrType === 'agent'"
        ref="attrMapTable"
        :ruleType="adrType"
        :tableData="tableData"
        :ciTypeAttributes="ciTypeAttributes"
        :uniqueKey="uniqueKey"
      />
      <HttpSnmpAD
        v-else
        :isEdit="true"
        ref="httpSnmpAd"
        :ruleType="adrType"
        :ruleName="adrName"
        :ciTypeAttributes="ciTypeAttributes"
        :adCITypeList="adCITypeList"
        :currentTab="adr_id"
        :uniqueKey="uniqueKey"
        :style="{ marginBottom: '20px' }"
      />
    </div>
    <template v-if="adrType === 'snmp'">
      <div class="attr-ad-header">{{ $t('cmdb.ciType.nodeConfig') }}</div>
      <a-form :form="form3" layout="inline" class="attr-ad-snmp-form">
        <NodeSetting ref="nodeSetting" :initNodes="nodes" :form="form3" />
      </a-form>
    </template>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.adExecConfig') }}</div>
    <a-form-model
      :model="form"
      :labelCol="labelCol"
      labelAlign="left"
      :wrapperCol="{ span: 14 }"
      class="attr-ad-form"
    >
      <a-form-model-item :label="$t('cmdb.ciType.adExecTarget')">
        <CustomRadio v-model="agent_type" :radioList="agentTypeRadioList">
          <a-input
            :style="{ width: '300px' }"
            :placeholder="$t('cmdb.ciType.oneagentIdTips')"
            v-show="agent_type === 'agent_id'"
            slot="extra_agent_id"
            v-model="form.agent_id"
          />
          <a-input
            :style="{ width: '300px' }"
            v-show="agent_type === 'query_expr'"
            slot="extra_query_expr"
            :placeholder="$t('cmdb.ciType.selectFromCMDBTips')"
            v-model="form.query_expr"
          >
            <a @click="handleOpenCmdb" slot="suffix"><a-icon type="menu"/></a>
          </a-input>
        </CustomRadio>
      </a-form-model-item>
      <a-form-model-item
        :labelCol="labelCol"
        :label="$t('cmdb.ciType.adAutoInLib')"
        :extra="$t('cmdb.ciType.adAutoInLibTip')"
      >
        <a-switch v-model="form.auto_accept" />
      </a-form-model-item>
      <a-form-model-item
        :labelCol="labelCol"
        :wrapperCol="{ span: 6 }"
        :label="$t('cmdb.ciType.adInterval')"
      >
        <el-popover v-model="cronVisible" trigger="click">
          <template slot>
            <Vcrontab
              v-if="adrType"
              ref="cronTab"
              :hideComponent="['second', 'year']"
              :expression="cron"
              :hasFooter="true"
              @fill="crontabFill"
              @hide="hideCron"
            ></Vcrontab>
          </template>
          <a-input
            v-model="cron"
            slot="reference"
            :placeholder="$t('cmdb.ciType.cronTips')"
          />
        </el-popover>
      </a-form-model-item>
    </a-form-model>
    <template v-if="adrType === 'http'">
      <template v-if="isVCenter">
        <div class="attr-ad-header">私有云</div>
        <a-form-model
          :model="privateCloudForm"
          labelAlign="left"
          :labelCol="labelCol"
          :wrapperCol="{ span: 6 }"
          class="attr-ad-form"
        >
          <a-form-model-item label="地址">
            <a-input v-model="privateCloudForm.host" />
          </a-form-model-item>
          <a-form-model-item label="账号">
            <a-input v-model="privateCloudForm.account" />
          </a-form-model-item>
          <a-form-model-item label="密码">
            <a-input-password v-model="privateCloudForm.password" />
          </a-form-model-item>
          <a-form-model-item label="是否证书验证">
            <a-switch v-model="privateCloudForm.insecure" />
          </a-form-model-item>
          <a-form-model-item label="虚拟平台名">
            <a-input v-model="privateCloudForm.vcenterName" />
          </a-form-model-item>
        </a-form-model>
      </template>

      <template v-else>
        <div class="attr-ad-header">{{ $t('cmdb.ciType.cloudAccessKey') }}</div>
        <!-- <div class="public-cloud-info">{{ $t('cmdb.ciType.cloudAccessKeyTip') }}</div> -->
        <a-form-model
          :model="form2"
          labelAlign="left"
          :labelCol="labelCol"
          :wrapperCol="{ span: 6 }"
          class="attr-ad-form"
        >
          <a-form-model-item label="key">
            <a-input-password v-model="form2.key" />
          </a-form-model-item>
          <a-form-model-item label="secret">
            <a-input-password v-model="form2.secret" />
          </a-form-model-item>
        </a-form-model>
      </template>
    </template>

    <AttrADTest
      :adtId="currentAdt.id"
    />

    <div class="attr-ad-footer">
      <a-button type="primary" @click="handleSave">{{ $t('save') }}</a-button>
    </div>
    <CMDBExprDrawer ref="cmdbDrawer" @copySuccess="copySuccess" />
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
import { mapState } from 'vuex'
import Vcrontab from '@/components/Crontab'
import { putCITypeDiscovery, postCITypeDiscovery } from '../../api/discovery'

import HttpSnmpAD from '../../components/httpSnmpAD'
import AttrMapTable from '@/modules/cmdb/components/attrMapTable/index.vue'
import CMDBExprDrawer from '@/components/CMDBExprDrawer'
import NodeSetting from '@/modules/cmdb/components/nodeSetting/index.vue'
import AttrADTest from './attrADTest.vue'
import { Popover } from 'element-ui'

export default {
  name: 'AttrADTabpane',
  components: {
    Vcrontab,
    HttpSnmpAD,
    CMDBExprDrawer,
    NodeSetting,
    AttrMapTable,
    AttrADTest,
    ElPopover: Popover
  },
  props: {
    adr_id: {
      type: Number,
      default: 0,
    },
    adrList: {
      type: Array,
      default: () => {},
    },
    adCITypeList: {
      type: Array,
      default: () => {},
    },
    currentAdt: {
      type: Object,
      default: () => {},
    },
    currentAdr: {
      type: Object,
      default: () => {},
    },
    ciTypeAttributes: {
      type: Array,
      default: () => [],
    },
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      tableData: [],
      form: {
        agent_id: '',
        auto_accept: false,
        query_expr: '',
      },
      form2: {
        key: '',
        secret: '',
      },
      privateCloudForm: {
        host: '',
        account: '',
        password: '',
        insecure: false,
        vcenterName: '',
      },
      interval: 'cron', // interval  cron
      cron: '',
      intervalValue: 3,
      agent_type: 'agent_id',
      nodes: [
        {
          id: uuidv4(),
          ip: '',
          community: '',
          version: '',
        },
      ],
      form3: this.$form.createForm(this, { name: 'snmp_form' }),
      cronVisible: false,
      uniqueKey: '',
      isVCenter: false,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
      user: (state) => state.user,
    }),
    adrType() {
      return this.currentAdr?.type || ''
    },
    adrName() {
      return this.currentAdr?.name || ''
    },
    adrIsInner() {
      return this.currentAdr?.is_inner || ''
    },
    agentTypeRadioList() {
      const radios = [
        { value: 'agent_id', label: this.$t('cmdb.ciType.specifyNodes') },
        { value: 'query_expr', label: this.$t('cmdb.ciType.selectFromCMDBTips') },
      ]

      const permissions = this?.user?.roles?.permissions
      if ((permissions.includes('cmdb_admin') || permissions.includes('admin')) && this.adrType === 'agent') {
        radios.unshift({ value: 'all', label: this.$t('cmdb.ciType.allNodes') })
      }

      return radios
    },
    radioList() {
      return [
        { value: 'interval', label: this.$t('cmdb.ciType.byInterval') },
        { value: 'cron', label: '按cron', layout: 'vertical' },
      ]
    },
    labelCol() {
      const span = this.$i18n.locale === 'en' ? 4 : 2
      return {
        span
      }
    }
  },
  mounted() {},
  methods: {
    init() {
      const _find = this.adrList.find((item) => Number(item.id) === Number(this.adr_id))
      const _findADT = this.adCITypeList.find((item) => Number(item.id) === Number(this.currentAdt.id))
      this.uniqueKey = _find?.unique_key ?? ''

      if (this.adrType === 'http') {
        const {
          category = undefined,
          key = '',
          secret = '',
          host = '',
          account = '',
          password = '',
          insecure = false,
          vcenterName = ''
        } = _findADT?.extra_option ?? {}

        if (_find?.name === 'VCenter') {
          this.isVCenter = true
          this.privateCloudForm = {
            host,
            account,
            password,
            insecure,
            vcenterName,
          }
        } else {
          this.isVCenter = false
          this.form2 = {
            key,
            secret,
          }
        }

        this.$refs.httpSnmpAd.setCurrentCate(category)
      }
      if (this.adrType === 'snmp') {
        this.nodes = _findADT?.extra_option?.nodes?.length ? _findADT?.extra_option?.nodes : [
          {
            id: uuidv4(),
            ip: '',
            community: '',
            version: '',
          },
        ]
        this.$nextTick(() => {
          this.$refs.nodeSetting.initNodesFunc()
          this.$nextTick(() => {
            this.$refs.nodeSetting.setNodeField()
          })
        })
      }
      if (this.adrType === 'agent') {
        this.tableData = (_find?.attributes || []).map((item) => {
          if (_findADT.attributes) {
            return {
              ...item,
              attr: _findADT.attributes[`${item.name}`],
            }
          } else {
            const _find = this.ciTypeAttributes.find((ele) => ele.name === item.name)
            if (_find) {
              return {
                ...item,
                attr: _find.name,
              }
            }
            return item
          }
        })
      }
      this.form = {
        auto_accept: _findADT?.auto_accept || false,
        agent_id: _findADT.agent_id || '',
        query_expr: _findADT.query_expr || '',
      }
      if (_findADT.query_expr) {
        this.agent_type = 'query_expr'
      } else if (_findADT.agent_id) {
        this.agent_type = 'agent_id'
      } else {
        this.agent_type = this.agentTypeRadioList[0].value
      }

      this.interval = 'cron'
      this.cron = _findADT?.cron || ''
    },

    crontabFill(cron) {
      this.cron = cron
    },
    handleSave() {
      const { currentAdt } = this
      let params
      if (this.adrType === 'http') {
        params = {
          extra_option: {
            ...(this.isVCenter ? this.privateCloudForm : this.form2),
            category: this.$refs.httpSnmpAd.currentCate,
          },
        }
      }
      if (this.adrType === 'snmp') {
        params = {
          extra_option: { nodes: this.$refs.nodeSetting?.getNodeValue() ?? [] },
        }
      }
      if (this.adrType === 'agent') {
        const $table = this.$refs.attrMapTable
        const { fullData: _tableData } = $table.getTableData()
        const attributes = {}
        _tableData.forEach((td) => {
          if (td.attr) {
            attributes[`${td.name}`] = td.attr
          }
        })
        params = {
          ...params,
          attributes,
        }
      } else {
        const _tableData = this.$refs.httpSnmpAd.getTableData()
        const attributes = {}
        _tableData.forEach((td) => {
          if (td.attr) {
            attributes[`${td.name}`] = td.attr
          }
        })
        params = {
          ...params,
          attributes,
        }
      }

      params = {
        ...params,
        ...this.form,
        adr_id: currentAdt.adr_id,
        cron: this.interval === 'cron' ? this.cron : null,
      }

      if (this.agent_type === 'agent_id' || this.agent_type === 'all') {
        params.query_expr = ''
        if (this.agent_type === 'agent_id' && !params.agent_id) {
          this.$message.error(this.$t('cmdb.ciType.specifyNodesTips'))
          return
        }
      }

      if (this.agent_type === 'query_expr' || this.agent_type === 'all') {
        params.agent_id = ''
        if (this.agent_type === 'query_expr' && !params.query_expr) {
          this.$message.error(this.$t('cmdb.ciType.selectFromCMDBTips'))
          return
        }
      }

      if (!this.cron) {
        this.$message.error(this.$t('cmdb.ciType.cronRequiredTip'))
        return
      }

      if (currentAdt?.isClient) {
        if (currentAdt?.extra_option) {
          params.extra_option = {
            ...(params?.extra_option || {}),
            ...(currentAdt?.extra_option || {})
          }
        }
        postCITypeDiscovery(this.CITypeId, params).then((res) => {
          this.$message.success(this.$t('saveSuccess'))
          this.$emit('handleSave', res.id)
        })
      } else {
        putCITypeDiscovery(currentAdt.id, params).then((res) => {
          this.$message.success(this.$t('saveSuccess'))
          this.$emit('handleSave', res.id)
        })
      }
    },
    handleOpenCmdb() {
      this.$refs.cmdbDrawer.open()
    },
    copySuccess(text) {
      this.form = {
        ...this.form,
        query_expr: `${text}`,
      }
    },
    hideCron() {
      this.cronVisible = false
    },
  },
}
</script>

<style lang="less" scoped>
.attr-ad-tab-pane {
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;

  .attr-ad-attributemap-main {
    margin-left: 17px;
  }

  .attr-ad-form {
    /deep/ .ant-form-item-label {
      margin-left: 17px;
    }

    /deep/ .ant-form-item-control-wrapper {
      // margin-left: -40px;
    }
  }

  .public-cloud-info {
    color: @text-color_3;
    font-size: 12px;
    font-weight: 400;
    margin-left: 17px;
    margin-bottom: 20px;
  }
}
.attr-ad-snmp-form {
  .ant-form-item {
    margin-bottom: 0;
  }
}
</style>
