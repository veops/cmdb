<template>
  <div class="rack-table">
    <CITable
      ref="xTable"
      :attrList="preferenceAttrList"
      :columns="columns"
      :data="rackList"
      :height="tableHeight"
      :sortConfig="{ remote: false, trigger: 'default' }"
      :showCheckbox="false"
      :showOperation="false"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex'

import CITable from '@/modules/cmdb/components/ciTable/index.vue'

export default {
  name: 'RackTable',
  components: {
    CITable
  },
  props: {
    rackList: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    },
    preferenceAttrList: {
      type: Array,
      default: () => {}
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      return `${this.windowHeight - 295}px`
    },
  }
}
</script>

<style lang="less" scoped>
</style>
