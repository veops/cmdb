<template>
  <CustomDrawer
    :hasFooter="false"
    :title="$t('acl.viewMatchResult')"
    :visible="patternVisible"
    width="500"
    @close="
      () => {
        patternVisible = false
      }
    "
  >
    <vxe-table
      size="mini"
      stripe
      class="ops-stripe-table"
      :data="tableData"
      :max-height="`${windowHeight - 110}px`">
      <vxe-table-column field="name" :title="$t('acl.resourceName')"></vxe-table-column>
      <vxe-table-column field="uid" :title="$t('acl.creator')">
        <template #default="{row}">
          {{ getRoleName(row.uid) }}
        </template>
      </vxe-table-column>
      <vxe-table-column field="created_at" :title="$t('created_at')"></vxe-table-column>
      <template slot="empty">
        <img :src="require(`@/assets/data_empty.png`)" />
        <p style="font-size: 14px; line-height: 17px; color: rgba(0, 0, 0, 0.6)">{{ $t('noData') }}</p>
      </template>
    </vxe-table>
  </CustomDrawer>
</template>

<script>
import { mapState } from 'vuex'
import { patternResults } from '@/modules/acl/api/trigger'
export default {
  name: 'TriggerPattern',
  props: {
    roles: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      patternVisible: false,
      tableData: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: state => state.windowHeight,
    }),
  },
  methods: {
    open(params) {
      patternResults(params).then(res => {
        this.patternVisible = true
        this.tableData = res
      })
    },
    getRoleName(uid) {
      if (uid) {
        const _find = this.roles.find(item => item.uid === uid)
        if (_find) {
          return _find.name
        }
        return ''
      }
      return ''
    },
  },
}
</script>

<style></style>
