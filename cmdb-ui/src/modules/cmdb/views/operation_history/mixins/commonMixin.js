import { PAGINATION_CONFIG } from '../constants'

export default {
  data() {
    return {
      DEFAULT_PAGE_SIZE: PAGINATION_CONFIG.DEFAULT_PAGE_SIZE,
      PAGE_SIZE_OPTIONS: PAGINATION_CONFIG.PAGE_SIZE_OPTIONS
    }
  },

  computed: {
    windowHeightOffset() {
      return this.isExpand ? 396 : 331
    }
  },

  methods: {
    applyFilter(updates = {}) {
      Object.assign(this.queryParams, {
        page: 1,
        page_size: this.DEFAULT_PAGE_SIZE,
        ...updates
      })
      this.getTable(this.queryParams)
    },

    handleError(error, action = 'operation') {
      if (process.env.NODE_ENV === 'development') {
        console.error(`[OperationHistory] ${action} failed:`, error)
      }
      this.$message.error(
        this.$t('cmdb.history.operationFailed', {
          action,
          error: error.message
        })
      )
    },

    createMergeRowMethod(fields, groupFields = ['created_at']) {
      return ({ row, _rowIndex, column, visibleData }) => {
        const cellValue = row[column.property]

        if (!cellValue || !fields.includes(column.property)) {
          return
        }

        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]

        const checkGroupMatch = (compareRow) => {
          return groupFields.every(field => compareRow[field] === row[field])
        }

        if (prevRow && prevRow[column.property] === cellValue && checkGroupMatch(prevRow)) {
          return { rowspan: 0, colspan: 0 }
        }

        let countRowspan = 1
        while (nextRow && nextRow[column.property] === cellValue && checkGroupMatch(nextRow)) {
          nextRow = visibleData[++countRowspan + _rowIndex]
        }

        if (countRowspan > 1) {
          return { rowspan: countRowspan, colspan: 1 }
        }
      }
    }
  }
}
