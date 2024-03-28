<template>
  <div class="cmdb-batch-upload-result" v-if="visible">
    <p class="cmdb-batch-upload-label">5. {{ $t('cmdb.batch.uploadResult') }}</p>
    <div class="cmdb-batch-upload-result-content">
      <h4>
        {{ $t('cmdb.batch.total') }}&nbsp;<span style="color: blue">{{ total }}</span>
        {{ $t('cmdb.batch.successItems') }} <span style="color: lightgreen">{{ success }}</span>
        {{ $t('cmdb.batch.failedItems') }} <span style="color: red">{{ errorNum }} </span>{{ $t('cmdb.batch.items') }}
      </h4>
      <div>
        <span>{{ $t('cmdb.batch.errorTips') }}: </span>
        <ol>
          <li :key="item + index" v-for="(item, index) in errorItems">{{ item }}</li>
        </ol>
      </div>
    </div>
  </div>
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
      this.visible = true
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
        this.$emit('uploadResultDone')
        this.$message.success(this.$t('cmdb.batch.requestSuccessTips'))
      }
    },
  },
}
</script>
<style lang="less" scoped>
@import '~@/style/static.less';

.cmdb-batch-upload-result {
  .cmdb-batch-upload-result-content {
    background-color: rgba(240, 245, 255, 0.35);
    border-radius: 5px;
    padding: 12px;
  }
}
</style>
