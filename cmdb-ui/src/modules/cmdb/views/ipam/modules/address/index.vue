<template>
  <div
    ref="addressRef"
    class="address"
  >
    <div v-if="addressNullTip" class="address-null">
      <img class="address-null-img" :src="require(`@/modules/cmdb/assets/ipam_address_null.png`)"></img>
      <div class="address-null-tip">{{ $t('noData') }}</div>
      <div class="address-null-tip2">{{ $t(addressNullTip) }}</div>
    </div>

    <a-spin
      v-else
      :tip="loadTip"
      :spinning="loading"
    >
      <div class="address-header">
        <div class="address-header-left">
          <a-input-search
            v-model="searchValue"
            :placeholder="$t('placeholderSearch')"
            class="address-header-search"
          />

          <a-select
            class="address-header-filter"
            v-model="currentStatus"
          >
            <a-icon slot="suffixIcon" type="caret-down" />
            <a-select-option
              v-for="(item) in filterOption"
              :key="item.value"
              :value="item.value"
            >
              {{ $t(item.label) }}
            </a-select-option>
          </a-select>

          <a-select
            v-if="scopeSelectOption.length > 1"
            class="address-header-filter"
            v-model="currentSelectScope"
            showSearch
          >
            <a-icon slot="suffixIcon" type="caret-down" />
            <a-select-option
              v-for="(key) in scopeSelectOption"
              :key="key"
              :value="key"
            >
              {{ key }}
            </a-select-option>
          </a-select>

          <div v-if="selectedIPList.length" class="ops-list-batch-action">
            <span @click="clickBatchAssign">{{ $t('cmdb.ipam.batchAssign') }}</span>
            <a-divider type="vertical" />
            <span @click="clickBatchRecycle">{{ $t('cmdb.ipam.batchRecycle') }}</span>
            <a-divider type="vertical" />
            <span @click="handleExport">{{ $t('export') }}</span>
            <span>{{ $t('cmdb.ci.selectRows', { rows: selectedIPList.length }) }}</span>
          </div>

          <div
            v-if="currentLayout === 'grid'"
            class="address-header-status"
          >
            <div
              v-for="(item) in statusOption"
              :key="item.value"
              class="address-header-status-item"
            >
              <div
                class="address-header-status-dot"
                :style="{
                  backgroundColor: `${STATUS_COLOR[item.value]}22`
                }"
              >
                <div
                  class="address-header-status-dot-content"
                  :style="{
                    backgroundColor: STATUS_COLOR[item.value]
                  }"
                ></div>
              </div>
              <div
                class="address-header-status-text"
              >
                {{ $t(item.label) }}: {{ item.count }}
              </div>
            </div>
          </div>
        </div>

        <div class="address-header-right">
          <div class="address-header-layout">
            <div
              v-for="(item) in layoutList"
              :key="item.value"
              :class="['address-header-layout-item', currentLayout === item.value ?'address-header-layout-item-active' : '']"
              @click="handleChangeLayout(item.value)"
            >
              <ops-icon :type="item.icon" />
            </div>
          </div>
        </div>
      </div>

      <div class="address-main">
        <TableIP
          v-if="currentLayout === 'table'"
          ref="tableIPRef"
          :columns="columns"
          :allTableData="filterIPList"
          :referenceShowAttrNameMap="referenceShowAttrNameMap"
          :referenceCIIdMap="referenceCIIdMap"
          :columnWidth="columnWidth"
          :addressCITypeId="addressCITypeId"
          @openAssign="openAssign"
          @recycle="handleRecycle"
          @selectChange="handleTableSelectChange"
        />

        <GridIP
          v-if="currentLayout === 'grid'"
          :ipList="filterIPList"
          :columns="columns"
          :referenceShowAttrNameMap="referenceShowAttrNameMap"
          :referenceCIIdMap="referenceCIIdMap"
          @openAssign="openAssign"
          @recycle="handleRecycle"
        />
      </div>
    </a-spin>

    <AssignForm
      ref="assignFormRef"
      :attrList="attrList"
      @ok="getIPList"
      @batchAssign="batchAssign"
    />
  </div>
</template>

<script>
import moment from 'moment'
import _ from 'lodash'
import ExcelJS from 'exceljs'
import FileSaver from 'file-saver'
import { getIPAMAddress, getIPAMHosts, postIPAMAddress, getIPAMSubnetById } from '@/modules/cmdb/api/ipam.js'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { ADDRESS_STATUS, STATUS_COLOR, STATUS_OPTION, STATUS_LABEL } from './constants.js'
import { getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'
import { strLength } from '@/modules/cmdb/utils/helper.js'

import TableIP from './tableIP.vue'
import GridIP from './gridIP.vue'
import AssignForm from './assignForm.vue'

export default {
  name: 'Address',
  components: {
    TableIP,
    GridIP,
    AssignForm
  },
  props: {
    nodeData: {
      type: [Object, null],
      default: null
    },
    addressCIType: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      STATUS_COLOR,
      searchValue: '',
      ipList: {},
      currentSelectScope: '',
      columns: [],
      attrList: [],
      attributes: {},
      subnetData: {},
      referenceShowAttrNameMap: {},
      referenceCIIdMap: {},
      columnWidth: {},
      loading: false,
      selectedIPList: [],
      loadTip: this.$t('loading'),

      currentStatus: 'all',
      filterOption: [
        {
          value: 'all',
          label: 'cmdb.ipam.allStatus',
        },
        ...STATUS_OPTION,
      ],

      currentLayout: 'table',
      layoutList: [
        {
          value: 'table',
          icon: 'monitor-list_view'
        },
        {
          value: 'grid',
          icon: 'veops-map_view'
        }
      ],
    }
  },
  provide() {
    return {
      handleSearch: this.getIPList,
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      }
    }
  },
  computed: {
    addressNullTip() {
      if (
        this?.nodeData?.isSubnet &&
        this?.nodeData?.cidr &&
        this?.nodeData?.children?.length === 0
      ) {
        const cidrSplit = this.nodeData?.cidr?.split?.('/')
        const cidrNumber = cidrSplit[cidrSplit.length - 1]
        if (Number(cidrNumber) >= 16) {
          return ''
        } else {
          return 'cmdb.ipam.addressNullTip2'
        }
      }
      return 'cmdb.ipam.addressNullTip'
    },
    addressCITypeId() {
      return this.addressCIType?.id || null
    },
    filterIPList() {
      let ipList = this.ipList?.[this.currentSelectScope]

      if (!ipList?.length) {
        return []
      }

      if (this.searchValue) {
        ipList = ipList.filter((item) => item.ip.indexOf(this.searchValue) !== -1)
      }

      if (this.currentStatus !== 'all') {
        ipList = ipList.filter((item) => item._ip_status === this.currentStatus)
      }

      return ipList
    },
    scopeSelectOption() {
      if (typeof this.ipList === 'object') {
        return Object.keys(this.ipList)
      }

      return []
    },
    statusOption() {
      const ipList = this.ipList?.[this.currentSelectScope] || []
      const statusCount = {
        [ADDRESS_STATUS.OFFLINE_ASSIGNED]: 0,
        [ADDRESS_STATUS.OFFLINE_UNASSIGNED]: 0,
        [ADDRESS_STATUS.ONLINE_ASSIGNED]: 0,
        [ADDRESS_STATUS.ONLINE_UNASSIGNED]: 0,
      }
      ipList.forEach((item) => {
        if (item._ip_status) {
          statusCount[item._ip_status]++
        }
      })
      return STATUS_OPTION.map((option) => ({
        ...option,
        count: statusCount[option.value]
      }))
    }
  },
  watch: {
    nodeData: {
      deep: true,
      immediate: true,
      handler(node, oldNode) {
        if (
          node &&
          node?.isSubnet &&
          node?.cidr &&
          node?.children?.length === 0 &&
          node?.key !== oldNode?.key
        ) {
          const cidrSplit = node?.cidr?.split?.('/')
          const cidrNumber = cidrSplit[cidrSplit.length - 1]

          if (Number(cidrNumber) >= 16) {
            this.initData()
          }
        }
      }
    }
  },
  methods: {
    async initData() {
      this.loadTip = this.$t('loading')
      this.loading = true
      try {
        await this.getColumns()
        await this.handleReferenceShowAttrName()
        await this.getIPList(true)
        this.calcColumnWidth()
      } catch (error) {
        console.log('initData fail', error)
      }
      this.loading = false
    },

    async getColumns() {
      const getAttrRes = await getCITypeAttributesById(this.addressCITypeId)
      this.attributes = _.cloneDeep(getAttrRes)
      this.attrList = _.cloneDeep(getAttrRes.attributes)

      const attrList = getAttrRes.attributes

      const filterAttrList = _.remove(attrList, (item) => {
        return ['ip', 'subnet_mask', 'assign_status', 'is_used', '_updated_by', '_updated_at', 'ipam_address_id'].includes(item.name)
      })

      const columns = []
      ;['ip', 'subnet_mask'].forEach((key) => {
        const attr = filterAttrList.find((item) => item.name === key)
        if (attr) {
          columns.push({
            field: attr.name,
            title: attr.alias || attr.name || ''
          })
        }
      })

      columns.push({
        field: '_ip_status',
        title: this.$t('status')
      })

      attrList.map((attr) => {
        columns.push({
          field: attr.name,
          title: attr.alias || attr.name || '',
          ...attr
        })
      })
      this.columns = columns
    },

    async getIPList(isInit = false) {
      const hostsList = await getIPAMHosts({
        cidr: this.nodeData.cidr
      })

      const res = await getIPAMAddress({
        parent_id: this.nodeData.key
      })

      const subnetData = await getIPAMSubnetById(this.nodeData.key)
      this.subnetData = subnetData

      const addressMap = {}
      if (res?.result?.length) {
        res.result.forEach((item) => {
          addressMap[item.ip] = item
        })
      }

      const ipList = {}
      let currentSelectScope = ''

      hostsList.map((ip) => {
        let colData = {
          ip,
          _ip_status: ADDRESS_STATUS.OFFLINE_UNASSIGNED
        }
        if (addressMap[ip]) {
          const data = addressMap[ip]
          const assigned = data.assign_status === 0 || data.assign_status === 2

          if (data.is_used) {
            colData._ip_status = assigned ? ADDRESS_STATUS.ONLINE_ASSIGNED : ADDRESS_STATUS.ONLINE_UNASSIGNED
          } else if (assigned) {
            colData._ip_status = ADDRESS_STATUS.OFFLINE_ASSIGNED
          }

          colData = {
            ...colData,
            ...data
          }
        }

        const itemData = {
          ...colData,
          subnet_mask: colData?.subnet_mask ?? subnetData?.subnet_mask ?? undefined,
          gateway: colData?.gateway ?? subnetData?.gateway ?? undefined
        }

        const key = ip.split(/\.(?=[^.]*$)/)?.[0]
        if (ipList[key]) {
          ipList[key].push(itemData)
        } else {
          if (!currentSelectScope) {
            currentSelectScope = key
          }
          ipList[key] = [itemData]
        }
      })
      this.ipList = ipList
      if (isInit) {
        this.currentSelectScope = currentSelectScope
      }
      this.handleReferenceCIIdMap()
    },

    async handleReferenceShowAttrName() {
      const needRequiredCITypeIds = this.columns?.filter((col) => col?.is_reference && col?.reference_type_id).map((col) => col.reference_type_id) || []
      if (!needRequiredCITypeIds.length) {
        this.referenceShowAttrNameMap = {}
        return
      }

      const res = await getCITypes({
        type_ids: needRequiredCITypeIds.join(',')
      })

      const map = {}
      res.ci_types.forEach((ciType) => {
        map[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      this.referenceShowAttrNameMap = map
    },

    async handleReferenceCIIdMap() {
      const referenceTypeCol = this.columns.filter((col) => col?.is_reference && col?.reference_type_id) || []
      if (!this.ipList?.[this.currentSelectScope]?.length || !referenceTypeCol?.length) {
        this.referenceCIIdMap = {}
        return
      }

      const map = {}
      this.ipList[this.currentSelectScope].forEach((row) => {
        referenceTypeCol.forEach((col) => {
          const ids = Array.isArray(row[col.field]) ? row[col.field] : row[col.field] ? [row[col.field]] : []
          if (ids.length) {
            if (!map?.[col.reference_type_id]) {
              map[col.reference_type_id] = {}
            }
            ids.forEach((id) => {
              map[col.reference_type_id][id] = {}
            })
          }
        })
      })

      if (!Object.keys(map).length) {
        this.referenceCIIdMap = {}
        return
      }

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      allRes.forEach((res) => {
        res.result.forEach((item) => {
          if (map?.[item._type]?.[item._id]) {
            map[item._type][item._id] = item
          }
        })
      })

      this.referenceCIIdMap = map
    },

    calcColumnWidth() {
      const columnWidth = {}
      this.columns.forEach((col) => {
        columnWidth[col.field] = Math.min(Math.max(100, ...this.ipList[this.currentSelectScope].map(item => strLength(item[col.field]))), 350)
      })

      const wrapWidth = this.$refs.addressRef?.clientWidth
      const totalWidth = Object.values(columnWidth).reduce((acc, cur) => acc + cur, 0)

      if (totalWidth < wrapWidth) {
        this.columnWidth = {
          ip: 130
        }
      } else {
        this.columnWidth = {
          ...columnWidth,
          ip: 130
        }
      }
    },

    handleExport() {
      let tableData = []
      if (this.currentLayout === 'table') {
        tableData = this.$refs.tableIPRef.getCheckedTableData()
        this.selectedIPList = []
      } else {
        tableData = this.filterIPList
      }

      if (!tableData.length) {
        return
      }

      const wb = new ExcelJS.Workbook()
      const ws = wb.addWorksheet(this.tabActive)

      const columns = this.columns.map((col) => {
        return {
          header: col.title,
          key: col.field,
          width: 20
        }
      })
      ws.columns = columns

      tableData.forEach((data) => {
        const row = {}
        columns.forEach(({ key }) => {
          let value = data?.[key] ?? null
          if (key === '_ip_status') {
            const text = STATUS_LABEL?.[data?.[key]]
            value = text ? this.$t(text) : null
          }
          row[key] = value
        })
        ws.addRow(row)
      })

      wb.xlsx.writeBuffer().then((buffer) => {
        const fileName = `cmdb-${this.$t('cmdb.ipam.addressAssign')}-${moment().format('YYYYMMDDHHmmss')}.xlsx`
        const file = new Blob([buffer], {
          type: 'application/octet-stream',
        })
        FileSaver.saveAs(file, fileName)
      })
    },

    openAssign(data) {
      this.$refs.assignFormRef.open({
        nodeId: this?.nodeData?._id,
        ipData: _.cloneDeep(data)
      })
    },

    handleRecycle(ip) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.ipam.recycleTip'),
        onOk: () => {
          postIPAMAddress({
            ips: [ip],
            parent_id: this.nodeData._id,
            assign_status: 1
          }).then(() => {
            this.$message.success(this.$t('cmdb.ipam.recycleSuccess', { ip }))
            this.getIPList()
          })
        },
      })
    },

    handleChangeLayout(value) {
      if (this.currentLayout !== value) {
        if (value === 'grid') {
          this.selectedIPList = []
        }
        this.currentLayout = value
      }
    },

    handleTableSelectChange(ips) {
      this.selectedIPList = ips
    },

    clickBatchAssign() {
      this.$refs.assignFormRef.open({
        nodeId: this?.nodeData?._id,
        ipData: {
          subnet_mask: this?.subnetData?.subnet_mask ?? undefined,
          gateway: this?.subnetData?.gateway ?? undefined
        },
        ipList: this.selectedIPList
      })
    },

    async batchAssign({
      paramsList,
      ipList
    }) {
      let successNum = 0
      let errorNum = 0

      try {
        this.loading = true

        this.loadTip = this.$t('cmdb.ipam.batchAssignInProgress', {
          total: ipList.length,
          successNum: successNum,
          errorNum: errorNum,
        })

        await _.reduce(
          paramsList,
          (promiseChain, params) => {
            const ipCount = params?.ips?.length ?? 0

            return promiseChain.then(() => {
              return postIPAMAddress(params).then(() => {
                successNum += ipCount
              }).catch(() => {
                errorNum += ipCount
              }).finally(() => {
                this.loadTip = this.$t('cmdb.ipam.batchAssignInProgress', {
                  total: ipList.length,
                  successNum: successNum,
                  errorNum: errorNum,
                })
              })
            })
          },
          Promise.resolve()
        )

        if (this.$refs.tableIPRef) {
          this.$refs.tableIPRef.clearCheckbox()
          this.selectedIPList = []
        }
        this.$message.success(this.$t('cmdb.ipam.batchAssignCompleted'))
        this.loading = false
        this.getIPList()
      } catch (error) {
        console.log('error', error)
      }
    },

    clickBatchRecycle() {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.ipam.recycleTip'),
        onOk: () => {
          this.handleBatchRecycle()
        },
      })
    },

    async handleBatchRecycle() {
      let successNum = 0
      let errorNum = 0

      try {
        this.loading = true

        this.loadTip = this.$t('cmdb.ipam.batchRecycleInProgress', {
          total: this.selectedIPList.length,
          successNum: successNum,
          errorNum: errorNum,
        })

        const ipChunk = _.chunk(this.selectedIPList, 5)

        await _.reduce(
          ipChunk,
          (promiseChain, ips) => {
            const ipCount = ips.length
            console.log('ipCount', ipCount, successNum, errorNum)
            return promiseChain.then(() => {
              return postIPAMAddress({
                ips,
                parent_id: this.nodeData._id,
                assign_status: 1
              }).then(() => {
                successNum += ipCount
              }).catch(() => {
                errorNum += ipCount
              }).finally(() => {
                this.loadTip = this.$t('cmdb.ipam.batchRecycleInProgress', {
                  total: this.selectedIPList.length,
                  successNum: successNum,
                  errorNum: errorNum,
                })
              })
            })
          },
          Promise.resolve()
        )

        if (this.$refs.tableIPRef) {
          this.$refs.tableIPRef.clearCheckbox()
          this.selectedIPList = []
        }
        this.$message.success(this.$t('cmdb.ipam.batchRecycleCompleted'))
        this.loading = false
        this.getIPList()
      } catch (error) {
        console.log('error', error)
      }
    }
  }
}
</script>

<style lang="less" scoped>
.address {
  width: 100%;
  height: fit-content;

  &-header {
    width: 100%;
    display: flex;
    align-items: baseline;
    justify-content: space-between;

    &-left {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      row-gap: 12px
    }

    &-search {
      height: 32px;
      width: 246px;
      flex-shrink: 0;
      margin-right: 16px
    }

    &-filter {
      width: 150px;
      margin-right: 16px;
      flex-shrink: 0;
    }

    &-status {
      display: flex;
      align-items: center;
      flex-shrink: 0;
      column-gap: 20px;

      &-item {
        display: flex;
        align-items: center;
      }

      &-dot {
        width: 12px;
        height: 12px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;

        &-content {
          width: 6px;
          height: 6px;
          border-radius: 6px;
        }
      }

      &-text {
        margin-left: 4px;
        font-size: 14px;
        font-weight: 400;
        color: #4E5969;
      }
    }

    &-right {
      display: flex;
      align-items: center;
      flex-shrink: 0;
      column-gap: 24px;
    }

    &-layout {
      display: flex;
      align-items: center;
      height: 32px;
      border: solid 1px #E4E7ED;

      &-item {
        height: 100%;
        width: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        cursor: pointer;

        &:not(:last-child) {
          border-right: solid 1px #E4E7ED;
        }

        &-active {
          color: #2F54EB;
          background-color: #F0F5FF;
        }

        &:hover {
          color: #2F54EB;
        }
      }
    }
  }

  &-main {
    margin-top: 22px;
  }

  &-null {
    width: 100%;
    padding-top: 130px;
    text-align: center;

    &-img {
      height: 200px;
    }

    &-tip {
      font-size: 14px;
      font-weight: 400;
      color: #86909C;
    }

    &-tip2 {
      font-size: 14px;
      font-weight: 400;
      color: #2F54EB;
    }
  }
}
</style>
