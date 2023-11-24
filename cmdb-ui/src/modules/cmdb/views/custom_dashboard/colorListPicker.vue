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
        '#5DADF2,#86DFB7,#5A6F96,#7BD5FF,#FFB980,#4D58D6,#D9B6E9,#8054FF',
        '#9BA1F9,#0F2BA8,#A2EBFE,#4982F6,#FEB09C,#6C78E8,#FFDDAB,#4D66BD',
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
