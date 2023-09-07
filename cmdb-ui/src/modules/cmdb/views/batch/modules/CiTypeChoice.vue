<template>
  <a-space>
    <span>模板类型：</span>
    <a-select
      showSearch
      placeholder="请选择模板类型"
      @change="selectCiType"
      :style="{ width: '300px' }"
      class="ops-select"
      :filter-option="filterOption"
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
    >下载模板</a-button
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
      <a-divider orientation="left">模型属性</a-divider>
      <a-checkbox
        @change="changeCheckAll"
        :style="{ marginBottom: '20px' }"
        :indeterminate="indeterminate"
        :checked="checkAll"
      >
        全选
      </a-checkbox>
      <br />
      <a-checkbox-group v-model="checkedAttrs">
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
        <a-divider orientation="left">模型关联</a-divider>
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
            <a-select :style="{ flex: 1 }" size="small" v-model="parentsForm[item.alias || item.name].attr">
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
import { downloadExcel } from '../../../utils/helper'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCITypeParent } from '@/modules/cmdb/api/CITypeRelation'

export default {
  name: 'CiTypeChoice',
  data() {
    return {
      ciTypeList: [],
      ciTypeName: '',
      selectNum: 0,
      selectCiTypeAttrList: [],
      visible: false,
      checkedAttrs: [],
      indeterminate: false,
      checkAll: true,
      parentsType: [],
      parentsForm: {},
      checkedParents: [],
    }
  },
  created: function() {
    getCITypes().then((res) => {
      this.ciTypeList = res.ci_types
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
      // 当选择好模板类型时的回调函数
      this.selectNum = el
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
      getCITypeParent(this.selectNum).then((res) => {
        this.parentsType = res.parents
        const _parentsForm = {}
        res.parents.forEach((item) => {
          const _find = item.attributes.find((attr) => attr.id === item.unique_id)
          _parentsForm[item.alias || item.name] = { attr: _find?.alias || _find?.name, value: '' }
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
      const columns1 = this.checkedAttrs.map((item) => {
        return {
          v: item,
          t: 's',
          s: {
            numFmt: 'string',
          },
        }
      })
      const columns2 = this.checkedParents.map((p) => {
        return {
          v: `$${p}.${this.parentsForm[p].attr}`,
          t: 's',
          s: {
            font: {
              color: {
                rgb: 'FF0000',
              },
            },
          },
        }
      })
      downloadExcel([[...columns1, ...columns2]], this.ciTypeName)
      this.handleCancel()
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
