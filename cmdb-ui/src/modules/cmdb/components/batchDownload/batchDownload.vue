<template>
  <a-modal
    :visible="visible"
    :title="$t('cmdb.components.downloadCI')"
    @cancel="handleCancel"
    @ok="handleOk"
    width="700px"
  >
    <a-form :form="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 15 }">
      <a-form-item :label="$t('cmdb.components.filename')">
        <a-input
          :placeholder="$t('cmdb.components.filenameInputTips')"
          v-decorator="['filename', { rules: [{ required: true, message: $t('cmdb.components.filenameInputTips') }] }]"
        />
      </a-form-item>
      <a-form-item :label="$t('cmdb.components.saveType')">
        <a-select
          :placeholder="$t('cmdb.components.saveTypeTips')"
          v-decorator="[
            'type',
            { rules: [{ required: true, message: $t('cmdb.components.saveTypeTips') }], initialValue: 'xlsx' },
          ]"
        >
          <a-select-option v-for="item in typeList" :key="item.id" :values="item.id">{{ item.label }}</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item :label="$t('cmdb.ciType.selectAttributes')">
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
          />{{ $t('checkAll') }}
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
    return {
      visible: false,
      form: this.$form.createForm(this),
      preferenceAttrList: [],
      checkedKeys: [],
      checkAll: false,
      indeterminate: false,
      defaultChecked: [],
    }
  },
  computed: {
    typeList() {
      return [
        {
          id: 'xlsx',
          label: this.$t('cmdb.components.xlsx'),
        },
        {
          id: 'csv',
          label: this.$t('cmdb.components.csv'),
        },
        {
          id: 'html',
          label: this.$t('cmdb.components.html'),
        },
        {
          id: 'xml',
          label: this.$t('cmdb.components.xml'),
        },
        {
          id: 'txt',
          label: this.$t('cmdb.components.txt'),
        },
      ]
    },
  },
  methods: {
    ...mapMutations('cmdbStore', ['SET_IS_TABLE_LOADING']),
    open({ preferenceAttrList, ciTypeName = undefined }) {
      this.preferenceAttrList = preferenceAttrList
      this.visible = true
      this.$nextTick((res) => {
        this.form.setFieldsValue({
          filename: ciTypeName
            ? `cmdb-${ciTypeName}-${moment().format('YYYYMMDDHHmmss')}`
            : `cmdb-${moment().format('YYYYMMDDHHmmss')}`,
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
