<template>
  <div>
    <div class="attr-ad-header attr-ad-header-margin">{{ $t('cmdb.ciType.configCheckTitle') }}</div>
    <div class="attr-ad-content">
      <div class="ad-test-title-info">{{ $t('cmdb.ciType.checkTestTip') }}</div>
      <div
        class="ad-test-btn"
        @click="showCheckModal"
      >
        {{ $t('cmdb.ciType.checkTestBtn') }}
      </div>
      <div class="ad-test-btn-info">{{ $t('cmdb.ciType.checkTestTip2') }}</div>
      <!-- <div
        class="ad-test-btn"
        @click="showTestModal"
      >
        {{ $t('cmdb.ciType.checkTestBtn1') }}
      </div>
      <div class="ad-test-btn-info">{{ $t('cmdb.ciType.checkTestTip3') }}</div> -->
    </div>

    <a-modal
      v-model="checkModalVisible"
      :footer="null"
      :width="900"
    >
      <div class="check-modal-title">{{ $t('cmdb.ciType.checkModalTitle') }}</div>
      <div class="check-modal-info">{{ $t('cmdb.ciType.checkModalTip') }}</div>
      <div class="check-modal-info">{{ $t('cmdb.ciType.checkModalTip1') }}</div>
      <div class="check-modal-info">{{ $t('cmdb.ciType.checkModalTip2') }}</div>
      <ops-table
        size="mini"
        :data="checkTableData"
        :scroll-y="{ enabled: true }"
        height="400"
        class="check-modal-table"
      >
        <vxe-column field="oneagent_name" :title="$t('cmdb.ciType.checkModalColumn1')"></vxe-column>
        <vxe-column field="oneagent_id" :title="$t('cmdb.ciType.checkModalColumn2')"></vxe-column>
        <vxe-column
          field="status"
          :min-width="70"
          :title="$t('cmdb.ciType.checkModalColumn3')"
        >
          <template #default="{ row }">
            <div
              :class="['check-modal-status', row.status ? 'check-modal-status-online' : 'check-modal-status-offline']"
            >
              {{ $t(`cmdb.ciType.${row.status ? 'checkModalColumnStatus1' : 'checkModalColumnStatus2'}`) }}
            </div>
          </template>
        </vxe-column>
        <vxe-column field="sync_at" :title="$t('cmdb.ciType.checkModalColumn4')"></vxe-column>
      </ops-table>
    </a-modal>

    <a-modal
      v-model="testModalVisible"
      :footer="null"
      :width="596"
    >
      <div class="check-modal-title">{{ $t('cmdb.ciType.testModalTitle') }}</div>
      <p class="test-modal-text">{{ testResultText }}</p>
    </a-modal>
  </div>
</template>

<script>
import {
  getAdtSyncHistories,
  postAdtTest,
  getAdtTestResult
} from '@/modules/cmdb/api/discovery.js'
import moment from 'moment'

export default {
  name: 'AttrADTest',
  props: {
    adtId: {
      type: Number,
      default: 0,
    }
  },
  data() {
    return {
      checkModalVisible: false,
      checkTableData: [],
      testModalVisible: false,
      testResultText: '',
    }
  },
  methods: {
    async showCheckModal() {
      await this.queryCheckTableData()
      this.checkModalVisible = true
    },
    async queryCheckTableData() {
      const res = await getAdtSyncHistories(this.adtId)
      if (res?.result?.length) {
        const newTableData = res.result
        newTableData.forEach((item) => {
          const syncTime = moment(item.sync_at).valueOf()
          const nowTime = new Date().getTime()
          item.status = nowTime - syncTime <= 10 * 60 * 1000
        })
        this.checkTableData = newTableData
      } else {
        this.checkTableData = []
      }
    },
    async showTestModal() {
      await this.queryTestResult()
      this.testModalVisible = true
    },
    async queryTestResult() {
      const res = await postAdtTest(this.adtId)
      const exec_id = res?.exec_id
      if (exec_id) {
        const res = await getAdtTestResult(exec_id)

        if (res?.stdout) {
          this.testResultText = res.stdout
        }
      }
    }
  },
}
</script>

<style lang="less" scoped>
.attr-ad-content {
  margin-left: 17px;
  margin-bottom: 20px;

  .ad-test-title-info {
    color: @text-color_3;
    font-size: 12px;
    font-weight: 400;
  }

  .ad-test-btn {
    margin-top: 30px;
    padding: 5px 12px;
    background-color: #F4F9FF;
    border: solid 1px @primary-color_8;
    display: inline-block;
    cursor: pointer;

    color: @link-color;
    font-size: 12px;
    font-weight: 400;
  }

  .ad-test-btn-info {
    margin-top: 4px;
    color: @text-color_3;
    font-size: 12px;
    font-weight: 400;
  }
}

.check-modal-table {
  margin-top: 14px;
}

.check-modal-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
}

.check-modal-info {
  color: @text-color_3;
  font-size: 12px;
  font-weight: 400;
}

.check-modal-status {
  display: inline-block;
  padding: 2px 11px;
  font-size: 12px;
  font-weight: 400;

  &-online {
    background-color: #E5F6DF;
    color: #30AD2D;
  }

  &-offline {
    background-color: #FFDADA;
    color: #F14E4E;
  }
}

.test-modal-text {
  margin-top: 14px;
  padding: 12px;
  width: 100%;
  height: 312px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-all;
  border: solid 1px @border-color-base;
}
</style>
