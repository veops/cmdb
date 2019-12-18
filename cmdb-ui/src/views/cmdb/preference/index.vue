<template>
  <a-card>
    <div class="card-list" ref="content">
      <a-list :grid="{gutter: 24, lg: 4, md: 3, sm: 2, xs: 1}" :dataSource="citypeData.ci_types">
        <a-list-item slot="renderItem" slot-scope="item" v-if="!item.is_attached && item.enabled">
          <template>
            <a-card :hoverable="true">
              <a-card-meta>
                <a-avatar
                  class="card-avatar"
                  slot="avatar"
                  :src="item.avatar"
                  :size="32"
                  :style="item.is_subscribed ? 'color: #FFF; backgroundColor: green' : 'color: #FFF; backgroundColor: lightgrey'"
                >{{ item.avatar || item.name[0].toUpperCase() }}</a-avatar>
                <span class="margin-bottom: 3px" slot="title">{{ item.alias || item.name }}</span>
                <span
                  :class="item.is_subscribed?'subscribe-success':'unsubscribe'"
                  slot="title"
                >{{ item.is_subscribed ? "已订阅" : "未订阅" }}</span>
              </a-card-meta>
              <template class="ant-card-actions" slot="actions">
                <a :disabled="!item.is_subscribed" @click="unsubscribe(item.id)">取消</a>
                <a @click="showDrawer(item.id, item.alias || item.name)">订阅</a>
              </template>
            </a-card>
          </template>
        </a-list-item>
      </a-list>

      <template>
        <div>
          <a-drawer
            :title="'订阅模型: ' + typeName"
            :width="600"
            @close="onClose"
            :visible="visible"
            :wrapStyle="{height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px'}"
          >
            <a-alert message="既可以定义树形视图, 也可以订阅资源视图, 资源视图会在SideBar单独呈现" type="info" showIcon />
            <a-divider>
              树形视图
              <span
                v-if="treeSubscribed"
                style="font-weight: 500; font-size: 12px; color: green"
              >已订阅</span>
              <span style="font-weight: 500; font-size: 12px; color: red" v-else>未订阅</span>
            </a-divider>
            <a-select
              ref="tree"
              mode="multiple"
              placeholder="- - 目录层级的选择 - -"
              :value="treeViews"
              style="width: 100%"
              @change="handleTreeSub"
            >
              <a-select-option v-for="attr in attrList" :key="attr.title">{{ attr.title }}</a-select-option>
            </a-select>
            <a-button
              @click="subTreeSubmit"
              type="primary"
              :style="{float: 'right', marginTop: '10px'}"
            >订阅</a-button>
            <br />
            <br />

            <a-divider>
              资源视图
              <span
                v-if="instanceSubscribed"
                style="font-weight: 500; font-size: 12px; color: green"
              >已订阅</span>
              <span style="font-weight: 500; font-size: 12px; color: red" v-else>未订阅</span>
            </a-divider>
            <template>
              <a-transfer
                :dataSource="attrList"
                :showSearch="true"
                :listStyle="{
                  width: '230px',
                  height: '500px',
                }"
                :titles="['未选属性','已选属性']"
                :render="item=>item.title"
                :targetKeys="selectedAttrList"
                @change="handleChange"
                @search="handleSearch"
              >
                <span slot="notFoundContent">没数据</span>
              </a-transfer>
            </template>
            <div
              :style="{
                position: 'absolute',
                left: 0,
                bottom: 0,
                width: '100%',
                borderTop: '1px solid #e9e9e9',
                padding: '10px 16px',
                background: '#fff',
                textAlign: 'right',
              }"
            >
              <a-button :style="{marginRight: '8px'}" @click="onClose">取消</a-button>
              <a-button @click="subInstanceSubmit" type="primary">订阅</a-button>
            </div>
          </a-drawer>
        </div>
      </template>
    </div>
  </a-card>
</template>

<script>
import router, { resetRouter } from '@/router'
import store from '@/store'
import { notification } from 'ant-design-vue'
import { getCITypes } from '@/api/cmdb/CIType'
import {
  getPreference,
  subscribeCIType,
  getSubscribeAttributes,
  getSubscribeTreeView,
  subscribeTreeView
} from '@/api/cmdb/preference'
import { getCITypeAttributesByName } from '@/api/cmdb/CITypeAttr'
import { Promise } from 'q'

export default {
  data () {
    return {
      visible: false,
      typeId: null,
      typeName: null,
      instanceSubscribed: false,
      treeSubscribed: false,
      citypeData: {},
      attrList: [],
      selectedAttrList: [],
      treeViews: []
    }
  },
  created () {
    this.getCITypes()
  },
  methods: {
    getCITypes () {
      getCITypes().then(res => {
        getPreference(true, true).then(pref => {
          pref.forEach(item => {
            res.ci_types.forEach(ciType => {
              if (item.id === ciType.id) {
                ciType.is_subscribed = true
              }
            })
          })
          this.citypeData = res
        })
      })
    },
    unsubscribe (citypeId) {
      const that = this
      this.$confirm({
        title: '警告',
        content: '真的要取消订阅吗 ?',
        onOk () {
          const unsubCIType = subscribeCIType(citypeId, '')
          const unsubTree = subscribeTreeView(citypeId, '')
          Promise.all([unsubCIType, unsubTree])
            .then(() => {
              notification.success({
                message: '取消成功'
              })
              that.resetRoute()
            })
            .catch(e => {
              console.log(e)
              notification.error({
                message: e.response.data.message
              })
            })
        },
        onCancel () {}
      })
    },
    // 显示右边的弹出框
    showDrawer (typeId, typeName) {
      this.typeId = typeId
      this.typeName = typeName
      this.getAttrList()
      this.getTreeView(typeId)
    },
    onClose () {
      this.visible = false
      this.resetRoute()
    },
    getAttrList () {
      getCITypeAttributesByName(this.typeId).then(res => {
        const attributes = res.attributes
        getSubscribeAttributes(this.typeId).then(_res => {
          const attrList = []
          const selectedAttrList = []
          const subAttributes = _res.attributes
          this.instanceSubscribed = _res.is_subscribed
          subAttributes.forEach(item => {
            selectedAttrList.push(item.id.toString())
          })

          attributes.forEach(item => {
            const data = {
              key: item.id.toString(),
              title: item.alias || item.name
            }
            attrList.push(data)
          })

          this.attrList = attrList
          this.selectedAttrList = selectedAttrList
          this.visible = true
        })
      })
    },
    handleTreeSub (values) {
      this.treeViews = values
    },
    // 处理点击改变事件
    handleChange (targetKeys, direction, moveKeys) {
      this.selectedAttrList = targetKeys
    },
    handleSearch (dir, value) {},
    // 处理提交事件
    subInstanceSubmit () {
      subscribeCIType(this.typeId, this.selectedAttrList)
        .then(res => {
          notification.success({
            message: '订阅成功'
          })
          this.resetRoute()
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getTreeView (typeId) {
      const that = this
      this.treeViews = []
      getSubscribeTreeView()
        .then(res => {
          let hasMatch = false
          res.forEach(item => {
            if (item.type_id === typeId) {
              hasMatch = true
              const levels = []
              if (item.levels && item.levels.length >= 1) {
                item.levels.forEach(level => {
                  levels.push(level.alias)
                })
              }
              if (levels.length > 0) {
                that.treeSubscribed = true
              } else {
                that.treeSubscribed = false
              }
              that.treeViews = levels
            }
          })
          if (!hasMatch) {
            that.treeSubscribed = false
          }
        })
        .catch(e => {
          console.log(e)
          notification.error({
            message: e.response.data.message
          })
        })
    },
    subTreeSubmit () {
      subscribeTreeView(this.typeId, this.treeViews)
        .then(res => {
          notification.success({
            message: '订阅成功'
          })
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },

    resetRoute () {
      resetRouter()
      const roles = store.getters.roles
      store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
        router.addRoutes(store.getters.addRouters)
        this.getCITypes()
      })
    }
  }
}
</script>

<style lang="less" scoped>
.card-avatar {
  width: 48px;
  height: 48px;
  border-radius: 48px;
}

.ant-card-actions {
  background: #f7f9fa;
  li {
    float: left;
    text-align: center;
    margin: 12px 0;
    color: rgba(0, 0, 0, 0.45);
    width: 50%;

    &:not(:last-child) {
      border-right: 1px solid #e8e8e8;
    }

    a {
      color: rgba(0, 0, 0, 0.45);
      line-height: 22px;
      display: inline-block;
      width: 100%;
      &:hover {
        color: #1890ff;
      }
    }
  }
}

.new-btn {
  background-color: #fff;
  border-radius: 2px;
  width: 100%;
  height: 188px;
}

.meta-content {
  position: relative;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  height: 64px;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
.subscribe-success {
  float: right;
  color: green;
  font-size: 12px;
  font-weight: 500;
}
.unsubscribe {
  float: right;
  color: gray;
  font-size: 12px;
  font-weight: 300;
}
</style>
