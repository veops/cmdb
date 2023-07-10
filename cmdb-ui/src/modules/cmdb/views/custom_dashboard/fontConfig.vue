<template>
  <a-space>
    <a-input
      v-model="color"
      size="small"
      style="width:100px;"
      type="color"
    ><a-icon
      slot="addonBefore"
      type="font-colors"
    /></a-input>
    <a-input size="small" v-model="fontSize">
      <a-icon slot="addonBefore" type="font-size" />
      <span slot="addonAfter">px</span>
    </a-input>
  </a-space>
</template>

<script>
export default {
  name: 'FontConfig',
  data() {
    return {
      color: '#2f2f2f',
      fontSize: 50,
    }
  },
  methods: {
    getConfig() {
      return {
        color: this.color || '#2f2f2f',
        fontSize: `${this.fontSize || 50}px`,
      }
    },
    setConfig(config = {}) {
      const { color = '#2f2f2f', fontSize = '50px' } = config
      this.color = color
      this.fontSize = fontSize.split('px')[0]
    },
  },
}
</script>

<style></style>
