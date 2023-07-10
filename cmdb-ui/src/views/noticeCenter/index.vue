<template>
  <TwoColumnLayout appName="notice-center">
    <template #one>
      <div
        :class="{ 'notice-center-left': true, 'notice-center-left-select': current.value === item.value }"
        v-for="item in leftList"
        :key="item.label"
        @click="
          () => {
            current = item
            selectedRowKeys = []
            $refs.opsTable.getVxetableRef().clearCheckboxRow()
            $refs.opsTable.getVxetableRef().clearCheckboxReserve()
            updateTableData()
          }
        "
      >
        <span>{{ item.label }}</span>
        <span v-if="item.value === false">{{ totalUnreadNum > 99 ? '99+' : totalUnreadNum }}</span>
      </div>
    </template>
    <template #two>
      <div class="notice-center-header">
        <div>
          <a-badge
            v-for="app in apps"
            :key="app.value"
            :count="getAppCount(app)"
            :offset="[-4, 5]"
            :numberStyle="{
              minWidth: '14px',
              height: '14px',
              lineHeight: '14px',
              borderRadius: '7px',
              padding: ' 0 4px',
            }"
            :class="{ 'notice-center-header-app': true, 'notice-center-header-app-selected': currentApp === app.value }"
          >
            <span @click="changeApp(app)">{{ app.label }}</span>
          </a-badge>
        </div>
        <div class="notice-center-categories">
          <span
            :class="{ 'notice-center-categories-selected': currentCategory === cate }"
            v-for="cate in categories"
            :key="cate"
            @click="changeCate(cate)"
          >{{ cate }}</span
          >
        </div>
        <div>
          <a-input-search
            allow-clear
            v-model="filterName"
            class="ops-input-radius"
            :style="{ width: '300px', marginRight: '20px' }"
            placeholder="请输入你需要搜索的内容"
            @search="updateTableData()"
          />
          <div class="ops-list-batch-action">
            <template v-if="!!selectedRowKeys.length">
              <span @click="batchChangeIsRead('read')">标为已读</span>
              <a-divider type="vertical" />
              <span @click="batchChangeIsRead('unread')">标为未读</span>
              <span>选取: {{ selectedRowKeys.length }} 项</span>
            </template>
          </div>
        </div>
      </div>
      <OpsTable
        size="small"
        ref="opsTable"
        stripe
        class="ops-stripe-table"
        :data="tableData"
        show-overflow
        show-header-overflow
        @checkbox-change="onSelectChange"
        @checkbox-all="onSelectChange"
        :row-class-name="rowClassName"
        :checkbox-config="{ reserve: true }"
        :row-config="{ keyField: 'id' }"
        :height="tableHeight"
      >
        <vxe-column type="checkbox" width="60px"></vxe-column>
        <vxe-column field="content" title="标题内容">
          <template #default="{row}">
            <span v-html="row.content"></span>
          </template>
        </vxe-column>
        <vxe-column field="created_at" title="提交时间" width="150px">
          <template #default="{row}">
            {{ moment(row.created_at).format('YYYY-MM-DD HH:mm:ss') }}
          </template>
        </vxe-column>
        <vxe-column field="category" title="类型" width="150px">
          <template #default="{row}">
            {{ `${row.app_name}-${row.category}` }}
          </template>
        </vxe-column>
      </OpsTable>
      <div class="notice-center-pagination">
        <a-pagination
          size="small"
          show-size-changer
          show-quick-jumper
          :current="tablePage.currentPage"
          :total="tablePage.totalResult"
          :show-total="(total, range) => `当前展示 ${range[0]}-${range[1]} 条数据, 共 ${total} 条`"
          :page-size="tablePage.pageSize"
          :default-current="1"
          @change="pageOrSizeChange"
          @showSizeChange="pageOrSizeChange"
        />
      </div>
    </template>
  </TwoColumnLayout>
</template>

<script>
import moment from 'moment'
import { mapState } from 'vuex'
import TwoColumnLayout from '@/components/TwoColumnLayout'
import { getMessage, getNoticeApps, getNoticeCategoriesByApp, batchUpdateMessage } from '../../api/message'
import Bus from '../../bus'

export default {
  name: 'Notice',
  components: {
    TwoColumnLayout,
  },
  data() {
    return {
      leftList: [
        {
          value: '',
          label: '全部消息',
        },
        {
          value: false,
          label: '未读消息',
        },
        {
          value: true,
          label: '已读消息',
        },
      ],
      current: {
        value: '',
        label: '全部消息',
      },
      tablePage: {
        currentPage: 1,
        pageSize: 20,
        totalResult: 0,
      },
      filterName: '',
      tableData: [],
      apps: [],
      interval: null,
      currentApp: '',
      categories: [],
      currentCategory: undefined,
      selectedRowKeys: [],
    }
  },
  computed: {
    ...mapState({
      totalUnreadNum: (state) => state.notice.totalUnreadNum,
      appUnreadNum: (state) => state.notice.appUnreadNum,
      windowHeight: (state) => state.windowHeight,
    }),
    tableHeight() {
      if (this.categories.length) {
        return this.windowHeight - 236
      }
      return this.windowHeight - 205
    },
  },
  mounted() {
    this.intervalFunc()
    this.interval = setInterval(() => {
      this.intervalFunc()
    }, 30000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
    this.interval = null
  },
  methods: {
    moment,
    intervalFunc() {
      this.getNoticeApps()
      this.getNoticeCategoriesByApp()
      this.updateTableData(this.tablePage.currentPage, this.tablePage.pageSize)
    },
    getNoticeApps() {
      getNoticeApps().then((res) => {
        const _apps = res.app_names.map((appName) => ({
          value: appName,
          label: appName,
        }))
        if (_apps.length) {
          _apps.unshift({
            value: '',
            label: '全部',
          })
        }
        this.apps = _apps
      })
    },
    getNoticeCategoriesByApp() {
      if (this.currentApp) {
        getNoticeCategoriesByApp(this.currentApp).then((res) => {
          this.categories = res.categories
        })
      } else {
        this.categories = []
      }
    },
    updateTableData(currentPage = 1, pageSize = this.tablePage.pageSize) {
      getMessage({
        is_read: this.current.value,
        app_name: this.currentApp,
        category: this.currentCategory,
        page: currentPage,
        page_size: pageSize,
        order: this.tableSortData || '-create_at',
        search: this.filterName,
      }).then((res) => {
        this.tableData = res?.data_list || []
        this.tablePage = {
          ...this.tablePage,
          currentPage: res.page,
          pageSize: res.page_size,
          totalResult: res.total,
        }
      })
    },
    pageOrSizeChange(currentPage, pageSize) {
      this.updateTableData(currentPage, pageSize)
    },
    onSelectChange({ records }) {
      this.selectedRowKeys = records
    },
    getAppCount(app) {
      if (app.value) {
        const _find = this.appUnreadNum.find((item) => item.app_name === app.value)
        return _find?.count ?? 0
      }
      return this.totalUnreadNum
    },
    changeApp(app) {
      this.currentApp = app.value
      this.currentCategory = undefined
      this.filterName = ''
      this.selectedRowKeys = []
      this.$refs.opsTable.getVxetableRef().clearCheckboxRow()
      this.$refs.opsTable.getVxetableRef().clearCheckboxReserve()
      this.getNoticeCategoriesByApp()
      this.updateTableData()
    },
    changeCate(cate) {
      this.filterName = ''
      this.selectedRowKeys = []
      this.$refs.opsTable.getVxetableRef().clearCheckboxRow()
      this.$refs.opsTable.getVxetableRef().clearCheckboxReserve()
      this.currentCategory = cate
      this.updateTableData()
    },
    batchChangeIsRead(action) {
      batchUpdateMessage({ action, message_id_list: this.selectedRowKeys.map((item) => item.id) }).then((res) => {
        this.updateTableData()
        Bus.$emit('getUnreadMessageCount')
      })
    },
    rowClassName({ row, rowIndex, $rowIndex }) {
      if (row.is_read) {
        return 'notice-center-is_read'
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';

.notice-center-left {
  color: rgba(0, 0, 0, 0.7);
  padding: 0 12px 0 24px;
  height: 32px;
  line-height: 32px;
  border-left: 3px solid #fff;
  cursor: pointer;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  > span:nth-child(2) {
    background-color: #e1efff;
    border-radius: 2px;
    color: #9094a6;
    padding: 0 4px;
    font-size: 12px;
    height: 20px;
    line-height: 20px;
  }
}
.notice-center-left:hover,
.notice-center-left-select {
  background-color: #f0f5ff;
  border-color: #custom_colors[color_1];
  > span:nth-child(2) {
    background-color: #fff;
    color: #custom_colors[color_1];
  }
}
.notice-center-header {
  > div {
    margin-bottom: 10px;
  }
  .notice-center-header-app {
    border-radius: 16px;
    background-color: #f0f5ff;
    color: #9094a6;
    padding: 5px 14px;
    cursor: pointer;
    margin-right: 12px;
  }
  > .notice-center-header-app:hover,
  .notice-center-header-app-selected {
    background-color: #custom_colors[color_1];
    color: #fff;
  }
  .notice-center-categories {
    > span {
      color: #a5a9bc;
      padding: 4px 18px;
      background-color: #f0f5ff;
      cursor: pointer;
    }
    > span:hover,
    .notice-center-categories-selected {
      color: #fff;
      background-color: #custom_colors[color_1];
    }
  }
}
.notice-center-pagination {
  width: 100%;
  margin-top: 12px;
  display: inline-flex;
  justify-content: flex-end;
}
</style>
<style lang="less">
.notice-center-is_read {
  opacity: 0.6;
}
</style>
