<template>
  <a-form-model
    :model="formData"
    :labelCol="labelCol"
    :wrapperCol="{ span: 6 }"
    class="attr-ad-form"
  >
    <a-form-model-item
      :label="$t('cmdb.ciType.initialNode')"
      :extra="$t('cmdb.ciType.snmpFormTip4')"
    >
      <a-input
        v-model="formData.initial_node"
        :placeholder="$t('cmdb.ciType.defaultGateway')"
      />
    </a-form-model-item>

    <a-form-model-item
      :label="$t('cmdb.ciType.recursiveOrNot')"
      :extra="$t('cmdb.ciType.snmpFormTip5')"
    >
      <a-switch v-model="formData.recursive_scan" />
    </a-form-model-item>

    <a-form-model-item
      :label="$t('cmdb.ciType.maximumDepth')"
      :extra="$t('cmdb.ciType.snmpFormTip6')"
    >
      <a-input-number
        v-model="formData.max_depth"
        :min="0"
        :precision="0"
      />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
export default {
  name: 'SNMPScanningConfig',
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
  methods: {
  }
}
</script>
