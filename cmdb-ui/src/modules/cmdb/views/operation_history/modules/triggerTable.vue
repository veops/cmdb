<template>
  <div class="operation-history-table">
    <vxe-table
      show-overflow
      show-header-overflow
      stripe
      size="small"
      class="ops-stripe-table"
      :loading="loading"
      :data="tableData"
      v-bind="ci_id ? { height: 'auto' } : { 'max-height': `${windowHeight - 290}px` }"
    >
      <template #empty>
        <a-empty :image-style="{ height: '100px' }" :style="{ paddingTop: '10%' }">
          <img slot="image" :src="require('@/assets/data_empty.png')" />
          <span slot="description">{{ $t('noData') }}</span>
        </a-empty>
      </template>
      <vxe-column field="trigger_name" min-width="150" :title="$t('cmdb.history.triggerName')"></vxe-column>
      <vxe-column field="type" min-width="120" :title="$t('type')">
        <template #default="{ row }">
          {{ getTriggerType(row) }}
        </template>
      </vxe-column>
      <vxe-column min-width="120" :title="$t('cmdb.history.event')">
        <template #default="{ row }">
          {{ getEventType(row) }}
        </template>
      </vxe-column>
      <vxe-column min-width="100" :title="$t('cmdb.history.action')">
        <template #default="{ row }">
          {{ getActionType(row) }}
        </template>
      </vxe-column>
      <vxe-column min-width="80" :title="$t('cmdb.history.status')">
        <template #default="{ row }">
          <a-tag :color="row.is_ok ? 'green' : 'red'">
            {{ row.is_ok ? $t('cmdb.history.done') : $t('cmdb.history.undone') }}
          </a-tag>
        </template>
      </vxe-column>
      <vxe-column min-width="160" :title="$t('cmdb.history.triggerTime')">
        <template #default="{ row }">
          {{ row.updated_at || row.created_at }}
        </template>
      </vxe-column>
    </vxe-table>
    <pager
      v-if="!ci_id"
      :current-page.sync="tablePage.currentPage"
      :page-size.sync="tablePage.pageSize"
      :page-sizes="PAGE_SIZE_OPTIONS"
      :total="tablePage.totalResult"
      :isLoading="loading"
      @change="onChange"
      @showSizeChange="onShowSizeChange"
    ></pager>
  </div>
</template>

<script>
import Pager from '@/components/Pager'
import { getCiTriggers, getCiTriggersByCiId } from '@/modules/cmdb/api/history'
import { PAGINATION_CONFIG } from '../constants'
import commonMixin from '../mixins/commonMixin'

export default {
  name: 'TriggerTable',
  components: { Pager },
  mixins: [commonMixin],
  props: {
    ci_id: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      tableData: [],
      tablePage: {
        currentPage: 1,
        pageSize: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
        totalResult: 0,
      },
      PAGE_SIZE_OPTIONS: PAGINATION_CONFIG.PAGE_SIZE_OPTIONS
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    operateTypeMap() {
      return {
        '0': this.$t('cmdb.ciType.addInstance'),
        '1': this.$t('cmdb.ciType.deleteInstance'),
        '2': this.$t('cmdb.ciType.changeInstance'),
      }
    },
  },
  mounted() {
    this.updateTableData()
  },
  methods: {
    async updateTableData(currentPage = 1, pageSize = this.tablePage.pageSize) {
      try {
        this.loading = true
        const params = { page: currentPage, page_size: pageSize }

        if (this.ci_id) {
          const res = await getCiTriggersByCiId(this.ci_id, params)
          this.tableData = res.items.map((item) => ({
            ...item,
            trigger: res.id2trigger[item.trigger_id],
          }))
        } else {
          const res = await getCiTriggers(params)
          this.tableData = res?.result || []
          this.tablePage = {
            currentPage: res.page,
            pageSize: res.page_size,
            totalResult: res.numfound,
          }
        }
      } catch (error) {
        this.handleError(error, 'fetch trigger history')
      } finally {
        this.loading = false
      }
    },

    onChange(pageNum) {
      this.updateTableData(pageNum, this.tablePage.pageSize)
    },

    onShowSizeChange(size) {
      this.updateTableData(1, size)
    },

    getTriggerType(row) {
      if (!row.trigger) return ''
      return row.trigger.attr_id
        ? this.$t('cmdb.ciType.triggerDate')
        : this.$t('cmdb.ciType.triggerDataChange')
    },

    getEventType(row) {
      return this.operateTypeMap[row.operate_type] || ''
    },

    getActionType(row) {
      if (row.webhook) return 'Webhook'
      if (row.notify) return this.$t('cmdb.ciType.notify')
      return ''
    },
  },
}
</script>

<style lang="less" scoped>
@import '../styles/table.less';
</style>
