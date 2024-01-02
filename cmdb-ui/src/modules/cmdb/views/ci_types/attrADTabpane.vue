<template>
  <div :style="{ height: `${windowHeight - 156}px`, overflow: 'auto', position: 'relative' }">
    <a
      v-if="!adrIsInner"
      :style="{ position: 'absolute', right: 0, top: 0 }"
      @click="
        () => {
          $emit('openEditDrawer', currentAdr, 'edit', 'agent')
        }
      "
    >
      <a-space>
        <ops-icon type="icon-xianxing-edit" />
        <span>{{ $t('edit') }}</span>
      </a-space>
    </a>
    <div>{{ $t('alias') }}：<a-input v-model="alias" style="width:200px;" /></div>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.attributeMap') }}</div>
    <vxe-table
      v-if="adrType === 'agent'"
      ref="xTable"
      :edit-config="{ trigger: 'click', mode: 'cell' }"
      size="mini"
      stripe
      class="ops-stripe-table"
      :data="tableData"
      :style="{ width: '700px', marginBottom: '20px' }"
    >
      <vxe-colgroup :title="$t('cmdb.ciType.autoDiscovery')">
        <vxe-column field="name" :title="$t('name')"> </vxe-column>
        <vxe-column field="type" :title="$t('type')"> </vxe-column>
        <vxe-column field="desc" :title="$t('desc')"> </vxe-column>
      </vxe-colgroup>
      <vxe-colgroup :title="$t('cmdb.ciType.attributes')">
        <vxe-column field="attr" :title="$t('name')" :edit-render="{}">
          <template #default="{row}">
            {{ row.attr }}
          </template>
          <template #edit="{ row }">
            <vxe-select
              filterable
              clearable
              v-model="row.attr"
              type="text"
              :options="ciTypeAttributes"
              transfer
            ></vxe-select>
          </template>
        </vxe-column>
      </vxe-colgroup>
    </vxe-table>
    <HttpSnmpAD
      v-else
      :isEdit="true"
      ref="httpSnmpAd"
      :ruleType="adrType"
      :ruleName="adrName"
      :ciTypeAttributes="ciTypeAttributes"
      :adCITypeList="adCITypeList"
      :currentTab="adr_id"
      :style="{ marginBottom: '20px' }"
    />
    <a-form-model
      v-if="adrType === 'http'"
      :model="form2"
      :labelCol="{ span: 2 }"
      :wrapperCol="{ span: 8 }"
      :style="{ margin: '20px 0' }"
    >
      <a-form-model-item label="key">
        <a-input-password v-model="form2.key" />
      </a-form-model-item>
      <a-form-model-item label="secret">
        <a-input-password v-model="form2.secret" />
      </a-form-model-item>
    </a-form-model>
    <a-form :form="form3" v-if="adrType === 'snmp'" class="attr-ad-snmp-form">
      <a-col :span="24">
        <a-form-item :label="$t('cmdb.ciType.node')" :labelCol="{ span: 2 }" :wrapperCol="{ span: 20 }">
          <MonitorNodeSetting ref="monitorNodeSetting" :initNodes="nodes" :form="form3" />
        </a-form-item>
      </a-col>
    </a-form>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.adExecConfig') }}</div>
    <a-form-model :model="form" :labelCol="{ span: 2 }" :wrapperCol="{ span: 20 }">
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
      <a-form-model-item :label="$t('cmdb.ciType.adAutoInLib')">
        <a-switch v-model="form.auto_accept" />
      </a-form-model-item>
    </a-form-model>
    <div class="attr-ad-header">{{ $t('cmdb.ciType.adInterval') }}</div>
    <CustomRadio :radioList="radioList" v-model="interval">
      <span v-show="interval === 'interval'" slot="extra_interval">
        <a-input-number v-model="intervalValue" :min="1" /> {{ $t('seconds') }}
      </span>
    </CustomRadio>

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
import { putCITypeDiscovery } from '../../api/discovery'
import HttpSnmpAD from '../../components/httpSnmpAD'
import CMDBExprDrawer from '@/components/CMDBExprDrawer'
import MonitorNodeSetting from '@/components/MonitorNodeSetting'

export default {
  name: 'AttrADTabpane',
  components: { Vcrontab, HttpSnmpAD, CMDBExprDrawer, MonitorNodeSetting },
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
      interval: 'interval', // interval  cron
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
      alias: '',
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
      userRoles: (state) => state.user.roles,
    }),
    adrType() {
      return this.currentAdr.type
    },
    adrName() {
      return this.currentAdr.name
    },
    adrIsInner() {
      return this.currentAdr.is_inner
    },
    agentTypeRadioList() {
      const { permissions = [] } = this.userRoles
      if ((permissions.includes('cmdb_admin') || permissions.includes('admin')) && this.adrType !== 'http') {
        return [
          { value: 'all', label: this.$t('cmdb.ciType.allNodes') },
          { value: 'agent_id', label: this.$t('cmdb.ciType.specifyNodes') },
          { value: 'query_expr', label: this.$t('cmdb.ciType.selectFromCMDBTips') },
        ]
      }
      return [
        { value: 'agent_id', label: this.$t('cmdb.ciType.specifyNodes') },
        { value: 'query_expr', label: this.$t('cmdb.ciType.selectFromCMDBTips') },
      ]
    },
    radioList() {
      return [
        { value: 'interval', label: this.$t('cmdb.ciType.byInterval') },
        // { value: 'cron', label: '按cron', layout: 'vertical' },
      ]
    },
  },
  mounted() {},
  methods: {
    init() {
      const _find = this.adrList.find((item) => Number(item.id) === Number(this.adr_id))
      const _findADT = this.adCITypeList.find((item) => Number(item.id) === Number(this.currentAdt.id))
      this.alias = _findADT?.extra_option?.alias ?? ''
      if (this.adrType === 'http') {
        const { category = undefined, key = '', secret = '' } = _findADT?.extra_option ?? {}
        this.form2 = {
          key,
          secret,
        }
        this.$refs.httpSnmpAd.setCurrentCate(category)
      }
      if (this.adrType === 'snmp') {
        this.nodes = _findADT?.extra_option?.nodes ?? [
          {
            id: uuidv4(),
            ip: '',
            community: '',
            version: '',
          },
        ]
        this.$nextTick(() => {
          this.$refs.monitorNodeSetting.initNodesFunc()
          this.$nextTick(() => {
            this.$refs.monitorNodeSetting.setNodeField()
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
      if (_findADT.interval || (!_findADT.interval && !_findADT.cron)) {
        this.interval = 'interval'
        this.intervalValue = _findADT.interval || ''
      } else {
        this.interval = 'cron'
        this.cron = `0 ${_findADT.cron}`
      }
    },
    getAttrNameByAttrName(attrName) {
      const _find = this.ciTypeAttributes.find((item) => item.name === attrName)
      return _find?.alias || _find?.name || ''
    },
    crontabFill(cron) {
      this.cron = cron
    },
    handleSave() {
      const { currentAdt, alias } = this
      let params
      if (this.adrType === 'http') {
        params = {
          extra_option: {
            ...this.form2,
            category: this.$refs.httpSnmpAd.currentCate,
          },
        }
      }
      if (this.adrType === 'snmp') {
        params = {
          extra_option: { nodes: this.$refs.monitorNodeSetting?.getNodeValue() ?? [] },
        }
      }
      if (this.adrType === 'agent') {
        const $table = this.$refs.xTable
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
      if (this.interval === 'cron') {
        this.$refs.cronTab.submitFill()
      }
      params = {
        ...params,
        ...this.form,
        type_id: this.CITypeId,
        adr_id: currentAdt.adr_id,
        interval: this.interval === 'interval' ? this.intervalValue : null,
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
      if (params.extra_option) {
        params.extra_option.alias = alias
      } else {
        params.extra_option = {}
        params.extra_option.alias = alias
      }
      putCITypeDiscovery(currentAdt.id, params).then((res) => {
        this.$message.success(this.$t('saveSuccess'))
        this.$emit('handleSave')
      })
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
  },
}
</script>

<style lang="less">
.attr-ad-snmp-form {
  .ant-form-item {
    margin-bottom: 0;
  }
}
</style>
