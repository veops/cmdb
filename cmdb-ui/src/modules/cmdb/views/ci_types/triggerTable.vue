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
      <span class="trigger-tips">{{ tips }}</span>
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
      <vxe-column field="attr_name" title="属性名"></vxe-column>
      <vxe-column field="notify.subject" title="主题"></vxe-column>
      <vxe-column field="notify.body" title="内容"></vxe-column>
      <vxe-column field="notify.wx_to" title="微信通知">
        <template #default="{ row }">
          <span v-for="(person, index) in row.notify.wx_to" :key="person + index">[{{ person }}]</span>
        </template>
      </vxe-column>
      <vxe-column field="notify.mail_to" title="邮件通知">
        <template #default="{ row }">
          <span v-for="(email, index) in row.notify.mail_to" :key="email + index">[{{ email }}]</span>
        </template>
      </vxe-column>
      <vxe-column field="notify.before_days" title="提前">
        <template #default="{ row }">
          <span v-if="row.notify.before_days">{{ row.notify.before_days }}天</span>
        </template>
      </vxe-column>
      <vxe-column field="notify.notify_at" title="发送时间"></vxe-column>
      <vxe-column field="operation" title="操作" width="200px" align="center">
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
import { getTriggerList, deleteTrigger } from '../../api/CIType'
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
      tips: '主题、内容、微信通知和邮件通知都可以引用该模型的属性值，引用方法为: {{ attr_name }}',
      tableData: [],
      attrList: [],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    canAddTriggerAttr() {
      return this.attrList.filter((attr) => attr.value_type === '3' || attr.value_type === '4')
    },
  },
  provide() {
    return { refresh: this.getTableData }
  },
  mounted() {},
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
      this.$refs.triggerForm.createFromTriggerTable(this.canAddTriggerAttr)
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
      const _find = this.attrList.find((attr) => attr.id === row.attr_id)
      this.$refs.triggerForm.open({
        id: row.attr_id,
        alias: _find ? _find.alias || _find.name : '',
        trigger: { id: row.id, notify: row.notify },
        has_trigger: true,
      })
    },
  },
}
</script>

<style lang="less" scoped>
.ci-types-triggers {
  padding: 16px 24px 24px;
  .trigger-tips {
    border: 1px solid #d4380d;
    background-color: #fff2e8;
    padding: 2px 10px;
    border-radius: 4px;
    color: #d4380d;
    float: right;
  }
}
</style>
