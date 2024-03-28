<template>
  <div class="setting-discovery">
    <div :style="{ textAlign: 'right' }">
      <a-space v-if="!isSelected">
        <a-upload name="file" :multiple="false" accept=".json" :fileList="[]" :beforeUpload="beforeUpload">
          <a><a-icon type="upload" />{{ $t('cmdb.ad.upload') }}</a>
        </a-upload>
        <a @click="download"><a-icon type="download" />{{ $t('cmdb.ad.download') }}</a>
      </a-space>
    </div>
    <div v-for="{ type, label } in typeCategory" :key="type">
      <div class="type-header">
        <div>{{ label }}</div>
        <a-space v-if="!isSelected && type === 'agent'">
          <a @click="handleOpenEditDrawer(null, 'add', type)"><ops-icon type="icon-xianxing-tianjia"/></a>
        </a-space>
      </div>
      <a-row type="flex" justify="start">
        <DiscoveryCard
          @editRule="handleOpenEditDrawer(rule, 'edit', type)"
          @deleteRule="deleteRule(rule)"
          v-for="rule in typeCategoryChildren[type]"
          :key="rule.id"
          :rule="rule"
          :isSelected="isSelected"
        />
      </a-row>
    </div>
    <EditDrawer ref="editDrawer" />
  </div>
</template>

<script>
import { getDiscovery, deleteDiscovery } from '../../api/discovery'
import DiscoveryCard from './discoveryCard.vue'
import EditDrawer from './editDrawer.vue'
export default {
  name: 'AutoDiscovery',
  components: { DiscoveryCard, EditDrawer },
  props: {
    isSelected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      typeCategoryChildren: { agent: [], snmp: [], http: [] },
    }
  },
  computed: {
    typeCategory() {
      return [
        {
          type: 'agent',
          label: this.$t('cmdb.ad.agent'),
        },
        {
          type: 'snmp',
          label: this.$t('cmdb.ad.snmp'),
        },
        {
          type: 'http',
          label: this.$t('cmdb.ad.http'),
        },
      ]
    },
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
      const _typeCategoryChildren = { agent: [], snmp: [], http: [] }
      getDiscovery().then((res) => {
        this.typeCategory.forEach(({ type }) => {
          const _filterData = res.filter((list) => list.type === type && list.is_inner)
          _typeCategoryChildren[`${type}`] = _filterData
        })
        this.typeCategoryChildren = _typeCategoryChildren
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
      x.open('GET', `/api/v0.1/adr/template/export/file`, true)
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
      xhr.open('POST', `/api/v0.1/adr/template/import/file`)
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
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.setting-discovery {
  background-color: #fff;
  padding: 20px;
  border-radius: @border-radius-box;
  .type-header {
    width: 100%;
    display: inline-flex;
    height: 32px;
    line-height: 32px;
    padding-left: 10px;
    margin-bottom: 20px;
    border-left: 4px solid #custom_colors[color_1];
    justify-content: space-between;
    > div {
      font-weight: bold;
    }
  }
}
</style>
