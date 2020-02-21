<template>
  <div>
    <div id="hotTable" class="hotTable" style="overflow: hidden; height:275px">
      <HotTable :root="root" ref="HTable" :settings="hotSettings"></HotTable>
    </div>
  </div>
</template>

<script>
import { HotTable } from '@handsontable-pro/vue'
export default {
  name: 'Editor',
  components: {
    HotTable
  },
  props: { ciTypeAttrs: { type: Object, required: true } },
  data: function () {
    return {
      root: 'test-hot'
    }
  },
  computed: {
    hotSettings () {
      const whiteColumn = []
      const aliasList = []
      this.$props.ciTypeAttrs.attributes.forEach(item => {
        aliasList.push(item.alias)
        whiteColumn.push('')
      })
      const dt = {
        data: [whiteColumn],
        startRows: 11,
        startCols: 6,
        minRows: 5,
        minCols: 1,
        maxRows: 90,
        maxCols: 90,
        rowHeaders: true,
        // minSpareCols: 2,
        colHeaders: aliasList,
        minSpareRows: 2,
        // autoWrapRow: true,
        contextMenu: {
          items: {
            row_above: {
              name: 'insert a line at the top'
            },
            row_below: {
              name: 'insert a line at the bottom'
            },
            moverow: {
              name: 'Delete rows'
            },
            unfreeze_column: {
              name: 'Uncolumn fixation'
            },
            hsep1: '---------',
            hsep2: '---------'
          }
        },
        fixedColumnsLeft: 0,
        fixedRowsTop: 0,
        manualColumnFreeze: true,
        comments: true,
        customBorders: [],
        columnSorting: true,
        stretchH: 'all',
        afterChange: function (changes, source) {
          if (changes !== null) {
            document.getElementById('upload-button').disabled = false
          }
        }
      }
      return dt
    }
  },
  methods: {
    getDataList () {
      const data = this.$refs.HTable.$data.hotInstance.getData()
      data.unshift(this.$refs.HTable.$data.hotInstance.getColHeader())
      return data
    }
  }
}
</script>
<style>
@import '~handsontable/dist/handsontable.full.css';
</style>
