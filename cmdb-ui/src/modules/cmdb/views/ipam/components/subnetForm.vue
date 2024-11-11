<template>
  <CustomDrawer
    width="800px"
    :title="$t(actionType === 'edit' ? 'cmdb.ipam.editSubnet' : 'cmdb.ipam.addSubnet')"
    :visible="visible"
    :bodyStyle="{ height: 'calc(-108px + 100vh)' }"
    @close="handleClose"
  >
    <a-form-model
      ref="subnetFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 4 }"
      :wrapper-col="{ span: 17 }"
    >
      <div
        v-for="(group, groupIndex) in basicFormGroup"
        :key="groupIndex"
      >
        <div class="subnet-form-title">
          {{ group.name }}
        </div>

        <a-form-model-item
          v-for="(attr) in group.attributes"
          :key="attr.name"
          :label="attr.alias || attr.name"
          :prop="attr.name"
        >
          <CIReferenceAttr
            v-if="attr.is_reference"
            :referenceTypeId="attr.reference_type_id"
            :isList="attr.is_list"
            :referenceShowAttrName="attr.showAttrName"
            :initSelectOption="getInitReferenceSelectOption(attr)"
            v-model="form[attr.name]"
          />
          <a-select
            v-else-if="attr.is_choice"
            v-model="form[attr.name]"
            :mode="attr.is_list ? 'multiple' : 'default'"
            showSearch
            allowClear
          >
            <a-icon slot="suffixIcon" type="caret-down" />
            <a-select-option
              v-for="(choiceItem, choiceIndex) in attr.selectOption"
              :key="choiceIndex"
              :value="choiceItem.value"
            >
              {{ choiceItem.label }}
            </a-select-option>
          </a-select>
          <a-switch
            v-else-if="attr.is_bool"
            v-model="form[attr.name]"
          />
          <a-input
            v-else
            :placeholder="$t('placeholder1')"
            v-model="form[attr.name]"
          />
        </a-form-model-item>
      </div>

      <div class="subnet-form-title">
        <a-row>
          <a-col :span="4">
            {{ $t('cmdb.ipam.scanRule') }}
          </a-col>
          <a-switch v-model="form.scan_enabled" />
        </a-row>
      </div>

      <template v-if="form.scan_enabled">
        <a-form-model-item
          :label="$t('cmdb.ipam.adExecTarget')"
        >
          <CustomRadio
            v-model="agentType"
            :radioList="agentTypeRadioList"
          >
            <span
              v-show="agentType === 'master'"
              slot="extra_master"
              class="subnet-form-agent-tip"
            >
              {{ $t('cmdb.ipam.masterMachineTip') }}
            </span>
            <a-input
              v-show="agentType === 'agent_id'"
              slot="extra_agent_id"
              :style="{ width: '300px' }"
              :placeholder="$t('cmdb.ipam.oneagentIdTips')"
              v-model="agentId"
            />
          </CustomRadio>
        </a-form-model-item>

        <a-form-model-item
          :label="$t('cmdb.ipam.adInterval')"
        >
          <el-popover
            v-model="cronVisible"
            trigger="click"
          >
            <template slot>
              <Vcrontab
                ref="cronTab"
                :hideComponent="['second', 'year']"
                :expression="form.cron"
                :hasFooter="true"
                @fill="crontabFill"
                @hide="hideCron"
              ></Vcrontab>
            </template>
            <a-input
              v-model="form.cron"
              slot="reference"
              :placeholder="$t('cmdb.ipam.cronTips')"
            />
          </el-popover>
        </a-form-model-item>
      </template>
    </a-form-model>

    <div class="custom-drawer-bottom-action">
      <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
      <a-button @click="handleSubmit" type="primary">{{ $t('save') }}</a-button>
    </div>
  </CustomDrawer>
</template>

<script>
import {
  postIPAMSubnet,
  getIPAMSubnetById,
  putIPAMSubnet
} from '@/modules/cmdb/api/ipam.js'
import { getCITypeGroupById, getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'

import Vcrontab from '@/components/Crontab'
import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'SubnetForm',
  components: {
    Vcrontab,
    CIReferenceAttr
  },
  props: {
    subnetCIType: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      nodeId: null,
      parentId: null,
      actionType: 'create',
      visible: false,
      form: {
        scan_enabled: true,
        cron: ''
      },
      basicFormGroup: [],
      formRules: {},

      agentTypeRadioList: [
        { value: 'master', label: this.$t('cmdb.ipam.masterMachine') },
        { value: 'agent_id', label: this.$t('cmdb.ipam.specifyMachine') }
      ],
      agentType: 'master',
      agentId: '',

      cronVisible: false
    }
  },
  methods: {
    async open(nodeId, type, parentId) {
      this.visible = true
      this.actionType = type
      this.nodeId = nodeId
      this.parentId = parentId || null

      let nodeData = {}
      if (type === 'edit') {
        nodeData = await getIPAMSubnetById(nodeId)
        this.form.scan_enabled = !!nodeData.scan_enabled

        if (nodeData?.scan_enabled) {
          this.form.cron = nodeData.cron

          if (nodeData.agent_id) {
            if (nodeData.agent_id === '0x0000') {
              this.agentType = 'master'
            } else {
              this.agentType = 'agent_id'
              this.agentId = nodeData.agent_id
            }
          }
        }
      }

      // const res = await getCITypeAttributesById(SUB_NET_CITYPE_NAME)
      // const attributes = res?.attributes || []

      const groupAttr = await getCITypeGroupById(this.subnetCIType.id)
      const form = {
        ...this.form
      }
      const formRules = {}

      let basicFormGroup = []
      groupAttr.map((group) => {
        group.attributes = group?.attributes?.filter?.((attr) => !attr.sys_computed && !attr.is_computed) || []
        if (group.attributes.length) {
          group.attributes.forEach((attr) => {
            form[attr.name] = nodeData?.[attr.name] ?? undefined

            if (attr?.is_choice) {
              let choice_value = attr?.choice_value || []
              if (attr.name === 'assign_status') {
                choice_value = choice_value.filter((item) => item?.[0] !== 1)
              }

              attr.selectOption = choice_value.map((item) => {
                return {
                  label: item?.[1]?.label || item?.[0] || '',
                  value: item?.[0]
                }
              })
            }

            if (attr.is_required) {
              formRules[attr.name] = [
                {
                  required: true, message: this.$t('placeholder1')
                }
              ]
            }
          })

          basicFormGroup.push({
            name: group.name,
            attributes: group.attributes
          })
        }
      })

      basicFormGroup = await this.handleReferenceAttr(basicFormGroup, form)

      this.form = form
      this.$set(this, 'basicFormGroup', basicFormGroup)
      this.formRules = formRules
    },

    async handleReferenceAttr(basicFormGroup, ci) {
      const map = {}
      basicFormGroup.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id && ci[attr.name]) {
            const ids = Array.isArray(ci[attr.name]) ? ci[attr.name] : ci[attr.name] ? [ci[attr.name]] : []
            if (ids.length) {
              if (!map?.[attr.reference_type_id]) {
                map[attr.reference_type_id] = {}
              }
              ids.forEach((id) => {
                map[attr.reference_type_id][id] = {}
              })
            }
          }
        })
      })
      if (!Object.keys(map).length) {
        return basicFormGroup
      }

      const ciTypesRes = await getCITypes({
        type_ids: Object.keys(map).join(',')
      })
      const showAttrNameMap = {}
      ciTypesRes.ci_types.forEach((ciType) => {
        showAttrNameMap[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      const ciNameMap = {}
      allRes.forEach((res) => {
        res.result.forEach((item) => {
          ciNameMap[item._id] = item
        })
      })

      basicFormGroup.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            attr.showAttrName = showAttrNameMap?.[attr?.reference_type_id] || ''

            const referenceShowAttrNameMap = {}
            const referenceCIIds = ci[attr.name];
            (Array.isArray(referenceCIIds) ? referenceCIIds : referenceCIIds ? [referenceCIIds] : []).forEach((id) => {
              referenceShowAttrNameMap[id] = ciNameMap?.[id]?.[attr.showAttrName] ?? id
            })
            attr.referenceShowAttrNameMap = referenceShowAttrNameMap
          }
        })
      })

      return basicFormGroup
    },

    handleClose() {
      this.form = {
        scan_enabled: true,
        cron: ''
      }
      this.basicFormGroup = []
      this.formRules = {}
      this.agentType = 'master'
      this.agentId = ''
      this.cronVisible = false
      this.nodeId = null
      this.parentId = null
      this.actionType = 'create'

      this.$refs.subnetFormRef.clearValidate()

      this.visible = false
    },

    handleSubmit() {
      this.$refs.subnetFormRef.validate(async (valid) => {
        if (!valid || !this.validateScan()) {
          return
        }

        const { cron, ...otherParams } = this.form
        const params = {
          ...otherParams
        }

        if (this.form.scan_enabled) {
          params.cron = cron

          switch (this.agentType) {
            case 'master':
              params.agent_id = '0x0000'
              break
            case 'agent_id':
              params.agent_id = this.agentId
              break
            default:
              break
          }
        }

        if (this.actionType === 'edit') {
          if (this.parentId) {
            params.parent_id = this.parentId
          }
          await putIPAMSubnet(this.nodeId, params)
          this.$message.success(this.$t('editSuccess'))
        } else {
          params.parent_id = this.nodeId
          await postIPAMSubnet(params)
          this.$message.success(this.$t('addSuccess'))
        }

        this.$emit('ok')
        this.handleClose()
      })
    },

    validateScan() {
      if (this.form.scan_enabled) {
        switch (this.agentType) {
          case 'agent_id':
            if (!this.agentId) {
              this.$message.error(this.$t('cmdb.ipam.specifyMachineTips'))
              return false
            }
            break
          default:
            break
        }

        if (!this.form.cron) {
          this.$message.error(this.$t('cmdb.ipam.cronRequiredTip'))
          return false
        }
      }

      return true
    },

    handleOpenCmdb() {
      this.$refs.cmdbDrawer.open()
    },

    crontabFill(cron) {
      this.form.cron = cron
    },

    hideCron() {
      this.cronVisible = false
    },

    getInitReferenceSelectOption(attr) {
      const option = Object.keys(attr?.referenceShowAttrNameMap || {}).map((key) => {
        return {
          key: Number(key),
          title: attr?.referenceShowAttrNameMap?.[Number(key)] ?? ''
        }
      })
      return option
    }
  }
}
</script>

<style lang="less" scoped>
.subnet-form-title {
  font-size: 14px;
  font-weight: 700;
  color: #000000;
  margin-bottom: 20px;
}

.subnet-form-agent-tip {
  font-size: 12px;
  color: #86909c;
  line-height: 14px;
}
</style>
