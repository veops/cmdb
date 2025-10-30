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
    <div v-else class="upload-placeholder">
      <div class="upload-placeholder-content">
        <a-icon type="file-excel" class="upload-placeholder-icon" />
        <div class="upload-placeholder-text">
          <p class="upload-placeholder-title">{{ $t('cmdb.batch.pleaseUploadFile') }}</p>
          <p class="upload-placeholder-hint">{{ $t('cmdb.batch.uploadFileHint') }}</p>
        </div>
      </div>
    </div>
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
.cmdb-batch-upload-table {
  min-height: 200px;

  .upload-placeholder {
    height: 240px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed #d9d9d9;
    background: #fafafa;
    transition: all 0.3s ease;

    &:hover {
      border-color: @primary-color;
      background: fade(@primary-color, 5%);

      .upload-placeholder-icon {
        color: @primary-color;
        transform: translateY(-4px);
      }
    }

    &-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
    }

    &-icon {
      font-size: 72px;
      color: #bfbfbf;
      transition: all 0.3s ease;
    }

    &-text {
      text-align: center;
    }

    &-title {
      margin: 0 0 8px 0;
      font-size: 16px;
      font-weight: 500;
      color: @text-color_1;
    }

    &-hint {
      margin: 0;
      font-size: 14px;
      color: @text-color_3;
    }
  }
}
</style>
