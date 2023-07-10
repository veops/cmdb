<template>
  <div class="attr-ad" :style="{ height: `${windowHeight - 104}px` }">
    <div v-if="adCITypeList && adCITypeList.length">
      <a-tabs size="small" v-model="currentTab">
        <a-tab-pane v-for="item in adCITypeList" :key="item.adr_id">
          <a-space slot="tab">
            <span>{{ getADCITypeParam(item.adr_id) }}</span>
            <a-icon type="close-circle" @click="(e) => deleteADT(e, item)" />
          </a-space>
          <AttrADTabpane
            :ref="`attrAdTabpane_${item.adr_id}`"
            :currentTab="item.adr_id"
            :adrList="adrList"
            :adCITypeList="adCITypeList"
            :currentAdt="item"
            :ciTypeAttributes="ciTypeAttributes"
            :currentAdr="getADCITypeParam(item.adr_id, undefined, true)"
            @openEditDrawer="(data, type, adType) => openEditDrawer(data, type, adType)"
          />
        </a-tab-pane>
        <a-space
          @click="
            () => {
              $refs.adModal.open()
            }
          "
          slot="tabBarExtraContent"
          :style="{ cursor: 'pointer' }"
        >
          <ops-icon type="icon-xianxing-tianjia" :style="{ color: '#2F54EB' }" /><a>添加</a>
        </a-space>
      </a-tabs>
    </div>
    <a-empty
      v-else
      :image-style="{
        height: '60px',
      }"
    >
      <img slot="image" :src="require('@/assets/data_empty.png')" />
      <span slot="description"> 暂无数据 </span>
      <a-button
        @click="
          () => {
            $refs.adModal.open()
          }
        "
        type="primary"
        size="small"
        icon="plus"
        class="ops-button-primary"
      >
        添加
      </a-button>
    </a-empty>
    <ADModal ref="adModal" :CITypeId="CITypeId" @addPlugin="openEditDrawer(null, 'add', 'agent')" />
    <EditDrawer ref="editDrawer" :is_inner="false" @updateNotInner="updateNotInner" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ADModal from './adModal.vue'
import {
  getDiscovery,
  getCITypeDiscovery,
  deleteCITypeDiscovery,
  postCITypeDiscovery,
  deleteDiscovery,
} from '../../api/discovery'
import { getCITypeAttributesById } from '../../api/CITypeAttr'
import AttrADTabpane from './attrADTabpane.vue'
import EditDrawer from '../discovery/editDrawer.vue'

export default {
  name: 'AttrAutoDiscovery',
  components: { ADModal, AttrADTabpane, EditDrawer },
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
      adCITypeList: [],
      currentTab: '',
      deletePlugin: false,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
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
            this.$refs[`attrAdTabpane_${this.currentTab}`][0].init()
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
          this.$refs[`attrAdTabpane_${this.currentTab}`][0].init()
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
        this.adCITypeList = res.filter((item) => item.adr_id)
        if (res && res.length && !this.currentTab) {
          this.currentTab = res[0].adr_id
        }
        if (currentTab) {
          this.currentTab = currentTab
        }
      })
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
    async deleteADT(e, item) {
      e.preventDefault()
      e.stopPropagation()
      const that = this
      this.$confirm({
        title: `确认删除 【${this.getADCITypeParam(item.adr_id)}】`,
        content: (h) => (
          <div>
            <a-checkbox v-model={that.deletePlugin}>删除插件</a-checkbox>
          </div>
        ),
        onOk() {
          deleteCITypeDiscovery(item.id).then(async () => {
            if (that.currentTab === item.adr_id) {
              that.currentTab = ''
            }
            that.deletePlugin = false
            that.$message.success('删除成功！')
            that.getCITypeDiscovery()
            if (that.deletePlugin) {
              await deleteDiscovery(item.adr_id)
            }
          })
        },
        onCancel() {},
      })
    },
    openEditDrawer(data, type, adType) {
      this.$refs.editDrawer.open(data, type, adType)
    },
    async updateNotInner(adr) {
      const _idx = this.adCITypeList.findIndex((item) => item.adr_id === adr.id)
      if (_idx < 0) {
        await postCITypeDiscovery(this.CITypeId, { adr_id: adr.id, interval: 300 })
      }
      await this.getDiscovery()
      await this.getCITypeDiscovery()
      this.currentTab = adr.id
      this.$nextTick(() => {
        this.$refs[`attrAdTabpane_${this.currentTab}`][0].init()
      })
    },
  },
}
</script>

<style lang="less">
@import '~@/style/static.less';
.attr-ad {
  position: relative;
  padding: 0 12px;
  .attr-ad-header {
    width: 100%;
    display: inline-flex;
    height: 32px;
    line-height: 32px;
    padding-left: 10px;
    margin-bottom: 20px;
    border-left: 4px solid #custom_colors[color_1];
    font-size: 16px;
    color: rgba(0, 0, 0, 0.75);
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
