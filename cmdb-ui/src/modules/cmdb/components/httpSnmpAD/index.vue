<template>
  <div>
    <a-select v-if="ruleType === 'http'" :style="{ marginBottom: '10px' }" v-model="currentCate">
      <a-select-option v-for="cate in categories" :key="cate" :value="cate">{{ cate }}</a-select-option>
    </a-select>
    <vxe-table
      size="mini"
      stripe
      class="ops-stripe-table"
      show-overflow
      keep-source
      ref="xTable"
      resizable
      :data="tableData"
      :edit-config="isEdit ? { trigger: 'click', mode: 'cell' } : {}"
    >
      <template v-if="isEdit">
        <vxe-colgroup :title="$t('cmdb.ciType.autoDiscovery')">
          <vxe-column field="name" :title="$t('name')" width="100"> </vxe-column>
          <vxe-column field="type" :title="$t('type')" width="80"> </vxe-column>
          <vxe-column field="example" :title="$t('cmdb.components.example')">
            <template #default="{row}">
              <span v-if="row.type === 'json'">{{ JSON.stringify(row.example) }}</span>
              <span v-else>{{ row.example }}</span>
            </template>
          </vxe-column>
          <vxe-column field="desc" :title="$t('desc')"> </vxe-column>
        </vxe-colgroup>
        <vxe-colgroup :title="$t('cmdb.ciType.attributes')">
          <vxe-column field="attr" :title="$t('name')" :edit-render="{}">
            <template #default="{row}">
              {{ row.attr }}
            </template>
            <template #edit="{ row }">
              <vxe-select
                filterable
                clearable
                v-model="row.attr"
                type="text"
                :options="ciTypeAttributes"
                transfer
              ></vxe-select>
            </template>
          </vxe-column>
        </vxe-colgroup>
      </template>
      <template v-else>
        <vxe-column field="name" :title="$t('name')" width="100"> </vxe-column>
        <vxe-column field="type" :title="$t('type')" width="80"> </vxe-column>
        <vxe-column field="example" :title="$t('cmdb.components.example')">
          <template #default="{row}">
            <span v-if="row.type === 'object'">{{ JSON.stringify(row.example) }}</span>
            <span v-else>{{ row.example }}</span>
          </template>
        </vxe-column>
        <vxe-column field="desc" :title="$t('desc')"> </vxe-column>
      </template>
    </vxe-table>
  </div>
</template>

<script>
import { getHttpCategories, getHttpAttributes, getSnmpAttributes } from '../../api/discovery'
export default {
  name: 'HttpSnmpAD',
  props: {
    ruleName: {
      type: String,
      default: '',
    },
    ruleType: {
      type: String,
      default: 'http',
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    ciTypeAttributes: {
      type: Array,
      default: () => [],
    },
    adCITypeList: {
      type: Array,
      default: () => {},
    },
    currentTab: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      categories: [],
      currentCate: '',
      tableData: [],
    }
  },
  computed: {
    watchParams() {
      const { ruleType, ruleName } = this
      return { ruleType, ruleName }
    },
    httpMap() {
      return {
        阿里云: { name: 'aliyun' },
        腾讯云: { name: 'tencentcloud' },
        华为云: { name: 'huaweicloud' },
        AWS: { name: 'aws' },
      }
    },
  },
  watch: {
    currentCate: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          getHttpAttributes(this.httpMap[`${this.ruleName}`].name, { category: newVal }).then((res) => {
            if (this.isEdit) {
              this.formatTableData(res)
            } else {
              this.tableData = res
            }
          })
        }
      },
    },
    watchParams: {
      immediate: true,
      handler(newVal) {
        this.currentCate = ''
        this.$nextTick(() => {
          const { ruleType, ruleName } = newVal
          if (ruleType === 'snmp' && ruleName) {
            getSnmpAttributes(ruleName).then((res) => {
              if (this.isEdit) {
                this.formatTableData(res)
              } else {
                this.tableData = res
              }
            })
          }
          if (ruleType === 'http' && ruleName) {
            getHttpCategories(this.httpMap[`${this.ruleName}`].name).then((res) => {
              this.categories = res
              if (res && res.length) {
                this.currentCate = res[0]
              }
            })
          }
        })
      },
    },
  },
  mounted() {},
  methods: {
    setCurrentCate(cate) {
      if (cate) {
        this.currentCate = cate
        JSON.stringify(this.currentCate)
      }
    },
    formatTableData(list) {
      const _findADT = this.adCITypeList.find((item) => Number(item.adr_id) === Number(this.currentTab))
      this.tableData = (list || []).map((item) => {
        if (_findADT.attributes) {
          return {
            ...item,
            attr: _findADT.attributes[`${item.name}`],
          }
        } else {
          const _find = this.ciTypeAttributes.find((ele) => ele.name === item.name)
          if (_find) {
            return {
              ...item,
              attr: _find.name,
            }
          }
          return item
        }
      })
    },
    getTableData() {
      const $table = this.$refs.xTable
      const { fullData } = $table.getTableData()
      return fullData || []
    },
  },
}
</script>

<style></style>
