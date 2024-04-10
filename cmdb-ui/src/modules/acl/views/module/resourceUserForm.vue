<template>
  <CustomDrawer
    width="800px"
    placement="left"
    :title="$t('acl.resourceList')"
    @close="handleCancel"
    :visible="visible"
    :hasFooter="false"
  >
    <a-form-item :label="$t('acl.resourceType')" :label-col="{ span: 4 }" :wrapper-col="{ span: 14 }">
      <a-select v-model="typeSelected" style="width:100%" @change="refresh">
        <a-select-option v-for="type in resourceTypes" :value="type.id" :key="type.id">{{ type.name }}</a-select-option>
      </a-select>
    </a-form-item>
    <ops-table
      size="mini"
      stripe
      class="ops-stripe-table"
      :max-height="`${windowHeight - 180}px`"
      :data="records"
      ref="rTable"
    >
      <vxe-column
        field="name"
        :title="$t('acl.resourceName')"
        width="30%"
        :filters="[{ data: '' }]"
        :filter-method="filterNameMethod"
        :filter-recover-method="filterNameRecoverMethod"
      >
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-tooltip :title="$t('acl.copyResource')">
            <a-icon @click="copyResourceName" class="resource-user-form-copy" theme="filled" type="copy" />
          </a-tooltip>
        </template>
        <template #filter="{ $panel, column }">
          <template v-for="(option, index) in column.filters">
            <input
              class="my-input"
              type="type"
              :key="index"
              v-model="option.data"
              @input="$panel.changeOption($event, !!option.data, option)"
              @keyup.enter="$panel.confirmFilter()"
              :placeholder="$t('acl.pressEnter')"
            />
          </template>
        </template>
      </vxe-column>
      <vxe-column field="permissions" :title="$t('acl.permissionList')" width="70%">
        <template #default="{row}">
          <a-tag color="cyan" v-for="(r, index) in row.permissions" :key="index">{{ r }}</a-tag>
        </template>
      </vxe-column>
    </ops-table>
  </CustomDrawer>
</template>
<script>
import { mapState } from 'vuex'
import { searchPermResourceByRoleId } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'

export default {
  name: 'ResourceUserForm',
  data() {
    return {
      visible: false,
      rid: 0,
      records: [],
      resourceTypes: [],
      typeSelected: null,
      columnSearchText: {
        name: '',
      },
      filterName: '',
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  mounted() {
    this.loadResourceTypes()
  },
  methods: {
    loadUserResource(record) {
      this.visible = true
      this.rid = record.id
      this.refresh()
    },
    loadResourceTypes() {
      this.resourceTypes = []
      const appId = this.$route.name.split('_')[0]
      searchResourceType({ app_id: appId }).then((res) => {
        this.resourceTypes = res.groups
        if (res.groups && res.groups.length > 0) {
          this.typeSelected = res.groups[0].id
          console.log(this.typeSelected)
        } else {
          this.typeSelected = null
        }
      })
    },
    handleOk() {
      this.visible = false
    },
    refresh() {
      if (this.typeSelected) {
        searchPermResourceByRoleId(this.rid, {
          resource_type_id: this.typeSelected,
          app_id: this.$route.name.split('_')[0],
        }).then((res) => {
          this.records = res.resources
        })
      }
    },
    handleCancel() {
      this.visible = false
    },
    filterNameMethod({ option, row }) {
      this.filterName = option.data
      return row.name.toLowerCase().includes(option.data.toLowerCase())
    },
    filterNameRecoverMethod({ option }) {
      this.filterName = ''
      option.data = ''
    },
    copyResourceName() {
      const val = this.records
        .filter((item) => item.name.toLowerCase().includes(this.filterName.toLowerCase()))
        .map((item) => item.name)
        .join('\n')

      this.copy(val, () => {
        this.$message.success(this.$t('copySuccess'))
      })
    },
    copy(value, cb) {
      const textarea = document.createElement('textarea')
      textarea.readOnly = 'readonly'
      textarea.value = value
      document.body.appendChild(textarea)
      textarea.select()
      textarea.setSelectionRange(0, textarea.value.length)
      document.execCommand('Copy')
      document.body.removeChild(textarea)
      if (cb && Object.prototype.toString.call(cb) === '[object Function]') {
        cb()
      }
    },
  },
  watch: {
    '$route.name': function(newName, oldName) {
      this.resourceTypes = []
      this.loadResourceTypes()
    },
  },
}
</script>
<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}

.fold {
  width: calc(100% - 216px);
  display: inline-block;
}

.operator {
  margin-bottom: 18px;
}
.action-btn {
  margin-bottom: 1rem;
}
.custom-filter-dropdown {
  padding: 8px;
  border-radius: 4px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0;
}
</style>

<style lang="less" scoped>
.resource-user-form-copy {
  color: #c0c4cc;
  cursor: pointer;
  &:hover {
    color: #606266;
  }
}
</style>
