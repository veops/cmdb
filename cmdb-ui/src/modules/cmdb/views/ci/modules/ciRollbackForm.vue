<template>
  <CustomDrawer
    :closable="true"
    :title="drawerTitle"
    :visible="drawerVisible"
    @close="onClose"
    placement="right"
    width="800"
    :bodyStyle="{ paddingTop: 0 }"
  >
    <div class="custom-drawer-bottom-action">
      <a-button @click="onClose">{{ $t('cancel') }}</a-button>
      <a-button type="primary" @click="handleSubmit" :loading="loading" :disabled="!hasDiff">{{
        $t('submit')
      }}</a-button>
    </div>
    <a-form :form="form" :style="{ paddingTop: '20px' }">
      <a-form-item :label="$t('cmdb.ci.rollbackTo')" required :help="$t('cmdb.ci.baselineTips')">
        <a-date-picker
          :style="{ width: '278px' }"
          format="YYYY-MM-DD HH:mm:ss"
          valueFormat="YYYY-MM-DD HH:mm:ss"
          @ok="getBaselineDiff"
          :show-time="{ format: 'HH:mm:ss' }"
          :placeholder="$t('cmdb.ci.rollbackToTips')"
          v-decorator="['before_date', { rules: [{ required: true, message: $t('cmdb.ci.rollbackToTips') }] }]"
        />
      </a-form-item>
      <span :style="{ fontWeight: 'bold' }">{{ $t('cmdb.ci.baselineDiff') }}</span>
      <vxe-table
        ref="xTable"
        show-overflow
        show-header-overflow
        resizable
        border
        size="small"
        :span-method="mergeRowMethod"
        :data="tableData"
        :scroll-y="{ enabled: false, gt: 20 }"
        :scroll-x="{ enabled: false, gt: 0 }"
        class="ops-unstripe-table"
      >
        <template #empty>
          <a-empty :image-style="{ height: '100px' }" :style="{ paddingTop: '10%' }">
            <img slot="image" :src="require('@/assets/data_empty.png')" />
            <span slot="description"> {{ dataLoad }} </span>
          </a-empty>
        </template>
        <vxe-column field="instance" min-width="80" :title="$t('cmdb.ci.instance')"> </vxe-column>
        <vxe-column field="attr_name" min-width="80" :title="$t('cmdb.attribute')"> </vxe-column>
        <vxe-column field="cur" min-width="80" :title="$t('cmdb.ci.rollbackBefore')">
          <template #default="{ row }">
            <span v-if="row.value_type === '6'">{{ JSON.stringify(row.cur) }}</span>
            <span v-else>{{ row.cur }}</span>
          </template>
        </vxe-column>
        <vxe-column field="to" min-width="80" :title="$t('cmdb.ci.rollbackAfter')">
          <template #default="{ row }">
            <span v-if="row.value_type === '6'">{{ JSON.stringify(row.to) }}</span>
            <span v-else>{{ row.to }}</span>
          </template>
        </vxe-column>
      </vxe-table>
    </a-form>
  </CustomDrawer>
</template>

<script>
import { getCIsBaseline, CIBaselineRollback } from '../../../api/history'
export default {
  name: 'CiRollbackForm',
  props: {
    ciIds: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      form: this.$form.createForm(this),
      drawerTitle: this.$t('cmdb.ci.rollbackHeader'),
      drawerVisible: false,

      formLayout: 'horizontal',

      tableData: [],
      dataLoad: this.$t('noData'),
      loading: false,
      hasDiff: false,
      batched: false,
    }
  },
  methods: {
    onClose() {
      this.drawerVisible = false
      this.form.resetFields()
      this.tableData = []
      this.dataLoad = this.$t('noData')
    },
    onOpen(batched = false) {
      this.drawerTitle = this.$t('cmdb.ci.rollbackHeader')
      this.drawerVisible = true
      this.batched = batched
    },
    handleSubmit() {
      this.form.validateFields((err, values) => {
        if (!err) {
          const that = this
          this.$confirm({
            title: that.$t('warning'),
            content: that.$t('cmdb.ci.rollbackConfirm'),
            onOk() {
              if (that.batched) {
                that.$emit('batchRollbackAsync', values)
              } else {
                that.rollbackCI(values)
              }
            },
          })
        }
      })
    },
    rollbackCI(params) {
      CIBaselineRollback(this.ciIds[0], params).then((res) => {
        this.$message.success(this.$t('cmdb.ci.rollbackSuccess'))
        this.form.resetFields()
        this.$emit('getCIHistory')
      })
    },
    getBaselineDiff(value) {
      this.dataLoad = 'loading...'
      this.loading = true
      this.hasDiff = false
      getCIsBaseline({ ci_ids: this.ciIds.join(','), before_date: value }).then((res) => {
        this.tableData = res
        this.loading = false
        if (!res.length) {
          this.dataLoad = this.$t('cmdb.ci.noDiff', { baseline: value })
        } else {
          this.hasDiff = true
        }
      })
    },
    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['instance']
      const cellValue1 = row.instance
      if (cellValue1 && fields.includes(column.property)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow.instance === cellValue1) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow.instance === cellValue1) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },
  },
}
</script>
