<template>
  <a-modal :width="680" :title="title" :visible="visible" @ok="handleOk" @cancel="handleCancel">
    <CustomRadio
      :radioList="[
        { value: 1, label: $t('cmdb.components.all') },
        { value: 2, label: $t('cmdb.components.customize'), layout: 'vertical' },
        { value: 3, label: $t('cmdb.components.none') },
      ]"
      :value="radioValue"
      @change="changeRadioValue"
    >
      <template slot="extra_2" v-if="radioValue === 2">
        <treeselect
          v-if="colType === 'read_attr'"
          v-model="selectedAttr"
          :multiple="true"
          :clearable="true"
          searchable
          :options="attrGroup"
          :placeholder="$t('cmdb.ciType.selectAttributes')"
          value-consists-of="LEAF_PRIORITY"
          :limit="10"
          :limitText="(count) => `+ ${count}`"
          :normalizer="
            (node) => {
              return {
                id: node.name || -1,
                label: node.alias || node.name || $t('other'),
                title: node.alias || node.name || $t('other'),
                children: node.attributes,
              }
            }
          "
          appendToBody
          zIndex="1050"
        >
        </treeselect>
        <a-form-model
          :model="form"
          :rules="rules"
          v-if="colType === 'read_ci'"
          :labelCol="{ span: 2 }"
          :wrapperCol="{ span: 10 }"
          ref="form"
        >
          <a-form-model-item :label="$t('name')" prop="name">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <FilterComp
            ref="filterComp"
            :isDropdown="false"
            :canSearchPreferenceAttrList="canSearchPreferenceAttrList"
            @setExpFromFilter="setExpFromFilter"
            :expression="expression"
          />
        </a-form-model>
      </template>
    </CustomRadio>
  </a-modal>
</template>

<script>
import { grantCiType, revokeCiType } from '../../api/CIType'
import { getCITypeAttributesByTypeIds } from '../../api/CITypeAttr'
import FilterComp from '@/components/CMDBFilterComp'

export default {
  name: 'ReadGrantModal',
  components: { FilterComp },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  inject: {
    provide_attrGroup: {
      from: 'attrGroup',
    },
    provide_filerPerimissions: {
      from: 'filerPerimissions',
    },
  },
  data() {
    return {
      visible: false,
      colType: '',
      row: {},
      radioValue: 1,
      radioStyle: {
        display: 'block',
        height: '30px',
        lineHeight: '30px',
      },
      selectedAttr: [],
      ruleList: [],
      canSearchPreferenceAttrList: [],
      expression: '',
      form: {
        name: '',
      },
      rules: {
        name: [{ required: true, message: this.$t('cmdb.components.customizeFilterName') }],
      },
    }
  },
  computed: {
    title() {
      if (this.colType === 'read_attr') {
        return this.$t('cmdb.components.attributeGrant')
      }
      return this.$t('cmdb.components.ciGrant')
    },
    attrGroup() {
      return this.provide_attrGroup()
    },
    filerPerimissions() {
      return this.provide_filerPerimissions()
    },
    filterKey() {
      if (this.colType === 'read_attr') {
        return 'attr_filter'
      }
      return 'ci_filter'
    },
  },
  methods: {
    async open(colType, row) {
      this.visible = true
      this.colType = colType
      this.row = row
      this.form = {
        name: '',
      }
      if (this.colType === 'read_ci') {
        await getCITypeAttributesByTypeIds({ type_ids: this.CITypeId }).then((res) => {
          this.canSearchPreferenceAttrList = res.attributes.filter((item) => item.value_type !== '6')
        })
      }
      if (this.filerPerimissions[row.rid]) {
        const _tempValue = this.filerPerimissions[row.rid][this.filterKey]
        if (_tempValue && _tempValue.length) {
          this.radioValue = 2
          if (this.colType === 'read_attr') {
            this.selectedAttr = _tempValue
          } else {
            this.expression = `q=${_tempValue}`
            this.form = {
              name: this.filerPerimissions[row.rid].name || '',
            }
            this.$nextTick(() => {
              this.$refs.filterComp.visibleChange(true)
            })
          }
        }
      }
    },
    async handleOk() {
      if (this.radioValue === 1) {
        await grantCiType(this.CITypeId, this.row.rid, {
          perms: ['read'],
          attr_filter: this.colType === 'read_attr' ? [] : undefined,
          ci_filter: this.colType === 'read_ci' ? '' : undefined,
        })
      } else if (this.radioValue === 2) {
        if (this.colType === 'read_ci') {
          this.$refs.filterComp.handleSubmit()
        }
        await grantCiType(this.CITypeId, this.row.rid, {
          perms: ['read'],
          attr_filter: this.colType === 'read_attr' ? this.selectedAttr : undefined,
          ci_filter: this.colType === 'read_ci' ? this.expression.slice(2) : undefined,
          name: this.colType === 'read_ci' ? this.form.name : undefined,
        })
      } else {
        const _tempValue = this.filerPerimissions?.[this.row.rid]?.[this.filterKey]
        await revokeCiType(this.CITypeId, this.row.rid, {
          perms: ['read'],
          attr_filter: this.colType === 'read_attr' ? _tempValue : undefined,
          ci_filter: this.colType === 'read_ci' ? _tempValue : undefined,
        })
      }
      this.$emit('updateTableDataRead', this.row, this.radioValue === 1 || this.radioValue === 2)
      this.handleCancel()
    },
    handleCancel() {
      this.radioValue = 1
      this.selectedAttr = []
      if (this.$refs.form) {
        this.$refs.form.resetFields()
      }
      this.visible = false
    },
    setExpFromFilter(filterExp) {
      let expression = ''
      if (filterExp) {
        expression = `q=${filterExp}`
      }
      this.expression = expression
    },
    changeRadioValue(value) {
      if (this.id_filter) {
        this.$message.warning(this.$t('cmdb.serviceTree.grantedByServiceTreeTips'))
      } else {
        this.radioValue = value
      }
    },
  },
}
</script>

<style></style>
