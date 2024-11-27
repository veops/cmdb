<template>
  <div v-if="unitList.length" class="rack-view">
    <div class="rack-view-col">
      <RackUnitView
        viewType="front"
        :countList="countList"
        :unitList="unitList"
        :rackId="rackData._id"
        @migrateDevice="migrateDevice"
        @openDeviceForm="openDeviceForm"
        @draggable="handleDraggable"
        @refreshRackAllData="refreshRackAllData"
        @openDeviceDetail="openDeviceDetail"
      />
    </div>

    <div class="rack-view-col">
      <RackUnitView
        viewType="rear"
        :countList="countList"
        :unitList="unitList"
        :rackId="rackData._id"
        @migrateDevice="migrateDevice"
        @openDeviceForm="openDeviceForm"
        @draggable="handleDraggable"
        @refreshRackAllData="refreshRackAllData"
        @openDeviceDetail="openDeviceDetail"
      />
    </div>

    <DeviceForm
      ref="deviceFormRef"
      :CITypeRelations="CITypeRelations"
      :rackId="rackData._id"
      @ok="refreshRackAllData"
    />

    <MigrateModal
      ref="migrateModalRef"
      :rackList="rackList"
      @ok="refreshRackAllData"
    />

    <CIDetailDrawer
      ref="CIdetailRef"
      :typeId="deviceCITypeId"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import { putDevice } from '@/modules/cmdb/api/dcim.js'
import { DEVICE_CITYPE_NAME } from '../../../constants.js'

import RackUnitView from './rackUnitView.vue'
import DeviceForm from './deviceForm/index.vue'
import MigrateModal from './migrateModal.vue'
import CIDetailDrawer from '@/modules/cmdb/views/ci/modules/ciDetailDrawer.vue'

export default {
  name: 'RackView',
  components: {
    RackUnitView,
    DeviceForm,
    MigrateModal,
    CIDetailDrawer
  },
  props: {
    CITypeRelations: {
      type: Array,
      default: () => []
    },
    rackData: {
      type: Object,
      default: () => {}
    },
    deviceList: {
      type: Array,
      default: () => []
    },
    rackList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      unitList: [],
      countList: [],

      deviceAttrList: [],
      deviceCITypeId: 0,
    }
  },
  inject: [
    'getRackList',
    'getDeviceList'
  ],
  provide() {
    return {
      handleSearch: this.refreshRackAllData,
      attrList: () => {
        return this.deviceAttrList
      },
      attributes: () => {
        return {
          attributes: this.deviceAttrList
        }
      }
    }
  },
  watch: {
    deviceList: {
      immediate: true,
      deep: true,
      handler(deviceList) {
        this.initData(deviceList)
      }
    }
  },
  methods: {
    async initData(deviceList) {
      const CITypeMap = this.CITypeRelations.reduce((map, cur) => {
        map[cur.id] = cur
        return map
      }, {})

      const _deviceList = _.cloneDeep(deviceList)

      // 建立设备map, 并处理U位异常情况
      const deviceMap = {}
      _deviceList.forEach((device, index) => {
        const CITYpe = CITypeMap?.[device?._type] || {}

        device.deviceImage = this.getDeviceViewImage(CITYpe?.name)
        device.name = device?.[CITYpe?.show_key] || device._id || ''
        device.icon = CITYpe?.icon || ''
        device.CITypeName = CITYpe?.alias || CITYpe?.name || ''
        device.id = device._id

        if (index > 0) {
          const abnormalDevice = _deviceList.slice(0, index).find((item) => {
            const unitCount = item.abnormal ? item.abnormalUnitcount : item.u_count

            return item.u_start <= device.u_start && device.u_start <= (item.u_start + unitCount - 1)
          })

          if (abnormalDevice) {
            abnormalDevice.abnormal = true
            const endCount = Math.max(abnormalDevice.u_start + abnormalDevice.u_count, device.u_start + device.u_count)
            abnormalDevice.abnormalUnitcount = endCount - abnormalDevice.u_start

            if (abnormalDevice?.abnormalList?.length) {
              abnormalDevice.abnormalList.push(device)
            } else {
              abnormalDevice.abnormalList = [device]
            }
          } else {
            deviceMap[device.u_start] = device
          }
        } else {
          deviceMap[device.u_start] = device
        }
      })

      let unitIndex = 1
      const unitList = []

      while (unitIndex <= this.rackData.u_count) {
        if (deviceMap[unitIndex]) {
          const device = deviceMap[unitIndex]
          const unitCount = device?.abnormal ? device.abnormalUnitcount : device.u_count

          unitList.push({
            ...device,
            unitCount,
            type: 'device',
            key: uuidv4(),
            abnormal: device?.abnormal ?? false,
            abnormalList: device.abnormalList
          })

          unitIndex += unitCount
          device.assign = true
        } else {
          unitList.push({
            type: 'gap',
            unitCount: 1,
            key: uuidv4()
          })
          unitIndex += 1
        }
      }

      this.unitList = _.reverse(unitList)
      this.countList = Array.from({ length: this.rackData.u_count }, (_, i) => this.rackData.u_count - i)
    },

    getDeviceViewImage(name) {
      const image = {
        front: require('@/modules/cmdb/assets/dcim/device/server_front.png'),
        rear: require('@/modules/cmdb/assets/dcim/device/server_rear.png')
      }

      switch (name) {
        case DEVICE_CITYPE_NAME.ROUTER:
          image.front = require('@/modules/cmdb/assets/dcim/device/router_front.png')
          image.rear = require('@/modules/cmdb/assets/dcim/device/router_rear.png')
          break
        case DEVICE_CITYPE_NAME.FIRE_WALL:
          image.front = require('@/modules/cmdb/assets/dcim/device/firewall_front.png')
          image.rear = require('@/modules/cmdb/assets/dcim/device/firewall_rear.png')
          break
        case DEVICE_CITYPE_NAME.SERVER:
          image.front = require('@/modules/cmdb/assets/dcim/device/server_front.png')
          image.rear = require('@/modules/cmdb/assets/dcim/device/server_rear.png')
          break
        case DEVICE_CITYPE_NAME.RAID:
          image.front = require('@/modules/cmdb/assets/dcim/device/raid_front.png')
          image.rear = require('@/modules/cmdb/assets/dcim/device/raid_rear.png')
          break
        case DEVICE_CITYPE_NAME.SWITCH:
        case DEVICE_CITYPE_NAME.FC_SWITCH:
        case DEVICE_CITYPE_NAME.F5:
          image.front = require('@/modules/cmdb/assets/dcim/device/switch_front.png')
          image.rear = require('@/modules/cmdb/assets/dcim/device/switch_rear.png')
          break
        default:
          break
      }

      return image
    },

    openDeviceForm(deviceData) {
      this.$refs.deviceFormRef.open(deviceData)
    },

    handleDraggable({
      startUnit,
      deviceId,
      oldUnitList
    }) {
      putDevice(
        this.rackData._id,
        deviceId,
        {
          to_u_start: startUnit
        }
      ).then(() => {
        this.getDeviceList()
      }).catch((error) => {
        console.log('putDevice fail', error)
        this.unitList = oldUnitList
      })
    },

    migrateDevice(deviceId) {
      this.$refs.migrateModalRef.open({
        deviceId,
        rackId: this.rackData._id
      })
    },

    refreshRackAllData() {
      this.getRackList()
      this.getDeviceList()
    },

    async openDeviceDetail(data) {
      const deviceCIType = this.CITypeRelations.find((item) => item.id === data._type)
      this.deviceAttrList = deviceCIType?.attributes || []
      this.deviceCITypeId = data?._type

      this.$nextTick(() => {
        this.$refs.CIdetailRef.create(data._id)
      })
    }
  }
}
</script>

<style lang="less" scoped>
.rack-view {
  display: flex;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: calc(100vh - 160px);

  &-col {
    width: 50%;
  }
}
</style>
