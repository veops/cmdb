<template>
  <div class="ci-types-triggers">
    <div style="margin-bottom: 10px">
      <a-button
        type="primary"
        @click="handleAddTrigger"
        size="small"
        class="ops-button-primary"
        icon="plus"
      >新增触发器</a-button
      >
    </div>
    <vxe-table
      stripe
      :data="tableData"
      size="small"
      show-overflow
      highlight-hover-row
      keep-source
      :max-height="windowHeight - 180"
      class="ops-stripe-table"
    >
      <vxe-column field="option.name" title="名称"></vxe-column>
      <vxe-column field="option.description" title="备注"></vxe-column>
      <vxe-column field="type" title="类型">
        <template #default="{ row }">
          <span v-if="row.attr_id">日期属性</span>
          <span v-else>数据变更</span>
        </template>
      </vxe-column>
      <vxe-column field="option.enable" title="开启">
        <template #default="{ row }">
          <a-switch :checked="row.option.enable" @click="changeEnable(row)"></a-switch>
        </template>
      </vxe-column>

      <!-- <vxe-column field="attr_name" title="属性名"></vxe-column>
      <vxe-column field="option.subject" title="主题"></vxe-column>
      <vxe-column field="option.body" title="内容"></vxe-column>
      <vxe-column field="option.wx_to" title="微信通知">
        <template #default="{ row }">
          <span v-for="(person, index) in row.option.wx_to" :key="person + index">[{{ person }}]</span>
        </template>
      </vxe-column>
      <vxe-column field="option.mail_to" title="邮件通知">
        <template #default="{ row }">
          <span v-for="(email, index) in row.option.mail_to" :key="email + index">[{{ email }}]</span>
        </template>
      </vxe-column>
      <vxe-column field="option.before_days" title="提前">
        <template #default="{ row }">
          <span v-if="row.option.before_days">{{ row.option.before_days }}天</span>
        </template>
      </vxe-column>
      <vxe-column field="option.notify_at" title="发送时间"></vxe-column> -->
      <vxe-column field="operation" title="操作" width="80px" align="center">
        <template #default="{ row }">
          <a-space>
            <a @click="handleEdit(row)"><a-icon type="edit"/></a>
            <a style="color:red;" @click="handleDetele(row.id)"><a-icon type="delete"/></a>
          </a-space>
        </template>
      </vxe-column>
    </vxe-table>
    <TriggerForm ref="triggerForm" :CITypeId="CITypeId" />
  </div>
</template>

<script>
import _ from 'lodash'
import { getTriggerList, deleteTrigger, updateTrigger } from '../../api/CIType'
import { getCITypeAttributesById } from '../../api/CITypeAttr'
import TriggerForm from './triggerForm.vue'
import { getAllDepAndEmployee } from '@/api/company'

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
      allTreeDepAndEmp: [],
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
      provide_allTreeDepAndEmp: () => {
        return this.allTreeDepAndEmp
      },
    }
  },
  mounted() {
    this.getAllDepAndEmployee()
  },
  methods: {
    getAllDepAndEmployee() {
      getAllDepAndEmployee({ block: 0 }).then((res) => {
        this.allTreeDepAndEmp = res
      })
    },
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
        title: '警告',
        content: '确认删除该触发器吗?',
        onOk() {
          deleteTrigger(that.CITypeId, id).then(() => {
            that.$message.success('删除成功！')
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
