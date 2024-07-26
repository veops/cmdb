<template>
  <div class="private-cloud-wrap">
    <CloudTab
      v-model="formData.tabActive"
      @change="handleTabChange"
    />
    <a-form-model
      :model="formData"
      labelAlign="right"
      :labelCol="labelCol"
      :wrapperCol="{ span: 6 }"
      class="attr-ad-form"
    >
      <a-form-model-item
        v-if="formData.tabActive === TAB_KEY.CONFIG"
        :required="true"
        :label="$t('cmdb.ad.tabConfig')"
      >
        <a-select
          showSearch
          optionFilterProp="title"
          v-model="formData._reference"
          @change="handleSelectChange"
        >
          <a-select-option
            v-for="(item) in accountsList"
            :key="item.id"
            :value="item.id"
            :title="item.name"
          >
            {{ item.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>
      <a-form-model-item :required="true" :label="$t('cmdb.ciType.host')">
        <a-input
          :disabled="formData.tabActive === TAB_KEY.CONFIG"
          v-model="formData.host"
        />
      </a-form-model-item>
      <a-form-model-item :required="true" :label="$t('cmdb.ciType.account')">
        <a-input
          :disabled="formData.tabActive === TAB_KEY.CONFIG"
          v-model="formData.account"
        />
      </a-form-model-item>
      <a-form-model-item v-if="formData.tabActive === TAB_KEY.CUSTOM" :required="true" :label="$t('cmdb.ciType.password')">
        <a-input-password v-model="formData.password" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cmdb.ciType.vcenterName')">
        <a-input v-model="formData.vcenterName" />
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { getHTTPAccounts } from '@/modules/cmdb/api/discovery'
import { TAB_KEY } from '../constants.js'
import CloudTab from '../cloudTab/index.vue'

export default {
  name: 'VCenterForm',
  components: {
    CloudTab
  },
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
  data() {
    return {
      TAB_KEY,
      accountsList: [],
    }
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
    async init(id) {
      const res = await getHTTPAccounts({
        adr_id: id
      })
      this.accountsList = res?.length ? res : []

      this.$nextTick(() => {
        const { _reference = '', host = '', account = '', tabActive } = this?.formData || {}
        const findSelect = this.accountsList?.find((item) => item.id === _reference)
        const newFormData = findSelect?.config || {}

        const changeData = {
          ...this.value,
          _reference: findSelect?.id ?? '',
        }
        if (tabActive === TAB_KEY.CONFIG) {
          changeData.host = newFormData?.host ?? host
          changeData.account = newFormData?.account ?? account
        }

        this.$emit('change', changeData)
      })
    },

    handleTabChange(key) {
      if (key === TAB_KEY.CONFIG) {
        this.handleSelectChange(this.formData._referenceValue)
      }
    },

    handleSelectChange(id) {
      const accountConfig = this.accountsList.find((item) => item.id === id)?.config || {}
      const { host, account } = this?.value
      this.$emit('change', {
        ...this.value,
        host: accountConfig?.host ?? host ?? '',
        account: accountConfig?.account ?? account ?? ''
      })
    }
  }
}
</script>

<style lang="less" scoped>
.private-cloud-wrap {
  margin-left: 17px;

  .input-disabled {
    /deep/ input {
      color: rgba(0, 0, 0, 0.25);
      background-color: #f5f5f5;
      pointer-events: none;
      opacity: 1;
    }
  }
}
</style>
