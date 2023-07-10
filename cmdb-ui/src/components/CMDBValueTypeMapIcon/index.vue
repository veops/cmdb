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
    getPropertyStyle(attr) {
      switch (attr.value_type) {
        case '0':
          return { color: '#cf1322', backgroundColor: '#fff1f0' }
        case '1':
          return { color: '#d4b106', backgroundColor: '#feffe6' }
        case '2':
          return { color: '#d46b08', backgroundColor: '#fff7e6' }
        case '3':
          return { color: '#531dab', backgroundColor: '#f9f0ff' }
        case '4':
          return { color: '#389e0d', backgroundColor: '#f6ffed' }
        case '5':
          return { color: '#08979c', backgroundColor: '#e6fffb' }
        case '6':
          return { color: '#c41d7f', backgroundColor: '#fff0f6' }
      }
    },
    getPropertyIcon(attr) {
      switch (attr.value_type) {
        case '0':
          return 'icon-xianxing-shishu'
        case '1':
          return 'icon-xianxing-fudianshu'
        case '2':
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
