<template>
    <a-modal wrapClassName="attrbute-store-wrapper" width="80%" :visible="visible" @cancel="handleCancel">
      <template slot="title">
        <div class="attrbute-store-header">
          <span>属性库</span>
          <div class="attrbute-store-search">
            <a-input-group compact>
              <a-select class="attrbute-store-search-select" v-model="searchKey">
                <a-select-option value="alias">
                  别名
                </a-select-option>
                <a-select-option value="name">
                  名称
                </a-select-option>
              </a-select>
              <a-input
                ref="input"
                slot="default"
                class="attrbute-store-search-input"
                v-model="searchValue"
                @pressEnter="pressEnter"
                allowClear
                @change="handleInput"
              >
                <a-icon slot="suffix" type="search" @click="pressEnter" :style="{ cursor: 'pointer' }" />
              </a-input>
            </a-input-group>
          </div>
        </div>
      </template>
      <a-spin :spinning="loading" :style="{ height: '100%' }">
        <a-row v-if="attrList.length">
          <a-col
            class="attrbute-store-col"
            :xxl="4"
            :xl="6"
            :lg="8"
            :md="12"
            :sm="24"
            v-for="item in attrList"
            :key="item.id"
          >
            <AttributeCard
              @ok="
                () => {
                  searchAttributes()
                }
              "
              :isStore="true"
              :property="item"
            />
          </a-col>
        </a-row>
        <a-empty v-else>
          <img slot="image" :src="require('@/assets/data_empty.png')" />
          <span slot="description"> 暂无数据 </span>
        </a-empty>
      </a-spin>
      <template slot="footer">
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
          :pageSizeOptions="['20', '50', '100', '200']"
        />
      </template>
    </a-modal>
  </template>
  
  <script>
  import { searchAttributes } from '../../api/CITypeAttr'
  import AttributeCard from './attributeCard.vue'
  export default {
    name: 'AttributeStore',
    components: { AttributeCard },
    data() {
      return {
        visible: false,
        attrList: [],
        tablePage: {
          currentPage: 1,
          pageSize: 50,
          totalResult: 0,
        },
        loading: false,
        searchKey: 'alias',
        searchValue: '',
      }
    },
    methods: {
      open() {
        this.visible = true
        this.searchAttributes()
      },
      handleCancel() {
        this.visible = false
      },
      async searchAttributes(currentPage = 1, pageSize = this.tablePage.pageSize) {
        this.loading = true
        const params = {
          page: currentPage,
          page_size: pageSize,
        }
        if (this.searchKey && this.searchValue) {
          params[this.searchKey] = this.searchValue
        }
        searchAttributes(params)
          .then((res) => {
            this.attrList = res.attributes
            this.tablePage = {
              ...this.tablePage,
              currentPage: res.page,
              pageSize: res.page_size,
              totalResult: res.numfound,
            }
          })
          .finally(() => {
            this.loading = false
          })
      },
      pageOrSizeChange(currentPage, pageSize) {
        this.searchAttributes(currentPage, pageSize)
      },
      pressEnter() {
        this.searchAttributes(1)
      },
      handleInput(e) {
        if (!e.target.value) {
          this.pressEnter()
        }
      },
    },
  }
  </script>
  
  <style lang="less" scoped>
  .attrbute-store-wrapper {
    .attrbute-store-col {
      display: flex;
      justify-content: center;
    }
  }
  </style>
  
  <style lang="less">
  .attrbute-store-wrapper {
    .ant-modal-body {
      height: 70vh;
      overflow: auto;
    }
    .attrbute-store-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
  }
  </style>
  
  <style lang="less">
  @import '~@/style/static.less';
  
  .attrbute-store-search {
    width: 300px;
    display: inline-block;
    margin-right: 60px;
    .ant-input-group.ant-input-group-compact > *:first-child,
    .ant-input-group.ant-input-group-compact > .ant-select:first-child > .ant-select-selection {
      border-top-left-radius: 20px !important;
      border-bottom-left-radius: 20px !important;
      background-color: #custom_colors[color_1];
      color: #fff;
      border: none;
    }
    .ant-select-focused .ant-select-selection,
    .ant-select-selection:focus {
      box-shadow: none;
    }
    .ant-select-selection__rendered {
      margin-right: 12px;
    }
    .ant-select-arrow {
      color: #fff;
      font-size: 10px;
      right: 8px;
    }
    .attrbute-store-search-select {
      width: 65px;
      .ant-select-selection-selected-value {
        font-size: 12px;
      }
    }
    .attrbute-store-search-input {
      display: inline-block;
      width: calc(100% - 65px);
      .ant-input {
        background-color: #f0f5ff;
        border: none;
        border-radius: 20px;
        &:focus {
          box-shadow: none;
        }
      }
    }
  }
  </style>
  