<template>
  <a-modal :visible="visible" title="导出数据" @cancel="handleCancel" okText="导出" @ok="handleOk">
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 15 }">
      <a-form-item label="文件名">
        <a-input
          placeholder="请输入文件名"
          v-decorator="['filename', { rules: [{ required: true, message: '请输入文件名' }] }]"
        />
      </a-form-item>
      <a-form-item label="保存类型">
        <a-select
          placeholder="请选择保存类型"
          v-decorator="['type', { rules: [{ required: true, message: '请选择保存类型' }], initialValue: 'xlsx' }]"
        >
          <a-select-option v-for="item in typeList" :key="item.id" :values="item.id">{{ item.label }}</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="选择字段">
        <div
          :style="{
            paddingLeft: '26px',
            backgroundColor: '#e9e9e9',
            borderTopLeftRadius: '5px',
            borderTopRightRadius: '5px',
          }"
        >
          <a-checkbox
            :indeterminate="indeterminate"
            :checked="checkAll"
            @change="onCheckAllChange"
            :style="{ marginRight: '10px' }"
          />全选
        </div>
        <div
          :style="{
            height: '200px',
            overflow: 'auto',
            borderLeft: '1px solid #e9e9e9',
            borderBottom: '1px solid #e9e9e9',
          }"
        >
          <a-tree
            checkable
            defaultExpandAll
            :selectable="false"
            :auto-expand-parent="true"
            :tree-data="preferenceAttrList"
            :replaceFields="replaceFields"
            :checkedKeys="checkedKeys"
            @check="check"
          />
        </div>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { mapMutations } from 'vuex'
import _ from 'lodash'
import moment from 'moment'
import Treeselect from '@riophae/vue-treeselect'
export default {
  name: 'BatchDownload',
  components: { Treeselect },
  props: {
    replaceFields: {
      type: Object,
      default: () => {
        return { children: 'children', title: 'alias', key: 'name' }
      },
    },
    treeType: {
      type: String,
      default: 'default',
    },
  },
  data() {
    const typeList = [
      {
        id: 'xlsx',
        label: 'Excel工作簿(*.xlsx)',
      },
      {
        id: 'csv',
        label: 'CSV(逗号分隔)(*.csv)',
      },
      {
        id: 'html',
        label: '网页(*.html)',
      },
      {
        id: 'xml',
        label: 'XML数据(*.xml)',
      },
      {
        id: 'txt',
        label: '文本文件(制表符分隔)(*.txt)',
      },
    ]
    return {
      typeList,
      visible: false,
      form: this.$form.createForm(this),
      preferenceAttrList: [],
      checkedKeys: [],
      checkAll: false,
      indeterminate: false,
      defaultChecked: [],
    }
  },
  methods: {
    ...mapMutations('cmdbStore', ['SET_IS_TABLE_LOADING']),
    open({ preferenceAttrList }) {
      this.preferenceAttrList = preferenceAttrList
      this.visible = true
      this.$nextTick((res) => {
        this.form.setFieldsValue({
          filename: `cmdb-${moment().format('YYYYMMDDHHmmss')}`,
        })
        if (this.treeType === 'tree') {
          const _check = ['ci_type_alias']
          preferenceAttrList.forEach((colGroup) => {
            if (colGroup.children && colGroup.children.length) {
              _check.push(...colGroup.children.map((attr) => attr[`${this.replaceFields.key}`]))
            }
          })
          this.defaultChecked = _check
          this.checkedKeys = _check
        } else {
          this.checkedKeys = preferenceAttrList.map((attr) => attr[`${this.replaceFields.key}`])
        }
        this.checkAll = true
        this.indeterminate = false
      })
    },
    check(checkedKeys) {
      if (this.treeType === 'tree') {
        this.checkedKeys = checkedKeys.filter((item) => !item.startsWith('parent-'))
      } else {
        this.checkedKeys = checkedKeys
      }
      if (this.treeType === 'tree') {
        const isEqual = _.isEqual(this.checkedKeys.length, this.defaultChecked.length)
        this.checkAll = isEqual
        this.indeterminate = !!checkedKeys.length && !isEqual
        return
      }
      this.checkAll = this.checkedKeys.length === this.preferenceAttrList.length
      this.indeterminate = !!checkedKeys.length && checkedKeys.length < this.preferenceAttrList.length
    },
    handleCancel() {
      this.visible = false
    },
    handleOk() {
      this.form.validateFields((err, values) => {
        if (!err) {
          this.SET_IS_TABLE_LOADING(true)
          this.$nextTick(() => {
            this.$emit('batchDownload', { ...values, checkedKeys: this.checkedKeys })
            setTimeout(() => {
              this.SET_IS_TABLE_LOADING(false)
              this.handleCancel()
            }, 2000)
          })
        }
      })
    },
    onCheckAllChange(e) {
      Object.assign(this, {
        checkedKeys: e.target.checked ? this.preferenceAttrList.map((attr) => attr[`${this.replaceFields.key}`]) : [],
        indeterminate: false,
        checkAll: e.target.checked,
      })
    },
  },
}
</script>

<style></style>
