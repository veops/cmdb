<template>
  <!-- v-decorator="[ item.name, { rules: [ { required: item.is_required ? true: false } ] } ]" -->
  <a-drawer
    :title="title + CIType.alias"
    width="500"
    @close="() => { visible = false; $emit('refresh', true) }"
    :visible="visible"
    :wrapStyle="{height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px'}"
  >
    <p v-if="action === 'update'">{{ $t('ci.batchUpdateTip') }}</p>
    <a-form :form="form" :layout="formLayout" @submit="createInstance">
      <a-button type="primary" @click="createInstance">Submit</a-button>
      <a-form-item
        v-bind="formItemLayout"
        :label="attr.alias || attr.name"
        v-for="(attr, attr_idx) in attributeList"
        :key="attr.name + attr_idx"
      >
        <a-select
          v-decorator="[ attr.name, { rules: [ { required: attr.is_required && action === 'create' ? true: false } ] } ]"
          :placeholder="$t('tip.pleaseSelect')"
          v-if="attr.is_choice"
        >
          <a-select-option
            :value="choice"
            :key="'New_' + attr.name + choice_idx"
            v-for="(choice, choice_idx) in attr.choice_value"
          >{{ choice }}</a-select-option>
        </a-select>
        <a-input-number
          v-decorator="[ attr.name, { rules: [ { required: attr.is_required && action === 'create' ? true: false } ] } ]"
          style="width: 100%"
          v-else-if="valueTypeMap[attr.value_type] == 'int' || valueTypeMap[attr.value_type] == 'float'"
        />
        <a-date-picker
          v-decorator="[ attr.name, { rules: [ { required: attr.is_required && action === 'create' ? true: false } ] } ]"
          style="width: 100%"
          :format="valueTypeMap[attr.value_type] == 'date' ? 'YYYY-MM-DD': 'YYYY-MM-DD HH:mm:ss'"
          v-else-if="valueTypeMap[attr.value_type] == 'date' || valueTypeMap[attr.value_type] == 'datetime'"
        />
        <a-input
          v-decorator="[attr.name, {validateTrigger: ['submit'], rules: [{ required: attr.is_required && action === 'create' ? true: false}]}]"
          style="width: 100%"
          v-else
        />
      </a-form-item>
    </a-form>
  </a-drawer>
</template>

<script>
import { getCIType } from '@/api/cmdb/CIType'
import { getCITypeAttributesById } from '@/api/cmdb/CITypeAttr'
import { addCI } from '@/api/cmdb/ci'

import { notification } from 'ant-design-vue'

var valueTypeMap = {
  '0': 'int',
  '1': 'float',
  '2': 'text',
  '3': 'datetime',
  '4': 'date',
  '5': 'time',
  '6': 'json'
}

export default {
  data () {
    return {
      action: '',
      form: this.$form.createForm(this),

      visible: false,
      attributeList: [],
      typeId: this.$router.currentRoute.meta.typeId,
      CIType: {},
      valueTypeMap: valueTypeMap,

      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 8 }
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 16 }
        }
      },
      formLayout: 'horizontal'
    }
  },
  computed: {
    title () {
      return this.action === 'create' ? this.$t('tip.create') + ' ' : this.$t('ci.batchUpdate') + ' '
    }
  },
  watch: {
    '$route.path': function (oldValue, newValue) {
      this.typeId = this.$router.currentRoute.meta.typeId
      this.getCIType()
      this.getAttributeList()
    }
  },
  created () {
    this.getCIType()
    this.getAttributeList()
  },
  methods: {
    getCIType () {
      getCIType(this.typeId).then(res => {
        this.CIType = res.ci_types[0]
      })
    },
    getAttributeList () {
      getCITypeAttributesById(this.typeId).then(res => {
        const attrList = res.attributes
        this.attributeList = attrList.sort((x, y) => y.is_required - x.is_required)
      })
    },
    createInstance (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        Object.keys(values).forEach(k => {
          if (typeof values[k] === 'object') {
            values[k] = values[k].format('YYYY-MM-DD HH:mm:ss')
          }
        })
        if (!err) {
          if (this.action === 'update') {
            this.$emit('submit', values)
            return
          }

          values.ci_type = this.typeId
          addCI(values)
            .then(res => {
              notification.success({
                message: this.$t('tip.addSuccess')
              })
            })
            .catch(e => {
              notification.error({
                message: e.response.data.message
              })
            })
        } else {
          notification.error({
            message: err
          })
        }
      })
    }
  }
}
</script>
