<template>
  <span :class="['operate-type-text', typeClass]">
    <a-icon v-if="showIcon" :type="iconType" class="type-icon" />
    <span>{{ operateType }}</span>
  </span>
</template>

<script>
export default {
  name: 'OperateTypeTag',
  props: {
    operateType: {
      type: String,
      required: true
    },
    showIcon: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    typeClass() {
      const type = this.operateType.toLowerCase()
      if (type.includes(this.$t('new').toLowerCase())) {
        return 'type-new'
      }
      if (type.includes(this.$t('update').toLowerCase())) {
        return 'type-update'
      }
      return 'type-delete'
    },
    iconType() {
      const type = this.operateType.toLowerCase()
      if (type.includes(this.$t('new').toLowerCase())) {
        return 'plus-circle'
      }
      if (type.includes(this.$t('update').toLowerCase())) {
        return 'edit'
      }
      return 'delete'
    }
  }
}
</script>

<style lang="less" scoped>
.operate-type-text {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  line-height: 22px;
  font-weight: 400;
  white-space: nowrap;

  .type-icon {
    font-size: 14px;
  }

  &.type-new {
    color: #52c41a;

    .type-icon {
      color: #52c41a;
    }
  }

  &.type-update {
    color: #fa8c16;

    .type-icon {
      color: #fa8c16;
    }
  }

  &.type-delete {
    color: #f5222d;

    .type-icon {
      color: #f5222d;
    }
  }
}
</style>
