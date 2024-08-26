<template>
  <CustomDrawer
    :title="$t('cmdb.ciType.viewAllAttr')"
    :visible="visible"
    placement="right"
    width="800"
    :bodyStyle="{ height: '100vh' }"
    @close="handleClose"
  >
    <vxe-table
      resizable
      size="mini"
      :span-method="mergeRowMethod"
      :data="tableData"
      show-overflow
      show-header-overflow
      border
      class="ops-stripe-table"
      :height="windowHeight - 160"
    >
      <vxe-table-column align="center" field="groupId" :title="$t('cmdb.ciType.attrGroup')" :width="100">
        <template #default="{row}">
          <span>{{ row.groupName }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="name" :title="$t('cmdb.ciType.attrName')" :width="150"></vxe-table-column>
      <vxe-table-column field="alias" :title="$t('cmdb.ciType.attrAlias')" :width="150"></vxe-table-column>
      <vxe-table-column field="typeText" :title="$t('type')" :width="100"></vxe-table-column>
      <vxe-table-column field="code" :title="$t('cmdb.ciType.attrCode')">
        <template #default="{row}">
          <a @click="copyText(row.code)" >{{ row.code }}</a>
        </template>
      </vxe-table-column>
    </vxe-table>
  </CustomDrawer>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'
import { valueTypeMap } from '@/modules/cmdb/utils/const'
import { getPropertyType } from '@/modules/cmdb/utils/helper'

export default {
  name: 'AllAttrDrawer',
  data() {
    return {
      visible: false,
      tableData: [],
    }
  },
  inject: {
    providerGroupsData: {
      default: () => {
        return () => {
          return {
            CITypeGroups: [],
            otherGroupAttributes: [],
          }
        }
      }
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  methods: {
    async open() {
      this.visible = true
      const tableData = []
      const typeMap = valueTypeMap()
      const providerGroupsData = _.cloneDeep(this.providerGroupsData() || {})
      const groupsData = providerGroupsData?.CITypeGroups || []
      const otherAttrData = providerGroupsData?.otherGroupAttributes || []

      groupsData.forEach((group) => {
        if (group?.attributes?.length) {
          const attrArr = group.attributes.map((attr) => {
            if (attr.is_password) {
              attr.value_type = '7'
            }
            if (attr.is_link) {
              attr.value_type = '8'
            }
            attr.groupId = group.id
            attr.groupName = group.name
            attr.code = ['0', '1', '6'].includes(attr.value_type) ? `{{ ${attr.name} }}` : `'''{{ ${attr.name} }}'''`
            attr.typeText = typeMap?.[attr.value_type] ?? ''

            return attr
          })
          tableData.push(...attrArr)
        }
      })

      otherAttrData.forEach((attr) => {
        attr.value_type = getPropertyType(attr)

        attr.groupId = -1
        attr.groupName = this.$t('other')
        attr.code = `{{ ${attr.name} }}`
        attr.typeText = typeMap?.[attr.value_type] ?? ''
      })
      tableData.push(...otherAttrData)

      this.tableData = tableData
    },

    mergeRowMethod({ row, _rowIndex, column, visibleData }) {
      const fields = ['groupId']
      const currentValue = row.groupId

      if (currentValue && fields.includes(column.property)) {
        const prevRow = visibleData[_rowIndex - 1]
        let nextRow = visibleData[_rowIndex + 1]
        if (prevRow && prevRow.groupId === currentValue) {
          return { rowspan: 0, colspan: 0 }
        } else {
          let countRowspan = 1
          while (nextRow && nextRow.groupId === currentValue) {
            nextRow = visibleData[++countRowspan + _rowIndex]
          }
          if (countRowspan > 1) {
            return { rowspan: countRowspan, colspan: 1 }
          }
        }
      }
    },

    handleClose() {
      this.visible = false
    },

    copyText(text) {
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
