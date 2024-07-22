<template>
  <a-modal
    :visible="visible"
    :title="title"
    :width="880"
    :bodyStyle="{ maxHeight: '60vh', overflowY: 'auto' }"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <PublicTable
      v-if="httpName === 'public'"
      ref="publicTable"
    />
    <VCenterTable
      v-else-if="httpName === 'vcenter'"
      ref="vcenterTable"
    />
  </a-modal>
</template>

<script>
import { getHTTPAccounts, postHTTPAccounts } from '@/modules/cmdb/api/discovery'
import { defaultConfig } from './constants.js'

import PublicTable from './publicTable.vue'
import VCenterTable from './vcenterTable.vue'

export default {
  name: 'AccountConfig',
  components: {
    PublicTable,
    VCenterTable
  },
  props: {},
  data() {
    return {
      visible: false,
      rule: {}
    }
  },
  computed: {
    title() {
      if (this?.rule?.option?.category === 'private_cloud') {
        return `${this.rule?.name || ''} ${this.$t('cmdb.ciType.account')}`
      }
      return this.$t('cmdb.ciType.cloudAccessKey')
    },
    httpName() {
      if (this?.rule?.option?.category === 'private_cloud') {
        return this?.rule?.option?.en || ''
      }
      return 'public'
    }
  },
  methods: {
    async open(rule) {
      if (!rule?.id) {
        return
      }
      this.rule = rule

      const res = await getHTTPAccounts({
        adr_id: rule.id
      })
      console.log('getHTTPAccounts res', res)

      this.visible = true
      this.$nextTick(() => {
        const data = res?.length ? this.handleAccountsData(res) : []
        switch (this.httpName) {
          case 'public':
            this.$refs.publicTable.setData(data)
            break
          case 'vcenter':
            this.$refs.vcenterTable.setData(data)
            break
          default:
            break
        }
      })
    },
    handleAccountsData(accounts) {
      const config = defaultConfig[this.httpName] || {}

      return accounts.map((item) => {
        return {
          id: item?.id,
          name: item?.name || '',
          ...config,
          ...(item?.config || {})
        }
      })
    },
    handleCancel() {
      this.visible = false
    },
    async handleOk() {
      let tableData = {}
      switch (this.httpName) {
        case 'public':
          tableData = this.$refs.publicTable.getData()
          break
        case 'vcenter':
          tableData = this.$refs.vcenterTable.getData()
          break
        default:
          break
      }
      if (tableData.isError) {
        return
      }
      const accounts = tableData.data.map((item) => {
        const { name, id, ...otherConfig } = item
        const newData = {
          name,
          config: otherConfig,
        }
        if (id) {
          newData.id = id
        }

        return newData
      })
      postHTTPAccounts({
        adr_id: this.rule.id,
        accounts,
      }).then(() => {
        this.$message.success(this.$t('updateSuccess'))
        this.handleCancel()
      })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
