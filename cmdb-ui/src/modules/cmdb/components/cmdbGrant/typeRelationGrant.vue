<template>
  <div class="ci-relation-grant">
    <vxe-table size="mini" stripe class="ops-stripe-table" :data="tableData" :max-height="`${tableHeight}px`">
      <vxe-column field="name"></vxe-column>
      <vxe-column v-for="col in columns" :key="col" :field="col" :title="permMap[col]">
        <template #default="{row}">
          <a-checkbox @change="(e) => handleChange(e, col, row)" v-model="row[col]"></a-checkbox>
        </template>
      </vxe-column>
    </vxe-table>
    <a-space>
      <span class="grant-button" @click="grantDepart">授权用户/部门</span>
      <!-- <span class="grant-button" @click="grantRole">授权角色</span> -->
    </a-space>
  </div>
</template>

<script>
import { permMap } from './constants.js'
import { grantTypeRelation, revokeTypeRelation } from '../../api/CITypeRelation.js'
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
  },
  data() {
    return {
      permMap,
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
  },
  methods: {
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
