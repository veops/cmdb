<template>
  <div class="cmdb-batch-upload-table">
    <vxe-table
      v-if="uploadData && uploadData.length"
      ref="xTable"
      stripe
      show-header-overflow
      show-overflow=""
      size="small"
      class="ops-stripe-table"
      height="auto"
      :data="dataSource"
      resizable
      :row-style="rowStyle"
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
    <a-empty
      v-else
      :image-style="{
        height: '80px',
        marginTop: '10px',
      }"
    >
      <img slot="image" :src="require('@/assets/data_empty.png')" />
      <template slot="description">
        <p>{{ $t('noData') }}</p>
        <p>{{ $t('cmdb.batch.pleaseUploadFile') }}</p>
      </template>
    </a-empty>
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
    return {
      errorIndexList: [],
    }
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
  watch: {
    uploadData() {
      this.errorIndexList = []
    },
  },
  methods: {
    uploadResultError(index) {
      const _errorIndexList = _.cloneDeep(this.errorIndexList)
      _errorIndexList.push(index)
      this.errorIndexList = _errorIndexList
    },
    rowStyle({ rowIndex }) {
      if (this.errorIndexList.includes(rowIndex)) {
        return 'color:red;'
      }
    },
    downloadError() {
      const data = this.uploadData.filter((item, index) => this.errorIndexList.includes(index))
      this.$refs.xTable.exportData({
        data,
        type: 'xlsx',
        columnFilterMethod({ column }) {
          return column.property
        },
      })
    },
  },
}
</script>
<style lang="less" scoped>
@import '~@/style/static.less';

.cmdb-batch-upload-table {
  height: 200px;
  padding: 20px;
  background: linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
    linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
    linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y,
    linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y;
  background-size: 15px 1px, 15px 1px, 1px 15px, 1px 15px;
  background-position: 0 0, 0 100%, 0 0, 100% 0;
  .ant-empty-description {
    p:last-child {
      color: @primary-color;
    }
  }
}
</style>
