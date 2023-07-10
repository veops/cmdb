<template>
  <div class="attribute-card">
    <div class="attribute-card-content">
      <div class="attribute-card-value-type-icon handle" :style="{ ...getPropertyStyle(property) }">
        <ValueTypeIcon :attr="property" />
      </div>
      <div :class="{ 'attribute-card-content-inner': true, 'attribute-card-name-required': property.is_required }">
        <div :class="{ 'attribute-card-name': true, 'attribute-card-name-default-show': property.default_show }">
          {{ property.alias || property.name }}
        </div>
        <div class="attribute-card_value-type">{{ valueTypeMap[property.value_type] }}</div>
      </div>
      <div class="attribute-card-trigger" v-if="property.value_type === '3' || property.value_type === '4'">
        <a @click="openTrigger"><ops-icon type="ops-trigger"/></a>
      </div>
    </div>
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
              <components
                :is="`ops_${item.property}`"
                v-if="property[item.property]"
                :style="{ width: '1em', height: '1em' }"
              />
              <ops-icon v-else :type="`ops-${item.property}-disabled`" />
            </a-descriptions-item>
            <a-descriptions-item label></a-descriptions-item>
          </a-descriptions>
        </div>
        <a-space :style="{ cursor: 'pointer' }">
          <components
            v-for="item in propertyList.filter((p) => property[p.property])"
            :key="item.property"
            :is="`ops_${item.property}`"
          />
        </a-space>
      </a-popover>

      <a-space class="attribute-card-operation">
        <a><a-icon type="edit" @click="handleEdit"/></a>
        <a style="color:red;"><a-icon type="delete" @click="handleDelete"/></a>
      </a-space>
    </div>
    <TriggerForm ref="triggerForm" :CITypeId="CITypeId" />
  </div>
</template>

<script>
import { deleteCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
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
import { getPropertyStyle } from '../../utils/helper'
import TriggerForm from './triggerForm.vue'
export default {
  name: 'AttributeCard',
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
  },
  data() {
    const propertyList = [
      {
        label: '是否唯一',
        property: 'is_unique',
      },
      {
        label: '是否选择',
        property: 'is_choice',
      },
      {
        label: '默认显示',
        property: 'default_show',
      },
      {
        label: '可排序',
        property: 'is_sortable',
      },
      {
        label: '是否索引',
        property: 'is_index',
      },
      {
        label: '是否密码',
        property: 'is_password',
      },
      {
        label: '是否链接',
        property: 'is_link',
      },
    ]
    return {
      valueTypeMap,
      propertyList,
    }
  },
  methods: {
    getPropertyStyle,
    handleEdit() {
      this.$emit('edit')
    },
    handleDelete() {
      const that = this
      this.$confirm({
        title: '警告',
        content: `确认删除 【${that.property.alias || that.property.name}】？`,
        onOk() {
          deleteCITypeAttributesById(that.CITypeId, { attr_id: [that.property.id] }).then(() => {
            that.$message.success('删除成功！')
            that.$emit('ok')
          })
        },
        onCancel() {},
      })
    },
    openTrigger() {
      this.$refs.triggerForm.open(this.property)
    },
  },
}
</script>

<style lang="less" scoped>
.attribute-card {
  width: 182px;
  height: 80px;
  background: #f8faff;
  border-radius: 5px;
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
      font-size: 12px;
      cursor: move;
      background: #ffffff !important;
      box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
      border-radius: 2px;
      text-align: center;
      line-height: 32px;
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
        color: #2f54eb;
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
    background: linear-gradient(180deg, #96abd6 0%, #ecf2ff 0.01%, #ffffff 143.33%);
    border-radius: 0px 0px 5px 5px;
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
    .attribute-card-operation {
      visibility: hidden;
    }
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
