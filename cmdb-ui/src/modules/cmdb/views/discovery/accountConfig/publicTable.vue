<template>
  <div class="table-wrap">
    <div @click="addItem" class="add-btn" v-if="configData.length === 0">
      <a-icon class="add-btn-icon" type="plus-circle" theme="twoTone" />
      <span class="add-btn-text">{{ $t('cmdb.ad.addConfig') }}</span>
    </div>
    <template v-else>
      <ops-table
        :data="configData"
        size="mini"
        show-overflow
        show-header-overflow
        :row-config="{ height: 42 }"
        :min-height="78"
      >
        <vxe-column width="170" :title="$t('name')">
          <template #header="{ column }">
            <span class="column-header-required">*</span>
            {{ column.title }}
          </template>
          <template #default="{ row }">
            <a-input v-model="row.name"></a-input>
          </template>
        </vxe-column>
        <vxe-column width="300" title="key">
          <template #header="{ column }">
            <span class="column-header-required">*</span>
            {{ column.title }}
          </template>
          <template #default="{ row }">
            <a-input-password v-model="row.key"></a-input-password>
          </template>
        </vxe-column>
        <vxe-column width="300" title="secret">
          <template #default="{ row }">
            <a-input-password v-model="row.secret"></a-input-password>
          </template>
        </vxe-column>
      </ops-table>
      <div class="actions">
        <div
          v-for="(item, index) in configData"
          :key="item.client_id"
          class="actions-item"
        >
          <a-icon
            type="minus-circle"
            class="actions-item-btn"
            @click="deleteItem(index)"
          />
          <a-icon
            type="plus-circle"
            class="actions-item-btn"
            @click="addItem"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import { defaultConfig } from './constants.js'

export default {
  name: 'PublicTable',
  data() {
    return {
      configData: []
    }
  },
  methods: {
    setData(data = []) {
      this.configData = data.map((item) => {
        return {
          ...item,
          client_id: uuidv4()
        }
      })
    },
    getData() {
      let isError = false
      const keyArr = ['name', 'key', 'secret', 'id']
      const data = this.configData.map((item) => {
        const pickData = _.pickBy(item, (v, k) => {
          return keyArr.includes(k) && v
        })

        return pickData
      })

      const errMsg = {
        name: this.$t('name'),
        key: 'key'
      }

      let errKey
      for (let i = 0; i < data.length && !errKey; i++) {
        const item = data[i]
        const curErrKey = keyArr.find((key) => !item?.[key] && errMsg?.[key])
        if (curErrKey) {
          errKey = curErrKey
        }
      }

      if (errKey) {
        isError = true
        this.$message.error(`${this.$t('placeholder1')} ${errMsg[errKey]}`)
      }

      return {
        isError,
        data
      }
    },
    deleteItem(index) {
      this.configData.splice(index, 1)
    },
    addItem() {
      this.configData.push({
        name: `${this.$t('cmdb.ad.defaultName')}${this.configData.length + 1}`,
        ...defaultConfig['public']
      })
    }
  }
}
</script>

<style lang="less" scoped>
.table-wrap {
  display: flex;

  .add-btn {
    padding: 5px 12px;
    cursor: pointer;
    border-radius: 1px;
    border: 1px solid #B1C9FF;
    background-color: #F4F9FF;
    display: flex;
    align-items: center;
    justify-content: center;

    &-icon {
      font-size: 12px;
    }

    &-text {
      font-size: 12px;
      font-weight: 400;
      color: #2F54EB;
      margin-left: 6px;
    }
  }

  .column-header-required {
    color: #FD4C6A;
  }

  .actions {
    padding-top: 36px;
    margin-left: 16px;

    &-item {
      height: 42px;
      display: flex;
      align-items: center;
      gap: 12px;

      &-btn {
        cursor: pointer;
        color: #2f54eb;
      }
    }
  }
}
</style>
