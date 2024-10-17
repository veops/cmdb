<template>
  <div class="instance-detail">
    <div
      class="instance-detail-hide"
      @click="hideDetail"
    >
      <a-icon class="instance-detail-hide-icon" type="right" />
    </div>

    <div class="instance-detail-null" v-if="!ci._id" >
      <img
        :src="require('@/modules/cmdb/assets/no_permission.png')"
        class="instance-detail-null-img"
      />
      <span class="instance-detail-null-text" >{{ $t('noData') }}</span>
    </div>
    <template v-else>
      <div
        class="instance-detail-header"
      >
        <div class="instance-detail-header-line-1"></div>
        <div class="instance-detail-header-line-2"></div>
        <div class="instance-detail-header-row">
          <CIIcon
            :icon="ciType.icon"
            :title="ciType.name || ''"
            :size="20"
          />
          <div class="instance-detail-header-title">
            {{ detailTitle }}
          </div>

          <ops-icon
            :type="favorId ? 'veops-collected' : 'veops-collect'"
            :style="{ color: favorId ? '#FAD337' : '#A5A9BC' }"
            class="instance-detail-header-collect"
            @click="clickCollect"
          />

          <a class="instance-detail-header-share" @click="shareCi">
            <a-icon type="share-alt" />
            {{ $t('cmdb.ci.share') }}
          </a>
        </div>
      </div>

      <div class="instance-detail-attr">
        <div
          v-for="(group) in attributeGroups"
          :key="group.id"
          class="instance-detail-attr-group"
        >
          <span class="instance-detail-attr-group-name">{{ group.name || $t('other') }}</span>

          <div class="instance-detail-attr-list">
            <div
              v-for="(attr) in group.attributes"
              :key="attr.id"
              class="instance-detail-attr-item"
            >
              <a-tooltip :title="attr.alias || attr.name || ''">
                <div class="instance-detail-attr-item-label">
                  <span class="instance-detail-attr-item-label-text">
                    {{ attr.alias || attr.name || '' }}
                  </span>
                  <span class="instance-detail-attr-item-label-colon">:</span>
                </div>
              </a-tooltip>

              <div class="instance-detail-attr-item-value">
                <AttrDisplay
                  :attr="attr"
                  :ci="ci"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import _ from 'lodash'
import { getCIById, searchCI } from '@/modules/cmdb/api/ci'
import { getCITypeGroupById, getCITypes, getCIType } from '@/modules/cmdb/api/CIType'

import AttrDisplay from './attrDisplay.vue'
import CIIcon from '@/modules/cmdb/components/ciIcon/index.vue'

export default {
  name: 'InstanceDetail',
  components: {
    AttrDisplay,
    CIIcon
  },
  props: {
    CIId: {
      type: [String, Number],
      default: -1
    },
    CITypeId: {
      type: [String, Number],
      default: -1
    },
    favorList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      ci: {},
      ciType: {},
      attributeGroups: [],
      isNullData: false,
    }
  },
  computed: {
    watchParams() {
      return {
        CIId: this.CIId,
        CITypeId: this.CITypeId
      }
    },
    detailTitle() {
      const attrName = this?.ciType?.show_name || this?.ciType?.unique_name || ''
      return attrName ? (this?.ci?.[attrName] || '') : ''
    },
    favorId() {
      const id = this.favorList.find((item) => item?.option?.CIId === this.CIId)?.id
      return id ?? null
    }
  },
  watch: {
    watchParams: {
      immediate: true,
      deep: true,
      handler(newVal) {
        if (newVal?.CIId !== -1 && newVal?.CITypeId !== -1) {
          this.initData()
        }
      }
    }
  },
  methods: {
    async initData() {
      const ci = await this.getCI()
      if (!ci) {
        this.isNullData = true
        return
      }
      await this.getCIType()
      await this.getAttributes()
    },

    async getCI() {
      const res = await getCIById(this.CIId)
      const ci = res.result?.[0] || {}
      this.ci = ci
      return ci
    },

    async getCIType() {
      const res = await getCIType(this.CITypeId)
      this.ciType = res?.ci_types?.[0] || {}
    },

    async getAttributes() {
      const res = await getCITypeGroupById(this.CITypeId, { need_other: 1 })
      this.attributeGroups = res
      this.handleReferenceAttr()
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
    },

    shareCi() {
      const text = `${document.location.host}/cmdb/cidetail/${this.CITypeId}/${this.CIId}`
      this.$copyText(text)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    },

    clickCollect() {
      if (this.favorId) {
        this.$emit('deleteCollect', this.favorId)
      } else {
        this.$emit('addCollect', {
          CIId: this.CIId,
          CITypeId: this.CITypeId,
          title: this.detailTitle,
          icon: this.ciType?.icon,
          CITypeTitle: this.ciType?.name || ''
        })
      }
    },

    hideDetail() {
      this.$emit('hideDetail')
    }
  }
}
</script>

<style lang="less" scoped>
.instance-detail {
  width: 100%;
  height: 100%;
  border-radius: 2px;
  border: 1px solid #E4E7ED;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
  position: relative;

  &-hide {
    position: absolute;
    left: 0;
    top: 50%;
    margin-top: -21px;
    border-radius: 0px 2px 2px 0px;
    background-color: #2f54eb;
    width: 13px;
    height: 43px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
    cursor: pointer;

    &-icon {
      color: #FFFFFF;
      font-size: 12px;
    }

    &:hover {
      background-color: #597ef7;
    }
  }

  &-null {
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    padding-top: 100px;

    &-img {
      width: 180px;
    }

    &-text {
      color: #86909C;
      margin-top: 20px;
    }
  }

  &-header {
    width: 100%;
    height: 75px;
    background-color: #EBF0F9;
    overflow: hidden;
    position: relative;
    display: flex;
    align-items: center;
    padding: 0 20px;
    flex-shrink: 0;

    &-line-1 {
      height: 44px;
      width: 300px;
      position: absolute;
      right: -20px;
      top: 0px;
      transform: rotate(40deg);
      background: rgba(248, 249, 253, 0.60);
    }

    &-line-2 {
      height: 44px;
      width: 300px;
      position: absolute;
      right: -110px;
      top: 0px;
      transform: rotate(40deg);
      background: rgba(248, 249, 253, 0.60);
    }

    &-row {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      position: relative;
      z-index: 2;
    }

    &-title {
      font-size: 16px;
      font-weight: 700;
      color: #1D2129;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      text-wrap: nowrap;
      margin-left: 9px;
    }

    &-collect {
      margin-left: 8px;
      margin-right: 8px;
    }

    &-share {
      margin-left: auto;
      flex-shrink: 0;
    }
  }

  &-attr {
    width: 100%;
    overflow-y: auto;
    height: 100%;
    padding: 20px;

    &-group {
      &:not(:first-child) {
        margin-top: 15px;
      }

      &-name {
        font-size: 14px;
        font-weight: 700;
        color: #1D2129;
      }
    }

    &-item {
      margin-top: 15px;
      display: flex;
      align-items: flex-start;

      &-label {
        font-size: 14px;
        font-weight: 400;
        color: #86909C;
        width: 25%;
        flex-shrink: 0;
        display: flex;
        align-items: center;

        &-text {
          overflow: hidden;
          text-overflow: ellipsis;
          text-wrap: nowrap;
        }

        &-colon {
          flex-shrink: 0;
        }
      }

      &-value {
        margin-left: 12px;
      }
    }
  }
}
</style>
