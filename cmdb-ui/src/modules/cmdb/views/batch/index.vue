<template>
  <div class="cmdb-batch-upload" :style="{ height: `${windowHeight - 64}px` }">
    <div class="cmdb-batch-upload-header">
      <div class="cmdb-batch-upload-header-title">
        <ops-icon type="ops-cmdb-batch" class="cmdb-batch-upload-header-icon" />
        <span>{{ $t('cmdb.menu.batchUpload') }}</span>
      </div>
    </div>

    <a-steps :current="currentStep" class="cmdb-batch-upload-steps">
      <a-step>
        <span slot="title">{{ $t('cmdb.batch.selectCIType') }}</span>
        <span slot="description">{{ $t('cmdb.batch.downloadTemplate') }}</span>
      </a-step>
      <a-step :title="$t('cmdb.batch.uploadFile')" />
      <a-step :title="$t('cmdb.batch.dataPreview')" />
    </a-steps>

    <div class="cmdb-batch-upload-content">
      <a-card class="cmdb-batch-upload-card">
        <template slot="title">
          <span class="cmdb-batch-upload-card-title">1. {{ $t('cmdb.batch.selectCIType') }} & {{ $t('cmdb.batch.downloadTemplate') }}</span>
        </template>
        <CiTypeChoice ref="ciTypeChoice" @getCiTypeAttr="showCiType" @stepChange="handleStepChange" />
      </a-card>

      <a-card class="cmdb-batch-upload-card">
        <template slot="title">
          <span class="cmdb-batch-upload-card-title">2. {{ $t('cmdb.batch.uploadFile') }}</span>
        </template>
        <UploadFileForm
          :isUploading="isUploading"
          :ciType="ciType"
          ref="uploadFileForm"
          @uploadDone="uploadDone"
        ></UploadFileForm>
      </a-card>

      <a-card class="cmdb-batch-upload-card">
        <template slot="title">
          <span class="cmdb-batch-upload-card-title">3. {{ $t('cmdb.batch.dataPreview') }}</span>
        </template>
        <CiUploadTable :ciTypeAttrs="ciTypeAttrs" ref="ciUploadTable" :uploadData="uploadData"></CiUploadTable>
      </a-card>
    </div>
    <div class="cmdb-batch-upload-action">
      <a-space size="large">
        <a-button :disabled="!(ciType && uploadData.length)" @click="handleUpload" type="primary">
          <a-icon type="upload" />
          {{ $t('upload') }}
        </a-button>
        <a-button @click="handleCancel">{{ $t('cancel') }}</a-button>
        <a-button v-if="hasError && !isUploading" @click="downloadError" type="primary" ghost class="ops-button-ghost">
          <a-icon type="download" />
          {{ $t('cmdb.batch.downloadFailed') }}
        </a-button>
      </a-space>
    </div>

    <UploadResult
      v-if="ciType"
      ref="uploadResult"
      :upLoadData="uploadData"
      :ciType="ciType"
      :unique-field="uniqueField"
      :isUploading="isUploading"
      @uploadResultDone="uploadResultDone"
      @uploadResultError="uploadResultError"
    ></UploadResult>
  </div>
</template>

<script>
import moment from 'moment'
import { mapState } from 'vuex'
import CiTypeChoice from './modules/CiTypeChoice'
import CiUploadTable from './modules/CiUploadTable'
import UploadFileForm from './modules/UploadFileForm'
import UploadResult from './modules/UploadResult'
import { filterNull } from '@/modules/cmdb/api/batch'

export default {
  name: 'BatchUpload',
  components: {
    CiTypeChoice,
    CiUploadTable,
    UploadFileForm,
    UploadResult,
  },
  data() {
    return {
      ciTypeAttrs: {},
      uploadData: [],
      ciType: 0,
      uniqueField: '',
      uniqueId: 0,
      isUploading: false,
      hasError: false,
      currentStep: 0,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  methods: {
    showCiType(message) {
      this.ciTypeAttrs = message ?? {}
      this.ciType = message?.type_id ?? 0
      this.uniqueField = message?.unique ?? ''
      this.uniqueId = message?.unique_id ?? 0
      if (message) {
        this.currentStep = Math.max(this.currentStep, 1)
      }
    },
    handleStepChange(step) {
      this.currentStep = Math.max(this.currentStep, step)
    },
    uploadDone(dataList) {
      const _uploadData = filterNull(dataList).map((item, i) => {
        if (i > 0) {
          const _ele = {}
          item.forEach((ele, j) => {
            if (ele !== undefined && ele !== null) {
              const _find = this.ciTypeAttrs.attributes.find(
                (attr) => attr.alias === dataList[0][j] || attr.name === dataList[0][j]
              )
              if (_find?.value_type === '4' && typeof ele === 'number') {
                _ele[dataList[0][j]] = moment(Math.round((ele - 25569) * 86400 * 1000 - 28800000)).format('YYYY-MM-DD')
              } else if (_find?.value_type === '3' && typeof ele === 'number') {
                _ele[dataList[0][j]] = moment(Math.round((ele - 25569) * 86400 * 1000 - 28800000)).format(
                  'YYYY-MM-DD HH:mm:ss'
                )
              } else if (_find?.value_type === '5' && typeof ele === 'number') {
                _ele[dataList[0][j]] = moment(Math.round(ele * 86400 * 1000 - 28800000)).format('HH:mm:ss')
              } else {
                _ele[dataList[0][j]] = ele
              }
            }
          })
          return _ele
        }
        return item
      })
      this.uploadData = _uploadData.slice(1)
      this.hasError = false
      this.isUploading = false
      if (_uploadData.length > 1) {
        this.currentStep = Math.max(this.currentStep, 2)
      }
    },
    handleUpload() {
      if (!this.ciType) {
        this.$message.error(this.$t('cmdb.batch.unselectCIType'))
        return
      }
      if (this.uploadData && this.uploadData.length > 0) {
        this.isUploading = true
        this.$nextTick(() => {
          this.$refs.uploadResult.upload2Server()
        })
      } else {
        this.$message.error(this.$t('cmdb.batch.pleaseUploadFile'))
      }
    },
    handleCancel() {
      if (!this.isUploading) {
        this.showCiType(null)
        this.$refs.ciTypeChoice.selectNum = undefined
        this.hasError = false
        this.currentStep = 0
        this.uploadData = []
      } else {
        this.$message.warning(this.$t('cmdb.batch.batchUploadCanceled'))
        this.isUploading = false
      }
    },
    uploadResultDone() {
      this.isUploading = false
    },
    uploadResultError(index) {
      this.hasError = true
      this.$refs.ciUploadTable.uploadResultError(index)
    },
    downloadError() {
      this.$refs.ciUploadTable.downloadError()
    },
  },
}
</script>
<style lang="less">
@import '../index.less';
.cmdb-batch-upload-label {
  color: @text-color_1;
  font-weight: bold;
  white-space: pre;
  > span {
    color: red;
  }
}
</style>
<style lang="less" scoped>
.cmdb-batch-upload {
  margin-bottom: -24px;
  padding: 24px;
  background-color: #f7f8fa;
  border-radius: @border-radius-box;
  overflow: auto;

  &-header {
    margin-bottom: 24px;

    &-title {
      display: flex;
      align-items: center;
      font-size: 18px;
      font-weight: 600;
      color: @text-color_1;
      gap: 10px;
    }

    &-icon {
      font-size: 24px;
      color: @primary-color;
    }
  }

  &-steps {
    background: #fff;
    padding: 24px 48px;
    border-radius: 8px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

    /deep/ .ant-steps-item-process .ant-steps-item-icon {
      background-color: @primary-color;
      border-color: @primary-color;

      .ant-steps-icon {
        color: #fff;
      }
    }

    /deep/ .ant-steps-item-finish .ant-steps-item-icon {
      border-color: @primary-color;

      .ant-steps-icon {
        color: @primary-color;
      }
    }

    /deep/ .ant-steps-item-wait .ant-steps-item-icon {
      border-color: #d9d9d9;

      .ant-steps-icon {
        color: rgba(0, 0, 0, 0.25);
      }
    }
  }

  &-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  &-card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: box-shadow 0.3s ease;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }

    /deep/ .ant-card-head {
      border-bottom: 1px solid #e8eaed;
      background: #fafafa;
      border-radius: 8px 8px 0 0;

      .ant-card-head-title {
        font-size: 15px;
        font-weight: 600;
        color: @text-color_1;
      }
    }

    /deep/ .ant-card-body {
      padding: 24px;
    }
  }

  &-action {
    margin-top: 24px;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    display: flex;
    justify-content: center;
  }
}
</style>
