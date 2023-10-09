<template>
  <div :style="{ marginBottom: '-24px' }">
    <a-tabs :activeKey="activeKey" @change="changeTab" class="ops-tab" type="card">
      <!-- <a-tab-pane key="1" tab="接收服务器">
        <Receive />
      </a-tab-pane> -->
      <a-tab-pane key="2" tab="发送服务器">
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

<style></style>
