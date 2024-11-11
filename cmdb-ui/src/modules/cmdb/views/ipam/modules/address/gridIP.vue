<template>
  <div
    class="ip-grid"
    :style="{
      gap: gridGap + 'px'
    }"
  >
    <div
      v-for="(item) in gridList"
      :key="item.ip"
      class="ip-grid-item"
      :style="{
        width: gridItemSize + 'px',
        height: gridItemSize + 'px',
        backgroundColor: `${STATUS_COLOR[item._ip_status]}22`,
        color: STATUS_COLOR[item._ip_status],
        borderColor: STATUS_COLOR[item._ip_status]
      }"
      @click="clickGridItem(item, $event)"
    >
      {{ item.gridTitle }}
    </div>

    <div
      v-show="infoCardVisible"
      class="info-card"
      :style="{
        top: infoCardY + 'px',
        left: infoCardX + 'px',
        width: infoCardWidth + 'px',
        height: infoCardHeight + 'px',
      }"
    >
      <div class="info-card-header">
        <div class="info-card-ip">
          {{ infoCardData.ip }}
        </div>
        <div
          class="info-card-status-dot"
          :style="{
            backgroundColor: `${STATUS_COLOR[infoCardData._ip_status]}22`
          }"
        >
          <div
            class="info-card-status-dot-content"
            :style="{
              backgroundColor: STATUS_COLOR[infoCardData._ip_status]
            }"
          ></div>
        </div>

        <div class="info-card-status-text">
          {{ $t(STATUS_LABEL[infoCardData._ip_status]) }}
        </div>

        <a-button
          type="primary"
          class="ops-button-ghost info-card-recycle"
          ghost
          @click="clickRecycle(infoCardData)"
        >
          <ops-icon type="veops-recycle" />
          {{ $t('cmdb.ipam.recycle') }}
        </a-button>
      </div>
      <div class="info-card-main">
        <div
          v-for="(col) in filterColumns"
          :key="col.field"
          class="info-card-main-row"
        >
          <div class="info-card-main-title">
            <a-tooltip :title="col.title">
              {{ col.title }}
            </a-tooltip>
          </div>
          <div class="info-card-main-value">
            <a-tooltip :title="infoCardTip[col.field]" placement="topLeft" >
              <template v-if="col.is_reference && infoCardData[col.field]" >
                <a
                  v-for="(ciId) in (col.is_list ? infoCardData[col.field] : [infoCardData[col.field]])"
                  :key="ciId"
                  :href="`/cmdb/cidetail/${col.reference_type_id}/${ciId}`"
                  target="_blank"
                >
                  {{ getReferenceAttrValue(ciId, col) }}
                </a>
              </template>
              <template v-else-if="col.is_link && infoCardData[col.field]">
                <a
                  v-for="(linkItem, linkIndex) in (col.is_list ? infoCardData[col.field] : [infoCardData[col.field]])"
                  :key="linkIndex"
                  :href="
                    linkItem.startsWith('http') || linkItem.startsWith('https')
                      ? `${linkItem}`
                      : `http://${linkItem}`
                  "
                  target="_blank"
                >
                  {{ getChoiceValueLabel(col, linkItem) || linkItem }}
                </a>
              </template>
              <template v-else-if="col.is_choice && infoCardData[col.field]">
                <span
                  v-for="value in (col.is_list ? infoCardData[col.field] : [infoCardData[col.field]])"
                  :key="value"
                  class="column-default-choice"
                >
                  {{ getChoiceValueLabel(col, value) || value }}
                </span>
              </template>
              <template v-else>
                {{ infoCardData[col.field] !== undefined ? Array.isArray(infoCardData[col.field]) ? infoCardData[col.field].join(', ') : infoCardData[col.field] : '' }}
              </template>
            </a-tooltip>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { STATUS_COLOR, STATUS_LABEL, ADDRESS_STATUS } from './constants.js'

export default {
  name: 'GridIP',
  props: {
    ipList: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    referenceShowAttrNameMap: {
      type: Object,
      default: () => {}
    },
    referenceCIIdMap: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      STATUS_COLOR,
      STATUS_LABEL,

      gridItemSize: 52, //
      gridGap: 8,

      infoCardX: 0,
      infoCardY: 0,
      infoCardWidth: 375,
      infoCardVisible: false,
      infoCardData: {},
      infoCardTip: {}
    }
  },
  computed: {
    gridList() {
      const list = this.ipList.map((item) => {
        const ipSplit = item?.ip?.split('.') || []
        const gridTitle = ipSplit?.[ipSplit.length - 1] || ''

        return {
          ...item,
          gridTitle
        }
      })

      return list
    },
    filterColumns() {
      return this.columns.filter((col) => col.field !== '_ip_status') || []
    },
    infoCardHeight() {
      let infoCardHeight = 311
      if (this.filterColumns.length < 6) {
        infoCardHeight -= ((6 - this.filterColumns.length) * 36)
      }

      return infoCardHeight
    }
  },
  mounted() {
    window.addEventListener('click', this.handleClick)
  },
  beforeDestroy() {
    window.removeEventListener('click', this.handleClick)
  },
  methods: {
    handleClick(event) {
      const classStr = event?.target?.classList?.value
      if (classStr.indexOf('info-card') === -1 && classStr.indexOf('ip-grid-item') === -1) {
        this.infoCardVisible = false
      }
    },

    clickGridItem(item, event) {
      if ([ADDRESS_STATUS.OFFLINE_UNASSIGNED, ADDRESS_STATUS.ONLINE_UNASSIGNED].includes(item?._ip_status)) {
        this.$emit('openAssign', item)
      } else {
        this.showInfoCard(item, event)
      }
    },

    showInfoCard(item, event) {
      let infoCardX = event.clientX - event.offsetX
      let infoCardY = event.clientY - event.offsetY + this.gridItemSize + this.gridGap

      // 右侧是否超出视口边界
      if (infoCardX + this.infoCardWidth > window.innerWidth) {
        infoCardX = infoCardX + this.gridItemSize - this.infoCardWidth
      }

      // 底部是否超出视口边界
      if (infoCardY + this.infoCardHeight > window.innerHeight) {
        infoCardY = infoCardY - this.gridItemSize - this.gridGap * 2 - this.infoCardHeight
      }

      const infoCardTip = {}
      this.filterColumns.forEach((col) => {
        const arrayValue = Array.isArray(item[col.field]) ? item[col.field] : [item[col.field]]
        infoCardTip[col.field] = arrayValue.map((value) => {
          if (value === undefined || value === null) {
            return value
          }

          if (col.is_reference) {
            return this.getReferenceAttrValue(value, col) || value
          }
          if (col.is_link || col.is_choice) {
            return this.getChoiceValueLabel(col, value) || value
          }
          return value
        }).join(', ')
      })

      this.infoCardX = infoCardX
      this.infoCardY = infoCardY
      this.infoCardVisible = true
      this.infoCardData = item
      this.infoCardTip = infoCardTip
    },

    clickRecycle(data) {
      this.$emit('recycle', data.ip)
    },

    getReferenceAttrValue(id, col) {
      const ci = this?.referenceCIIdMap?.[col?.reference_type_id]?.[id]
      if (!ci) {
        return id
      }

      const attrName = this.referenceShowAttrNameMap?.[col.reference_type_id]
      return ci?.[attrName] || id
    },

    getChoiceValueLabel(col, colValue) {
      const _find = col?.choice_value?.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find?.[1]?.label || ''
      }
      return ''
    },
  }
}
</script>

<style lang="less" scoped>
.ip-grid {
  display: flex;
  flex-wrap: wrap;

  max-height: calc(100vh - 230px);
  overflow-y: auto;
  overflow-x: hidden;

  &-item {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 400;
    cursor: pointer;

    &:hover {
      border-style: solid;
      border-width: 1px;
    }
  }

  .info-card {
    position: fixed;
    top: 0;
    left: 0;
    transition: top 0.2s, left 0.2s;
    padding: 23px 18px;

    border-radius: 2px;
    background-color: #FFFFFF;
    box-shadow: -2px 4px 12px 0px rgba(168, 191, 211, 0.25);

    &-header {
      display: flex;
      align-items: center;
    }

    &-ip {
      font-size: 18px;
      font-weight: 700;
      color: #2F54EB;
    }

    &-status-dot {
      width: 12px;
      height: 12px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: 14px;

      &-content {
        width: 6px;
        height: 6px;
        border-radius: 6px;
      }
    }

    &-status-text {
      font-size: 12px;
      font-weight: 400;
      color: #4E5969;
      margin-left: 4px;
    }

    &-recycle {
      margin-left: auto;
    }

    &-main {
      margin-top: 15px;
      width: 100%;
      border: solid 1px #F0F1F5;
      border-bottom-style: none;
      max-height: calc(100% - 47px);
      overflow-y: auto;
      overflow-x: hidden;

      &-row {
        height: 36px;
        line-height: 36px;
        display: flex;
        align-items: center;
      }

      &-title {
        border-right: solid 1px #F0F1F5;
        background-color: #F7F8FA;
        padding-left: 17px;
        padding-right: 10px;
        width: 32%;
        height: 100%;
        flex-shrink: 0;

        font-size: 14px;
        font-weight: 400;
        color: #4E5969;
        overflow: hidden;
        text-overflow: ellipsis;
        text-wrap: nowrap;
        border-bottom: solid 1px #E4E7ED;
      }

      &-value {
        width: 68%;
        flex-shrink: 0;
        padding-left: 18px;
        padding-right: 10px;
        height: 100%;

        font-size: 14px;
        font-weight: 400;
        color: #4E5969;
        overflow: hidden;
        text-overflow: ellipsis;
        text-wrap: nowrap;
        border-bottom: solid 1px #F0F1F5;
      }
    }
  }
}
</style>
