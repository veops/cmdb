<template>
  <a-modal :width="680" :title="title" :visible="visible" @ok="handleOk" @cancel="handleCancel">
    <div class="read-grant-modal-desc">{{ modalDesc }}</div>
    <a-radio-group v-model="radioValue" @change="(e) => changeRadioValue(e.target.value)" style="width: 100%;">
      <div class="radio-option">
        <a-radio :value="1">
          {{ $t('cmdb.components.all') }}
        </a-radio>
        <span class="radio-desc">{{ $t('cmdb.components.allDesc') }}</span>
      </div>
      <div class="radio-option">
        <a-radio :value="2">
          {{ $t('cmdb.components.customize') }}
        </a-radio>
        <span class="radio-desc">{{ $t('cmdb.components.customizeDesc') }}</span>
      </div>
      <div v-if="radioValue === 2" style="margin-left: 24px; margin-top: 12px; margin-bottom: 12px;">
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
          <div class="read-ci-tip">{{ $t('cmdb.ciType.ciGrantTip') }}</div>
        </a-form-model>
      </div>
      <div class="radio-option">
        <a-radio :value="3">
          {{ $t('cmdb.components.none') }}
        </a-radio>
        <span class="radio-desc">{{ $t('cmdb.components.noneDesc') }}</span>
      </div>
    </a-radio-group>
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
    modalDesc() {
      if (this.colType === 'read_attr') {
        return this.$t('cmdb.components.readAttrModalDesc')
      }
      return this.$t('cmdb.components.readCIModalDesc')
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

<style lang="less" scoped>
.read-grant-modal-desc {
  color: #999;
  font-size: 12px;
  margin-bottom: 16px;
  padding: 8px 12px;
  background-color: #f5f5f5;
  border-left: 3px solid @primary-color;
}

.radio-option {
  margin-bottom: 12px;
  display: flex;
  align-items: baseline;

  .radio-desc {
    color: #999;
    font-size: 12px;
    margin-left: 8px;
  }
}

.read-ci-tip {
  font-size: 12px;
  line-height: 22px;
  color: #a5a9bc;
}
</style>
