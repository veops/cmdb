<template>
  <a-empty
    :image-style="{
      height: '200px',
    }"
    :style="{ paddingTop: '10%' }"
  >
    <img slot="image" :src="require('@/modules/cmdb/assets/itsm_uninstalled.png')" />
    <span slot="description"> {{ $t('cmdb.history.itsmUninstalled') }} </span>
    <a-button href="https://veops.cn/apply" target="_blank" type="primary">
      {{ $t('cmdb.history.applyItsm') }}
    </a-button>
  </a-empty>
</template>

<script>
export default {
  name: 'RelatedItsm',
}
</script>
