<template>
  <div>
    <div class="ci-detail-header">{{ this.type.alias }}</div>
    <div class="ci-detail-page">
      <CiDetailTab ref="ciDetailTab" :typeId="typeId" />
    </div>
  </div>
</template>

<script>
import CiDetailTab from './modules/ciDetailTab.vue'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCIType } from '@/modules/cmdb/api/CIType'

export default {
  name: 'CiDetailPage',
  components: { CiDetailTab },
  data() {
    return {
      typeId: Number(this.$route.params.typeId),
      type: {},
      attrList: [],
      attributes: {},
    }
  },
  provide() {
    return {
      attrList: () => {
        return this.attrList
      },
      attributes: () => {
        return this.attributes
      },
    }
  },
  mounted() {
    const { ciId = undefined } = this.$route.params
    if (ciId) {
      this.$refs.ciDetailTab.create(Number(ciId))
    }
    getCIType(this.typeId).then((res) => {
      this.type = res.ci_types[0]
    })
    this.getAttributeList()
  },
  methods: {
    async getAttributeList() {
      await getCITypeAttributesById(this.typeId).then((res) => {
        this.attrList = res.attributes
        this.attributes = res
      })
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';

.ci-detail-header {
  border-left: 3px solid @primary-color;
  padding-left: 10px;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 10px;
}
.ci-detail-page {
  background-color: #fff;
  height: calc(100vh - 122px);
}
</style>
