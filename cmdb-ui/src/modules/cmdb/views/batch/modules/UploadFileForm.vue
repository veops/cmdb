<template>
  <div class="cmdb-batch-upload-dragger">
    <a-upload-dragger
      ref="upload"
      :multiple="false"
      :customRequest="customRequest"
      accept=".xls,.xlsx"
      :showUploadList="false"
      :fileList="fileList"
      :disabled="!ciType || isUploading"
    >
      <img :style="{ width: '80px', height: '80px' }" src="@/assets/file_upload.png" />
      <p class="ant-upload-text">{{ $t('cmdb.batch.drawTips') }}</p>
      <p class="ant-upload-hint">{{ $t('cmdb.batch.supportFileTypes') }}</p>
    </a-upload-dragger>
    <div v-for="item in fileList" :key="item.name" class="cmdb-batch-upload-dragger-file">
      <span><a-icon type="file" :style="{ color: '#2F54EB', marginRight: '5px' }" />{{ item.name }}</span>
      <a-progress :status="progressStatus" :percent="percent" />
    </div>
  </div>
</template>

<script>
import { processFile } from '@/modules/cmdb/api/batch'

export default {
  name: 'UploadFileForm',
  props: {
    ciType: {
      type: Number,
      default: 0,
    },
    isUploading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ciItemNum: 0,
      fileList: [],
      dataList: [],
      progressStatus: 'active',
      percent: 0,
    }
  },
  watch: {
    ciType: {
      handler(newValue) {
        if (!newValue) {
          this.ciItemNum = 0
          this.fileList = []
          this.dataList = []
          this.progressStatus = 'active'
          this.percent = 0
          this.$emit('uploadDone', this.dataList)
        }
      },
    },
  },
  methods: {
    customRequest(data) {
      this.fileList = [data.file]
      processFile(data.file).then((res) => {
        this.progressStatus = 'success'
        this.percent = 100
        this.ciItemNum = res.length - 1
        this.dataList = res
        this.$emit('uploadDone', this.dataList)
      })
    },
    beforeUpload() {
      return false
    },
  },
}
</script>

<style lang="less">
.cmdb-batch-upload-dragger {
  height: 220px;
  margin: 16px 0;
  .ant-upload.ant-upload-drag {
    background: rgba(240, 245, 255, 0.35);
    border: none;
  }
  .ant-upload.ant-upload-drag .ant-upload-drag-container {
    vertical-align: baseline;
  }
}
</style>
<style lang="less" scoped>
.cmdb-batch-upload-dragger {
  position: relative;
  .cmdb-batch-upload-dragger-file {
    background-color: #fff;
    box-shadow: 0px 2px 5px rgba(78, 94, 160, 0.2);
    border-radius: 4px;
    position: absolute;
    width: 80%;
    left: 50%;
    bottom: 24px;
    padding: 2px 8px;
    transform: translate(-50%);
    display: inline-flex;
    > span {
      white-space: nowrap;
      margin-right: 10px;
    }
  }
}
</style>
