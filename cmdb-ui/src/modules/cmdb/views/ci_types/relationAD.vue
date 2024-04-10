<template>
  <div class="relation-ad" :style="{ height: `${windowHeight - 130}px` }">
    <div class="relation-ad-item" v-for="item in relationList" :key="item.id">
      <treeselect
        class="custom-treeselect"
        :style="{ width: '200px', marginRight: '10px', '--custom-height': '32px' }"
        v-model="item.attrName"
        :multiple="false"
        :clearable="true"
        searchable
        :options="ciTypeADTAttributes"
        value-consists-of="LEAF_PRIORITY"
        :placeholder="$t('cmdb.ciType.selectAttributes')"
        :normalizer="
          (node) => {
            return {
              id: node.name,
              label: node.name,
            }
          }
        "
      >
        <div :title="node.label" slot="option-label" slot-scope="{ node }">
          <div>{{ node.label }}</div>
          <div :style="{ fontSize: '12px', color: '#cbcbcb', lineHeight: '12px' }">{{ node.raw.desc }}</div>
        </div>
      </treeselect>
      <a><a-icon type="swap"/></a>
      <treeselect
        class="custom-treeselect"
        :style="{ width: '200px', margin: '0 10px', '--custom-height': '32px' }"
        v-model="item.type_name"
        :multiple="false"
        :clearable="true"
        searchable
        :options="ciTypeGroup"
        value-consists-of="LEAF_PRIORITY"
        :placeholder="$t('cmdb.ciType.selectCIType')"
        :disableBranchNodes="true"
        @select="changeType(item)"
        :normalizer="
          (node) => {
            return {
              id: node.name || $t('other'),
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
        :style="{ width: '200px', marginRight: '10px', '--custom-height': '32px' }"
        v-model="item.attr_name"
        :multiple="false"
        :clearable="true"
        searchable
        :options="item.attributes"
        value-consists-of="LEAF_PRIORITY"
        :placeholder="$t('cmdb.ciType.selectAttributes')"
        :normalizer="
          (node) => {
            return {
              id: node.name,
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
    </div>
    <div class="relation-ad-footer">
      <a-button type="primary" @click="handleSave">{{ $t('save') }}</a-button>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import { v4 as uuidv4 } from 'uuid'
import Treeselect from '@riophae/vue-treeselect'
import { getCITypeAttributesById } from '../../api/CITypeAttr'
import { getCITypeGroups } from '../../api/ciTypeGroup'
import { getDiscovery, getCITypeDiscovery, postCITypeDiscovery, putCITypeDiscovery } from '../../api/discovery'

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
      relationList: [],
      ciTypeADTAttributes: [],
      ciTypeGroup: [],
      adt_id: null,
      adrList: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  created() {
    getCITypeGroups({ need_other: true }).then((res) => {
      this.ciTypeGroup = res
        .filter((item) => item.ci_types && item.ci_types.length)
        .map((item) => {
          item.id = `parent_${item.id || -1}`
          return { ..._.cloneDeep(item) }
        })
    })
  },
  async mounted() {
    await this.getDiscovery()
    this.getCITypeDiscovery()
  },
  methods: {
    async getDiscovery() {
      await getDiscovery().then((res) => {
        this.adrList = res
      })
    },
    getCITypeDiscovery() {
      getCITypeDiscovery(this.CITypeId).then(async (res) => {
        // Options for the first drop-down box
        const _ciTypeADTAttributes = []
        res
          .filter((adt) => adt.adr_id)
          .forEach((adt) => {
            const _find = this.adrList.find((adr) => adr.id === adt.adr_id)
            if (_find && _find.attributes) {
              _ciTypeADTAttributes.push(..._find.attributes)
            }
          })
        console.log(_ciTypeADTAttributes)
        this.ciTypeADTAttributes = _.uniqBy(_ciTypeADTAttributes, 'name')
        // Options for the first drop-down box
        const _find = res.find((adt) => !adt.adr_id)
        if (_find) {
          this.adt_id = _find.id
          const _relationList = []
          const keys = Object.keys(_find.relation)
          for (let i = 0; i < keys.length; i++) {
            const { attributes } = await getCITypeAttributesById(_find.relation[`${keys[i]}`].type_name)
            _relationList.push({
              id: uuidv4(),
              attrName: keys[i],
              type_name: _find.relation[`${keys[i]}`].type_name,
              attr_name: _find.relation[`${keys[i]}`].attr_name,
              attributes,
            })
          }
          this.relationList = _relationList.length
            ? _relationList
            : [
                {
                  id: uuidv4(),
                  attrName: undefined,
                  type_name: undefined,
                  attr_name: undefined,
                  attributes: [],
                },
              ]
        } else {
          this.adt_id = null
          this.relationList = [
            {
              id: uuidv4(),
              attrName: undefined,
              type_name: undefined,
              attr_name: undefined,
              attributes: [],
            },
          ]
        }
      })
    },
    changeType(item) {
      console.log(item)
      this.$nextTick(() => {
        getCITypeAttributesById(item.type_name).then((res) => {
          item.attr_name = undefined
          item.attributes = res.attributes.map((item) => {
            return { ...item, value: item.id, label: item.alias || item.name }
          })
        })
      })
    },
    addRelation() {
      const _relationList = _.cloneDeep(this.relationList)
      _relationList.push({
        id: uuidv4(),
        attrName: undefined,
        type_name: undefined,
        attr_name: undefined,
        attributes: [],
      })
      this.relationList = _relationList
    },
    deleteRelation(item) {
      const _idx = this.relationList.findIndex(({ id }) => item.id === id)
      if (_idx > -1) {
        this.relationList.splice(_idx, 1)
      }
    },
    async handleSave() {
      const _relation = {}
      this.relationList.forEach(({ attrName, type_name, attr_name }) => {
        if (attrName) {
          _relation[`${attrName}`] = { type_name, attr_name }
        }
      })
      if (_relation) {
        if (this.adt_id) {
          await putCITypeDiscovery(this.adt_id, { relation: _relation })
        } else {
          await postCITypeDiscovery(this.CITypeId, { relation: _relation })
        }
        this.$message.success(this.$t('saveSuccess'))
        this.getCITypeDiscovery()
      }
    },
  },
}
</script>

<style lang="less" scoped>
.relation-ad {
  overflow: auto;
  padding: 0 20px;
  .relation-ad-item {
    display: inline-flex;
    justify-content: flex-start;
    align-items: center;
    margin: 10px 0;
  }
  .relation-ad-footer {
    width: 690px;
    text-align: right;
    margin: 10px 0;
  }
}
</style>
