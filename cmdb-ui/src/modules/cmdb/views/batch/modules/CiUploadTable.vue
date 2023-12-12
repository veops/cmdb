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
      resizable
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
      const _columns = []
      if (this.ciTypeAttrs.attributes) {
        _columns.push(
          ...this.ciTypeAttrs.attributes.map((item) => {
            return {
              title: item.alias || item.name,
              field: item.alias || item.name,
            }
          })
        )
      }
      if (this.uploadData && this.uploadData.length) {
        Object.keys(this.uploadData[0]).forEach((key) => {
          if (key.startsWith('$')) {
            _columns.push({ title: key, field: key })
          }
        })
      }
      return _columns
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
