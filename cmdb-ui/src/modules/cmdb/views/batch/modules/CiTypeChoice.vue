<template>
  <a-space>
    <span>{{ $t('cmdb.ciType.ciType') }}: </span>
    <a-select
      showSearch
      :placeholder="$t('cmdb.batch.selectCITypeTips')"
      @change="selectCiType"
      :style="{ width: '300px' }"
      class="ops-select"
      :filter-option="filterOption"
      v-model="selectNum"
    >
      <a-select-option v-for="ciType in ciTypeList" :key="ciType.name" :value="ciType.id">{{
        ciType.alias
      }}</a-select-option>
    </a-select>
    <a-button
      @click="openModal"
      :disabled="!selectNum"
      type="primary"
      class="ops-button-primary"
      icon="download"
    >{{ $t('cmdb.batch.downloadTemplate') }}</a-button
    >
    <a-modal
      :bodyStyle="{ paddingTop: 0 }"
      width="800px"
      :title="`${ciTypeName}`"
      :visible="visible"
      @cancel="handleCancel"
      @ok="handleOk"
      wrapClassName="ci-type-choice-modal"
    >
      <a-divider orientation="left">{{ $t('cmdb.ciType.attributes') }}</a-divider>
      <a-checkbox
        @change="changeCheckAll"
        :style="{ marginBottom: '20px' }"
        :indeterminate="indeterminate"
        :checked="checkAll"
      >
        {{ $t('checkAll') }}
      </a-checkbox>
      <br />
      <a-checkbox-group style="width:100%" v-model="checkedAttrs">
        <a-row>
          <a-col :span="6" v-for="item in selectCiTypeAttrList.attributes" :key="item.alias || item.name">
            <a-checkbox :disabled="item.name === selectCiTypeAttrList.unique" :value="item.alias || item.name">
              {{ item.alias || item.name }}
              <span style="color: red" v-if="item.name === selectCiTypeAttrList.unique">*</span>
            </a-checkbox>
          </a-col>
        </a-row>
      </a-checkbox-group>
      <template v-if="parentsType && parentsType.length">
        <a-divider orientation="left">{{ $t('cmdb.ciType.relation') }}</a-divider>
        <a-row :gutter="[24, 24]" align="top" type="flex">
          <a-col :style="{ display: 'inline-flex' }" :span="12" v-for="item in parentsType" :key="item.id">
            <a-checkbox @click="clickParent(item)" :checked="checkedParents.includes(item.alias || item.name)">
            </a-checkbox>
            <span
              :style="{
                display: 'inline-block',
                overflow: 'hidden',
                whiteSpace: 'nowrap',
                textOverflow: 'ellipsis',
                width: '80px',
                margin: '0 5px',
                textAlign: 'right',
              }"
              :title="item.alias || item.name"
            >{{ item.alias || item.name }}</span
            >
            <a-select
              :style="{ flex: 1 }"
              size="small"
              v-model="parentsForm[item.alias || item.name].selectedParentAttr"
            >
              <a-select-option
                :title="attr.alias || attr.name"
                v-for="attr in item.attributes"
                :key="attr.alias || attr.name"
                :value="attr.alias || attr.name"
              >
                {{ attr.alias || attr.name }}
              </a-select-option>
            </a-select>
          </a-col>
        </a-row>
      </template>
    </a-modal>
  </a-space>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import ExcelJS from 'exceljs'
import FileSaver from 'file-saver'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCITypeParent, getCanEditByParentIdChildId } from '@/modules/cmdb/api/CITypeRelation'
import { searchPermResourceByRoleId } from '@/modules/acl/api/permission'

export default {
  name: 'CiTypeChoice',
  data() {
    return {
      ciTypeList: [],
      ciTypeName: '',
      selectNum: null,
      selectCiTypeAttrList: [],
      visible: false,
      checkedAttrs: [],
      indeterminate: false,
      checkAll: true,
      parentsType: [],
      parentsForm: {},
      checkedParents: [],
      canEdit: {},
    }
  },
  computed: {
    ...mapState({
      rid: (state) => state.user.rid,
    }),
  },
  async created() {
    const { resources } = await searchPermResourceByRoleId(this.rid, {
      resource_type_id: 'CIType',
      app_id: 'cmdb',
    })
    getCITypes().then((res) => {
      this.ciTypeList = res.ci_types.filter((type) => {
        const _findRe = resources.find((re) => re.name === type.name)
        return _findRe?.permissions.includes('create') ?? false
      })
    })
  },
  watch: {
    checkedAttrs() {
      if (this.checkedAttrs.length < this.selectCiTypeAttrList.attributes.length) {
        this.indeterminate = true
        this.checkAll = false
      }
      if (this.checkedAttrs.length === this.selectCiTypeAttrList.attributes.length) {
        this.indeterminate = false
        this.checkAll = true
      }
    },
  },
  methods: {
    selectCiType(el) {
      // Callback function when a template type is selected
      getCITypeAttributesById(el).then((res) => {
        this.$emit('getCiTypeAttr', res)
        this.selectCiTypeAttrList = res
      })

      this.ciTypeList.forEach((item) => {
        if (this.selectNum === item.id) {
          this.ciTypeName = item.alias || item.name
        }
      })
    },

    openModal() {
      getCITypeParent(this.selectNum).then(async (res) => {
        for (let i = 0; i < res.parents.length; i++) {
          await getCanEditByParentIdChildId(res.parents[i].id, this.selectNum).then((p_res) => {
            this.canEdit = {
              ..._.cloneDeep(this.canEdit),
              [res.parents[i].id]: p_res.result,
            }
          })
        }
        this.parentsType = res.parents.filter((parent) => this.canEdit[parent.id])
        const _parentsForm = {}
        res.parents.forEach((item) => {
          const _find = item.attributes.find((attr) => attr.id === item.unique_id)
          _parentsForm[item.alias || item.name] = { ...item, selectedParentAttr: _find?.alias || _find?.name }
        })
        this.parentsForm = _parentsForm
        this.checkedParents = []
        this.visible = true
        this.checkedAttrs = this.selectCiTypeAttrList.attributes.map((item) => item.alias || item.name)
      })
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
    },
    handleCancel() {
      this.visible = false
    },
    handleOk() {
      const excel_name = `${this.ciTypeName}.xlsx`
      const wb = new ExcelJS.Workbook()
      const ws = wb.addWorksheet(this.ciTypeName)
      const choice_value_obj = {}
      const columns1 = this.checkedAttrs.map((item, index) => {
        const _find = this.selectCiTypeAttrList.attributes.find((attr) => item === attr.alias || item === attr.name)
        if (_find?.choice_value && _find?.choice_value.length) {
          choice_value_obj[item] = {
            choice_value: _find?.choice_value,
            columnIdx: index + 1,
          }
        }
        return {
          header: item,
          key: item,
          width: 20,
        }
      })

      const columns2 = this.checkedParents.map((p, idx) => {
        const _selectedParentAttr = this.parentsForm[p].selectedParentAttr
        const _find = this.parentsForm[p].attributes.find(
          (attr) => _selectedParentAttr === attr.alias || _selectedParentAttr === attr.name
        )
        if (_find?.choice_value && _find?.choice_value.length) {
          choice_value_obj[p] = {
            choice_value: _find?.choice_value,
            columnIdx: columns1.length + idx + 1,
          }
        }
        return {
          header: `$${p}.${this.parentsForm[p].selectedParentAttr}`,
          key: `$${p}.${this.parentsForm[p].selectedParentAttr}`,
          width: 40,
          style: {
            font: {
              color: { argb: 'ff0000' },
            },
          },
        }
      })
      ws.columns = [...columns1, ...columns2]

      for (let row = 2; row < 5000; row++) {
        Object.keys(choice_value_obj).forEach((key) => {
          const formulae = `"${choice_value_obj[key].choice_value.map((value) => value[0]).join(',')}"`
          if (formulae.length <= 255) {
            ws.getCell(row, choice_value_obj[key].columnIdx).dataValidation = {
              type: 'list',
              formulae: [formulae],
            }
          }
        })
      }

      wb.xlsx.writeBuffer().then((buffer) => {
        const file = new Blob([buffer], {
          type: 'application/octet-stream',
        })
        FileSaver.saveAs(file, excel_name)
        this.handleCancel()
      })
    },
    changeCheckAll(e) {
      if (e.target.checked) {
        this.checkedAttrs = this.selectCiTypeAttrList.attributes.map((item) => item.alias || item.name)
      } else {
        const _find = this.selectCiTypeAttrList.attributes.find(
          (item) => item.name === this.selectCiTypeAttrList.unique
        )
        this.checkedAttrs = [_find?.alias || _find?.name]
      }
    },
    clickParent(item) {
      const _idx = this.checkedParents.findIndex((p) => p === (item.alias || item.name))
      if (_idx > -1) {
        this.checkedParents.splice(_idx, 1)
      } else {
        this.checkedParents.push(item.alias || item.name)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.step-form-style-desc {
  padding: 0 56px;
  color: rgba(0, 0, 0, 0.45);
  h3 {
    margin: 0 0 12px;
    color: rgba(0, 0, 0, 0.45);
    font-size: 16px;
    line-height: 32px;
  }
  h4 {
    margin: 0 0 4px;
    color: rgba(0, 0, 0, 0.45);
    font-size: 14px;
    line-height: 22px;
  }
  p {
    margin-top: 0;
    margin-bottom: 12px;
    line-height: 22px;
  }
}
</style>

<style lang="less">
.ci-type-choice-modal {
  .ant-checkbox-disabled .ant-checkbox-inner {
    border-color: #2f54eb !important;
    background-color: #2f54eb;
  }
  .ant-checkbox-disabled.ant-checkbox-checked .ant-checkbox-inner::after {
    border-color: #fff;
  }
}
</style>
