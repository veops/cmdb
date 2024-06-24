<template>
  <div
    :class="{
      'discovery-card': true,
      'discovery-card-http': rule.type === DISCOVERY_CATEGORY_TYPE.HTTP,
      'discovery-card-small': isSelected,
      'discovery-card-small-selected': isSelected && selectedIds().findIndex((item) => item.id === rule.id) > -1,
    }"
    @click="clickCard"
  >
    <div
      class="discovery-card-inner"
      v-if="rule.is_inner"
    >
      <span class="discovery-card-inner-text">{{ $t('cmdb.ad.innerFlag') }}</span>
    </div>
    <div
      class="discovery-background-top"
      :style="{ background: borderTopColorMap[rule.name] || '' }"
    ></div>
    <div class="discovery-top">
      <div class="discovery-header">
        <img
          v-if="icon.id && icon.url"
          class="discovery-header-icon"
          :src="`/api/common-setting/v1/file/${icon.url}`"
        />
        <ops-icon
          v-else
          :type="icon.name || 'caise-chajian'"
          :style="{ color: icon.color }"
          class="discovery-header-icon"
        />
        <span :title="rule.name">{{ rule.name }}</span>
      </div>
      <template v-if="!isSelected">
        <div
          class="discovery-resources"
          v-if="rule.type === DISCOVERY_CATEGORY_TYPE.HTTP && rule.resources.length"
        >
          <a-tooltip>
            <template slot="title">
              {{ $t('cmdb.ad.discoveryCardResoureTip') }}
            </template>
            <div class="discovery-resources-left">
              <ops-icon class="discovery-resources-icon" type="cmdb-discovery_resources" />
              <span class="discovery-resources-count">{{ rule.resources.length }}{{ $i18n.locale === 'zh' ? '个' : '' }}</span>
            </div>
          </a-tooltip>
          <div class="discovery-resources-right">
            <template v-for="(item, index) in rule.resources">
              <span
                :key="index"
                v-if="index < 2"
                class="discovery-resources-item"
                :style="{ maxWidth: rule.resources.length >= 2 ? '70px' : '160px' }"
              >
                {{ item }}
              </span>
            </template>
            <span v-if="rule.resources.length > 2" class="discovery-resources-item">
              <ops-icon type="veops-more" />
            </span>
          </div>
        </div>
        <a-divider
          :style="{ margin: rule.type === DISCOVERY_CATEGORY_TYPE.HTTP ? '10px 0' : '7px 0' }"
        />
        <div class="discovery-footer">
          <a-space v-if="rule.type === 'agent' && rule.is_plugin">
            <a @click="handleEdit">
              <a-icon type="edit" />
            </a>
            <a
              v-if="isDeletable"
              @click="handleDelete"
              :style="{ color: 'red' }"
            >
              <a-icon type="delete" />
            </a>
          </a-space>
          <a v-else @click="handleEdit"><a-icon type="eye"/></a>
          <span>{{ rule.is_plugin ? 'Plugin' : $t('cmdb.custom_dashboard.default') }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { DISCOVERY_CATEGORY_TYPE } from './constants.js'

export default {
  name: 'DiscoveryCard',
  props: {
    rule: {
      type: Object,
      default: () => {},
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      DISCOVERY_CATEGORY_TYPE,
      borderTopColorMap: {
        '阿里云': '#FFB287',
        '腾讯云': '#87BEFF',
        '华为云': '#FFB8B8',
        'AWS': '#FFC187',
      }
    }
  },
  computed: {
    icon() {
      return this.rule?.option?.icon ?? { color: '', name: 'caise-wuliji' }
    },
    isDeletable() {
      return ![this.$t('cmdb.ad.server'), this.$t('cmdb.ad.vserver'), this.$t('cmdb.ad.nic'), this.$t('cmdb.ad.disk'), 'server', 'vserver', 'NIC', 'harddisk'].includes(this.rule.name)
    },
  },
  inject: {
    setSelectedIds: {
      from: 'setSelectedIds',
      default: () => {},
    },
    selectedIds: {
      default: () => [],
    },
  },
  methods: {
    handleEdit() {
      this.$emit('editRule')
    },
    handleDelete() {
      this.$emit('deleteRule')
    },
    clickCard() {
      if (this.setSelectedIds) {
        this.setSelectedIds(this.rule.id, this.rule.type)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.discovery-card {
  display: inline-block;
  width: 180px;
  height: 105px;
  box-shadow: 0px 2px 8px rgba(122, 140, 204, 0.25);
  border-radius: 4px;
  position: relative;
  margin-bottom: 40px;
  margin-right: 40px;

  &-inner {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 4;

    width: 50px;
    height: 30px;
    border-left: 50px solid transparent;
    border-top: 30px solid @primary-color_4;

    &-text {
      width: 30px;
      position: absolute;
      top: -28px;
      right: 3px;
      text-align: right;

      color: @primary-color;
      font-size: 10px;
      font-weight: 400;
    }
  }

  .discovery-background-top {
    width: 100%;
    height: 10px;
    position: absolute;
    left: 0;
    top: 0;
    z-index: 1;
    background: linear-gradient(90.54deg, #879fff 1.32%, #a0ddff 99.13%);
    border-radius: 4px 4px 0 0;
  }

  .discovery-top {
    width: 100%;
    height: calc(100% - 5px);
    position: absolute;
    left: 0;
    top: 5px;
    z-index: 1;
    background-color: #fff;
    z-index: 2;
    border-radius: 4px;
    padding: 12px;
    .discovery-header {
      width: 100%;
      height: 45px;
      display: flex;
      align-items: center;
      > i {
        margin-right: 10px;
      }
      > span {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        color: #000;
      }

      &-icon {
        font-size: 22px;
        max-height: 22px;
        max-width: 22px;
      }
    }

    .discovery-resources {
      display: flex;
      justify-content: space-between;
      align-items: center;

      &-count {
        margin-left: 3px;
        color: @text-color_3;
        font-size: 12px;
        font-weight: 400;
        flex-shrink: 0;
      }

      &-right {
        display: flex;
        align-items: center;
      }

      &-item {
        padding: 3px 6px;
        border-radius: 12px;
        background-color: @layout-content-background;

        color: @text-color_3;
        font-size: 11px;
        font-weight: 400;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;

        &:not(:last-child) {
          margin-right: 6px;
        }
      }
    }

    .discovery-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      > span {
        color: #86909c;
        background-color: #f0f5ff;
        border-radius: 2px;
        padding: 2px 8px;
        font-size: 11px;
      }
    }
  }

  &-http {
    width: 263px;
    height: 142px;

    .discovery-header {
      &-icon {
        font-size: 30px !important;
        max-height: 30px !important;
        max-width: 30px !important;
      }
    }
  }
}
.discovery-card-small {
  width: 170px;
  height: 80px;
  cursor: pointer;
  // &:hover {
  //   .discovery-top {
  //     background-color: #f0f1f5;
  //   }
  // }
}
.discovery-card-small:hover,
.discovery-card-small-selected {
  .discovery-top {
    background-color: #f0f1f5;
  }
}
</style>
