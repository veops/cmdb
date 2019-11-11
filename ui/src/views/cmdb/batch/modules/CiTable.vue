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
        // minSpareCols: 2, //列留白
        colHeaders: aliasList,
        minSpareRows: 2, // 行留白
        // autoWrapRow: true, // 自动换行
        // 自定义右键菜单，可汉化，默认布尔值
        contextMenu: {
          items: {
            row_above: {
              name: '上方插入一行'
            },
            row_below: {
              name: '下方插入一行'
            },
            moverow: {
              name: '删除行'
            },
            unfreeze_column: {
              name: '取消列固定'
            },
            hsep1: '---------', // 提供分隔线
            hsep2: '---------'
          }
        },
        // width: '100%',
        // fillHandle: true, // 选中拖拽复制 possible values: true, false, "horizontal", "vertical"
        fixedColumnsLeft: 0, // 固定左边列数
        fixedRowsTop: 0, // 固定上边列数
        manualColumnFreeze: true, // 手动固定列
        // manualColumnMove: true, // 手动移动列
        // manualRowMove: true, // 手动移动行
        // manualColumnResize: true, // 手工更改列距
        // manualRowResize: true, // 手动更改行距
        comments: true, // 添加注释
        customBorders: [], // 添加边框
        columnSorting: true, // 排序
        stretchH: 'all', // 根据宽度横向扩展，last:只扩展最后一列，none：默认不扩展
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
