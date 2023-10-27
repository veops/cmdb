<template>
  <span>
    <ops-icon :type="getPropertyIcon(attr)" />
  </span>
</template>

<script>
export default {
  name: 'ValueTypeIcon',
  props: {
    attr: {
      type: Object,
      default: () => {},
    },
  },
  methods: {
    getPropertyIcon(attr) {
      switch (attr.value_type) {
        case '0':
          return 'icon-xianxing-shishu'
        case '1':
          return 'icon-xianxing-fudianshu'
        case '2':
          if (attr.is_password) {
            return 'icon-xianxing-password'
          }
          if (attr.is_link) {
            return 'icon-xianxing-link'
          }
          return 'icon-xianxing-wenben'
        case '3':
          return 'icon-xianxing-datetime'
        case '4':
          return 'icon-xianxing-date'
        case '5':
          return 'icon-xianxing-time'
        case '6':
          return 'icon-xianxing-json'
      }
    },
  },
}
</script>

<style></style>
