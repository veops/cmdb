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
      let valueType = attr.value_type

      if (valueType === '2') {
        if (attr.is_password) {
          valueType = '7'
        } else if (attr.is_link) {
          valueType = '8'
        } else if (!attr.is_index) {
          valueType = '9'
        }
      }

      if (
        valueType === '7' &&
        attr.is_bool
      ) {
        valueType = '10'
      }

      if (
        valueType === '0' &&
        attr.is_reference
      ) {
        valueType = '11'
      }

      switch (valueType) {
        case '0':
          return 'duose-shishu'
        case '1':
          return 'duose-fudianshu'
        case '2':
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
        case '9':
          return 'duose-changwenben1'
        case '10':
          return 'duose-boole'
        case '11':
          return 'duose-quote'
        default:
          return ''
      }
    },
  },
}
</script>

<style></style>
