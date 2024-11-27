<template>
  <a-modal
    :visible="visible"
    :width="700"
    :title="$t(modalTitle)"
    :confirmLoading="confirmLoading"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="dcimFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      class="dcim-form"
    >
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

        <a-input-number
          v-model="form[item.name]"
          class="dcim-form-input"
          v-else-if="(item.value_type === '0' || item.value_type === '1') && !item.is_list"
        />

        <a-date-picker
          v-else-if="(item.value_type === '4' || item.value_type === '3') && !item.is_list"
          v-model="form[item.name]"
          class="dcim-form-input"
          :format="item.value_type === '4' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
          :valueFormat="item.value_type === '4' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
          :showTime="item.value_type === '4' ? false : { format: 'HH:mm:ss' }"
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
import { postDCIM, putDCIM } from '@/modules/cmdb/api/dcim.js'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'
import { DCIM_TYPE } from '../constants'

import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'DCIMForm',
  components: {
    CIReferenceAttr
  },
  props: {
    allAttrList: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      visible: false,
      nodeId: null,
      parentId: null,
      dcimType: '',

      formList: [],
      form: {},
      formRules: {},

      confirmLoading: false,
    }
  },
  computed: {
    modalTitle() {
      switch (this.dcimType) {
        case DCIM_TYPE.REGION:
          return this.nodeId ? 'cmdb.dcim.editRegion' : 'cmdb.dcim.addRegion'
        case DCIM_TYPE.IDC:
          return this.nodeId ? 'cmdb.dcim.editIDC' : 'cmdb.dcim.addIDC'
        case DCIM_TYPE.SERVER_ROOM:
          return this.nodeId ? 'cmdb.dcim.editServerRoom' : 'cmdb.dcim.addServerRoom'
        case DCIM_TYPE.RACK:
          return this.nodeId ? 'cmdb.dcim.editRack' : 'cmdb.dcim.addRack'
        default:
          return ''
      }
    }
  },
  methods: {
    async open({
      nodeId = null,
      parentId = null,
      dcimType = ''
    }) {
      this.nodeId = nodeId

      let nodeData = {}
      if (nodeId) {
        const res = await searchCI({
          q: `_id:${nodeId}`,
          count: 9999
        })
        nodeData = res?.result?.[0] || {}
      }

      this.parentId = parentId
      this.dcimType = dcimType
      this.visible = true

      const form = {}
      const formRules = {}
      let formList = []

      let attrList = _.cloneDeep(this.allAttrList?.[dcimType]?.attributes)
      attrList = attrList?.filter?.((attr) => !attr.sys_computed && !attr.is_computed) || []

      if (attrList.length) {
        attrList.forEach((attr) => {
          let value = nodeData?.[attr.name] ?? attr?.default?.default ?? undefined

          if (
            Array.isArray(value) &&
            ['0', '1', '2', '9'].includes(attr.value_type)
          ) {
            value = value.join(',')
          }
          form[attr.name] = value

          if (attr?.is_choice) {
            const choice_value = attr?.choice_value || []
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
      this.nodeId = null
      this.parentId = null
      this.dcimType = ''
      this.form = {}
      this.formRules = {}
      this.formList = []
      this.confirmLoading = false

      this.$refs.dcimFormRef.clearValidate()
    },

    handleOk() {
      this.$refs.dcimFormRef.validate(async (valid) => {
        if (!valid) {
          return
        }
        this.confirmLoading = true

        try {
          if (this.nodeId) {
            await putDCIM(
              this.dcimType,
              this.nodeId,
              {
                ...this.form,
                parent_id: Number(this.parentId)
              }
            )
          } else {
            await postDCIM(
              this.dcimType,
              {
                ...this.form,
                parent_id: Number(this.parentId)
              }
            )
          }
          this.$emit('ok', {
            dcimType: this.dcimType,
            editType: this.nodeId ? 'edit' : 'create'
          })
          this.handleCancel()
        } catch (error) {
          console.log('submit fail', error)
        }

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
.dcim-form {
  padding-right: 12px;
  max-height: 400px;
  overflow-y: auto;
  overflow-x: hidden;

  &-input {
    width: 100%;
  }
}
</style>
