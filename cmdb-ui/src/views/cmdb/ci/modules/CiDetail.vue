<template>
  <a-drawer
    width="80%"
    placement="left"
    @close="() => { visible = false }"
    :visible="visible"
    :wrapStyle="{height: 'calc(100% - 108px)', overflow: 'auto', paddingBottom: '108px'}"
  >
    <a-card
      :bordered="false"
      :tabList="tabList"
      :activeTabKey="activeTabKey"
      :selectedKeys="[typeId]"
      @tabChange="(key) => {this.activeTabKey = key}"
    >
      <div v-if="activeTabKey === 'tab_1'">
        <a-card
          type="inner"
          :title="group.name || $t('tip.other')"
          :key="group.name"
          v-for="group in attributeGroups"
        >
          <description-list title size="small">
            <div :key="attr.name" v-for="(attr, index) in group.attributes">
              <div v-if="index % 3 === 0" style="clear: both"></div>
              <description-list-item :term="attr.alias || attr.name">{{ ci[attr.name] }}</description-list-item>
            </div>
          </description-list>
        </a-card>
      </div>

      <div v-if="activeTabKey === 'tab_2'">
        <div v-for="parent in parentCITypes" :key="'ctr_' + parent.ctr_id">
          <a-card type="inner" :title="parent.alias || parent.name" v-if="firstCIs[parent.name]">
            <a-table
              rowKey="ci_id"
              size="middle"
              :columns="firstCIColumns[parent.id]"
              :dataSource="firstCIs[parent.name]"
              :pagination="false"
              :scroll="{x: '100%'}"
            ></a-table>
          </a-card>
        </div>
        <div v-for="child in childCITypes" :key="'ctr_' + child.ctr_id">
          <a-card type="inner" :title="child.alias || child.name" v-if="secondCIs[child.name]">
            <a-table
              rowKey="ci_id"
              size="middle"
              :columns="secondCIColumns[child.id]"
              :dataSource="secondCIs[child.name]"
              :pagination="false"
              :scroll="{x: '100%'}"
            ></a-table>
          </a-card>
        </div>
      </div>

      <div v-if="activeTabKey === 'tab_3'">
        <a-card type="inner" :bordered="false">
          <a-table
            bordered
            rowKey="hid"
            size="middle"
            :columns="historyColumns"
            :dataSource="ciHistory"
            :pagination="false"
            :scroll="{x: '100%'}"
          >
            <template
              slot="operate_type"
              slot-scope="operate_type"
            >{{ operate_type | operateTypeFilter }}</template>
          </a-table>
        </a-card>
      </div>
    </a-card>
  </a-drawer>
</template>

<script>
import i18n from '@/locales'
import DescriptionList from '@/components/DescriptionList'

import { getCITypeGroupById } from '@/api/cmdb/CIType'
import { getCITypeChildren, getCITypeParent } from '@/api/cmdb/CITypeRelation'
import { getFirstCIs, getSecondCIs } from '@/api/cmdb/CIRelation'
import { getCIHistory } from '@/api/cmdb/history'
import { getCIById } from '@/api/cmdb/ci'
import { notification } from 'ant-design-vue'

const DescriptionListItem = DescriptionList.Item

export default {
  components: {
    DescriptionList,
    DescriptionListItem
  },
  props: {
    typeId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      visible: false,
      parentCITypes: [],
      childCITypes: [],
      firstCIs: {},
      firstCIColumns: {},
      secondCIs: {},
      secondCIColumns: {},
      ci: {},

      attributeGroups: [],
      tabList: [
        {
          key: 'tab_1',
          tab: this.$t('ci.attribute')
        },
        {
          key: 'tab_2',
          tab: this.$t('ci.relation')
        },
        {
          key: 'tab_3',
          tab: this.$t('ci.history')
        }
      ],
      activeTabKey: 'tab_1',
      rowSpanMap: {},
      historyColumns: [
        {
          title: this.$t('ci.time'),
          dataIndex: 'created_at',
          key: 'created_at',
          customRender: (value, row, index) => {
            const obj = {
              children: value,
              attrs: {}
            }
            obj.attrs.rowSpan = this.rowSpanMap[index]
            return obj
          }
        },
        {
          title: this.$t('ci.user'),
          dataIndex: 'username',
          key: 'username',
          customRender: (value, row, index) => {
            const obj = {
              children: value,
              attrs: {}
            }
            obj.attrs.rowSpan = this.rowSpanMap[index]
            return obj
          }
        },
        {
          title: this.$t('tip.operate'),
          dataIndex: 'operate_type',
          key: 'operate_type',
          scopedSlots: { customRender: 'operate_type' }
        },
        {
          title: this.$t('ci.attribute'),
          dataIndex: 'attr_alias',
          key: 'attr_name'
        },
        {
          title: 'Old',
          dataIndex: 'old',
          key: 'old'
        },
        {
          title: 'New',
          dataIndex: 'new',
          key: 'new'
        }
      ],
      ciHistory: []
    }
  },
  filters: {
    operateTypeFilter (operateType) {
      const operateTypeMap = {
        '0': i18n.t('button.add'),
        '1': i18n.t('button.delete'),
        '2': i18n.t('button.update')
      }
      return operateTypeMap[operateType]
    }
  },
  methods: {
    create () {
      this.getAttributes()
      this.getCI()
      this.getFirstCIs()
      this.getSecondCIs()
      this.getParentCITypes()
      this.getChildCITypes()
      this.getCIHistory()
    },
    getAttributes () {
      getCITypeGroupById(this.typeId, { need_other: 1 })
        .then(res => {
          this.attributeGroups = res
        })
        .catch(e => {
          console.log(e)
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getCI () {
      getCIById(this.ciId)
        .then(res => {
          this.ci = res.ci
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },

    getFirstCIs () {
      getFirstCIs(this.ciId)
        .then(res => {
          const firstCIs = {}
          res.first_cis.forEach(item => {
            if (item.ci_type in firstCIs) {
              firstCIs[item.ci_type].push(item)
            } else {
              firstCIs[item.ci_type] = [item]
            }
          })
          this.firstCIs = firstCIs
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getSecondCIs () {
      getSecondCIs(this.ciId)
        .then(res => {
          const secondCIs = {}
          res.second_cis.forEach(item => {
            if (item.ci_type in secondCIs) {
              secondCIs[item.ci_type].push(item)
            } else {
              secondCIs[item.ci_type] = [item]
            }
          })
          this.secondCIs = secondCIs
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getParentCITypes () {
      getCITypeParent(this.typeId)
        .then(res => {
          this.parentCITypes = res.parents

          const firstCIColumns = {}
          res.parents.forEach(item => {
            const columns = []
            item.attributes.forEach(attr => {
              columns.push({ key: 'p_' + attr.id, dataIndex: attr.name, title: attr.alias })
            })
            firstCIColumns[item.id] = columns
          })
          this.firstCIColumns = firstCIColumns
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getChildCITypes () {
      getCITypeChildren(this.typeId)
        .then(res => {
          this.childCITypes = res.children

          const secondCIColumns = {}
          res.children.forEach(item => {
            const columns = []
            item.attributes.forEach(attr => {
              columns.push({ key: 'c_' + attr.id, dataIndex: attr.name, title: attr.alias })
            })
            secondCIColumns[item.id] = columns
          })
          this.secondCIColumns = secondCIColumns
        })
        .catch(e => {
          notification.error({
            message: e.response.data.message
          })
        })
    },
    getCIHistory () {
      getCIHistory(this.ciId)
        .then(res => {
          this.ciHistory = res
          const rowSpanMap = {}
          let startIndex = 0
          let startCount = 1
          res.forEach((item, index) => {
            if (index === 0) {
              return
            }
            if (res[index].record_id === res[startIndex].record_id) {
              startCount += 1
              rowSpanMap[index] = 0
              if (index === res.length - 1) {
                rowSpanMap[startIndex] = startCount
              }
            } else {
              rowSpanMap[startIndex] = startCount
              startIndex = index
              startCount = 1
              if (index === res.length - 1) {
                rowSpanMap[index] = 1
              }
            }
          })
          this.rowSpanMap = rowSpanMap
        })
        .catch(e => {
          console.log(e)
          notification.error({
            message: e.response.data.message
          })
        })
    }
  }
}
</script>

<style lange="less">
div.term {
  background-color: rgb(225, 238, 246);
  font-weight: 400;
  min-width: 120px !important;
  padding-left: 10px;
}
div.content {
  word-wrap: break-word;
  word-break: break-all;
  font-weight: bold;
  padding-left: 10px;
}
</style>
