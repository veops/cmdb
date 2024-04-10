<template>
  <div class="ci-relation-grant">
    <vxe-table
      ref="xTable"
      size="mini"
      stripe
      class="ops-stripe-table"
      :data="tableData"
      :max-height="`${tableHeight}px`"
      :row-style="(params) => getCurrentRowStyle(params, addedRids)"
    >
      <vxe-column field="name"></vxe-column>
      <vxe-column v-for="col in columns" :key="col" :field="col" :title="permMap[col]">
        <template #default="{row}">
          <a-checkbox @change="(e) => handleChange(e, col, row)" v-model="row[col]"></a-checkbox>
        </template>
      </vxe-column>
    </vxe-table>
    <a-space>
      <span class="grant-button" @click="grantDepart">{{ $t('cmdb.components.grantUser') }}</span>
      <span class="grant-button" @click="grantRole">{{ $t('cmdb.components.grantRole') }}</span>
    </a-space>
  </div>
</template>

<script>
import { permMap } from './constants.js'
import { grantTypeRelation, revokeTypeRelation } from '../../api/CITypeRelation.js'
import { getCurrentRowStyle } from './utils'

export default {
  name: 'TypeRelationGrant',
  inject: ['loading', 'isModal'],
  props: {
    tableData: {
      type: Array,
      default: () => [],
    },
    grantType: {
      type: String,
      default: 'type_relation',
    },
    typeRelationIds: {
      type: Array,
      default: null,
    },
    addedRids: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      columns: ['create', 'grant', 'delete'],
    }
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    tableHeight() {
      if (this.isModal) {
        return (this.windowHeight - 104) / 2
      }
      return (this.windowHeight - 104) / 2 - 116
    },
    permMap() {
      return permMap()
    }
  },
  methods: {
    getCurrentRowStyle,
    grantDepart() {
      this.$emit('grantDepart', this.grantType)
    },
    grantRole() {
      this.$emit('grantRole', this.grantType)
    },
    handleChange(e, col, row) {
      const first = this.typeRelationIds[0]
      const second = this.typeRelationIds[1]
      if (e.target.checked) {
        grantTypeRelation(first, second, row.rid, { perms: [col] }).catch(() => {
          this.$emit('getTableData')
        })
      } else {
        revokeTypeRelation(first, second, row.rid, { perms: [col] }).catch(() => {
          this.$emit('getTableData')
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.ci-relation-grant {
  padding: 10px 0;
}
</style>
