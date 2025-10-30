<template>
  <div class="setting-discovery">
    <div v-if="!isSelected" class="setting-discovery-header">
      <a-input-search
        class="setting-discovery-search"
        :placeholder="$t('cmdb.ad.pluginSearchTip')"
        @search="onSearchDiscovery"
      />
      <div class="setting-discovery-radio">
        <div
          v-for="{ type, label } in typeCategory"
          :key="type"
          :class="['setting-discovery-radio-item', radioKey === type ? 'setting-discovery-radio-item_active' : '']"
          @click="changeRadio(type)"
        >
          {{ label }}
        </div>
      </div>

      <div class="setting-discovery-header-action">
        <a-upload
          name="file"
          :multiple="false"
          accept=".json"
          :fileList="[]"
          :beforeUpload="beforeUpload"
        >
          <a-button
            type="primary"
            class="ops-button-ghost"
            ghost
          >
            <a-icon type="upload" />
            {{ $t('cmdb.ad.upload') }}
          </a-button>
        </a-upload>
        <a-button
          type="primary"
          class="ops-button-ghost"
          ghost
          @click="download"
        >
          <a-icon type="download" />
          {{ $t('cmdb.ad.download') }}
        </a-button>
      </div>
    </div>
    <div
      class="setting-discovery-body"
      :style="{ height: !isSelected ? `${windowHeight - 160}px` : '' }"
    >
      <template v-if="!showNullData">
        <div v-for="{ type, label } in typeCategory" :key="type">
          <template v-if="filterCategoryChildren[type] && (filterCategoryChildren[type].children.length || (showAddPlugin && type === DISCOVERY_CATEGORY_TYPE.PLUGIN))">
            <div class="type-header">
              <div>{{ label }}</div>
            </div>
            <a-row type="flex" justify="start">
              <DiscoveryCard
                v-for="rule in filterCategoryChildren[type].children"
                :key="rule.id"
                :rule="rule"
                :isSelected="isSelected"
                @editRule="handleOpenEditDrawer(rule, 'edit', type)"
                @deleteRule="deleteRule(rule)"
                @openAccountConfig="openAccountConfig(rule)"
              />
              <div
                v-if="showAddPlugin && type === DISCOVERY_CATEGORY_TYPE.PLUGIN"
                class="setting-discovery-add"
                @click="handleOpenEditDrawer(null, 'add', DISCOVERY_CATEGORY_TYPE.PLUGIN)"
              >
                <a-icon class="setting-discovery-add-icon" type="plus-circle" />
                <span class="setting-discovery-add-text">
                  {{ $t('cmdb.ad.addPlugin') }}
                </span>
              </div>
            </a-row>
          </template>
        </div>
      </template>
      <div class="setting-discovery-empty" v-else>
        <img class="setting-discovery-empty-img" :src="require(`@/assets/data_empty.png`)" />
        <p class="setting-discovery-empty-text">{{ $t('noData') }}</p>
      </div>
    </div>
    <EditDrawer ref="editDrawer" :isDiscoveryPage="true" />
    <AccountConfig ref="accountConfig"/>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'
import { getDiscovery, deleteDiscovery } from '../../api/discovery'
import { DISCOVERY_CATEGORY_TYPE } from './constants.js'
import DiscoveryCard from './discoveryCard.vue'
import EditDrawer from './editDrawer.vue'
import AccountConfig from './accountConfig/index.vue'

export default {
  name: 'AutoDiscovery',
  components: {
    DiscoveryCard,
    EditDrawer,
    AccountConfig
  },
  props: {
    isSelected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      typeCategoryChildren: {},
      DISCOVERY_CATEGORY_TYPE,
      radioKey: '',
      searchValue: '',
      accountConfigVisible: false,
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    typeCategory() {
      return [
        {
          type: DISCOVERY_CATEGORY_TYPE.HTTP,
          label: this.$t('cmdb.ad.http'),
        },
        {
          type: DISCOVERY_CATEGORY_TYPE.PRIVATE_CLOUD,
          label: this.$t('cmdb.ad.privateCloud'),
        },
        {
          type: DISCOVERY_CATEGORY_TYPE.AGENT,
          label: this.$t('cmdb.ad.agent'),
        },
        {
          type: DISCOVERY_CATEGORY_TYPE.COMPONENT,
          label: this.$t('cmdb.ad.component'),
        },
        {
          type: DISCOVERY_CATEGORY_TYPE.SNMP,
          label: this.$t('cmdb.ad.snmp'),
        },
        {
          type: DISCOVERY_CATEGORY_TYPE.PLUGIN,
          label: this.$t('cmdb.ad.plugin'),
        }
      ]
    },
    filterCategoryChildren() {
      const _typeCategoryChildren = _.cloneDeep(this.typeCategoryChildren)
      const _filterCategoryChildren = Object.values(_typeCategoryChildren).reduce((obj, category) => {
        if (this.radioKey === '' || category.type === this.radioKey) {
          category.children = category.children.filter((item) => {
            return item?.name?.indexOf(this.searchValue) !== -1
          })
          obj[category.type] = category
        }
        return obj
      }, {})

      return _filterCategoryChildren
    },
    showNullData() {
      const showCount = Object.values(this.filterCategoryChildren).reduce((acc, item) => {
        return acc + (item?.children?.length || 0)
      }, 0)
      return showCount === 0
    },
    showAddPlugin() {
      return !this.isSelected && this.searchValue === ''
    }
  },
  provide() {
    return {
      getDiscovery: this.getDiscovery,
    }
  },
  mounted() {
    this.getDiscovery()
  },
  methods: {
    getDiscovery() {
      const _typeCategoryChildren = {
        [DISCOVERY_CATEGORY_TYPE.HTTP]: {
          type: DISCOVERY_CATEGORY_TYPE.HTTP,
          children: []
        },
        [DISCOVERY_CATEGORY_TYPE.PRIVATE_CLOUD]: {
          type: DISCOVERY_CATEGORY_TYPE.PRIVATE_CLOUD,
          children: []
        },
        [DISCOVERY_CATEGORY_TYPE.AGENT]: {
          type: DISCOVERY_CATEGORY_TYPE.AGENT,
          children: []
        },
        [DISCOVERY_CATEGORY_TYPE.COMPONENT]: {
          type: DISCOVERY_CATEGORY_TYPE.COMPONENT,
          children: []
        },
        [DISCOVERY_CATEGORY_TYPE.SNMP]: {
          type: DISCOVERY_CATEGORY_TYPE.SNMP,
          children: []
        },
        [DISCOVERY_CATEGORY_TYPE.PLUGIN]: {
          type: DISCOVERY_CATEGORY_TYPE.PLUGIN,
          children: []
        }
      }
      getDiscovery().then((res) => {
        this.typeCategory.forEach(({ type }) => {
          let categoryChildren = []
          switch (type) {
            case DISCOVERY_CATEGORY_TYPE.PRIVATE_CLOUD:
              categoryChildren = res.filter((list) => list?.option?.category === 'private_cloud' && list?.type === 'http')
              break
            case DISCOVERY_CATEGORY_TYPE.HTTP:
              categoryChildren = res.filter((list) => list?.option?.category !== 'private_cloud' && list?.type === 'http')
              break
            case DISCOVERY_CATEGORY_TYPE.PLUGIN:
              categoryChildren = res.filter((list) => list.is_plugin)
              break
            case DISCOVERY_CATEGORY_TYPE.AGENT:
              categoryChildren = res.filter((list) => !list.is_plugin && list.type === type)
              break
            default:
              categoryChildren = res.filter((list) => list.type === type)
              break
          }
          _typeCategoryChildren[`${type}`]['children'] = categoryChildren
        })
        this.$set(this, 'typeCategoryChildren', _typeCategoryChildren)
      })
    },
    handleOpenEditDrawer(data, type, autoType) {
      this.$refs.editDrawer.open(data, type, autoType)
    },
    deleteRule(rule) {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('confirmDelete', { name: `${rule.name}` }),
        onOk() {
          deleteDiscovery(rule.id).then(() => {
            that.$message.success(that.$t('deleteSuccess'))
            that.getDiscovery()
          })
        },
      })
    },
    download() {
      const x = new XMLHttpRequest()
      const that = this
      const base_url = process.env.VUE_APP_API_BASE_URL || '/api'
      x.open('GET', `${base_url}/v0.1/adr/template/export/file`, true)
      x.responseType = 'blob'
      x.onload = function(e) {
        const url = window.URL.createObjectURL(x.response)
        const a = document.createElement('a')
        a.href = url
        a.download = that.$t('cmdb.ad.rule')
        a.click()
      }
      x.send()
    },
    beforeUpload(file) {
      const formData = new FormData()
      formData.append('file', file)
      const that = this
      var xhr = new XMLHttpRequest()
      const base_url = process.env.VUE_APP_API_BASE_URL || '/api'
      xhr.open('POST', `${base_url}/v0.1/adr/template/import/file`)
      xhr.onreadystatechange = function() {
        const state = Number(xhr.readyState)
        if (state === 4) {
          if (xhr.status === 200) {
            that.$message.success(that.$t('uploadSuccess'))
            that.getDiscovery()
          }
        }
      }
      xhr.ontimeout = function() {
        that.$httpError(that.$t('cmdb.ad.timeout'))
      }

      xhr.send(formData)
      return false
    },

    onSearchDiscovery(v) {
      this.searchValue = v
    },

    changeRadio(key) {
      this.radioKey = key === this.radioKey ? '' : key
    },

    openAccountConfig(rule) {
      this.$refs.accountConfig.open(rule)
    }
  },
}
</script>

<style lang="less" scoped>
.setting-discovery {
  &-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;

    &-action {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;

      &-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border: solid 1px @primary-color_8;
        background-color: #F4F9FF;
        color: @link-color;
      }
    }
  }

  &-search {
    width: 280px;
    flex-shrink: 0;

    /deep/ .ant-input {
      border-radius: 6px;
      border: 1px solid #e8eaed;
      transition: all 0.2s ease;

      &:hover {
        border-color: #c3cdd7;
      }

      &:focus {
        border-color: @primary-color;
        box-shadow: 0 0 0 2px fade(@primary-color, 10%);
      }
    }
  }

  &-radio {
    display: flex;
    align-items: center;
    margin-left: 16px;
    gap: 8px;
    overflow: auto;
    margin-right: 16px;

    &-item {
      padding: 6px 16px;
      font-size: 14px;
      font-weight: 400;
      line-height: 22px;
      cursor: pointer;
      flex-shrink: 0;
      border-radius: 6px;
      transition: all 0.2s ease;
      color: @text-color_2;

      &:hover {
        color: @primary-color;
        background-color: fade(@primary-color, 8%);
      }

      &_active {
        background-color: @primary-color;
        color: #fff;
        font-weight: 500;
      }
    }
  }

  &-body {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    padding: 24px;
    overflow: auto;

    .setting-discovery-add {
      height: 105px;
      width: 180px;
      border-radius: 6px;
      border: 2px dashed #d9d9d9;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s ease;
      background: #fafafa;

      &:hover {
        border-color: @primary-color;
        background: fade(@primary-color, 5%);

        .setting-discovery-add-icon {
          color: @primary-color;
          transform: scale(1.1);
        }
      }

      &-icon {
        color: #bfbfbf;
        font-size: 24px;
        transition: all 0.3s ease;
      }

      &-text {
        color: @text-color_2;
        font-size: 13px;
        font-weight: 400;
        margin-top: 8px;
      }
    }

    .setting-discovery-empty {
      text-align: center;
      padding: 40px 0;

      &-text {
        margin-top: 16px;
        color: @text-color_3;
        font-size: 14px;
      }

      &-img {
        width: 120px;
        opacity: 0.6;
      }
    }
  }

  .type-header {
    width: 100%;
    display: flex;
    align-items: center;
    height: 40px;
    padding-left: 12px;
    margin-bottom: 20px;
    border-left: 3px solid @primary-color;
    background: linear-gradient(90deg, fade(@primary-color, 5%) 0%, transparent 100%);
    border-radius: 0 4px 4px 0;

    > div {
      font-weight: 600;
      font-size: 15px;
      color: @text-color_1;
    }
  }
}
</style>
