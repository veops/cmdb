<template>
  <a-modal width="800px" :visible="visible" @ok="handleOK" @cancel="handleCancel" :closable="false">
    <Discovery :isSelected="true" :style="{ maxHeight: '75vh', overflow: 'auto' }" />
    <template #footer>
      <a-space>
        <a-button @click="handleCancel">取消</a-button>
        <a-button type="primary" @click="handleOK">确认</a-button>
        <a-button type="primary" @click="addPlugin">新建plugin</a-button>
      </a-space>
    </template>
  </a-modal>
</template>

<script>
import _ from 'lodash'
import Discovery from '../discovery'
import { postCITypeDiscovery } from '../../api/discovery'
export default {
  name: 'ADModal',
  components: { Discovery },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      visible: false,
      selectedIds: [],
    }
  },
  provide() {
    return {
      setSelectedIds: this.setSelectedIds,
      selectedIds: () => {
        return this.selectedIds
      },
    }
  },
  inject: ['getCITypeDiscovery'],
  methods: {
    open() {
      this.visible = true
    },
    handleCancel() {
      this.selectedIds = []
      this.visible = false
    },
    async handleOK() {
      if (this.selectedIds && this.selectedIds.length) {
        const promises = this.selectedIds.map(({ id, type }) => {
          return postCITypeDiscovery(this.CITypeId, { adr_id: id, interval: type === 'agent' ? 300 : 3600 })
        })
        await Promise.all(promises)
          .then((res) => {
            this.getCITypeDiscovery(res[0].id)
            this.$message.success('添加成功')
          })
          .catch(() => {
            this.getCITypeDiscovery()
          })
          .finally(() => {
            this.handleCancel()
          })
      }
      this.handleCancel()
    },
    setSelectedIds(id, type) {
      const _selectedIds = _.cloneDeep(this.selectedIds)
      const _idx = _selectedIds.findIndex((item) => item.id === id)
      if (_idx > -1) {
        _selectedIds.splice(_idx, 1)
      } else {
        _selectedIds.push({ id, type })
      }
      this.selectedIds = _selectedIds
    },
    addPlugin() {
      this.handleCancel()
      this.$emit('addPlugin')
    },
  },
}
</script>

<style></style>
