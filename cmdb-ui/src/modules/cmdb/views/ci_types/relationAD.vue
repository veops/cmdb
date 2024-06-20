<template>
  <div class="relation-ad" :style="{ height: `${windowHeight - 200}px` }">
    <div class="relation-ad-table-tip">
      <ops-icon class="relation-ad-table-tip-icon" type="cmdb-prompt" />
      <span class="relation-ad-table-tip-text">1. {{ $t('cmdb.ciType.relationADTip') }}</span>
      <span class="relation-ad-table-tip-text">2. {{ $t('cmdb.ciType.relationADTip2') }}</span>
      <span class="relation-ad-table-tip-text">3. {{ $t('cmdb.ciType.relationADTip3') }}</span>
    </div>
    <!-- <div class="relation-ad-tip">{{ $t('cmdb.ciType.relationADTip') }}</div> -->
    <div class="relation-ad-header">
      <div class="relation-ad-header-left">{{ $t('cmdb.ciType.relationADHeader1') }}</div>
      <div class="relation-ad-header-left">{{ $t('cmdb.ciType.relationADHeader2') }}</div>
    </div>
    <div class="relation-ad-main">
      <div class="relation-ad-item" v-for="item in relationList" :key="item.id">
        <treeselect
          class="custom-treeselect"
          :style="{ width: '230px', '--custom-height': '32px' }"
          v-model="item.ad_key"
          :multiple="false"
          :clearable="true"
          searchable
          :options="ciTypeADTAttributes"
          value-consists-of="LEAF_PRIORITY"
          :placeholder="$t('cmdb.ciType.relationADSelectAttr')"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: node.label,
              }
            }
          "
        >
          <div :title="node.label" slot="option-label" slot-scope="{ node }">
            <div>{{ node.label }}</div>
            <!-- <div :style="{ fontSize: '12px', color: '#cbcbcb', lineHeight: '12px' }">{{ node.raw.desc }}</div> -->
          </div>
        </treeselect>
        <div
          class="relation-ad-item-link"
        >
          <div class="relation-ad-item-link-left"></div>
          <div class="relation-ad-item-link-right"></div>
        </div>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '230px', marginRight: '10px', '--custom-height': '32px' }"
          v-model="item.peer_type_id"
          :multiple="false"
          :clearable="true"
          searchable
          :options="relationOptions"
          value-consists-of="LEAF_PRIORITY"
          :placeholder="$t('cmdb.ciType.relationADSelectCIType')"
          :disableBranchNodes="true"
          @select="changeType(item)"
          :normalizer="
            (node) => {
              return {
                id: node.value || $t('other'),
                label: node.alias || node.name || $t('other'),
                title: node.alias || node.name || $t('other'),
                children: node.ci_types,
              }
            }
          "
        >
          <div
            :title="node.label"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            {{ node.label }}
          </div>
        </treeselect>
        <treeselect
          class="custom-treeselect"
          :style="{ width: '230px', marginRight: '18px', '--custom-height': '32px' }"
          v-model="item.peer_attr_id"
          :multiple="false"
          :clearable="true"
          searchable
          :options="item.attributes"
          value-consists-of="LEAF_PRIORITY"
          :placeholder="$t('cmdb.ciType.relationADSelectModelAttr')"
          :normalizer="
            (node) => {
              return {
                id: node.value,
                label: node.alias || node.name,
                title: node.alias || node.name,
              }
            }
          "
        >
          <div
            :title="node.label"
            slot="option-label"
            slot-scope="{ node }"
            :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
          >
            {{ node.label }}
          </div>
        </treeselect>
        <div class="relation-ad-item-action">
          <a @click="copyRelation(item)">
            <a-icon type="copy" />
          </a>
          <a @click="deleteRelation(item)">
            <a-icon type="minus-circle" />
          </a>
          <a @click="addRelation">
            <a-icon type="plus-circle" />
          </a>
        </div>
      </div>
      <div class="relation-ad-footer">
        <a-button type="primary" @click="handleSave">{{ $t('save') }}</a-button>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid'
import Treeselect from '@riophae/vue-treeselect'
import {
  getCITypeAttributes,
  getCITypeRelations,
  postCITypeRelations
} from '../../api/discovery'
import {
  getCITypeChildren,
  getCITypeParent
} from '../../api/CITypeRelation.js'

export default {
  name: 'RelationAutoDiscovery',
  components: { Treeselect },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      relationList: [], // 关系自动发现数据
      ciTypeADTAttributes: [], // 自动发现 options
      adt_id: null,
      adrList: [],
      relationOptions: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  async mounted() {
    await this.getCITypeAttributes()
    await this.getCITypeRelationOptions()
    this.getCITypeRelations()
  },
  methods: {
    async getCITypeAttributes() {
      const res = await getCITypeAttributes(this.CITypeId)
      this.ciTypeADTAttributes = res.map((item) => {
        return {
          id: item,
          value: item,
          label: item
        }
      })
    },
    async getCITypeRelationOptions() {
      const childRes = await getCITypeChildren(this.CITypeId)
      const parentRes = await getCITypeParent(this.CITypeId)
      const options = [...childRes.children, ...parentRes.parents]

      options.forEach((item) => {
        item.value = item.id
        item.label = item.alias || item.name
        const attributes = item?.attributes?.filter((attr) => !attr.is_password && !attr.is_list && attr.value_type !== '6')
        attributes.forEach((attr) => {
          attr.value = attr.id
          attr.label = attr.alias || attr.name
        })
        item.attributes = attributes
      })
      this.relationOptions = options
    },
    async getCITypeRelations() {
      getCITypeRelations(this.CITypeId).then(async (res) => {
        if (res?.length) {
          // this.adt_id = _find.id
          const _relationList = []
          res.forEach((item) => {
            const attributes = this?.relationOptions?.find((option) => option?.value === item.peer_type_id)?.attributes || []
            _relationList.push({
              id: uuidv4(),
              ad_key: item.ad_key,
              peer_type_id: item.peer_type_id,
              peer_attr_id: item.peer_attr_id,
              attributes,
            })
          })
          this.relationList = _relationList.length
            ? _relationList
            : [
                {
                  id: uuidv4(),
                  ad_key: undefined,
                  peer_type_id: undefined,
                  peer_attr_id: undefined,
                  attributes: [],
                },
              ]
        } else {
          this.adt_id = null
          this.relationList = [
            {
              id: uuidv4(),
              ad_key: undefined,
              peer_type_id: undefined,
              peer_attr_id: undefined,
              attributes: [],
            },
          ]
        }
      })
    },
    changeType(item) {
      this.$nextTick(() => {
        const peer_type_id = item.peer_type_id
        const attributes = this?.relationOptions?.find((option) => option?.value === peer_type_id)?.attributes

        item.attributes = attributes
        item.peer_attr_id = undefined
      })
    },
    addRelation() {
      const _relationList = _.cloneDeep(this.relationList)
      _relationList.push({
        id: uuidv4(),
        ad_key: undefined,
        peer_type_id: undefined,
        peer_attr_id: undefined,
        attributes: [],
      })
      this.relationList = _relationList
    },
    copyRelation(item) {
      const _relationList = _.cloneDeep(this.relationList)
      _relationList.push({
        ...item,
        id: uuidv4()
      })
      this.relationList = _relationList
    },

    deleteRelation(item) {
      if (this.relationList.length <= 1) {
        this.$message.error(this.$t('cmdb.ciType.deleteRelationAdTip'))
        return
      }
      const _idx = this.relationList.findIndex(({ id }) => item.id === id)
      if (_idx > -1) {
        this.relationList.splice(_idx, 1)
      }
    },

    async handleSave() {
      const _relation = this.relationList.map(({ ad_key, peer_attr_id, peer_type_id }) => {
        return {
          ad_key,
          peer_attr_id,
          peer_type_id
        }
      })
      if (_relation.length) {
        await postCITypeRelations(this.CITypeId, { relations: _relation })
        this.$message.success(this.$t('saveSuccess'))
        this.getCITypeRelations()
      }
    },
  },
}
</script>

<style lang="less" scoped>
.relation-ad {
  overflow: auto;
  padding: 0 20px;

  &-tip {
    color: @text-color_4;
    font-size: 12px;
    font-weight: 400;
    line-height: 22px;
  }

  &-header {
    margin-top: 20px;
    display: flex;
    align-items: center;
    font-size: 14px;
    font-weight: 700;
    line-height: 22px;

    &-left {
      width: 230px;
      margin-right: 63px;
    }
  }

  &-main {
    display: inline-block;
  }

  .relation-ad-item {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-top: 10px;

    &-link {
      position: relative;
      height: 1px;
      width: 63px;
      background-color: @border-color-base;

      &-left {
        position: absolute;
        top: -6px;
        left: -6px;
        z-index: 10;
        width: 12px;
        height: 12px;
        background-color: @primary-color;
        border: solid 3px #E2E7FC;
        border-radius: 50%
      }

      &-right {
        position: absolute;
        z-index: 10;
        top: -5px;
        right: 0px;
        width: 2px;
        height: 10px;
        border-radius: 1px 0px 0px 1px;
        background-color: @primary-color;
      }
    }

    &-action {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  &-table-tip {
    display: inline-flex;
    align-items: center;
    padding: 3px 16px;
    color: @text-color_2;
    font-size: 14px;
    font-weight: 400;
    border: solid 1px @primary-color_8;
    background-color: @primary-color_5;
    border-radius: 2px;

    &-icon {
      font-size: 16px;
      color: @primary-color;
      margin-right: 8px;
    }

    &-text {
      &:not(:last-child) {
        padding-right: 10px;
        margin-right: 10px;
        border-right: solid 1px @primary-color_8;
      }
    }
  }

  &-footer {
    // width: 690px;
    text-align: right;
    margin: 10px 0;
  }
}
</style>
