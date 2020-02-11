<template>
  <div>
    <div style="margin-bottom: 2rem">
      <a-button type="primary" v-if="addGroupBtnVisible" @click="handleAddGroup">添加分组</a-button>

      <template v-else>
        <span>
          <a-input
            size="small"
            type="text"
            style="width: 10rem;margin-right: 0.5rem"
            ref="addGroupInput"
            v-model.trim="newGroupName" />
          <a @click="handleCreateGroup" style="margin-right: 0.5rem">保存</a>
          <a @click="handleCancelCreateGroup">{{ $t('button.cancel') }}</a>
        </span>
      </template>

    </div>

    <div :key="index" v-for="(CITypeGroup, index) in CITypeGroups">
      <div class="group-header">

        <template style="margin-bottom: 2rem;" v-if="!CITypeGroup.editable">

          <span style="margin-right: 0.2rem">{{ CITypeGroup.name }}</span>
          <span style="color: #c3cdd7; margin-right: 0.5rem">({{ CITypeGroup.attributes.length }})</span>

          <a-button type="link" size="small" @click="handleEditGroupName(index, CITypeGroup)"><a-icon type="edit" /></a-button>
        </template>
        <template v-else>
          <span style="font-size: 1rem">
            <a-input
              size="small"
              type="text"
              style="width: 15%;margin-right: 0.5rem"
              ref="editGroupInput"
              v-model.trim="CITypeGroup.name" />
            <a @click="handleSaveGroupName(index, CITypeGroup)" style="margin-right: 0.5rem">保存</a>
            <a @click="handleCancelGroupName(index, CITypeGroup)">{{ $t('button.cancel') }}</a>
          </span>
        </template>

        <div style="float: right">

          <a-button-group size="small">
            <a-tooltip>
              <template slot="title">
                上移
              </template>
              <a-button icon="arrow-up" size="small" @click="handleMoveGroup(index, index-1)" :disabled="index===0"/>
            </a-tooltip>

            <a-tooltip>
              <template slot="title">
                下移
              </template>
              <a-button icon="arrow-down" size="small" @click="handleMoveGroup(index, index+1)" :disabled="index===CITypeGroups.length-1" />
            </a-tooltip>

            <a-tooltip>
              <template slot="title">
                添加属性
              </template>
              <a-button icon="plus" size="small" @click="handleAddExistGroupAttr(index)"/>
            </a-tooltip>
            <a-tooltip>
              <template slot="title">
                删除分组
              </template>
              <a-button icon="delete" size="small" @click="handleDeleteGroup(CITypeGroup.id)" :disabled="CITypeGroup.attributes.length!==0" />

            </a-tooltip>

          </a-button-group>
        </div>

      </div>

      <div
        class="box"
        style="min-height: 2rem; margin-bottom: 1.5rem;"
      >

        <draggable
          v-model="CITypeGroup.attributes"
          group="properties"
          @start="drag=true"
          @change="(e)=>{handleChange(e, CITypeGroup.id)}"
          :filter="'.filter-empty'"
          :animation="100"
          tag="div"
          style="width: 100%; display: flex;flex-flow: wrap"
        >

          <li
            class="property-item"
            v-for="item in CITypeGroup.attributes"
            :key="item.id"
          >
            {{ item.alias }}
          </li>

          <template
            v-if="!CITypeGroup.attributes.length"
            style="height: 2rem"
          >
            <li
              class="property-item-empty"
              @click="handleAddExistGroupAttr(index)"
              style="">添加属性</li>

          </template>

        </draggable>

      </div>

    </div>
    <div class="group-header">

      <template>

        <span style="margin-right: 0.2rem">更多属性</span>
        <span style="color: #c3cdd7; margin-right: 0.5rem">({{ otherGroupAttributes.length }})</span>
      </template>
      <div style="float: right">
        <a-button-group size="small">
          <a-tooltip>
            <template slot="title">
              上移
            </template>
            <a-button icon="arrow-up" size="small" disabled/>
          </a-tooltip>

          <a-tooltip>
            <template slot="title">
              下移
            </template>
            <a-button icon="arrow-down" size="small" disabled />
          </a-tooltip>

          <a-tooltip>
            <template slot="title">
              添加属性
            </template>
            <a-button icon="plus" size="small" @click="handleAddOtherGroupAttr"/>
          </a-tooltip>
          <a-tooltip>
            <template slot="title">
              删除分组
            </template>
            <a-button icon="delete" size="small" disabled />

          </a-tooltip>

        </a-button-group>
      </div>
    </div>

    <div class="box">
      <draggable
        v-model="otherGroupAttributes"
        group="properties"
        @start="drag=true"
        @change="(e)=>{handleChange(e, -1)}"
        :animation="0"
        style="min-height: 2rem; width: 100%; display: flex; flex-flow: wrap">

        <li
          class="property-item"
          v-for="item in otherGroupAttributes"
          :key="item.id"
        >
          {{ item.alias }}
        </li>

        <template
          v-if="!otherGroupAttributes.length"
          style="display: block"
        >
          <li
            class="property-item-empty"
            @click="handleAddOtherGroupAttr"
            style="">添加属性</li>

        </template>

      </draggable>
    </div>
    <a-modal
      title="添加字段"
      :width="'80%'"
      v-model="modalVisible"
      @ok="handleSubmit"
      @cancel="modalVisible = false"

    >
      <a-form :form="form" @submit="handleSubmit">

        <a-form-item
        >
          <a-checkbox-group
            v-decorator="['checkedAttributes']"
            style="width: 90%"
          >

            <a-row :gutter="{ xs: 8, sm: 16, md: 24}" type="flex" justify="start">
              <a-col
                v-for="attribute in attributes"
                :key="attribute.id"
                :sm="8"
                :md="6"
                :lg="4"
                :xxl="3"
                style="line-height: 1.8rem"
              >
                <a-checkbox
                  :value="attribute.id">
                  {{ attribute.alias }}
                </a-checkbox>

              </a-col>

            </a-row>
          </a-checkbox-group>
        </a-form-item>

        <a-form-item>
          <a-input
            name="groupId"
            type="hidden"
            v-decorator="['groupId']"
          />
        </a-form-item>

        <a-form-item>
          <a-input
            name="groupIndex"
            type="hidden"
            v-decorator="['groupIndex']"
          />
        </a-form-item>
      </a-form>
    </a-modal>

  </div >

</template>

<script>
/* eslint-disable */
import {
  deleteCITypeGroupById,
  getCITypeGroupById,
  createCITypeGroupById,
  updateCITypeGroupById
} from '@/api/cmdb/CIType'
import { getCITypeAttributesById, updateCITypeAttributesById, transferCITypeAttrIndex, transferCITypeGroupIndex } from '@/api/cmdb/CITypeAttr'
import draggable from 'vuedraggable'

export default {
  name: 'Group',
  components: {
    draggable
  },
  data () {
    return {
      form: this.$form.createForm(this),
      CITypeId: this.$route.params.CITypeId,
      CITypeName: this.$route.params.CITypeName,
      CITypeGroups: [],
      addRemoveGroupFlag: {},
      attributes: [],
      otherGroupAttributes: [],
      addGroupBtnVisible: true,
      newGroupName: '',
      modalVisible: false

    }
  },
  beforeCreate () {
  },
  created () {

  },
  computed: {

  },
  mounted () {
    this.getCITypeGroupData()
  },
  methods: {
    setOtherGroupAttributes () {
      const orderMap = this.attributes.reduce(function (map, obj) {
        map[obj.id] = obj.order
        return map
      }, {})

      const inGroupAttrKeys = this.CITypeGroups
        .filter(x => x.attributes && x.attributes.length > 0)
        .map(x => x.attributes).flat().map(x => x.id)

      this.CITypeGroups.forEach(group => {
        group.attributes.forEach(attribute => {
          attribute.order = orderMap[attribute.id]
          attribute.originOrder = attribute.order
          attribute.originGroupName = group.name
        })
        group.originCount = group.attributes.length
        group.editable = false
        group.originOrder = group.order
        group.originName = group.name
        // group.attributes = group.attributes.sort((a, b) => a.order - b.order)
      })

      this.otherGroupAttributes = this.attributes.filter(x => !inGroupAttrKeys.includes(x.id)).sort((a, b) => a.order - b.order)
      this.attributes = this.attributes.sort((a, b) => a.order - b.order)
      this.CITypeGroups = this.CITypeGroups.sort((a, b) => a.order - b.order)
      this.otherGroupAttributes.forEach(attribute => {
        attribute.originOrder = attribute.order
      })

      // console.log('setOtherGroupAttributes', this.CITypeGroups, this.otherGroupAttributes)
    },
    getCITypeGroupData () {
      const promises = [
        getCITypeAttributesById(this.CITypeId),
        getCITypeGroupById(this.CITypeId)
      ]
      Promise.all(promises)
        .then(values => {
          this.attributes = values[0].attributes
          this.CITypeGroups = values[1]
          this.setOtherGroupAttributes()
        })
    },

    handleEditGroupName (index, CITypeGroup) {
      CITypeGroup.editable = true
      this.$set(this.CITypeGroups, index, CITypeGroup)
    },
    handleSaveGroupName (index, CITypeGroup) {
      if (CITypeGroup.name === CITypeGroup.originName) {
        this.handleCancelGroupName(index, CITypeGroup)
      } else if (this.CITypeGroups.map(x => x.originName).includes(CITypeGroup.name)) {
        this.$message.error('分组名称已存在')
      } else {
        updateCITypeGroupById(CITypeGroup.id, { name: CITypeGroup.name, attributes: CITypeGroup.attributes.map(x => x.id), order: CITypeGroup.order })
          .then(res => {
            CITypeGroup.editable = false
            this.$set(this.CITypeGroups, index, CITypeGroup)
            this.$message.success('修改成功')
          })
          .catch(err => this.requestFailed(err))
      }
    },
    handleCancelGroupName (index, CITypeGroup) {
      CITypeGroup.editable = false
      this.$set(this.CITypeGroups, index, CITypeGroup)
    },

    handleCancel (CITypeGroup) {
      CITypeGroup.editable = false
    },
    handleAddGroup () {
      this.addGroupBtnVisible = false
    },
    handleCreateGroup () {
      const groupOrders = this.CITypeGroups.map(x => x.order)

      const maxGroupOrder = Math.max(groupOrders.length, groupOrders.length ? Math.max(...groupOrders) : 0)

      console.log('groupOrder', groupOrders, 'maxOrder', maxGroupOrder)
      createCITypeGroupById(this.CITypeId, { name: this.newGroupName, order: maxGroupOrder + 1 })
        .then(res => {
          this.addGroupBtnVisible = true
          this.newGroupName = ''
          this.getCITypeGroupData()
        })
        .catch(err => this.requestFailed(err))
    },
    handleCancelCreateGroup () {
      this.addGroupBtnVisible = true
      this.newGroupName = ''
    },

    handleMoveGroup (beforeIndex, afterIndex) {
      const fromGroupId = this.CITypeGroups[beforeIndex].id
      const toGroupId = this.CITypeGroups[afterIndex].id
      transferCITypeGroupIndex(this.CITypeId, { from: fromGroupId, to: toGroupId }).then(res => {
        this.$message.success('操作成功')
        const beforeGroup = this.CITypeGroups[beforeIndex]
        this.CITypeGroups[beforeIndex] = this.CITypeGroups[afterIndex]

        this.$set(this.CITypeGroups, beforeIndex, this.CITypeGroups[afterIndex])
        this.$set(this.CITypeGroups, afterIndex, beforeGroup)
      }).catch(err => {
        this.$httpError(err, '移动出错')
      })
    },
    handleAddExistGroupAttr (index) {
      const group = this.CITypeGroups[index]
      this.modalVisible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({
          checkedAttributes: group.attributes.map(x => x.id),
          groupId: group.id,
          groupIndex: index

        })
      })
    },

    handleAddOtherGroupAttr () {
      this.modalVisible = true
      this.$nextTick(() => {
        this.form.setFieldsValue({
          checkedAttributes: this.otherGroupAttributes.map(x => x.id),
          groupId: null

        })
      })
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          // eslint-disable-next-line no-console
          console.log('Received values of form: ', values)

          this.CITypeGroups.forEach(group => {
            if (group.id === values.groupId) {
              group.attributes = this.attributes.filter(x => values.checkedAttributes.includes(x.id))
            } else {
              group.attributes = group.attributes.filter(x => !values.checkedAttributes.includes(x.id))
            }
          })
          // this.CITypeGroups = this.CITypeGroups

          this.otherGroupAttributes.forEach(attributes => {
            if (values.groupId === null) {
              this.otherGroupAttributes = this.otherGroupAttributes.filter(x => values.checkedAttributes.includes(x.id))
            } else {
              this.otherGroupAttributes = this.otherGroupAttributes.filter(x => !values.checkedAttributes.includes(x.id))
            }
          })

          console.log('add group attribute', this.otherGroupAttributes, this.CITypeGroups)
          this.updatePropertyIndex()
        }
      })
    },

    handleDeleteGroup (groupId) {
      deleteCITypeGroupById(groupId)
        .then(res => {
          this.updatePropertyIndex()
        })
        .catch(err => this.requestFailed(err))
    },
    handleChange (e, group) {
      if (e.hasOwnProperty('moved') && e.moved.oldIndex !== e.moved.newIndex) {
        if (group === -1) {
          this.$message.error('更多属性不能进行排序, 如需排序需添加入其他分组中！')
        } else {
          transferCITypeAttrIndex(this.CITypeId,
            {
              from: { attr_id: e.moved.element.id, group_id: group > -1 ? group : null },
              to: { order: e.moved.newIndex, group_id: group > -1 ? group : null }
            }).then(res => this.$message.success('保存成功')).catch(err => {
            this.$httpError(err)
            this.abortDraggable()
          })
        }
      }

      if (e.hasOwnProperty('added')) {
        this.addRemoveGroupFlag = { to: { group_id: group > -1 ? group : null, order: e.added.newIndex }, inited: true }
      }

      if (e.hasOwnProperty('removed')) {
        this.$nextTick(() => {
          transferCITypeAttrIndex(this.CITypeId,
            {
              from: { attr_id: e.removed.element.id, group_id: group > -1 ? group : null },
              to: { group_id: this.addRemoveGroupFlag.to.group_id, order: this.addRemoveGroupFlag.to.order }
            }).then(res => this.$message.success('保存成功')).catch(err => {
            this.$httpError(err)
            this.abortDraggable()
          }).finally(() => {
            this.addRemoveGroupFlag = {}
          })
        })
      }
    },
    abortDraggable () {
      this.$nextTick(() => {
        this.$router.push({name: 'ci_type'})
      })
    },
    updatePropertyIndex () {
      const attributes = []    // 全部属性
      let attributeOrder = 0    // 属性组
      let groupOrder = 0   // 组排序
      const promises = [

      ]

      this.CITypeGroups.forEach(group => {
        const groupName = group.name

        let groupAttributes = []
        let groupUpdate = false
        group.order = groupOrder

        group.attributes.forEach(attribute => {
          groupAttributes.push(attribute.id)

          if (attribute.originGroupName !== group.name || attribute.originOrder !== attributeOrder) {
            attributes.push({ attr_id: attribute.id, order: attributeOrder })
            groupUpdate = true
          }
          attributeOrder++
        })

        groupAttributes = new Set(groupAttributes)
        if (group.originCount !== groupAttributes.size || groupUpdate || group.originOrder !== group.order) {
          promises.push(updateCITypeGroupById(group.id, { name: groupName, attributes: [...groupAttributes], order: groupOrder }))
        }
        groupOrder++
      })

      this.otherGroupAttributes.forEach(attribute => {
        if (attribute.originOrder !== attributeOrder) {
          console.log('this attribute:', attribute.name, 'old order', attribute.originOrder, 'new order', attributeOrder)
          attributes.push({ attr_id: attribute.id, order: attributeOrder })
        }

        attributeOrder++
      })

      if (attributes && attributes.length > 0) {
        promises.unshift(updateCITypeAttributesById(this.CITypeId, { attributes: attributes }))
      }

      const that = this
      Promise.all(promises)
        .then(values => {
          that.$message.success(`修改成功`)
          that.getCITypeGroupData()
          that.modalVisible = false
        })
        .catch(err => that.requestFailed(err))
    },
    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
      this.$message.error(`${msg}`)
    }
  },
  watch: {}

}
</script>

<style lang="less" scoped>
  .search {
    margin-bottom: 54px;
  }

  .fold {
    width: calc(100% - 216px);
    display: inline-block
  }

  .operator {
    margin-bottom: 18px;
  }

  .group-header {
    font-size: 1.15rem;
  }

  .property-item {
    width: calc(20% - 2rem);
    margin:0.5rem 0.8rem;
    border:1px solid #d9d9d9;
    border-radius: 5px;
    cursor: pointer;overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
    height: 2.5rem;
    line-height: 2.5rem;
  }

  .property-item:hover{
    border:1px dashed #40a9ff;
  }

  .property-item-empty {
    width: calc(100% - 10px);
    margin:0.5rem 0.8rem;
    border:1px dashed #d9d9d9;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
    height: 3.5rem;
    line-height: 3.5rem;
    color: #40a9ff;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
