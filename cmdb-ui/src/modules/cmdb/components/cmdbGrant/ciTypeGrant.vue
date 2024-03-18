<template>
  <div class="ci-type-grant">
    <vxe-table
      ref="xTable"
      size="mini"
      stripe
      class="ops-stripe-table"
      :data="filterTableData"
      :max-height="`${tableHeight}px`"
      :row-style="(params) => getCurrentRowStyle(params, addedRids)"
    >
      <vxe-column field="name"></vxe-column>
      <vxe-column v-for="col in columns" :key="col" :field="col" :title="permMap[col]">
        <template #default="{row}">
          <ReadCheckbox
            v-if="['read'].includes(col.split('_')[0])"
            :value="row[col.split('_')[0]]"
            :valueKey="col"
            :rid="row.rid"
            @openReadGrantModal="() => openReadGrantModal(col, row)"
          />
          <a-checkbox v-else-if="col === 'grant'" :checked="row[col]" @click="clickGrant(col, row)"></a-checkbox>
          <a-checkbox @change="(e) => handleChange(e, col, row)" v-else v-model="row[col]"></a-checkbox>
        </template>
      </vxe-column>
      <template #empty>
        <div v-if="loading()" style="height: 200px; line-height: 200px;color:#2F54EB">
          <a-icon type="loading" /> {{ $t('loading') }}
        </div>
        <div v-else>
          <img :style="{ width: '100px' }" :src="require('@/assets/data_empty.png')" />
          <div>{{ $t('noData') }}</div>
        </div>
      </template>
    </vxe-table>
    <a-space>
      <span class="grant-button" @click="grantDepart">{{ $t('cmdb.components.grantUser') }}</span>
      <span class="grant-button" @click="grantRole">{{ $t('cmdb.components.grantRole') }}</span>
    </a-space>
  </div>
</template>

<script>
import _ from 'lodash'
import { permMap } from './constants.js'
import { grantCiType, revokeCiType } from '../../api/CIType'
import ReadCheckbox from './readCheckbox.vue'
import { getCurrentRowStyle } from './utils'

export default {
  name: 'CiTypeGrant',
  components: { ReadCheckbox },
  inject: ['loading', 'isModal'],
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
    tableData: {
      type: Array,
      default: () => [],
    },
    grantType: {
      type: String,
      default: 'ci_type',
    },
    addedRids: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    filterTableData() {
      const _tableData = this.tableData.filter((data) => {
        const _intersection = _.intersection(
          Object.keys(data),
          this.columns.map((col) => col.split('_')[0])
        )
        return _intersection && _intersection.length
      })
      return _.uniqBy(_tableData, (item) => item.rid)
    },
    columns() {
      if (this.grantType === 'ci_type') {
        return ['config', 'grant']
      }
      return ['read_attr', 'read_ci', 'create', 'update', 'delete']
    },
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
    async handleChange(e, col, row) {
      if (e.target.checked) {
        await grantCiType(this.CITypeId, row.rid, { perms: [col] }).catch(() => {
          this.$emit('getTableData')
        })
      } else {
        await revokeCiType(this.CITypeId, row.rid, { perms: [col] }).catch(() => {
          this.$emit('getTableData')
        })
      }
    },
    grantDepart() {
      this.$emit('grantDepart', this.grantType)
    },
    grantRole() {
      this.$emit('grantRole', this.grantType)
    },
    openReadGrantModal(col, row) {
      this.$emit('openReadGrantModal', col, row)
    },
    clickGrant(col, row, rowIndex) {
      if (!row[col]) {
        this.handleChange({ target: { checked: true } }, col, row)
        const _idx = this.tableData.findIndex((item) => item.rid === row.rid)
        this.$set(this.tableData, _idx, { ...this.tableData[_idx], grant: true })
      } else {
        const that = this
        this.$confirm({
          title: that.$t('warning'),
          content: that.$t('cmdb.components.confirmRevoke', { name: `${row.name}` }),
          onOk() {
            that.handleChange({ target: { checked: false } }, col, row)
            const _idx = that.tableData.findIndex((item) => item.rid === row.rid)
            that.$set(that.tableData, _idx, { ...that.tableData[_idx], grant: false })
          },
        })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.ci-type-grant {
  padding: 10px 0;
}
</style>
