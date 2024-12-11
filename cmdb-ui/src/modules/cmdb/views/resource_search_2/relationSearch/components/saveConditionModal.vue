<template>
  <a-modal
    :title="$t('cmdb.relationSearch.saveCondition')"
    :visible="visible"
    dialogClass="save-condition-modal"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="saveConditionForm"
      :model="form"
      :rules="formRule"
      :labelCol="labelCol"
      :wrapperCol="wrapperCol"
    >
      <a-form-model-item
        :label="$t('cmdb.relationSearch.conditionName')"
        prop="name"
      >
        <a-input v-model="form.name" />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
export default {
  name: 'SaveConditionModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    labelCol() {
      return {
        span: this.$i18n.locale === 'en' ? 7 : 4
      }
    },
    wrapperCol() {
      return {
        span: this.$i18n.locale === 'en' ? 17 : 20
      }
    },
  },
  data() {
    return {
      form: {
        name: ''
      },
      formRule: {
        name: [
          { required: true, message: this.$t('placeholder1') }
        ],
      }
    }
  },
  methods: {
    handleOk() {
      this.$refs.saveConditionForm.validate((valid) => {
        if (!valid) {
          return
        }

        this.$emit('ok', {
          name: this.form.name
        })
        this.handleCancel()
      })
    },

    handleCancel() {
      this.$refs.saveConditionForm.clearValidate()
      this.form.name = ''
      this.$emit('cancel')
    }
  }
}
</script>
