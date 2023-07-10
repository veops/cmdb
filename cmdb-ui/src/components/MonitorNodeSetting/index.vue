<template>
  <div>
    <a-form-item v-for="(node, index) in nodes" :key="node.id">
      <a-row :gutter="24">
        <a-col :span="6" :offset="1">
          <a-form-item :label="index ? '' : 'ip地址'">
            <a-input
              allowClear
              size="small"
              v-decorator="[
                `node_ip_${node.id}`,
                {
                  rules: [
                    { required: false, message: '请输入ip地址' },
                    {
                      pattern:
                        '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                      message: 'ip地址格式错误',
                      trigger: 'blur',
                    },
                  ],
                },
              ]"
              placeholder="请输入ip地址"
            />
          </a-form-item>
        </a-col>

        <a-col :span="6">
          <a-form-item :label="index ? '' : 'community'" colon>
            <a-input
              allowClear
              size="small"
              v-decorator="[
                `node_community_${node.id}`,
                {
                  rules: [{ required: false, message: '请输入community' }],
                },
              ]"
              placeholder="请输入community"
            />
          </a-form-item>
        </a-col>

        <a-col :span="6">
          <a-form-item :label="index ? '' : '版本'" colon>
            <a-select
              size="small"
              v-decorator="[
                `node_version_${node.id}`,
                {
                  rules: [{ required: false, message: '请输入版本' }],
                },
              ]"
              placeholder="请选择版本"
            >
              <a-select-option value="1">
                v1
              </a-select-option>
              <a-select-option value="2c">
                v2c
              </a-select-option>
              <a-select-option value="3">
                v3
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="3">
          <a-form-item :label="index ? '' : ' '" :colon="false">
            <a @click="() => removeNode(node.id, 1)" :style="{ color: 'red' }">
              <a-icon type="delete" />
            </a>
          </a-form-item>
        </a-col>
      </a-row>
    </a-form-item>

    <a-form-item style="text-align: center">
      <a-button type="dashed" style="width: 30%;" @click="addNode">
        <a-icon type="plus" />
        添加节点
      </a-button>
    </a-form-item>
  </div>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'MonitorNodeSetting',
  props: {
    initNodes: {
      type: Array,
      default: () => [],
    },
    form: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      nodes: [],
    }
  },
  methods: {
    initNodesFunc() {
      this.nodes = _.cloneDeep(this.initNodes)
    },
    addNode() {
      const newNode = {
        id: uuidv4(),
        ip: '',
        community: '',
        version: '',
      }
      this.nodes.push(newNode)
      this.$nextTick(() => {
        this.form.setFieldsValue({
          [`node_ip_${newNode.id}`]: newNode.ip,
          [`node_community_${newNode.id}`]: newNode.community,
          [`node_version_${newNode.id}`]: newNode.version,
        })
      })
    },
    removeNode(removeId, minLength) {
      if (this.nodes.length <= minLength) {
        this.$message.error('不可再删除！')
        return
      }
      const _idx = this.nodes.findIndex((item) => item.id === removeId)
      if (_idx > -1) {
        this.nodes.splice(_idx, 1)
      }
    },
    getInfoValuesFromForm(values) {
      return this.nodes.map((item) => {
        return {
          id: item.id,
          ip: values[`node_ip_${item.id}`],
          community: values[`node_community_${item.id}`],
          version: values[`node_version_${item.id}`],
        }
      })
    },
    setNodeField() {
      if (this.nodes && this.nodes.length) {
        this.nodes.forEach((item) => {
          this.form.setFieldsValue({
            [`node_ip_${item.id}`]: item.ip,
            [`node_community_${item.id}`]: item.community,
            [`node_version_${item.id}`]: item.version,
          })
        })
      }
    },
    getNodeValue() {
      const values = this.form.getFieldsValue()
      return this.getInfoValuesFromForm(values)
    },
  },
}
</script>

<style></style>
