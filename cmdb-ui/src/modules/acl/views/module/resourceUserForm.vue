<template>
  <CustomDrawer
    width="800px"
    placement="left"
    title="资源列表"
    @close="handleCancel"
    :visible="visible"
    :hasFooter="false"
  >
    <a-form-item label="资源类型" :label-col="{ span: 2 }" :wrapper-col="{ span: 14 }">
      <a-select v-model="typeSelected" style="width:100%" @change="refresh">
        <a-select-option v-for="type in resourceTypes" :value="type.id" :key="type.id">{{ type.name }}</a-select-option>
      </a-select>
    </a-form-item>
    <vxe-table :max-height="`${windowHeight - 180}px`" :data="records" ref="rTable">
      <vxe-column
        field="name"
        title="资源名"
        width="30%"
        :filters="[{ data: '' }]"
        :filter-method="filterNameMethod"
        :filter-recover-method="filterNameRecoverMethod"
      >
        <template #header="{ column }">
          <span>{{ column.title }}</span>
          <a-tooltip title="复制资源名">
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
              placeholder="按回车确认筛选"
            />
          </template>
        </template>
      </vxe-column>
      <vxe-column field="permissions" title="权限列表" width="70%">
        <template #default="{row}">
          <a-tag color="cyan" v-for="(r, index) in row.permissions" :key="index">{{ r }}</a-tag>
        </template>
      </vxe-column>
    </vxe-table>
    <!-- <a-table
      :columns="columns"
      :dataSource="records"
      :rowKey="record => record.id"
      :pagination="false"
      ref="rTable"
      size="middle"
      :scroll="{ y: 300 }"
    > -->
    <!-- <div slot="filterDropdown" slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }" class="custom-filter-dropdown">
          <a-input
            v-ant-ref="c => searchInput = c"
            :placeholder="` ${column.title}`"
            :value="selectedKeys[0]"
            @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
            @pressEnter="() => handleSearch(selectedKeys, confirm, column)"
            style="width: 188px; margin-bottom: 8px; display: block;"
          />
          <a-button
            type="primary"
            @click="() => handleSearch(selectedKeys, confirm, column)"
            icon="search"
            size="small"
            style="width: 90px; margin-right: 8px"
          >搜索</a-button>
          <a-button
            @click="() => handleReset(clearFilters, column)"
            size="small"
            style="width: 90px"
          >重置</a-button>
        </div>
        <a-icon slot="filterIcon" slot-scope="filtered" type="search" :style="{ color: filtered ? '#108ee9' : undefined }" />

        <template slot="nameSearchRender" slot-scope="text">
          <span v-if="columnSearchText.name">
            <template v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${columnSearchText.name})|(?=${columnSearchText.name})`, 'i'))">
              <mark v-if="fragment.toLowerCase() === columnSearchText.name.toLowerCase()" :key="i" class="highlight">{{ fragment }}</mark>
              <template v-else>{{ fragment }}</template>
            </template>
          </span>
          <template v-else>{{ text }}</template>
        </template> -->
    <!-- <template slot="permissions" slot-scope="record">
        <a-tag color="cyan" v-for="(r, index) in record" :key="index">{{ r }}</a-tag>
      </template>
    </a-table> -->
    <!-- <div
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
      <a-button :style="{marginRight: '8px'}" @click="handleCancel">
        取消
      </a-button>
      <a-button @click="handleOk" type="primary">确定</a-button>
    </div> -->
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
      // columns: [
      //   {
      //     title: '资源名',
      //     field: 'name',
      //     sorter: false,
      //     width: '30%',
      //     // scopedSlots: {
      //     //   customRender: 'nameSearchRender',
      //     //   filterDropdown: 'filterDropdown',
      //     //   filterIcon: 'filterIcon'
      //     // },
      //     // onFilter: (value, record) => record.name && record.name.toLowerCase().includes(value.toLowerCase()),
      //     // onFilterDropdownVisibleChange: (visible) => {
      //     //   if (visible) {
      //     //     setTimeout(() => {
      //     //       this.searchInput.focus()
      //     //     }, 0)
      //     //   }
      //     // }
      //   },
      //   {
      //     title: '权限列表',
      //     field: 'permissions',
      //     width: '70%',
      //     slots: { default: 'permissions_default' },
      //   },
      // ],
    }
  },
  computed: {
    ...mapState({
      windowHeight: state => state.windowHeight,
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
    // handleSearch(selectedKeys, confirm, column) {
    //   confirm()
    //   this.columnSearchText[column.dataIndex] = selectedKeys[0]
    // },
    // handleReset(clearFilters, column) {
    //   clearFilters()
    //   this.columnSearchText[column.dataIndex] = ''
    // },
    loadResourceTypes() {
      this.resourceTypes = []
      const appId = this.$route.name.split('_')[0]
      searchResourceType({ app_id: appId }).then(res => {
        this.resourceTypes = res.groups
        if (res.groups && res.groups.length > 0) {
          this.typeSelected = res.groups[0].id
          console.log(this.typeSelected)
        } else {
          this.typeSelected = null
        }
      })
      // .catch(err => this.$httpError(err))
    },
    handleOk() {
      this.visible = false
    },
    refresh() {
      if (this.typeSelected) {
        searchPermResourceByRoleId(this.rid, {
          resource_type_id: this.typeSelected,
          app_id: this.$route.name.split('_')[0],
        }).then(res => {
          this.records = res.resources
        })
        // .catch(err=>this.$httpError(err))
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
        .filter(item => item.name.toLowerCase().includes(this.filterName.toLowerCase()))
        .map(item => item.name)
        .join('\n')

      this.copy(val, () => {
        this.$message.success('复制成功')
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
