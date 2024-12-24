<template>
  <div class="rack-container">
    <div class="rack-title">
      <ops-icon
        :type="titleData.icon"
        class="rack-title-icon"
      />
      <span
        class="rack-title-text"
      >
        {{ $t(titleData.text) }}
      </span>
    </div>

    <RackHeader :viewType="viewType" />

    <div
      class="rack-container-main"
      :style="{
        flexDirection: viewType === 'front' ? 'row' : 'row-reverse'
      }"
    >
      <div class="rack-container-main-left">
        <div
          v-for="(item, index) in countList"
          :key="index"
          class="rack-container-main-left-count"
          :style="{
            backgroundColor: item % 2 === 0 ? '#3D4151' : '#5E6772',
            height: unitHeight + 'px',
            lineHeight: unitHeight + 'px'
          }"
        >
          {{ item }}
        </div>
      </div>

      <div class="rack-container-main-list">
        <draggable
          filter=".undraggable"
          :list="unitList"
          @start="handleDraggableStart"
          @end="handleDraggableEnd"
        >
          <div
            v-for="(item, index) in unitList"
            :key="item.key"
            :class="[item.type === 'gap' || item.abnormal ? 'undraggable' : '']"
          >
            <div
              v-if="item.type === 'device'"
              :class="['rack-container-main-list-device', item.abnormal ? '' : 'rack-container-main-list-device_normal']"
              :style="{
                height: unitHeight * item.unitCount + 'px'
              }"
              @click="clickDevice(item)"
            >
              <div class="rack-container-main-list-device-action">
                <div
                  class="rack-container-main-list-device-action-btn"
                  @click.stop="removeDevice(item)"
                >
                  {{ $t('cmdb.dcim.remove') }}
                </div>
                <div
                  class="rack-container-main-list-device-action-btn"
                  @click.stop="migrateDevice(item)"
                >
                  {{ $t('cmdb.dcim.migrate') }}
                </div>
              </div>

              <div
                v-if="item.abnormal"
                class="rack-container-main-list-device-abnormal"
              >
                <span
                  class="rack-container-main-list-device-abnormal-text"
                >
                  {{ $t('cmdb.dcim.unitAbnormal') }}
                </span>
                <a-icon
                  type="right"
                  class="rack-container-main-list-device-abnormal-icon"
                />
              </div>

              <div class="rack-container-main-list-device-header"></div>
              <img
                v-for="(unitIndex) in item.unitCount"
                :key="unitIndex"
                :src="item.deviceImage[viewType]"
              />

              <div
                class="rack-container-main-list-device-sider"
                :style="{
                  right: viewType === 'front' ? '-154px' : '-157px'
                }"
              >
                <div
                  v-for="(nameItem, nameIndex) in getNameList(item)"
                  :key="nameIndex"
                  class="rack-container-main-list-device-name"
                  @click.stop="openDeviceDetail(nameItem)"
                >
                  <CIIcon size="14" :icon="nameItem.icon" />
                  <span class="rack-container-main-list-device-name-text">{{ nameItem.name }}</span>
                </div>
              </div>
            </div>
            <div
              v-if="item.type === 'gap'"
              :class="['rack-container-main-list-gap', viewType === 'rear' ? 'rack-container-main-list-gap_rear' : '']"
              :style="{
                height: unitHeight + 'px'
              }"
              @click="addDevice(index)"
            >
              <a-icon
                type="plus-circle"
                class="rack-container-main-list-gap-icon"
              />
              <span
                class="rack-container-main-list-gap-text"
              >
                {{ $t('cmdb.dcim.addDevice') }}
              </span>
            </div>
          </div>
        </draggable>
      </div>

      <div class="rack-container-main-right">
        <div class="rack-container-main-right-part-1"></div>
        <div class="rack-container-main-right-part-2"></div>

        <img
          v-if="viewType === 'front'"
          :src="require(`@/modules/cmdb/assets/dcim/rack_front_part.png`)"
          class="rack-container-main-right-part-3"
        />
      </div>
    </div>

    <div class="rack-container-footer">
      <template v-if="viewType === 'front'">
        <div class="rack-container-footer-dot"></div>
        <div class="rack-container-footer-dot"></div>
      </template>
    </div>

    <AbnormalModal
      ref="abnormalModalRef"
      @ok="editDevice"
    />
  </div>
</template>

<script>
import _ from 'lodash'
import { deleteDevice } from '@/modules/cmdb/api/dcim.js'

import RackHeader from './rackHeader/index.vue'
import draggable from 'vuedraggable'
import CIIcon from '@/modules/cmdb/components/ciIcon/index.vue'
import AbnormalModal from './abnormalModal.vue'

export default {
  name: 'RackUnitView',
  components: {
    RackHeader,
    draggable,
    CIIcon,
    AbnormalModal
  },
  props: {
    viewType: {
      type: String,
      default: 'front'
    },
    countList: {
      type: Array,
      default: () => []
    },
    unitList: {
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
      oldDraggableList: [],
      draggableDevice: {},

      unitHeight: 24
    }
  },
  computed: {
    titleData() {
      return {
        icon: this.viewType === 'front' ? 'veops-front' : 'veops-rear',
        text: this.viewType === 'front' ? 'cmdb.dcim.frontView' : 'cmdb.dcim.rearView'
      }
    }
  },
  methods: {
    addDevice(index) {
      const sliceUnitList = this.unitList.slice(0, index)
      const unitCount = sliceUnitList.reduce((acc, cur) => acc + cur.unitCount, 0)

      this.$emit('openDeviceForm', {
        unitStart: this.countList.length - unitCount
      })
    },

    editDevice(data) {
      this.$emit('openDeviceForm', {
        CITypeId: data?._type,
        deviceId: data?.id,
        unitStart: data?.u_start,
        unitCount: data?.u_count,
        name: data?.name
      })
    },

    handleDraggableStart(e) {
      this.oldDraggableList = _.cloneDeep(this.unitList)
      this.draggableDevice = this.oldDraggableList?.[e.oldIndex] || {}
    },

    handleDraggableEnd(e) {
      if (e.newIndex === e.oldIndex) {
        return
      }

      const sliceUnitList = this.unitList.slice(0, e.newIndex)
      const unitCount = sliceUnitList.reduce((acc, cur) => acc + cur.unitCount, 0)

      /**
       * 拖拽后的起始U位 = 总U数 - 该设备以上的U数 - 该设备U数 + 1
       */
      const startUnit = this.countList.length - unitCount - this.draggableDevice.unitCount + 1

      if (this?.draggableDevice?.id) {
        this.$emit('draggable', {
          startUnit,
          deviceId: this.draggableDevice.id,
          oldUnitList: this.oldDraggableList
        })
      }

      this.draggableDevice = {}
      this.oldDraggableList = []
    },

    getNameList(item) {
      const nameList = [item]

      if (item?.abnormalList?.length) {
        nameList.push(...item.abnormalList)
      }

      return nameList
    },

    clickDevice(data) {
      if (data.abnormal) {
        this.$refs.abnormalModalRef.open(data)
      }
    },

    removeDevice(data) {
      const content = this.$t('cmdb.dcim.removeDeviceTip', {
        deviceName: `${data.CITypeName} ${data.name}`
      })

      this.$confirm({
        title: this.$t('warning'),
        content,
        onOk: () => {
          deleteDevice(
            this.rackId,
            data.id
          ).then(() => {
            this.$message.success(this.$t('deleteSuccess'))
            this.$emit('refreshRackAllData')
          })
        },
      })
    },

    migrateDevice(data) {
      this.$emit('migrateDevice', data.id)
    },

    openDeviceDetail(deviceData) {
      this.$emit('openDeviceDetail', deviceData)
    }
  }
}
</script>

<style lang="less" scoped>
.rack-container {
  width: 236px;

  .rack-title {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;

    &-icon {
      font-size: 14px;
    }

    &-text {
      font-size: 14px;
      font-weight: 700;
      color: #4E5969;
      margin-left: 6px;
    }
  }

  &-main {
    display: flex;
    width: 100%;

    &-left {
      min-width: 17px;
      flex-shrink: 0;
      z-index: 2;

      &-count {
        width: 100%;
        border-bottom: solid 1px rgba(116, 138, 171, 0.25);
        text-align: center;
        font-size: 12px;
        font-weight: 400;
        color: #FFFFFF;
      }
    }

    &-list {
      width: 100%;

      &-device {
        background-color: #2C2D31;
        border-bottom: solid 1px rgba(116, 138, 171, 0.25);
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;

        &-header {
          width: 195px;
          height: 6px;
          clip-path: polygon(20px 0, 175px 0, 195px 100%, 0px 100%);
          background-color: #5D6271;
        }

        img {
          width: 195px;
          height: 17px;
        }

        &-action {
          display: none;
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border: 1px solid #10D4FF;
          background: linear-gradient(90deg, rgba(0, 0, 0, 0.80) 0%, rgba(102, 102, 102, 0.80) 100%);
          align-items: center;
          justify-content: center;

          &-btn {
            font-size: 14px;
            font-weight: 400;
            color: #FFFFFF;
            padding: 0 10px;
            cursor: pointer;

            &:not(:first-child) {
              border-left: solid 1px rgba(165, 169, 188, 0.44);
            }

            &:hover {
              color: #10D4FF;
            }
          }
        }

        &-abnormal {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border: 1px solid #F00;
          background-color: rgba(128, 47, 47, 0.66);
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;

          &-text {
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 700;
          }

          &-icon {
            color: #FFFFFF;
            font-size: 12px;
          }
        }

        &-name {
          display: flex;
          align-items: center;
          cursor: pointer;

          &-text {
            margin-left: 3px;
            font-size: 12px;
            font-weight: 400;
            color: #1D2129;

            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            text-wrap: nowrap;
          }

          &:hover {
            .rack-container-main-list-device-name-text {
              color: #3F75FF;
            }
          }
        }

        &-sider {
          position: absolute;
          top: 0;
          width: 140px;
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: center;
          row-gap: 6px;
          padding-left: 7px;

          &::after {
            content: "";
            position: absolute;
            top: 5%;
            left: 0;
            width: 4px;
            height: 90%;
            border: solid 1px #10D4FF;
            border-left: none;
          }
        }

        &_normal:hover {
          .rack-container-main-list-device-action {
            display: flex;
          }
        }
      }

      &-gap {
        width: 100%;
        border-bottom: solid 1px rgba(116, 138, 171, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        background-color: #EBEFF8;

        &-icon {
          font-size: 12px;
          display: none;
          color: @primary-color;
        }

        &-text {
          font-size: 12px;
          font-weight: 400;
          color: @primary-color;
          margin-left: 6px;
          display: none;
        }

        &_rear {
          background-color: #CACDD9;
          border-bottom: solid 1px #E4E7ED;
        }

        &:hover {
          background-color: @primary-color_4;

          .rack-container-main-list-gap-icon {
            display: inline-block;
          }

          .rack-container-main-list-gap-text {
            display: inline-block;
          }
        }
      }
    }

    &-right {
      flex-shrink: 0;
      display: flex;
      background-color: #86909C;
      position: relative;

      &-part-1 {
        width: 7px;
        height: 100%;
        border-right: solid 1px rgba(255, 255, 255, 0.33);
      }

      &-part-2 {
        width: 7px;
        height: 100%;
        background: linear-gradient(270deg, rgba(134, 144, 156, 0.00) 0%, rgba(69, 78, 89, 0.88) 100%);
        filter: blur(0.25px);
      }

      &-part-3 {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 21px;
        height: 57.6px;
        transform: translate(-50%, -50%);
      }
    }
  }

  &-footer {
    height: 12px;
    width: 100%;
    background-color: #86909C;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0px 14px;

    &-dot {
      width: 4px;
      height: 4px;
      border-radius: 4px;
      background-color: #E8EBEE;
      border: solid 1px #FFFFFF;
      box-shadow: 3px 3px 7px 0px rgba(136, 150, 163, 0.58) inset, -3px -3px 7px 0px #FFF inset;
    }
  }
}
</style>
