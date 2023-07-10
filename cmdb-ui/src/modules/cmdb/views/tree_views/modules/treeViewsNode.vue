<template>
  <div
    :style="{
      width: '100%',
      display: 'inline-flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }"
    @click="clickNode"
  >
    <span :style="{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }">{{ this.title }}</span>
    <a-icon :style="{ fontSize: '10px', color: '#0C3CFF' }" v-if="childLength && !isLeaf" :type="switchIcon"></a-icon>
  </div>
</template>

<script>
export default {
  name: 'TreeViewsNode',
  props: {
    title: {
      type: String,
      default: '',
    },
    treeKey: {
      type: String,
      default: '',
    },
    levels: {
      type: Array,
      default: () => [],
    },
    isLeaf: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return {
      switchIcon: 'down',
    }
  },
  computed: {
    childLength() {
      const reg = /(?<=\()\S+(?=\))/g
      return Number(this.title.match(reg)[0])
    },
  },
  methods: {
    clickNode() {
      this.$emit('onNodeClick', this.treeKey)
      this.switchIcon = this.switchIcon === 'down' ? 'up' : 'down'
    },
  },
}
</script>

<style></style>
