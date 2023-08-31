<template>
  <div
    :class="{
      'discovery-card': true,
      'discovery-card-small': isSelected,
      'discovery-card-small-selected': isSelected && selectedIds().findIndex((item) => item.id === rule.id) > -1,
    }"
    @click="clickCard"
  >
    <div class="discovery-bottom"></div>
    <div class="discovery-top">
      <div class="discovery-header">
        <img
          v-if="icon.id && icon.url"
          :src="`/api/common-setting/v1/file/${icon.url}`"
          :style="{ maxHeight: '30px', maxWidth: '30px' }"
        />
        <ops-icon v-else :type="icon.name || 'caise-chajian'" :style="{ fontSize: '30px', color: icon.color }" />
        <span :title="rule.name">{{ rule.name }}</span>
      </div>
      <template v-if="!isSelected">
        <a-divider :style="{ margin: '5px 0' }" />
        <div class="discovery-footer">
          <a-space v-if="rule.type === 'agent'">
            <a @click="handleEdit"><ops-icon type="icon-xianxing-edit"/></a>
            <a
              v-if="isDeletable"
              @click="handleDelete"
              :style="{ color: 'red' }"
            ><ops-icon
              type="icon-xianxing-delete"
            /></a>
          </a-space>
          <a v-else @click="handleEdit"><a-icon type="eye"/></a>
          <span>{{ rule.is_plugin ? 'Plugin' : '默认' }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
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
  computed: {
    icon() {
      return this.rule?.option?.icon ?? { color: '', name: 'caise-wuliji' }
    },
    isDeletable() {
      return !['物理机', '虚拟机', '网卡', '硬盘', 'server', 'vserver', 'NIC', 'harddisk'].includes(this.rule.name)
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
  .discovery-bottom {
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
      height: 50px;
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
    }
    .discovery-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      > span {
        color: #a5a9bc;
        background-color: #d8eaff;
        border-radius: 2px;
        padding: 0 5px;
        font-size: 12px;
      }
    }
  }
}
.discovery-card-small {
  width: 170px;
  height: 80px;
  cursor: pointer;
}
.discovery-card-small:hover,
.discovery-card-small-selected {
  .discovery-top {
    background-color: #f0f1f5;
  }
}
</style>
