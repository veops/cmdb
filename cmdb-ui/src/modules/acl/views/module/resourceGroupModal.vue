<template>
  <a-modal v-model="visible" :title="`${$t('acl.memberManage')}${editRecord.name}`" @ok="handleSubmit" :width="690">
    <!-- <CustomTransfer
      ref="customTransfer"
      :show-search="true"
      :data-source="resources"
      :filter-option="filterOption"
      :target-keys="targetKeys"
      :render="(item) => item.title"
      @change="handleChange"
      @search="handleSearch"
      @selectChange="selectChange"
    >
    </CustomTransfer> -->
    <a-transfer
      :dataSource="resources"
      :showSearch="true"
      :listStyle="{
        width: '300px',
        height: '450px',
      }"
      :titles="[]"
      :render="(item) => item.title"
      :targetKeys="targetKeys"
      @change="handleChange"
      @selectChange="selectChange"
      :selectedKeys="selectedKeys"
    >
      <span slot="notFoundContent">{{ $t('noData') }}</span>
      <template slot="children" slot-scope="{ props: { direction, filteredItems } }">
        <div class="ant-transfer-list-content" v-if="direction === 'right'">
          <div
            @dblclick="(e) => changeSingleItem(e, item)"
            v-for="item in filteredItems"
            :key="item.key"
            :style="{ height: '32px' }"
          >
            <li
              :class="
                `ant-transfer-list-content-item ${
                  selectedKeys.includes(item.key) ? 'ant-transfer-list-content-item-selected' : ''
                }`
              "
              style="padding:0 12px 0 12px;position:relative"
              @click="setSelectedKeys(item)"
            >
              <div :class="`ant-transfer-list-content-item-text`" style="display:inline">
                {{ item.title }}
                <div class="ant-transfer-list-icon" @click="(e) => changeSingleItem(e, item)">
                  <a-icon type="left" />
                </div>
              </div>
            </li>
          </div>
        </div>
        <div v-if="direction === 'left'" class="ant-transfer-list-content">
          <div
            @dblclick="(e) => changeSingleItem(e, item)"
            v-for="item in filteredItems"
            :key="item.key"
            :style="{ height: '32px' }"
          >
            <li
              :class="
                `ant-transfer-list-content-item ${
                  selectedKeys.includes(item.key) ? 'ant-transfer-list-content-item-selected' : ''
                }`
              "
              style="padding:0 12px 0 12px;position:relative"
              @click="setSelectedKeys(item)"
            >
              <div class="ant-transfer-list-content-item-text" style="display:inline">
                {{ item.title }}
                <div @click="(e) => changeSingleItem(e, item)" class="ant-transfer-list-icon">
                  <a-icon type="right" />
                </div>
              </div>
            </li>
          </div>
        </div>
      </template>
    </a-transfer>
  </a-modal>
</template>
<script>
import _ from 'lodash'
import { updateResourceGroup, searchResource, getResourceGroupItems } from '@/modules/acl/api/resource'

export default {
  name: 'ResourceGroupModal',
  data() {
    return {
      visible: false,
      editRecord: {},
      resources: [],
      targetKeys: [],
      selectedKeys: [],
    }
  },
  methods: {
    handleSubmit() {
      const items = this.targetKeys.map((key) => {
        return this.resources.filter((item) => item.name === key)[0]['id']
      })
      updateResourceGroup(this.editRecord['id'], { items: items.join(',') }).then(() => {
        this.visible = false
        this.$message.success(this.$t('updateSuccess'))
      })
      // .catch(err => this.$httpError(err))
    },
    // filterOption(inputValue, option) {
    //   return option.description.indexOf(inputValue) > -1
    // },
    // handleChange(targetKeys, direction, moveKeys) {
    //   console.log(JSON.parse(JSON.stringify(targetKeys)))
    //   this.targetKeys = targetKeys
    // },
    // handleSearch(dir, value) {
    //   console.log('search:', dir, value)
    // },
    async handleEdit(record) {
      this.editRecord = record
      this.visible = true
      this.selectedKeys = []
      await this.loadChildren(record.id)
      await this.loadResource()
    },
    loadChildren(_id) {
      getResourceGroupItems(_id).then((res) => {
        this.targetKeys = res.map((item) => item.name)
      })
      // .catch(err => this.$httpError(err))
    },
    loadResource() {
      const params = {
        app_id: this.editRecord['app_id'],
        resource_type_id: this.editRecord['resource_type_id'],
        page_size: 9999,
      }
      searchResource(params).then((res) => {
        this.resources = res['resources'].map((item) => {
          return {
            id: item.id,
            name: item.name,
            key: item.name,
            description: item.name,
            title: item.name,
          }
        })
      })
      // .catch(err => this.$httpError(err))
    },
    setSelectedKeys(item) {
      const idx = this.selectedKeys.findIndex((key) => key === item.key)
      if (idx > -1) {
        this.selectedKeys.splice(idx, 1)
      } else {
        this.selectedKeys.push(item.key)
      }
    },
    changeSingleItem(e, item) {
      e.stopPropagation()
      e.preventDefault()
      const idx = this.targetKeys.findIndex((key) => key === item.key)
      if (idx > -1) {
        this.targetKeys.splice(idx, 1)
      } else {
        this.targetKeys.push(item.key)
      }
    },
    handleChange(targetKeys, direction, moveKeys) {
      const _selectedKeys = _.cloneDeep(this.selectedKeys)
      moveKeys.forEach((key) => {
        const idx = _selectedKeys.findIndex((selected) => selected === key)
        if (idx > -1) {
          _selectedKeys.splice(idx, 1)
        }
      })
      this.selectedKeys = _.cloneDeep(_selectedKeys)
      this.targetKeys = targetKeys
    },
    selectChange(sourceSelectedKeys, targetSelectedKeys) {
      const _selectedKeys = _.cloneDeep(this.selectedKeys)
      const list = [
        { data: sourceSelectedKeys, name: 'source' },
        { data: targetSelectedKeys, name: 'target' },
      ]
      list.forEach((item) => {
        if (!item.data.__ob__) {
          if (item.data.length) {
            item.data.forEach((key) => {
              const idx = _selectedKeys.findIndex((selected) => selected === key)
              if (idx > -1) {
              } else {
                _selectedKeys.push(key)
              }
            })
            this.selectedKeys = _.cloneDeep(_selectedKeys)
          } else {
            let _list = []
            if (item.name === 'source') {
              _list = _selectedKeys.filter((key) => this.targetKeys.includes(key))
            } else {
              _list = _selectedKeys.filter((key) => !this.targetKeys.includes(key))
            }
            this.selectedKeys = _list
          }
        }
      })
    },
  },
}
</script>

<style lang="less">
.ant-transfer-list-body-customize-wrapper {
  padding: 0 !important;
  height: 100%;
  max-height: calc(100% - 44px);
}
.ant-transfer-list-content-item {
  transition: all 0.3s;
  .ant-transfer-list-icon {
    position: absolute;
    top: 4px;
    right: 4px;
    display: none;
    &:hover {
      color: #1f78d1;
    }
  }
  &:hover .ant-transfer-list-icon {
    display: inline;
    background-color: #c0eaff;
    border-radius: 4px;
  }
}
.ant-transfer-list-content-item-selected {
  background-color: #f0faff;
}
</style>
