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
      <ops-icon type="itsm-folder" />
      <p class="ant-upload-hint">{{ $t('cmdb.batch.supportFileTypes') }}</p>
      <p v-html="$t('cmdb.batch.drawTips1')"></p>
      <p v-html="$t('cmdb.batch.drawTips2')"></p>
      <div v-for="item in fileList" :key="item.name" class="cmdb-batch-upload-dragger-file">
        <span><a-icon type="file" :style="{ color: '#2F54EB', marginRight: '5px' }" />{{ item.name }}</span>
        <a-progress :status="progressStatus" :percent="percent" />
      </div>
    </a-upload-dragger>
    <div class="cmdb-batch-upload-tips">
      <p>{{ $t('cmdb.batch.tips1') }}</p>
      <div>{{ $t('cmdb.batch.tips2') }}</div>
      <div>{{ $t('cmdb.batch.tips3') }}</div>
      <div>{{ $t('cmdb.batch.tips4') }}</div>
      <div>{{ $t('cmdb.batch.tips5') }}</div>
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
      handler() {
        this.ciItemNum = 0
        this.fileList = []
        this.dataList = []
        this.progressStatus = 'active'
        this.percent = 0
        this.$emit('uploadDone', this.dataList)
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
@import '~@/style/static.less';

.cmdb-batch-upload-dragger {
  height: auto;
  margin: 16px 0;
  .ant-upload p {
    margin-bottom: 5px;
  }
  .ant-upload.ant-upload-drag {
    border: none;
    background: linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
      linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
      linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y,
      linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y;
    background-size: 15px 1px, 15px 1px, 1px 15px, 1px 15px;
    background-position: 0 0, 0 100%, 0 0, 100% 0;
    .ant-upload-drag-container > i {
      font-size: 60px;
    }
    .cmdb-batch-upload-tips {
      color: @primary-color;
    }
  }
  .ant-upload.ant-upload-drag .ant-upload-drag-container {
    vertical-align: baseline;
  }
}
</style>
<style lang="less" scoped>
@import '~@/style/static.less';

.cmdb-batch-upload-dragger {
  position: relative;
  display: flex;
  > span {
    display: inline-block;
    width: 50%;
  }
  .cmdb-batch-upload-dragger-file {
    background-color: @primary-color_7;
    border-radius: 2px;
    width: 80%;
    padding: 2px 8px;
    display: inline-flex;
    > span {
      white-space: nowrap;
      margin-right: 10px;
    }
  }
  .cmdb-batch-upload-tips {
    width: 50%;
    padding-left: 20px;
    color: @text-color_3;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    p:first-child {
      color: @text-color_1;
    }
  }
}
</style>
