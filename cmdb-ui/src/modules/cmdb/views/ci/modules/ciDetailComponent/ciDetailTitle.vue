<template>
  <div class="ci-detail-title-card">
    <div class="ci-detail-title-main">
      <CIIcon :icon="icon" size="24" />
      <span class="ci-detail-title-text">{{ title }}</span>
    </div>
    <div class="ci-detail-title-meta">
      <div class="ci-detail-title-meta-item" v-if="ci._id">
        <span class="meta-label">CI ID:</span>
        <span class="meta-value">{{ ci._id }}</span>
      </div>
      <div class="ci-detail-title-meta-item" v-if="ci[CI_DEFAULT_ATTR.UPDATE_TIME]">
        <span class="meta-label">{{ $t('cmdb.components.updateTime') }}:</span>
        <span class="meta-value">{{ ci[CI_DEFAULT_ATTR.UPDATE_TIME] }}</span>
      </div>
      <div class="ci-detail-title-meta-item" v-if="ci[CI_DEFAULT_ATTR.UPDATE_USER]">
        <span class="meta-label">{{ $t('cmdb.components.updater') }}:</span>
        <span class="meta-value">{{ ci[CI_DEFAULT_ATTR.UPDATE_USER] }}</span>
      </div>
      <div class="ci-detail-title-meta-item ci-detail-title-meta-item-citype" v-if="findCIType.alias">
        <span class="meta-label">{{ $t('cmdb.ciType.ciType') }}:</span>
        <a-tag color="blue">
          {{ findCIType.alias }}
        </a-tag>
      </div>
    </div>
  </div>
</template>

<script>
import { CI_DEFAULT_ATTR } from '@/modules/cmdb/utils/const.js'

import CIIcon from '@/modules/cmdb/components/ciIcon'

export default {
  name: 'CIDetailTitle',
  components: {
    CIIcon
  },
  props: {
    ci: {
      type: Object,
      default: () => {}
    },
    ci_types: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      icon: '',
      title: '',
      CI_DEFAULT_ATTR
    }
  },
  computed: {
    findCIType() {
      return this.ci_types?.find?.((item) => item?.id === this.ci?._type) || {}
    }
  },
  watch: {
    findCIType: {
      deep: true,
      immediate: true,
      handler(val) {
        this.icon = val?.icon || ''
        this.title = this?.ci?.[val?.show_name] || this?.ci?.[val?.unique_key] || ''
      },
    }
  }
}
</script>

<style lang="less" scoped>
.ci-detail-title-card {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border: 1px solid #e8eaed;
}

.ci-detail-title-main {
  display: flex;
  align-items: center;
  column-gap: 12px;
  flex-shrink: 0;
  min-width: 0;
}

.ci-detail-title-text {
  font-size: 18px;
  font-weight: 600;
  color: @text-color_1;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ci-detail-title-meta {
  display: flex;
  align-items: center;
  column-gap: 20px;
  row-gap: 6px;
  flex-wrap: nowrap;
  max-width: 100%;
  overflow: hidden;
}

.ci-detail-title-meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
  flex-shrink: 0;

  &-citype {
    flex-shrink: 1;

    .ant-tag {
      border-radius: 4px;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap-mode: nowrap;
    }
  }

  .meta-label {
    font-size: 12px;
    color: @text-color_3;
    font-weight: 500;
    flex-shrink: 0;
  }

  .meta-value {
    font-size: 12px;
    color: @text-color_2;
    background: #f5f7fa;
    padding: 2px 8px;
    border-radius: 4px;
  }
}
</style>
