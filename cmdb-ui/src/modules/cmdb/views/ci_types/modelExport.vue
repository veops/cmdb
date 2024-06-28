<template>
  <a-modal
    :visible="visible"
    :title="$t('cmdb.ciType.modelExport')"
    :width="560"
    @cancel="handleCancel"
    @ok="handleOK"
  >
    <a-form
      :form="form"
      :labelCol="{ span: 5 }"
      :wrapperCol="{ span: 19 }"
    >
      <a-form-item
        :label="$t('cmdb.ciType.filename')"
      >
        <a-input v-decorator="['name', { rules: [{ required: true, message: $t('cmdb.ciType.filenameInputTips') }], initialValue: 'cmdb_template' }]" />
      </a-form-item>
      <a-form-item
        :label="$t('cmdb.ciType.selectModel')"
      >
        <a-transfer
          class="model-export-transfer"
          :dataSource="transferDataSource"
          :targetKeys="targetKeys"
          :render="item => item.title"
          :titles="[$t('cmdb.ciType.unselectModel'), $t('cmdb.ciType.selectedModel')]"
          :listStyle="{
            width: '180px',
            height: `262px`,
          }"
          @change="onChange"
        >
          <template
            slot="children"
            slot-scope="{ props: { direction, selectedKeys }, on: { itemSelect, itemSelectAll } }"
          >
            <a-tree
              v-if="direction === 'left'"
              blockNode
              checkable
              :checkedKeys="[...selectedKeys, ...targetKeys]"
              :treeData="treeData"
              :checkStrictly="false"
              @check="
                (_, props) => {
                  onChecked(_, props, [...selectedKeys, ...targetKeys], itemSelect, itemSelectAll);
                }
              "
              @select="
                (_, props) => {
                  onChecked(_, props, [...selectedKeys, ...targetKeys], itemSelect, itemSelectAll);
                }
              "
            />
          </template>
        </a-transfer>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import _ from 'lodash'
import { exportCITypeGroups } from '@/modules/cmdb/api/ciTypeGroup'

export default {
  name: 'ModelExport',
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    CITypeGroups: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      form: this.$form.createForm(this, { name: 'model-export' }),
      targetKeys: [],
      btnLoading: false,
    }
  },
  computed: {
    transferDataSource() {
      const dataSource = this.CITypeGroups.reduce((acc, item) => {
        const types = _.cloneDeep(item?.ci_types || [])
        types.forEach((item) => {
          item.key = String(item.id)
          item.title = item?.alias || item?.name || this.$t('other')
        })
        return acc.concat(types)
      }, [])
      return dataSource
    },
    treeData() {
      const treeData = _.cloneDeep(this.CITypeGroups)
      let newTreeData = treeData.map((item) => {
        const childrenKeys = []
        const children = (item.ci_types || []).map((child) => {
          const key = String(child?.id)
          const disabled = this.targetKeys.includes(key)
          childrenKeys.push(key)

          return {
            key,
            title: child?.alias || child?.name || this.$t('other'),
            disabled,
            children: []
          }
        })
        return {
          key: String(item?.id),
          title: item?.name || this.$t('other'),
          children,
          childrenKeys,
          disabled: children.every((item) => item.disabled),
        }
      })
      console.log('treeData', newTreeData)
      newTreeData = newTreeData.filter((item) => item.children.length > 0)

      return newTreeData
    }
  },
  methods: {
    onChange(targetKeys, direction, moveKeys) {
      const childKeys = []
      const newTargetKeys = [...targetKeys]

      if (direction === 'right') {
        // 如果是选中父节点，添加时去除父节点，添加其子节点
        this.treeData.forEach((item) => {
          const parentIndex = newTargetKeys.findIndex((key) => item.key === key)
          if (parentIndex !== -1) {
            newTargetKeys.splice(parentIndex, 1)
            childKeys.push(...item.childrenKeys)
          }
        })
      }

      const uniqTargetKeys = _.uniq([...newTargetKeys, ...childKeys])
      this.targetKeys = uniqTargetKeys
    },
    onChecked(_, e, checkedKeys, itemSelect, itemSelectAll) {
      const { eventKey } = e.node
      const selected = checkedKeys.indexOf(eventKey) === -1
      const childrenKeys = this.treeData.find((item) => item.key === eventKey)?.childrenKeys || []

      // 如果当前点击是子节点，处理其联动父节点
      this.treeData.forEach((item) => {
        if (item.childrenKeys.includes(eventKey)) {
          if (selected && item.childrenKeys.every((childKey) => [eventKey, ...checkedKeys].includes(childKey))) {
            itemSelect(item.key, true)
          } else if (!selected) {
            itemSelect(item.key, false)
          }
        }
      })

      itemSelectAll([eventKey, ...childrenKeys], selected)
    },
    handleCancel() {
      this.$emit('cancel')
      this.form.resetFields()
      this.targetKeys = []
    },
    handleOK() {
      this.form.validateFields(async (err, values) => {
        if (err || !this.targetKeys.length || this.btnLoading) {
          return
        }
        this.btnLoading = true
        const hide = this.$message.loading(this.$t('loading'), 0)

        try {
          const typeIds = this.targetKeys.join(',')
          const res = await exportCITypeGroups({
            type_ids: typeIds
          })
          console.log('exportCITypeGroups res', res)

          if (res) {
            const jsonStr = JSON.stringify(res)
            const blob = new Blob([jsonStr], { type: 'application/json' })

            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url

            const fileName = values.name
            a.download = fileName

            a.click()
            URL.revokeObjectURL(url)
          }
        } catch (error) {
          console.log('exportCITypeGroups fail', error)
          hide()
          this.btnLoading = false
        }
        hide()
        this.btnLoading = false
      })
    }
  }
}
</script>

<style lang="less" scoped>
.model-export-transfer {
  /deep/ .ant-transfer-list {
    .ant-transfer-list-body {
      overflow: auto;
    }

    &:first-child {
      .ant-transfer-list-header {
        .ant-transfer-list-header-selected {
          span:first-child {
            display: none;
          }
        }
      }
    }

    .ant-transfer-list-header-title {
      color: @primary-color;
      font-weight: 400;
      font-size: 12px;
    }
  }
}
</style>
