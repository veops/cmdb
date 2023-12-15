<template>
  <span :id="`ci-detail-attr-${attr.name}`">
    <span v-if="!isEdit || attr.value_type === '6'">
      <PasswordField
        :style="{ display: 'inline-block' }"
        v-if="attr.is_password && ci[attr.name]"
        :ci_id="ci._id"
        :attr_id="attr.id"
      ></PasswordField>
      <template v-else-if="attr.value_type === '6'">{{ JSON.stringify(ci[attr.name] || {}) }}</template>
      <template v-else-if="attr.is_choice">
        <template v-if="attr.is_list">
          <span
            v-for="value in ci[attr.name]"
            :key="value"
            :style="{
              borderRadius: '4px',
              padding: '1px 5px',
              margin: '2px',
              ...getChoiceValueStyle(attr, value),
              display: 'inline-flex',
              alignItems: 'center',
            }"
          >
            <img
              v-if="getChoiceValueIcon(attr, value).id && getChoiceValueIcon(attr, value).url"
              :src="`/api/common-setting/v1/file/${getChoiceValueIcon(attr, value).url}`"
              :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
            />
            <ops-icon
              v-else
              :style="{ color: getChoiceValueIcon(attr, value).color, marginRight: '5px' }"
              :type="getChoiceValueIcon(attr, value).name"
            />
            {{ value }}</span
          >
        </template>
        <span
          v-else
          :style="{
            borderRadius: '4px',
            padding: '1px 5px',
            margin: '2px 0',
            ...getChoiceValueStyle(attr, ci[attr.name]),
            display: 'inline-flex',
            alignItems: 'center',
          }"
        >
          <img
            v-if="getChoiceValueIcon(attr, ci[attr.name]).id && getChoiceValueIcon(attr, ci[attr.name]).url"
            :src="`/api/common-setting/v1/file/${getChoiceValueIcon(attr, ci[attr.name]).url}`"
            :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
          />
          <ops-icon
            v-else
            :style="{ color: getChoiceValueIcon(attr, ci[attr.name]).color, marginRight: '5px' }"
            :type="getChoiceValueIcon(attr, ci[attr.name]).name"
          />
          {{ ci[attr.name] }}
        </span>
      </template>
      <template v-else-if="attr.is_list">
        <span> {{ ci[attr.name].join(',') }}</span>
      </template>
      <template v-else>{{ getName(ci[attr.name]) }}</template>
    </span>
    <template v-else>
      <a-form :form="form">
        <a-form-item label="" :colon="false">
          <a-select
            :style="{ width: '100%' }"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
              },
            ]"
            placeholder="请选择"
            v-if="attr.is_choice"
            :mode="attr.is_list ? 'multiple' : 'default'"
            showSearch
            allowClear
            size="small"
            :getPopupContainer="(trigger) => trigger.parentElement"
          >
            <a-select-option
              :value="choice[0]"
              :key="'New_' + attr.name + choice_idx"
              v-for="(choice, choice_idx) in attr.choice_value"
            >
              <span :style="{ ...(choice[1] ? choice[1].style : {}), display: 'inline-flex', alignItems: 'center' }">
                <template v-if="choice[1] && choice[1].icon && choice[1].icon.name">
                  <img
                    v-if="choice[1].icon.id && choice[1].icon.url"
                    :src="`/api/common-setting/v1/file/${choice[1].icon.url}`"
                    :style="{ maxHeight: '13px', maxWidth: '13px', marginRight: '5px' }"
                  />
                  <ops-icon
                    v-else
                    :style="{ color: choice[1].icon.color, marginRight: '5px' }"
                    :type="choice[1].icon.name"
                  />
                </template>
                {{ choice[0] }}
              </span>
            </a-select-option>
          </a-select>
          <a-select
            :style="{ width: '100%' }"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
              },
            ]"
            placeholder="请选择"
            v-else-if="attr.is_list"
            mode="tags"
            showSearch
            allowClear
            size="small"
            :getPopupContainer="(trigger) => trigger.parentElement"
          >
          </a-select>
          <a-input-number
            size="small"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
              },
            ]"
            style="width: 100%"
            v-else-if="attr.value_type === '0' || attr.value_type === '1'"
          />
          <a-date-picker
            size="small"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
              },
            ]"
            style="width: 100%"
            :format="attr.value_type === '4' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
            :valueFormat="attr.value_type === '4' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:mm:ss'"
            v-else-if="attr.value_type === '4' || attr.value_type === '3'"
            :showTime="attr.value_type === '4' ? false : { format: 'HH:mm:ss' }"
          />
          <!-- <a-input
            size="small"
            @focus="(e) => handleFocusInput(e, attr)"
            v-decorator="[
              attr.name,
              {
                validateTrigger: ['submit'],
                rules: [{ required: attr.is_required }],
              },
            ]"
            style="width: 100%"
            v-else-if="attr.value_type === '6'"
          /> -->
          <a-input
            size="small"
            v-decorator="[
              attr.name,
              {
                validateTrigger: ['submit'],
                rules: [{ required: attr.is_required }],
              },
            ]"
            style="width: 100%"
            v-else
          />
        </a-form-item>
      </a-form>
    </template>
    <a v-if="!isEdit && !attr.is_computed" @click="handleEdit" :style="{ opacity: 0 }"><a-icon type="edit"/></a>
    <JsonEditor ref="jsonEditor" @jsonEditorOk="jsonEditorOk" />
  </span>
</template>

<script>
import _ from 'lodash'
import moment from 'moment'
import { updateCI } from '@/modules/cmdb/api/ci'
import JsonEditor from '../../../components/JsonEditor/jsonEditor.vue'
import PasswordField from '../../../components/passwordField/index.vue'
import { getAttrPassword } from '../../../api/CITypeAttr'

export default {
  name: 'CiDetailAttrContent',
  components: { JsonEditor, PasswordField },
  props: {
    ci: {
      type: Object,
      default: () => {},
    },
    attr: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      isEdit: false,
      form: this.$form.createForm(this, this.attr.name),
    }
  },
  mounted() {
    document.addEventListener('click', this.eventListener)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.eventListener)
  },
  methods: {
    moment,
    eventListener(e) {
      const datePickerContainer = document.getElementsByClassName('ant-calendar-picker-container')
      if (this.isEdit && !datePickerContainer.length) {
        const dom = document.getElementById(`ci-detail-attr-${this.attr.name}`)
        e.stopPropagation()
        e.preventDefault()
        if (dom) {
          const isSelf = dom.contains(e.target)
          if (!isSelf) {
            this.handleCloseEdit()
          }
        }
      }
    },
    handleEdit(e) {
      e.stopPropagation()
      e.preventDefault()
      if (this.attr.value_type === '6') {
        const jsonData = this.ci[this.attr.name]
        this.$refs.jsonEditor.open(null, null, jsonData || {})
        return
      }
      this.isEdit = true
      this.$nextTick(async () => {
        if (this.attr.is_list && !this.attr.is_choice) {
          this.form.setFieldsValue({
            [`${this.attr.name}`]: this.ci[this.attr.name]|| null,
          })
          return
        }
        if (this.attr.is_password) {
          await getAttrPassword(this.ci._id, this.attr.id).then((res) => {
            this.form.setFieldsValue({
              [`${this.attr.name}`]: res.value ?? null,
            })
          })
          return
        }
        this.form.setFieldsValue({
          [`${this.attr.name}`]: this.ci[this.attr.name] ?? null,
        })
      })
    },
    async handleCloseEdit() {
      const newData = this.form.getFieldValue(this.attr.name)
      if (!_.isEqual(this.ci[this.attr.name], newData)) {
        await updateCI(this.ci._id, { [`${this.attr.name}`]: newData })
          .then(() => {
            this.$message.success('更新成功！')
            this.$emit('updateCIByself', { [`${this.attr.name}`]: newData }, this.attr.name)
          })
          .catch(() => {
            this.$emit('refresh', this.attr.name)
          })
      }
      this.isEdit = false
    },
    // handleFocusInput(e, attr) {
    //   console.log('focus')
    //   if (this.attr.value_type === '6') {
    //     e.preventDefault()
    //     e.stopPropagation()
    //     // e.srcElement.blur()
    //     const jsonData = this.form.getFieldValue(attr.name)
    //     this.$refs.jsonEditor.open(null, null, jsonData ? JSON.parse(jsonData) : {})
    //   }
    // },
    jsonEditorOk(jsonData) {
      if (!_.isEqual(this.ci[this.attr.name], jsonData)) {
        updateCI(this.ci._id, { [`${this.attr.name}`]: jsonData })
          .then(() => {
            this.$message.success('更新成功！')
            this.$emit('updateCIByself', { [`${this.attr.name}`]: jsonData }, this.attr.name)
          })
          .catch(() => {
            this.$emit('refresh', this.attr.name)
          })
      }
    },
    getChoiceValueStyle(col, colValue) {
      const _find = col.choice_value.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.style || {}
      }
      return {}
    },
    getChoiceValueIcon(col, colValue) {
      const _find = col.choice_value.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.icon || {}
      }
      return {}
    },
    getName(name) {
      return name ?? ''
    },
  },
}
</script>

<style></style>
