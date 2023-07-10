<template>
  <div class="cmdb-batch-upload" :style="{ height: `${windowHeight - 64}px` }">
    <div id="title">
      <ci-type-choice @getCiTypeAttr="showCiType" />
    </div>
    <a-row>
      <a-col :span="12">
        <upload-file-form ref="uploadFileForm" @uploadDone="uploadDone"></upload-file-form>
      </a-col>
      <a-col :span="24" v-if="ciType && uploadData.length">
        <CiUploadTable :ciTypeAttrs="ciTypeAttrs" ref="ciUploadTable" :uploadData="uploadData"></CiUploadTable>
        <div class="cmdb-batch-upload-action">
          <a-space size="large">
            <a-button type="primary" ghost @click="handleCancel">取消</a-button>
            <a-button @click="handleUpload" type="primary">上传</a-button>
          </a-space>
        </div>
      </a-col>
      <a-col :span="24">
        <upload-result
          ref="uploadResult"
          :upLoadData="uploadData"
          :ciType="ciType"
          :unique-field="uniqueField"
        ></upload-result>
      </a-col>
    </a-row>
  </div>
</template>

<script>
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
      displayUpload: true,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  inject: ['reload'],
  methods: {
    showCiType(message) {
      this.ciTypeAttrs = message
      this.ciType = message.type_id
      this.uniqueField = message.unique
      this.uniqueId = message.unique_id
    },
    uploadDone(dataList) {
      const _uploadData = filterNull(dataList).map((item, i) => {
        if (i > 0) {
          const _ele = {}
          item.forEach((ele, j) => {
            if (ele !== undefined && ele !== null) {
              _ele[dataList[0][j]] = ele
            }
          })
          return _ele
        }
        return item
      })
      this.uploadData = _uploadData.slice(1)
    },
    handleUpload() {
      if (!this.ciType) {
        this.$message.error('尚未选择模板类型')
        return
      }
      if (this.uploadData && this.uploadData.length > 0) {
        this.$nextTick(() => {
          this.$refs.uploadResult.upload2Server()
        })
      } else {
        this.$message.error('请上传文件')
      }
    },
    handleCancel() {
      this.reload()
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
