<template>
  <div class="editable-cell">
    <div v-if="editable.x" class="editable-cell-input-wrapper">
      <a-input :value="value | joinList" @change="handleChange" @pressEnter="check" />
      <a-icon type="check" class="editable-cell-icon-check" @click="check" />
    </div>
    <div v-else class="editable-cell-text-wrapper">
      {{ value | joinList }}
      <a-icon type="edit" class="editable-cell-icon" @click="edit" />
    </div>
  </div>
</template>
<script>
export default {
  props: {
    // eslint-disable-next-line
    text: {
      required: true
    }
  },
  data () {
    return {
      value: this.text,
      editable: { x: false }
    }
  },
  methods: {
    handleChange (e) {
      const value = e.target.value
      this.value = value
    },
    check () {
      //   this.editable.x = false
      this.$emit('change', [this.value, this.editable])
    },
    edit () {
      this.editable.x = true
    }
  },
  filters: {
    jsonDump: function (v) {
      if (typeof v === 'object') {
        return JSON.stringify(v)
      } else {
        return v
      }
    },
    joinList: function (itemValue) {
      if (typeof itemValue === 'object' && itemValue) {
        try {
          if (typeof itemValue[0] !== 'object') {
            return itemValue.join(',')
          } else {
            return JSON.stringify(itemValue)
          }
        } catch (e) {
          return JSON.stringify(itemValue)
        }
      } else if (itemValue !== null && itemValue !== 'undefined' && itemValue !== undefined && itemValue !== 'null') {
        return itemValue + ''
      } else {
        return ''
      }
    }
  }
}
</script>

<style scoped>
.editable-cell {
  position: relative;
}

.editable-cell-icon,
.editable-cell-icon-check {
  position: absolute;
  right: 0;
  width: 15px;
  cursor: pointer;
}

.editable-cell-icon {
  display: none;
}

td:hover > .editable-cell .editable-cell-icon {
  display: inline-block;
}

.editable-cell-icon:hover,
.editable-cell-icon-check:hover {
  color: #108ee9;
}
</style>
