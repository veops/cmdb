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
      <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
      <a-button type="primary" @click="createInstance">{{ $t('submit') }}</a-button>
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
      <template v-if="parentsType && parentsType.length">
        <a-divider style="font-size:14px;margin:14px 0;font-weight:700;">{{ $t('cmdb.menu.citypeRelation') }}</a-divider>
        <a-form>
          <a-row :gutter="24" align="top" type="flex">
            <a-col :span="12" v-for="item in parentsType" :key="item.id">
              <a-form-item :label="item.alias || item.name" :colon="false">
                <a-input-group compact style="width: 100%">
                  <a-select v-model="parentsForm[item.name].attr">
                    <a-select-option
                      :title="attr.alias || attr.name"
                      v-for="attr in item.attributes"
                      :key="attr.name"
                      :value="attr.name"
                    >
                      {{ attr.alias || attr.name }}
                    </a-select-option>
                  </a-select>
                  <a-input :placeholder="$t('cmdb.ci.tips1')" v-model="parentsForm[item.name].value" style="width: 50%" />
                </a-input-group>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </template>
    </template>
    <template v-if="action === 'update'">
      <a-form :form="form">
        <p>{{ $t('cmdb.ci.tips2') }}</p>
        <a-row :gutter="24" v-for="list in batchUpdateLists" :key="list.name">
          <a-col :span="11">
            <a-form-item>
              <el-select showSearch size="small" filterable v-model="list.name" :placeholder="$t('cmdb.ci.tips3')">
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
                :placeholder="$t('placeholder2')"
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
                <a-icon type="delete" />
              </a>
            </a-form-item>
          </a-col>
        </a-row>
        <a-button type="primary" ghost icon="plus" @click="handleAdd">{{ $t('cmdb.ci.newUpdateField') }}</a-button>
      </a-form>
    </template>
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
  </CustomDrawer>
</template>

<script>
import _ from 'lodash'
import moment from 'moment'
import { Select, Option } from 'element-ui'
import { getCIType, getCITypeGroupById } from '@/modules/cmdb/api/CIType'
import { addCI } from '@/modules/cmdb/api/ci'
import JsonEditor from '../../../components/JsonEditor/jsonEditor.vue'
import { valueTypeMap } from '../../../utils/const'
import CreateInstanceFormByGroup from './createInstanceFormByGroup.vue'
import { getCITypeParent, getCanEditByParentIdChildId } from '@/modules/cmdb/api/CITypeRelation'

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
      action: '',
      form: this.$form.createForm(this),
      visible: false,
      attributeList: [],

      CIType: {},

      batchUpdateLists: [],
      editAttr: null,
      attributesByGroup: [],
      parentsType: [],
      parentsForm: {},
      canEdit: {},
    }
  },
  computed: {
    title() {
      return this.action === 'create' ? this.$t('create') + ' ' : this.$t('cmdb.ci.batchUpdate') + ' '
    },
    typeId() {
      if (this.typeIdFromRelation) {
        return this.typeIdFromRelation
      }
      return this.$router.currentRoute.meta.typeId
    },
    valueTypeMap() {
      return valueTypeMap()
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
          _attributesByGroup.push({ id: -1, name: this.$t('other'), attributes: otherGroupAttr })
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
            if (
              _tempFind.value_type === '3' &&
              values[k] &&
              Object.prototype.toString.call(values[k]) === '[object Object]'
            ) {
              values[k] = values[k].format('YYYY-MM-DD HH:mm:ss')
            }
            if (
              _tempFind.value_type === '4' &&
              values[k] &&
              Object.prototype.toString.call(values[k]) === '[object Object]'
            ) {
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
          if (
            _tempFind.value_type === '3' &&
            values[k] &&
            Object.prototype.toString.call(values[k]) === '[object Object]'
          ) {
            values[k] = values[k].format('YYYY-MM-DD HH:mm:ss')
          }
          if (
            _tempFind.value_type === '4' &&
            values[k] &&
            Object.prototype.toString.call(values[k]) === '[object Object]'
          ) {
            values[k] = values[k].format('YYYY-MM-DD')
          }
          if (_tempFind.value_type === '6') {
            values[k] = values[k] ? JSON.parse(values[k]) : undefined
          }
        })
        values.ci_type = _this.typeId
        console.log(this.parentsForm)
        Object.keys(this.parentsForm).forEach((type) => {
          if (this.parentsForm[type].value) {
            values[`$${type}.${this.parentsForm[type].attr}`] = this.parentsForm[type].value
          }
        })
        addCI(values).then((res) => {
          _this.$message.success(this.$t('addSuccess'))
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
        if (action === 'create') {
          getCITypeParent(this.typeId).then(async (res) => {
            for (let i = 0; i < res.parents.length; i++) {
              await getCanEditByParentIdChildId(res.parents[i].id, this.typeId).then((p_res) => {
                this.canEdit = {
                  ..._.cloneDeep(this.canEdit),
                  [res.parents[i].id]: p_res.result,
                }
              })
            }
            this.parentsType = res.parents.filter((parent) => this.canEdit[parent.id])
            const _parentsForm = {}
            res.parents.forEach((item) => {
              const _find = item.attributes.find((attr) => attr.id === item.unique_id)
              _parentsForm[item.name] = { attr: _find.name, value: '' }
            })
            this.parentsForm = _parentsForm
          })
        }
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
          return this.valueTypeMap[_find.value_type]
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
