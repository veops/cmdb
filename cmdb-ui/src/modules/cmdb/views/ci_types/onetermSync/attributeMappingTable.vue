<template>
  <div class="attribute-mapping-table">
    <a-table
      :columns="columns"
      :dataSource="fixedMappings"
      :pagination="false"
      size="small"
      rowKey="oneterm_field"
    >
      <template #cmdb_attr="text, record, index">
        <a-select
          v-model="record.cmdb_attr"
          style="width: 100%"
          :placeholder="$t('cmdb.ciType.onetermSync.selectAttribute')"
          show-search
          :filter-option="filterOption"
          @change="() => validateMapping(index)"
        >
          <a-select-option
            v-for="attr in availableAttributes"
            :key="attr.name"
            :value="attr.name"
            :disabled="isAttributeUsed(attr.name, index)"
          >
            <span>{{ attr.alias || attr.name }}</span>
            <span style="margin-left: 8px; color: #999; font-size: 12px;">({{ attr.name }})</span>
          </a-select-option>
        </a-select>
      </template>

      <template #oneterm_field="text, record">
        <span style="font-size: 13px; color: #666;">
          {{ $t(`cmdb.ciType.onetermSync.onetermField${record.oneterm_field.charAt(0).toUpperCase() + record.oneterm_field.slice(1).replace(/_./g, m => m[1].toUpperCase())}`) }}
          <span v-if="record.required" style="color: #f5222d; margin-left: 4px;">*</span>
          <a-tooltip v-if="record.oneterm_field === 'protocols'" placement="right">
            <template slot="title">
              <div style="max-width: 300px;">
                <div>{{ $t('cmdb.ciType.onetermSync.protocolsFormatHint') }}</div>
                <div style="margin-top: 8px; font-family: 'Courier New', monospace; font-size: 12px;">
                  <div>• ssh</div>
                  <div>• ssh:2222</div>
                  <div>• rdp,vnc</div>
                  <div>• ssh:22,rdp:3389</div>
                </div>
              </div>
            </template>
            <a-icon type="question-circle" :style="{ marginLeft: '4px', cursor: 'help' }" />
          </a-tooltip>
        </span>
      </template>

    </a-table>
  </div>
</template>

<script>
import _ from 'lodash'
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { DEFAULT_ATTR_MAPPING } from './constants'

export default {
  name: 'AttributeMappingTable',
  props: {
    ciTypeId: {
      type: Number,
      required: true,
    },
    mappings: {
      type: Array,
      default: () => [],
    },
    syncStrategy: {
      type: String,
      default: 'physical',
    },
  },
  data() {
    return {
      allAttributes: [],
      fixedMappings: _.cloneDeep(DEFAULT_ATTR_MAPPING),
      columns: [
        {
          title: this.$t('cmdb.ciType.onetermSync.cmdbAttribute'),
          dataIndex: 'cmdb_attr',
          width: '45%',
          scopedSlots: { customRender: 'cmdb_attr' },
        },
        {
          title: '',
          width: '60px',
          align: 'center',
          customRender: () => <a-icon type="arrow-right" style="color: #999;" />,
        },
        {
          title: this.$t('cmdb.ciType.onetermSync.onetermField'),
          dataIndex: 'oneterm_field',
          width: '45%',
          scopedSlots: { customRender: 'oneterm_field' },
        },
      ],
    }
  },
  computed: {
    availableAttributes() {
      return this.allAttributes.filter((attr) => {
        // Exclude JSON type (value_type: 6)
        if (attr.value_type === '6' || attr.value_type === 6) return false

        // Exclude attachment type
        if (attr.is_attachment) return false

        // Exclude password type
        if (attr.is_password) return false

        // Exclude reference attributes (is_link=true)
        if (attr.is_link) return false

        // Exclude multi-value attributes
        if (attr.is_list) return false
        if (attr.is_choice && attr.is_choice === 2) return false

        // Exclude computed attributes
        if (attr.is_computed) return false

        return true
      })
    },
  },
  watch: {
    mappings: {
      handler(val) {
        if (val && val.length) {
          val.forEach((m) => {
            const fixed = this.fixedMappings.find((f) => f.oneterm_field === m.oneterm_field)
            if (fixed) {
              fixed.cmdb_attr = m.cmdb_attr
            }
          })
        }
      },
      immediate: true,
      deep: true,
    },
  },
  mounted() {
    this.loadCITypeAttributes()
  },
  methods: {
    async loadCITypeAttributes() {
      try {
        const res = await getCITypeAttributesById(this.ciTypeId)
        // API returns { attributes: [...] }
        this.allAttributes = res.attributes || []
      } catch (e) {
        console.error('Failed to load attributes:', e)
        this.$message.error(this.$t('cmdb.ciType.onetermSync.loadAttributesFailed'))
      }
    },

    filterOption(input, option) {
      const text = option.componentOptions.children[0].text.toLowerCase()
      return text.includes(input.toLowerCase())
    },

    isAttributeUsed(attrName, currentIndex) {
      return this.fixedMappings.some(
        (m, index) => index !== currentIndex && m.cmdb_attr === attrName
      )
    },

    validateMapping(index) {
      this.emitChange()
    },

    emitChange() {
      this.$emit('change', this.fixedMappings)
    },
  },
}
</script>

<style lang="less" scoped>
.attribute-mapping-table {
  /deep/ .ant-table {
    .ant-table-thead > tr > th {
      background: #fafafa;
      font-weight: 500;
    }

    .ant-table-tbody > tr > td {
      padding: 12px 16px;
    }

    .ant-table-tbody > tr:hover > td {
      background: #f5f5f5;
    }
  }
}
</style>
