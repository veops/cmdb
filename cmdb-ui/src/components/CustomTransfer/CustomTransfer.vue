<template>
  <a-transfer v-bind="$attrs" v-on="$listeners" :data-source="dataSource" :target-keys="targetKeys"> </a-transfer>
</template>

<script>
export default {
  name: 'CustomTransfer',
  props: {
    dataSource: {
      type: Array,
      default: () => [],
    },
    targetKeys: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    // 穿梭框双击实现
    leftToRight(leftList, dataSource, targetKeys, sourceImportantKey, targetImportantKey) {
      for (let i = 0; i < leftList.length; i++) {
        leftList[i].ondblclick = e => {
          dataSource.forEach(item => {
            if (item[`${sourceImportantKey}`] === e.toElement.innerText) {
              targetKeys.push(item[`${targetImportantKey}`])
            }
          })
        }
      }
    },
    rightToLeft(rightList, dataSource, targetKeys, sourceImportantKey, targetImportantKey) {
      for (let i = 0; i < rightList.length; i++) {
        rightList[i].ondblclick = e => {
          dataSource.forEach(item => {
            if (item[`${sourceImportantKey}`] === e.toElement.innerText) {
              const idx = targetKeys.findIndex(item1 => {
                return item1 === item[`${targetImportantKey}`]
              })
              targetKeys.splice(idx, 1)
            }
          })
        }
      }
    },
    // 必须传入importantKey，用来做键名比对，传错或不传会造成错误
    dbClick(sourceSelectedKeys, targetSelectedKeys, sourceImportantKey, targetImportantKey) {
      window.setTimeout(() => {
        const element = document.getElementsByClassName('ant-transfer-list-content')
        if (this.dataSource.length !== this.targetKeys.length) {
          const leftList = element[0].children
          const rightList = element[1] ? element[1].children : []
          this.leftToRight(leftList, this.dataSource, this.targetKeys, sourceImportantKey, targetImportantKey)
          this.rightToLeft(rightList, this.dataSource, this.targetKeys, sourceImportantKey, targetImportantKey)
        }
        if (this.targetKeys.length && this.targetKeys.length === this.dataSource.length) {
          const rightList = element[0].children
          this.rightToLeft(rightList, this.dataSource, this.targetKeys, sourceImportantKey, targetImportantKey)
        }
      }, 100)
    },
  },
}
</script>

<style></style>
