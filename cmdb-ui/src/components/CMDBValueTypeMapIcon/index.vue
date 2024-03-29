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
          return 'duose-shishu'
        case '1':
          return 'duose-fudianshu'
        case '2':
          if (attr.is_password) {
            return 'duose-password'
          }
          if (attr.is_link) {
            return 'duose-link'
          }
          return 'duose-wenben'
        case '3':
          return 'duose-datetime'
        case '4':
          return 'duose-date'
        case '5':
          return 'duose-time'
        case '6':
          return 'duose-json'
        case '7':
          return 'duose-password'
        case '8':
          return 'duose-link'
      }
    },
  },
}
</script>

<style></style>
