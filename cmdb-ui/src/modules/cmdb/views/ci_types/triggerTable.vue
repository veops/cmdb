<template>
  <div class="ci-types-triggers">
    <div style="margin-bottom: 10px">
      <a-button
        type="primary"
        @click="handleAddTrigger"
        size="small"
        class="ops-button-primary"
        icon="plus"
      >{{ $t('cmdb.ciType.newTrigger') }}</a-button
      >
    </div>
    <ops-table
      stripe
      :data="tableData"
      size="small"
      show-overflow
      highlight-hover-row
      keep-source
      :max-height="windowHeight - 180"
      class="ops-stripe-table"
    >
      <vxe-column field="option.name" :title="$t('name')"></vxe-column>
      <vxe-column field="option.description" :title="$t('desc')"></vxe-column>
      <vxe-column field="type" :title="$t('type')">
        <template #default="{ row }">
          <span v-if="row.attr_id">{{ $t('cmdb.ciType.triggerDate') }}</span>
          <span v-else>{{ $t('cmdb.ciType.triggerDataChange') }}</span>
        </template>
      </vxe-column>
      <vxe-column field="option.enable" :title="$t('cmdb.ciType.triggerEnable')">
        <template #default="{ row }">
          <a-switch :checked="row.option.enable" @click="changeEnable(row)"></a-switch>
        </template>
      </vxe-column>
      <vxe-column field="operation" :title="$t('operation')" width="100px" align="center">
        <template #default="{ row }">
          <a-space>
            <a @click="handleEdit(row)"><a-icon type="edit"/></a>
            <a style="color:red;" @click="handleDetele(row.id)"><a-icon type="delete"/></a>
          </a-space>
        </template>
      </vxe-column>
    </ops-table>
    <TriggerForm ref="triggerForm" :CITypeId="CITypeId" />
  </div>
</template>

<script>
import _ from 'lodash'
import { getTriggerList, deleteTrigger, updateTrigger } from '../../api/CIType'
import { getCITypeAttributesById } from '../../api/CITypeAttr'
import TriggerForm from './triggerForm.vue'

export default {
  name: 'TriggerTable',
  components: { TriggerForm },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      tableData: [],
      attrList: [],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  provide() {
    return {
      refresh: this.getTableData,
    }
  },
  methods: {
    async getTableData() {
      const [triggerList, attrList] = await Promise.all([
        getTriggerList(this.CITypeId),
        getCITypeAttributesById(this.CITypeId),
      ])
      triggerList.forEach((trigger) => {
        const _find = attrList.attributes.find((attr) => attr.id === trigger.attr_id)
        if (_find) {
          trigger.attr_name = _find.alias || _find.name
        }
      })
      this.tableData = triggerList
      this.attrList = attrList.attributes
    },
    handleAddTrigger() {
      this.$refs.triggerForm.createFromTriggerTable(this.attrList)
    },
    handleDetele(id) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteTrigger'),
        onOk() {
          deleteTrigger(that.CITypeId, id).then(() => {
            that.$message.success(that.$t('deleteSuccess'))
            that.getTableData()
          })
        },
      })
    },
    handleEdit(row) {
      this.$refs.triggerForm.open(
        {
          id: row.attr_id,
          alias: row?.option?.name ?? '',
          trigger: { id: row.id, attr_id: row.attr_id, option: row.option },
          has_trigger: true,
        },
        this.attrList
      )
    },
    changeEnable(row) {
      const _row = _.cloneDeep(row)
      delete _row.id
      const enable = row?.option?.enable ?? true
      _row.option.enable = !enable
      updateTrigger(this.CITypeId, row.id, _row).then(() => {
        this.getTableData()
      })
    },
  },
}
</script>

<style lang="less" scoped>
.ci-types-triggers {
  padding: 16px 24px 24px;
}
</style>
