<template>
  <div
    @click="
      () => {
        if (isAdd) {
          $emit('add')
        }
      }
    "
    :class="{ 'attribute-card': true, 'attribute-card-add': isAdd, 'attribute-card-inherited': inherited }"
  >
    <div class="attribute-card-uniqueKey" v-if="isUnique">{{ $t('cmdb.ciType.uniqueKey') }}</div>
    <template v-if="!isAdd">
      <a-tooltip :title="inherited ? $t('cmdb.ciType.inheritFrom', { name: property.inherited_from }) : ''">
        <div class="attribute-card-content">
          <div :class="{ 'attribute-card-value-type-icon': true, handle: !inherited }">
            <ValueTypeIcon :attr="property" />
          </div>
          <div :class="{ 'attribute-card-content-inner': true, 'attribute-card-name-required': property.is_required }">
            <div :class="{ 'attribute-card-name': true, 'attribute-card-name-default-show': property.default_show }">
              {{ property.alias || property.name }}
            </div>
            <div v-if="property.is_password" class="attribute-card_value-type">{{ $t('cmdb.ciType.password') }}</div>
            <div v-else-if="property.is_link" class="attribute-card_value-type">{{ $t('cmdb.ciType.link') }}</div>
            <div v-else class="attribute-card_value-type">{{ valueTypeMap[property.value_type] }}</div>
          </div>
          <div
            class="attribute-card-trigger"
            v-if="(property.value_type === '3' || property.value_type === '4') && !isStore"
          >
            <a @click="openTrigger"><ops-icon type="ops-trigger"/></a>
          </div>
        </div>
      </a-tooltip>

      <div class="attribute-card-footer">
        <a-popover
          trigger="click"
          :arrowPointAtCenter="true"
          placement="bottom"
          overlayClassName="attribute-card-footer-popover"
        >
          <div slot="content">
            <h3 :style="{ textAlign: 'center', paddingTop: '0.5em' }">
              <span>{{ property.alias }}({{ property.name }})</span>
            </h3>
            <a-descriptions layout="horizontal" bordered size="small" :column="2">
              <a-descriptions-item v-for="item in propertyList" :key="item.property" :label="item.label">
                <ops-icon
                  :style="{ color: property[item.property] ? '#7f97fa' : '', fontSize: '10px' }"
                  :type="`ops-${item.property}-disabled`"
                />
              </a-descriptions-item>
              <a-descriptions-item label></a-descriptions-item>
            </a-descriptions>
          </div>
          <a-space :style="{ cursor: 'pointer' }">
            <ops-icon
              v-for="item in propertyList.filter((p) => property[p.property])"
              :key="item.property"
              :style="{ color: '#7f97fa', fontSize: '10px' }"
              :type="`ops-${item.property}-disabled`"
            />
          </a-space>
        </a-popover>

        <a-space class="attribute-card-operation" v-if="!inherited">
          <a v-if="!isStore"><a-icon type="edit" @click="handleEdit"/></a>
          <a-tooltip :title="$t('cmdb.ciType.computeForAllCITips')">
            <a v-if="!isStore && property.is_computed"><a-icon type="redo" @click="handleCalcComputed"/></a>
          </a-tooltip>
          <a v-if="!isUnique" style="color:red;"><a-icon type="delete" @click="handleDelete"/></a>
        </a-space>
      </div>
      <TriggerForm ref="triggerForm" :CITypeId="CITypeId" />
    </template>
    <template v-else>
      <a><a-icon type="plus"/></a>
      <div>{{ $t('cmdb.ciType.addAttribute') }}</div>
    </template>
  </div>
</template>

<script>
import { deleteCITypeAttributesById, deleteAttributesById, calcComputedAttribute } from '@/modules/cmdb/api/CITypeAttr'
import ValueTypeIcon from '@/components/CMDBValueTypeMapIcon'
import {
  ops_default_show,
  ops_is_choice,
  ops_is_index,
  ops_is_link,
  ops_is_password,
  ops_is_sortable,
  ops_is_unique,
} from '@/core/icons'
import { valueTypeMap } from '../../utils/const'
import TriggerForm from './triggerForm.vue'
export default {
  name: 'AttributeCard',
  inject: {
    unique: {
      from: 'unique',
      default: () => undefined,
    },
  },
  components: {
    ValueTypeIcon,
    TriggerForm,
    ops_default_show,
    ops_is_choice,
    ops_is_index,
    ops_is_link,
    ops_is_password,
    ops_is_sortable,
    ops_is_unique,
  },
  props: {
    property: {
      type: Object,
      default: () => {},
    },
    CITypeId: {
      type: Number,
      default: null,
    },
    isStore: {
      type: Boolean,
      default: false,
    },
    attributes: {
      type: Array,
      default: () => [],
    },
    isAdd: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {}
  },
  computed: {
    isUnique() {
      if (this.unique) {
        return this.property?.name === this.unique()
      }
      return false
    },
    valueTypeMap() {
      return valueTypeMap()
    },
    propertyList() {
      return [
        {
          label: this.$t('cmdb.ciType.isUnique'),
          property: 'is_unique',
        },
        {
          label: this.$t('cmdb.ciType.isChoice'),
          property: 'is_choice',
        },
        {
          label: this.$t('cmdb.ciType.defaultShow'),
          property: 'default_show',
        },
        {
          label: this.$t('cmdb.ciType.isSortable'),
          property: 'is_sortable',
        },
        {
          label: this.$t('cmdb.ciType.isIndex'),
          property: 'is_index',
        },
      ]
    },
    inherited() {
      return this.property?.inherited || false
    },
  },
  methods: {
    handleEdit() {
      this.$emit('edit')
    },
    handleDelete() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDelete', { name: `${that.property.alias || that.property.name}` }),
        onOk() {
          if (that.isStore) {
            deleteAttributesById(that.property.id).then(() => {
              that.$message.success(that.$t('deleteSuccess'))
              that.$emit('ok')
            })
          } else {
            deleteCITypeAttributesById(that.CITypeId, { attr_id: [that.property.id] }).then(() => {
              that.$message.success(that.$t('deleteSuccess'))
              that.$emit('ok')
            })
          }
        },
        onCancel() {},
      })
    },
    openTrigger() {
      this.$refs.triggerForm.open(this.property, this.attributes)
    },
    handleCalcComputed() {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmcomputeForAllCITips'),
        onOk() {
          calcComputedAttribute(that.property.id).then(() => {
            that.$message.success(that.$t('cmdb.ciType.computeSuccess'))
          })
        },
      })
    },
  },
}
</script>

<style lang="less" scoped>
.attribute-card {
  width: 182px;
  height: 80px;
  background: @primary-color_6;
  border-radius: 2px;
  position: relative;
  margin-bottom: 16px;
  transition: all 0.3s;
  &:hover {
    box-shadow: 0 4px 12px #4e5ea066;
    .attribute-card-operation {
      visibility: visible !important;
    }
  }
  .attribute-card-content {
    height: 50px;
    display: inline-flex;
    align-items: center;
    padding: 8px;
    width: 100%;
    .attribute-card-value-type-icon {
      width: 32px;
      height: 32px;
      font-size: 16px;
      background: #ffffff !important;
      box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
      border-radius: 2px;
      text-align: center;
      line-height: 32px;
    }
    .handle {
      cursor: move;
    }
    .attribute-card-content-inner {
      padding-left: 12px;
      font-weight: 400;
      font-size: 12px;
      width: 120px;
      position: relative;
      .attribute-card-name {
        width: 100%;
        color: rgba(0, 0, 0, 0.8);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .attribute-card-name-default-show {
        color: @primary-color;
      }
      .attribute-card_value-type {
        font-size: 10px;
        color: rgba(0, 0, 0, 0.35);
      }
    }
    .attribute-card-name-required::before {
      content: '*';
      width: 5px;
      color: red;
      position: absolute;
      left: 3px;
    }
    .attribute-card-trigger {
      position: absolute;
      right: 8px;
      top: 8px;
    }
  }
  .attribute-card-footer {
    width: 182px;
    height: 30px;
    padding: 0 8px;
    position: absolute;
    bottom: 0;
    left: 0;
    background: @primary-color_5;
    border-radius: 0px 0px 2px 2px;
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid @primary-color_3;
    .attribute-card-operation {
      visibility: hidden;
    }
  }
  .attribute-card-uniqueKey {
    position: absolute;
    right: -12px;
    top: 0;
    color: @func-color_2;
    background: url('../../assets/unique_card.png');
    font-size: 10px;
    z-index: 1;
    background-size: 100% 100%;
    background-repeat: no-repeat;
    min-width: 55px;
    padding: 2px 0 2px 5px;
  }
}
.attribute-card-inherited {
  background: @primary-color_7;
  .attribute-card-footer {
    background: @text-color_7;
  }
}

.attribute-card-add {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  background-color: inherit;
  &:hover {
    box-shadow: none;
    background-color: @primary-color_6;
  }
  &:after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 1;
    background: linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
      linear-gradient(90deg, @text-color_5 50%, transparent 0) repeat-x,
      linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y,
      linear-gradient(0deg, @text-color_5 50%, transparent 0) repeat-y;
    background-size: 15px 1px, 15px 1px, 1px 15px, 1px 15px;
    background-position: 0 0, 0 100%, 0 0, 100% 0;
  }
  div {
    color: @text-color_4;
    font-size: 12px;
  }
}
</style>
<style lang="less">
.attribute-card-footer-popover {
  .ant-popover-inner-content {
    padding: 0;
  }
  .ant-descriptions-bordered .ant-descriptions-item-label {
    background-color: #f8faff;
  }
}
</style>
