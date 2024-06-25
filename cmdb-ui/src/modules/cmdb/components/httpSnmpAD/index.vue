<template>
  <div class="http-snmp-ad">
    <HttpADCategory
      v-if="!isEdit && isCloud"
      :categories="categories"
      :currentCate="currentCate"
      :tableData="tableData"
      :ruleType="ruleType"
      @clickCategory="setCurrentCate"
    />
    <template v-else>
      <a-select v-if="isCloud" :style="{ marginBottom: '10px', minWidth: '120px' }" v-model="currentCate">
        <a-select-option v-for="cate in categoriesSelect" :key="cate" :value="cate">{{ cate }}</a-select-option>
      </a-select>
      <AttrMapTable
        v-if="isEdit"
        ref="attrMapTable"
        :ruleType="ruleType"
        :tableData="tableData"
        :ciTypeAttributes="ciTypeAttributes"
        :uniqueKey="uniqueKey"
      />
      <ADPreviewTable
        v-else
        :tableData="tableData"
      />
    </template>
  </div>
</template>

<script>
import { getHttpCategories, getHttpAttributes, getSnmpAttributes } from '../../api/discovery'
import AttrMapTable from '@/modules/cmdb/components/attrMapTable/index.vue'
import ADPreviewTable from './adPreviewTable.vue'
import HttpADCategory from './httpADCategory.vue'

export default {
  name: 'HttpSnmpAD',
  components: {
    AttrMapTable,
    ADPreviewTable,
    HttpADCategory
  },
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
    uniqueKey: {
      type: String,
      default: '',
    }
  },
  data() {
    return {
      categories: [],
      categoriesSelect: [],
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
        VCenter: { name: 'vcenter' },
        KVM: { name: 'kvm' },
      }
    },
    isCloud() {
      return ['http', 'private_cloud'].includes(this.ruleType)
    }
  },
  watch: {
    currentCate: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          getHttpAttributes(this.ruleName, { resource: newVal }).then((res) => {
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
          if (['snmp', 'components'].includes(ruleType) && ruleName) {
            getSnmpAttributes(ruleType, ruleName).then((res) => {
              if (this.isEdit) {
                this.formatTableData(res)
              } else {
                this.tableData = res
              }
            })
          }

          if (this.isCloud && ruleName) {
            getHttpCategories(this.ruleName).then((res) => {
              this.categories = res
              const categoriesSelect = []
              res.forEach((category) => {
                if (category?.items?.length) {
                  categoriesSelect.push(...category.items)
                }
              })
              this.categoriesSelect = categoriesSelect
              if (this.isEdit && categoriesSelect?.length) {
                this.currentCate = categoriesSelect[0]
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
      const $table = this.$refs.attrMapTable
      const { fullData } = $table.getTableData()
      return fullData || []
    }
  },
}
</script>

<style>
.http-snmp-ad {
  height: 100%;
}
</style>
