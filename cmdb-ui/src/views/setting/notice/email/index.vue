<template>
  <div class="ops-setting-notice-mail">
    <a-tabs :activeKey="activeKey" @change="changeTab" class="ops-tab">
      <!-- <a-tab-pane key="1" tab="接收服务器">
        <Receive />
      </a-tab-pane> -->
      <a-tab-pane key="2" :tab="$t('cs.notice.sendServer')">
        <Send />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import Receive from './receive.vue'
import Send from './send.vue'
export default {
  name: 'NoticeEmail',
  components: { Receive, Send },
  data() {
    return {
      activeKey: '2',
    }
  },
  methods: {
    changeTab(activeKey) {
      this.activeKey = activeKey
    },
  },
}
</script>

<style lang="less" scoped>
.ops-setting-notice-mail {
  padding: 20px;
  padding-top: 0;
  background-color: #fff;
  border-radius: @border-radius-box;
  overflow: auto;
  margin-bottom: -24px;
  height: calc(100vh - 64px);
}
</style>
