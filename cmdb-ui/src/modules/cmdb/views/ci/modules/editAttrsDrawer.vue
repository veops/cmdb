<template>
  <CustomDrawer
    :visible="visible"
    width="600"
    @close="
      () => {
        visible = false
      }
    "
    title="字段设置"
  >
    <CustomTransfer
      ref="customTransfer"
      :dataSource="attrList"
      :showSearch="true"
      :listStyle="{
        width: '230px',
        height: '500px',
      }"
      :titles="['未选属性', '已选属性']"
      :render="item => item.title"
      :targetKeys="selectedAttrList"
      @change="handleChange"
      @selectChange="selectChange"
    >
      <span slot="notFoundContent">没数据</span>
    </CustomTransfer>
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleSubmit" type="primary">确定</a-button>
    </div>
  </CustomDrawer>
</template>

<script>
import { subscribeCIType, getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { getCITypeAttributesByName } from '@/modules/cmdb/api/CITypeAttr'
export default {
  name: 'EditAttrsDrawer',
  data() {
    return {
      attrList: [],
      typeId: null,
      visible: false,
      selectedAttrList: [],
    }
  },
  methods: {
    open(typeId) {
      this.typeId = typeId
      this.getAttrs()
    },
    getAttrs() {
      getCITypeAttributesByName(this.typeId).then(res => {
        const attributes = res.attributes
        getSubscribeAttributes(this.typeId).then(_res => {
          const attrList = []
          const selectedAttrList = []
          const subAttributes = _res.attributes
          this.instanceSubscribed = _res.is_subscribed
          subAttributes.forEach(item => {
            selectedAttrList.push(item.id.toString())
          })

          attributes.forEach(item => {
            const data = {
              key: item.id.toString(),
              title: item.alias || item.name,
            }
            attrList.push(data)
          })

          this.attrList = attrList
          this.selectedAttrList = selectedAttrList
          this.visible = true
        })
      })
    },
    handleChange(targetKeys, direction, moveKeys) {
      this.selectedAttrList = targetKeys
    },
    handleSubmit() {
      if (this.selectedAttrList.length) {
        subscribeCIType(this.typeId, this.selectedAttrList).then(res => {
          this.$message.success('订阅成功！')
          this.visible = false
          this.$emit('refresh')
        })
      } else {
        this.$confirm({
          title: '警告',
          content: '必须至少选择一个字段',
        })
      }
    },
    selectChange(sourceSelectedKeys, targetSelectedKeys) {
      this.$refs.customTransfer.dbClick(sourceSelectedKeys, targetSelectedKeys, 'title', 'key')
    },
  },
}
</script>

<style></style>
