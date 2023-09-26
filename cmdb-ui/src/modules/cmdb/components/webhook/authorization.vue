<template>
  <div class="authorization-wrapper">
    <div class="authorization-header">
      <a-space>
        <span>Authorization Type</span>
        <a-select size="small" v-model="authorizationType" style="width: 200px" :showSearch="true">
          <a-select-option value="none">
            None
          </a-select-option>
          <a-select-option value="BasicAuth">
            Basic Auth
          </a-select-option>
          <a-select-option value="Bearer">
            Bearer
          </a-select-option>
          <a-select-option value="APIKey">
            APIKey
          </a-select-option>
          <a-select-option value="OAuth2.0">
            OAuth2.0
          </a-select-option>
        </a-select>
      </a-space>
    </div>
    <div style="margin-top:10px">
      <table v-if="authorizationType === 'BasicAuth'">
        <tr>
          <td><a-input class="authorization-input" v-model="BasicAuth.username" placeholder="用户名" /></td>
        </tr>
        <tr>
          <td><a-input class="authorization-input" v-model="BasicAuth.password" placeholder="密码" /></td>
        </tr>
      </table>

      <table v-else-if="authorizationType === 'Bearer'">
        <tr>
          <td><a-input class="authorization-input" v-model="Bearer.token" placeholder="token" /></td>
        </tr>
      </table>

      <table v-else-if="authorizationType === 'APIKey'">
        <tr>
          <td><a-input class="authorization-input" v-model="APIKey.key" placeholder="key" /></td>
        </tr>
        <tr>
          <td><a-input class="authorization-input" v-model="APIKey.value" placeholder="value" /></td>
        </tr>
      </table>

      <table v-else-if="authorizationType === 'OAuth2.0'">
        <tr>
          <td><a-input class="authorization-input" v-model="OAuth2.client_id" placeholder="client_id" /></td>
        </tr>
        <tr>
          <td>
            <a-input class="authorization-input" v-model="OAuth2.client_secret" placeholder="client_secret" />
          </td>
        </tr>
        <tr>
          <td>
            <a-input
              class="authorization-input"
              v-model="OAuth2.authorization_base_url"
              placeholder="authorization_base_url"
            />
          </td>
        </tr>
        <tr>
          <td>
            <a-input class="authorization-input" v-model="OAuth2.token_url" placeholder="token_url" />
          </td>
        </tr>
        <tr>
          <td><a-input class="authorization-input" v-model="OAuth2.redirect_url" placeholder="redirect_url" /></td>
        </tr>
        <tr>
          <td>
            <a-input class="authorization-input" v-model="OAuth2.scope" placeholder="scope" />
          </td>
        </tr>
      </table>

      <a-empty
        v-else
        :image-style="{
          height: '60px',
        }"
      >
        <img slot="image" :src="require('@/assets/data_empty.png')" />
        <span slot="description"> 暂无请求认证 </span>
      </a-empty>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Authorization',
  data() {
    return {
      authorizationType: 'none',
      BasicAuth: {
        username: '',
        password: '',
      },
      Bearer: {
        token: '',
      },
      APIKey: {
        key: '',
        value: '',
      },
      OAuth2: {
        client_id: '',
        client_secret: '',
        authorization_base_url: '',
        token_url: '',
        redirect_url: '',
        scope: '',
      },
    }
  },
}
</script>

<style lang="less" scoped>
.authorization-wrapper {
  table {
    width: 100%;
    border-collapse: collapse;
  }
  table,
  td,
  th {
    border: 1px solid #f3f4f6;
  }
  .authorization-input {
    border: none;
    &:focus {
      box-shadow: none;
    }
  }
}
</style>
