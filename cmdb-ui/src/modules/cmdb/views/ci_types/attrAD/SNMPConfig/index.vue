<template>
  <a-form-model
    :model="formData"
    :labelCol="labelCol"
    :wrapperCol="{ span: 6 }"
    class="attr-ad-form"
  >
    <a-form-model-item
      :label="$t('cmdb.ciType.defaultVersion')"
    >
      <a-select
        v-model="formData.version"
        allowClear
      >
        <a-select-option value="1">
          v1
        </a-select-option>
        <a-select-option value="2c">
          v2c
        </a-select-option>
      </a-select>
    </a-form-model-item>

    <a-form-model-item
      :label="$t('cmdb.ciType.defaultCommunity')"
    >
      <a-input v-model="formData.community" />
    </a-form-model-item>

    <a-form-model-item
      :label="$t('cmdb.ciType.timeout')"
      :extra="$t('cmdb.ciType.snmpFormTip2')"
    >
      <a-input-number
        v-model="formData.timeout"
        :min="0"
        :precision="0"
      />
    </a-form-model-item>

    <a-form-model-item
      :label="$t('cmdb.ciType.retryCount')"
      :extra="$t('cmdb.ciType.snmpFormTip3')"
    >
      <a-input-number
        v-model="formData.retries"
        :min="0"
        :precision="0"
      />
    </a-form-model-item>
  </a-form-model>
</template>

<script>
export default {
  name: 'SNMPConfig',
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
  }
}
</script>

<style lang="less" scoped>
</style>
