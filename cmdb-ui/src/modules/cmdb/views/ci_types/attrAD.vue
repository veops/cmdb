<template>
  <div class="attr-ad" :style="{ height: `${windowHeight - 130}px` }">
    <div v-if="adCITypeList && adCITypeList.length">
      <AttrADTabs
        :adCITypeList="adCITypeList"
        :currentTab="currentTab"
        :getADCITypeParam="getADCITypeParam"
        @changeTab="changeTab"
        @changeAlias="changeAlias"
        @deleteADT="deleteADT"
        @clickAdd="() => $refs.adModal.open()"
      />
      <AttrADTabpane
        :key="`attrAdTabpane_${currentTab}`"
        :ref="`attrAdTabpaneRef`"
        :adr_id="currentADData.adr_id"
        :CITypeId="CITypeId"
        :adrList="adrList"
        :adCITypeList="adCITypeList"
        :currentAdt="currentADData"
        :ciTypeAttributes="ciTypeAttributes"
        :currentAdr="getADCITypeParam(currentADData.adr_id, undefined, true)"
        @openEditDrawer="(data, type, adType) => openEditDrawer(data, type, adType)"
        @handleSave="saveTabpane"
      />
    </div>
    <a-empty
      v-else
      :image-style="{
        height: '60px',
      }"
    >
      <img slot="image" :src="require('@/assets/data_empty.png')" />
      <span slot="description"> {{ $t('noData') }} </span>
      <a-button
        @click="
          () => {
            $refs.adModal.open()
          }
        "
        type="primary"
        size="small"
        icon="plus"
      >
        {{ $t('add') }}
      </a-button>
    </a-empty>
    <ADModal
      ref="adModal"
      :CITypeId="CITypeId"
      @pushCITypeList="pushCITypeList"
      @addPlugin="openEditDrawer(null, 'add', 'plugin')"
    />
    <EditDrawer ref="editDrawer" :is_inner="false" @updateNotInner="updateNotInner" />
  </div>
</template>

<script>
import _ from 'lodash'
import { mapState } from 'vuex'
import {
  getDiscovery,
  getCITypeDiscovery,
  deleteCITypeDiscovery,
  deleteDiscovery,
  putCITypeDiscovery
} from '../../api/discovery'
import { getCITypeAttributesById } from '../../api/CITypeAttr'

import ADModal from './adModal.vue'
import AttrADTabpane from './attrADTabpane.vue'
import EditDrawer from '../discovery/editDrawer.vue'
import AttrADTabs from './attrADTabs.vue'

export default {
  name: 'AttrAutoDiscovery',
  components: {
    ADModal,
    AttrADTabpane,
    EditDrawer,
    AttrADTabs
  },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      ciTypeAttributes: [],
      adrList: [],
      serviceCITYpeList: [],
      clientCITypeList: [],
      currentTab: '',
      deletePlugin: false,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    currentADData() {
      return this?.adCITypeList?.find((item) => item?.id === this?.currentTab) ?? {}
    },
    adCITypeList() {
      const uniqueArray = _.differenceBy(this.clientCITypeList, this.serviceCITYpeList, 'id')
      return [...this.serviceCITYpeList, ...uniqueArray]
    }
  },
  provide() {
    return {
      getCITypeDiscovery: this.getCITypeDiscovery,
    }
  },
  watch: {
    currentTab: {
      handler() {
        if (this.currentTab) {
          this.$nextTick(() => {
            this.$refs[`attrAdTabpaneRef`].init()
          })
        }
      },
    },
  },
  async created() {
    await this.getDiscovery()
    await this.getCITypeDiscovery()
    getCITypeAttributesById(this.CITypeId).then((res) => {
      this.ciTypeAttributes = res.attributes.map((item) => {
        return { ...item, value: item.name, label: item.name }
      })
      if (this.currentTab) {
        this.$nextTick(() => {
          this.$refs[`attrAdTabpaneRef`].init()
        })
      }
    })
  },
  methods: {
    async getDiscovery() {
      await getDiscovery().then((res) => {
        this.adrList = res
      })
    },
    async getCITypeDiscovery(currentTab) {
      await getCITypeDiscovery(this.CITypeId).then((res) => {
        const serviceCITYpeList = res.filter((item) => item.adr_id)
        serviceCITYpeList.forEach((item) => {
          const _find = this.adrList.find((adr) => adr.id === item.adr_id)
          item.icon = _find?.option?.icon || {}
        })

        this.serviceCITYpeList = serviceCITYpeList
        this.$nextTick(() => {
          if (this.adCITypeList && this.adCITypeList.length && !this.currentTab) {
            this.currentTab = this.adCITypeList[0].id
          }
          if (currentTab) {
            this.currentTab = currentTab
          }
        })
      })
    },
    pushCITypeList(list) {
      list.forEach((item) => {
        const _find = this.adrList.find((adr) => adr.id === item.adr_id)
        item.icon = _find?.option?.icon || {}
      })
      this.$set(this, 'clientCITypeList', [
        ...this.clientCITypeList,
        ...list
      ])
      this.currentTab = list[0].id
    },
    getADCITypeParam(adr_id, params = 'name', isAll = false) {
      const _find = this.adrList.find((item) => item.id === adr_id)
      if (_find) {
        if (isAll) {
          return _find
        }
        return _find[`${params}`]
      }
    },
    async deleteADT(item) {
      const that = this
      const is_plugin = this.getADCITypeParam(item.adr_id, 'is_plugin')

      this.$confirm({
        title: that.$t('cmdb.ciType.confirmDeleteADT', { pluginName: `${item?.extra_option?.alias || this.getADCITypeParam(item.adr_id)}` }),
        content: (h) => {
          if (!is_plugin) {
            return ''
          }
          return (
            <div>
              <a-checkbox
                v-model={that.deletePlugin}
              >
                {that.$t('cmdb.ciType.deletePlugin')}
              </a-checkbox>
            </div>
          )
        },
        onOk () {
          if (item.isClient) {
            const adtIndex = that.clientCITypeList.findIndex((listItem) => listItem.id === item.id)
            if (adtIndex !== -1) {
              that.clientCITypeList.splice(adtIndex, 1)
              that.currentTab = that?.adCITypeList?.[0]?.id ?? ''

              if (is_plugin && that.deletePlugin) {
                that.deleteDiscovery(item.adr_id)
              }
            }
          } else {
            deleteCITypeDiscovery(item.id).then(async () => {
              if (that.currentTab === item.id) {
                that.currentTab = ''
              }
              that.$message.success(that.$t('deleteSuccess'))
              that.getCITypeDiscovery()
              if (is_plugin && that.deletePlugin) {
                that.deleteDiscovery(item.adr_id)
              }
              that.deletePlugin = false
            })
          }
        },
        onCancel() {
          that.deletePlugin = false
        },
      })
    },

    deleteDiscovery(id) {
      deleteDiscovery(id).finally(async () => {
        this.deletePlugin = false
        await this.getDiscovery()
      })
    },

    openEditDrawer(data, type, adType) {
      this.$refs.editDrawer.open(data, type, adType)
    },
    async updateNotInner(adr) {
      const _idx = this.adCITypeList.findIndex((item) => item.adr_id === adr.id)
      await this.getDiscovery()
      if (_idx < 0) {
        const ciType = {
          adr_id: adr.id,
          id: new Date().getTime(),
          extra_option: {
            alias: ''
          },
          isClient: true,
        }
        this.pushCITypeList([ciType])
      }
      this.$nextTick(() => {
        this.$refs[`attrAdTabpaneRef`].init()
      })
    },

    changeTab(id) {
      console.log('changeTab', id)
      this.currentTab = id
    },

    changeAlias({ id, value, isClient }) {
      if (isClient) {
        const adtIndex = this.clientCITypeList.findIndex((item) => item.id === id)
        this.clientCITypeList[adtIndex].extra_option.alias = value
      } else {
        const adtIndex = this.adCITypeList.findIndex((item) => item.id === id)
        const oldExtraOption = this.adCITypeList?.[adtIndex]?.extra_option

        const params = {
          extra_option: {
            ...(oldExtraOption || {}),
            alias: value
          }
        }
        putCITypeDiscovery(id, params).then(async () => {
          this.$message.success(this.$t('saveSuccess'))
          await this.getCITypeDiscovery()
        })
      }
    },

    saveTabpane(id) {
      const adtIndex = this.clientCITypeList.findIndex((listItem) => listItem.id === this.currentTab)
      if (adtIndex !== -1) {
        this.clientCITypeList.splice(adtIndex, 1)
      }
      this.getCITypeDiscovery(id)
    }
  },
}
</script>

<style lang="less">
.attr-ad {
  position: relative;
  padding: 0 20px;

  .attr-ad-header {
    width: 100%;
    display: inline-flex;
    height: 32px;
    line-height: 32px;
    padding-left: 10px;
    margin-bottom: 20px;
    border-left: 4px solid @primary-color;
    font-size: 16px;
    color: rgba(0, 0, 0, 0.75);
    margin-top: 30px;
  }

  .attr-ad-header-margin {
    margin-bottom: 0px;
  }

  .attr-ad-footer {
    width: 60%;
    text-align: right;
    margin-bottom: 10px;
  }
}
</style>

<style lang="less">
.attr-ad {
  .ant-empty {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  &:not(.ant-tabs-tab-active).ant-tabs-tab {
    color: #a5a9bc;
  }
  .ant-form-item {
    margin-bottom: 8px;
  }
}
</style>
