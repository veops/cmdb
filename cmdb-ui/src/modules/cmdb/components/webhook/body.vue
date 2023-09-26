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
      <vue-json-editor v-model="jsonData" :showBtns="false" :mode="'text'" />
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
import vueJsonEditor from 'vue-json-editor'

export default {
  name: 'Body',
  components: { vueJsonEditor },
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
      jsonData: {},
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
  }
}
</style>
