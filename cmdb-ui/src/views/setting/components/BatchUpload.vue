<template>
  <a-modal
    :visible="visible"
    :title="$t('cs.companyStructure.batchImport')"
    dialogClass="ops-modal setting-structure-upload"
    :width="800"
    @cancel="close"
  >
    <div class="setting-structure-upload-steps">
      <div
        :class="{ 'setting-structure-upload-step': true, selected: index + 1 <= currentStep }"
        v-for="(step, index) in stepList"
        :key="step.value"
      >
        <div :class="{ 'setting-structure-upload-step-icon': true }">
          <ops-icon :type="step.icon" />
        </div>
        <span>{{ step.label }}</span>
      </div>
    </div>
    <template v-if="currentStep === 1">
      <a-upload :multiple="false" :customRequest="customRequest" accept=".xlsx" :showUploadList="false">
        <a-button :style="{ marginBottom: '20px' }" type="primary">
          <a-icon type="upload" />{{ $t('cs.companyStructure.selectFile') }}</a-button
        >
      </a-upload>
      <p>
        <a @click="download">
          <slot name="downloadTemplateText">{{ $t('cs.companyStructure.clickDownloadImportTemplate') }}</slot>
        </a>
      </p>
    </template>
    <div
      :style="{
        height: '60px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        whiteSpace: 'pre-wrap',
      }"
      v-if="currentStep === 3"
    >
      {{ $t('cs.companyStructure.importSuccess', { allCount: allCount })
      }}<span :style="{ color: '#2362FB' }"> {{ allCount - errorCount }} </span>{{ $t('cs.companyStructure.count') }},
      {{ $t('cs.companyStructure.importFailed') }}<span :style="{ color: '#D81E06' }"> {{ errorCount }} </span
      >{{ $t('cs.companyStructure.count') }}
    </div>
    <slot>
      <vxe-table
        v-if="currentStep === 2 || has_error"
        ref="employeeTable"
        stripe
        :data="importData"
        show-overflow
        show-header-overflow
        highlight-hover-row
        size="small"
        class="ops-stripe-table"
        :max-height="400"
        :column-config="{ resizable: true }"
      >
        <vxe-column field="email" :title="$t('cs.companyStructure.email')" min-width="120" fixed="left"></vxe-column>
        <vxe-column field="username" :title="$t('cs.companyStructure.username')" min-width="80"></vxe-column>
        <vxe-column field="nickname" :title="$t('cs.companyStructure.nickname')" min-width="80"></vxe-column>
        <vxe-column field="password" :title="$t('cs.companyStructure.password')" min-width="80"></vxe-column>
        <vxe-column field="sex" :title="$t('cs.companyStructure.sex')" min-width="60"></vxe-column>
        <vxe-column field="mobile" :title="$t('cs.companyStructure.mobile')" min-width="80"></vxe-column>
        <vxe-column
          field="department_name"
          :title="$t('cs.companyStructure.departmentName')"
          min-width="80"
        ></vxe-column>
        <vxe-column field="position_name" :title="$t('cs.companyStructure.positionName')" min-width="80"></vxe-column>
        <vxe-column field="work_region" :title="$t('cs.companyStructure.work_region')" min-width="80"></vxe-column>
        <vxe-column
          v-if="has_error"
          field="err"
          :title="$t('cs.companyStructure.importFailedReason')"
          min-width="120"
          fixed="right"
        >
          <template #default="{ row }">
            <span :style="{ color: '#D81E06' }">{{ row.err }}</span>
          </template>
        </vxe-column>
      </vxe-table>
    </slot>
    <a-space slot="footer">
      <a-button size="small" type="primary" ghost @click="close">{{ $t('cancel') }}</a-button>
      <a-button v-if="currentStep !== 1" size="small" type="primary" ghost @click="goPre">{{
        $t('cs.companyStructure.prevStep')
      }}</a-button>
      <a-button v-if="currentStep !== 3" size="small" type="primary" @click="goNext">{{
        $t('cs.companyStructure.nextStep')
      }}</a-button>
      <a-button v-else size="small" type="primary" @click="close">{{ $t('cs.companyStructure.done') }}</a-button>
    </a-space>
  </a-modal>
</template>

<script>
export default {
  name: 'BatchUpload',
  data() {
    const stepList = [
      {
        value: 1,
        label: this.$t('cs.companyStructure.uploadFile'),
        icon: 'icon-shidi-tianjia',
      },
      {
        value: 2,
        label: this.$t('cs.companyStructure.confirmData'),
        icon: 'icon-shidi-yunshangchuan',
      },
      {
        value: 3,
        label: this.$t('cs.companyStructure.uploadDone'),
        icon: 'icon-shidi-queren',
      },
    ]

    return {
      stepList,
      visible: false,
      currentStep: 1,
      importData: [],
      has_error: false,
      allCount: 0,
      errorCount: 0,
    }
  },
  methods: {
    open() {
      this.importData = []
      this.has_error = false
      this.errorCount = 0
      this.visible = true
    },
    close() {
      this.currentStep = 1
      this.visible = false
    },
    async goNext() {
      if (this.currentStep === 2) {
        this.allCount = this.importData.length
        this.$emit('import', { importData: this.importData }, (res) => {
          if (res.length) {
            const errData = res.filter((item) => {
              return item.err.length
            })
            console.log('err', errData)
            this.has_error = true
            this.errorCount = errData.length
            this.currentStep += 1
            this.importData = errData
            this.$message.error(this.$t('cs.companyStructure.dataErr'))
          } else {
            this.currentStep += 1
            this.$message.success(this.$t('cs.companyStructure.opSuccess'))
          }
          this.$emit('refresh')
        })
      }
    },
    goPre() {
      this.has_error = false
      this.errorCount = 0
      this.currentStep -= 1
    },
    download() {
      this.$emit('downloadTemplate')
    },
    customRequest(data) {
      this.fileList = [data.file]
      this.$emit('customRequest', { data }, (importData) => {
        this.importData = importData
        this.currentStep = 2
      })
    },
  },
}
</script>

<style lang="less">
.setting-structure-upload {
  .ant-modal-body {
    padding: 24px 48px;
  }
  .setting-structure-upload-steps {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 20px;
    .setting-structure-upload-step {
      display: inline-block;
      text-align: center;
      position: relative;
      .setting-structure-upload-step-icon {
        width: 86px;
        height: 86px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-image: url('../../../assets/icon-bg.png');
        margin-bottom: 20px;
        > i {
          font-size: 40px;
          color: #fff;
        }
      }
      > span {
        font-size: 16px;
        font-weight: 600;
        color: rgba(0, 0, 0, 0.5);
      }
    }
    .setting-structure-upload-step:not(:first-child)::before {
      content: '';
      height: 2px;
      width: 223px;
      position: absolute;
      background-color: #e7ecf3;
      left: -223px;
      top: 43px;
      z-index: 0;
    }
    .selected.setting-structure-upload-step {
      &:not(:first-child)::before {
        background-color: #7eb0ff;
      }
    }
    .selected {
      .setting-structure-upload-step-icon {
        background-image: url('../../../assets/icon-bg-selected.png');
      }
      > span {
        color: rgba(0, 0, 0, 0.8);
      }
    }
  }
}
</style>
