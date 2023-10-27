<template>
  <div class="body-wrapper">
    <div class="body-header">
      <!-- <a-space>
        <span>Content Type</span>
        <a-select size="small" v-model="contentType" style="width: 200px" :showSearch="true">
          <a-select-option value="none">
            None
          </a-select-option>
          <a-select-opt-group v-for="item in segmentedContentTypes" :key="item.title" :label="item.title">
            <a-select-option v-for="ele in item.contentTypes" :key="ele" :value="ele">
              {{ ele }}
            </a-select-option>
          </a-select-opt-group>
        </a-select>
      </a-space> -->
    </div>
    <div style="margin-top:10px">
      <codemirror style="z-index: 9999" :options="cmOptions" v-model="jsonData"></codemirror>
      <!-- <a-empty
        v-else
        :image-style="{
          height: '60px',
        }"
      >
        <img slot="image" :src="require('@/assets/data_empty.png')" />
        <span slot="description"> 暂无请求体 </span>
      </a-empty> -->
    </div>
  </div>
</template>

<script>
import { codemirror } from 'vue-codemirror'
import 'codemirror/lib/codemirror.css'

require('codemirror/mode/python/python.js')

export default {
  name: 'Body',
  components: { codemirror },
  data() {
    const segmentedContentTypes = [
      {
        title: 'text',
        contentTypes: [
          'application/json',
          'application/ld+json',
          'application/hal+json',
          'application/vnd.api+json',
          'application/xml',
        ],
      },
      {
        title: 'structured',
        contentTypes: ['application/x-www-form-urlencoded', 'multipart/form-data'],
      },
      {
        title: 'others',
        contentTypes: ['text/html', 'text/plain'],
      },
    ]
    return {
      segmentedContentTypes,
      //   contentType: 'none',
      jsonData: '',
      cmOptions: {
        lineNumbers: true,
        mode: 'python',
        height: '200px',
        tabSize: 4,
        lineWrapping: true,
      },
    }
  },
}
</script>

<style lang="less" scoped></style>
<style lang="less">
.body-wrapper {
  div.jsoneditor-menu {
    display: none;
  }
  div.jsoneditor {
    border-color: #f3f4f6;
    .jsoneditor-outer {
      border-color: #f3f4f6;
    }
  }
}
</style>
