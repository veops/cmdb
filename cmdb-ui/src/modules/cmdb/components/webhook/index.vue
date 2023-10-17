<template>
  <div>
    <a-input-group compact>
      <treeselect
        :disable-branch-nodes="true"
        class="custom-treeselect custom-treeselect-bgcAndBorder"
        :style="{
          '--custom-height': '30px',
          lineHeight: '30px',
          '--custom-bg-color': '#fff',
          '--custom-border': '1px solid #d9d9d9',
          display: 'inline-block',
          width: '100px',
        }"
        v-model="method"
        :multiple="false"
        :clearable="false"
        searchable
        :options="methodList"
        value-consists-of="LEAF_PRIORITY"
        placeholder="请选择方式"
      >
      </treeselect>
      <a-input :style="{ display: 'inline-block', width: 'calc(100% - 100px)' }" v-model="url" />
    </a-input-group>
    <a-tabs>
      <a-tab-pane key="Parameters" tab="Parameters">
        <Parameters ref="Parameters" />
      </a-tab-pane>
      <a-tab-pane key="Body" tab="Body" force-render>
        <Body ref="Body" />
      </a-tab-pane>
      <a-tab-pane key="Headers" tab="Headers" force-render>
        <Header ref="Header" />
      </a-tab-pane>
      <a-tab-pane key="Authorization" tab="Authorization" force-render>
        <Authorization ref="Authorization" />
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import Parameters from './paramaters.vue'
import Body from './body.vue'
import Header from './header.vue'
import Authorization from './authorization.vue'
export default {
  name: 'Webhook',
  components: { Parameters, Body, Header, Authorization },
  data() {
    const methodList = [
      {
        id: 'GET',
        label: 'GET',
      },
      {
        id: 'POST',
        label: 'POST',
      },
      {
        id: 'PUT',
        label: 'PUT',
      },
      {
        id: 'DELETE',
        label: 'DELETE',
      },
    ]
    return {
      methodList,
      method: 'GET',
      url: '',
    }
  },
  methods: {
    getParams() {
      const parameters = {}
      this.$refs.Parameters.parameters.forEach((item) => {
        parameters[item.key] = item.value
      })
      let body = this.$refs.Body.jsonData
      try {
        JSON.parse(body)
        body = JSON.parse(body)
      } catch {}
      const headers = {}
      this.$refs.Header.headers.forEach((item) => {
        headers[item.key] = item.value
      })
      let authorization = {}
      const type = this.$refs.Authorization.authorizationType
      if (type !== 'none') {
        if (type === 'OAuth2.0') {
          authorization = { ...this.$refs.Authorization['OAuth2'], type }
        } else {
          authorization = { ...this.$refs.Authorization[type], type }
        }
      }
      const { method, url } = this
      return { method, url, parameters, body, headers, authorization }
    },
    setParams(params) {
      const { method, url, parameters, body, headers, authorization = {} } = params ?? {}
      this.method = method
      this.url = url
      this.$refs.Parameters.parameters =
        Object.keys(parameters).map((key) => {
          return {
            id: uuidv4(),
            key: key,
            value: parameters[key],
          }
        }) || []
      if (body && Object.prototype.toString.call(body) === '[object Object]') {
        this.$refs.Body.jsonData = JSON.stringify(body)
      } else {
        this.$refs.Body.jsonData = body
      }
      this.$refs.Header.headers =
        Object.keys(headers).map((key) => {
          return {
            id: uuidv4(),
            key: key,
            value: headers[key],
          }
        }) || []
      const { type = 'none' } = authorization
      console.log(type)
      this.$refs.Authorization.authorizationType = type
      if (type !== 'none') {
        const _authorization = _.cloneDeep(authorization)
        delete _authorization.type
        if (type === 'OAuth2.0') {
          this.$refs.Authorization.OAuth2 = _authorization
        } else {
          this.$refs.Authorization[type] = _authorization
        }
      }
    },
  },
}
</script>

<style></style>
