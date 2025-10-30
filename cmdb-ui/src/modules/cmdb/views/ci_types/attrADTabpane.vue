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
    <div class="attr-ad-header attr-ad-header_between">
      <span>
        {{ $t('cmdb.ciType.attributeMap') }}
        <a-tooltip :title="$t('cmdb.ciType.attributeMapHint')">
          <a-icon type="question-circle" style="margin-left: 4px; color: #999; font-size: 14px; cursor: help;" />
        </a-tooltip>
      </span>
      <div class="attr-ad-open">
        <span class="attr-ad-open-label">{{ $t('cmdb.ciType.enable') }}</span>
        <a-switch v-model="form.enabled" v-if="isClient" />
        <a-popconfirm
          v-else
          :title="$t('cmdb.ciType.enableTip')"
          :ok-text="$t('confirm')"
          :cancel-text="$t('cancel')"
          @confirm="changeEnabled"
        >
          <a-switch :checked="form.enabled" />
        </a-popconfirm>
      </div>
    </div>
    <div class="attr-ad-attributemap-main">
      <AttrMapTable
        v-if="adrType === DISCOVERY_CATEGORY_TYPE.AGENT"
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
        :currentAdt="currentAdt"
        :style="{ marginBottom: '20px' }"
      />
    </div>
    <template v-if="adrType === DISCOVERY_CATEGORY_TYPE.SNMP">
      <div class="attr-ad-header">{{ $t('cmdb.ciType.scanningParameter') }}</div>
      <div class="attr-ad-form attr-ad-snmp-form">
        <div class="attr-ad-snmp-form-title">
          {{ $t('cmdb.ciType.SNMPConfiguration') }}
        </div>
        <NodeSetting ref="nodeSetting" />
        <SNMPConfig v-model="SNMPScanningConfigForm" />

        <div class="attr-ad-snmp-form-title">
          {{ $t('cmdb.ciType.scanningConfiguration') }}
        </div>
        <SNMPScanningConfig v-model="SNMPScanningConfigForm" />
        <CIDRTags v-model="SNMPScanningConfigForm.cidr" />
      </div>
    </template>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.adExecConfig') }}</div>
    <a-form-model
      :model="form"
      :labelCol="labelCol"
      labelAlign="right"
      :wrapperCol="{ span: 14 }"
      class="attr-ad-form"
    >
      <a-form-model-item :required="true" :label="$t('cmdb.ciType.adExecTarget')">
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
        <div class="ant-form-explain" v-if="agent_type === 'all'">{{ $t('cmdb.ciType.allNodesTip') }}</div>
        <div class="ant-form-explain" v-if="agent_type === 'query_expr'">{{ $t('cmdb.ciType.queryExprTip') }}</div>
        <div class="ant-form-explain" v-if="agent_type === 'master'">{{ $t('cmdb.ciType.masterNodeTip') }}</div>
      </a-form-model-item>
      <a-form-model-item
        :labelCol="labelCol"
        :label="$t('cmdb.ciType.adAutoInLib')"
        :extra="$t('cmdb.ciType.adAutoInLibTip')"
      >
        <a-switch v-model="form.auto_accept" />
        <div class="ant-form-explain">{{ $t('cmdb.ciType.adAutoInLibTip') }}</div>
      </a-form-model-item>
      <a-form-model-item
        :labelCol="labelCol"
        :wrapperCol="{ span: 6 }"
        :label="$t('cmdb.ciType.adInterval')"
        :required="true"
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
    <template v-if="adrType === DISCOVERY_CATEGORY_TYPE.HTTP">
      <template v-if="isPrivateCloud">
        <template v-if="privateCloudName === PRIVATE_CLOUD_NAME.VCenter">
          <div class="attr-ad-header">{{ $t('cmdb.ciType.privateCloud') }}</div>
          <VcenterForm
            v-model="privateCloudForm"
            ref="httpForm"
          />
        </template>
      </template>

      <template v-else>
        <div class="attr-ad-header">{{ $t('cmdb.ciType.cloudAccessKey') }}</div>
        <!-- <div class="public-cloud-info">{{ $t('cmdb.ciType.cloudAccessKeyTip') }}</div> -->
        <PublicCloud
          v-model="publicCloudForm"
          ref="httpForm"
        />
      </template>
    </template>

    <template v-if="adrType === DISCOVERY_CATEGORY_TYPE.COMPONENT">
      <div class="attr-ad-header">{{ $t('cmdb.ciType.portScanConfig') }}</div>
      <PortScanConfig v-model="portScanConfigForm" />
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
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import { mapState } from 'vuex'
import Vcrontab from '@/components/Crontab'
import { putCITypeDiscovery, postCITypeDiscovery } from '../../api/discovery'
import { DISCOVERY_CATEGORY_TYPE, PRIVATE_CLOUD_NAME } from '@/modules/cmdb/views/discovery/constants.js'
import { TAB_KEY } from './attrAD/constants.js'

import HttpSnmpAD from '../../components/httpSnmpAD'
import AttrMapTable from '@/modules/cmdb/components/attrMapTable/index.vue'
import CMDBExprDrawer from '@/components/CMDBExprDrawer'
import NodeSetting from './attrAD/nodeSetting/index.vue'
import AttrADTest from './attrADTest.vue'
import { Popover } from 'element-ui'
import VcenterForm from './attrAD/privateCloud/vcenterForm.vue'
import PublicCloud from './attrAD/publicCloud/index.vue'
import PortScanConfig from './attrAD/portScanConfig/index.vue'
import CIDRTags from './attrAD/cidrTags/index.vue'
import SNMPScanningConfig from './attrAD/SNMPScanningConfig/index.vue'
import SNMPConfig from './attrAD/SNMPConfig/index.vue'

export default {
  name: 'AttrADTabpane',
  components: {
    Vcrontab,
    HttpSnmpAD,
    CMDBExprDrawer,
    NodeSetting,
    AttrMapTable,
    AttrADTest,
    ElPopover: Popover,
    VcenterForm,
    PublicCloud,
    PortScanConfig,
    CIDRTags,
    SNMPScanningConfig,
    SNMPConfig
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
        enabled: true,
      },
      publicCloudForm: {
        key: '',
        secret: '',
        _reference: '',
        tabActive: TAB_KEY.CUSTOM,
      },
      privateCloudForm: {
        host: '',
        account: '',
        password: '',
        // insecure: false,
        vcenterName: '',
        _reference: '',
        tabActive: TAB_KEY.CUSTOM,
      },
      portScanConfigForm: {
        cidr: '',
        ports: '',
        enable_cidr: '',
      },
      cron: '',
      cronVisible: false,
      intervalValue: 3,
      agent_type: 'agent_id',
      nodeSettingForm: this.$form.createForm(this, { name: 'snmp_form' }),
      uniqueKey: '',
      isPrivateCloud: false,
      privateCloudName: '',
      PRIVATE_CLOUD_NAME,
      DISCOVERY_CATEGORY_TYPE,
      isClient: false, // 是否前端新增临时数据
      SNMPScanningConfigForm: {
        version: '2c',
        community: 'public',
        timeout: 5,
        retries: 3,
        initial_node: '',
        recursive_scan: true,
        max_depth: 5,
        cidr: []
      }, // snmp scanning config form data
    }
  },
  provide() {
    return {
      provide_labelCol: () => {
        return this.labelCol
      },
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
      return this?.currentAdr?.option?.en || this.currentAdr?.name || ''
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
      if ((permissions.includes('cmdb_admin') || permissions.includes('admin')) && this.adrType === DISCOVERY_CATEGORY_TYPE.AGENT) {
        radios.unshift({ value: 'all', label: this.$t('cmdb.ciType.allNodes') })
      }

      if (this.adrType !== DISCOVERY_CATEGORY_TYPE.AGENTv || this?.currentAdr?.is_plugin) {
        radios.unshift({ value: 'master', label: this.$t('cmdb.ciType.masterNode') })
      }

      return radios
    },
    labelCol() {
      const isEn = this.$i18n.locale === 'en'
      return {
        xl: {
          span: isEn ? 4 : 3
        },
        lg: {
          span: isEn ? 5 : 4
        },
        sm: {
          span: isEn ? 6 : 5
        }
      }
    }
  },
  mounted() {},
  methods: {
    init() {
      const _find = this.adrList.find((item) => Number(item.id) === Number(this.adr_id))
      const _findADT = this.adCITypeList.find((item) => Number(item.id) === Number(this.currentAdt.id))
      this.uniqueKey = _find?.unique_key ?? ''
      this.isClient = _findADT?.isClient ?? false

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.HTTP) {
        const {
          category = undefined,
          key = '',
          secret = '',
          host = '',
          account = '',
          password = '',
          // insecure = false,
          vcenterName = '',
          _reference = ''
        } = _findADT?.extra_option ?? {}

        if (_find?.option?.category === 'private_cloud') {
          this.isPrivateCloud = true
          this.privateCloudName = _find?.option?.en || ''

          switch (this.privateCloudName) {
            case PRIVATE_CLOUD_NAME.VCenter:
              this.privateCloudForm = {
                host,
                account,
                password,
                // insecure,
                vcenterName,
                _reference,
                tabActive: _reference ? TAB_KEY.CONFIG : TAB_KEY.CUSTOM
              }
              break
            default:
              break
          }
        } else {
          this.isPrivateCloud = false
          this.publicCloudForm = {
            key,
            secret,
            _reference,
            tabActive: _reference ? TAB_KEY.CONFIG : TAB_KEY.CUSTOM
          }
        }

        this.$refs.httpSnmpAd.setCurrentCate(category)
        this.$nextTick(() => {
          this.$refs.httpForm.init(this.adr_id)
        })
      }

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.COMPONENT) {
        const {
          cidr = '',
          ports = '',
          enable_cidr = '',
        } = _findADT?.extra_option ?? {}
        this.portScanConfigForm = {
          cidr,
          ports,
          enable_cidr
        }
      }

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.SNMP) {
        const extra_option = _findADT?.extra_option ?? {}
        const {
          nodes,
          cidr = []
        } = extra_option

        const initializeNodes = nodes?.length ? nodes : [
          {
            id: uuidv4(),
            ip: '',
            community: 'public',
            version: '',
          },
        ]
        this.$nextTick(() => {
          this.$refs.nodeSetting.initNodesFunc(initializeNodes)
        })

        let cidrList = []
        if (Array.isArray(cidr) && cidr?.length) {
          cidrList = cidr.map((v) => {
            return {
              id: uuidv4(),
              value: v?.value ? v.value : v
            }
          })
        }
        this.SNMPScanningConfigForm = {
          version: extra_option?.version ?? '2c',
          community: extra_option?.community ?? 'public',
          timeout: extra_option?.timeout ?? 5,
          retries: extra_option?.retries ?? 3,
          initial_node: extra_option?.initial_node ?? '',
          recursive_scan: extra_option?.recursive_scan ?? true,
          max_depth: extra_option?.max_depth ?? 5,
          cidr: cidrList
        }
      }
      if (this.adrType === DISCOVERY_CATEGORY_TYPE.AGENT) {
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
        agent_id: _findADT?.agent_id && _findADT?.agent_id !== '0x0000' ? _findADT.agent_id : '',
        query_expr: _findADT.query_expr || '',
        enabled: _findADT?.enabled ?? true,
      }

      const allMachineIndex = this.agentTypeRadioList.findIndex((item) => item.value === 'all')

      if (_findADT.query_expr) {
        this.agent_type = 'query_expr'
      } else if (_findADT.agent_id) {
        this.agent_type = _findADT.agent_id === '0x0000' ? 'master' : 'agent_id'
      } else if (_findADT.agent_id === '' && allMachineIndex !== -1) {
        this.agent_type = 'all'
      } else {
        this.agent_type = this.agentTypeRadioList[0].value
      }

      this.cron = _findADT?.cron || ''
    },

    crontabFill(cron) {
      this.cron = cron
    },
    handleSave() {
      const { currentAdt } = this
      let params

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.HTTP) {
        const { isError, data: cloudOption } = this.validateHTTPForm()
        if (isError) {
          return
        }

        params = {
          extra_option: {
            ...cloudOption,
            category: this.$refs.httpSnmpAd.currentCate,
          },
        }
      }

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.COMPONENT) {
        const portScanConfigForm = _.omitBy(this.portScanConfigForm, _.isEmpty) || {}
        params = {
          extra_option: {
            ...portScanConfigForm,
          },
        }
      }

      if (this.adrType === DISCOVERY_CATEGORY_TYPE.SNMP) {
        const {
          cidr,
          ...otherConfigForm
        } = this.SNMPScanningConfigForm
        const nodes = this.$refs.nodeSetting?.getNodeValue() ?? []

        params = {
          extra_option: {
            ...otherConfigForm,
            nodes,
            cidr: cidr?.map((item) => item.value) || []
          },
        }

        if (
          !otherConfigForm?.recursive_scan &&
          nodes?.some((item) => !item?.ip)
        ) {
          this.$message.error(this.$t('cmdb.ciType.recursiveTip'))
          return
        }
      }
      if (this.adrType === DISCOVERY_CATEGORY_TYPE.AGENT) {
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
        cron: this.cron,
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

      if (this.agent_type === 'master') {
        params.agent_id = '0x0000'
      }

      if (!this.cron) {
        this.$message.error(this.$t('cmdb.ciType.cronRequiredTip'))
        return
      }

      if (currentAdt?.extra_option) {
        params.extra_option = {
          ...(currentAdt?.extra_option || {}),
          ...(params?.extra_option || {})
        }
      }

      // 去除合并后的旧配置
      if (params.extra_option) {
        params.extra_option = this.handleOldExtraOption(params.extra_option)
      }

      if (currentAdt?.isClient) {
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

    /**
     * HTTP 表单校验
     * 公有云 私有云
     */
    validateHTTPForm() {
      let isError = false
      let data = {}

      const formData = this?.[this.isPrivateCloud ? 'privateCloudForm' : 'publicCloudForm']
      if (formData.tabActive === TAB_KEY.CONFIG) {
        if (!formData._reference) {
          isError = true
          this.$message.error(this.$t('cmdb.ad.configErrTip'))
        }

        data._reference = formData._reference
        if (this.privateCloudName === PRIVATE_CLOUD_NAME.VCenter) {
          data.vcenterName = formData.vcenterName
        }

        return {
          isError,
          data
        }
      }

      if (this.isPrivateCloud) {
        if (this.privateCloudName === PRIVATE_CLOUD_NAME.VCenter) {
          data = _.pick(this.privateCloudForm, ['host', 'account', 'password', 'vcenterName'])
          const vcenterErros = {
            'host': `${this.$t('placeholder1')} ${this.$t('cmdb.ciType.host')}`,
            'account': `${this.$t('placeholder1')} ${this.$t('cmdb.ciType.account')}`,
            'password': `${this.$t('placeholder1')} ${this.$t('cmdb.ciType.password')}`
          }
          const findError = Object.keys(this.privateCloudForm).find((key) => !this.privateCloudForm[key] && vcenterErros[key])
          if (findError) {
            isError = true
            this.$message.error(this.$t(vcenterErros[findError]))
          }
        }
      } else {
        data = _.pick(this.publicCloudForm, ['key', 'secret'])
        const publicCloudErros = {
          'key': `${this.$t('placeholder1')} key`,
          'secret': `${this.$t('placeholder1')} secret`
        }
        const findError = Object.keys(this.publicCloudForm).find((key) => !this.publicCloudForm[key] && publicCloudErros[key])
        if (findError) {
          isError = true
          this.$message.error(this.$t(publicCloudErros[findError]))
        }
      }

      return {
        isError,
        data
      }
    },

    /**
     * 去除多余旧配置
     */
    handleOldExtraOption(option) {
      let extra_option = _.cloneDeep(option)

      // VCenter 旧配置
      if (extra_option?.insecure) {
        Reflect.deleteProperty(extra_option, 'insecure')
      }

      // 根据 HTTP 选项去除多余属性
      const formData = this?.[this.isPrivateCloud ? 'privateCloudForm' : 'publicCloudForm']
      switch (formData.tabActive) {
        case TAB_KEY.CUSTOM:
          Reflect.deleteProperty(extra_option, '_reference')
          break
        case TAB_KEY.CONFIG:
          extra_option = _.omit(extra_option, ['host', 'account', 'password', 'key', 'secret'])
          break
        default:
          break
      }

      return extra_option
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
    changeEnabled() {
      if (!this.isClient) {
        putCITypeDiscovery(this.currentAdt.id, {
          enabled: !this.form.enabled
        }).then((res) => {
          this.form.enabled = !this.form.enabled
          this.$message.success(this.$t('saveSuccess'))
          this.$emit('handleSave', res.id)
        })
      }
    }
  },
}
</script>

<style lang="less" scoped>
.attr-ad-tab-pane {
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;

  .attr-ad-header_between {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
  }

  .attr-ad-open {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0px 20px;

    &-label {
      font-size: 14px;
      font-weight: 600;
      margin-right: 6px;
    }
  }

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
  &-title {
    font-size: 16px;
    color: #000000;
    margin-bottom: 12px;
  }

  /deep/ .ant-input-number {
    width: 100%;
  }

  /deep/ .ant-form-extra {
    font-size: 12px;
  }
}
</style>
