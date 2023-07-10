<template>
  <a-tabs id="preValueArea" v-model="activeKey" size="small" :tabBarStyle="{ borderBottom: 'none' }">
    <a-tab-pane key="define" :disabled="disabled">
      <span style="font-size:12px;" slot="tab">定义</span>
      <PreValueTag type="add" :item="[]" @add="addNewValue" :disabled="disabled">
        <template #default>
          <a-button
            :style="{ marginBottom: '10px', fontSize: '12px', padding: '1px 7px' }"
            type="primary"
            ghost
            :disabled="disabled"
            size="small"
          >
            <a-icon type="plus" />添加</a-button
          >
        </template>
      </PreValueTag>
      <draggable :list="valueList" handle=".handle" :disabled="disabled">
        <PreValueTag
          :disabled="disabled"
          v-for="(item, index) in valueList"
          :key="`${item[0]}_${index}`"
          :item="item"
          @deleteValue="deleteValue"
          @editValue="editValue"
        />
      </draggable>
    </a-tab-pane>
    <a-tab-pane key="webhook" :disabled="disabled">
      <span style="font-size:12px;" slot="tab">Webhook</span>
      <a-form-model :model="form">
        <a-row :gutter="24">
          <a-col :span="24">
            <a-form-model-item label="地址" prop="url" :labelCol="{ span: 3 }" :wrapperCol="{ span: 16 }">
              <a-input v-model="form.url" :disabled="disabled">
                <a-select
                  :showArrow="false"
                  slot="addonBefore"
                  style="width:60px;"
                  v-model="form.method"
                  :disabled="disabled"
                >
                  <a-select-option value="get">
                    GET
                  </a-select-option>
                  <a-select-option value="post">
                    POST
                  </a-select-option>
                  <a-select-option value="put">
                    PUT
                  </a-select-option>
                </a-select>
              </a-input>
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-col :span="24">
          <a-form-model-item prop="ret_key" :labelCol="{ span: 3 }" :wrapperCol="{ span: 18 }">
            <template slot="label">
              <span
                style="position:relative;white-space:pre;"
              >{{ `过滤` }}
                <a-tooltip
                  title="返回的结果按字段来过滤，层级嵌套用##分隔，比如k1##k2，web请求返回{k1: [{k2: 1}, {k2: 2}]}, 解析结果为[1, 2]"
                >
                  <a-icon
                    style="position:absolute;top:3px;left:-17px;color:#2f54eb;"
                    type="question-circle"
                    theme="filled"
                  />
                </a-tooltip>
              </span>
            </template>
            <a-input style="width:150px;" v-model="form.ret_key" placeholder="k1##k2" :disabled="disabled" />
          </a-form-model-item>
        </a-col>
      </a-form-model>
    </a-tab-pane>
  </a-tabs>
</template>

<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import PreValueTag from './preValueTag.vue'
import { defautValueColor } from '../../utils/const'
import ColorPicker from '../../components/colorPicker/index.vue'

export default {
  name: 'PreValueArea',
  components: { draggable, PreValueTag, ColorPicker },
  props: {
    disabled: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      defautValueColor,
      activeKey: 'define', // define webhook
      valueList: [],
      form: {
        url: '',
        method: 'get',
        ret_key: '',
      },
    }
  },
  watch: {
    disabled: {
      immediate: false,
      handler(newValue) {
        const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
        if (newValue) {
          // 如果是disabled 把tab 的ink-bar也置灰
          dom.style.backgroundColor = '#00000040'
        } else {
          dom.style.backgroundColor = '#2f54eb'
        }
      },
    },
  },
  methods: {
    addNewValue(newValue, newStyle, newIcon) {
      if (newValue) {
        const idx = this.valueList.findIndex((v) => v[0] === newValue)
        if (idx > -1) {
          this.$message.warning('当前值已存在！')
        } else {
          this.valueList.push([newValue, { style: newStyle, icon: { ...newIcon } }])
        }
      }
    },
    deleteValue(item) {
      const _valueList = _.cloneDeep(this.valueList)
      const idx = _valueList.findIndex((v) => v[0] === item[0])
      if (idx > -1) {
        _valueList.splice(idx, 1)
        this.valueList = _valueList
      }
    },
    editValue(item, newValue, newStyle, newIcon) {
      const _valueList = _.cloneDeep(this.valueList)
      const idx = _valueList.findIndex((v) => v[0] === item[0])
      if (idx > -1) {
        _valueList[idx] = [newValue, { style: newStyle, icon: { ...newIcon } }]
        this.valueList = _valueList
      }
    },
    getData() {
      if (this.activeKey === 'define') {
        return {
          choice_value: this.valueList,
          choice_web_hook: null,
        }
      } else {
        return { choice_value: [], choice_web_hook: this.form }
      }
    },
    setData({ choice_value, choice_web_hook }) {
      if (choice_web_hook) {
        this.form = choice_web_hook
        this.activeKey = 'webhook'
      } else {
        this.valueList = choice_value
        this.activeKey = 'define'
      }
      const dom = document.querySelector('#preValueArea .ant-tabs-ink-bar')
      if (this.disabled) {
        // 如果是disabled 把tab 的ink-bar也置灰
        dom.style.backgroundColor = '#00000040'
      } else {
        dom.style.backgroundColor = '#2f54eb'
      }
    },
  },
}
</script>

<style lang="less" scoped>
.pre-value-edit-color {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-wrap: wrap;
  .pre-value-edit-color-item {
    cursor: pointer;
    display: inline-block;
    width: 25px;
    height: 20px;
    margin: 5px;
  }
}
</style>
