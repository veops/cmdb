<template>
  <div>
    <a-modal
      v-model="addGroupModal"
      :title="$t('cmdb.ciType.addGroup')"
      @cancel="handleCancelCreateGroup"
      @ok="handleCreateGroup"
    >
      <span>
        <a-form-item :label="$t('name')" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-input type="text" v-model.trim="newGroupName" />
        </a-form-item>
      </span>
    </a-modal>
    <div class="ci-types-attributes" :style="{ maxHeight: `${windowHeight - 104}px` }">
      <a-space style="margin-bottom: 10px">
        <a-button type="primary" @click="handleAddGroup" size="small" class="ops-button-primary" icon="plus">{{
          $t('cmdb.ciType.group')
        }}</a-button>
        <a-button type="primary" @click="handleOpenUniqueConstraint" size="small" class="ops-button-primary">{{
          $t('cmdb.ciType.uniqueConstraint')
        }}</a-button>
      </a-space>
      <div :key="CITypeGroup.id" v-for="(CITypeGroup, index) in CITypeGroups">
        <div>
          <div
            :style="{ height: '32px', lineHeight: '32px', display: 'inline-block', fontSize: '14px' }"
            v-if="!CITypeGroup.editable"
          >
            <span style="font-weight:700">{{ CITypeGroup.name }}</span>
            <span style="color: #c3cdd7;margin:0 5px;">({{ CITypeGroup.attributes.length }})</span>

            <a v-if="!CITypeGroup.inherited" @click="handleEditGroupName(index, CITypeGroup)">
              <a-icon type="edit" />
            </a>
            <a v-else :style="{ cursor: 'not-allowed', color: 'gray' }">
              <a-icon type="edit" />
            </a>
          </div>
          <template v-else>
            <span>
              <a-input
                type="text"
                style="width: 200px;margin-right:10px;"
                ref="editGroupInput"
                v-model.trim="CITypeGroup.name"
              />
              <a @click="handleSaveGroupName(index, CITypeGroup)" style="margin-right: 0.5rem">{{ $t('save') }}</a>
              <a @click="handleCancelGroupName(index, CITypeGroup)">{{ $t('cancel') }}</a>
            </span>
          </template>
          <a-space style="float: right">
            <a-tooltip v-if="index">
              <template slot="title">{{ $t('cmdb.ciType.up') }}</template>
              <a><a-icon type="arrow-up" v-if="index" @click="handleMoveGroup(index, index - 1)"/></a>
            </a-tooltip>

            <a-tooltip v-if="index !== CITypeGroups.length - 1">
              <template slot="title">{{ $t('cmdb.ciType.up') }}</template>
              <a
              ><a-icon
                type="arrow-down"
                v-if="index !== CITypeGroups.length - 1"
                @click="handleMoveGroup(index, index + 1)"
              /></a>
            </a-tooltip>

            <a-tooltip>
              <template slot="title">{{ $t('cmdb.ciType.selectAttribute') }}</template>
              <a><a-icon type="plus" @click="handleAddGroupAttr(index)"/></a>
            </a-tooltip>
            <a-tooltip>
              <template slot="title">{{ $t('cmdb.ciType.deleteGroup') }}</template>
              <a
                :style="{ color: CITypeGroup.inherited ? 'gray' : 'red' }"
                :disabled="CITypeGroup.inherited"
              ><a-icon
                type="delete"
                @click="handleDeleteGroup(CITypeGroup)"
              /></a>
            </a-tooltip>
          </a-space>
        </div>
        <div class="ci-types-attributes-wrapper">
          <draggable
            v-model="CITypeGroup.attributes"
            group="properties"
            @start="drag = true"
            @change="
              (e) => {
                handleChange(e, CITypeGroup.name)
              }
            "
            :filter="'.filter-empty'"
            :animation="300"
            tag="div"
            style="width: 100%; display: flex;flex-flow: wrap"
            handle=".handle"
          >
            <AttributeCard
              v-for="item in CITypeGroup.attributes"
              :key="item.id"
              @edit="handleEditProperty(item)"
              :property="item"
              @ok="handleOk"
              :CITypeId="CITypeId"
              :attributes="attributes"
            />
            <i></i> <i></i> <i></i> <i></i> <i></i>
          </draggable>
        </div>
      </div>
      <div>
        <div :style="{ height: '32px', lineHeight: '32px', display: 'inline-block', fontSize: '14px' }">
          <span style="font-weight:700">{{ $t('other') }}</span>
          <span style="color: #c3cdd7;margin-left:5px;">({{ otherGroupAttributes.length }})</span>
        </div>
        <div style="float: right">
          <a-tooltip>
            <template slot="title">{{ $t('cmdb.ciType.selectAttribute') }}</template>
            <a @click="handleAddGroupAttr(undefined)"><a-icon type="plus"/></a>
          </a-tooltip>
        </div>
      </div>

      <div class="ci-types-attributes-wrapper">
        <draggable
          v-model="otherGroupAttributes"
          group="properties"
          @start="drag = true"
          @change="
            (e) => {
              handleChange(e, null)
            }
          "
          :animation="300"
          style="min-height: 2rem; width: 100%; display: flex; flex-flow: wrap"
          handle=".handle"
        >
          <AttributeCard
            v-for="item in otherGroupAttributes"
            :key="item.id"
            @edit="handleEditProperty(item)"
            :property="item"
            @ok="handleOk"
            :CITypeId="CITypeId"
            :attributes="attributes"
          />
          <i></i> <i></i> <i></i> <i></i> <i></i>
        </draggable>
      </div>
    </div>
    <AttributeEditForm
      ref="attributeEditForm"
      :CITypeId="CITypeId"
      :CITypeName="CITypeName"
      @ok="handleOk"
    ></AttributeEditForm>
    <NewCiTypeAttrModal
      ref="newCiTypeAttrModal"
      :CITypeId="CITypeId"
      :linked-ids="linkedIds"
      @ok="handleOk"
    ></NewCiTypeAttrModal>
    <UniqueConstraint ref="uniqueConstraint" :CITypeId="CITypeId" />
  </div>
</template>

<script>
import {
  deleteCITypeGroupById,
  getCITypeGroupById,
  createCITypeGroupById,
  updateCITypeGroupById,
  getTriggerList,
} from '@/modules/cmdb/api/CIType'
import {
  getCITypeAttributesById,
  updateCITypeAttributesById,
  transferCITypeAttrIndex,
  transferCITypeGroupIndex,
} from '@/modules/cmdb/api/CITypeAttr'
import draggable from 'vuedraggable'
import AttributeCard from './attributeCard.vue'
import AttributeEditForm from './attributeEditForm.vue'
import NewCiTypeAttrModal from './newCiTypeAttrModal.vue'
import UniqueConstraint from './uniqueConstraint.vue'

export default {
  name: 'AttributesTable',
  components: {
    draggable,
    AttributeCard,
    AttributeEditForm,
    NewCiTypeAttrModal,
    UniqueConstraint,
  },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
    CITypeName: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      form: this.$form.createForm(this),
      CITypeGroups: [],
      addRemoveGroupFlag: {},
      attributes: [],
      otherGroupAttributes: [],
      addGroupModal: false,
      newGroupName: '',
    }
  },
  computed: {
    linkedIds() {
      return this.attributes.map((i) => i.id)
    },
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  provide() {
    return { refresh: this.getCITypeGroupData }
  },
  beforeCreate() {},
  created() {},
  mounted() {
    this.getCITypeGroupData()
  },
  methods: {
    handleEditProperty(property) {
      this.$refs.attributeEditForm.handleEdit(property, this.attributes)
    },
    handleOk() {
      this.getCITypeGroupData()
    },
    setOtherGroupAttributes() {
      const orderMap = this.attributes.reduce(function(map, obj) {
        map[obj.id] = obj.order
        return map
      }, {})

      const inGroupAttrKeys = this.CITypeGroups.filter((x) => x.attributes && x.attributes.length > 0)
        .map((x) => x.attributes)
        .flat()
        .map((x) => x.id)

      this.CITypeGroups.forEach((group) => {
        group.attributes.forEach((attribute) => {
          attribute.order = orderMap[attribute.id]
          attribute.originOrder = attribute.order
          attribute.originGroupName = group.name
        })
        group.originCount = group.attributes.length
        group.editable = false
        group.originOrder = group.order
        group.originName = group.name
      })

      this.otherGroupAttributes = this.attributes
        .filter((x) => !inGroupAttrKeys.includes(x.id))
        .sort((a, b) => a.order - b.order)
      this.attributes = this.attributes.sort((a, b) => a.order - b.order)
      this.CITypeGroups = this.CITypeGroups.sort((a, b) => a.order - b.order)
      this.otherGroupAttributes.forEach((attribute) => {
        attribute.originOrder = attribute.order
      })

      // console.log('setOtherGroupAttributes', this.CITypeGroups, this.otherGroupAttributes)
    },
    getCITypeGroupData() {
      const promises = [
        getCITypeAttributesById(this.CITypeId),
        getCITypeGroupById(this.CITypeId),
        getTriggerList(this.CITypeId),
      ]
      Promise.all(promises).then((values) => {
        console.log(values)
        this.attributes = values[0].attributes
        const temp = {}
        this.attributes.forEach((attr) => {
          temp[attr.id] = attr
        })
        this.CITypeGroups = values[1]
        this.CITypeGroups.forEach((g) => {
          g.attributes.forEach((a) => {
            a.is_required = (temp[a.id] && temp[a.id].is_required) || false
            a.default_show = (temp[a.id] && temp[a.id].default_show) || false
            const idx = values[2].findIndex((item) => item.attr_id === a.id)
            a.has_trigger = idx > -1
            if (idx > -1) {
              a.trigger = values[2][idx]
            }
          })
        })
        this.setOtherGroupAttributes()
      })
    },

    handleEditGroupName(index, CITypeGroup) {
      CITypeGroup.editable = true
      this.$set(this.CITypeGroups, index, CITypeGroup)
    },
    handleSaveGroupName(index, CITypeGroup) {
      if (CITypeGroup.name === CITypeGroup.originName) {
        this.handleCancelGroupName(index, CITypeGroup)
      } else if (this.CITypeGroups.map((x) => x.originName).includes(CITypeGroup.name)) {
        this.$message.error(this.$t('cmdb.ciType.groupExisted'))
      } else {
        updateCITypeGroupById(CITypeGroup.id, {
          name: CITypeGroup.name,
          attributes: CITypeGroup.attributes.map((x) => x.id),
          order: CITypeGroup.order,
        }).then((res) => {
          CITypeGroup.editable = false
          this.$set(this.CITypeGroups, index, CITypeGroup)
          this.$message.success(this.$t('updateSuccess'))
        })
      }
    },
    handleCancelGroupName(index, CITypeGroup) {
      CITypeGroup.editable = false
      CITypeGroup.name = CITypeGroup.originName
      this.$set(this.CITypeGroups, index, CITypeGroup)
    },

    handleCancel(CITypeGroup) {
      CITypeGroup.editable = false
    },
    handleAddGroup() {
      this.addGroupModal = true
    },
    handleCreateGroup() {
      const groupOrders = this.CITypeGroups.map((x) => x.order)

      const maxGroupOrder = Math.max(groupOrders.length, groupOrders.length ? Math.max(...groupOrders) : 0)

      console.log('groupOrder', groupOrders, 'maxOrder', maxGroupOrder)
      createCITypeGroupById(this.CITypeId, { name: this.newGroupName, order: maxGroupOrder + 1 }).then((res) => {
        this.addGroupModal = false
        this.newGroupName = ''
        this.getCITypeGroupData()
      })
    },
    handleCancelCreateGroup() {
      this.addGroupModal = false
      this.newGroupName = ''
    },

    handleMoveGroup(beforeIndex, afterIndex) {
      const fromGroupId = this.CITypeGroups[beforeIndex].name
      const toGroupId = this.CITypeGroups[afterIndex].name
      transferCITypeGroupIndex(this.CITypeId, { from: fromGroupId, to: toGroupId }).then((res) => {
        this.$message.success(this.$t('operateSuccess'))
        const beforeGroup = this.CITypeGroups[beforeIndex]
        this.CITypeGroups[beforeIndex] = this.CITypeGroups[afterIndex]

        this.$set(this.CITypeGroups, beforeIndex, this.CITypeGroups[afterIndex])
        this.$set(this.CITypeGroups, afterIndex, beforeGroup)
      })
    },
    handleAddGroupAttr(index) {
      let group = null
      if (index === 0 || index) {
        group = this.CITypeGroups[index]
        console.log(group)
      }
      this.$refs.newCiTypeAttrModal.handleEdit(group)
    },

    handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          // eslint-disable-next-line no-console
          console.log('Received values of form: ', values)

          this.CITypeGroups.forEach((group) => {
            if (group.id === values.groupId) {
              group.attributes = this.attributes.filter((x) => values.checkedAttributes.includes(x.id))
            } else {
              group.attributes = group.attributes.filter((x) => !values.checkedAttributes.includes(x.id))
            }
          })

          this.otherGroupAttributes.forEach((attributes) => {
            if (values.groupId === null) {
              this.otherGroupAttributes = this.otherGroupAttributes.filter((x) =>
                values.checkedAttributes.includes(x.id)
              )
            } else {
              this.otherGroupAttributes = this.otherGroupAttributes.filter(
                (x) => !values.checkedAttributes.includes(x.id)
              )
            }
          })

          console.log('add group attribute', this.otherGroupAttributes, this.CITypeGroups)
          this.updatePropertyIndex()
        }
      })
    },

    handleDeleteGroup(group) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteGroup', { groupName: `${group.name}` }),
        onOk() {
          deleteCITypeGroupById(group.id).then((res) => {
            that.CITypeGroups = that.CITypeGroups.filter((g) => g.id !== group.id)
            that.updatePropertyIndex()
          })
        },
      })
    },
    handleChange(e, group) {
      console.log('changess', group)
      if (e.hasOwnProperty('moved') && e.moved.oldIndex !== e.moved.newIndex) {
        if (group === -1) {
          this.$message.error(this.$t('cmdb.ciType.attributeSortedTips'))
        } else {
          transferCITypeAttrIndex(this.CITypeId, {
            from: { attr_id: e.moved.element.id, group_name: group },
            to: { order: e.moved.newIndex, group_name: group },
          })
            .then((res) => this.$message.success(this.$t('updateSuccess')))
            .catch(() => {
              this.abortDraggable()
            })
        }
      }

      if (e.hasOwnProperty('added')) {
        this.addRemoveGroupFlag = { to: { group_name: group, order: e.added.newIndex }, inited: true }
      }

      if (e.hasOwnProperty('removed')) {
        this.$nextTick(() => {
          transferCITypeAttrIndex(this.CITypeId, {
            from: { attr_id: e.removed.element.id, group_name: group },
            to: { group_name: this.addRemoveGroupFlag.to.group_name, order: this.addRemoveGroupFlag.to.order },
          })
            .then((res) => this.$message.success(this.$t('saveSuccess')))
            .catch(() => {
              this.abortDraggable()
            })
            .finally(() => {
              this.addRemoveGroupFlag = {}
            })
        })
      }
    },
    abortDraggable() {
      this.$nextTick(() => {
        this.$router.push({ name: 'ci_type' })
      })
    },
    updatePropertyIndex() {
      const attributes = [] // All attributes
      let attributeOrder = 0 // attribute group
      let groupOrder = 0 // group sort
      const promises = []

      this.CITypeGroups.forEach((group) => {
        const groupName = group.name

        let groupAttributes = []
        let groupUpdate = false
        group.order = groupOrder

        group.attributes.forEach((attribute) => {
          groupAttributes.push(attribute.id)

          if (attribute.originGroupName !== group.name || attribute.originOrder !== attributeOrder) {
            attributes.push({ attr_id: attribute.id, order: attributeOrder })
            groupUpdate = true
          }
          attributeOrder++
        })

        groupAttributes = new Set(groupAttributes)
        if (group.originCount !== groupAttributes.size || groupUpdate || group.originOrder !== group.order) {
          promises.push(
            updateCITypeGroupById(group.id, { name: groupName, attributes: [...groupAttributes], order: groupOrder })
          )
        }
        groupOrder++
      })

      this.otherGroupAttributes.forEach((attribute) => {
        if (attribute.originOrder !== attributeOrder) {
          console.log(
            'this attribute:',
            attribute.name,
            'old order',
            attribute.originOrder,
            'new order',
            attributeOrder
          )
          attributes.push({ attr_id: attribute.id, order: attributeOrder })
        }

        attributeOrder++
      })

      if (attributes && attributes.length > 0) {
        promises.unshift(updateCITypeAttributesById(this.CITypeId, { attributes: attributes }))
      }

      const that = this
      Promise.all(promises).then((values) => {
        that.$message.success(that.$t('updateSuccess'))
        that.getCITypeGroupData()
        that.modalVisible = false
      })
    },
    handleOpenUniqueConstraint() {
      this.$refs.uniqueConstraint.open(this.attributes)
    },
  },
  watch: {},
}
</script>

<style lang="less" scoped>
.fold {
  width: calc(100% - 216px);
  display: inline-block;
}

.ci-types-attributes {
  padding: 16px 24px 24px;
  overflow-y: auto;
  .property-item-empty {
    color: #40a9ff;
    width: calc(100% - 20px);
    margin: 5px;
    border: 1px dotted #d9d9d9;
    border-radius: 2px;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
    height: 60px;
    line-height: 60px;
    transition: all 0.3s;
    &:hover {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
  }
  .ci-types-attributes-wrapper > div {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    min-height: 20px;
    > i {
      width: 182px;
    }
  }
}

@media screen and (max-width: 900px) {
  .fold {
    width: 100%;
  }
}
</style>
