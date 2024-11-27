<template>
  <a-modal
    :visible="visible"
    :width="500"
    :title="$t('cmdb.dcim.addDevice')"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <a-form-model
      ref="deviceFormRef"
      :model="form"
      :rules="formRules"
      :label-col="{ span: 5 }"
      :wrapper-col="{ span: 19 }"
      class="device-form"
    >
      <a-form-model-item
        :label="$t('cmdb.dcim.ciType')"
        prop="CITypeId"
      >
        <a-select
          v-model="form.CITypeId"
          showSearch
          allowClear
          optionFilterProp="title"
          @change="handleCITypeChange"
        >
          <a-select-option
            v-for="(item) in CITypeRelations"
            :key="item.id"
            :value="item.id"
            :title="item.alias || item.name"
          >
            {{ item.alias || item.name }}
          </a-select-option>
        </a-select>
      </a-form-model-item>

      <a-form-model-item
        :label="$t('cmdb.dcim.device')"
        prop="deviceId"
      >
        <a-popover trigger="click" placement="bottom">
          <DeviceSelect
            slot="content"
            :CITypeId="form.CITypeId"
            :currentCITYpe="currentCITYpe"
            :currentSelect="form.deviceId"
            @change="handleDeviceChange"
          />
          <div
            class="device-form-select"
          >
            {{ deviceName }}
          </div>
        </a-popover>
      </a-form-model-item>

      <a-form-model-item
        :label="$t('cmdb.dcim.unitStart')"
        prop="unitStart"
      >
        <a-input-number
          v-model="form.unitStart"
          :min="1"
          :precision="0"
          class="device-form-input"
        />
      </a-form-model-item>

      <a-form-model-item
        v-if="showUnitCount"
        :label="$t('cmdb.dcim.unitCount')"
        prop="unitCount"
      >
        <a-input-number
          v-model="form.unitCount"
          :min="1"
          :precision="0"
          class="device-form-input"
        />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import { postDevice } from '@/modules/cmdb/api/dcim.js'

import DeviceSelect from './deviceSelect.vue'

export default {
  name: 'DeviceForm',
  components: {
    DeviceSelect
  },
  props: {
    CITypeRelations: {
      type: Array,
      default: () => []
    },
    rackId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      visible: false,
      form: {
        CITypeId: undefined,
        deviceId: undefined,
        unitStart: undefined,
        unitCount: undefined
      },

      deviceName: '',
      showUnitCount: true,
      formRules: {
        CITypeId: [
          {
            required: true, message: this.$t('placeholder2')
          }
        ],
        deviceId: [
          {
            required: true, message: this.$t('placeholder2')
          }
        ],
        unitStart: [
          {
            required: true, message: this.$t('placeholder1')
          }
        ],
        unitCount: [
          {
            required: true, message: this.$t('placeholder1')
          }
        ]
      }
    }
  },
  computed: {
    currentCITYpe() {
      return this.CITypeRelations.find((CIType) => CIType?.id === this.form.CITypeId) || {}
    }
  },
  methods: {
    open(deviceData) {
      this.visible = true

      if (deviceData) {
        this.form = {
          CITypeId: deviceData?.CITypeId ?? undefined,
          deviceId: deviceData?.deviceId ?? undefined,
          unitStart: deviceData?.unitStart ?? undefined,
          unitCount: deviceData?.unitCount ?? undefined,
        }

        if (this.form.unitCount) {
          this.showUnitCount = false
        }
        this.deviceName = deviceData?.name || ''
      }
    },

    handleCancel() {
      this.form = {
        CITypeId: undefined,
        deviceId: undefined,
        unitStart: undefined,
        unitCount: undefined
      }
      this.deviceName = ''
      this.showUnitCount = true
      this.$refs.deviceFormRef.clearValidate()

      this.visible = false
    },

    handleOk() {
      this.$refs.deviceFormRef.validate(async (valid) => {
        if (!valid) {
          return
        }

        await postDevice(
          this.rackId,
          this.form.deviceId,
          {
            u_start: this.form.unitStart,
            u_count: this.form.unitCount
          }
        )

        this.handleCancel()
        this.$message.success(this.$t('addSuccess'))
        this.$emit('ok')
      })
    },

    handleDeviceChange({
      name,
      value,
      unitCount
    }) {
      this.form.deviceId = value
      this.deviceName = name

      this.form.unitCount = unitCount || undefined
      this.showUnitCount = !unitCount
    },

    handleCITypeChange() {
      this.form.deviceId = undefined
      this.deviceName = ''
      this.showUnitCount = true
      this.form.unitCount = undefined
    }
  }
}
</script>

<style lang="less" scoped>
.device-form {
  &-select {
    border: 1px solid #e4e7ed;
    border-radius: 2px;
    line-height: 32px;
    min-height: 32px;
    padding: 0 12px;
    cursor: pointer;

    &:hover {
      border-color: #597ef7;
    }
  }

  &-input {
    width: 100%;
  }
}
</style>
