<template>
  <CustomLayout :editable="false" />
</template>

<script>
import CustomLayout from '../custom_dashboard/customLayout.vue'
export default {
  name: 'Dashboard',
  components: { CustomLayout },
}
</script>

<style></style>
