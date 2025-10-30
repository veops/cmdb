<template>
  <span :id="`ci-detail-attr-${attr.name}`">
    <span v-if="!isEdit || attr.value_type === '6'">
      <template v-if="attr.is_reference" >
        <a
          v-for="(ciId) in (attr.is_list ? ci[attr.name] : [ci[attr.name]])"
          :key="ciId"
          :href="`/cmdb/cidetail/${attr.reference_type_id}/${ciId}`"
          target="_blank"
        >
          {{ attr.referenceShowAttrNameMap ? attr.referenceShowAttrNameMap[ciId] || ciId : ciId }}
        </a>
      </template>
      <PasswordField
        :style="{ display: 'inline-block' }"
        v-else-if="attr.is_password && ci[attr.name]"
        :ci_id="ci._id"
        :attr_id="attr.id"
      ></PasswordField>
      <a-tooltip
        v-else-if="attr.value_type === '6'"
        :title="JSON.stringify(ci[attr.name] || {})"
        overlayClassName="ci-detail-attr-json-tooltip"
      >
        <span class="ci-detail-attr-json">
          {{ JSON.stringify(ci[attr.name] || {}) }}
        </span>
      </a-tooltip>
      <template v-else-if="attr.is_choice">
        <template v-if="attr.is_list">
          <span
            v-for="value in ci[attr.name]"
            :key="value"
            :style="{
              borderRadius: '4px',
              padding: '1px 0',
              margin: '0 2px',
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
            {{ getChoiceValueLabel(attr, value) || value }}</span
          >
        </template>
        <span
          v-else
          :style="{
            borderRadius: '4px',
            padding: '1px 0',
            margin: '0',
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
          {{ getChoiceValueLabel(attr, ci[attr.name]) || ci[attr.name] }}
        </span>
      </template>
      <template v-else-if="attr.is_list">
        <span> {{ ci[attr.name] && Array.isArray(ci[attr.name]) ? ci[attr.name].join(',') : ci[attr.name] }}</span>
      </template>
      <template v-else>{{ getName(ci[attr.name]) }}</template>
    </span>
    <template v-else>
      <a-form :form="form">
        <a-form-item label="" :colon="false">
          <CIReferenceAttr
            v-if="attr.is_reference"
            :referenceTypeId="attr.reference_type_id"
            :isList="attr.is_list"
            :referenceShowAttrName="attr.showAttrName"
            :initSelectOption="getInitReferenceSelectOption(attr)"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required, message: $t('placeholder2') + `${attr.alias || attr.name}` }],
              }
            ]"
          />
          <a-switch
            v-else-if="attr.is_bool"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
                valuePropName: 'checked',
              }
            ]"
          />
          <a-select
            :style="{ width: '200px' }"
            v-decorator="[
              attr.name,
              {
                rules: [{ required: attr.is_required }],
              },
            ]"
            :placeholder="$t('placeholder2')"
            v-else-if="attr.is_choice"
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
                {{ choice[1] ? choice[1].label || choice[0] : choice[0] }}
              </span>
            </a-select-option>
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
            v-else-if="(attr.value_type === '0' || attr.value_type === '1') && !attr.is_list"
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
            v-else-if="(attr.value_type === '4' || attr.value_type === '3') && !attr.is_list"
            :showTime="attr.value_type === '4' ? false : { format: 'HH:mm:ss' }"
          />
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
    <a v-if="!isEdit && !attr.is_computed && !attr.sys_computed && showEdit" @click="handleEdit" :style="{ opacity: 0 }"><a-icon type="edit"/></a>
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
import CIReferenceAttr from '@/components/ciReferenceAttr/index.vue'

export default {
  name: 'CiDetailAttrContent',
  components: { JsonEditor, PasswordField, CIReferenceAttr },
  props: {
    ci: {
      type: Object,
      default: () => {},
    },
    attr: {
      type: Object,
      default: () => {},
    },
    showEdit: {
      type: Boolean,
      default: true
    }
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
        if (this.attr.is_list && !this.attr.is_choice && !this.attr.is_reference) {
          this.form.setFieldsValue({
            [`${this.attr.name}`]: Array.isArray(this.ci[this.attr.name])
              ? this.ci[this.attr.name].join(',')
              : this.ci[this.attr.name],
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
        await updateCI(this.ci._id, { [`${this.attr.name}`]: newData ?? null })
          .then(() => {
            this.$message.success(this.$t('updateSuccess'))
            this.$emit('updateCIByself', { [`${this.attr.name}`]: newData }, this.attr.name)

            if (this.attr.is_reference) {
              this.$emit('refreshReferenceAttr')
            }
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
            this.$message.success(this.$t('updateSuccess'))
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

    getChoiceValueLabel(col, colValue) {
      const _find = col.choice_value.find((item) => String(item[0]) === String(colValue))
      if (_find) {
        return _find[1]?.label || ''
      }
      return ''
    },

    getName(name) {
      return name ?? ''
    },

    getInitReferenceSelectOption(attr) {
      const option = Object.keys(attr?.referenceShowAttrNameMap || {}).map((key) => {
        return {
          key: Number(key),
          title: attr?.referenceShowAttrNameMap?.[key] ?? ''
        }
      })
      return option
    }
  },
}
</script>

<style lang="less" scoped>
.ci-detail-attr-json {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>

<style lang="less">
.ci-detail-attr-json-tooltip {

  .ant-tooltip-content {
    max-height: 300px;
    overflow-y: auto;
  }
}
</style>
