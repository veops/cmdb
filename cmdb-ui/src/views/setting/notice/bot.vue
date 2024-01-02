<template>
  <div>
    <vxe-table
      ref="xTable"
      :data="tableData"
      size="mini"
      stripe
      class="ops-stripe-table"
      show-overflow
      :edit-config="{ showIcon: false, trigger: 'manual', mode: 'row' }"
    >
      <vxe-column v-for="col in columns" :key="col.field" :field="col.field" :title="col.title" :edit-render="{}">
        <template #header> <span v-if="col.required" :style="{ color: 'red' }">* </span>{{ col.title }} </template>
        <template #edit="{ row }">
          <vxe-input v-model="row[col.field]" type="text"></vxe-input>
        </template>
      </vxe-column>
      <vxe-column :title="$t('operation')" width="80" v-if="!disabled">
        <template #default="{ row }">
          <template v-if="$refs.xTable.isActiveByRow(row)">
            <a @click="saveRowEvent(row)"><a-icon type="save"/></a>
          </template>
          <a-space v-else>
            <a @click="editRowEvent(row)"><ops-icon type="icon-xianxing-edit"/></a>
            <a style="color:red" @click="deleteRowEvent(row)"><ops-icon type="icon-xianxing-delete"/></a>
          </a-space>
        </template>
      </vxe-column>
    </vxe-table>
    <div :style="{ color: '#f5222d' }" v-if="errorFlag">{{ $t('cs.notice.robotConfigErrorTips') }}</div>
    <a-button v-if="!disabled" icon="plus-circle" class="ops-button-primary" type="primary" @click="insertEvent">{{
      $t('add')
    }}</a-button>
  </div>
</template>

<script>
export default {
  name: 'Bot',
  props: {
    columns: {
      type: Array,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      tableData: [],
      errorFlag: false,
    }
  },
  methods: {
    async insertEvent() {
      const $table = this.$refs.xTable
      const record = {
        name: '',
        url: '',
      }
      const { row: newRow } = await $table.insertAt(record, -1)
      await $table.setActiveRow(newRow)
    },
    saveRowEvent(row) {
      const $table = this.$refs.xTable
      $table.clearActived()
    },
    editRowEvent(row) {
      const $table = this.$refs.xTable
      $table.setActiveRow(row)
    },
    deleteRowEvent(row) {
      const $table = this.$refs.xTable
      $table.remove(row)
    },
    getData(callback) {
      const $table = this.$refs.xTable
      const { fullData: _tableData } = $table.getTableData()
      const requiredObj = {}
      this.columns.forEach((col) => {
        if (col.required) {
          requiredObj[col.field] = true
        }
      })
      let flag = true
      _tableData.forEach((td) => {
        Object.keys(requiredObj).forEach((key) => {
          if (requiredObj[key]) {
            flag = !!(flag && td[`${key}`])
          }
        })
      })
      this.errorFlag = !flag
      callback(flag, _tableData)
    },
    setData(value) {
      this.tableData = value
      this.errorFlag = false
    },
  },
}
</script>

<style></style>
