<template>
  <CustomDrawer
    :title="title + CIType.alias"
    width="800"
    @close="handleClose"
    :maskClosable="false"
    :visible="visible"
    wrapClassName="create-instance-form"
    :bodyStyle="{ paddingTop: 0 }"
    :headerStyle="{ borderBottom: 'none' }"
  >
    <div class="custom-drawer-bottom-action">
      <a-button @click="handleClose">取消</a-button>
      <a-button type="primary" @click="createInstance">提交</a-button>
    </div>
    <template v-if="action === 'create'">
      <template v-for="group in attributesByGroup">
        <CreateInstanceFormByGroup
          :ref="`createInstanceFormByGroup_${group.id}`"
          :key="group.id || group.name"
          :group="group"
          @handleFocusInput="handleFocusInput"
          :attributeList="attributeList"
        />
      </template>
    </template>
    <template v-if="action === 'update'">
      <a-form :form="form">
        <p>可根据需要修改字段，当值为<strong>空</strong>时，则该字段<strong>置空</strong></p>
        <a-row :gutter="24" v-for="list in batchUpdateLists" :key="list.name">
          <a-col :span="11">
            <a-form-item>
              <el-select showSearch size="small" filterable v-model="list.name" placeholder="请选择需要修改的字段">
                <el-option
                  v-for="attr in attributeList"
                  :key="attr.name"
                  :value="attr.name"
                  :disabled="batchUpdateLists.findIndex((item) => item.name === attr.name) > -1"
                  :label="attr.alias || attr.name"
                >
                </el-option>
              </el-select>
            </a-form-item>
          </a-col>
          <a-col :span="11">
            <a-form-item>
              <a-select
                :style="{ width: '100%' }"
                v-decorator="[list.name, { rules: [{ required: false }] }]"
                placeholder="请选择"
                v-if="getFieldType(list.name).split('%%')[0] === 'select'"
                :mode="getFieldType(list.name).split('%%')[1] === 'multiple' ? 'multiple' : 'default'"
                showSearch
                allowClear
              >
                <a-select-option
                  :value="choice[0]"
                  :key="'New_' + choice + choice_idx"
                  v-for="(choice, choice_idx) in getSelectFieldOptions(list.name)"
                >
                  <span :style="choice[1] ? choice[1].style || {} : {}">
                    <ops-icon
                      :style="{ color: choice[1].icon.color }"
                      v-if="choice[1] && choice[1].icon && choice[1].icon.name"
                      :type="choice[1].icon.name"
                    />
                    {{ choice[0] }}
                  </span>
                </a-select-option>
              </a-select>
              <a-input-number
                v-decorator="[list.name, { rules: [{ required: false }] }]"
                style="width: 100%"
                v-if="getFieldType(list.name) === 'input_number'"
              />
              <a-date-picker
                v-decorator="[list.name, { rules: [{ required: false }] }]"
                style="width: 100%"
                :format="getFieldType(list.name) == 'date' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
                v-if="getFieldType(list.name) === 'date' || getFieldType(list.name) === 'datetime'"
                :showTime="getFieldType(list.name) === 'date' ? false : { format: 'HH:mm:ss' }"
              />
              <a-input
                v-if="getFieldType(list.name) === 'input'"
                @focus="(e) => handleFocusInput(e, list)"
                v-decorator="[list.name, { rules: [{ required: false }] }]"
              />
            </a-form-item>
          </a-col>
          <a-col :span="2">
            <a-form-item>
              <a :style="{ color: 'red', marginTop: '2px' }" @click="handleDelete(list.name)">
                <a-icon type="delete"/>
              </a>
            </a-form-item>
          </a-col>
        </a-row>
        <a-button type="primary" ghost icon="plus" @click="handleAdd">新增修改字段</a-button>
      </a-form>
    </template>
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
  </CustomDrawer>
</template>

<script>
import moment from 'moment'
import { Select, Option } from 'element-ui'
import { getCIType, getCITypeGroupById } from '@/modules/cmdb/api/CIType'
import { addCI } from '@/modules/cmdb/api/ci'
import JsonEditor from '../../../components/JsonEditor/jsonEditor.vue'
import { valueTypeMap } from '../../../utils/const'
import CreateInstanceFormByGroup from './createInstanceFormByGroup.vue'

export default {
  name: 'CreateInstanceForm',
  components: {
    ElSelect: Select,
    ElOption: Option,
    JsonEditor,
    CreateInstanceFormByGroup,
  },
  props: {
    typeIdFromRelation: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      valueTypeMap,
      action: '',
      form: this.$form.createForm(this),
      visible: false,
      attributeList: [],

      CIType: {},

      batchUpdateLists: [],
      editAttr: null,
      attributesByGroup: [],
    }
  },
  computed: {
    title() {
      return this.action === 'create' ? '创建 ' : '批量修改 '
    },
    typeId() {
      if (this.typeIdFromRelation) {
        return this.typeIdFromRelation
      }
      return this.$router.currentRoute.meta.typeId
    },
  },
  provide() {
    return {
      getFieldType: this.getFieldType,
    }
  },
  inject: ['attrList'],
  methods: {
    moment,
    async getCIType() {
      await getCIType(this.typeId).then((res) => {
        this.CIType = res.ci_types[0]
      })
    },
    async getAttributeList() {
      const _attrList = this.attrList()
      this.attributeList = _attrList.sort((x, y) => y.is_required - x.is_required)
      await getCITypeGroupById(this.typeId).then((res1) => {
        const _attributesByGroup = res1.map((g) => {
          g.attributes = g.attributes.filter((attr) => !attr.is_computed)
          return g
        })
        const attrHasGroupIds = []
        res1.forEach((g) => {
          const id = g.attributes.map((attr) => attr.id)
          attrHasGroupIds.push(...id)
        })
        const otherGroupAttr = this.attributeList.filter(
          (attr) => !attrHasGroupIds.includes(attr.id) && !attr.is_computed
        )
        if (otherGroupAttr.length) {
          _attributesByGroup.push({ id: -1, name: '其他', attributes: otherGroupAttr })
        }
        this.attributesByGroup = _attributesByGroup
      })
    },
    createInstance() {
      const _this = this
      if (_this.action === 'update') {
        this.form.validateFields((err, values) => {
          if (err) {
            return
          }
          Object.keys(values).forEach((k) => {
            const _tempFind = this.attributeList.find((item) => item.name === k)
            if (_tempFind.value_type === '3' && values[k]) {
              values[k] = values[k].format('YYYY-MM-DD HH:mm:ss')
            }
            if (_tempFind.value_type === '4' && values[k]) {
              values[k] = values[k].format('YYYY-MM-DD')
            }
            if (_tempFind.value_type === '6') {
              values[k] = values[k] ? JSON.parse(values[k]) : undefined
            }
          })

          _this.$emit('submit', values)
        })
      } else {
        let values = {}
        for (let i = 0; i < this.attributesByGroup.length; i++) {
          const data = this.$refs[`createInstanceFormByGroup_${this.attributesByGroup[i].id}`][0].getData()
          if (data === 'error') {
            return
          }
          values = { ...values, ...data }
        }

        Object.keys(values).forEach((k) => {
          const _tempFind = this.attributeList.find((item) => item.name === k)
          if (_tempFind.value_type === '3' && values[k]) {
            values[k] = values[k].format('YYYY-MM-DD HH:mm:ss')
          }
          if (_tempFind.value_type === '4' && values[k]) {
            values[k] = values[k].format('YYYY-MM-DD')
          }
          if (_tempFind.value_type === '6') {
            values[k] = values[k] ? JSON.parse(values[k]) : undefined
          }
        })
        values.ci_type = _this.typeId
        addCI(values).then((res) => {
          _this.$message.success('新增成功!')
          _this.visible = false
          _this.$emit('reload', { ci_id: res.ci_id })
        })
      }
    },
    handleClose() {
      this.visible = false
    },
    handleOpen(visible, action) {
      this.visible = visible
      this.action = action
      this.$nextTick(() => {
        this.form.resetFields()
        Promise.all([this.getCIType(), this.getAttributeList()]).then(() => {
          this.batchUpdateLists = [{ name: this.attributeList[0].name }]
        })
      })
    },
    getFieldType(name) {
      const _find = this.attributeList.find((item) => item.name === name)
      if (_find) {
        if (_find.is_choice) {
          if (_find.is_list) {
            return 'select%%multiple'
          }
          return 'select'
        } else if (_find.value_type === '0' || _find.value_type === '1') {
          return 'input_number'
        } else if (_find.value_type === '4' || _find.value_type === '3') {
          return valueTypeMap[_find.value_type]
        } else {
          return 'input'
        }
      }
      return 'input'
    },
    getSelectFieldOptions(name) {
      const _find = this.attributeList.find((item) => item.name === name)
      if (_find) {
        return _find.choice_value
      }
      return []
    },
    handleAdd() {
      this.batchUpdateLists.push({ name: undefined })
    },
    handleDelete(name) {
      const _idx = this.batchUpdateLists.findIndex((item) => item.name === name)
      if (_idx > -1) {
        this.batchUpdateLists.splice(_idx, 1)
      }
    },
    handleFocusInput(e, attr) {
      console.log(attr)
      const _tempFind = this.attributeList.find((item) => item.name === attr.name)
      if (_tempFind.value_type === '6') {
        this.editAttr = attr
        e.srcElement.blur()
        const jsonData = this.form.getFieldValue(attr.name)
        this.$refs.jsonEditor.open(null, null, jsonData ? JSON.parse(jsonData) : {})
      } else {
        this.editAttr = null
      }
    },
    jsonEditorOk(jsonData) {
      this.form.setFieldsValue({ [this.editAttr.name]: JSON.stringify(jsonData) })
    },
  },
}
</script>
<style lang="less">
.create-instance-form {
  .ant-form-item {
    margin-bottom: 5px;
  }
  .ant-drawer-body {
    overflow-y: auto;
    max-height: calc(100vh - 110px);
  }
}
</style>