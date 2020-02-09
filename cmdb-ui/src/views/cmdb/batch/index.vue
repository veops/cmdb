<template>
  <div>
    <div id="title">
      <ci-type-choice @getCiTypeAttr="showCiType">
      </ci-type-choice>
    </div>
    <a-row>
      <a-col :span="18">
        <a-card style="height: 605px">
          <a-button class="ant-btn-primary" style="margin-left: 10px;" :disabled="uploadFlag" id="upload-button" @click="uploadData">{{ $t('button.upload') }}</a-button>
          <upload-file-form v-if="displayUpload" ref="fileEditor"></upload-file-form>
          <ci-table v-if="editorOnline" :ciTypeAttrs="ciTypeAttrs" ref="onlineEditor"></ci-table>
        </a-card>
      </a-col>
      <a-col :span="6">
        <div style="min-height: 604px; background: white">
          <a-card :title="$t('batch.uploadResult')">
            <upload-result v-if="beginLoad" :upLoadData="needDataList" :ciType="ciType" :unique-field="uniqueField"></upload-result>
          </a-card>
        </div>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import CiTypeChoice from './modules/CiTypeChoice'
import CiTable from './modules/CiTable'
import UploadFileForm from './modules/UploadFileForm'
import UploadResult from './modules/UploadResult'
import { filterNull } from '@/api/cmdb/batch'

export default {
  name: 'Batch',
  components: {
    CiTypeChoice,
    CiTable,
    UploadFileForm,
    UploadResult
  },
  data () {
    return {
      editorOnline: false,
      uploadFlag: true,
      ciTypeAttrs: [],
      needDataList: [],
      ciType: -1,
      uniqueField: '',
      uniqueId: 0,
      beginLoad: false,
      displayUpload: true
    }
  },
  methods: {
    showCiType (message) {
      this.ciTypeAttrs = message
      this.ciType = message.type_id
      this.uniqueField = message.unique
      this.uniqueId = message.unique_id
      this.editorOnline = false
      this.$nextTick(() => {
        this.editorOnline = true
      })
    },
    uploadData () {
      if (this.ciType < 0) {
        alert('尚未选择模板类型！')
        return
      }
      this.beginLoad = false
      const fileData = this.$refs.fileEditor.dataList
      if (fileData.length > 0) {
        this.needDataList = filterNull(fileData)
      } else {
        this.needDataList = filterNull(this.$refs.onlineEditor.getDataList())
      }
      this.displayUpload = false
      this.$nextTick(() => {
        this.beginLoad = true
        this.displayUpload = true
      })
    }
  }
}
</script>
