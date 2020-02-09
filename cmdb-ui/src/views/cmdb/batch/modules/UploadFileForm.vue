<template>
  <div>
    <a-form :form="form" style="max-width: 500px; margin: 40px auto 0;">
      <a-upload-dragger ref="upload" :multiple="true" :customRequest="customRequest" accept=".xls">
        <p class="ant-upload-drag-icon">
          <a-icon type="inbox" />
        </p>
        <p class="ant-upload-text">{{ $t('batch.dragFileHere') }}</p>
        <p class="ant-upload-hint">{{ $t('batch.suportFileType') }} : xls</p>
      </a-upload-dragger>
    </a-form>
    <a-divider>or</a-divider>
  </div>
</template>

<script>
import { processFile } from '@/api/cmdb/batch'

export default {
  name: 'Step2',
  data () {
    return {
      labelCol: { lg: { span: 5 }, sm: { span: 5 } },
      wrapperCol: { lg: { span: 19 }, sm: { span: 19 } },
      form: this.$form.createForm(this),
      loading: false,
      timer: 0,
      ciItemNum: 0,
      dataList: []
    }
  },

  methods: {
    customRequest (data) {
      processFile(data.file).then(res => {
        this.ciItemNum = res.length - 1
        document.getElementById('upload-button').disabled = false
        this.dataList = res
      })
    },

    handleChange (info) {
      document.getElementById('load-button').disabled = false
      console.log(info)
    },
    clear () {
      console.log(this.$refs.upload.$children[0].onSuccess('', ''))
    }
  }
}
</script>

<style lang="less" scoped>
.stepFormText {
  margin-bottom: 24px;
  .ant-form-item-label,
  .ant-form-item-control {
    line-height: 22px;
  }
}
</style>
