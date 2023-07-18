<template>
  <div class="acl-resources">
    <div v-if="allResourceTypes.length">
      <a-tabs default-active-key="1" @change="loadCurrentType">
        <a-tab-pane v-for="rtype in allResourceTypes" :key="rtype.id" :tab="rtype.name"> </a-tab-pane>
      </a-tabs>
      <div class="acl-resources-header">
        <a-space>
          <a-button @click="handleCreate" type="primary">{{ btnName }}</a-button>
          <a-input-search
            class="ops-input"
            placeholder="搜索 | 资源名"
            v-model="searchName"
            @search="
              () => {
                this.tablePage.currentPage = 1
                this.searchData()
              }
            "
          ></a-input-search>

          <div v-if="!!selectedRows.length" class="ops-list-batch-action">
            <span @click="handleBatchPerm">授权</span>
            <a-divider type="vertical" />
            <span @click="handleBatchRevoke">权限回收</span>
            <span>选取: {{ selectedRows.length }} 项</span>
          </div>
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
      <a-spin :spinning="loading">
        <ops-table
          size="small"
          stripe
          class="ops-stripe-table"
          :data="tableData"
          highlight-hover-row
          :height="`${windowHeight - 250}px`"
          :checkbox-config="{ reserve: true }"
          @checkbox-change="changeCheckbox"
          @checkbox-all="changeCheckbox"
          ref="xTable"
          row-id="id"
          show-overflow
        >
          <!-- 1 -->
          <vxe-table-column type="checkbox" fixed="left"></vxe-table-column>

          <!-- 2 -->

          <vxe-table-column field="name" title="资源名" :min-widh="150" fixed="left" show-overflow>
            <template #title="{row}">
              {{ row.isGroup ? '资源组名' : '资源名' }}
            </template>
          </vxe-table-column>

          <!-- 3 -->
          <vxe-table-column field="user" title="创建者" :min-widh="100"> </vxe-table-column>

          <!-- 4 -->
          <vxe-table-column field="created_at" title="创建时间" :min-widh="220" align="center"> </vxe-table-column>

          <!-- 5 -->
          <vxe-table-column field="updated_at" title="最后修改时间" :min-widh="220" fixed="center"> </vxe-table-column>

          <!-- 6 -->

          <vxe-table-column
            field="action"
            title="操作"
            :min-widh="200"
            fixed="right"
            align="center"
            show-overflow>
            <template #default="{row}">
              <span v-show="row.isGroup">
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
          </vxe-table-column>
        </ops-table>
        <vxe-pager
          size="small"
          :layouts="['Total', 'PrevPage', 'JumpNumber', 'NextPage', 'Sizes']"
          :current-page.sync="tablePage.currentPage"
          :page-size.sync="tablePage.pageSize"
          :total="tablePage.total"
          :page-sizes="pageSizeOptions"
          @page-change="handlePageChange"
          :style="{ marginTop: '10px' }"
        >
        </vxe-pager>
      </a-spin>
    </div>
    <div v-else style="text-align: center;margin-top:20%">
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
        deleteResourceById(id, { app_id: this.$route.name.split('_')[0] }).then((res) => {
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
.acl-resources {
  border-radius: 15px;
  background-color: #fff;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 12px 24px 24px 24px;
  .acl-resources-header {
    width: 100%;
    display: inline-flex;
    margin-bottom: 15px;
    align-items: center;
    justify-content: space-between;
    .ant-switch {
      margin-left: auto;
    }
  }
}
</style>
