<template>
  <div class="cmdb-batch-upload-table">
    <vxe-table
      stripe
      show-header-overflow
      show-overflow=""
      size="small"
      class="ops-stripe-table"
      :max-height="200"
      :data="dataSource"
    >
      <vxe-column type="seq" width="40" />
      <vxe-column
        v-for="item in columns"
        :key="item.field"
        :field="item.field"
        :title="item.title"
        :min-width="100"
      ></vxe-column>
    </vxe-table>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: 'CiUploadTable',
  props: {
    ciTypeAttrs: {
      type: Object,
      required: true,
    },
    uploadData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {}
  },
  computed: {
    columns() {
      if (this.ciTypeAttrs.attributes) {
        return this.ciTypeAttrs.attributes.map((item) => {
          return {
            title: item.alias || item.name,
            field: item.alias || item.name,
          }
        })
      }
      return []
    },
    dataSource() {
      return _.cloneDeep(this.uploadData)
    },
  },
  methods: {},
}
</script>
<style lang="less" scoped>
.cmdb-batch-upload-table {
  overflow: auto;
}
</style>
