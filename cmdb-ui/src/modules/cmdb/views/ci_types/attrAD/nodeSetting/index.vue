<template>
  <a-form-item
    :labelCol="labelCol"
    :wrapperCol="{ span: 18 }"
  >
    <span slot="label">
      {{ $t('cmdb.ciType.nodeList') }}
      <a-tooltip :title="$t('cmdb.ciType.snmpFormTip1')">
        <a-icon type="question-circle" />
      </a-tooltip>
    </span>
    <div class="node-setting-wrap">
      <ops-table
        :data="nodes"
        size="mini"
        show-header-overflow
        :row-config="{ height: 42 }"
        border
        :min-height="78"
      >
        <vxe-column width="170" :title="$t('cmdb.ciType.nodeSettingIp')">
          <template #default="{ row }">
            <a-input v-model="row.ip"></a-input>
          </template>
        </vxe-column>
        <vxe-column width="170" :title="$t('cmdb.ciType.nodeSettingCommunity')">
          <template #default="{ row }">
            <a-input v-model="row.community"></a-input>
          </template>
        </vxe-column>
        <vxe-column width="170" :title="$t('cmdb.ciType.nodeSettingVersion')">
          <template #default="{ row }">
            <a-select
              v-model="row.version"
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
            </a-select>
          </template>
        </vxe-column>
        <vxe-column min-wdith="90">
          <template #default="{ row }">
            <div class="action">
              <a @click="() => copyNode(row.id)">
                <a-icon type="copy" />
              </a>
              <a @click="() => removeNode(row.id, 1)">
                <a-icon type="minus-circle" />
              </a>
              <a @click="addNode">
                <a-icon type="plus-circle" />
              </a>
            </div>
          </template>
        </vxe-column>
      </ops-table>
    </div>
  </a-form-item>
</template>

<script>
import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'MonitorNodeSetting',
  inject: ['provide_labelCol'],
  props: {
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
  computed: {
    labelCol() {
      return this.provide_labelCol()
    }
  },
  methods: {
    initNodesFunc(nodes) {
      this.nodes = _.cloneDeep(nodes)
    },
    addNode() {
      const newNode = {
        id: uuidv4(),
        ip: '',
        community: 'public',
        version: '',
      }
      this.nodes.push(newNode)
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
      const copyNode = this.nodes.find((item) => item.id === id)
      if (copyNode) {
        const newNode = {
          ...copyNode,
          id: uuidv4(),
        }
        this.nodes.push(newNode)
      }
    },

    getNodeValue() {
      const nodes = this.nodes.map((node) => {
        return _.pick(node, ['ip', 'community', 'version'])
      })
      return nodes
    },
  },
}
</script>

<style lang="less" scoped>
.node-setting-wrap {
  max-width: 600px;

  .ant-row {
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
