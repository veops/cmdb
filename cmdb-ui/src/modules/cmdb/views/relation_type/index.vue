<template>
  <a-card :bordered="false">
    <div class="action-btn">
      <a-button @click="handleCreate" type="primary" style="margin-bottom: 15px;">新增关系类型</a-button>
    </div>
    <vxe-table
      ref="relationTypeTable"
      :data="tableData"
      keep-source
      highlight-hover-row
      :edit-config="{ trigger: 'manual', mode: 'row' }"
      @edit-closed="handleEditClose"
    >
      <vxe-table-column
        field="name"
        title="名称"
        :edit-render="{ name: 'input', attrs: { type: 'text' }, events: { keyup: customCloseEdit } }"
      ></vxe-table-column>
      <vxe-table-column field="updateTime" title="更新时间">
        <template #default="{row}">
          {{ row.updated_at || row.created_at }}
        </template>
      </vxe-table-column>
      <vxe-table-column field="operation" title="操作" align="center">
        <template #default="{row}">
          <template>
            <a><a-icon type="edit" @click="handleEdit(row)"/></a>
            <a-divider type="vertical" />
            <a-popconfirm title="确认删除吗?" @confirm="handleDelete(row)" okText="是" cancelText="否">
              <a :style="{ color: 'red' }"><a-icon type="delete"/></a>
            </a-popconfirm>
          </template>
        </template>
      </vxe-table-column>
    </vxe-table>
  </a-card>
</template>

<script>
import moment from 'moment'
import {
  getRelationTypes,
  deleteRelationType,
  addRelationType,
  updateRelationType,
} from '@/modules/cmdb/api/relationType'

export default {
  name: 'RelationType',
  data() {
    return {
      tableData: [],
    }
  },

  computed: {},
  mounted() {
    this.loadData()
  },

  methods: {
    loadData() {
      getRelationTypes().then((res) => {
        this.tableData = res
      })
    },
    handleEdit(row) {
      const $table = this.$refs.relationTypeTable
      $table.setActiveRow(row)
    },
    handleCreate() {
      const $table = this.$refs.relationTypeTable
      const newRow = {
        name: '',
        created_at: moment().format('YYYY-MM-DD hh:mm:ss'),
      }
      $table.insert(newRow).then(({ row }) => $table.setActiveRow(row))
    },
    handleEditClose({ row, rowIndex, column }) {
      const $table = this.$refs.relationTypeTable
      if (row.id) {
        if (row.name && $table.isUpdateByRow(row, 'name')) {
          this.updateRelationType(row.id, { name: row.name })
        } else {
          $table.revertData(row)
        }
      } else {
        if (row.name) {
          this.createRelationType({ name: row.name })
        } else {
          this.loadData()
        }
      }
    },
    updateRelationType(id, data) {
      updateRelationType(id, data).then((res) => {
        this.$message.success('更新成功!')
        this.loadData()
      })
    },

    createRelationType(data) {
      addRelationType(data).then((res) => {
        this.$message.success('新增成功！')
        this.loadData()
      })
    },
    handleDelete(record) {
      this.deleteRelationType(record.id)
    },
    deleteRelationType(id) {
      deleteRelationType(id).then((res) => {
        this.$message.success('删除成功！')
        this.loadData()
      })
    },
    customCloseEdit(value, $event) {
      // 回车结束编辑
      if ($event.keyCode === 13) {
        const $table = this.$refs.relationTypeTable
        $table.clearActived()
      }
    },
  },
  watch: {},
}
</script>

<style lang="less" scoped></style>
