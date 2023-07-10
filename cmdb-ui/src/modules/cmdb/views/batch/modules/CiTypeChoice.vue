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
      @click="downLoadExcel"
      :disabled="!selectNum"
      type="primary"
      class="ops-button-primary"
      icon="download"
    >下载模板</a-button
    >
  </a-space>
</template>

<script>
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { writeExcel } from '@/modules/cmdb/api/batch'

export default {
  name: 'CiTypeChoice',
  data() {
    return {
      ciTypeList: [],
      ciTypeName: '',
      selectNum: 0,
      selectCiTypeAttrList: [],
    }
  },
  created: function() {
    getCITypes().then((res) => {
      this.ciTypeList = res.ci_types
    })
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

    downLoadExcel() {
      const columns = []
      this.selectCiTypeAttrList.attributes.forEach((item) => {
        columns.push(item.alias)
      })
      const excel = writeExcel(columns, this.ciTypeName)
      const tempLink = document.createElement('a')
      tempLink.download = this.ciTypeName + '.xls'
      tempLink.style.display = 'none'
      const blob = new Blob([excel])
      tempLink.href = URL.createObjectURL(blob)
      document.body.appendChild(tempLink)
      tempLink.click()
      document.body.removeChild(tempLink)
    },
    filterOption(input, option) {
      return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
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
