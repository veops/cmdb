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
      <a-select v-if="isCloud" :style="{ marginBottom: '10px', minWidth: '200px' }" v-model="currentCate">
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
import _ from 'lodash'
import { getHttpCategories, getHttpAttributes, getSnmpAttributes, getHttpAttrMapping } from '../../api/discovery'
import { DISCOVERY_CATEGORY_TYPE } from '@/modules/cmdb/views/discovery/constants.js'
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
    },
    currentAdt: {
      type: Object,
      default: () => {},
    }
  },
  data() {
    return {
      categories: [],
      categoriesSelect: [],
      currentCate: '',
      tableData: [],
      httpAttrMap: {}
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
      return [DISCOVERY_CATEGORY_TYPE.HTTP, DISCOVERY_CATEGORY_TYPE.PRIVATE_CLOUD].includes(this.ruleType)
    }
  },
  watch: {
    currentCate: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.getHttpAttr(newVal)
        }
      },
    },
    watchParams: {
      immediate: true,
      handler(newVal) {
        this.currentCate = ''
        this.$nextTick(() => {
          const { ruleType, ruleName } = newVal
          if ([DISCOVERY_CATEGORY_TYPE.SNMP, DISCOVERY_CATEGORY_TYPE.COMPONENT].includes(ruleType) && ruleName) {
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
                this.currentCate = this?.currentAdt?.extra_option?.category || categoriesSelect[0]
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
      this.tableData = (list || []).map((val) => {
        const item = _.cloneDeep(val)

        if (_findADT?.attributes?.[item.name]) {
          item.attr = _findADT.attributes[item.name]
        }

        const attrMapName = this.httpAttrMap?.[item?.name]

        if (
          this.isEdit &&
          !item.attr &&
          attrMapName &&
          this.ciTypeAttributes.some((ele) => ele.name === attrMapName)
        ) {
          item.attr = attrMapName
        }

        if (!item.attr) {
          const _find = this.ciTypeAttributes.find((ele) => ele.name === item.name)
          if (_find) {
            item.attr = _find.name
          }
        }

        return item
      })
    },
    getTableData() {
      const $table = this.$refs.attrMapTable
      const { fullData } = $table.getTableData()
      return fullData || []
    },

    async getHttpAttr(val) {
      await this.getHttpAttrMapping(this.ruleName, val)
      getHttpAttributes(this.ruleName, { resource: val }).then((res) => {
        if (this.isEdit) {
          this.formatTableData(res)
        } else {
          this.tableData = res
        }
      })
    },

    async getHttpAttrMapping(name, resource) {
      const res = await getHttpAttrMapping(name, resource)
      this.httpAttrMap = res || {}
    }
  },
}
</script>

<style>
.http-snmp-ad {
  height: 100%;
}
</style>
