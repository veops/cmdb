<template>
  <div class="public-cloud-wrap">
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
      <a-form-model-item :required="true" label="key">
        <a-input-password
          :class="[formData.tabActive === TAB_KEY.CONFIG ? 'input-disabled' : '']"
          v-model="formData.key"
        />
      </a-form-model-item>
      <a-form-model-item v-if="formData.tabActive === TAB_KEY.CUSTOM" :required="true" label="secret">
        <a-input-password v-model="formData.secret" />
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { getHTTPAccounts } from '@/modules/cmdb/api/discovery'
import { TAB_KEY } from '../constants.js'
import CloudTab from '../cloudTab/index.vue'

export default {
  name: 'PublicCloud',
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
      accountsList: []
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
        const { _reference = '', key = '', tabActive } = this?.formData || {}
        const findSelect = this.accountsList?.find((item) => item.id === _reference)
        const newFormData = findSelect?.config || {}

        const changeData = {
          ...this.value,
          _reference: findSelect?.id ?? '',
        }
        if (tabActive === TAB_KEY.CONFIG) {
          changeData.key = newFormData?.key ?? key
        }
        this.$emit('change', changeData)
      })
    },

    handleTabChange(key) {
      if (key === TAB_KEY.CONFIG) {
        this.handleSelectChange(this.formData._reference)
      }
    },

    handleSelectChange(id) {
      const accountConfig = this.accountsList.find((item) => item.id === id)?.config || {}
      const { key } = this?.value
      this.$emit('change', {
        ...this.value,
        key: accountConfig?.key ?? key ?? '',
      })
    }
  }
}
</script>

<style lang="less" scoped>
.public-cloud-wrap {
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
