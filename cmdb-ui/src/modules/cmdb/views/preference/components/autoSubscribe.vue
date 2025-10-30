<template>
  <a-modal
    :title="$t('cmdb.preference.autoSub')"
    :visible="visible"
    :width="600"
    @cancel="handleCancel"
    @ok="handleOk"
  >
    <a-form-model
      ref="autuSubFormRef"
      :model="form"
      :rules="rules"
      :label-col="{ span: 7 }"
      :wrapper-col="{ span: 15 }"
    >
      <a-form-model-item
        :label="$t('cmdb.preference.autoSubScope')"
        prop="base_strategy"
      >
        <a-radio-group
          v-model="form.base_strategy"
          :options="baseStrategyOptions"
        />
        <div class="ant-form-explain">{{ $t('cmdb.preference.autoSubScopeHint') }}</div>
      </a-form-model-item>
      <a-form-model-item
        :label="form.base_strategy === 'all' ? $t('cmdb.preference.excludeGroup') : $t('cmdb.preference.selectGroup')"
        prop="group_ids"
      >
        <a-select
          v-model="form.group_ids"
          mode="multiple"
          optionFilterProp="title"
          :options="groupSelectOptions"
          :placeholder="form.base_strategy === 'all' ? $t('cmdb.preference.excludeGroupPlaceholder') : $t('cmdb.preference.selectGroupPlaceholder')"
        />
        <div class="ant-form-explain">
          {{ form.base_strategy === 'all' ? $t('cmdb.preference.excludeGroupHint') : $t('cmdb.preference.selectGroupHint') }}
        </div>
      </a-form-model-item>

      <a-form-model-item
        :label="form.base_strategy === 'all' ? $t('cmdb.preference.excludeModel') : $t('cmdb.preference.selectModel')"
        prop="type_ids"
      >
        <a-select
          v-model="form.type_ids"
          mode="multiple"
          optionFilterProp="title"
          :placeholder="form.base_strategy === 'all' ? $t('cmdb.preference.excludeModelPlaceholder') : $t('cmdb.preference.selectModelPlaceholder')"
        >
          <a-select-opt-group
            v-for="(group) in modelSelectOptions"
            :key="group.value"
            :title="group.label"
          >
            <span slot="label">{{ group.label }}</span>
            <a-select-option
              v-for="(type) in group.children"
              :key="type.value"
              :value="type.value"
              :title="type.label"
            >
              {{ type.label }}
            </a-select-option>
          </a-select-opt-group>
        </a-select>
        <div class="ant-form-explain">
          {{ form.base_strategy === 'all' ? $t('cmdb.preference.excludeModelHint') : $t('cmdb.preference.selectModelHint') }}
        </div>
      </a-form-model-item>

      <a-form-model-item
        :label="$t('cmdb.preference.isEnable')"
        prop="enabled"
      >
        <a-switch v-model="form.enabled" />
        <div class="ant-form-explain">{{ $t('cmdb.preference.enableAutoSubTip') }}</div>
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { putAutoSubscription } from '@/modules/cmdb/api/preference.js'

export default {
  name: 'AutoSubscribe',
  props: {
    ciType: {
      type: Array,
      default: () => []
    },
    autoSub: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      visible: false,
      form: {
        base_strategy: 'all',
        group_ids: [],
        type_ids: [],
        enabled: true,
      },
      rules: {
        base_strategy: [{ required: true, message: this.$t('placeholder2') }],
      },
      baseStrategyOptions: [
        {
          label: this.$t('cmdb.preference.subscribeAllModel'),
          value: 'all'
        },
        {
          label: this.$t('cmdb.preference.selectiveSubscription'),
          value: 'none'
        }
      ],
      groupSelectOptions: [],
      modelSelectOptions: []
    }
  },
  methods: {
    async open() {
      this.form = {
        base_strategy: this.autoSub?.base_strategy || 'all',
        group_ids: this.autoSub?.group_ids || [],
        type_ids: this.autoSub?.type_ids || [],
        enabled: this.autoSub?.enabled ?? true
      }

      this.groupSelectOptions = this.ciType.map((group) => {
        return {
          label: group.name,
          title: group.name,
          value: group.id
        }
      })

      const modelSelectOptions = this.ciType.filter((group) => group?.ci_types?.length)
      this.modelSelectOptions = modelSelectOptions.map((group) => {
        return {
          label: group.name,
          value: group.id,
          children: group.ci_types.map((type) => {
            return {
              label: type.alias || type.name,
              value: type.id
            }
          })
        }
      })

      this.visible = true
    },
    handleCancel() {
      this.visible = false
    },
    handleOk() {
      this.$refs.autuSubFormRef.validate(async (valid) => {
        if (valid) {
          const { base_strategy, group_ids, type_ids, enabled } = this.form

          const params = {
            base_strategy: base_strategy,
            group_ids: group_ids.join(','),
            type_ids: type_ids.join(','),
            enabled: enabled
          }

          putAutoSubscription(params).then(() => {
            this.$message.success(this.$t('saveSuccess'))
            this.handleCancel()
            this.$emit('ok')
          })
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
