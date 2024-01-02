<template>
  <div class="cmdb-batch-upload" :style="{ height: `${windowHeight - 64}px` }">
    <div id="title">
      <ci-type-choice ref="ciTypeChoice" @getCiTypeAttr="showCiType" />
    </div>
    <a-row>
      <a-col :span="12">
        <upload-file-form
          :isUploading="isUploading"
          :ciType="ciType"
          ref="uploadFileForm"
          @uploadDone="uploadDone"
        ></upload-file-form>
      </a-col>
      <a-col :span="24" v-if="ciType && uploadData.length">
        <CiUploadTable :ciTypeAttrs="ciTypeAttrs" ref="ciUploadTable" :uploadData="uploadData"></CiUploadTable>
        <div class="cmdb-batch-upload-action">
          <a-space size="large">
            <a-button type="primary" ghost @click="handleCancel">{{ $t('cancel') }}</a-button>
            <a-button @click="handleUpload" type="primary">{{ $t('upload') }}</a-button>
            <a-button v-if="hasError && !isUploading" @click="downloadError" type="primary">{{ $t('cmdb.batch.downloadFailed') }}</a-button>
          </a-space>
        </div>
      </a-col>
      <a-col :span="24" v-if="ciType">
        <upload-result
          ref="uploadResult"
          :upLoadData="uploadData"
          :ciType="ciType"
          :unique-field="uniqueField"
          :isUploading="isUploading"
          @uploadResultDone="uploadResultDone"
          @uploadResultError="uploadResultError"
        ></upload-result>
      </a-col>
    </a-row>
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
        this.$refs.ciTypeChoice.selectNum = null
        this.hasError = false
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
<style lang="less" scoped>
.cmdb-batch-upload {
  margin-bottom: -24px;
  padding: 24px;
  background-color: #fff;
  border-radius: 20px;
  overflow: auto;
  .cmdb-batch-upload-action {
    width: 50%;
    text-align: center;
    margin: 12px 0;
  }
}
</style>
