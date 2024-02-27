<template>
  <CustomDrawer
    width="80%"
    placement="left"
    @close="
      () => {
        visible = false
      }
    "
    :visible="visible"
    :hasTitle="false"
    :hasFooter="false"
    :bodyStyle="{ padding: 0, height: '100vh' }"
    destroyOnClose
  >
    <CiDetailTab ref="ciDetailTab" :typeId="typeId" :treeViewsLevels="treeViewsLevels" />
  </CustomDrawer>
</template>

<script>
import CiDetailTab from './ciDetailTab.vue'
export default {
  name: 'CiDetailDrawer',
  components: { CiDetailTab },
  props: {
    typeId: {
      type: Number,
      required: false,
      default: null,
    },
    treeViewsLevels: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      visible: false,
    }
  },
  methods: {
    create(ciId, activeTabKey = 'tab_1', ciDetailRelationKey = '1') {
      this.visible = true
      this.$nextTick(() => {
        this.$refs.ciDetailTab.create(ciId, activeTabKey, ciDetailRelationKey)
      })
    },
  },
}
</script>
