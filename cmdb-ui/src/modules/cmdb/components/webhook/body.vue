<template>
  <div class="body-wrapper">
    <MonacoCodeEditor
      v-model="jsonData"
      language="json"
      :height="200"
      storageKey="cmdbWebhookBodyEditor"
    />
  </div>
</template>

<script>
import MonacoCodeEditor from '@/components/MonacoCodeEditor'

export default {
  name: 'Body',
  components: {
    MonacoCodeEditor
  },
  data() {
    return {
      jsonData: ''
    }
  }
}
</script>
