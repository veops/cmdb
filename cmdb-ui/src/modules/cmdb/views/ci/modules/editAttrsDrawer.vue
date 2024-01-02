<template>
  <CustomDrawer
    :visible="visible"
    width="600"
    @close="
      () => {
        visible = false
      }
    "
    :title="$t('cmdb.ci.attributeSettings')"
  >
    <CustomTransfer
      ref="customTransfer"
      :dataSource="attrList"
      :showSearch="true"
      :listStyle="{
        width: '230px',
        height: '500px',
      }"
      :titles="[$t('cmdb.components.unselectAttributes'), $t('cmdb.components.selectAttributes')]"
      :render="item => item.title"
      :targetKeys="selectedAttrList"
      @change="handleChange"
      @selectChange="selectChange"
    >
      <span slot="notFoundContent">{{ $t('noData') }}</span>
    </CustomTransfer>
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleSubmit" type="primary">{{ $t('confirm') }}</a-button>
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
      const that = this
      if (this.selectedAttrList.length) {
        subscribeCIType(this.typeId, this.selectedAttrList).then(res => {
          this.$message.success(this.$t('cmdb.components.subSuccess'))
          this.visible = false
          this.$emit('refresh')
        })
      } else {
        this.$confirm({
          title: that.$t('warning'),
          content: that.$t('cmdb.ci.tips4'),
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
