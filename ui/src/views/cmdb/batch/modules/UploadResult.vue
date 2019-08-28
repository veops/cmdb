<template>
  <div>
    <h4>共&nbsp;<span style="color: blue">{{ total }}</span> 条,已完成 <span style="color: lightgreen">{{ complete }}</span> 条
      ,失败 <span style="color: red">{{ errorNum }} </span>条</h4>

    <a-progress :percent="mPercent"/>
    <div class="my-box">
      <span>错误信息：</span>
      <ol>
        <li :key="item" v-for="item in errorItems">{{ item }}</li>
      </ol>
    </div>
  </div>
</template>

<script>
import { uploadData } from '@/api/cmdb/batch'

export default {
  name: 'Result',
  props: {
    upLoadData: {
      required: true,
      type: Array
    },
    ciType: {
      required: true,
      type: Number
    },
    uniqueField: {
      required: true,
      type: String
    }
  },
  data: function () {
    return {
      total: 0,
      complete: 0,
      errorNum: 0,
      errorItems: []
    }
  },
  mounted: function () {
    document.getElementById('upload-button').disabled = true
    this.upload2Server()
  },
  computed: {
    mpercent () {
      return Math.round(this.complete / this.total * 10000) / 100
    },
    progressStatus () {
      if (this.complete === this.total) {
        return null
      } else {
        return 'active'
      }
    }
  },
  methods: {
    upload2Server () {
      this.total = this.$props.upLoadData.length - 1
      for (let i = 0; i < this.total; i++) {
        const item = {}
        let itemUniqueName = 'unknown'
        for (let j = 0; j < this.$props.upLoadData[0].length; j++) {
          item[this.$props.upLoadData[0][j]] = this.$props.upLoadData[i + 1][j]
          if (this.$props.upLoadData[0][j] === this.$props.uniqueField) {
            itemUniqueName = this.$props.upLoadData[i + 1][j] || 'unknown'
          }
        }
        uploadData(this.$props.ciType, item).then(res => {
          console.log(res)
        }).catch(err => {
          this.errorNum += 1
          console.log(err)
          this.errorItems.push(itemUniqueName + ': ' + (((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'))
        })
        this.complete += 1
      }
    }
  }
}

</script>
<style scoped>
  .my-box {
    margin-top: 20px;
    color: red;
    border: 1px red dashed;
    padding: 8px;
    border-radius:5px;
    height: 429px;
    overflow-y: auto;
  }
</style>
