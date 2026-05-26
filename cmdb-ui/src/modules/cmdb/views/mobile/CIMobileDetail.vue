<template>
  <div class="mobile-detail-page">
    <div class="mobile-header">
      <a-icon type="arrow-left" class="mobile-back-btn" @click="goBack" />
      <span class="mobile-header-title">
        {{ typeInfo.alias || typeInfo.name || $t('cmdb.ci.mobileDetail') }}
      </span>
      <span class="mobile-header-right"></span>
    </div>

    <div v-if="loading" class="mobile-loading">
      <a-spin size="large" />
      <p>{{ $t('loading') }}</p>
    </div>

    <div v-else-if="!hasPermission" class="mobile-empty">
      <a-empty :image-style="{ height: '80px' }">
        <span slot="description">{{ $t('cmdb.ci.noPermission') }}</span>
      </a-empty>
    </div>

    <div v-else class="mobile-content">
      <div class="mobile-card">
        <div class="mobile-card-title">
          <a-icon type="info-circle" />
          {{ $t('cmdb.ci.coreInfo') }}
          <span class="mobile-card-title-ciid">#{{ ci._id }}</span>
        </div>
        <div class="mobile-card-body">
          <div
            v-for="entry in coreAttrEntries"
            :key="entry.name"
            :class="['mobile-attr-row', entry._isLongValue ? 'mobile-attr-row-stacked' : '']"
          >
            <span class="mobile-attr-label">{{ entry.alias }}</span>
            <span class="mobile-attr-value">{{ entry.value }}</span>
          </div>
        </div>
      </div>

      <div class="mobile-card" v-if="parentRelations.length">
        <div class="mobile-card-title">
          <a-icon type="arrow-up" />
          {{ $t('cmdb.ci.parentRelations') }}
        </div>
        <div class="mobile-card-body">
          <div
            class="mobile-relation-item"
            v-for="(item, idx) in parentRelations"
            :key="'p-' + idx"
            @click="goToCI(item._type, item._id)"
          >
            <a-icon type="link" class="mobile-relation-icon" />
            <div class="mobile-relation-info">
              <span class="mobile-relation-type">{{ item._type_name || '' }}</span>
              <span class="mobile-relation-name">{{ getCIName(item) }}</span>
            </div>
            <a-icon type="right" class="mobile-relation-arrow" />
          </div>
        </div>
      </div>

      <div class="mobile-card" v-if="childRelations.length">
        <div class="mobile-card-title">
          <a-icon type="arrow-down" />
          {{ $t('cmdb.ci.childRelations') }}
        </div>
        <div class="mobile-card-body">
          <div
            class="mobile-relation-item"
            v-for="(item, idx) in childRelations"
            :key="'c-' + idx"
            @click="goToCI(item._type, item._id)"
          >
            <a-icon type="link" class="mobile-relation-icon" />
            <div class="mobile-relation-info">
              <span class="mobile-relation-type">{{ item._type_name || '' }}</span>
              <span class="mobile-relation-name">{{ getCIName(item) }}</span>
            </div>
            <a-icon type="right" class="mobile-relation-arrow" />
          </div>
        </div>
      </div>

      <div class="mobile-card" v-if="historyList.length">
        <div class="mobile-card-title">
          <a-icon type="clock-circle" />
          {{ $t('cmdb.ci.recentHistory') }}
        </div>
        <div class="mobile-card-body">
          <div class="mobile-history-item" v-for="(h, idx) in historyList" :key="'h-' + idx">
            <div class="mobile-history-meta">
              <a-tag :color="h._operateColor">{{ h._operateLabel }}</a-tag>
              <span class="mobile-history-attr">{{ h.attr_alias || h.attr_name }}</span>
            </div>
            <div class="mobile-history-values" v-if="h.old || h.new">
              <span class="mobile-history-old">{{ formatValue(h.old) || '-' }}</span>
              <a-icon type="arrow-right" class="mobile-history-arrow-icon" />
              <span class="mobile-history-new">{{ formatValue(h.new) || '-' }}</span>
            </div>
            <div class="mobile-history-time">
              {{ h.created_at }}
              <span class="mobile-history-user">by {{ h.username }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getCIMobileDetail } from '@/modules/cmdb/api/ci'

export default {
  name: 'CIMobileDetail',
  data() {
    return {
      typeId: null,
      ciId: null,
      ci: {},
      typeInfo: {},
      attrAliasMap: {},
      parentRelations: [],
      childRelations: [],
      historyList: [],
      loading: true,
      hasPermission: true
    }
  },
  computed: {
    coreAttrEntries() {
      const ci = this.ci || {}
      const aliasMap = this.attrAliasMap || {}
      const excludeKeys = new Set(['_id', '_type', 'ci_type', 'ci_type_alias', 'unique', 'unique_alias',
        '_updated_at', '_updated_by', '__ci_type_name__'])
      const entries = []

      Object.keys(ci).forEach((key) => {
        if (!excludeKeys.has(key) && !key.startsWith('__') && !key.startsWith('_')) {
          const value = ci[key]
          if (value !== null && value !== undefined && value !== '') {
            const alias = aliasMap[key] || key
            const strValue = this.formatValue(value)
            entries.push({
              name: key,
              alias: alias,
              value: strValue,
              _isLongValue: strValue.length > 24
            })
          }
        }
      })

      return entries
    }
  },
  mounted() {
    this.typeId = Number(this.$route.params.typeId)
    this.ciId = Number(this.$route.params.ciId)
    if (this.ciId) {
      this.fetchData()
    }
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getCIMobileDetail(this.ciId)
        this.ci = res.ci || {}
        this.typeInfo = res.type || {}
        this.attrAliasMap = res.attribute_alias_map || {}
        this.parentRelations = (res.relations && res.relations.parents) || []
        this.childRelations = (res.relations && res.relations.children) || []
        this.historyList = (res.history || []).map((h) => {
          const colors = { '0': 'green', '1': 'red', '2': 'blue' }
          const labels = { '0': this.$t('new'), '1': this.$t('delete'), '2': this.$t('update') }
          return {
            ...h,
            _operateColor: colors[h.operate_type] || 'default',
            _operateLabel: labels[h.operate_type] || h.operate_type
          }
        })
        this.hasPermission = true
      } catch (e) {
        if (e.response && e.response.status === 403 || e.response && e.response.status === 404) {
          this.hasPermission = false
        }
      } finally {
        this.loading = false
      }
    },
    formatValue(value) {
      if (value === null || value === undefined) return '-'
      if (typeof value === 'object') return JSON.stringify(value)
      return String(value)
    },
    getCIName(ci) {
      if (!ci) return ''
      return ci.name || ci.alias || ci.hostname || ci.ip || ci._id || ''
    },
    goToCI(typeId, ciId) {
      if (typeId != null && ciId != null) {
        this.$router.push(`/cmdb/mobile/${typeId}/${ciId}`)
      }
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style lang="less" scoped>
.mobile-detail-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding-bottom: 32px;
  -webkit-overflow-scrolling: touch;
}

.mobile-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 48px;
  padding: 0 16px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
}

.mobile-back-btn {
  font-size: 18px;
  color: #333;
  flex-shrink: 0;
}

.mobile-header-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
  flex: 1;
  padding: 0 8px;
}

.mobile-header-right {
  width: 18px;
  flex-shrink: 0;
}

.mobile-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: #999;
}

.mobile-empty {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
}

.mobile-content {
  padding: 12px;
}

.mobile-card {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.mobile-card-title {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;

  .anticon {
    margin-right: 6px;
    color: @primary-color;
  }
}

.mobile-card-title-ciid {
  margin-left: auto;
  font-size: 12px;
  font-weight: 400;
  color: #bbb;
}

.mobile-card-body {
  padding: 0;
}

.mobile-attr-row {
  display: flex;
  align-items: flex-start;
  padding: 10px 16px;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  &.mobile-attr-row-stacked {
    flex-direction: column;
    gap: 4px;
  }
}

.mobile-attr-label {
  min-width: 80px;
  max-width: 40%;
  flex-shrink: 0;
  font-size: 13px;
  color: #999;
  line-height: 1.5;

  .mobile-attr-row-stacked & {
    max-width: 100%;
    margin-bottom: 2px;
  }
}

.mobile-attr-value {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  color: #333;
  word-break: break-word;
  overflow-wrap: break-word;
  line-height: 1.5;

  .mobile-attr-row-stacked & {
    padding-left: 0;
  }
}

.mobile-relation-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: #f5f5f5;
  }
}

.mobile-relation-icon {
  font-size: 14px;
  color: @primary-color;
  margin-right: 10px;
  flex-shrink: 0;
}

.mobile-relation-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mobile-relation-type {
  font-size: 11px;
  color: #999;
  background: #f0f0f0;
  padding: 1px 6px;
  border-radius: 3px;
  align-self: flex-start;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-relation-name {
  font-size: 13px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.mobile-relation-arrow {
  font-size: 12px;
  color: #ccc;
  margin-left: 8px;
  flex-shrink: 0;
}

.mobile-history-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
}

.mobile-history-meta {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  flex-wrap: wrap;
  gap: 6px;
}

.mobile-history-attr {
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

.mobile-history-values {
  display: flex;
  align-items: flex-start;
  font-size: 12px;
  margin-bottom: 4px;
  gap: 4px;
}

.mobile-history-old {
  color: #ff4d4f;
  background: #fff1f0;
  padding: 2px 8px;
  border-radius: 3px;
  max-width: 45%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex-shrink: 0;
}

.mobile-history-arrow-icon {
  margin-top: 3px;
  font-size: 11px;
  color: #999;
  flex-shrink: 0;
}

.mobile-history-new {
  color: #52c41a;
  background: #f6ffed;
  padding: 2px 8px;
  border-radius: 3px;
  max-width: 45%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex-shrink: 0;
}

.mobile-history-time {
  font-size: 11px;
  color: #bbb;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mobile-history-user {
  margin-left: 8px;
}
</style>
