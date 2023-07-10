<template>
  <div :style="{ backgroundColor: '#fff', padding: '24px' }">
    <div v-if="allResourceTypes.length > 0">
      <a-tabs default-active-key="1" @change="loadCurrentType">
        <a-tab-pane v-for="rtype in allResourceTypes" :key="rtype.id" :tab="rtype.name"> </a-tab-pane>
      </a-tabs>
      <div class="resources-action-btn">
        <a-space>
          <a-button @click="handleCreate" type="primary">{{ btnName }}</a-button>
          <a-input-search
            placeholder="搜索 | 资源名"
            v-model="searchName"
            @search="
              () => {
                this.tablePage.currentPage = 1
                this.searchData()
              }
            "
          ></a-input-search>
          <a-dropdown v-if="selectedRows && selectedRows.length">
            <a-button type="primary" ghost>
              批量操作
            </a-button>
            <a-menu slot="overlay">
              <a-menu-item @click="handleBatchPerm">
                <a href="javascript:;">授权</a>
              </a-menu-item>
              <a-menu-item @click="handleBatchRevoke">
                <a href="javascript:;">权限回收</a>
              </a-menu-item>
            </a-menu>
          </a-dropdown>

          <span
            v-if="selectedRows && selectedRows.length"
          >已选择<strong>{{ selectedRows.length }}</strong
          >项</span
          >
        </a-space>

        <a-space>
          <a-button
            type="primary"
            ghost
            @click="
              () => {
                $refs.resourceBatchPerm.open(currentType.id)
              }
            "
          >便捷授权</a-button
          >
          <a-switch
            v-model="isGroup"
            @change="
              () => {
                searchName = ''
                tablePage.currentPage = 1
                searchData()
                selectedRows = []
                $refs.xTable && $refs.xTable.clearCheckboxRow()
                $refs.xTable && $refs.xTable.clearCheckboxReserve()
              }
            "
            un-checked-children="组"
          ></a-switch>
        </a-space>
      </div>
      <a-spin
        :spinning="loading"
      ><vxe-grid
        :columns="tableColumns"
        :data="tableData"
        highlight-hover-row
        :max-height="`${windowHeight - 245}px`"
        :checkbox-config="{ reserve: true }"
        @checkbox-change="changeCheckbox"
        @checkbox-all="changeCheckbox"
        ref="xTable"
        row-id="id"
        show-overflow
      >
        <template #name_header>
          {{ isGroup ? '资源组名' : '资源名' }}
        </template>
        <template #action_default="{row}">
          <span v-show="isGroup">
            <a @click="handleDisplayMember(row)">成员</a>
            <a-divider type="vertical" />
            <a @click="handleGroupEdit(row)">编辑</a>
            <a-divider type="vertical" />
          </span>
          <a-tooltip title="查看授权">
            <a @click="handlePerm(row)"><a-icon type="eye"/></a>
          </a-tooltip>
          <a-divider type="vertical" />
          <a-tooltip title="授权">
            <a :style="{ color: '#4bbb13' }" @click="handlePermManage(row)">
              <a-icon type="usergroup-add" />
            </a>
          </a-tooltip>
          <a-divider type="vertical" />
          <a-popconfirm title="确认删除?" @confirm="handleDelete(row)" @cancel="cancel" okText="是" cancelText="否">
            <a style="color: red"><a-icon type="delete"/></a>
          </a-popconfirm>
        </template>
        <template #pager>
          <vxe-pager
            :layouts="['Total', 'PrevPage', 'JumpNumber', 'NextPage', 'Sizes']"
            :current-page.sync="tablePage.currentPage"
            :page-size.sync="tablePage.pageSize"
            :total="tablePage.total"
            :page-sizes="pageSizeOptions"
            @page-change="handlePageChange"
          >
          </vxe-pager>
        </template> </vxe-grid
      ></a-spin>
    </div>
    <div v-else style="text-align: center">
      <a-icon style="font-size:50px; margin-bottom: 20px; color: orange" type="info-circle" />
      <h3>暂无类型信息，请先添加资源类型！</h3>
    </div>
    <resourceForm ref="resourceForm" @fresh="handleOk"> </resourceForm>
    <resourcePermForm ref="resourcePermForm"> </resourcePermForm>
    <ResourcePermManageForm
      ref="resourcePermManageForm"
      :groupTypeMessage="currentType"
      @close="closePerm"
    ></ResourcePermManageForm>
    <resource-group-modal ref="resourceGroupModal"></resource-group-modal>
    <resource-group-member ref="resourceGroupMember"></resource-group-member>
    <ResourceBatchPerm ref="resourceBatchPerm" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import resourceForm from './module/resourceForm'
import resourcePermForm from './module/resourcePermForm'
import ResourceGroupModal from './module/resourceGroupModal'
import ResourceGroupMember from './module/resourceGroupMember'
import ResourcePermManageForm from './module/resourcePermManageForm'
import ResourceBatchPerm from './module/resourceBatchPerm.vue'
import {
  deleteResourceById,
  searchResource,
  searchResourceType,
  getResourceGroups,
  deleteResourceGroup,
} from '@/modules/acl/api/resource'

export default {
  name: 'Resources',
  components: {
    resourceForm,
    resourcePermForm,
    ResourceGroupModal,
    ResourceGroupMember,
    ResourcePermManageForm,
    ResourceBatchPerm,
  },
  data() {
    return {
      loading: false,
      tablePage: {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      },
      tableData: [],
      tableColumns: [
        {
          type: 'checkbox',
          fixed: 'left',
        },
        {
          title: '资源名',
          field: 'name',
          minWidth: '150px',
          showOverflow: 'tooltip',
          fixed: 'left',
          slots: {
            header: 'name_header',
          },
        },
        {
          title: '创建者',
          minWidth: '100px',
          field: 'user',
        },
        {
          title: '创建时间',
          minWidth: '220px',
          field: 'created_at',
          align: 'center',
        },
        {
          title: '最后修改时间',
          minWidth: '220px',
          field: 'updated_at',
          align: 'center',
        },
        {
          title: '操作',
          field: 'action',
          width: '200px',
          fixed: 'right',
          align: 'center',
          slots: {
            default: 'action_default',
          },
        },
      ],
      btnName: '新增资源',
      isGroup: false,
      allResourceTypes: [],
      currentType: { id: 0 },
      pageSizeOptions: [10, 25, 50, 100],
      searchName: '',
      selectedRows: [],
    }
  },

  beforeCreate() {
    this.form = this.$form.createForm(this)
  },
  computed: mapState({
    windowHeight: (state) => state.windowHeight,
  }),
  mounted() {
    // this.getAllResourceTypes()
  },
  inject: ['reload'],
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.getAllResourceTypes()
    })
  },
  methods: {
    async searchData() {
      const { currentPage, pageSize } = this.tablePage
      const param = {
        app_id: this.$route.name.split('_')[0],
        resource_type_id: this.currentType.id,
        page_size: pageSize,
        page: currentPage,
        q: this.searchName,
      }
      this.loading = true
      if (!this.isGroup) {
        await searchResource(param).then((res) => {
          this.tablePage = { ...this.tablePage, total: res.numfound, currentPage: res.page }
          this.tableData = res.resources
          this.loading = false
        })
      } else {
        await getResourceGroups(param).then((res) => {
          this.tablePage = { ...this.tablePage, total: res.numfound, currentPage: res.page }
          this.tableData = res.groups
          this.loading = false
        })
      }
    },
    handleDisplayMember(record) {
      this.$refs['resourceGroupMember'].handleEdit(record)
    },
    handleGroupEdit(record) {
      this.$refs['resourceGroupModal'].handleEdit(record)
    },
    async getAllResourceTypes() {
      await searchResourceType({ page_size: 9999, app_id: this.$route.name.split('_')[0] }).then((res) => {
        this.allResourceTypes = res.groups
        if (res.groups && res.groups.length) {
          this.loadCurrentType(res.groups[0].id)
        }
      })
    },
    handlePermManage(record) {
      this.$refs['resourcePermManageForm'].editPerm(record, this.isGroup) // todo fix
    },
    loadCurrentType(rtypeId) {
      this.searchName = ''
      this.selectedRows = []
      this.tablePage.currentPage = 1
      this.$refs.xTable && this.$refs.xTable.clearCheckboxRow()
      this.$refs.xTable && this.$refs.xTable.clearCheckboxReserve()
      if (rtypeId) {
        this.currentType = this.allResourceTypes.find((item) => item.id === rtypeId)
      }
      this.searchData()
    },
    handlePerm(record) {
      this.$refs.resourcePermForm.handlePerm(record, this.isGroup)
    },
    handleDelete(record) {
      this.deleteResource(record.id)
    },
    handleOk() {
      this.tablePage.currentPage = 1
      this.searchData()
    },
    handleCreate() {
      this.$refs.resourceForm.handleCreate(this.currentType)
    },
    deleteResource(id) {
      if (!this.isGroup) {
        deleteResourceById(id).then((res) => {
          this.$message.success(`删除成功`)
          this.handleOk()
        })
        // .catch(err => this.requestFailed(err))
      } else {
        deleteResourceGroup(id).then((res) => {
          this.$message.success(`删除成功`)
          this.handleOk()
        })
        // .catch(err => this.requestFailed(err))
      }
    },
    // requestFailed(err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
    cancel() {},
    handlePageChange({ currentPage, pageSize }) {
      this.tablePage.currentPage = currentPage
      this.tablePage.pageSize = pageSize
      this.searchData()
    },
    changeCheckbox({ records }) {
      // console.log(records)
      this.selectedRows = this.$refs.xTable.getCheckboxRecords().concat(this.$refs.xTable.getCheckboxReserveRecords())
    },
    handleBatchPerm() {
      this.$refs['resourcePermManageForm'].editPerm(this.selectedRows, this.isGroup)
    },
    handleBatchRevoke() {
      this.$refs['resourcePermManageForm'].editPerm(this.selectedRows, this.isGroup, 'revoke')
    },
    closePerm() {
      this.$refs.xTable.clearCheckboxRow()
      this.selectedRows = []
    },
  },
  watch: {
    '$route.name': function(newName, oldName) {
      this.isGroup = false
      this.tablePage = {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      }
    },
    searchName: {
      immediate: true,
      handler(newVal) {
        if (!newVal) {
          this.tablePage.currentPage = 1
          this.searchData()
        }
      },
    },
  },
}
</script>

<style lang="less" scoped>
.resources-action-btn {
  width: 100%;
  display: inline-flex;
  margin-bottom: 15px;
  align-items: center;
  justify-content: space-between;
  .ant-switch {
    margin-left: auto;
  }
}
</style>
