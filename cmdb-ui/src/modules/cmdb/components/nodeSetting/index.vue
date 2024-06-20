<template>
  <div class="node-setting-wrap">
    <a-row v-for="(node) in nodes" :key="node.id">
      <a-col :span="6">
        <a-form-item :label="$t('cmdb.ciType.nodeSettingIp')">
          <a-input
            allowClear
            v-decorator="[
              `node_ip_${node.id}`,
              {
                rules: [
                  { required: false, message: $t('cmdb.ciType.nodeSettingIpTip') },
                  {
                    pattern:
                      '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                    message: $t('cmdb.ciType.nodeSettingIpTip1'),
                    trigger: 'blur',
                  },
                ],
              },
            ]"
            :placeholder="$t('cmdb.ciType.nodeSettingIpTip')"
          />
        </a-form-item>
      </a-col>

      <a-col :span="6">
        <a-form-item :label="$t('cmdb.ciType.nodeSettingCommunity')">
          <a-input
            allowClear
            v-decorator="[
              `node_community_${node.id}`,
              {
                rules: [{ required: false, message: $t('cmdb.ciType.nodeSettingCommunityTip') }],
              },
            ]"
            :placeholder="$t('cmdb.ciType.nodeSettingCommunityTip')"
          />
        </a-form-item>
      </a-col>

      <a-col :span="5">
        <a-form-item :label="$t('cmdb.ciType.nodeSettingVersion')">
          <a-select
            v-decorator="[
              `node_version_${node.id}`,
              {
                rules: [{ required: false, message: $t('cmdb.ciType.nodeSettingVersionTip') }],
              },
            ]"
            :placeholder="$t('cmdb.ciType.nodeSettingVersionTip')"
            allowClear
            class="node-setting-select"
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
        <div class="action">
          <a @click="() => copyNode(node.id)">
            <a-icon type="copy" />
          </a>
          <a @click="() => removeNode(node.id, 1)">
            <a-icon type="minus-circle" />
          </a>
          <a @click="addNode">
            <a-icon type="plus-circle" />
          </a>
        </div>
      </a-col>
    </a-row>
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
    copyNode(id) {
      const newNode = {
        id: uuidv4(),
        ip: this.form.getFieldValue(`node_ip_${id}`),
        community: this.form.getFieldValue(`node_community_${id}`),
        version: this.form.getFieldValue(`node_version_${id}`),
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

<style lang="less" scoped>
.node-setting-wrap {
  margin-left: 17px;

  .ant-row {
    // display: flex;

    /deep/ .ant-input-clear-icon {
      color: rgba(0,0,0,.25);

      &:hover {
        color: rgba(0, 0, 0, 0.45);
      }
    }
  }

  .node-setting-select {
    width: 150px;
  }
}

.action {
  height: 36px;
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
