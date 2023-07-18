<template>
  <div class="acl-resource-types">
    <div class="acl-resource-types-header">
      <a-button @click="handleCreate" type="primary" style="margin-right: 0.3rem">{{ btnName }}</a-button>
      <a-input-search
        class="ops-input"
        :style="{ display: 'inline', marginLeft: '10px', width: '200px' }"
        placeholder="搜索 | 资源类型名"
        v-model="searchName"
        allowClear
        @search="
          () => {
            this.tablePage.currentPage = 1
            this.searchData()
          }
        "
      ></a-input-search>
    </div>
    <a-spin :spinning="loading">
      <ops-table
        stripe
        size="small"
        class="ops-stripe-table"
        :data="groups"
        :height="`${windowHeight - 200}px`"
        highlight-hover-row
      >
        <!-- 1 -->
        <vxe-table-column
          field="name"
          title="资源类型名"
          :min-width="175"
          fixed="left"
          show-overflow
        ></vxe-table-column>

        <!-- 2 -->
        <vxe-table-column field="description" title="描述" :min-width="175"></vxe-table-column>

        <!-- 3 -->
        <vxe-table-column field="id" title="权限" :min-width="300">
          <template #default="{ row }">
            <a-tag color="cyan" v-for="perm in id2perms[row.id]" :key="perm.id">{{ perm.name }}</a-tag>
          </template>
        </vxe-table-column>

        <!-- 4 -->
        <vxe-table-column field="action" title="操作" :width="100" fixed="right">
          <template #default="{ row }">
            <a @click="handleEdit(row)"><a-icon type="edit"/></a>
            <a-divider type="vertical" />
            <a-popconfirm title="确认删除?" @confirm="handleDelete(row)" okText="是" cancelText="否">
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

    <resourceTypeForm ref="resourceTypeForm" :handleOk="handleOk"> </resourceTypeForm>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import resourceTypeForm from './module/resourceTypeForm'
import { deleteResourceTypeById, searchResourceType } from '@/modules/acl/api/resource'

export default {
  name: 'ResourceType',
  components: {
    resourceTypeForm,
  },
  data() {
    return {
      loading: false,
      groups: [],
      id2perms: {},
      btnName: '新增资源类型',
      pageSizeOptions: [10, 25, 50, 100],
      tablePage: {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      },
      tableColumns: [
        {
          title: '资源类型名',
          field: 'name',
          minWidth: '175px',
          fixed: 'left',
          showOverflow: 'tooltip',
        },
        {
          title: '描述',
          field: 'description',
          minWidth: '175px',
        },
        {
          title: '权限',
          field: 'id',
          minWidth: '300px',
          slots: {
            default: 'id_default',
          },
        },
        {
          title: '操作',
          field: 'action',
          minWidth: '175px',
          slots: { default: 'action_default' },
          fixed: 'right',
        },
      ],
      searchName: '',
    }
  },

  beforeCreate() {},
  mounted() {
    this.searchData()
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
  },
  watch: {
    '$route.name': function(newName, oldName) {
      this.tablePage = {
        total: 0,
        currentPage: 1,
        pageSize: 50,
      }
      this.searchData()
    },
    searchName: {
      immediate: true,
      handler(newVal, oldVal) {
        if (!newVal) {
          this.tablePage.currentPage = 1
          this.searchData()
        }
      },
    },
  },
  inject: ['reload'],

  methods: {
    searchData() {
      const { currentPage, pageSize } = this.tablePage
      this.loading = true
      const param = {
        app_id: this.$route.name.split('_')[0],
        page_size: pageSize,
        page: currentPage,
        q: this.searchName,
      }
      searchResourceType(param).then((res) => {
        this.tablePage = {
          ...this.tablePage,
          total: res.numfound,
          currentPage: res.page,
        }
        this.groups = res.groups
        this.id2perms = res.id2perms
        this.loading = false
      })
    },
    handleEdit(record) {
      var perms = []
      var permList = this.id2perms[record.id]
      if (permList) {
        for (var i = 0; i < permList.length; i++) {
          perms.push(permList[i].name)
        }
      }
      record.perms = perms
      this.$refs.resourceTypeForm.handleEdit(record)
    },
    handleDelete(record) {
      this.deleteResourceType(record.id)
    },
    handleOk() {
      this.searchData()
    },
    handleCreate() {
      this.$refs.resourceTypeForm.handleCreate()
    },
    deleteResourceType(id) {
      deleteResourceTypeById(id).then((res) => {
        this.$message.success(`删除成功`)
        this.handleOk()
      })
      // .catch(err => this.requestFailed(err))
    },
    // requestFailed(err) {
    //   const msg = ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试'
    //   this.$message.error(`${msg}`)
    // },
    handlePageChange({ currentPage, pageSize }) {
      this.tablePage.currentPage = currentPage
      this.tablePage.pageSize = pageSize
      this.searchData()
    },
  },
}
</script>

<style lang="less" scoped>
.acl-resource-types {
  border-radius: 15px;
  background-color: #fff;
  height: calc(100vh - 64px);
  margin-bottom: -24px;
  padding: 24px;
  .acl-resource-types-header {
    width: 100%;
    display: inline-flex;
    margin-bottom: 15px;
    align-items: center;
  }
}
</style>
