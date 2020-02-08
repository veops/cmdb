<template>
  <div>
    <a-form :form="form" style="max-width: 500px; margin: 30px auto 0;">
      <a-row>
        <a-col :span="18">
          <a-form-item label="模板类型" :labelCol="labelCol" :wrapperCol="wrapperCol">
            <a-select
              placeholder="--请选择模板类型--"
              v-decorator="['ciTypes', { rules: [{required: true, message: '模板类型必须选择'}] }]"
              @change="selectCiType"
            >
              <a-select-option v-for="ciType in ciTypeList" :key="ciType.name" :value="ciType.id">{{ ciType.alias }}</a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item>
            <a-button
              style="margin-left: 20px"
              :disabled="downLoadButtonDis"
              @click="downLoadExcel"
            >{{ $t('button.download') }}</a-button>
          </a-form-item>
        </a-col>
      </a-row>
    </a-form>
    <a-divider />
  </div>
</template>

<script>
import { getCITypes } from '@/api/cmdb/CIType'
import { getCITypeAttributesById } from '@/api/cmdb/CITypeAttr'
import { writeExcel } from '@/api/cmdb/batch'

export default {
  name: 'CiTypeChoice',
  data () {
    return {
      labelCol: { lg: { span: 5 }, sm: { span: 5 } },
      wrapperCol: { lg: { span: 19 }, sm: { span: 19 } },
      form: this.$form.createForm(this),
      ciTypeList: [],
      ciTypeName: '',
      downLoadButtonDis: true,
      selectNum: 0,
      selectCiTypeAttrList: []
    }
  },
  created: function () {
    getCITypes().then(res => {
      this.ciTypeList = res.ci_types
    })
  },
  methods: {
    selectCiType (el) {
      // 当选择好模板类型时的回调函数
      this.downLoadButtonDis = false
      this.selectNum = el
      getCITypeAttributesById(el).then(res => {
        this.$emit('getCiTypeAttr', res)
        this.selectCiTypeAttrList = res
      })

      this.ciTypeList.forEach(item => {
        if (this.selectNum === item.id) {
          this.ciTypeName = item.alias || item.name
        }
      })
    },

    downLoadExcel () {
      const columns = []
      this.selectCiTypeAttrList.attributes.forEach(item => {
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
    }
  }
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
