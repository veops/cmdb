<template>
  <a-modal
    width="800px"
    :visible="visible"
    dialogClass="new-ci_type-attr-modal"
    :bodyStyle="{ overflow: 'auto', maxHeight: `600px` }"
    @cancel="
      () => {
        visible = false
      }
    "
    :destroyOnClose="true"
  >
    <template slot="footer">
      <a-button
        @click="
          () => {
            visible = false
          }
        "
      >取消</a-button
      >
      <a-button :loading="confirmLoading" @click="handleSubmit(false)" type="primary">继续添加</a-button>
      <a-button :loading="confirmLoading" type="primary" @click="handleSubmit">确定</a-button>
    </template>
    <a-tabs v-model="activeKey">
      <a-tab-pane key="1" tab="新建属性">
        <div :style="{ overflow: 'auto', maxHeight: '480px' }">
          <create-new-attribute ref="createNewAttribute" :hasFooter="false" @done="handleAddNewAttr" />
        </div>
      </a-tab-pane>
      <a-tab-pane key="2" tab="已有属性" force-render>
        <AttributesTransfer
          :dataSource="unLinkdAttrs"
          :targetKeys="targetKeys"
          @setTargetKeys="setTargetKeys"
          @changeSingleItem="changeSingleItem"
          :hasFooter="false"
          :isSortable="false"
          :isFixable="false"
        />
      </a-tab-pane>
    </a-tabs>
  </a-modal>
</template>

<script>
import _ from 'lodash'
import { searchAttributes, createCITypeAttributes, updateCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { updateCITypeGroupById, getCITypeGroupById } from '@/modules/cmdb/api/CIType'
import CreateNewAttribute from './ceateNewAttribute.vue'
import { valueTypeMap } from '../../utils/const'
import AttributesTransfer from '../../components/attributesTransfer'

export default {
  name: 'NewCiTypeAttrModal',
  components: { CreateNewAttribute, AttributesTransfer },
  props: {
    linkedIds: {
      type: Array,
      required: true,
    },
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      valueTypeMap,
      activeKey: '1',
      visible: false,
      attributes: [],
      totalAttributes: [],
      targetKeys: [],
      currentGroup: null,
      confirmLoading: false,
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    unLinkdAttrs() {
      return this.totalAttributes
        .filter((attr) => {
          return !this.linkedIds.includes(attr.id)
        })
        .map((attr) => {
          return { key: String(attr.id), title: attr.alias || attr.name, name: attr.name }
        })
    },
  },
  beforeMount() {
    this.loadTotalAttrs()
  },
  methods: {
    async handleSubmit(isCloseModal = true) {
      console.log(this.targetKeys)

      if (this.activeKey === '2') {
        if (this.targetKeys.length) {
          this.confirmLoading = true
          await this.handleLinkAttrToCiType({ attr_id: this.targetKeys.map((i) => Number(i)) })
          if (this.currentGroup) {
            await this.updateCurrentGroup()
            const { id, name, order, attributes } = this.currentGroup
            const attrIds = attributes.map((i) => i.id)
            this.targetKeys.forEach((key) => {
              attrIds.push(Number(key))
            })
            await updateCITypeGroupById(id, { name, order, attributes: [...new Set(attrIds)] })
          }
          this.confirmLoading = false
          this.handleClose(isCloseModal)
        }
      } else {
        try {
          this.$refs.createNewAttribute.handleSubmit(isCloseModal)
        } catch (e) {}
      }
    },
    handleEdit(group) {
      this.targetKeys = []
      this.visible = true
      this.currentGroup = group
      this.activeKey = '1'
      this.$nextTick(() => {
        this.$refs.createNewAttribute.checkCanDefineComputed()
      })
    },
    async loadTotalAttrs() {
      const res = await searchAttributes({ page_size: 9999 })
      this.totalAttributes = res.attributes
    },
    async handleAddNewAttr(newAttrId, { is_required, default_show }, isCloseModal = true) {
      this.confirmLoading = true
      await this.handleLinkAttrToCiType({ attr_id: [newAttrId] })
      await updateCITypeAttributesById(this.CITypeId, {
        attributes: [{ attr_id: newAttrId, is_required: is_required || false, default_show: default_show || false }],
      })
      if (this.currentGroup) {
        await this.updateCurrentGroup()
        const { id, name, order, attributes } = this.currentGroup
        const attrIds = attributes.map((i) => i.id)
        attrIds.push(newAttrId)
        await updateCITypeGroupById(id, { name, order, attributes: attrIds })
      }
      this.confirmLoading = false
      this.loadTotalAttrs()
      this.$nextTick(() => {
        this.handleClose(isCloseModal)
      })
    },
    async handleLinkAttrToCiType(data) {
      const res = await createCITypeAttributes(this.CITypeId, data)
      return res
    },
    handleClose(isCloseModal = true) {
      this.$emit('ok')
      this.$message.success('添加成功！')
      if (isCloseModal) {
        this.visible = false
      }
      this.confirmLoading = false
    },
    setTargetKeys(targetKeys) {
      this.targetKeys = targetKeys
    },
    changeSingleItem(item) {
      const idx = this.targetKeys.findIndex((key) => key === item.key)
      if (idx > -1) {
        this.targetKeys.splice(idx, 1)
      } else {
        this.targetKeys.push(item.key)
      }
    },
    async updateCurrentGroup() {
      await getCITypeGroupById(this.CITypeId).then((res) => {
        const _find = res.find((item) => item.id === this.currentGroup.id)
        if (_find) {
          this.currentGroup.attributes = _.cloneDeep(_find.attributes)
        }
      })
    },
  },
}
</script>

<style lang="less">
.new-ci_type-attr-modal {
  .ant-modal-header {
    border-bottom: none;
    padding-bottom: 0;
  }
}
</style>
