<template>
  <a-modal
    :visible="visible"
    :width="700"
    :title="$t('cmdb.ipam.addressAssign')"
    :confirmLoading="confirmLoading"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="assignFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      class="assign-form"
    >
      <a-form-model-item
        label="IP"
      >
        <span class="assign-form-ip" >{{ ipList.join(', ') }}</span>
      </a-form-model-item>
      <a-form-model-item
        v-for="(item) in formList"
        :key="item.name"
        :label="item.alias || item.name"
        :prop="item.name"
      >
        <CIReferenceAttr
          v-if="item.is_reference"
          :referenceTypeId="item.reference_type_id"
          :isList="item.is_list"
          :referenceShowAttrName="item.showAttrName"
          :initSelectOption="getInitReferenceSelectOption(item)"
          v-model="form[item.name]"
        />
        <a-select
          v-else-if="item.is_choice"
          :mode="item.is_list ? 'multiple' : 'default'"
          showSearch
          allowClear
          v-model="form[item.name]"
        >
          <a-icon slot="suffixIcon" type="caret-down" />
          <a-select-option
            v-for="(choiceItem, choiceIndex) in item.selectOption"
            :key="choiceIndex"
            :value="choiceItem.value"
          >
            {{ choiceItem.label }}
          </a-select-option>
        </a-select>
        <a-switch
          v-else-if="item.is_bool"
          v-model="form[item.name]"
        />
        <a-input
          v-else
          :placeholder="$t('placeholder1')"
          v-model="form[item.name]"
        />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import _ from 'lodash'
import { postIPAMAddress } from '@/modules/cmdb/api/ipam.js'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'

import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'AssignForm',
  components: {
    CIReferenceAttr
  },
  props: {
    attrList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      visible: false,
      ipData: {},
      ipList: [],
      nodeId: -1,
      formList: [],
      form: {},
      formRules: {},
      confirmLoading: false,
      isBatch: false
    }
  },
  methods: {
    async open({
      ipList = [],
      ipData = null,
      nodeId,
    }) {
      this.isBatch = ipList.length !== 0
      this.ipList = ipList.length ? _.cloneDeep(ipList) : [ipData?.ip ?? '']
      this.ipData = ipData || {}
      this.nodeId = nodeId || -1
      this.visible = true

      const form = {}
      const formRules = {}
      let formList = []
      let attrList = _.cloneDeep(this.attrList)
      attrList = attrList?.filter?.((attr) => !attr.sys_computed && !attr.is_computed) || []

      if (ipData?.assign_status === 1) {
        ipData.assign_status = undefined
      }

      if (attrList.length) {
        _.remove(attrList, (item) => {
          return ['subnet_mask', 'gateway', 'name', 'mac_address', 'is_used', 'ip', 'ipam_address_id'].includes(item.name)
        })

        const assingStatusIndex = attrList.findIndex((attr) => attr.name === 'assign_status')
        if (assingStatusIndex > 0) {
          const assign_status = attrList.splice(assingStatusIndex, 1)
          attrList.unshift(...assign_status)
        }

        attrList.forEach((attr) => {
          form[attr.name] = ipData?.[attr.name] ?? undefined

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
          formList.push(attr)

          if (attr.is_required) {
            formRules[attr.name] = [
              {
                required: true, message: attr?.is_choice ? this.$t('placeholder2') : this.$t('placeholder1')
              }
            ]
          }
        })
      }

      formList = await this.handleReferenceAttr(formList, form)

      this.form = form
      this.formList = formList
      this.formRules = formRules
    },

    async handleReferenceAttr(formList, ci) {
      const map = {}
      formList.forEach((attr) => {
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
      if (!Object.keys(map).length) {
        return formList
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

      formList.forEach((attr) => {
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

      return formList
    },

    handleCancel() {
      this.visible = false
      this.ipData = {}
      this.nodeId = -1
      this.form = {}
      this.formRules = {}
      this.formList = []
      this.confirmLoading = false
      this.isBatch = false

      this.$refs.assignFormRef.clearValidate()
    },

    handleOk() {
      this.$refs.assignFormRef.validate(async (valid) => {
        if (!valid) {
          return
        }

        this.confirmLoading = true

        if (!this.isBatch) {
          await postIPAMAddress({
            ips: this.ipList,
            parent_id: this.nodeId,
            ...this.form,
            subnet_mask: this?.ipData?.subnet_mask ?? undefined,
            gateway: this?.ipData?.gateway ?? undefined
          })

          this.$emit('ok')
        } else {
          const ipChunk = _.chunk(this.ipList, 5)
          const paramsList = ipChunk.map((ips) => ({
            ips,
            parent_id: this.nodeId,
            ...this.form,
            subnet_mask: this?.ipData?.subnet_mask ?? undefined,
            gateway: this?.ipData?.gateway ?? undefined
          }))
          this.$emit('batchAssign', {
            paramsList,
            ipList: this.ipList
          })
        }

        this.handleCancel()
        this.confirmLoading = false
      })
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
.assign-form {
  padding-right: 12px;
  max-height: 400px;
  overflow-y: auto;
  overflow-x: hidden;

  &-ip {
    max-height: 100px;
    overflow-y: auto;
    overflow-x: hidden;
    display: block;
  }
}
</style>
