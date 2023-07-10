<template>
  <div class="cmdb-batch-upload-result" v-if="visible">
    <h3 class="cmdb-batch-upload-result-title">上传结果</h3>
    <div class="cmdb-batch-upload-result-content">
      <h4>
        共&nbsp;<span style="color: blue">{{ total }}</span> 条，已成功
        <span style="color: lightgreen">{{ success }}</span> 条，失败 <span style="color: red">{{ errorNum }} </span>条
      </h4>
      <div>
        <span>错误信息：</span>
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
  },
  data: function() {
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
  methods: {
    async sleep(n) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve()
        }, n || 5)
      })
    },
    async upload2Server() {
      this.visible = true
      this.success = 0
      this.errorNum = 0
      this.errorItems = []
      for (let i = 0; i < this.total; i++) {
        // await this.sleep(20)
        const item = this.upLoadData[i]
        await uploadData(this.ciType, item)
          .then((res) => {
            console.log(res)
            this.success += 1
          })
          .catch((err) => {
            this.errorNum += 1
            this.errorItems.push(((err.response || {}).data || {}).message || '请求出现错误，请稍后再试')
          })
          .finally(() => {
            this.complete += 1
          })
      }
    },
  },
}
</script>
<style lang="less" scoped>
@import '~@/style/static.less';

.cmdb-batch-upload-result {
  .cmdb-batch-upload-result-title {
    border-left: 4px solid #custom_colors[color_1];
    padding-left: 10px;
  }
  .cmdb-batch-upload-result-content {
    background-color: rgba(240, 245, 255, 0.35);
    border-radius: 5px;
    padding: 12px;
  }
}
</style>
