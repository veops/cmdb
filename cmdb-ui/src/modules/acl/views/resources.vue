<template>
  <div class="acl-resources">
    <div v-if="allResourceTypes.length">
      <a-tabs default-active-key="1" @change="loadCurrentType">
        <a-tab-pane v-for="rtype in allResourceTypes" :key="rtype.id" :tab="rtype.name"> </a-tab-pane>
      </a-tabs>
      <div class="acl-resources-header">
        <a-space>
          <a-button @click="handleCreate" type="primary">{{ $t('acl.addResource') }}</a-button>
          <a-input-search
            class="ops-input"
            :placeholder="`${$t('search')} | ${$t('acl.resource')}`"
            v-model="searchName"
            @search="
              () => {
                this.tablePage.currentPage = 1
                this.searchData()
              }
            "
          ></a-input-search>

          <div v-if="!!selectedRows.length" class="ops-list-batch-action">
            <span @click="handleBatchPerm">{{ $t('grant') }}</span>
            <a-divider type="vertical" />
            <span @click="handleBatchRevoke">{{ $t('acl.revoke') }}</span>
            <span>{{ $t('selectRows', { rows: selectedRows.length }) }}</span>
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
          >{{ $t('acl.convenient') }}</a-button
          >
          <a-switch
            v-model="isGroup"
            @change="
              () => {
                searchName = ''
                tablePage.currentPage = 1
                searchData()
                selectedRows = []
                $refs.xTable && $refs.xTable.getVxetableRef().clearCheckboxRow()
                $refs.xTable && $refs.xTable.getVxetableRef().clearCheckboxReserve()
              }
            "
            :un-checked-children="$t('acl.group2')"
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
          :checkbox-config="{ reserve: true, highlight: true, range: true }"
          @checkbox-change="changeCheckbox"
          @checkbox-all="changeCheckbox"
          @checkbox-range-end="onSelectRangeEnd"
          ref="xTable"
          row-id="id"
          show-overflow
          resizable
        >
          <!-- 1 -->
          <vxe-table-column type="checkbox" fixed="left" :width="60"></vxe-table-column>

          <!-- 2 -->

          <vxe-table-column field="name" :title="$t('acl.resourceName')" :min-widh="150" fixed="left" show-overflow>
            <template #title="{ row }">
              {{ row.isGroup ? $t('acl.groupName') : $t('acl.resourceName') }}
            </template>
          </vxe-table-column>

          <!-- 3 -->
          <vxe-table-column field="user" :title="$t('acl.creator')" :min-widh="100"> </vxe-table-column>

          <!-- 4 -->
          <vxe-table-column field="created_at" :title="$t('created_at')" :min-widh="220" align="center">
          </vxe-table-column>

          <!-- 5 -->
          <vxe-table-column field="updated_at" :title="$t('updated_at')" :min-widh="220" fixed="center">
          </vxe-table-column>

          <!-- 6 -->

          <vxe-table-column
            field="action"
            :title="$t('operation')"
            :min-widh="200"
            fixed="right"
            align="center"
            show-overflow
          >
            <template #default="{ row }">
              <span v-show="isGroup">
                <a @click="handleDisplayMember(row)">{{ $t('acl.member') }}</a>
                <a-divider type="vertical" />
                <a @click="handleGroupEdit(row)">{{ $t('edit') }}</a>
                <a-divider type="vertical" />
              </span>
              <a-tooltip :title="$t('acl.viewAuth')">
                <a @click="handlePerm(row)"><a-icon type="eye"/></a>
              </a-tooltip>
              <a-divider type="vertical" />
              <a-tooltip :title="$t('grant')">
                <a :style="{ color: '#4bbb13' }" @click="handlePermManage(row)">
                  <a-icon type="usergroup-add" />
                </a>
              </a-tooltip>
              <a-divider type="vertical" />
              <a-popconfirm
                :title="$t('confirmDelete')"
                @confirm="handleDelete(row)"
                @cancel="cancel"
                :okText="$t('yes')"
                :cancelText="$t('no')"
              >
                <a style="color: red"><a-icon type="delete"/></a>
              </a-popconfirm>
            </template>
          </vxe-table-column>
        </ops-table>
        <a-pagination
          size="small"
          show-size-changer
          show-quick-jumper
          :current="tablePage.currentPage"
          :total="tablePage.total"
          :show-total="(total, range) => `当前展示 ${range[0]}-${range[1]} 条数据, 共 ${total} 条`"
          :page-size="tablePage.pageSize"
          :default-current="1"
          :page-size-options="pageSizeOptions"
          @change="pageOrSizeChange"
          @showSizeChange="pageOrSizeChange"
          :style="{ marginTop: '10px', textAlign: 'right' }"
        />
      </a-spin>
    </div>
    <div v-else style="text-align: center; margin-top: 20%">
      <a-icon style="font-size: 50px; margin-bottom: 20px; color: orange" type="info-circle" />
      <h3>{{ $t('acl.addTypeTips') }}</h3>
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
      isGroup: false,
      allResourceTypes: [],
      currentType: { id: 0 },
      pageSizeOptions: ['20', '50', '100', '200'],
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
      this.$refs.xTable && this.$refs.xTable.getVxetableRef().clearCheckboxRow()
      this.$refs.xTable && this.$refs.xTable.getVxetableRef().clearCheckboxReserve()
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
          this.$message.success(this.$t('deleteSuccess'))
          this.handleOk()
        })
      } else {
        deleteResourceGroup(id).then((res) => {
          this.$message.success(this.$t('deleteSuccess'))
          this.handleOk()
        })
      }
    },
    cancel() {},
    pageOrSizeChange(currentPage, pageSize) {
      this.tablePage.currentPage = currentPage
      this.tablePage.pageSize = pageSize
      this.searchData()
    },
    changeCheckbox({ records }) {
      // console.log(records)
      this.selectedRows = this.$refs.xTable
        .getVxetableRef()
        .getCheckboxRecords()
        .concat(this.$refs.xTable.getVxetableRef().getCheckboxReserveRecords())
    },
    onSelectRangeEnd({ records }) {
      this.selectedRows = records
    },
    handleBatchPerm() {
      this.$refs['resourcePermManageForm'].editPerm(this.selectedRows, this.isGroup)
    },
    handleBatchRevoke() {
      this.$refs['resourcePermManageForm'].editPerm(this.selectedRows, this.isGroup, 'revoke')
    },
    closePerm() {
      this.$refs.xTable.getVxetableRef().clearCheckboxRow()
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
@import '~@/style/static.less';

.acl-resources {
  border-radius: @border-radius-box;
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
