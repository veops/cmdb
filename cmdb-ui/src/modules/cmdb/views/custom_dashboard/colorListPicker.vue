<template>
  <a-select v-model="currenColor">
    <a-select-option v-for="i in list" :value="i" :key="i">
      <div>
        <span :style="{ backgroundColor: color }" class="color-box" v-for="color in i.split(',')" :key="color"></span>
      </div>
    </a-select-option>
  </a-select>
</template>

<script>
export default {
  name: 'ColorListPicker',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    value: {
      type: [String, Array],
      default: null,
    },
  },
  data() {
    return {
      list: [
        '#6592FD,#6EE3EB,#44C2FD,#5F59F7,#1A348F,#7D8FCF,#A6D1E5,#8E56DD',
        '#C1A9DC,#E2B5CD,#EE8EBC,#8483C3,#4D66BD,#213764,#D9B6E9,#DD88EB',
        '#6FC4DF,#9FE8CE,#16B4BE,#86E6FB,#1871A3,#E1BF8D,#ED8D8D,#DD88EB',
        '#F8B751,#FC9054,#FFE380,#DF963F,#AB5200,#EA9387,#FFBB7C,#D27467',
      ],
    }
  },
  computed: {
    currenColor: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('change', val)
        return val
      },
    },
  },
}
</script>

<style lang="less" scoped>
.color-box {
  display: inline-block;
  width: 40px;
  height: 10px;
}
</style>
