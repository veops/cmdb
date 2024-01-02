<template>
  <a-modal :visible="visible" @cancel="handleCancel" :footer="null" :width="550" :maskClosable="false">
    <a-button
      @click="handleAddUnique(-1)"
      ghost
      type="primary"
      icon="plus"
      size="small"
      :style="{ marginBottom: '10px' }"
    >{{ $t('new') }}</a-button
    >
    <ops-table
      :loading="loading"
      :data="tableData"
      :edit-config="{ trigger: 'manual', mode: 'row', showIcon: false, autoClear: false, showStatus: true }"
      highlight-hover-row
      show-overflow
      ref="xTable"
      size="mini"
      keep-source
      stripe
      class="ops-stripe-table"
    >
      <vxe-column field="attr_ids" :title="$t('cmdb.ciType.attributes')" :edit-render="{}">
        <template #default="{ row }">
          <template v-for="(attr, index) in row.attr_ids">
            <span :key="attr" :style="{ color: '#2f54eb' }">{{ getDisplayName(attr) }}</span>
            <span :key="`_${attr}`" v-if="index !== row.attr_ids.length - 1"> + </span>
          </template>
        </template>
        <template #edit="{ row }">
          <vxe-select transfer size="small" v-model="row.attr_ids" clearable multiple>
            <vxe-option
              v-for="attr in attributes.filter((attr) => attr.value_type !== '6')"
              :key="attr.id"
              :value="attr.id"
              :label="attr.alias || attr.name"
            ></vxe-option>
          </vxe-select>
        </template>
      </vxe-column>
      <vxe-column filed="opeartion" :title="$t('operation')" width="100">
        <template #default="{ row }">
          <template v-if="$refs.xTable.getVxetableRef().isActiveByRow(row)">
            <a-space>
              <a> <a-icon @click="saveRowEvent(row)" type="save"/></a>
            </a-space>
          </template>
          <template v-else>
            <a-space>
              <a> <a-icon @click="editRowEvent(row)" type="edit"/></a>
              <a-popconfirm :title="$t('cmdb.ciType.confirmDelete2')" @confirm="removeRowEvent(row)">
                <a :style="{ color: 'red' }"> <a-icon type="delete"/></a>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </vxe-column>
    </ops-table>
  </a-modal>
</template>

<script>
import {
  getUniqueConstraintList,
  addUniqueConstraint,
  updateUniqueConstraint,
  deleteUniqueConstraint,
} from '../../api/CIType'
export default {
  name: 'UniqueConstraint',
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      visible: false,
      attributes: [],
      tableData: [],
    }
  },
  methods: {
    open(attributes) {
      this.visible = true
      this.attributes = attributes
      this.getTableList()
    },
    handleCancel() {
      this.visible = false
    },
    getTableList() {
      this.loading = true
      getUniqueConstraintList(this.CITypeId).then((res) => {
        this.tableData = res
        this.loading = false
      })
    },
    async handleAddUnique(row) {
      const $table = this.$refs.xTable.getVxetableRef()
      const record = {
        attr_ids: [],
      }
      const { row: newRow } = await $table.insertAt(record, row)
      await $table.setActiveRow(newRow)
    },
    saveRowEvent(row) {
      const $table = this.$refs.xTable.getVxetableRef()
      $table.clearActived().then(() => {
        if (row.id) {
          updateUniqueConstraint(this.CITypeId, row.id, { attr_ids: row.attr_ids }).then((res) => {
            this.getTableList()
          })
        } else {
          addUniqueConstraint(this.CITypeId, { attr_ids: row.attr_ids }).then((res) => {
            this.getTableList()
          })
        }
      })
    },
    editRowEvent(row) {
      const $table = this.$refs.xTable.getVxetableRef()
      $table.setActiveRow(row)
    },
    removeRowEvent(row) {
      deleteUniqueConstraint(this.CITypeId, row.id).then((res) => {
        this.$message.success(this.$t('deleteSuccess'))
        this.getTableList()
      })
    },
    getDisplayName(attrId) {
      const _find = this.attributes.find((attr) => attr.id === attrId)
      return _find.alias || _find.name
    },
  },
}
</script>

<style></style>
