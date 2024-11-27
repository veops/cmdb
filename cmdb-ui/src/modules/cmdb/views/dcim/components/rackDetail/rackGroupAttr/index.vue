<template>
  <div class="rack-group-attr">
    <el-descriptions
      v-for="group in attributeGroups"
      class="rack-group-attr-desc"
      :title="group.name || $t('other')"
      :key="group.name"
      border
      :column="3"
    >
      <el-descriptions-item
        v-for="attr in group.attributes"
        :label="`${attr.alias || attr.name}`"
        :key="attr.name"
      >
        <ci-detail-attr-content
          :ci="ci"
          :attr="attr"
          :attributeGroups="attributeGroups"
          :showEdit="false"
        />
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<script>
import _ from 'lodash'
import { getCITypeGroupById, getCITypes } from '@/modules/cmdb/api/CIType'
import { searchCI } from '@/modules/cmdb/api/ci'

import { Descriptions, DescriptionsItem } from 'element-ui'
import CiDetailAttrContent from '@/modules/cmdb/views/ci/modules/ciDetailAttrContent.vue'

export default {
  name: 'RackGroupAttr',
  components: {
    ElDescriptions: Descriptions,
    ElDescriptionsItem: DescriptionsItem,
    CiDetailAttrContent
  },
  props: {
    ci: {
      type: Object,
      default: () => {}
    },
    rackCITYpeId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      attributeGroups: []
    }
  },
  mounted() {
    this.getAttributes()
  },
  methods: {
    getAttributes() {
      getCITypeGroupById(this.rackCITYpeId, { need_other: 1 })
        .then((res) => {
          this.attributeGroups = res

          this.handleReferenceAttr()
        })
        .catch((e) => {})
    },

    async handleReferenceAttr() {
      const map = {}
      this.attributeGroups.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id && this.ci[attr.name]) {
            const ids = Array.isArray(this.ci[attr.name]) ? this.ci[attr.name] : this.ci[attr.name] ? [this.ci[attr.name]] : []
            if (ids.length) {
              if (!map?.[attr.reference_type_id]) {
                map[attr.reference_type_id] = {}
              }
              ids.forEach((id) => {
                map[attr.reference_type_id][id] = {}
              })
            }
          }
        })
      })

      if (!Object.keys(map).length) {
        return
      }

      const ciTypesRes = await getCITypes({
        type_ids: Object.keys(map).join(',')
      })
      const showAttrNameMap = {}
      ciTypesRes.ci_types.forEach((ciType) => {
        showAttrNameMap[ciType.id] = ciType?.show_name || ciType?.unique_name || ''
      })

      const allRes = await Promise.all(
        Object.keys(map).map((key) => {
          return searchCI({
            q: `_type:${key},_id:(${Object.keys(map[key]).join(';')})`,
            count: 9999
          })
        })
      )

      const ciNameMap = {}
      allRes.forEach((res) => {
        res.result.forEach((item) => {
          ciNameMap[item._id] = item
        })
      })

      const newAttrGroups = _.cloneDeep(this.attributeGroups)

      newAttrGroups.forEach((group) => {
        group.attributes.forEach((attr) => {
          if (attr?.is_reference && attr?.reference_type_id) {
            attr.showAttrName = showAttrNameMap?.[attr?.reference_type_id] || ''

            const referenceShowAttrNameMap = {}
            const referenceCIIds = this.ci[attr.name];
            (Array.isArray(referenceCIIds) ? referenceCIIds : referenceCIIds ? [referenceCIIds] : []).forEach((id) => {
              referenceShowAttrNameMap[id] = ciNameMap?.[id]?.[attr.showAttrName] ?? id
            })
            attr.referenceShowAttrNameMap = referenceShowAttrNameMap
          }
        })
      })

      this.$set(this, 'attributeGroups', newAttrGroups)
    }
  }
}
</script>

<style lang="less" scoped>
.rack-group-attr {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;

  &-desc {
    margin-bottom: 25px;
  }
}
</style>
