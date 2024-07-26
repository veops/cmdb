<template>
  <a-form-model
    :model="formData"
    labelAlign="right"
    :labelCol="labelCol"
    :wrapperCol="{ span: 6 }"
    class="attr-ad-form"
  >
    <a-form-model-item :extra="`${$t('cmdb.ciType.example')}: 192.168.0.0/16`" :label="$t('cmdb.ciType.portScanLabel1')">
      <a-input v-model="formData.cidr" />
    </a-form-model-item>
    <a-form-model-item :extra="`${$t('cmdb.ciType.example')}: 8000-8800`" :label="$t('cmdb.ciType.portScanLabel2')">
      <a-input v-model="formData.ports" />
    </a-form-model-item>
    <a-form-model-item :extra="`${$t('cmdb.ciType.example')}: 0x1234`" :label="$t('cmdb.ciType.portScanLabel3')">
      <a-input v-model="formData.enable_cidr" />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
export default {
  name: 'PortScanConfig',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: Object,
      default: () => {},
    },
  },
  inject: ['provide_labelCol'],
  computed: {
    formData: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit('change', newValue)
      }
    },
    labelCol() {
      return this.provide_labelCol()
    }
  },
}
</script>

<style lang="less" scoped>
</style>
