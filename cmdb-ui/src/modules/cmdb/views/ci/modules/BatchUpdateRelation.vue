<template>
  <a-drawer
    :title="$t('cmdb.ci.batchAddRelation')"
    width="50%"
    @close="() => { visible = false; $emit('refresh', true) }"
    :visible="visible"
    :wrapStyle="{ overflow: 'auto' }"
  >
    <a-form :form="form" :layout="formLayout" @submit="commitUpdateRelation">
      <a-button type="primary" @click="commitUpdateRelation">Submit</a-button>
      <a-form-item
        v-bind="formItemLayout"
        :label="item.alias || item.name"
        v-for="item in parentCITypes"
        :key="item.id"
      >
        <template v-for="_item in item.attributes">
          <a-input
            v-decorator="[_item.name, {validateTrigger: ['submit'], rules: []}]"
            style="width: 100%"
            v-if="_item.id == item.unique_id"
            :key="_item.id"
            :placeholder="_item.alias || _item.name"
          />
        </template>
      </a-form-item>
    </a-form>
  </a-drawer>
</template>

<script>
import { getCITypeParent } from '@/modules/cmdb/api/CITypeRelation'

export default {
  props: {
    typeId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      action: '',
      form: this.$form.createForm(this),
      parentCITypes: [],
      visible: false,

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
  created () {
    this.getParentCITypes()
  },
  methods: {
    getParentCITypes () {
      getCITypeParent(this.typeId).then(res => {
        this.parentCITypes = res.parents
      })
    },
    commitUpdateRelation (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          this.$emit('submit', values)
        }
      })
    }
  }
}
</script>
