<template>
  <a-tabs type="card" class="ops-tab" v-model="activeKey" @change="changeActiveKey">
    <a-tab-pane v-for="item in authList" :key="item.value">
      <span slot="tab">
        {{ item.label }}
        <a-icon
          v-if="enable_list.find((en) => en.auth_type === item.value)"
          type="check-circle"
          theme="filled"
          style="color:#2f54eb"
        />
      </span>
      <div class="setting-auth">
        <components :ref="item.value" :is="item.value === 'OIDC' ? 'OAUTH2' : item.value" :data_type="item.value" />
        <div class="setting-auth-operation">
          <a-space>
            <a-button :loading="loading" type="primary" @click="handleSave">保存</a-button>
            <a-button :loading="loading" @click="handleReset">重置</a-button>
          </a-space>
        </div>
      </div>
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import _ from 'lodash'
import LDAP from './ldap.vue'
import CAS from './cas.vue'
import AuthCommonConfig from './common.vue'
import OAUTH2 from './oauth2.vue'
import { getAuthData, postAuthData, putAuthData, getAuthDataEnable } from '@/api/auth'
export default {
  name: 'Auth',
  components: { LDAP, CAS, AuthCommonConfig, OAUTH2 },
  data() {
    const authList = [
      {
        value: 'LDAP',
        label: 'LDAP',
      },
      {
        value: 'CAS',
        label: 'CAS',
      },
      {
        value: 'OAUTH2',
        label: 'OAUTH2',
      },
      {
        value: 'OIDC',
        label: 'OIDC',
      },
      {
        value: 'AuthCommonConfig',
        label: '通用',
      },
    ]
    return {
      authList,
      activeKey: 'LDAP',
      dataTypeId: null,
      loading: false,
      enable_list: [],
    }
  },
  mounted() {
    this.changeActiveKey()
    this.getAuthDataEnable()
  },
  methods: {
    getAuthDataEnable() {
      getAuthDataEnable().then((res) => {
        this.enable_list = res.enable_list
      })
    },
    changeActiveKey() {
      getAuthData(this.activeKey).then((res) => {
       const _res = _.cloneDeep(res)
        this.$refs[this.activeKey][0].setData(_res?.data ?? null)
        if (_res && JSON.stringify(_res) !== '{}') {
          this.dataTypeId = _res.id
        } else {
          this.dataTypeId = null
        }
      })
    },
    handleSave() {
      this.$refs[this.activeKey][0].getData(async (data) => {
        this.loading = true
        if (this.dataTypeId) {
          await putAuthData(this.activeKey, this.dataTypeId, { data }).finally(() => {
            this.loading = false
          })
        } else {
          await postAuthData(this.activeKey, { data }).finally(() => {
            this.loading = false
          })
        }
        this.$message.success('保存成功')
        this.changeActiveKey()
        this.getAuthDataEnable()
      })
    },
    handleReset() {
      this.changeActiveKey()
    },
  },
}
</script>

<style lang="less" scoped>
.setting-auth {
  background-color: #fff;
  height: calc(100vh - 128px);
  overflow: auto;
  border-radius: 0 5px 5px 5px;
  padding-top: 24px;
  .setting-auth-operation {
    padding: 0 100px 24px 100px;
    text-align: right;
  }
}
</style>

<style lang="less">
.setting-auth {
  .jsoneditor-outer {
    height: var(--custom-height) !important;
    border: 1px solid #2f54eb;
  }
  div.jsoneditor-menu {
    background-color: #2f54eb;
  }
  .jsoneditor-modes {
    display: none;
  }
}
</style>
