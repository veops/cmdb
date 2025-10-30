<template>
  <a-modal
    v-model="visible"
    :title="$t('cmdb.batch.uploadResult')"
    :footer="null"
    :width="700"
    :maskClosable="false"
  >
    <div class="cmdb-batch-upload-result">
      <a-result
        :status="errorNum > 0 ? 'warning' : 'success'"
        :title="errorNum > 0 ? $t('cmdb.batch.uploadPartialSuccess') : $t('cmdb.batch.uploadAllSuccess')"
      >
        <template #subTitle>
          <div class="upload-result-summary">
            <span>{{ $t('cmdb.batch.total') }}: <strong>{{ total }}</strong></span>
            <a-divider type="vertical" />
            <span class="success-text">{{ $t('cmdb.batch.successItems') }}: <strong>{{ success }}</strong></span>
            <a-divider type="vertical" />
            <span class="error-text">{{ $t('cmdb.batch.failedItems') }}: <strong>{{ errorNum }}</strong></span>
          </div>
        </template>
        <template #extra>
          <a-button type="primary" @click="handleOk">{{ $t('confirm') }}</a-button>
        </template>
      </a-result>

      <div v-if="errorItems.length > 0" class="error-details">
        <a-divider orientation="left">{{ $t('cmdb.batch.errorTips') }}</a-divider>
        <div class="error-list">
          <div
            v-for="(item, index) in errorItems"
            :key="index"
            class="error-item"
          >
            <a-icon type="close-circle" class="error-icon" />
            <span>{{ item }}</span>
          </div>
        </div>
      </div>
    </div>
  </a-modal>
</template>

<script>
import { uploadData } from '@/modules/cmdb/api/batch'

export default {
  name: 'Result',
  props: {
    upLoadData: {
      required: true,
      type: Array,
    },
    ciType: {
      required: true,
      type: Number,
    },
    uniqueField: {
      required: true,
      type: String,
    },
    isUploading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      visible: false,
      complete: 0,
      errorNum: 0,
      success: 0,
      errorItems: [],
    }
  },
  mounted() {},
  computed: {
    total() {
      return this.upLoadData.length || 0
    },
  },
  watch: {
    ciType: {
      handler() {
        this.visible = false
      },
    },
  },
  methods: {
    async upload2Server() {
      this.success = 0
      this.errorNum = 0
      this.errorItems = []
      const floor = Math.ceil(this.total / 6)
      for (let i = 0; i < floor; i++) {
        if (this.isUploading) {
          const itemList = this.upLoadData.slice(6 * i, 6 * i + 6)
          const promises = itemList.map((x) => uploadData(this.ciType, x))
          await Promise.allSettled(promises)
            .then((res) => {
              res.forEach((r, j) => {
                if (r.status === 'fulfilled') {
                  this.success += 1
                } else {
                  this.errorItems.push(r?.reason?.response?.data.message ?? this.$t('cmdb.batch.requestFailedTips'))
                  this.errorNum += 1
                  this.$emit('uploadResultError', 6 * i + j)
                }
              })
            })
            .finally(() => {
              this.complete += 6
            })
        } else {
          break
        }
      }
      if (this.isUploading) {
        this.visible = true
        this.$emit('uploadResultDone')
      }
    },
    handleOk() {
      this.visible = false
    },
  },
}
</script>
<style lang="less" scoped>
.cmdb-batch-upload-result {
  .upload-result-summary {
    font-size: 14px;
    margin-top: 16px;

    strong {
      font-size: 18px;
      margin-left: 4px;
    }

    .success-text {
      color: #52c41a;

      strong {
        color: #52c41a;
      }
    }

    .error-text {
      color: #ff4d4f;

      strong {
        color: #ff4d4f;
      }
    }
  }

  .error-details {
    margin-top: 24px;

    .error-list {
      max-height: 300px;
      overflow-y: auto;
      padding: 12px;
      background: #fff1f0;
      border: 1px solid #ffccc7;
      border-radius: 6px;

      .error-item {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        padding: 8px 0;
        color: @text-color_2;

        &:not(:last-child) {
          border-bottom: 1px solid #ffe7e5;
        }

        .error-icon {
          color: #ff4d4f;
          font-size: 16px;
          margin-top: 2px;
          flex-shrink: 0;
        }

        span {
          flex: 1;
          word-break: break-all;
        }
      }
    }
  }
}
</style>
