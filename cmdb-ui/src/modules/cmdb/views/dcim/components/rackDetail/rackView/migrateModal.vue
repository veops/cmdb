<template>
  <a-modal
    :title="$t('cmdb.dcim.deviceMigrate')"
    :visible="visible"
    :width="500"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="deviceMigrateFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      class="device-migrate"
    >
      <a-form-model-item
        :label="$t('cmdb.dcim.rack')"
        prop="to_rack_id"
      >
        <a-select
          v-model="form.to_rack_id"
          showSearch
          allowClear
          optionFilterProp="title"
        >
          <a-select-option
            v-for="(rack) in rackList"
            :key="rack._id"
            :value="rack._id"
            :title="rack.name"
          >
            {{ rack.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item
        :label="$t('cmdb.dcim.unitStart')"
        prop="to_u_start"
      >
        <a-input-number
          v-model="form.to_u_start"
          :min="1"
          :precision="0"
          class="device-migrate-input"
        />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { migrateDevice } from '@/modules/cmdb/api/dcim.js'

export default {
  name: 'MigrateModal',
  props: {
    rackList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      visible: false,
      form: {
        to_rack_id: undefined,
        to_u_start: undefined,
      },
      formRules: {
        to_rack_id: [
          {
            required: true, message: this.$t('placeholder2')
          }
        ],
        to_u_start: [
          {
            required: true, message: this.$t('placeholder1')
          }
        ]
      },

      deviceId: '',
      rackId: ''
    }
  },
  methods: {
    open(data) {
      this.visible = true
      this.deviceId = data?.deviceId || ''
      this.rackId = data?.rackId || ''
    },

    handleCancel() {
      this.deviceId = ''
      this.rackId = ''
      this.form = {
        to_rack_id: undefined,
        to_u_start: undefined,
      }

      this.$refs.deviceMigrateFormRef.clearValidate()
      this.visible = false
    },

    handleOk() {
      this.$refs.deviceMigrateFormRef.validate(async (valid) => {
        if (!valid) {
          return
        }

        migrateDevice(
          this.rackId,
          this.deviceId,
          {
            ...this.form
          }
        ).then(() => {
          this.$message.success(this.$t('cmdb.dcim.migrationSuccess'))
          this.handleCancel()
          this.$emit('ok')
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>
.device-migrate {
  &-input {
    width: 100%;
  }
}
</style>
